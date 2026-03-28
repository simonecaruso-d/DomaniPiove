# Environment Setting
import html
from httpx import stream
import markdown
import numpy as np
from openai import OpenAI
import pandas as pd
import plotly.graph_objects as go
import re
import streamlit as st
import time

import configuration.ConfigurationStreamlit as Configuration

# CSS Templates
def PageStylesCss(animate=True):
    if animate:
        enterItemCss = f'opacity: 0; transform: translateY(28px); animation: forecastEnterUp {Configuration.AnimationDuration} {Configuration.AnimationEasing} forwards; will-change: opacity, transform;'
        delay1Css    = f'animation-delay: {Configuration.AnimationDelay1};'
        delay2Css    = f'animation-delay: {Configuration.AnimationDelay2};'
    else:
        enterItemCss = 'opacity: 1; transform: none;'
        delay1Css    = delay2Css = ''

    return f"""<style>
        .forecast-enter-item    {{ {enterItemCss} }}
        .forecast-enter-delay-1 {{ {delay1Css} }}
        .forecast-enter-delay-2 {{ {delay2Css} }}
        @keyframes forecastEnterUp {{ from {{ opacity: 0; transform: translateY(28px); }}
                                      to   {{ opacity: 1; transform: translateY(0); }} }}
        
        .filters-section-title {{color: {Configuration.Palette1VeryDark} !important; font-weight: {Configuration.FontWeight4} !important; font-size: {Configuration.FontSize5} !important; font-family: {Configuration.FontFamily} !important; letter-spacing: {Configuration.LetterSpacing2} !important; margin-bottom: {Configuration.Spacing2} !important; opacity: {Configuration.Opacity2} !important; line-height: {Configuration.LineHeight5} !important;}}
        .filter-label          {{color: {Configuration.Palette1VeryDark}; font-weight: {Configuration.FontWeight3}; font-size: {Configuration.FontSize1}; font-family: {Configuration.FontFamily}; letter-spacing: {Configuration.LetterSpacing1}; margin-bottom: {Configuration.Spacing0B}; opacity: {Configuration.Opacity1};}}

        /* ── Outer containers ── */
        div[data-testid="stSelectbox"],
        div[data-testid="stDateInput"],
        div[data-testid="stTextInput"],
        div[data-testid="stMultiSelect"] {{background: {Configuration.Palette1VeryDark} !important; backdrop-filter: blur(20px) saturate(1.6) !important; -webkit-backdrop-filter: blur(20px) saturate(1.6) !important; border-radius: 10px !important; padding: 0px 6px !important; border: none !important; outline: none !important; box-shadow: 0 1px 8px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.07) !important; transition: box-shadow 0.18s ease, transform 0.18s ease !important;}}
        div[data-testid="stSelectbox"]:focus-within,
        div[data-testid="stDateInput"]:focus-within,
        div[data-testid="stTextInput"]:focus-within,
        div[data-testid="stMultiSelect"]:focus-within {{box-shadow: 0 3px 16px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.11) !important; transform: translateY(-1px) !important;}}
        div[data-testid="stSelectbox"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stTextInput"] label,
        div[data-testid="stMultiSelect"] label {{display: none !important;}}

        /* ── Selectbox BaseWeb inner ── */
        div[data-testid="stSelectbox"] div[data-baseweb="select"],
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {{background: transparent !important; background-color: transparent !important; border: none !important; border-color: transparent !important; outline: none !important; box-shadow: none !important; min-height: 28px !important; height: 28px !important;}}
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child:hover,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child:focus {{background-color: transparent !important; border: none !important; border-color: transparent !important; box-shadow: none !important;}}
        div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] div {{font-size: {Configuration.FontSize1} !important; line-height: {Configuration.LineHeight2} !important; color: rgba(255,255,255,0.88) !important; font-family: {Configuration.FontFamily} !important; font-weight: {Configuration.FontWeight1} !important;}}

        /* ── MultiSelect BaseWeb inner ── */
        div[data-testid="stMultiSelect"] div[data-baseweb="select"],
        div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child {{background: transparent !important; background-color: transparent !important; border: none !important; border-color: transparent !important; outline: none !important; box-shadow: none !important; min-height: 28px !important;}}
        div[data-testid="stMultiSelect"] div[data-baseweb="select"] span,
        div[data-testid="stMultiSelect"] div[data-baseweb="select"] div {{font-size: {Configuration.FontSize1} !important; line-height: {Configuration.LineHeight2} !important; color: rgba(255,255,255,0.88) !important; font-family: {Configuration.FontFamily} !important; font-weight: {Configuration.FontWeight1} !important;}}
        div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{background-color: rgba(255,255,255,0.15) !important; border-radius: 6px !important; font-size: {Configuration.FontSize3} !important; font-family: {Configuration.FontFamily} !important; color: rgba(255,255,255,0.90) !important; padding: 1px 6px !important; margin: 1px !important;}}
        div[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg {{fill: rgba(255,255,255,0.55) !important; width: 10px !important; height: 10px !important;}}

        /* ── Date input inner ── */
        div[data-testid="stDateInput"] div[data-baseweb="input"],
        div[data-testid="stDateInput"] div[data-baseweb="base-input"] {{background: transparent !important; background-color: transparent !important; border: none !important; border-color: transparent !important; box-shadow: none !important; min-height: 28px !important; height: 28px !important;}}
        div[data-testid="stDateInput"] input {{color: rgba(255,255,255,0.88) !important; font-size: {Configuration.FontSize1} !important; font-family: {Configuration.FontFamily} !important; font-weight: {Configuration.FontWeight1} !important; padding: 0 4px !important;}}

        /* ── Icons ── */
        div[data-testid="stSelectbox"] svg,
        div[data-testid="stMultiSelect"] svg {{fill: rgba(255,255,255,0.35) !important; width: 14px !important; height: 14px !important;}}
        div[data-testid="stDateInput"] button,
        div[data-testid="stDateInput"] svg {{color: rgba(255,255,255,0.35) !important; fill: rgba(255,255,255,0.35) !important; width: 14px !important; height: 14px !important;}}

        /* ── Dropdown menu (selectbox + multiselect) ── */
        div[data-baseweb="popover"] ul,
        div[data-baseweb="menu"] {{background: {Configuration.Palette1VeryDark} !important; backdrop-filter: blur(28px) saturate(1.5) !important; border: none !important; border-radius: 10px !important; box-shadow: 0 8px 28px rgba(0,0,0,0.38) !important; padding: 4px !important;}}
        div[data-baseweb="menu"] li,
        div[data-baseweb="menu"] li * {{color: rgba(255,255,255,0.78) !important; font-size: {Configuration.FontSize3} !important; font-family: {Configuration.FontFamily} !important; background-color: transparent !important; border-radius: {Configuration.Spacing0B} !important; padding: 3px 8px !important; line-height: {Configuration.LineHeight2} !important;}}
        div[data-baseweb="menu"] li:hover {{background: rgba(255,255,255,0.09) !important;}}

        /* ── Calendario date picker ── */
        div[data-baseweb="calendar"] {{background: {Configuration.Palette1VeryDark} !important; border: none !important; border-radius: 10px !important; box-shadow: 0 8px 28px rgba(0,0,0,0.38) !important; font-family: {Configuration.FontFamily} !important;}}
        div[data-baseweb="calendar"] * {{font-size: {Configuration.FontSize3} !important; font-family: {Configuration.FontFamily} !important; color: rgba(255,255,255,0.85) !important;}}
        div[data-baseweb="calendar"] button {{font-size: {Configuration.FontSize3} !important; background: transparent !important; border: none !important; color: rgba(255,255,255,0.85) !important; border-radius: {Configuration.Spacing0B} !important;}}
        div[data-baseweb="calendar"] button:hover {{background: rgba(255,255,255,0.10) !important;}}
        div[data-baseweb="calendar"] [aria-selected="true"] button,
        div[data-baseweb="calendar"] [data-selected="true"] button {{background: rgba(255,255,255,0.22) !important; color: {Configuration.WhiteColor} !important; font-weight: {Configuration.FontWeight4} !important;}}
        div[data-baseweb="calendar"] [data-testid="CalendarHeader"] *,
        div[data-baseweb="calendar"] select {{font-size: {Configuration.FontSize3} !important; font-weight: {Configuration.FontWeight3} !important; color: rgba(255,255,255,0.90) !important; background: transparent !important; border: none !important;}}
    
        /* ── Grafico ── */
        div[data-testid="stPlotlyChart"] > div {{border-radius: {Configuration.Spacing4} !important; overflow: hidden !important; border: {Configuration.Spacing4} solid rgba({Configuration.Palette1VeryDark}, 0.10) !important; box-shadow: 0 4px 24px rgba({Configuration.Palette1VeryDark}, 0.06) !important; background: rgba(66, 103, 118, 0.005) !important;}}
        .chart-title {{color: {Configuration.Palette1VeryDark} !important; font-weight: {Configuration.FontWeight4} !important; font-size: {Configuration.FontSize5} !important; font-family: {Configuration.FontFamily} !important; letter-spacing: {Configuration.LetterSpacing2} !important; opacity: {Configuration.Opacity2} !important; line-height: {Configuration.LineHeight5} !important; margin-bottom: {Configuration.Spacing1} !important;}}
        .chart-subtitle {{color: {Configuration.Palette1VeryDark} !important; font-weight: {Configuration.FontWeight1} !important; font-size: {Configuration.FontSize3} !important; font-family: {Configuration.FontFamily} !important; opacity: {Configuration.Opacity0} !important; line-height: {Configuration.LineHeight2} !important; margin-bottom: {Configuration.Spacing2} !important;}}

        .llm-title {{color: {Configuration.PrimaryColor} !important; font-weight: {Configuration.FontWeight4} !important; font-size: {Configuration.FontSize5} !important; font-family: {Configuration.FontFamily} !important; letter-spacing: {Configuration.LetterSpacing2} !important; opacity: {Configuration.Opacity2} !important; line-height: {Configuration.LineHeight5} !important; margin-bottom: {Configuration.Spacing1} !important;}}
        .llm-subtitle {{color: {Configuration.PrimaryColor} !important; font-weight: {Configuration.FontWeight1} !important; font-size: {Configuration.FontSize3} !important; font-family: {Configuration.FontFamily} !important; opacity: {Configuration.Opacity0} !important; line-height: {Configuration.LineHeight2} !important; margin-bottom: {Configuration.Spacing2} !important;}}
        .llm-disclaimer {{color: {Configuration.PrimaryColor} !important; font-weight: {Configuration.FontWeight1} !important; font-size: {Configuration.FontSize1} !important; font-family: {Configuration.FontFamily} !important; opacity: {Configuration.Opacity1} !important; line-height: {Configuration.LineHeight3} !important; margin-top: {Configuration.Spacing1} !important;}}
    </style>"""

