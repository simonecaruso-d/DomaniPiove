# Environment Setting
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.Configuration as Configuration
import getData.HelpersGetData as Helpers

# Functions
def BuildVisualCrossingParams(apiKey):
    'Build request params for Visual Crossing timeline endpoint'
    return {
        'unitGroup'  : 'metric',
        'include'    : 'hours',
        'elements'   : 'datetimeEpoch,temp,feelslike,humidity,visibility,precipprob,precip,snow,cloudcover,windspeed,preciptype',
        'key'        : apiKey,
        'contentType': 'json'}

def BuildVisualCrossingRecord(cityId, retrievalDatetime, hourEntry):
    'Map one Visual Crossing hourly entry to standardized output fields'
    temperature              = hourEntry.get('temp')
    feltTemperature          = hourEntry.get('feelslike')
    humidity                 = hourEntry.get('humidity') / 100
    visibility               = Helpers.NormalizeVisibilityToMeters(hourEntry.get('visibility'), 'km')
    precipitation            = hourEntry.get('precip')
    precipitationProbability = hourEntry.get('precipprob') / 100
    cloudCover               = hourEntry.get('cloudcover') / 100
    windSpeed                = hourEntry.get('windspeed')

    precipitationTypes                    = hourEntry.get('preciptype') or []
    if isinstance(precipitationTypes, str): precipitationTypes = [precipitationTypes]
    precipitationTypes                    = {str(value).lower() for value in precipitationTypes}

    snowfall = hourEntry.get('snow')
    if snowfall is None and precipitation is not None and 'snow' in precipitationTypes: snowfall = Helpers.EstimateSnowfall(precipitation, temperature)

    return {
        'Provider'                : 'VisualCrossing',
        'RetrievalDatetime'       : Helpers.ParseIsoDateTime(retrievalDatetime),
        'Datetime'                : Helpers.ParseUnixTimestamp(hourEntry['datetimeEpoch']),
        'CityId'                  : cityId,
        'Temperature'             : temperature,
        'FeltTemperature'         : feltTemperature,
        'Humidity'                : humidity,
        'Visibility'              : visibility,
        'PrecipitationProbability': precipitationProbability,
        'Rain'                    : precipitation if precipitation is not None and 'snow' not in precipitationTypes else 0.0,
        'Snowfall'                : snowfall,
        'CloudCover'              : cloudCover,
        'WindSpeed'               : windSpeed,
    }

def FetchVisualCrossing(cityId, latitude, longitude, forecastDays=Configuration.OthersMaxForecastDays):
    'Get hourly forecasts from Visual Crossing Timeline API'
    retrievalDatetime = Helpers.CurrentUtcIso()
    records = []

    requestParameters = BuildVisualCrossingParams(Configuration.VisualCrossingApiKey)
    requestUrl        = f'{Configuration.VisualCrossingUrl}/{latitude},{longitude}'
    data              = Helpers.SafeRequest(requestUrl, requestParameters, 'VisualCrossing')
    days              = data.get('days')

    for day in days:
        for hourEntry in day.get('hours', []):
            record               = BuildVisualCrossingRecord(cityId, retrievalDatetime, hourEntry)
            if record is not None: records.append(record)
    return records