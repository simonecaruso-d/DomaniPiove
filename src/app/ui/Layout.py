# Environment Setting
import base64
import pandas as pd
import streamlit as st
from urllib.parse import quote_plus

import configuration.ConfigurationStreamlit as Configuration

# Components
def SetupPage():
    'Configure the base page metadata and layout.'
    st.set_page_config(page_title            = Configuration.PageTitle,
                       page_icon             = Configuration.PageIcon,
                       layout                = Configuration.Layout,
                       initial_sidebar_state = Configuration.InitialSidebarState)

def LoadLogo():
    'Load and encode the app logo as a base64 string.'
    with open(Configuration.LogoPath, 'rb') as file: return base64.b64encode(file.read()).decode()

def LoadSidebarIcons(pageIconPath):
    'Load and encode sidebar page icons as base64 strings.'
    iconsB64 = {}
    for page, iconPath in pageIconPath.items(): 
        with open(iconPath, 'rb') as file: iconsB64[page] = base64.b64encode(file.read()).decode()
    return iconsB64

def LoadFooterIcons(footerIconPath):
    'Load and encode sidebar footer icons as base64 strings.'
    iconsB64 = {}
    for key, iconPath in footerIconPath.items():
        with open(iconPath, 'rb') as file: iconsB64[key] = base64.b64encode(file.read()).decode()
    return iconsB64

def GetCurrentPage(pages):
    'Resolve the active page from query parameters with a safe fallback.'
    currentPage                = st.query_params.get('page', pages[0])
    if currentPage not in pages: return pages[0]
    return currentPage

def RenderSidebar(sidebarIcons, footerIcons, pages):
    'Render the sidebar navigation and footer.'
    currentPage     = GetCurrentPage(pages)
    navigationItems = []

    for page in pages:
        activeClass = 'active' if page == currentPage else ''
        icon        = sidebarIcons.get(page, '')
        navigationItems.append(f"""<a class="sidebar-nav-item {activeClass}" href="?page={quote_plus(page)}" target="_self">
                               <span class="sidebar-nav-item-content"><img class="sidebar-icon" src="data:image/png;base64,{icon}" alt="" /><span>{page}</span></span></a>""")

    emailIcon       = footerIcons.get('Email', '')
    copyrightIcon   = footerIcons.get('Copyright', '')

    footerHtml      = (
        """<div class="sidebar-footer"><a class="sidebar-footer-link" href="mailto:simocaruso1997@libero.it">"""
        f'<img class="sidebar-footer-icon" src="data:image/png;base64,{emailIcon}" alt="" />'
        """<span class="sidebar-footer-text">Contattami</span></a><div class="sidebar-footer-item">"""
        f'<img class="sidebar-footer-icon" src="data:image/png;base64,{copyrightIcon}" alt="" />'
        """<span class="sidebar-footer-text">Simone Caruso 2026, v 1.0</span></div></div>""")

    st.sidebar.markdown('<div class="sidebar-shell">' + '<div class="sidebar-nav">' + ''.join(navigationItems) + '</div>' + footerHtml + '</div>', unsafe_allow_html=True)
    return currentPage

def FormatUpdateLabel(updateDate):
    'Return a plain-text update label for topbar rendering.'
    try:
        value     = updateDate.iloc[0] if hasattr(updateDate, 'iloc') else updateDate
        timestamp = pd.to_datetime(value, utc=True, errors='coerce')
        formatted = timestamp.strftime('%d %b %Y, %H:%M UTC') if not pd.isna(timestamp) else None
    except Exception: formatted = None
    if not formatted: return 'Ultimo aggiornamento: n.d.'
    return f'Ultimo aggiornamento: {formatted}'

def RenderUpdateIndicator(updateDate):
    'Build the topbar live-update indicator HTML.'
    updateLabel = FormatUpdateLabel(updateDate)
    return (f"""<div class="topbar-live"><span class="topbar-live-dot"></span><span>{updateLabel}</span></div>""")

