# Environment Setting
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.ConfigurationWeather as Configuration
import weather.HelpersGetData as Helpers

# Functions
def BuildOpenMeteoParams(latitude, longitude, forecastDays):
    'Build request params for Open-Meteo hourly forecast endpoint'
    return {'latitude': float(latitude), 'longitude': float(longitude), 'timezone': 'Europe/Rome', 'forecast_days': forecastDays, 'hourly': ','.join(Configuration.OpenMeteoFields),}

def BuildOpenMeteoRecord(cityId, retrievalDatetime, hourly, index):
    'Map one Open-Meteo hourly position to standardized output fields'
    humidity                 = hourly['relative_humidity_2m'][index]
    precipitationProbability = hourly['precipitation_probability'][index]
    cloudCover               = hourly['cloud_cover'][index]

    return {
        'Provider'                : 'OpenMeteo',
        'RetrievalDatetime'       : Helpers.ParseIsoDateTime(retrievalDatetime),
        'Datetime'                : Helpers.ParseIsoDateTime(hourly['time'][index], 'Europe/Rome'),
        'CityId'                  : cityId,
        'Temperature'             : hourly['temperature_2m'][index],
        'FeltTemperature'         : hourly['apparent_temperature'][index],
        'Humidity'                : humidity / 100 if humidity is not None else None,
        'Visibility'              : Helpers.NormalizeVisibilityToMeters(hourly['visibility'][index], 'm'),
        'PrecipitationProbability': precipitationProbability / 100 if precipitationProbability is not None else None,
        'Rain'                    : hourly['rain'][index],
        'Snowfall'                : hourly['snowfall'][index],
        'CloudCover'              : cloudCover / 100 if cloudCover is not None else None,
        'WindSpeed'               : hourly['wind_speed_10m'][index]}

def FetchOpenMeteo(cityId, latitude, longitude, forecastDays=Configuration.OthersMaxForecastDays):
    'Get hourly forecasts from Open-Meteo API'
    retrievalDateTime = Helpers.CurrentUtcIso()
    records           = []

    requestParameters = BuildOpenMeteoParams(latitude, longitude, forecastDays)
    data              = Helpers.SafeRequest(url=Configuration.OpenMeteoUrl, params=requestParameters, providerName='OpenMeteo')
    
    if not isinstance(data, dict): return []
    hourly                       = data.get('hourly')
    if not isinstance(hourly, dict) or 'time' not in hourly: return []

    for index in range(len(hourly['time'])):
        record               = BuildOpenMeteoRecord(cityId, retrievalDateTime, hourly, index)
        if record is not None: records.append(record)

    return records