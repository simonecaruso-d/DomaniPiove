# Environment Setting
import math
import numpy as np
import os
import pandas as pd
import random
from supabase import Client, create_client
import sys
import time
from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.ConfigurationWeather as Configuration

# Helpers
def NormalizeIsoDatetime(value):
    'Validate datetime is timezone-aware UTC and return ISO string; fails on naive/non-UTC values'
    if value is None: return None

    parsedValue = pd.to_datetime(value, errors='coerce')
    if pd.isna(parsedValue): raise ValueError(f'Invalid datetime value: {value}')
    if parsedValue.tzinfo is None: raise ValueError(f'Datetime value must be timezone-aware UTC, got naive value: {value}')
    if parsedValue.utcoffset() != pd.Timedelta(0): raise ValueError(f'Datetime value must already be UTC (+00:00), got: {value}')

    parsedValue = parsedValue.tz_convert('UTC')
    return parsedValue.isoformat()

def SanitizeValue(value):
    'Convert NaN/Inf and numpy scalars to database-safe python values'
    if value is None: return None
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)): return None
    if isinstance(value, np.generic): return value.item()
    if pd.isna(value): return None
    return value

def NormalizeIntegerValue(value, columnName):
    'Normalize values that must be integers (e.g. CityId), accepting 1 and 1.0 forms only'
    if value is None: return None
    value = SanitizeValue(value)
    if value is None: return None

    if isinstance(value, bool): raise ValueError(f'{columnName} must be an integer, got boolean: {value}')

    if isinstance(value, (int, np.integer)): return int(value)

    if isinstance(value, (float, np.floating)):
        if float(value).is_integer(): return int(value)
        raise ValueError(f'{columnName} must be an integer, got non-integer float: {value}')

    if isinstance(value, str):
        cleanValue = value.strip()
        if cleanValue == '': return None
        try: numericValue = float(cleanValue)
        except ValueError as parseError: raise ValueError(f'{columnName} must be an integer, got: {value}') from parseError
        if numericValue.is_integer(): return int(numericValue)
        raise ValueError(f'{columnName} must be an integer, got non-integer string: {value}')

    raise ValueError(f'{columnName} must be an integer, got unsupported type: {type(value).__name__}')

def ExecuteWithRetry(operationFactory, operationDescription, maxRetries=Configuration.MaxRetries, baseRetryDelaySeconds=Configuration.BaseRetryDelaySeconds, jitterSeconds=Configuration.JitterSeconds):
    'Execute a Supabase operation with retry and exponential backoff'
    lastException = None

    for attempt in range(1, maxRetries + 1):
        try: return operationFactory()
        except Exception as requestError:
            lastException = requestError
            if attempt < maxRetries:
                sleepSeconds = baseRetryDelaySeconds * (2 ** (attempt - 1))
                sleepSeconds += random.uniform(0, max(0.0, jitterSeconds))
                time.sleep(sleepSeconds)

    raise RuntimeError(f'{operationDescription} failed after {maxRetries} attempts') from lastException

def ChunkValues(values, chunkSize=200):
    'Yield list chunks to keep query size bounded'
    for index in range(0, len(values), chunkSize): yield values[index:index + chunkSize]

def NormalizeMetricName(value, maxLength=20):
    'Normalize metric names to DB-safe labels and validate max length'
    if value is None: return None

    normalizedValue = Configuration.DbSafeMetricNameMap.get(str(value), str(value))
    if len(normalizedValue) > maxLength: raise ValueError(f"Metric value '{normalizedValue}' exceeds max length {maxLength}")
    return normalizedValue

def PrepareAccuracyDataFrame(dataFrame, metricColumn='Metric', maxMetricLength=20):
    'Return a copy with metric names normalized for accuracy tables'
    preparedDataFrame = dataFrame.copy()
    if metricColumn in preparedDataFrame.columns:
        preparedDataFrame[metricColumn] = preparedDataFrame[metricColumn].map(lambda value: NormalizeMetricName(value, maxMetricLength))
    return preparedDataFrame

def PrepareRecordsForInsert(dataFrame, datetimeColumns, integerColumns=None):
    'Prepare DataFrame rows for Supabase insert, sanitizing values and datetimes'
    if integerColumns is None: integerColumns = set()

    preparedData = dataFrame.copy()
    preparedData = preparedData.replace([np.inf, -np.inf], np.nan)
    preparedData = preparedData.where(~preparedData.isna(), None)

    records = []
    for record in preparedData.to_dict('records'):
        cleanRecord = {}
        for columnName, columnValue in record.items():
            if columnName in datetimeColumns: columnValue = NormalizeIsoDatetime(columnValue)
            if columnName in integerColumns : columnValue = NormalizeIntegerValue(columnValue, columnName)
            cleanRecord[columnName] = SanitizeValue(columnValue)
        records.append(cleanRecord)

    return records