def ParameterFilterCss():
    return f"""<style>
        div[data-testid="stRadio"] > label {{display: none !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] {{display: flex !important; flex-wrap: wrap !important; gap: 6px !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] {{margin: 0 !important; padding: {Configuration.SpacingA} !important; border-radius: {Configuration.RadiusButton}px !important; border: {Configuration.WidthBorder}px solid transparent !important; background: {Configuration.PrimaryColor} !important; color: {Configuration.WhiteColor} !important; font-size: {Configuration.FontSize3} !important; font-family: {Configuration.FontFamily} !important; font-weight: {Configuration.FontWeight3} !important; transition: background-color 160ms ease, transform 160ms ease, box-shadow 160ms ease !important; cursor: pointer !important; display: flex !important; align-items: center !important; justify-content: center !important; text-align: center !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"]:hover {{background: {Configuration.Palette1Dark} !important; transform: translateY(-1px) !important; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12) !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {{display: none !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] > div:last-child {{margin: 0 !important; padding: 0 !important; width: 100% !important; display: flex !important; justify-content: center !important; align-items: center !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] input {{display: none !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] div {{color: inherit !important; font-size: {Configuration.FontSize3} !important; font-family: {Configuration.FontFamily} !important; text-align: center !important; width: 100% !important; margin: 0 !important; justify-content: center !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"],
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {{background: {Configuration.Palette1VeryDark} !important; color: {Configuration.WhiteColor} !important; box-shadow: 0 6px 14px rgba(47, 72, 88, 0.28) !important;}}
    </style>"""

def TitleCss():
    return f"""<style>
        .previsioni-title-fixed {{
            position: fixed; top: {Configuration.TitleTopPx}; left: {Configuration.TitleLeftCollapsedPx};
            margin: 0 !important; padding: 0 !important;
            color: {Configuration.PrimaryColor} !important; font-size: {Configuration.FontSize10} !important;
            line-height: {Configuration.LineHeight1} !important; font-weight: {Configuration.FontWeight4} !important;
            letter-spacing: {Configuration.LetterSpacing1} !important; font-family: {Configuration.FontFamily} !important;
            text-shadow: none !important; z-index: {Configuration.TitleZIndex};}}
        body:has([data-testid="stSidebar"][aria-expanded="true"])  .previsioni-title-fixed {{ left: {Configuration.TitleLeftExpandedPx}; }}
        body:has([data-testid="stSidebar"][aria-expanded="false"]) .previsioni-title-fixed {{ left: {Configuration.TitleLeftCollapsedPx}; }}
    </style><div class="previsioni-title-fixed">Previsioni</div>"""

