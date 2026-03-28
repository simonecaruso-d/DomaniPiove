# Environment Setting
import html
import math
import pandas as pd
import streamlit as st
 
import configuration.ConfigurationStreamlit as Configuration
 
# HTML Templates 
def BestProviderLineHtml(label, providerName, maeFormatted, animationClass=''):
    textGap = Configuration.Spacing0B if Configuration.ResponsiveViewportWidth <= 1366 else Configuration.Spacing1
    return (f'<div class="accuracy-enter-item {animationClass}" style="margin-bottom:{textGap};font-size:{Configuration.FontSize3};color:{Configuration.Palette2Dark};line-height:{Configuration.LineHeight3};">'
            f'A {html.escape(label.lower())} di distanza, '
            f'<span style="font-weight:{Configuration.FontWeight2};">{html.escape(providerName)}</span> '
            f'è il più affidabile con un errore medio di '
            f'<b>{html.escape(maeFormatted)}</b>.'
            f'</div>')

def WorstProviderLineHtml(label, providerName, maeFormatted, animationClass=''):
    textGap = Configuration.Spacing0B if Configuration.ResponsiveViewportWidth <= 1366 else Configuration.Spacing1
    return (f'<div class="accuracy-enter-item {animationClass}" style="margin-bottom:{textGap};font-size:{Configuration.FontSize3};color:{Configuration.Palette2Dark};line-height:{Configuration.LineHeight3};">'
            f'A {html.escape(label.lower())} di distanza, '
            f'<span style="font-weight:{Configuration.FontWeight2};">{html.escape(providerName)}</span> '
            f'è il meno affidabile con un errore medio di '
            f'<b>{html.escape(maeFormatted)}</b>.'
            f'</div>')

def SectionHeaderHtml(text, animationClass=''):
    sectionBottomGap = Configuration.Spacing1 if Configuration.ResponsiveViewportWidth <= 1366 else Configuration.Spacing2
    return (f'<div class="accuracy-enter-item {animationClass}" style="font-size:{Configuration.FontSize6};font-weight:{Configuration.FontWeight2};color:{Configuration.Palette2Dark};'
            f'letter-spacing:{Configuration.LetterSpacing2}; line-height:{Configuration.LineHeight5}; margin-top: 0; margin-bottom:{sectionBottomGap};">{text}</div>')

