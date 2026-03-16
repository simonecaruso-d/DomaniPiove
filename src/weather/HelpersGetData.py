# Environment Setting
import math
import requests
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.ConfigurationWeather as Configuration

# Request
def SafeRequest(url, params, providerName, headers=None,
                maxRetries=Configuration.MaxRetries, baseDelay=Configuration.BaseRetryDelaySeconds, jitter=Configuration.JitterSeconds, timeout=Configuration.TimeOutSeconds):
    'Execute HTTP request with error handling, returns data or None'
    for attempt in range(1, maxRetries + 1):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == maxRetries:
                print(f'{providerName}: Connection Error - {e}')
                return None
            time.sleep(baseDelay * attempt + jitter)
        except ValueError as e:
            print(f'{providerName}: JSON Parsing Error - {e}')
            return None

# Data Cleaning
def TruncateToMinuteIso(datetimeValue):
    'Convert datetime to ISO string with seconds and microseconds set to 0'
    return datetimeValue.replace(minute=0, second=0, microsecond=0).isoformat(timespec='seconds')

def NormalizeDateTimeToUtcIso(datetimeValue, sourceTimezone=None):
    'Normalize datetime to UTC ISO string and truncate to expected precision'
    if datetimeValue.tzinfo is None:
        if sourceTimezone is None: datetimeValue = datetimeValue.replace(tzinfo=timezone.utc)
        else: datetimeValue                      = datetimeValue.replace(tzinfo=ZoneInfo(sourceTimezone))
    return TruncateToMinuteIso(datetimeValue.astimezone(timezone.utc))

def ParseIsoDateTime(datetimeString, sourceTimezone=None):
    'Parse ISO datetime string (supports Z suffix), normalize to UTC and truncate to expected precision'
    return NormalizeDateTimeToUtcIso(datetime.fromisoformat(str(datetimeString).replace('Z', '+00:00')), sourceTimezone)

def ParseUnixTimestamp(unixSeconds):
    'Parse UNIX timestamp to UTC ISO datetime and truncate to expected precision'
    return NormalizeDateTimeToUtcIso(datetime.fromtimestamp(int(unixSeconds), tz=timezone.utc))

def CurrentUtcIso():
    'Get current UTC datetime in ISO format, truncated to expected precision'
    return NormalizeDateTimeToUtcIso(datetime.now(timezone.utc))

def NormalizeVisibilityToMeters(visibility, unit):
    'Normalize visibility values to meters'
    if visibility is None: return None
    if unit == 'km': return float(visibility) * 1000
    if unit == 'm': return float(visibility)
    raise ValueError(f'Unknown visibility unit: {unit}')

def NormalizeWindSpeedToKmh(windSpeed, unit):
    'Normalize wind speed values to km/h'
    if windSpeed is None: return None
    if unit == 'km/h': return float(windSpeed)
    if unit == 'm/s':  return float(windSpeed) * 3.6
    raise ValueError(f'Unknown wind speed unit: {unit}')

# Data Engineering
def DeriveHumidityFromDewPoint(temperature, dewPoint):
    'Estimate relative humidity (0-100) from temperature and dew point via Magnus formula'
    if temperature is None or dewPoint is None: return None
    numerator   = math.exp(17.625 * dewPoint   / (243.04 + dewPoint))
    denominator = math.exp(17.625 * temperature / (243.04 + temperature))
    return round(100 * numerator / denominator, 1)

def CalculateFeltTemperature(temperature, humidity, windSpeed):
    'Apparent temperature via Steadman formula (inputs: °C, %, m/s)'
    if any(value is None for value in [temperature, humidity, windSpeed]): return None
    vaporPressure = (humidity / 100) * 6.105 * math.exp(17.27 * temperature / (237.7 + temperature))
    return          round(temperature + 0.33 * vaporPressure - 0.70 * windSpeed - 4.00, 2)

def EstimateSnowfall(precipitation, temperature):
    'Estimate snowfall in cm (10:1 snow-to-water ratio) when temperature is at or below 2°C'
    if precipitation is None or temperature is None: return None
    if temperature <= 2.0                          : return round(float(precipitation) * 10, 2)
    else                                           : return 0.0