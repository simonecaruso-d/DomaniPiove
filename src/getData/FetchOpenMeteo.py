# Environment Setting
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.Configuration as Configuration
import getData.HelpersGetData as Helpers

# Functions
def BuildOpenMeteoParams(latitude, longitude, forecastDays):
    'Build request params for Open-Meteo hourly forecast endpoint'
    return {'latitude': float(latitude), 'longitude': float(longitude), 'timezone': 'Europe/Rome', 'forecast_days': forecastDays, 'hourly': ','.join(Configuration.OpenMeteoFields),}

def BuildOpenMeteoRecord(cityId, retrievalDatetime, hourly, index):
    'Map one Open-Meteo hourly position to standardized output fields'
    return {
        'Provider'                : 'OpenMeteo',
        'RetrievalDatetime'       : Helpers.ParseIsoDateTime(retrievalDatetime),
        'Datetime'                : Helpers.ParseIsoDateTime(hourly['time'][index], 'Europe/Rome'),
        'CityId'                  : cityId,
        'Temperature'             : hourly['temperature_2m'][index],
        'FeltTemperature'         : hourly['apparent_temperature'][index],
        'Humidity'                : hourly['relative_humidity_2m'][index] / 100,
        'Visibility'              : Helpers.NormalizeVisibilityToMeters(hourly['visibility'][index], 'm'),
        'PrecipitationProbability': hourly['precipitation_probability'][index] / 100,
        'Rain'                    : hourly['rain'][index],
        'Snowfall'                : hourly['snowfall'][index],
        'CloudCover'              : hourly['cloud_cover'][index] / 100,
        'WindSpeed'               : hourly['wind_speed_10m'][index],
    }

def FetchOpenMeteo(cityId, latitude, longitude, forecastDays=Configuration.OthersMaxForecastDays):
    'Get hourly forecasts from Open-Meteo API'
    retrievalDateTime = Helpers.CurrentUtcIso()
    records           = []

    requestParameters = BuildOpenMeteoParams(latitude, longitude, forecastDays)
    data              = Helpers.SafeRequest(url=Configuration.OpenMeteoUrl, params=requestParameters, providerName='OpenMeteo')
    
    if not isinstance(data, dict): return []
    hourly                       = data.get('hourly')

    for index in range(len(hourly['time'])):
        record               = BuildOpenMeteoRecord(cityId, retrievalDateTime, hourly, index)
        if record is not None: records.append(record)

    return records