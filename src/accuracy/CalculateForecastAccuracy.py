# Environment Setting
import os
import numpy as np
import pandas as pd
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import db.ReadFromSupabase                 as SupabaseReader
import db.WriteToSupabase                  as SupabaseWriter
import configuration.ConfigurationAccuracy as Configuration

# Helpers
def AssignDaySpan(forecastLeadDays):
    'Map lead time in days to configured DaySpan buckets using upper-bound assignment'
    if pd.isna(forecastLeadDays) or forecastLeadDays <= 0: return pd.NA

    for daySpan in Configuration.DaySpanValues:
        if forecastLeadDays <= daySpan: return daySpan

    return pd.NA

# Calculate
def BuildAggregatedData(columnsToSelect=Configuration.MetricColumns + ['CityId', 'Datetime', 'RetrievalDatetime', 'Provider']):
    'Build a row-level table linking each forecast row to the matching actual for the same city and datetime'
    forecastDf = SupabaseReader.SafeTableRead(tableName='Forecast', columns=columnsToSelect)
    actualDf   = SupabaseReader.SafeTableRead(tableName='Actual', columns=columnsToSelect)

    forecastDf['RetrievalDatetime'] = pd.to_datetime(forecastDf['RetrievalDatetime'], utc=True, errors='coerce')
    forecastDf['Datetime']          = pd.to_datetime(forecastDf['Datetime'], utc=True, errors='coerce')
    actualDf['RetrievalDatetime']   = pd.to_datetime(actualDf['RetrievalDatetime'], utc=True, errors='coerce')
    actualDf['Datetime']            = pd.to_datetime(actualDf['Datetime'], utc=True, errors='coerce')

    aggregatedDf                     = forecastDf.merge(actualDf, on=['CityId', 'Datetime'], how='left', suffixes=('_Forecast', '_Actual'))
    aggregatedDf['ForecastLeadDays'] = (aggregatedDf['Datetime'] - aggregatedDf['RetrievalDatetime_Forecast']).dt.total_seconds() / (60 * 60 * 24)

    return aggregatedDf

def UnpivotData(aggregatedDf, metricColumns=Configuration.MetricColumns):
    'Unpivot forecast/actual metric columns into Provider, RetrievalDatetime, Datetime, CityId, Metric, ForecastValue, ActualValue'
    idColumns  = ['Provider_Forecast', 'RetrievalDatetime_Forecast', 'Datetime', 'CityId']
    longFrames = []

    for metricName in metricColumns:
        forecastMetricColumn  = f'{metricName}_Forecast'
        actualMetricColumn    = f'{metricName}_Actual'
        metricFrame           = aggregatedDf[idColumns + [forecastMetricColumn, actualMetricColumn]].copy()
        metricFrame['Metric'] = metricName
        metricFrame           = metricFrame.rename(columns={'Provider_Forecast': 'Provider', 'RetrievalDatetime_Forecast': 'RetrievalDatetime', forecastMetricColumn: 'ForecastValue', actualMetricColumn: 'ActualValue',})
        longFrames.append(metricFrame[['Provider', 'RetrievalDatetime', 'Datetime', 'CityId', 'Metric', 'ForecastValue', 'ActualValue']])

    result                        = pd.concat(longFrames, ignore_index=True)
    result                        = result.dropna(subset=['ForecastValue', 'ActualValue'])
    result['ForecastLeadDaysRaw'] = (result['Datetime'] - result['RetrievalDatetime']).dt.total_seconds() / (60 * 60 * 24)
    result['DaySpan']             = result['ForecastLeadDaysRaw'].map(AssignDaySpan)
    result                        = result.dropna(subset=['DaySpan'])
    result['AE']                  = (result['ForecastValue'] - result['ActualValue']).abs()
    result['APE']                 = result['AE'] / result['ActualValue'].replace(0, np.nan)
    return result

def AggregateMetrics(unpivotedDf):
    'Calculate MAE and MAPE by Provider, DaySpan, Metric'
    byDaySpan         = unpivotedDf.groupby(['Provider', 'DaySpan', 'Metric']).agg(MAE=('AE', 'mean'), MAPE=('APE', 'mean')).reset_index()
    byDaySpan['MAPE'] = byDaySpan['MAPE'].fillna(0)
    byDaySpan['MAE']  = byDaySpan['MAE'].round(4)
    byDaySpan['MAPE'] = byDaySpan['MAPE'].round(4)

    byProvider         = unpivotedDf.groupby(['Provider', 'Metric']).agg(MAE=('AE', 'mean'), MAPE=('APE', 'mean')).reset_index()
    byProvider['MAPE'] = byProvider['MAPE'].fillna(0)
    byProvider['MAE']  = byProvider['MAE'].round(4)
    byProvider['MAPE'] = byProvider['MAPE'].round(4)

    return byDaySpan, byProvider

# Write To DB
def WriteToSupabase(byDaySpanDf, byProviderDf):
    'Write aggregated forecast accuracy metrics to Supabase tables ForecastAccuracyByDaySpan and ForecastAccuracyByProvider'
    byDaySpanWriteResult = SupabaseWriter.WriteForecastAccuracyByDaySpanToSupabase(byDaySpanDf)
    byProviderWriteResult = SupabaseWriter.WriteForecastAccuracyByProviderToSupabase(byProviderDf)
    return {'ByDaySpan': byDaySpanWriteResult, 'ByProvider': byProviderWriteResult}

# Main
def Wrapper():
    aggregatedDf          = BuildAggregatedData()
    unpivotedDf           = UnpivotData(aggregatedDf)
    byDaySpan, byProvider = AggregateMetrics(unpivotedDf)
    writeResult           = WriteToSupabase(byDaySpan, byProvider)
    print(writeResult)

    return

# Run
Wrapper()