def AlertCss():
    return f"""<style>
        div[data-testid="stAlert"] {{background-color: {Configuration.Palette1VeryDark} !important; border: none !important; border-radius: {Configuration.RadiusButton}px !important; box-shadow: none !important; outline: none !important;}}
        div[data-testid="stAlert"] > * {{background-color: {Configuration.Palette1VeryDark} !important; border: none !important; border-radius: {Configuration.RadiusButton}px !important; outline: none !important;}}
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] svg {{color: rgba(255,255,255,0.88) !important; fill: rgba(255,255,255,0.88) !important; font-family: {Configuration.FontFamily} !important; font-size: {Configuration.FontSize2} !important; font-weight: {Configuration.FontWeight4} !important;}}
    </style>"""

def TableCss():
    return f"""<style>
        /* Container con Scroll e Bordo Arrotondato */
        .scrollable-table-container {{max-height: {Configuration.HeightGraph}px; overflow-y: auto; overflow-x: hidden; border-radius: {Configuration.Spacing3} !important; border: {Configuration.WidthBorder}px solid rgba(255, 255, 255, 0.1); background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);}}
        .styled-table {{width: 100%; border-collapse: collapse; font-family: {Configuration.FontFamily}; background-color: transparent;}}

        /* Header: Sfondo scuro (o accent) e TESTO BIANCO */
        .styled-table th {{position: sticky; top: 0; background-color: {Configuration.Palette1VeryDark} !important; color: {Configuration.WhiteColor} !important; font-size: {Configuration.FontSize1} !important; font-weight: {Configuration.FontWeight3}; text-align: left; padding: 10px 12px !important; z-index: 2; letter-spacing: {Configuration.LetterSpacing2};}}

        /* Celle: Testo piccolo e scuro (o coerente con palette) */
        .styled-table td {{color: {Configuration.Palette1VeryDark} !important; font-size: {Configuration.FontSize1} !important; padding: 8px 12px !important; border-bottom: {Configuration.WidthBorder}px solid rgba(0,0,0,0.05); background-color: rgba(255, 255, 255, 0.4);}}

        /* Scrollbar sottile per non rovinare il design */
        .scrollable-table-container::-webkit-scrollbar {{ width: {Configuration.Spacing0B}; }}
        .scrollable-table-container::-webkit-scrollbar-thumb {{ background: rgba(0,0,0,0.1); border-radius: {Configuration.Spacing1}; }}
    </style>"""

def ConciergeCSS():
    st.markdown(f"""<style>
    /* ── Container risposta LLM ── */
    .concierge-container {{height: {Configuration.HeightGraph}px !important; overflow-y: auto !important; overflow-x: hidden !important; padding: 14px 16px !important; background: rgba(255, 255, 255, 0.6) !important; backdrop-filter: blur(10px) !important; border-radius: {Configuration.Spacing3} !important; border: {Configuration.WidthBorder}px solid rgba(0, 111, 96, 0) !important; margin-top: {Configuration.Spacing1} !important; box-sizing: border-box !important;}}
    .concierge-container,
    .concierge-container * {{color: {Configuration.PrimaryColor} !important; font-family: {Configuration.FontFamily} !important; font-size: {Configuration.FontSize2} !important; line-height: {Configuration.LineHeight3} !important;}}
    .concierge-container p {{margin: 0 0 0.55rem 0 !important;}}
    .concierge-container ul,
    .concierge-container ol {{margin: 0 0 0.55rem 0 !important; padding-left: 1.35rem !important;}}
    .concierge-container li {{margin: 0.18rem 0 !important; padding-left: 0.15rem !important;}}
    .concierge-container ul {{list-style-type: disc !important;}}
    .concierge-container ol {{list-style-type: decimal !important;}}
    .concierge-container ul ul,
    .concierge-container ul ol,
    .concierge-container ol ul,
    .concierge-container ol ol {{margin-top: 0.2rem !important; margin-bottom: 0.35rem !important; padding-left: 1.25rem !important;}}
    .concierge-container ul ul {{list-style-type: circle !important;}}
    .concierge-container ul ul ul {{list-style-type: square !important;}}
    .concierge-container h1,
    .concierge-container h2,
    .concierge-container h3,
    .concierge-container h4,
    .concierge-container h5,
    .concierge-container h6 {{margin: 0 0 0.45rem 0 !important; line-height: {Configuration.LineHeight2} !important;}}
    .concierge-container::-webkit-scrollbar       {{ width: {Configuration.Spacing0B}; }}
    .concierge-container::-webkit-scrollbar-thumb {{ background: rgba(0,0,0,0.12); border-radius: {Configuration.Spacing1}; }}

    /* ── Bottone ── */
    div[data-testid="stColumn"] button[kind="secondary"],
    div[data-testid="stColumn"] button[kind="primary"],
    div[data-testid="stColumn"] div[data-testid="stButton"] > button,
    div[data-testid="stColumn"] .stButton > button {{background-color: {Configuration.PrimaryColor} !important; color: {Configuration.WhiteColor} !important; border: none !important; width: 100% !important; font-family: {Configuration.FontFamily} !important; font-size: {Configuration.FontSize2} !important; font-weight: {Configuration.FontWeight3} !important; border-radius: {Configuration.RadiusButton}px !important; transition: background-color 160ms ease, transform 160ms ease, box-shadow 160ms ease !important;}}
    div[data-testid="stColumn"] button[kind="secondary"]:hover,
    div[data-testid="stColumn"] button[kind="primary"]:hover,
    div[data-testid="stColumn"] div[data-testid="stButton"] > button:hover,
    div[data-testid="stColumn"] .stButton > button:hover {{background-color: {Configuration.PrimaryColor} !important; transform: translateY(-1px) !important; box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;}}

    /* ── Spinner ── */
    [data-testid="stStatusWidget"],
    [data-testid="stSpinner"],
    div[aria-live="polite"],
    div[aria-live="assertive"] {{background-color: {Configuration.PrimaryColor} !important; border-radius: {Configuration.Spacing2} !important; padding: {Configuration.SpacingA} !important;}}
    [data-testid="stStatusWidget"] *,
    [data-testid="stSpinner"] *,
    div[aria-live="polite"] *,
    div[aria-live="assertive"] * {{color: {Configuration.WhiteColor} !important; font-family: {Configuration.FontFamily} !important; font-size: {Configuration.FontSize3} !important;}}
    [data-testid="stStatusWidget"] svg path,
    [data-testid="stSpinner"] svg path,
    div[aria-live="polite"] svg path,
    div[aria-live="assertive"] svg path {{fill: {Configuration.WhiteColor} !important; stroke: {Configuration.WhiteColor} !important;}}

    /* ── Empty slot wrapper ── */
    div[data-testid="stEmpty"] > div {{border-radius: {Configuration.Spacing3} !important; overflow: hidden !important;}}
    </style>""", unsafe_allow_html=True)