def InsertInBatches(supabaseClient, tableName, records, batchSize, progressDescription):
    'Insert records in fixed-size batches'
    insertedRows = 0
    for index in tqdm(range(0, len(records), batchSize), desc=progressDescription):
        batch = records[index:index + batchSize]
        ExecuteWithRetry(lambda batch=batch: supabaseClient.table(tableName).insert(batch).execute(), f'Insert batch in {tableName}')
        insertedRows += len(batch)

    return insertedRows

# Supabase Writing
def WriteForecastToSupabase(forecastDf, supabaseUrl=Configuration.SupabaseUrl, supabaseKey=Configuration.SupabaseKey, batchSize=Configuration.WriteBatchSize, tableName='Forecast'):
    'Fake SCD Type2: mark previous rows as not current on overlap, then insert incoming rows'
    if forecastDf is None or forecastDf.empty: return {'RowsMarkedNotCurrent': 0, 'RowsInserted': 0}

    try:
        supabaseClient: Client = create_client(supabaseUrl, supabaseKey)

        uniqueCombinations             = forecastDf[['Provider', 'Datetime', 'CityId']].drop_duplicates().copy()
        uniqueCombinations['Datetime'] = uniqueCombinations['Datetime'].map(NormalizeIsoDatetime)
        groupedKeys                    = uniqueCombinations.groupby(['Provider', 'CityId'])['Datetime'].agg(lambda values: sorted(set(values)))

        rowsMarkedNotCurrent = 0
        for (provider, cityId), datetimeValues in tqdm(groupedKeys.items(), total=len(groupedKeys), desc='Forecast | Mark previous as N'):
            updatedAtValue = pd.Timestamp.now(tz='UTC').isoformat()
            for datetimeChunk in ChunkValues(datetimeValues):
                ExecuteWithRetry(lambda provider=provider, cityId=cityId, datetimeChunk=datetimeChunk, updatedAtValue=updatedAtValue:
                                 (supabaseClient.table(tableName).update({'IsCurrent': 'N', 'UpdatedAt': updatedAtValue}).eq('Provider', provider).eq('CityId', int(cityId)).in_('Datetime', datetimeChunk).execute()),
                                 f'Forecast overlap update for Provider={provider}, CityId={int(cityId)}')

            rowsMarkedNotCurrent += len(datetimeValues)

        dataToInsert = forecastDf.copy()
        records      = PrepareRecordsForInsert(dataToInsert, {'RetrievalDatetime', 'Datetime'}, {'CityId'})
        rowsInserted = InsertInBatches(supabaseClient, tableName, records, batchSize, 'Forecast | Insert rows')

        return {'RowsMarkedNotCurrent': rowsMarkedNotCurrent, 'RowsInserted': rowsInserted}

    except Exception as writeError: raise RuntimeError(f'Error writing Forecast to Supabase: {writeError}') from writeError

def WriteActualToSupabase(actualDf, supabaseUrl=Configuration.SupabaseUrl, supabaseKey=Configuration.SupabaseKey, batchSize=Configuration.WriteBatchSize, tableName='Actual'):
    'SCD Type1 on overlap: delete existing rows by (Datetime, CityId), then insert incoming rows'
    if actualDf is None or actualDf.empty: return {'RowsDeletedForOverlap': 0, 'RowsInserted': 0}

    try:
        supabaseClient: Client = create_client(supabaseUrl, supabaseKey)

        uniqueCombinations             = actualDf[['Datetime', 'CityId']].drop_duplicates().copy()
        uniqueCombinations['Datetime'] = uniqueCombinations['Datetime'].map(NormalizeIsoDatetime)
        groupedKeys                    = uniqueCombinations.groupby(['CityId'])['Datetime'].agg(lambda values: sorted(set(values)))

        rowsDeletedForOverlap = 0
        for cityId, datetimeValues in tqdm(groupedKeys.items(), total=len(groupedKeys), desc='Actual | Delete overlaps'):
            for datetimeChunk in ChunkValues(datetimeValues):
                ExecuteWithRetry(lambda cityId=cityId, datetimeChunk=datetimeChunk:
                                 (supabaseClient.table(tableName).delete().eq('CityId', int(cityId)).in_('Datetime', datetimeChunk).execute()),
                                 f'Actual overlap delete for CityId={int(cityId)}')

            rowsDeletedForOverlap += len(datetimeValues)

        records      = PrepareRecordsForInsert(actualDf, {'RetrievalDatetime', 'Datetime'}, {'CityId'})
        rowsInserted = InsertInBatches(supabaseClient, tableName, records, batchSize, 'Actual | Insert rows')

        return {'RowsDeletedForOverlap': rowsDeletedForOverlap, 'RowsInserted': rowsInserted}

    except Exception as writeError: raise RuntimeError(f'Error writing Actual to Supabase: {writeError}') from writeError

