# Environment Setting
import os
import pandas as pd
import random
from supabase import Client, create_client
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.ConfigurationWeather as Configuration

# Helpers
def BuildSelectClause(columns):
    'Build the SELECT clause for Supabase, normalizing columns name and managing the * case'
    if columns is None                : return '*'
    elif isinstance(columns, str)     : return columns
    elif not isinstance(columns, list): raise ValueError('Columns must be a string or a list of strings')

    normalizedColumns = []
    for columnName in columns:
        cleanName     = columnName.strip()
        if cleanName == '*'                                     : return '*'
        if cleanName.startswith('"') and cleanName.endswith('"'): normalizedColumns.append(cleanName)
        else: normalizedColumns.append(f'"{cleanName}"')

    return ', '.join(normalizedColumns)

def SafeTableChunkFetch(supabaseClient, tableName, selectClause, filters, orderBy, ascending,
                        offset, pageSize, maxRetries, baseRetryDelaySeconds, jitterSeconds):
    'Executes a query con Supabase with retry and exponential backoff, returning the data or the final exception'
    lastException = None

    for attempt in range(1, maxRetries + 1):
        try:
            query = (supabaseClient.table(tableName).select(selectClause).range(offset, offset + pageSize - 1))

            if filters:
                for filterColumn, filterValue in filters.items():
                    if isinstance(filterValue, (list, tuple, set)): query = query.in_(filterColumn, list(filterValue))
                    elif filterValue is None                      : query = query.is_(filterColumn, 'null')
                    else                                          : query = query.eq(filterColumn, filterValue)

            if orderBy                                            : query = query.order(orderBy, desc=not ascending)

            response = query.execute()
            return response.data or [], None

        except Exception as requestError:
            lastException = requestError
            if attempt < maxRetries:
                sleepSeconds = baseRetryDelaySeconds * (2 ** (attempt - 1))
                sleepSeconds += random.uniform(0, max(0.0, jitterSeconds))
                time.sleep(sleepSeconds)

    return None, lastException

# Reading Tables
def SafeTableRead(supaBaseUrl = Configuration.SupabaseUrl, supabaseKey = Configuration.SupabaseKey,
                   tableName = '', columns = None, filters = None, orderBy = None, ascending = True, pageSize = Configuration.SupabasePageSize,
                   maxRetries = Configuration.MaxRetries, baseRetryDelaySeconds = Configuration.BaseRetryDelaySeconds, jitterSeconds = Configuration.JitterSeconds):
    'Reads an entire Supabase table into a DataFrame, handling pagination, retries, and errors according to parameters'
    selectClause   = BuildSelectClause(columns)
    safePageSize   = max(1, min(pageSize, 1000))
    safeMaxRetries = max(1, maxRetries)

    supabaseClient: Client = create_client(supaBaseUrl, supabaseKey)

    allRows = []
    offset  = 0

    while True:
        pageRows, lastException = SafeTableChunkFetch(supabaseClient, tableName, selectClause, filters, orderBy, ascending,
                                                      offset, safePageSize, safeMaxRetries, baseRetryDelaySeconds, jitterSeconds)

        if pageRows is None:
            if lastException is not None: raise RuntimeError(f"Failed to read table '{tableName}' at offset {offset} after {safeMaxRetries} attempts") from lastException
            print(f"Error reading table '{tableName}' at offset {offset} after {safeMaxRetries} attempts: {lastException}")

            if allRows: break
            return None

        if not pageRows: break

        allRows.extend(pageRows)
        offset += safePageSize

    return pd.DataFrame(allRows)