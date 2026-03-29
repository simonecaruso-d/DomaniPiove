# Environment Setting
from tqdm import tqdm
import os
import pandas as pd
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.ConfigurationWeather   as Configuration

import db.ReadFromSupabase           as SupabaseReader
import db.WriteToSupabase            as SupabaseWriter

import weather.FetchOpenMeteo        as OM
import weather.FetchOpenMeteoArchive as OMA
import weather.FetchMetNorway        as MN
import weather.FetchVisualCrossing   as VC
import weather.FetchBrightSky        as BS

# Functions
def FetchCityForecasts(cityId, latitude, longitude):
    'Fetch data from all providers and concatenate into a single DataFrame'
    records = []
    records.extend(OM.FetchOpenMeteo(cityId, latitude, longitude))
    records.extend(MN.FetchMetNorway(cityId, latitude, longitude))
    records.extend(VC.FetchVisualCrossing(cityId, latitude, longitude))
    records.extend(BS.FetchBrightSky(cityId, latitude, longitude))
    
    return pd.DataFrame(records)

def FetchCityActuals(cityId, latitude, longitude, pastDays=Configuration.HistoricalPastDays):
    'Fetch historical actuals and concatenate into a single DataFrame'
    records = []
    records.extend(OMA.FetchOpenMeteoArchive(cityId, latitude, longitude, pastDays))

    return pd.DataFrame(records)

def FetchAllCities():
    'Fetch forecasts and actuals for all cities in the database'
    allForecasts = []
    allActuals   = []
    cities       = SupabaseReader.SafeTableRead(tableName='City', columns=['Id', 'Latitude', 'Longitude'])
    
    for _, city in tqdm(cities.iterrows(), total=cities.shape[0], desc='Fetching data for cities'):
        cityId          = city['Id']
        latitude        = city['Latitude']
        longitude       = city['Longitude']
        forecastRecords = FetchCityForecasts(cityId, latitude, longitude)
        actualRecords   = FetchCityActuals(cityId, latitude, longitude)
        allForecasts.append(forecastRecords)
        allActuals.append(actualRecords)
    
    forecastDf              = pd.concat(allForecasts, ignore_index=True) if allForecasts else pd.DataFrame()
    forecastDf['IsCurrent'] = 'Y'
    actualDf                = pd.concat(allActuals, ignore_index=True) if allActuals else pd.DataFrame()

    if not forecastDf.empty:
        forecastDatetimeValues  = pd.to_datetime(forecastDf['Datetime'], utc=True, errors='coerce')
        forecastRetrievalValues = pd.to_datetime(forecastDf['RetrievalDatetime'], utc=True, errors='coerce')
        forecastDf              = forecastDf.loc[forecastDatetimeValues >= forecastRetrievalValues].reset_index(drop=True)

    if not actualDf.empty:
        actualDatetimeValues  = pd.to_datetime(actualDf['Datetime'], utc=True, errors='coerce')
        actualRetrievalValues = pd.to_datetime(actualDf['RetrievalDatetime'], utc=True, errors='coerce')
        actualDf              = actualDf.loc[actualDatetimeValues <= actualRetrievalValues].reset_index(drop=True)

    return forecastDf, actualDf

def WriteAllToSupabase(forecastDf, actualDf):
    'Write forecasts and actuals to Supabase with their dedicated SCD strategies'
    forecastWriteResult = SupabaseWriter.WriteForecastToSupabase(forecastDf)
    actualWriteResult   = SupabaseWriter.WriteActualToSupabase(actualDf)
    return forecastWriteResult, actualWriteResult

# Run
ForecastDf, ActualDf                   = FetchAllCities()
ForecastWriteResult, ActualWriteResult = WriteAllToSupabase(ForecastDf, ActualDf)

print(f'Forecast write summary: {ForecastWriteResult}')
print(f'Actual write summary: {ActualWriteResult}')