def WriteForecastAccuracyByDaySpanToSupabase(byDaySpanDf, supabaseUrl=Configuration.SupabaseUrl, supabaseKey=Configuration.SupabaseKey,
                                             batchSize=Configuration.WriteBatchSize, tableName='ForecastAccuracyByDaySpan'):
    'SCD Type1 on overlap: delete existing rows by (Provider, Metric, DaySpan), then insert incoming rows'
    if byDaySpanDf is None or byDaySpanDf.empty: return {'RowsDeletedForOverlap': 0, 'RowsInserted': 0}

    try:
        supabaseClient: Client = create_client(supabaseUrl, supabaseKey)

        preparedByDaySpanDf           = PrepareAccuracyDataFrame(byDaySpanDf, maxMetricLength=20)
        uniqueCombinations            = preparedByDaySpanDf[['Provider', 'Metric', 'DaySpan']].drop_duplicates().copy()
        uniqueCombinations['DaySpan'] = uniqueCombinations['DaySpan'].map(lambda value: NormalizeIntegerValue(value, 'DaySpan'))
        groupedKeys                   = uniqueCombinations.groupby(['Provider', 'Metric'])['DaySpan'].agg(lambda values: sorted(set(values)))

        rowsDeletedForOverlap = 0
        for (provider, metric), daySpanValues in tqdm(groupedKeys.items(), total=len(groupedKeys), desc='ForecastAccuracyByDaySpan | Delete overlaps'):
            for daySpanChunk in ChunkValues(daySpanValues):
                ExecuteWithRetry(lambda provider=provider, metric=metric, daySpanChunk=daySpanChunk:
                                 (supabaseClient.table(tableName).delete().eq('Provider', provider).eq('Metric', metric).in_('DaySpan', daySpanChunk).execute()),
                                 f'ForecastAccuracyByDaySpan overlap delete for Provider={provider}, Metric={metric}')

            rowsDeletedForOverlap += len(daySpanValues)

        records      = PrepareRecordsForInsert(preparedByDaySpanDf, set(), {'DaySpan'})
        rowsInserted = InsertInBatches(supabaseClient, tableName, records, batchSize, 'ForecastAccuracyByDaySpan | Insert rows')

        return {'RowsDeletedForOverlap': rowsDeletedForOverlap, 'RowsInserted': rowsInserted}

    except Exception as writeError: raise RuntimeError(f'Error writing ForecastAccuracyByDaySpan to Supabase: {writeError}') from writeError

def WriteForecastAccuracyByProviderToSupabase(byProviderDf, supabaseUrl=Configuration.SupabaseUrl, supabaseKey=Configuration.SupabaseKey,
                                    batchSize=Configuration.WriteBatchSize, tableName='ForecastAccuracyByProvider'):
    'SCD Type1 on overlap: delete existing rows by (Provider, Metric), then insert incoming rows'
    if byProviderDf is None or byProviderDf.empty: return {'RowsDeletedForOverlap': 0, 'RowsInserted': 0}

    try:
        supabaseClient: Client = create_client(supabaseUrl, supabaseKey)

        preparedByProviderDf = PrepareAccuracyDataFrame(byProviderDf, maxMetricLength=20)
        uniqueCombinations   = preparedByProviderDf[['Provider', 'Metric']].drop_duplicates().copy()
        groupedKeys          = uniqueCombinations.groupby(['Provider'])['Metric'].agg(lambda values: sorted(set(values)))

        rowsDeletedForOverlap = 0
        for provider, metricValues in tqdm(groupedKeys.items(), total=len(groupedKeys), desc='ForecastAccuracyByProvider | Delete overlaps'):
            for metricChunk in ChunkValues(metricValues):
                ExecuteWithRetry(lambda provider=provider, metricChunk=metricChunk:
                                 (supabaseClient.table(tableName).delete().eq('Provider', provider).in_('Metric', metricChunk).execute()),
                                 f'ForecastAccuracyByProvider overlap delete for Provider={provider}')

            rowsDeletedForOverlap += len(metricValues)

        records      = PrepareRecordsForInsert(preparedByProviderDf, set(), set())
        rowsInserted = InsertInBatches(supabaseClient, tableName, records, batchSize, 'ForecastAccuracyByProvider | Insert rows')

        return {'RowsDeletedForOverlap': rowsDeletedForOverlap, 'RowsInserted': rowsInserted}

    except Exception as writeError: raise RuntimeError(f'Error writing ForecastAccuracyByProvider to Supabase: {writeError}') from writeError