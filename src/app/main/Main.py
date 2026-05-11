# Environment Setting
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import streamlit as st
import sys

SourceDirectory = Path(__file__).resolve().parents[2]
if str(SourceDirectory) not in sys.path: sys.path.insert(0, str(SourceDirectory))

import app.main.Loader                      as Loader
import app.ui.Layout                        as HomeUI
import app.pages.Home                       as HomeElements
import app.pages.Accuratezza                as AccuracyElements
import app.pages.Previsioni                 as ForecastElements
import configuration.ConfigurationStreamlit as Configuration
import db.ReadFromSupabase                  as SupabaseReader
import db.TrackDashboardVisits              as VisitTracker

def NormalizeForecastColumns(forecast):
    'Normalize forecast columns used by the app.'
    forecast = forecast.copy()
    if 'RetrievalDatetime' in forecast.columns: forecast['RetrievalDatetime'] = pd.to_datetime(forecast['RetrievalDatetime'], errors='coerce').dt.date
    return forecast

@st.cache_data(ttl=3600*6, show_spinner=False)
def LoadData():
    'Load city and forecasts data from Supabase.'
    daysAgo14 = (datetime.now() - timedelta(days=14)).isoformat()
    dateFilter = {'Datetime': {'gte': daysAgo14}}

    loadedTables   = {}
    tableReadTasks = {
        'StaticEvents'              : lambda: SupabaseReader.SafeTableRead(tableName='StaticEvents', columns='*'),
        'Calendar'                  : lambda: SupabaseReader.SafeTableRead(tableName='Calendar', columns='*'),
        'City'                      : lambda: SupabaseReader.SafeTableRead(tableName='City', columns='*'),
        'Forecast'                  : lambda: SupabaseReader.SafeTableRead(tableName='Forecast', columns='*', filters=dateFilter, orderBy='Datetime'),
        'ForecastAccuracyByDaySpan' : lambda: SupabaseReader.SafeTableRead(tableName='ForecastAccuracyByDaySpan', columns=['Provider', 'DaySpan', 'Metric', 'MAE']),
        'ForecastAccuracyByProvider': lambda: SupabaseReader.SafeTableRead(tableName='ForecastAccuracyByProvider', columns=['Provider', 'Metric', 'MAE'])}
  
    with ThreadPoolExecutor(max_workers=len(tableReadTasks)) as executor:
        futureByTable = {tableName: executor.submit(task) for tableName, task in tableReadTasks.items()}

        for tableName, future in futureByTable.items():
            try                          : loadedTables[tableName] = future.result()
            except Exception as readError: raise RuntimeError(f"Errore nel caricamento della tabella '{tableName}'") from readError

    staticEvents               = loadedTables['StaticEvents'].drop(columns=['Id'], errors='ignore')
    calendar                   = loadedTables['Calendar']
    city                       = loadedTables['City']
    forecast                   = NormalizeForecastColumns(loadedTables['Forecast'])
    forecastAccuracyByDaySpan  = loadedTables['ForecastAccuracyByDaySpan']
    forecastAccuracyByProvider = loadedTables['ForecastAccuracyByProvider'] 
    updateDate                 = forecast['UpdatedAt'].max()
    
    return staticEvents, calendar, city, forecast, forecastAccuracyByDaySpan, forecastAccuracyByProvider, updateDate

# Home
def RenderHomePage(city):
    'Render the complete Home page layout and content.'
    HomeElements.RenderTitle()
    HomeElements.RenderHomeContent(city)

def RenderAccuracyPage(forecastAccuracyByDaySpan):
    'Render the complete Accuracy page layout and content.'
    AccuracyElements.RenderTitle()
    AccuracyElements.RenderAccuracyContent(forecastAccuracyByDaySpan)

def RenderForecastPage(city, calendar, forecasts, forecastAccuracyByProvider, staticEventsTable):
    'Render the complete Forecast page layout and content.'
    ForecastElements.RenderTitle()
    ForecastElements.RenderForecastContent(city, calendar, forecasts, forecastAccuracyByProvider, staticEventsTable)

# Main
def Main():
    'Run the Home page entrypoint workflow.'
    HomeUI.SetupPage()
    Configuration.ApplyResponsiveScale(st.query_params)
    VisitTracker.EnsureVisitStarted()
    st.markdown(Loader.HideRunningIndicatorCss(), unsafe_allow_html=True)

    isFirstLoad = 'app_data' not in st.session_state

    if isFirstLoad:
        loaderSlot = Loader.RenderLoader()

        try:
            result = LoadData()
        except Exception as loadError:
            loaderSlot.empty()
            st.error(f"Errore nel caricamento dei dati: {loadError}")
            st.stop()

        loaderSlot.empty()
        st.session_state['app_data'] = result
        staticEvents, calendar, city, forecasts, forecastAccuracyByDaySpan, forecastAccuracyByProvider, updateDate = result
    
    else:
        staticEvents, calendar, city, forecasts, forecastAccuracyByDaySpan, forecastAccuracyByProvider, updateDate = st.session_state['app_data']
        forecasts = NormalizeForecastColumns(forecasts)
        st.session_state['app_data'] = (staticEvents, calendar, city, forecasts, forecastAccuracyByDaySpan, forecastAccuracyByProvider, updateDate)
        
    currentPage = HomeUI.RenderLayout(updateDate=updateDate)
    VisitTracker.TrackPageView(currentPage)

    if currentPage == 'Accuratezza':
        RenderAccuracyPage(forecastAccuracyByDaySpan)
        return

    elif currentPage == 'Previsioni':
        RenderForecastPage(city, calendar, forecasts, forecastAccuracyByProvider, staticEvents)
        return

    else:
        RenderHomePage(city)
        return

Main()