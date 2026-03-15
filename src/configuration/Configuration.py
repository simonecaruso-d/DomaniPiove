# Environment Setting
from dotenv import load_dotenv
import os 

# API Calls
MaxRetries            = 4
BaseRetryDelaySeconds = 0.7
JitterSeconds         = 0.2
TimeOutSeconds        = 10

# DB
load_dotenv()
SupabaseUrl      = os.getenv("SUPABASE_URL")
SupabaseKey      = os.getenv("SUPABASE_KEY")

SupabasePageSize = 1000
WriteBatchSize   = 500

# Retrieve Data
BrightSkyMaxForecastDays = 10
OthersMaxForecastDays    = 16
HistoricalPastDays       = 3

OpenMeteoFields          = ['temperature_2m', 'apparent_temperature', 'relative_humidity_2m', 'precipitation_probability', 'rain', 'showers', 'snowfall', 'cloud_cover', 'visibility', 'wind_speed_10m',]
OpenMeteoUrl             = 'https://api.open-meteo.com/v1/forecast'

OpenMeteoArchiveFields   = ['temperature_2m', 'apparent_temperature', 'relative_humidity_2m', 'precipitation', 'rain', 'snowfall', 'cloud_cover', 'visibility', 'wind_speed_10m',]
OpenMeteoArchiveUrl      = 'https://archive-api.open-meteo.com/v1/archive'

BrightSkyUrl             = 'https://api.brightsky.dev/weather'

MetNorwayUrl             = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'
MetNorwayUserAgent       = 'DomaniPiove/1.0 github.com/simoc/DomaniPiove'

VisualCrossingUrl        = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
VisualCrossingApiKey     = os.getenv('VISUAL_CROSSING_API_KEY')

PirateWeatherUrl         = 'https://api.pirateweather.net/forecast'
PirateWeatherApiKey      = os.getenv('PIRATE_WEATHER_API_KEY')