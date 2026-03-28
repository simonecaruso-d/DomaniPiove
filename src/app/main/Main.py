# Environment Setting
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
import sys
import threading

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

# Data Loading
def RunLoad(resultHolder, doneEvent):
    try: resultHolder['data'] = LoadData()
    except Exception as e: resultHolder['error'] = e
    finally: doneEvent.set()

@st.cache_data(ttl=1800)
def LoadData():
    'Load city and forecasts data from Supabase.'
    tableReadTasks = {
        'StaticEvents'              : lambda: SupabaseReader.SafeTableRead(tableName='StaticEvents', columns='*'),
        'Calendar'                  : lambda: SupabaseReader.SafeTableRead(tableName='Calendar', columns='*'),
        'City'                      : lambda: SupabaseReader.SafeTableRead(tableName='City', columns='*'),
        'Forecast'                  : lambda: SupabaseReader.SafeTableRead(tableName='Forecast', columns='*'),
        'ForecastAccuracyByDaySpan' : lambda: SupabaseReader.SafeTableRead(tableName='ForecastAccuracyByDaySpan', columns=['Provider', 'DaySpan', 'Metric', 'MAE']),
        'ForecastAccuracyByProvider': lambda: SupabaseReader.SafeTableRead(tableName='ForecastAccuracyByProvider', columns=['Provider', 'Metric', 'MAE'])}

    loadedTables = {}
    with ThreadPoolExecutor(max_workers=len(tableReadTasks)) as executor:
        futureByTable = {tableName: executor.submit(task) for tableName, task in tableReadTasks.items()}

        for tableName, future in futureByTable.items():
            try: loadedTables[tableName] = future.result()
            except Exception as readError: raise RuntimeError(f"Errore nel caricamento della tabella '{tableName}'") from readError

    staticEvents = loadedTables['StaticEvents']
    staticEvents.drop(columns=['Id'], inplace=True)

    calendar = loadedTables['Calendar']
    city     = loadedTables['City']

    forecast = loadedTables['Forecast']

    forecastAccuracyByDaySpan  = loadedTables['ForecastAccuracyByDaySpan']
    forecastAccuracyByProvider = loadedTables['ForecastAccuracyByProvider']

    updateDate = forecast['UpdatedAt'].max()
    
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
        resultHolder = {}
        doneEvent    = threading.Event()

        thread = threading.Thread(target=RunLoad, args=(resultHolder, doneEvent), daemon=True)
        add_script_run_ctx(thread, get_script_run_ctx())
        thread.start()

        if not doneEvent.wait(timeout=0.3): Loader.RenderLoader(doneEvent)

        if 'error' in resultHolder:
            st.error(f"Errore nel caricamento dei dati: {resultHolder['error']}")
            st.stop()

        st.session_state['app_data'] = resultHolder['data']
        staticEvents, calendar, city, forecasts, forecastAccuracyByDaySpan, forecastAccuracyByProvider, updateDate = resultHolder['data']
    else: staticEvents, calendar, city, forecasts, forecastAccuracyByDaySpan, forecastAccuracyByProvider, updateDate = st.session_state['app_data']
        
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