# Wrappers
def RenderStyles(logo, 
                 backgroundColor = Configuration.AccentColor, 
                 buttonRadiusPx  = Configuration.RadiusButton, 
                 inputRadiusPx   = Configuration.RadiusInput, 
                 primaryColor    = Configuration.PrimaryColor, 
                 cardRadiusPx    = Configuration.RadiusCard, 
                 borderWidthPx   = Configuration.WidthBorder, 
                 borderColor     = Configuration.TertiaryColor, 
                 pageTitle       = Configuration.PageTitle, 
                 updateDate      = None):
    'Inject global UI styles and render the custom topbar shell.'
    updateLabelEscaped    = FormatUpdateLabel(updateDate).replace('\\', '\\\\').replace('"', '\\"')
    topbarHeightPx        = Configuration.ScalePx(60)
    topbarLeftExpandedPx  = Configuration.ScalePx(244)
    topbarLeftCollapsedPx = Configuration.ScalePx(76)
    topbarLogoHeightPx    = Configuration.ScalePx(34)
    topbarPaddingX        = Configuration.ScalePx(24)
    topbarGap             = Configuration.ScalePx(12)
    sidebarCollapsedWidth = Configuration.ScalePx(76)

    st.markdown(f"""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"><style>
            :root {{
                --dp-primary: #ab8674;
                --dp-primary-dark: #96705e;
                --dp-bar-bg: linear-gradient(120deg, #ab8674 0%, #96705e 100%);
                --dp-bar-overlay: linear-gradient(120deg, rgba(255,255,255,0.28) 0%, rgba(255,255,255,0.00) 44%);
                --dp-text-soft: rgba(255,255,255,0.84);
                --dp-glass: rgba(255,255,255,0.14);
                --dp-glass-strong: rgba(255,255,255,0.22);
                --dp-shadow-soft: 0 10px 34px rgba(171,134,116,0.18);
                --dp-shadow-glow: 0 0 24px rgba(255,255,255,0.16);
                --dp-shadow-strong: 0 20px 48px rgba(120,80,58,0.28);
                --dp-glow-primary: 0 0 38px rgba(171,134,116,0.34);
                --dp-bar-blur: blur(14px) saturate(165%);
                --dp-bar-shadow: 0 10px 40px rgba(171,134,116,0.34), 0 0 30px rgba(171,134,116,0.26), inset 0 1px 0 rgba(255,255,255,0.20)}}

            html, body,
            [data-testid="stAppViewContainer"],
            [data-testid="stMain"],
            p, h1, h2, h3, h4, h5, h6,
            label, input, textarea, select,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] div {{font-family: 'Inter', sans-serif !important;}}

            .stApp {{background-color: {backgroundColor};
                background-image:
                    radial-gradient(circle at 15% 18%, rgba(171,134,116,0.10) 0%, rgba(171,134,116,0.00) 38%),
                    radial-gradient(circle at 84% 10%, rgba(198,167,150,0.12) 0%, rgba(198,167,150,0.00) 42%),
                    linear-gradient(180deg, rgba(255,255,255,0.96) 0%, rgba(250,247,244,0.98) 100%);}}

            [data-testid="stHeader"],
            [data-testid="stAppHeader"],
            [data-testid="stToolbar"],
            [data-testid="stSidebar"] {{background: var(--dp-bar-bg); box-shadow: var(--dp-bar-shadow); backdrop-filter: var(--dp-bar-blur); position: relative; overflow: hidden;}}

            [data-testid="stSidebar"] > div,
            [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{background: transparent !important;}}

            [data-testid="stHeader"]::before,
            [data-testid="stAppHeader"]::before,
            [data-testid="stToolbar"]::before,
            [data-testid="stSidebar"]::before {{content: ""; position: absolute; inset: 0; pointer-events: none; background: var(--dp-bar-overlay); opacity: 0.55;}}

            [data-testid="stHeader"]::after,
            [data-testid="stAppHeader"]::after,
            [data-testid="stToolbar"]::after,
            [data-testid="stSidebar"]::after {{content: ""; position: absolute; inset: 0; pointer-events: none; background: radial-gradient(circle at 18% 12%, rgba(255,255,255,0.20) 0%, rgba(255,255,255,0.00) 58%);}}

            [data-testid="stHeader"],
            [data-testid="stAppHeader"],
            [data-testid="stToolbar"] {{border-bottom: 1px solid rgba(255,255,255,0.20);}}

            .custom-topbar {{position: fixed; top: 0; left: 0; right: 0; height: {topbarHeightPx}px; background: linear-gradient(108deg, rgba(171,134,116,0.88) 0%, rgba(150,112,94,0.84) 58%, rgba(130,95,79,0.82) 100%); border-bottom: 1px solid rgba(255,255,255,0.22); display: flex !important; align-items: center; padding: 0 {topbarPaddingX}px; gap: {topbarGap}px; z-index: 2147483000; pointer-events: none; transition: padding-left 0.35s cubic-bezier(0.22, 1, 0.36, 1); backdrop-filter: blur(11px) saturate(160%); box-shadow: 0 10px 24px rgba(120,80,58,0.22), inset 0 1px 0 rgba(255,255,255,0.25); overflow: hidden; visibility: visible !important; opacity: 1 !important; box-sizing: border-box;}}
            .custom-topbar::before {{content: ""; position: absolute; inset: 0; pointer-events: none; background: linear-gradient(120deg, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.00) 46%); opacity: 0.55;}}
            .custom-topbar::after {{content: ""; position: absolute; inset: 0; pointer-events: none; background: radial-gradient(circle at 20% 10%, rgba(255,255,255,0.24) 0%, rgba(255,255,255,0.00) 56%);}}
            body:has([data-testid="stSidebar"][aria-expanded="true"]) .custom-topbar {{padding-left: {topbarLeftExpandedPx}px;}}
            body:has([data-testid="stSidebar"][aria-expanded="false"]) .custom-topbar {{padding-left: {topbarLeftCollapsedPx}px;}}
            .custom-topbar img {{position: relative; z-index: 1; height: {topbarLogoHeightPx}px; width: auto; filter: drop-shadow(0 0 8px rgba(255,255,255,0.48));}}
            .custom-topbar .topbar-title {{position: relative; z-index: 1; color: {Configuration.WhiteColor}; font-size: clamp(1.35rem, 1.15rem + 0.45vw, 1.7rem); font-weight: 700; letter-spacing: {Configuration.LetterSpacing2}; text-shadow: 0 0 16px rgba(255,255,255,0.35), 0 0 26px rgba(171,134,116,0.36); flex: 0 0 auto; white-space: nowrap;}}
            .topbar-live {{margin-left: auto; display: flex; align-items: center; gap: {Configuration.ScalePx(7)}px; color: {Configuration.WhiteColor}; font-size: {Configuration.FontSize3}; font-weight: 500; letter-spacing: {Configuration.LetterSpacing1}; white-space: nowrap; pointer-events: none; flex: 0 0 auto;}}
            .topbar-live-dot {{flex-shrink: 0; width: {Configuration.ScalePx(7)}px; height: {Configuration.ScalePx(7)}px; border-radius: 50%; background: #4ade80; animation: dp-live-pulse 2.4s ease-in-out infinite;}}

            /* Backup header text in case custom-topbar HTML is not mounted by the browser/runtime. */


            [data-testid="stSidebar"] {{border-right: 1px solid rgba(255,255,255,0.20);}}
            [data-testid="stSidebar"] * {{color: #FFFFFF !important; font-size: {Configuration.FontSize3} !important;}}

            [data-testid="stSidebar"] .sidebar-nav {{display: flex; flex-direction: column; gap: {Configuration.ScalePx(6)}px; padding-top: {Configuration.ScalePx(4)}px;}}
            [data-testid="stSidebar"] .sidebar-shell {{min-height: calc(100vh - 86px); display: flex; flex-direction: column;}}
            [data-testid="stSidebar"] .sidebar-nav-item {{display: block; text-decoration: none; color: #FFFFFF !important; border-radius: {buttonRadiusPx}px; padding: {Configuration.ScalePx(8)}px {Configuration.ScalePx(14)}px; font-size: {Configuration.FontSize3}; font-weight: 500; letter-spacing: {Configuration.LetterSpacing1}; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.05); transition: background 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease, border-color 0.25s ease;}}
            [data-testid="stSidebar"] .sidebar-nav-item:hover {{background: var(--dp-glass); border-color: rgba(255,255,255,0.14); box-shadow: var(--dp-shadow-glow), var(--dp-glow-primary); transform: translateX(2px);}}
            [data-testid="stSidebar"] .sidebar-nav-item.active {{background: var(--dp-glass-strong); border-color: rgba(255,255,255,0.26); box-shadow: 0 0 22px rgba(255,255,255,0.22), 0 8px 24px rgba(80,50,30,0.24), var(--dp-glow-primary); font-size: {Configuration.FontSize4}; font-weight: 700;}}
            [data-testid="stSidebar"] .sidebar-nav-item-content {{display: flex; align-items: center; gap: {Configuration.ScalePx(10)}px;}}
            [data-testid="stSidebar"] .sidebar-icon {{width: {Configuration.ScalePx(16)}px; height: {Configuration.ScalePx(16)}px; object-fit: contain; opacity: 0.96; transition: opacity 0.25s ease, transform 0.25s ease, filter 0.25s ease;}}
            [data-testid="stSidebar"] .sidebar-nav-item.active .sidebar-icon {{opacity: 1; transform: scale(1.08); filter: drop-shadow(0 0 6px rgba(255,255,255,0.28));}}

            [data-testid="stSidebar"][aria-expanded="false"] {{min-width: {sidebarCollapsedWidth}px !important; max-width: {sidebarCollapsedWidth}px !important; width: {sidebarCollapsedWidth}px !important; transform: translateX(0) !important;}}
            body:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stSidebar"] .sidebar-nav-item {{padding: {Configuration.ScalePx(9)}px 0; display: flex; justify-content: center; border-radius: {Configuration.ScalePx(14)}px;}}
            body:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stSidebar"] .sidebar-nav-item-content {{justify-content: center;}}
            body:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stSidebar"] .sidebar-nav-item-content span {{display: none;}}
            body:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stSidebar"] .sidebar-icon {{width: {Configuration.ScalePx(18)}px; height: {Configuration.ScalePx(18)}px;}}

            [data-testid="stSidebar"] .sidebar-footer {{margin-top: auto; padding: {Configuration.ScalePx(12)}px {Configuration.ScalePx(8)}px {Configuration.ScalePx(2)}px; border-top: 1px solid rgba(255,255,255,0.24); display: flex; flex-direction: column; gap: {Configuration.ScalePx(8)}px;}}
            [data-testid="stSidebar"] .sidebar-footer-item,
            [data-testid="stSidebar"] .sidebar-footer-link {{display: flex; align-items: center; gap: {Configuration.ScalePx(10)}px; text-decoration: none; color: #FFFFFF !important; border-radius: {buttonRadiusPx}px; padding: {Configuration.ScalePx(8)}px {Configuration.ScalePx(10)}px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); opacity: 0.96; transition: background 0.25s ease, opacity 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;}}
            [data-testid="stSidebar"] .sidebar-footer-link:hover {{background: rgba(255,255,255,0.16); box-shadow: 0 0 16px rgba(255,255,255,0.16), var(--dp-glow-primary); transform: translateX(1px); opacity: 1;}}
            [data-testid="stSidebar"] .sidebar-footer-icon {{width: {Configuration.ScalePx(15)}px; height: {Configuration.ScalePx(15)}px; object-fit: contain; opacity: 0.95;}}
            [data-testid="stSidebar"] .sidebar-footer-text {{font-size: {Configuration.FontSize2} !important; font-weight: 500; line-height: 1.2;}}

            body:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stSidebar"] .sidebar-footer {{align-items: center; padding-left: 0; padding-right: 0;}}
            body:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stSidebar"] .sidebar-footer-item,
            body:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stSidebar"] .sidebar-footer-link {{justify-content: center; padding: {Configuration.ScalePx(8)}px 0; width: {Configuration.ScalePx(44)}px; border-radius: {Configuration.ScalePx(14)}px;}}
            body:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stSidebar"] .sidebar-footer-text {{display: none;}}

            .stButton > button {{border-radius: {buttonRadiusPx}px; background: linear-gradient(95deg, {primaryColor} 0%, #b89483 100%); color: #FFFFFF; border: none; padding: {Configuration.ScalePx(10)}px {Configuration.ScalePx(24)}px; font-weight: 500; letter-spacing: {Configuration.LetterSpacing2}; transition: box-shadow 0.25s ease, transform 0.2s ease; box-shadow: var(--dp-shadow-soft), inset 0 1px 0 rgba(255,255,255,0.22);}}
            .stButton > button:hover {{box-shadow: 0 0 26px rgba(171,134,116,0.54), var(--dp-shadow-strong); transform: translateY(-2px);}}

            .stTextInput input, .stSelectbox > div, .stNumberInput input {{border-radius: {inputRadiusPx}px !important; border: 1px solid rgba(171,134,116,0.28) !important; background: rgba(255,255,255,0.72) !important; backdrop-filter: blur(8px); transition: box-shadow 0.25s ease, border-color 0.25s ease;}}
            .stTextInput input:focus, .stSelectbox > div:focus-within {{box-shadow: 0 0 0 3px rgba(171,134,116,0.20), 0 8px 20px rgba(171,134,116,0.12) !important; border-color: {primaryColor} !important;}}

            [data-testid="stDeckGlJsonChart"] {{ border-radius: {cardRadiusPx}px !important; overflow: hidden !important; box-shadow: 0 10px 34px rgba(171,134,116,0.18), 0 2px 8px rgba(171,134,116,0.10) !important; border: {borderWidthPx}px solid {borderColor} !important;}}

        </style>
        <script>
            (function() {{
                function syncTopbar() {{
                    var sidebar = document.querySelector('[data-testid="stSidebar"]');
                    var topbar  = document.querySelector('.custom-topbar');
                    if (!sidebar || !topbar) return;
                    var rawSidebarWidth = sidebar.offsetWidth || {Configuration.ScalePx(60)};
                    var maxSafeLeft = Math.max({Configuration.ScalePx(60)}, Math.floor((window.innerWidth || 0) * 0.45));
                    var sidebarWidth = Math.max({Configuration.ScalePx(60)}, Math.min(rawSidebarWidth, maxSafeLeft));
                    topbar.style.left = '0px';
                    topbar.style.paddingLeft = sidebarWidth + 'px';}}
                function syncViewport() {{
                    var widthBucket  = Math.round((window.innerWidth || 0) / 40) * 40;
                    var heightBucket = Math.round((window.innerHeight || 0) / 40) * 40;
                    if (!widthBucket || !heightBucket) return;

                    var params = new URLSearchParams(window.location.search);
                    var currentW = parseInt(params.get('vw') || '0', 10);
                    var currentH = parseInt(params.get('vh') || '0', 10);
                    if (currentW === widthBucket && currentH === heightBucket) return;

                    params.set('vw', String(widthBucket));
                    params.set('vh', String(heightBucket));
                    window.location.search = '?' + params.toString();}}
                function init() {{
                    syncTopbar();
                    syncViewport();
                    var sidebar = document.querySelector('[data-testid="stSidebar"]');
                    if (!sidebar) return;
                    new MutationObserver(syncTopbar).observe(sidebar, {{ attributes: true, attributeFilter: ['aria-expanded'] }});
                    window.addEventListener('resize', syncTopbar);
                    window.addEventListener('resize', function() {{
                        clearTimeout(window.__dpResizeTimer);
                        window.__dpResizeTimer = setTimeout(syncViewport, 200);}});}}
                if (document.readyState === 'loading') {{document.addEventListener('DOMContentLoaded', init);}} else {{
                    var attempts = 0;
                    var poll = setInterval(function() {{
                        if (document.querySelector('[data-testid="stSidebar"]') || ++attempts > 20) {{
                            clearInterval(poll);
                            init();}}}}, 100);}}}})();</script>""", unsafe_allow_html=True)

    st.markdown(
        f"""<div class="custom-topbar"><img src="data:image/png;base64,{logo}" /><span class="topbar-title">Domani Piove</span>{RenderUpdateIndicator(updateDate)}</div>""",
        unsafe_allow_html=True
    )

def RenderLayout(pageIconPaths = Configuration.PageIconPaths, footerIconPaths = Configuration.FooterIconPaths, pages = Configuration.Pages, updateDate = None):
    'Render styles and sidebar, then return the selected page key.'
    logo         = LoadLogo()
    sidebarIcons = LoadSidebarIcons(pageIconPaths)
    footerIcons  = LoadFooterIcons(footerIconPaths)
    RenderStyles(logo=logo, updateDate=updateDate)
    return RenderSidebar(sidebarIcons, footerIcons, pages)