def RenderConciergeMarkdownContainer(text):
    normalizedText = (text or '').replace('\r\n', '\n').replace('\r', '\n')
    normalizedText = re.sub(r'(?<=\S)\s+(?=[*+]\s)', '\n', normalizedText)
    normalizedText = re.sub(r'(?<=\S)\s+(?=\d+\.\s)', '\n', normalizedText)
    normalizedText = re.sub(r'(^|\n)([*+-])(?=\S)', r'\1\2 ', normalizedText)

    dayPartLabels = {'Mattina', 'Pranzo', 'Pomeriggio', 'Cena', 'Sera', 'Notte', 'Sera/Notte'}
    structuredLines = []
    insideDayPartSection = False
    lastNestedBulletIndex = None
    for rawLine in normalizedText.split('\n'):
        line = rawLine.rstrip()
        strippedLine = line.strip()
        bulletMatch = re.match(r'^(?:[*+-]|\d+\.)\s+(.*)$', strippedLine)

        if bulletMatch:
            itemText = bulletMatch.group(1).strip()
            itemLabel = itemText.rstrip(':').strip()
            if itemLabel in dayPartLabels:
                suffix = ':' if itemText.endswith(':') else ''
                structuredLines.append(f'* **{itemLabel}**{suffix}')
                insideDayPartSection = True
                lastNestedBulletIndex = None
            elif insideDayPartSection:
                structuredLines.append(f'    * {itemText}')
                lastNestedBulletIndex = len(structuredLines) - 1
            else:
                structuredLines.append(strippedLine)
                lastNestedBulletIndex = None
            continue

        if strippedLine and insideDayPartSection and lastNestedBulletIndex is not None and not strippedLine.startswith(('#', '_')):
            structuredLines[lastNestedBulletIndex] = f"{structuredLines[lastNestedBulletIndex]} {strippedLine}"
            continue

        structuredLines.append(line)
        if not strippedLine:
            lastNestedBulletIndex = None
        elif strippedLine.startswith(('#', '_')):
            lastNestedBulletIndex = None
        else:
            insideDayPartSection = False
            lastNestedBulletIndex = None

    normalizedText = '\n'.join(structuredLines)

    normalizedLines = []
    previousMeaningfulLine = ''
    for rawLine in normalizedText.split('\n'):
        line = rawLine.rstrip()
        strippedLine = line.strip()
        isBlank = strippedLine == ''
        isHeading = strippedLine.startswith('#')
        isListItem = bool(re.match(r'^(?:[*+-]\s|\d+\.\s)', strippedLine))

        if isHeading and normalizedLines and normalizedLines[-1] != '': normalizedLines.append('')

        if isListItem and previousMeaningfulLine and not re.match(r'^(?:[*+-]\s|\d+\.\s|#)', previousMeaningfulLine):
            if normalizedLines and normalizedLines[-1] != '': normalizedLines.append('')

        if not isListItem and previousMeaningfulLine and re.match(r'^(?:[*+-]\s|\d+\.\s)', previousMeaningfulLine) and not isBlank:
            if normalizedLines and normalizedLines[-1] != '': normalizedLines.append('')

        normalizedLines.append(line)

        if not isBlank: previousMeaningfulLine = strippedLine

    normalizedText = '\n'.join(normalizedLines)

    safeText     = html.escape(normalizedText)
    renderedHtml = markdown.markdown(safeText, extensions=['extra', 'sane_lists'])
    return f'<div class="concierge-container">{renderedHtml}</div>'

# Title
def RenderTitle():
    st.markdown(TitleCss(), unsafe_allow_html=True)

# Parameter Filter
def RenderParameterFilter():
    st.markdown(ParameterFilterCss(), unsafe_allow_html=True)
    st.markdown('<div class="filters-section-title">Seleziona un fenomeno meteorologico:</div>', unsafe_allow_html=True)
    selectedParameter = st.radio('Parametro', options=Configuration.Parameters, horizontal=True, index=0, key='accuracy_parameter_filter', label_visibility='collapsed')
    return selectedParameter

# Value Filters
def RenderCitySelectbox(city):
    cityOptions = city.sort_values(['State', 'City'])
    treeOptions = [None]
    treeLabels  = {None: 'Seleziona città'}

    for state, group in cityOptions.groupby('State', sort=True):
        regionKey = f'__region__{state}'
        treeOptions.append(regionKey)
        treeLabels[regionKey] = f'{state}'
        for _, row in group.iterrows():
            key             = f'__city__{row["Id"]}'
            treeOptions.append(key)
            treeLabels[key] = f'\u2003{row["City"]}'

    citySelectedKey = st.selectbox('Città', options=treeOptions, format_func=lambda k: treeLabels.get(k, k), key='filterCity', label_visibility='collapsed')
    return (int(citySelectedKey.replace('__city__', '')) if citySelectedKey and citySelectedKey.startswith('__city__') else None)

def RenderDateRangeInput(forecasts):
    today           = pd.Timestamp.now(tz='Europe/Rome').date()
    nextWeek        = (pd.Timestamp(today) + pd.Timedelta(days=6)).date()
    forecastsDt     = pd.to_datetime(forecasts['Datetime'], errors='coerce')
    minForecastDate = forecastsDt.min().date()
    maxForecastDate = forecastsDt.max().date()
    return st.date_input('Intervallo date', value=(today, nextWeek), min_value=minForecastDate, max_value=maxForecastDate, key='filterDate', label_visibility='collapsed', format='DD/MM/YYYY')

def RenderPartOfDayMultiselect(calendar):
    partOfDayOptionsENRaw = calendar['PartOfDay'].unique()
    partOfDayOptionsEN    = [p for p in Configuration.PartOfDayOrder if p in partOfDayOptionsENRaw]
    partOfDayOptionsIT    = [Configuration.PartOfDayToIta.get(p, p) for p in partOfDayOptionsEN]

    partOfDaySelectedIT = st.multiselect('Parte del giorno', options=partOfDayOptionsIT, default=[], placeholder='Tutte', key='filterPartOfDay', label_visibility='collapsed')
    return (None if not partOfDaySelectedIT else [Configuration.PartOfDayToEng.get(v, v) for v in partOfDaySelectedIT])

