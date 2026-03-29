# Environment Setting
from datetime import datetime, timedelta, timezone
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.ConfigurationWeather as Configuration
import weather.HelpersGetData as Helpers

# Functions
def BuildBrightSkyParams(latitude, longitude, forecastDays):
    'Build request params for Bright Sky hourly weather endpoint'
    startDate = datetime.now(timezone.utc).date()
    endDate   = startDate + timedelta(days=forecastDays - 1)

    return {'lat': round(float(latitude), 4), 'lon': round(float(longitude), 4), 'date': startDate.isoformat(), 'last_date': endDate.isoformat()}

def BuildBrightSkyRecord(cityId, retrievalDatetime, item):
    'Map one Bright Sky hourly entry to standardized output fields'
    temperature              = item.get('temperature')
    humidityRaw              = item.get('relative_humidity')
    if humidityRaw is None   : humidityRaw = Helpers.DeriveHumidityFromDewPoint(temperature, item.get('dew_point'))
    windSpeed                = item.get('wind_speed')
    windSpeedMs              = windSpeed / 3.6 if windSpeed is not None else None
    precipitation            = item.get('precipitation')
    feltTemperature          = item.get('feels_like')

    if feltTemperature is None: feltTemperature = Helpers.CalculateFeltTemperature(temperature, humidityRaw, windSpeedMs)
    precipitationType         = str(item.get('precipitation_type') or item.get('condition') or '').lower()
    snowfall                  = Helpers.EstimateSnowfall(precipitation, temperature)
    rain                      = precipitation
    
    if 'snow' in precipitationType and precipitation is not None: rain = 0.0

    return {
        'Provider'                : 'BrightSky',
        'RetrievalDatetime'       : Helpers.ParseIsoDateTime(retrievalDatetime),
        'Datetime'                : Helpers.ParseIsoDateTime(item['timestamp']),
        'CityId'                  : cityId,
        'Temperature'             : temperature,
        'FeltTemperature'         : feltTemperature,
        'Humidity'                : humidityRaw / 100 if humidityRaw is not None else None,
        'Visibility'              : Helpers.NormalizeVisibilityToMeters(item.get('visibility'), 'm'),
        'PrecipitationProbability': item.get('precipitation_probability') / 100 if item.get('precipitation_probability') is not None else None,
        'Rain'                    : rain,
        'Snowfall'                : snowfall,
        'CloudCover'              : item.get('cloud_cover') / 100 if item.get('cloud_cover') is not None else None,
        'WindSpeed'               : windSpeed}

def FetchBrightSky(cityId, latitude, longitude, forecastDays=Configuration.BrightSkyMaxForecastDays):
    'Get hourly forecasts from Bright Sky API'
    retrievalDatetime = Helpers.CurrentUtcIso()
    records           = []

    requestParameters = BuildBrightSkyParams(latitude, longitude, forecastDays)
    data              = Helpers.SafeRequest(Configuration.BrightSkyUrl, requestParameters, 'BrightSky')
    entries           = data.get('weather')

    for entry in entries:
        record = BuildBrightSkyRecord(cityId, retrievalDatetime, entry)
        if record is not None: records.append(record)
    return records