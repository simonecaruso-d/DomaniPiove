# Environment Setting
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.Configuration as Configuration
import getData.HelpersGetData as Helpers

# Functions
def BuildOpenMeteoArchiveParams(latitude, longitude, pastDays):
    'Build request params for the latest completed local days'
    endDate   = datetime.now(ZoneInfo('Europe/Rome')).date() - timedelta(days=1)
    startDate = endDate - timedelta(days=pastDays - 1)

    return {
        'latitude'  : float(latitude),
        'longitude' : float(longitude),
        'timezone'  : 'Europe/Rome',
        'start_date': startDate.isoformat(),
        'end_date'  : endDate.isoformat(),
        'hourly'    : ','.join(Configuration.OpenMeteoArchiveFields),}

def GetHourlyValue(hourly, fieldName, index):
    'Safely read one hourly value from Open-Meteo payload'
    values = hourly.get(fieldName)
    if values is None: return None
    return values[index]

def BuildOpenMeteoArchiveRecord(cityId, retrievalDatetime, hourly, index):
    'Map one Open-Meteo archive hourly position to standardized output fields'
    humidity   = GetHourlyValue(hourly, 'relative_humidity_2m', index)
    visibility = GetHourlyValue(hourly, 'visibility', index)
    rain       = GetHourlyValue(hourly, 'rain', index)
    snowfall   = GetHourlyValue(hourly, 'snowfall', index)

    return {
        'Provider'                : 'OpenMeteoArchive',
        'RetrievalDatetime'       : Helpers.ParseIsoDateTime(retrievalDatetime),
        'Datetime'                : Helpers.ParseIsoDateTime(hourly['time'][index], 'Europe/Rome'),
        'CityId'                  : cityId,
        'Temperature'             : GetHourlyValue(hourly, 'temperature_2m', index),
        'FeltTemperature'         : GetHourlyValue(hourly, 'apparent_temperature', index),
        'Humidity'                : humidity / 100 if humidity is not None else None,
        'Visibility'              : Helpers.NormalizeVisibilityToMeters(visibility, 'm') if visibility is not None else None,
        'PrecipitationProbability': 1 if (rain is not None and rain > 0) or (snowfall is not None and snowfall > 0) else 0,
        'Rain'                    : rain,
        'Snowfall'                : snowfall,
        'CloudCover'              : GetHourlyValue(hourly, 'cloud_cover', index) / 100 if GetHourlyValue(hourly, 'cloud_cover', index) is not None else None,
        'WindSpeed'               : GetHourlyValue(hourly, 'wind_speed_10m', index),
    }

def FetchOpenMeteoArchive(cityId, latitude, longitude, pastDays=Configuration.HistoricalPastDays):
    'Get hourly historical weather from Open-Meteo Archive API'
    retrievalDatetime = Helpers.CurrentUtcIso()
    records           = []

    requestParameters = BuildOpenMeteoArchiveParams(latitude, longitude, pastDays)
    data              = Helpers.SafeRequest(Configuration.OpenMeteoArchiveUrl, requestParameters, 'OpenMeteoArchive')
    
    if not isinstance(data, dict): return []
    hourly = data.get('hourly')
    if not isinstance(hourly, dict) or 'time' not in hourly: return []

    for index in range(len(hourly['time'])):
        record = BuildOpenMeteoArchiveRecord(cityId, retrievalDatetime, hourly, index)
        if record is not None: records.append(record)

    return records