def RenderProviderMultiselect(forecasts):
    providerOptions     = sorted(forecasts['Provider'].unique())
    providerSelectedRaw = st.multiselect('Provider', options=providerOptions, default=[], placeholder='Tutte', key='filterProvider', label_visibility='collapsed')
    return None if not providerSelectedRaw else providerSelectedRaw

def RenderRetrievalDateSelectbox(forecasts):
    retrievalDates = sorted(pd.to_datetime(forecasts['RetrievalDatetime'].unique()), reverse=True)
    return st.selectbox('Data Previsione', options=retrievalDates, format_func=lambda d: d.strftime('%d/%m/%Y'), index=0, key='filterRetrievalTime', label_visibility='collapsed')

def RenderValueFilters(city, calendar, forecasts, animate=True):
    st.markdown(PageStylesCss(animate=animate), unsafe_allow_html=True)
    st.markdown("<div class='filters-section-title'>Scegli cosa prevedere:</div>", unsafe_allow_html=True)

    columns = st.columns([2, 2, 2, 2, 2])

    with columns[0]:
        st.markdown("<div class='filter-label'>Città</div>", unsafe_allow_html=True)
        cityIdSelected = RenderCitySelectbox(city)

    with columns[1]:
        st.markdown("<div class='filter-label'>Intervallo date</div>", unsafe_allow_html=True)
        dateSelected = RenderDateRangeInput(forecasts)

    with columns[2]:
        st.markdown("<div class='filter-label'>Parte del giorno</div>", unsafe_allow_html=True)
        partOfDaySelected = RenderPartOfDayMultiselect(calendar)

    with columns[3]:
        st.markdown("<div class='filter-label'>Provider</div>", unsafe_allow_html=True)
        providerSelected = RenderProviderMultiselect(forecasts)

    with columns[4]:
        st.markdown("<div class='filter-label'>Data Previsione</div>", unsafe_allow_html=True)
        retrievalTimeSelected = RenderRetrievalDateSelectbox(forecasts)

    return {'cityId': cityIdSelected, 'dateRange': dateSelected, 'partOfDay': partOfDaySelected, 'provider': providerSelected, 'retrievalDatetime': retrievalTimeSelected}

def RenderNoCityAlert():
    st.markdown(AlertCss(), unsafe_allow_html=True)
    st.info('📍 Seleziona una città per visualizzare le previsioni.')
    st.stop()

# Data Helpers
def BuildDf(city, calendar, forecasts):
    calendar.drop(columns=['CreatedAt', 'UpdatedAt'], inplace=True, errors='ignore')
    city.drop(columns=['Province', 'Country', 'Region', 'Latitude', 'Longitude', 'CreatedAt', 'UpdatedAt'], inplace=True, errors='ignore')
    forecasts.drop(columns=['Id', 'CreatedAt', 'UpdatedAt'], inplace=True, errors='ignore')
    forecasts = forecasts.merge(city, left_on='CityId', right_on='Id', how='left').drop(columns=['Id'])
    forecasts = forecasts.merge(calendar, left_on='Datetime', right_on='Datetime', how='left')
    return forecasts

def FilterDf(df, selectedFilters):
    if selectedFilters['cityId'] is not None           : df = df[df['CityId'] == selectedFilters['cityId']]
    if selectedFilters['partOfDay'] is not None        : df = df[df['PartOfDay'].isin(selectedFilters['partOfDay'])]
    if selectedFilters['provider'] is not None         : df = df[df['Provider'].isin(selectedFilters['provider'])]
    if selectedFilters['retrievalDatetime'] is not None: df = df[pd.to_datetime(df['RetrievalDatetime']) == pd.to_datetime(selectedFilters['retrievalDatetime'])]
    if selectedFilters['dateRange'] is not None and len(selectedFilters['dateRange']) == 2:
        startDate, endDate = selectedFilters['dateRange']
        df = df[(pd.to_datetime(df['Datetime']).dt.date >= startDate) & (pd.to_datetime(df['Datetime']).dt.date <= endDate)]

    df = df[df['IsCurrent'] == 'Y']
    df.drop(columns=['IsCurrent'], inplace=True, errors='ignore')
    return df.reset_index(drop=True)

def FilterAccuracyByProvider(df, selectedFilters):
    if selectedFilters['provider'] is not None : df = df[df['Provider'].isin(selectedFilters['provider'])]
    return df.reset_index(drop=True)

# Graph
def HexToRgb(hex):
    hex     = hex.lstrip('#')
    r, g, b = int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)
    return f'{r},{g},{b}'

def InterpolateColor(hexA, hexB, t):
    hexA, hexB = hexA.lstrip('#'), hexB.lstrip('#')
    rA, gA, bA = int(hexA[0:2], 16), int(hexA[2:4], 16), int(hexA[4:6], 16)
    rB, gB, bB = int(hexB[0:2], 16), int(hexB[2:4], 16), int(hexB[4:6], 16)
    r          = int(rA + (rB - rA) * t)
    g          = int(gA + (gB - gA) * t)
    b          = int(bA + (bB - bA) * t)
    return f'#{r:02x}{g:02x}{b:02x}'

def PaletteColor(t, palette=[Configuration.Palette1VeryDark, Configuration.Palette1Dark, Configuration.Palette1Medium, Configuration.Palette1Light, Configuration.Palette1VeryLight]):
        t     = max(0.0, min(1.0, t))
        idx   = t * (len(palette) - 1)
        iLow  = int(idx)
        iHigh = min(iLow + 1, len(palette) - 1)
        return InterpolateColor(palette[iLow], palette[iHigh], idx - iLow)