# CSS Templates
def PageStylesCss(animate=True):
    if animate:
        enterItemCss = f'opacity: 0; transform: translateY(28px); animation: accuracyEnterUp {Configuration.AnimationDuration} {Configuration.AnimationEasing} forwards; will-change: opacity, transform;'
        delay1Css    = f'animation-delay: {Configuration.AnimationDelay1};'
        delay2Css    = f'animation-delay: {Configuration.AnimationDelay2};'
    else:
        enterItemCss = 'opacity: 1; transform: none;'
        delay1Css    = delay2Css = ''

    return f"""<style>
        .accuracy-enter-item    {{ {enterItemCss} }}
        .accuracy-enter-delay-1 {{ {delay1Css} }}
        .accuracy-enter-delay-2 {{ {delay2Css} }}
        @keyframes accuracyEnterUp {{ from {{ opacity: 0; transform: translateY(28px); }}
                                      to   {{ opacity: 1; transform: translateY(0); }} }}
        .accuracy-filter-title {{color: {Configuration.Palette2Light} !important; font-size: {Configuration.FontSize5} !important; font-family: {Configuration.FontFamily} !important; font-weight: {Configuration.FontWeight4} !important; letter-spacing: {Configuration.LetterSpacing2} !important; margin-bottom: {Configuration.Spacing2} !important; line-height: {Configuration.LineHeight5} !important; opacity: {Configuration.Opacity2} !important;}}
        div[data-testid="stRadio"] > label {{ display: none !important; }}
        div[data-testid="stRadio"] div[role="radiogroup"] {{display: flex !important; flex-wrap: wrap !important; gap: {Configuration.Spacing1B} !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] {{
            margin: 0 !important; padding: {Configuration.SpacingA} !important; border-radius: {Configuration.RadiusButton}px !important;
            border: {Configuration.WidthBorder}px solid transparent !important; background: {Configuration.Palette2Dark} !important;
            color: {Configuration.WhiteColor} !important; font-size: {Configuration.FontSize3} !important;
            font-family: {Configuration.FontFamily} !important; min-width: 90px !important;
            font-weight: {Configuration.FontWeight3} !important; transition: background-color 160ms ease, transform 160ms ease, box-shadow 160ms ease !important;
            cursor: pointer !important; display: flex !important; align-items: center !important;
            justify-content: center !important; text-align: center !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"]:hover {{background: {Configuration.Palette2Medium} !important; transform: translateY(-1px) !important; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12) !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {{ display: none !important; }}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] > div:last-child {{margin: 0 !important; padding: 0 !important; width: 100% !important; display: flex !important; justify-content: center !important; align-items: center !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] input {{ display: none !important; }}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] div {{color: inherit !important; font-size: {Configuration.FontSize3} !important; font-family: {Configuration.FontFamily} !important; text-align: center !important; width: 100% !important; margin: 0 !important; justify-content: center !important;}}
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"],
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {{background: {Configuration.Palette2Light} !important; color: {Configuration.WhiteColor} !important; box-shadow: 0 6px 14px rgba(47, 72, 88, 0.28) !important;}}
        .radar-dot-g .radar-tooltip {{ transition: opacity 180ms ease; }}
        .radar-dot-g:hover .radar-tooltip {{ opacity: 1 !important; }}
        .radar-dot-g:hover .radar-dot {{ r: 8; transition: r 150ms ease; }}
        .radar-dot {{ transition: r 150ms ease; }}
    </style>"""

def TitleCss():
    return f"""<style>
        .accuratezza-title-fixed {{
            position: fixed; top: {Configuration.TitleTopPx}; left: {Configuration.TitleLeftCollapsedPx};
            margin: 0 !important; padding: 0 !important;
            color: {Configuration.PrimaryColor} !important; font-size: {Configuration.FontSize8} !important;
            line-height: {Configuration.LineHeight2} !important; font-weight: {Configuration.FontWeight4} !important;
            letter-spacing: {Configuration.LetterSpacing2} !important; font-family: {Configuration.FontFamily} !important;
            text-shadow: none !important; z-index: 999997;}}
        body:has([data-testid="stSidebar"][aria-expanded="true"])  .accuratezza-title-fixed {{ left: {Configuration.TitleLeftExpandedPx}; }}
        body:has([data-testid="stSidebar"][aria-expanded="false"]) .accuratezza-title-fixed {{ left: {Configuration.TitleLeftCollapsedPx}; }}
    </style><div class="accuratezza-title-fixed">Accuratezza</div>"""
 
# Rendering Functions
def RenderTitle():
    st.markdown(TitleCss(), unsafe_allow_html=True)

def RenderParameterFilter(parameters=Configuration.Parameters):
    st.markdown(f'<div class="accuracy-filter-title">Seleziona un fenomeno meteorologico:</div>', unsafe_allow_html=True)
    selectedParameter = st.radio('Parametro', options=parameters, horizontal=True, index=0, key='accuracy_parameter_filter', label_visibility='collapsed')
    return selectedParameter
 
