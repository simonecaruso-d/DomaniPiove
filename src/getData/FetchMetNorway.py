# Environment Setting
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.Configuration as Configuration
import getData.HelpersGetData as Helpers

# Functions
def BuildMetNorwayParams(latitude, longitude):
    'Build request params for MET Norway Locationforecast endpoint'
    return {'lat': round(float(latitude), 4), 'lon': round(float(longitude), 4)}

def BuildMetNorwayRecord(cityId, retrievalDatetime, entry):
    'Map one MET Norway timeseries entry to standardized output fields'
    instant   = entry['data']['instant']['details']
    next1h    = entry.get('data', {}).get('next_1_hours', {}).get('details', {})

    temperature              = instant.get('air_temperature')
    humidity                 = instant.get('relative_humidity')
    windSpeed                = instant.get('wind_speed')
    precipitation            = next1h.get('precipitation_amount')

    return {
        'Provider'                : 'MetNorway',
        'RetrievalDatetime'       : Helpers.ParseIsoDateTime(retrievalDatetime),
        'Datetime'                : Helpers.ParseIsoDateTime(entry['time']),
        'CityId'                  : cityId,
        'Temperature'             : temperature,
        'FeltTemperature'         : Helpers.CalculateFeltTemperature(temperature, humidity, windSpeed),
        'Humidity'                : humidity / 100 if humidity is not None else None,
        'Visibility'              : None,
        'PrecipitationProbability': 1 if precipitation is not None and precipitation > 0 else 0 if precipitation is not None else None,
        'Rain'                    : precipitation,
        'Snowfall'                : Helpers.EstimateSnowfall(precipitation, temperature),
        'CloudCover'              : instant.get('cloud_area_fraction') / 100 if instant.get('cloud_area_fraction') is not None else None,
        'WindSpeed'               : Helpers.NormalizeWindSpeedToKmh(windSpeed, 'm/s'),
    }

def FetchMetNorway(cityId, latitude, longitude):
    'Get hourly forecasts from MET Norway Locationforecast API (no API key required)'
    retrievalDatetime = Helpers.CurrentUtcIso()
    records           = []

    requestParameters = BuildMetNorwayParams(latitude, longitude)
    data              = Helpers.SafeRequest(Configuration.MetNorwayUrl, requestParameters, 'MetNorway', {'User-Agent': Configuration.MetNorwayUserAgent})
    timeseries        = data.get('properties', {}).get('timeseries')

    for entry in timeseries:
        record        = BuildMetNorwayRecord(cityId, retrievalDatetime, entry)
        if record is not None: records.append(record)
    return records