def RenderForecastLineChart(df, selectedParameter, selectedFilters, forecastAccuracyByProvider, animate=True):
    animationClass = 'forecast-enter-delay-1' if animate else ''
    
    column = Configuration.ParametersEng2.get(selectedParameter)
    unit   = Configuration.ParametersMeasureUnits.get(selectedParameter, '')
    scale  = Configuration.ParametersScale.get(selectedParameter, 1)

    df             = df.copy()
    df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
    df[column]     = pd.to_numeric(df[column], errors='coerce') * scale

    accuracySubset           = forecastAccuracyByProvider[forecastAccuracyByProvider['Metric'].str.casefold() == column.casefold()].copy()
    accuracySubset           = FilterAccuracyByProvider(accuracySubset, selectedFilters)
    accuracySubset['MAE']    = pd.to_numeric(accuracySubset['MAE'], errors='coerce')
    accuracySubset           = accuracySubset.dropna(subset=['MAE'])
    accuracySubset['Weight'] = 1 / accuracySubset['MAE'].replace(0, float('nan'))
    totalWeight              = accuracySubset['Weight'].sum()
    accuracySubset['Weight'] = accuracySubset['Weight'] / totalWeight
    weights                  = accuracySubset.set_index('Provider')['Weight'].to_dict()
    if weights: df['_weight'] = df['Provider'].map(weights).fillna(0)
    else:       df['_weight'] = 1.0
  
    df                    = df.drop_duplicates(subset=['Datetime', 'Provider'])
    df['_weighted_value'] = df[column] * df['_weight']
    aggregated            = (df.groupby('Datetime', as_index=False).apply(lambda g: pd.Series({
                            'Value': g['_weighted_value'].sum() / g['_weight'].sum() if g['_weight'].sum() > 0 else float('nan'),
                            'ProviderInfo': '<br>'.join(f"{r['Provider']} ({(r['_weight'] / g['_weight'].sum()):.0%})" for _, r in g.iterrows() if r['_weight'] > 0)}), include_groups=False)
                            .sort_values('Datetime').reset_index(drop=True))

    valueMin        = aggregated['Value'].min()
    valueMax        = aggregated['Value'].max()    
    normalizedValue = lambda value: (value - valueMin) / (valueMax - valueMin) if valueMax > valueMin else 0.5

    st.markdown(f"<div class='chart-title forecast-enter-item {animationClass}'>{selectedParameter}</div>"
                f"<div class='chart-subtitle forecast-enter-item {animationClass}'>Andamento previsto</div>", unsafe_allow_html=True)

    figure = go.Figure()

    for i in range(len(aggregated) - 1):
        valueMid  = (aggregated['Value'].iloc[i] + aggregated['Value'].iloc[i+1]) / 2
        color     = PaletteColor(normalizedValue(valueMid))
        figure.add_trace(go.Scatter(
            x          = [aggregated['Datetime'].iloc[i], aggregated['Datetime'].iloc[i+1], aggregated['Datetime'].iloc[i+1], aggregated['Datetime'].iloc[i]],
            y          = [aggregated['Value'].iloc[i], aggregated['Value'].iloc[i+1], 0, 0],
            fill       = 'toself',
            fillcolor  = f'rgba({HexToRgb(color)}, 0.40)',
            line       = dict(color='rgba(0,0,0,0)', width=0),
            hoverinfo  = 'skip',
            showlegend = False))

    figure.add_trace(go.Scatter(
        x             = aggregated['Datetime'],
        y             = aggregated['Value'],
        mode          = 'lines',
        line          = dict(color='rgba(0,0,0,0)', width=0),
        customdata    = aggregated['ProviderInfo'],
        hovertemplate = (
            f'<span style="color:{Configuration.WhiteColor};">{selectedParameter}:&nbsp;<b>%{{y:.1f}}{unit}</b></span><br>'
            f'<br>'
            f'<span style="color:rgba(255,255,255,0.6);font-size:11px;">%{{customdata}}</span>'
            f'<extra></extra>'),
        showlegend    = False))

    figure.update_layout(
        paper_bgcolor        = f'rgba({HexToRgb(Configuration.AccentColor)}, 0.04)',
        plot_bgcolor         = 'rgba(0,0,0,0)',
        margin               = dict(l=Configuration.ScalePx(64), r=Configuration.ScalePx(16), t=Configuration.ScalePx(16), b=Configuration.ScalePx(16)),
        height               = Configuration.HeightGraph,
        font                 = dict(family=Configuration.FontFamily, size=Configuration.ScalePx(10), color=Configuration.Palette1VeryDark),
        xaxis                = dict(showgrid = True, gridcolor = f'rgba({HexToRgb(Configuration.Palette1VeryDark)}, 0.03)', gridwidth = 1, zeroline = False, tickformat = '%d %b\n%H:%M', tickfont = dict(size=Configuration.ScalePx(11), color=Configuration.Palette1VeryDark), showline = False, ticks = ''),
        yaxis                = dict(showgrid = True, gridcolor = f'rgba({HexToRgb(Configuration.Palette1VeryDark)}, 0.03)', gridwidth = 1, zeroline = False, ticksuffix = f' {unit}', tickfont = dict(size=Configuration.ScalePx(11), color=Configuration.Palette1VeryDark), showline = False, ticks = ''),
        hoverlabel           = dict(bgcolor = Configuration.Palette1VeryDark, bordercolor = Configuration.Palette1Dark, font_size = Configuration.ScalePx(12), font_family = Configuration.FontFamily, font_color = Configuration.WhiteColor, namelength = -1),
        hovermode            = 'x unified',
        showlegend           = False)

    st.plotly_chart(figure, use_container_width=True, config={'displayModeBar': False})

# Table
def GroupDf(df):
    df['Datetime'] = pd.to_datetime(df['Datetime']).dt.normalize()
    groupByColumns = ['Datetime', 'PartOfDay']
    valueColumn    = ['Temperature', 'FeltTemperature', 'Humidity', 'Visibility', 'PrecipitationProbability', 'Rain', 'Snowfall', 'CloudCover', 'WindSpeed']
    df             = df.groupby(groupByColumns)[valueColumn].mean().reset_index()
    return df