def RenderRadar(aggregatedDf, providers, daySpans, labels, parameter, animate=True):
    animationClass           = 'accuracy-enter-delay-1' if animate else ''
    N                        = len(daySpans)
    centerX, centerY, radius = Configuration.ScalePx(280), Configuration.ScalePx(260), Configuration.ScalePx(190)
    width, height            = Configuration.ScalePx(560), Configuration.ScalePx(500)
    angles                   = [2 * math.pi * i / N - math.pi / 2 for i in range(N)]

    defs = (f'<defs>'
            f'<radialGradient id="rbg" cx="50%" cy="50%" r="50%">'
            f'<stop offset="0%" stop-color="{Configuration.Palette2Light}" stop-opacity="0.04"/>'
            f'<stop offset="100%" stop-color="{Configuration.Palette2Dark}" stop-opacity="0.01"/>'
            f'</radialGradient>'
            f'<filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/>'
            f'<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'</defs>')

    background = f'<circle cx="{centerX}" cy="{centerY}" r="{radius + 20}" fill="url(#rbg)" />'

    scale      = Configuration.ParametersScale.get(parameter, 1)
    unit       = Configuration.ParametersMeasureUnits.get(parameter, '')
    allMae     = [abs(float(Lookup(aggregatedDf, ds, prov))) * scale for ds in daySpans for prov in providers if not pd.isna(Lookup(aggregatedDf, ds, prov))]
    dataMax    = max(allMae) if allMae else 1.0
    maxDisplay = dataMax * 1.15

    rings = ''
    for frac in [0.25, 0.5, 0.75, 1.0]:
        r         = radius * frac
        value     = maxDisplay * frac
        ringLabel = f'{value:.0f}{unit}' if scale != 1 else f'{value:.1f}{unit}'
        rings    += f'<circle cx="{centerX}" cy="{centerY}" r="{r}" fill="none" stroke="rgba(47,72,88,0.06)" stroke-width="1" stroke-dasharray="4,4"/>'
        rings    += (f'<text x="{centerX + 5}" y="{centerY - r + 12}" fill="rgba(47,72,88,0.28)" '
                     f'font-size="{Configuration.FontSizeAA}" font-family="{Configuration.FontFamily}" font-weight="{Configuration.FontWeight3}">{html.escape(ringLabel)}</text>')

    axes = ''
    for i, (a, lbl) in enumerate(zip(angles, labels)):
        ex, ey  = centerX + radius * math.cos(a), centerY + radius * math.sin(a)
        axes   += f'<line x1="{centerX}" y1="{centerY}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="rgba(47,72,88,0.08)" stroke-width="1"/>'
        textX   = centerX + (radius + 30) * math.cos(a)
        textY   = centerY + (radius + 30) * math.sin(a)
        anchor  = 'start' if math.cos(a) > 0.3 else ('end' if math.cos(a) < -0.3 else 'middle')
        axes   += (f'<text x="{textX:.1f}" y="{textY:.1f}" text-anchor="{anchor}" dominant-baseline="0.35em" '
                   f'fill="{Configuration.Palette2Dark}" font-size="{Configuration.FontSizeA}" font-weight="{Configuration.FontWeight3}" font-family="{Configuration.FontFamily}" '
                   f'letter-spacing="{Configuration.LetterSpacing1}">{html.escape(lbl)}</text>')

    polygons = ''
    dots     = ''
    for pi, prov in enumerate(providers):
        color   = Configuration.Palette2ByProvider[pi % len(Configuration.Palette2ByProvider)]
        points  = []
        dotList = []
        for i, ds in enumerate(daySpans):
            mae    = Lookup(aggregatedDf, ds, prov)
            r      = radius * MAEIntensity(mae, parameter, maxDisplay)
            px     = centerX + r * math.cos(angles[i])
            py     = centerY + r * math.sin(angles[i])
            points.append(f'{px:.1f},{py:.1f}')
            dotList.append((px, py, mae, prov))
        polygons += (f'<polygon points="{" ".join(points)}" fill="none" '
                     f'stroke="{color}" stroke-width="2.5" stroke-linejoin="round" '
                     f'opacity="{Configuration.Opacity2}" filter="url(#glow)">'
                     f'<animate attributeName="opacity" from="0" to="{Configuration.Opacity2}" dur="0.6s" fill="freeze"/>'
                     f'</polygon>')
        for (px, py, mae, provName) in dotList:
            tipText = f'{html.escape(provName)}: {html.escape(FormatMaeValue(mae, parameter))}'
            tipW    = max(len(tipText) * 6.5, 64)
            dots   += (f'<g class="radar-dot-g">'
                       f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{color}" stroke="#fff" stroke-width="2.5" '
                       f'filter="url(#glow)" class="radar-dot"/>'
                       f'<circle cx="{px:.1f}" cy="{py:.1f}" r="16" fill="transparent" class="radar-dot-hover"/>'
                       f'<g class="radar-tooltip" opacity="0" pointer-events="none">'
                       f'<rect x="{px - tipW/2:.1f}" y="{py - 34:.1f}" width="{tipW:.0f}" height="22" rx="8" '
                       f'fill="{color}" opacity="0.92"/>'
                       f'<text x="{px:.1f}" y="{py - 20:.1f}" text-anchor="middle" fill="#fff" '
                       f'font-size="{Configuration.FontSizeA}" font-weight="{Configuration.FontWeight4}" font-family="{Configuration.FontFamily}">{tipText}</text>'
                       f'</g></g>')

    providerLegend = ' &nbsp;·&nbsp; '.join(f'<span style="color:{Configuration.Palette2ByProvider[pi % len(Configuration.Palette2ByProvider)]};">■</span> {html.escape(prov)}' for pi, prov in enumerate(providers))
    title = (f'<div class="accuracy-enter-item {animationClass}" style="text-align:center;margin-bottom:{Configuration.Spacing0B};">'
             f'<div style="font-size:{Configuration.FontSize6};font-weight:{Configuration.FontWeight2};line-height:{Configuration.LineHeight5};color:{Configuration.Palette2Dark};letter-spacing:{Configuration.LetterSpacing2};">'
             f'Errore assoluto medio per provider</div>'
             f'<div style="font-size:{Configuration.FontSize1};font-weight:{Configuration.FontWeight1};color:{Configuration.Palette2VeryLight};margin-top:{Configuration.Spacing0B};line-height:{Configuration.LineHeight1};">'
             f'{providerLegend}</div></div>')

    svg = (f'<svg class="accuracy-enter-item {animationClass}" viewBox="0 0 {width} {height}" width="100%" '
           f'style="max-width:620px;margin:0 auto;display:block;">'
           f'{defs}{background}{rings}{axes}{polygons}{dots}</svg>')

    st.markdown(title + svg, unsafe_allow_html=True)

def RenderBestProviderSummary(aggregatedDf, daySpans, labels, parameter, animate=True):
    animationClass = 'accuracy-enter-delay-2' if animate else ''
    bestLines  = []
    worstLines = []
    
    isTightLaptopViewport = Configuration.ResponsiveViewportWidth <= 1366
    gapBetweenSections    = Configuration.Spacing3 if isTightLaptopViewport else Configuration.Spacing6
    sectionBuffer         = Configuration.Spacing1 if isTightLaptopViewport else Configuration.Spacing3

    for ds, lbl in zip(daySpans, labels):
        subset = aggregatedDf[aggregatedDf['DaySpanNumeric'] == ds].dropna(subset=['MAE'])
        best   = subset.loc[subset['MAE'].idxmin()]
        worst  = subset.loc[subset['MAE'].idxmax()]
        bestLines.append(BestProviderLineHtml(lbl, best['Provider'], FormatMaeValue(best['MAE'], parameter), animationClass))
        worstLines.append(WorstProviderLineHtml(lbl, worst['Provider'], FormatMaeValue(worst['MAE'], parameter), animationClass))

    if bestLines:
        st.markdown(SectionHeaderHtml('Provider più affidabile', animationClass) + ''.join(bestLines), unsafe_allow_html=True)
    if worstLines:
        st.markdown(f"<div style='height:{gapBetweenSections};'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='height:{gapBetweenSections};'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='height:{sectionBuffer};'></div>", unsafe_allow_html=True)
        st.markdown(SectionHeaderHtml('Provider meno affidabile', animationClass) + ''.join(worstLines), unsafe_allow_html=True)

# Data Helpers
def FormatMaeValue(maeValue, selectedParameter):
    scale = Configuration.ParametersScale.get(selectedParameter, 1)
    unit  = Configuration.ParametersMeasureUnits.get(selectedParameter, '')
    return f'{maeValue * scale:.2f}{unit}'
 
def BuildRawAccuracyData(forecastAccuracyByDaySpan, selectedParameter):
    selectedMetric       = Configuration.ParametersEng.get(selectedParameter)
    df                   = forecastAccuracyByDaySpan.copy()
    df['Metric']         = df['Metric'].astype(str)
    df                   = df[df['Metric'].str.casefold() == str(selectedMetric).casefold()]
    df['Provider']       = df['Provider'].astype(str)
    df['DaySpanNumeric'] = pd.to_numeric(df['DaySpan'], errors='coerce')
    df['MAE']            = pd.to_numeric(df['MAE'], errors='coerce')
 
    aggregatedDf = (df.dropna(subset=['DaySpanNumeric']).groupby(['DaySpanNumeric', 'Provider'], as_index=False).agg(MAE=('MAE', 'mean')).sort_values(['DaySpanNumeric', 'Provider']))
 
    providers = sorted(aggregatedDf['Provider'].unique())
    daySpans  = sorted(aggregatedDf['DaySpanNumeric'].unique())
    labels    = [f'{int(d)} Giorno' if d == 1 else f'{int(d)} Giorni' if float(d).is_integer() else f'{d:.2f} Giorni' for d in daySpans]
    return aggregatedDf, providers, daySpans, labels
 
def Lookup(aggregatedDf, daySpan, provider):
    result = aggregatedDf[(aggregatedDf['DaySpanNumeric'] == daySpan) & (aggregatedDf['Provider'] == provider)]
    return result.iloc[0]['MAE'] if len(result) > 0 else float('nan')
 
def MAEIntensity(mae, parameter, maxVal=None):
    if pd.isna(mae): return 0.3
    scale   = Configuration.ParametersScale.get(parameter, 1)
    disp    = abs(float(mae)) * scale
    if maxVal is not None and maxVal > 0: ceiling = maxVal
    else:
        _, mu   = Configuration.MaeThresholdsByParameter.get(parameter, (2, 5))
        ceiling = mu * 1.5
    return min(max(disp / ceiling, 0.08), 1.0)

def HexToRgb(hex):
    hex     = hex.lstrip('#')
    r, g, b = int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)
    return f'{r},{g},{b}'

# Wrapper
def RenderAccuracyContent(forecastAccuracyByDaySpan):
    animate = not st.session_state.get('_accuracy_entered', False)
    st.session_state['_accuracy_entered'] = True
    st.markdown(PageStylesCss(animate=animate), unsafe_allow_html=True)

    selectedParameter                     = RenderParameterFilter()
    st.session_state['selectedParameter'] = selectedParameter
    st.markdown(f"<div style='height:{Configuration.Spacing6};'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='height:1px; background: rgba({HexToRgb(Configuration.Palette2Dark)}, 0.08); border-radius:{Configuration.Border1}; margin: 0 0 {Configuration.Spacing2} 0;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='height:{Configuration.Spacing5};'></div>", unsafe_allow_html=True)

    aggregatedDf, providers, daySpans, labels = BuildRawAccuracyData(forecastAccuracyByDaySpan, selectedParameter)

    leftColumn, rightColumn = st.columns([1, 1], gap='large')
    with leftColumn : RenderRadar(aggregatedDf, providers, daySpans, labels, selectedParameter, animate=animate)
    with rightColumn: RenderBestProviderSummary(aggregatedDf, daySpans, labels, selectedParameter, animate=animate)