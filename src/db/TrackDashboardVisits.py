# Environment Setting
import hashlib
import os
import uuid
from datetime import datetime, timezone

import streamlit as st
from supabase import Client, create_client

import configuration.ConfigurationWeather as Configuration
import db.WriteToSupabase as SupabaseWriter

# Functions
def NowUtcIso():
    'Return current UTC datetime as ISO string.'
    return datetime.now(timezone.utc).isoformat()

def BuildVisitId():
    'Create a random visit identifier.'
    return str(uuid.uuid4())

def ReadHeadersFromStreamlit():
    'Read HTTP headers from Streamlit context when available.'
    context = getattr(st, 'context', None)
    headers = getattr(context, 'headers', None) if context is not None else None

    if headers is None: return {}

    try: return {str(key).lower(): str(value) for key, value in headers.items()}
    except Exception: return {}

def HashIp(ipValue):
    'Hash client IP with optional salt for privacy-safe tracking.'
    if not ipValue: return None

    salt       = os.getenv('ANALYTICS_HASH_SALT', '')
    normalized = str(ipValue).strip().lower()
    if not normalized: return None

    return hashlib.sha256(f'{salt}:{normalized}'.encode('utf-8')).hexdigest()

def ExtractClientIp(headers):
    'Extract client IP from forwarded headers if present.'
    xForwardedFor = headers.get('x-forwarded-for')
    if xForwardedFor: return xForwardedFor.split(',')[0].strip()

    return headers.get('x-real-ip')

def ReadQueryParams():
    'Read query params as plain dict with safe fallback.'
    try: return dict(st.query_params)
    except Exception: return {}

def ResolveCurrentPage(queryParams, defaultPage='Home'):
    'Resolve current page value from query params.'
    page = queryParams.get('page', defaultPage)
    if isinstance(page, list): return page[0] if page else defaultPage
    return page

def BuildBaseMetadata(appVersion='1.0.0'):
    'Build common metadata for each tracked event.'
    headers     = ReadHeadersFromStreamlit()
    queryParams = ReadQueryParams()
    currentPage = ResolveCurrentPage(queryParams=queryParams)
    clientIp    = ExtractClientIp(headers)

    return {'AppVersion': appVersion,
        'Page': str(currentPage),
        'UserAgent': headers.get('user-agent'),
        'Referrer': headers.get('referer') or headers.get('referrer'),
        'IpHash': HashIp(clientIp),
        'QueryParams': queryParams,
        'HeadersSample': {
            'accept_language': headers.get('accept-language'),
            'sec_ch_ua_platform': headers.get('sec-ch-ua-platform'),
            'sec_ch_ua_mobile': headers.get('sec-ch-ua-mobile'),
        }}

def BuildSupabaseClient(supabaseUrl=Configuration.SupabaseUrl, supabaseKey=Configuration.SupabaseKey):
    'Create Supabase client for analytics writes.'
    if not supabaseUrl or not supabaseKey: raise RuntimeError('SUPABASE_URL / SUPABASE_KEY missing for analytics tracking')
    return create_client(supabaseUrl, supabaseKey)

def EnsureVisitSessionValues():
    'Initialize visit/session values once per Streamlit session.'
    if 'visit_id' not in st.session_state: st.session_state['visit_id'] = BuildVisitId()
    if 'session_started_at' not in st.session_state: st.session_state['session_started_at'] = NowUtcIso()

def ReadSessionElapsedSeconds():
    'Compute elapsed seconds from session start.'
    try:
        startDatetime = datetime.fromisoformat(str(st.session_state.get('session_started_at')))
        return int((datetime.now(timezone.utc) - startDatetime).total_seconds())
    except Exception: return None

def BuildEventRow(eventType, page, payload, appVersion):
    'Build event row payload for the VisitEvents table.'
    EnsureVisitSessionValues()
    base = BuildBaseMetadata(appVersion=appVersion)

    return {
        'EventTs': NowUtcIso(),
        'VisitId': st.session_state['visit_id'],
        'SessionId': str(st.session_state.get('_session_id', st.session_state['visit_id'])),
        'EventType': str(eventType),
        'Page': str(page or base.get('Page') or 'Home'),
        'AppVersion': base.get('AppVersion'),
        'UserAgent': base.get('UserAgent'),
        'Referrer': base.get('Referrer'),
        'IpHash': base.get('IpHash'),
        'QueryParams': base.get('QueryParams') or {},
        'HeadersSample': base.get('HeadersSample') or {},
        'Payload': payload or {},
        'SessionStartedAt': st.session_state.get('session_started_at'),
        'SessionElapsedSeconds': ReadSessionElapsedSeconds()}

def WriteEventToSupabase(eventType, page=None, payload=None, appVersion='1.0.0', tableName='VisitEvents',
                         supabaseUrl=Configuration.SupabaseUrl, supabaseKey=Configuration.SupabaseKey, failSilently=True):
    'Write one analytics event to Supabase.'
    row = BuildEventRow(eventType=eventType, page=page, payload=payload, appVersion=appVersion)

    try:
        supabaseClient: Client = BuildSupabaseClient(supabaseUrl=supabaseUrl, supabaseKey=supabaseKey)
        SupabaseWriter.ExecuteWithRetry(
            lambda: supabaseClient.table(tableName).insert({
                'EventTs': row['EventTs'],
                'VisitId': row['VisitId'],
                'SessionId': row['SessionId'],
                'EventType': row['EventType'],
                'Page': row['Page'],
                'AppVersion': row['AppVersion'],
                'UserAgent': row['UserAgent'],
                'Referrer': row['Referrer'],
                'IpHash': row['IpHash'],
                'QueryParams': row['QueryParams'],
                'HeadersSample': row['HeadersSample'],
                'Payload': row['Payload'],
                'SessionStartedAt': row['SessionStartedAt'],
                'SessionElapsedSeconds': row['SessionElapsedSeconds'],
            }).execute(), operationDescription=f'Insert analytics event ({eventType})',)
    except Exception as writeError:
        if failSilently:
            print(f'[VisitTracker] Insert failed for {eventType}: {writeError}')
            return False
        raise

    return True

def EnsureVisitStarted(appVersion='1.0.0', tableName='VisitEvents', failSilently=True):
    'Send exactly one visit_start event per Streamlit session.'
    EnsureVisitSessionValues()
    if st.session_state.get('_visit_started_sent'): return False

    sent = WriteEventToSupabase(eventType='visit_start', page=None, payload={'source': 'streamlit_app_bootstrap'}, appVersion=appVersion, tableName=tableName, failSilently=failSilently)

    if sent: st.session_state['_visit_started_sent'] = True
    return sent

def TrackPageView(currentPage, appVersion='1.0.0', tableName='VisitEvents', failSilently=True):
    'Send page_view only when selected page changes.'
    previousPage = st.session_state.get('_last_tracked_page')
    if previousPage == currentPage: return False

    sent = WriteEventToSupabase(eventType='page_view', page=currentPage, payload={'previousPage': previousPage}, appVersion=appVersion, tableName=tableName, failSilently=failSilently,)

    if sent: st.session_state['_last_tracked_page'] = currentPage
    return sent