def ApplySeasonalLogic(row, weights=Configuration.ScoresWeights):
    month = row['Datetime'].month
    if month in [6, 7, 8]      : p = Configuration.ThresholdsSummer
    elif month in [12, 1, 2]   : p = Configuration.ThresholdsWinter
    elif month in [3, 4, 5]    : p = Configuration.ThresholdsSpring
    else                       : p = Configuration.ThresholdsFall
    
    scoreVisibility               = 1 if row['Visibility'] > p['VisibilityThreshold'] else max(0, row['Visibility'] / p['VisibilityThreshold'])
    scorePrecipitationProbability = 1 if row['PrecipitationProbability'] < p['PrecipProbThreshold'] else max(0, 1 - (row['PrecipitationProbability'] - p['PrecipProbThreshold']) / (1 - p['PrecipProbThreshold']))
    scoreRain                     = 1 if row['Rain'] < p['RainFreeMm'] else max(0, 1 - (row['Rain'] - p['RainFreeMm']) / p['RainMaxTolerance'])
    scoreSnowfall                 = 1 if row['Snowfall'] < p['SnowMaxTolerance'] else max(0, 1 - row['Snowfall'] / p['SnowMaxTolerance'])
    scoreWind                     = 1 if row['WindSpeed'] < p['WindThreshold'] else max(0, 1 - (row['WindSpeed'] - p['WindThreshold']) / p['WindThreshold'])
    scoreFeltTemperature          = np.exp(-(max(0, abs(row['Temperature'] - p['TempTarget']) - 2)**2) / (2 * p['TempTolerance']**2))
    scoreHumidity                 = np.exp(-(max(0, abs(row['Humidity'] - p['HumidityTarget']) - 0.05)**2) / (2 * 0.25**2))
    scoreCloudCover               = 1 - (row['CloudCover'])**p['CloudImpactExp']
    scorePrecipitationProbability = scorePrecipitationProbability**p['PrecipitationPenaltyExp']
    scoreRain                     = scoreRain**p['RainPenaltyExp']

    comfortScore   = (scoreFeltTemperature * weights['ScoreFeltTemperature'] + scoreCloudCover * weights['ScoreCloudCover'] + scorePrecipitationProbability * weights['ScorePrecipitationProbability'] + scoreWind * weights['ScoreWind'] + scoreVisibility * weights['ScoreVisibility'] + scoreHumidity * weights['ScoreHumidity'])
    weatherBlocker = min(scoreRain, scoreSnowfall)
    cloudRainPenalty = 1 - (p['CloudRainInteractionWeight'] * ((1 - scoreCloudCover) * (1 - scorePrecipitationProbability)))
    finalScore = np.clip(comfortScore * weatherBlocker * cloudRainPenalty, 0, 1)
    
    return pd.Series({
        'ScorePrecipitationProbability': scorePrecipitationProbability,
        'ScoreRain'                    : scoreRain,
        'ScoreSnowfall'                : scoreSnowfall,
        'ScoreCloudCover'              : scoreCloudCover,
        'ScoreHumidity'                : scoreHumidity,
        'ScoreWind'                    : scoreWind,
        'ScoreVisibility'              : scoreVisibility,
        'ScoreFeltTemperature'         : scoreFeltTemperature,
        'FinalScore'                   : round(finalScore, 2)})

def CalculateScore(df):
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    return pd.concat([df, df.apply(ApplySeasonalLogic, axis=1)], axis=1)

def GetStatus(score):
        if score >= 0.7: return '🟢 Vai, esci!'
        if score >= 0.4: return '🟡 Esci, ma fai attenzione'
        return                  '🔴 Forse è meglio restare a casa?'

def GetMotivation(row):
    if row['FinalScore'] >= 0.7: return ''
        
    labels = {
        'ScoreFeltTemperature': 'Temperatura sgradevole',
        'ScoreCloudCover': 'Cielo troppo coperto',
        'ScoreWind': 'Vento eccessivo',
        'ScorePrecipitationProbability': 'Alto rischio di pioggia',
        'ScoreVisibility': 'Scarsa visibilità',
        'ScoreRain': 'Pioggia in arrivo',
        'ScoreSnowfall': 'Neve in arrivo',
        'ScoreHumidity': 'Umidità fastidiosa'}
    
    scores            = row[list(labels.keys())]
    worstTwo          = scores.sort_values().head(2)
    motivations       = [labels[idx] for idx, val in worstTwo.items() if val < 0.8]
    if not motivations: return 'Condizioni variabili'
        
    return ' <br> '.join(motivations)

def CreateSummary(df):
    summaryDf = df.copy()
    weekdayNamesIt = {0: 'Lunedi', 1: 'Martedi', 2: 'Mercoledi', 3: 'Giovedi', 4: 'Venerdi', 5: 'Sabato', 6: 'Domenica'}

    summaryDf['PartOfDay'] = pd.Categorical(summaryDf['PartOfDay'], categories=Configuration.PartOfDayOrder, ordered=True)
    summaryDf = summaryDf.sort_values(by=['Datetime', 'PartOfDay'])

    summaryDf['Datetime']               = pd.to_datetime(summaryDf['Datetime'])
    summaryDf['Data']                   = summaryDf['Datetime'].dt.strftime('%d/%m/%Y')
    summaryDf['Giorno della settimana'] = summaryDf['Datetime'].dt.dayofweek.map(weekdayNamesIt)
    summaryDf['Parte del giorno']       = summaryDf['PartOfDay'].map(Configuration.PartOfDayToIta)
    summaryDf['Punteggio']              = summaryDf['FinalScore'].apply(lambda x: f'{100*x:.0f}%')
    summaryDf['Indicazione']            = summaryDf['FinalScore'].apply(lambda x: GetStatus(x))
    summaryDf['Motivo Principale']      = summaryDf.apply(GetMotivation, axis=1)

    return summaryDf[['Data', 'Giorno della settimana', 'Parte del giorno', 'Punteggio', 'Indicazione', 'Motivo Principale']]

def RenderForecastTable(df, animate=True):
    animationClass = 'forecast-enter-delay-1' if animate else ''
    st.markdown(TableCss(), unsafe_allow_html=True)
    summary        = CreateSummary(df)
    tableHtml      = summary.to_html(index=False, classes='styled-table', escape=False)
    st.markdown(f"<div class='scrollable-table-container forecast-enter-item {animationClass}'>{tableHtml}</div>", unsafe_allow_html=True)

# LLM
def BuildLlmModelSequence(defaultModel, fallbackModels):
    cachedModel   = st.session_state.get('_llm_last_successful_model')
    modelSequence = [cachedModel, defaultModel, *(fallbackModels or [])]

    uniqueModels = []
    for currentModel in modelSequence:
        if currentModel and currentModel not in uniqueModels: uniqueModels.append(currentModel)

    return uniqueModels

def IsRetryableLlmError(error):
    errorText = str(error).lower()
    return any(token in errorText for token in ['429', 'rate limit', 'rate-limit', 'rate_limited', 'temporarily rate-limited', 'temporarily rate limited', 'too many requests', 'connection error', 'timed out', 'timeout'])

def BuildFriendlyLlmError(error):
    if IsRetryableLlmError(error): return '⚠️ Il provider AI è temporaneamente occupato. Riprova tra qualche secondo.'
    return f'⚠️ Errore nella generazione dei consigli: {str(error)}'

def GenerateLLMComment(cityName, staticEventsTable, summaryTable,
                       orApiKey=Configuration.OpenRouterKey, model=Configuration.ModelF, 
                       fallbackModels=Configuration.LlmFallbackModels, maxRetries=Configuration.LlmMaxRetries, retryDelaySeconds=Configuration.LlmRetryDelaySeconds,
                       systemPrompt=Configuration.LLMPrompt, maxTokens=Configuration.MaxTokens, temperature=Configuration.Temperature, topP=Configuration.TopP):   
    try:        
        mostCommonMotivation   = summaryTable.groupby('Indicazione')['Motivo Principale'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else 'Condizioni variabili')
        motivationByIndication = {indication: mostCommonMotivation.get(indication, 'Condizioni variabili') for indication in summaryTable['Indicazione'].unique()}
        
        filledPrompt = systemPrompt.format(city = cityName, staticEventsTable = staticEventsTable, mostCommonMotivation = motivationByIndication, outputStructureMarkdown = Configuration.LLMResponseStructure)
        client       = OpenAI(base_url='https://openrouter.ai/api/v1', api_key=orApiKey)
        lastError    = None

        for currentModel in BuildLlmModelSequence(model, fallbackModels):
            for attempt in range(1, maxRetries + 1):
                streamedAnyChunk = False

                try:
                    stream = client.chat.completions.create(model = currentModel, max_tokens=maxTokens, temperature = temperature, top_p = topP, stream = True, messages = [{'role': 'user', 'content': filledPrompt}])
                    for chunk in stream:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            streamedAnyChunk = True
                            yield delta

                    st.session_state['_llm_last_successful_model'] = currentModel
                    return
                except Exception as currentError:
                    lastError = currentError
                    print(f'[LLM] Model {currentModel} failed on attempt {attempt}: {currentError}')

                    if streamedAnyChunk:
                        yield '\n\n⚠️ La risposta si è interrotta durante la generazione. Riprova tra qualche secondo.'
                        return

                    if IsRetryableLlmError(currentError) and attempt < maxRetries:
                        time.sleep(retryDelaySeconds * attempt)
                        continue

                    break

        if lastError is not None:
            yield BuildFriendlyLlmError(lastError)
            return

    except Exception as e: yield BuildFriendlyLlmError(e)

# Wrapper
def RenderFirstPart(forecasts, selectedParameter, selectedFilters, forecastAccuracyByProvider, animate):
    st.markdown(f"<div style='height:{Configuration.Spacing4};'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='height:1px; background: rgba({HexToRgb(Configuration.Palette1VeryDark)}, 0.08); border-radius:{Configuration.Border1}; margin: 0 0 {Configuration.Spacing2} 0;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='height:{Configuration.Spacing4};'></div>", unsafe_allow_html=True)
    RenderForecastLineChart(forecasts, selectedParameter, selectedFilters, forecastAccuracyByProvider, animate=animate)

    st.markdown(f"<div style='height:{Configuration.Spacing4};'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='height:1px; background: rgba({HexToRgb(Configuration.Palette1VeryDark)}, 0.08); border-radius:{Configuration.Border1}; margin: 0 0 {Configuration.Spacing2} 0;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='height:{Configuration.Spacing4};'></div>", unsafe_allow_html=True)

def RenderColumnLeft(animate, summaryTable):
        titleClass = 'forecast-enter-delay-1' if animate else ''
        st.markdown(f"<div class='chart-title forecast-enter-item {titleClass}'>Posso uscire?</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chart-subtitle forecast-enter-item {titleClass}'>Quale è la situazione per giorno e parte della giornata?</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='height: 55px;'></div>", unsafe_allow_html=True)
        RenderForecastTable(summaryTable)

@st.fragment
def RenderColumnRight(animate, city, selectedFilters, staticEventsTable, summaryTable):
    titleClass2        = 'forecast-enter-delay-2' if animate else ''
    cityName           = city[city['Id'] == selectedFilters['cityId']]['City'].iloc[0] if selectedFilters['cityId'] else "la città"
    st.markdown(f"<div class='llm-title forecast-enter-item {titleClass2}'>Consigli del Concierge</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='llm-subtitle forecast-enter-item {titleClass2}'>Idee per attività da fare nei prossimi giorni in base allo scenario meteorologico</div>", unsafe_allow_html=True)

    if st.button('✨ Genera Suggerimenti', use_container_width=True):
        st.session_state['llm_comment_cache'] = ''
        st.session_state['_streaming_active'] = True

    conciergeSlot = st.empty()

    if st.session_state.get('_streaming_active'):
        st.session_state['_streaming_active'] = False
        fullText = ''
        with st.spinner("Il Concierge sta analizzando le possibilità per te..."):
            for chunk in GenerateLLMComment(cityName, staticEventsTable, summaryTable=summaryTable):
                fullText += chunk
                conciergeSlot.markdown(RenderConciergeMarkdownContainer(fullText), unsafe_allow_html=True)
        st.session_state['llm_comment_cache'] = fullText

    elif st.session_state.get('llm_comment_cache'): conciergeSlot.markdown(RenderConciergeMarkdownContainer(st.session_state['llm_comment_cache']), unsafe_allow_html=True)

    else: conciergeSlot.markdown(f'<div class="concierge-container" style="display:flex;align-items:center;justify-content:center;color:rgba(0,0,0,0.3);font-size:{Configuration.FontSize3};"><i>Clicca sul bottone per ricevere consigli personalizzati per {cityName}</i></div>', unsafe_allow_html=True)

    st.markdown("<div class='llm-disclaimer'><strong>Nota</strong>: il Concierge usa un modello LLM e potrebbe fornire indicazioni non corrette. Verifica sempre le informazioni prima di decidere.</div>", unsafe_allow_html=True)

def RenderForecastContent(city, calendar, forecasts, forecastAccuracyByProvider, staticEventsTable):
    animate = not st.session_state.get('_forecast_entered', False)
    st.session_state['_forecast_entered'] = True
    
    st.markdown(PageStylesCss(animate=animate), unsafe_allow_html=True)
    ConciergeCSS()

    selectedFilters = RenderValueFilters(city, calendar, forecasts, animate=animate)
    st.session_state['selectedFilters'] = selectedFilters
    
    st.markdown(f"<div style='height: {Configuration.Spacing2};'></div>", unsafe_allow_html=True)
    selectedParameter = RenderParameterFilter()

    st.session_state['selectedParameter'] = selectedParameter
    st.markdown(f"<div style='height: {Configuration.Spacing4};'></div>", unsafe_allow_html=True)

    if selectedFilters['cityId'] is None: RenderNoCityAlert()

    forecasts    = BuildDf(city, calendar, forecasts)
    forecasts    = FilterDf(forecasts, selectedFilters)
    scoresTable  = CalculateScore(GroupDf(forecasts))

    RenderFirstPart(forecasts, selectedParameter, selectedFilters, forecastAccuracyByProvider, animate)
    
    columnLeft, columnRight = st.columns([1.25, 1])
    with columnLeft: RenderColumnLeft(animate, scoresTable)
    with columnRight: RenderColumnRight(animate, city, selectedFilters, staticEventsTable, CreateSummary(scoresTable))