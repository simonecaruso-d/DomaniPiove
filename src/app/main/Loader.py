# Environment Setting
import base64
import random
import streamlit as st

import configuration.ConfigurationStreamlit as Configuration

# Helpers
def GetBase64Logo(logoPath = Configuration.LogoPath):
    'Load the logo image and return it as a base64-encoded string for embedding in HTML.'
    with open(logoPath, "rb") as logoFile: return base64.b64encode(logoFile.read()).decode()

# CSS
def HideRunningIndicatorCss():
    'Return CSS to hide Streamlit\'s default running indicator and style the custom loader.'
    loaderMessageMaxWidth = Configuration.ScalePx(760)
    loaderBarWidth        = Configuration.ScalePx(320)
    loaderBarHeight       = Configuration.ScalePx(8)

    return f"""<style>
        [data-testid="stStatusWidget"] {{ display: none !important; }}
        .loader-container {{display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70vh; gap: {Configuration.Spacing4}; padding: {Configuration.Spacing3}; background: linear-gradient(135deg, {Configuration.PrimaryColor} 0%, {Configuration.Palette1Medium} 50%, {Configuration.Palette2Medium} 100%); border-radius: {Configuration.RadiusCard}px; box-shadow: 0 {Configuration.Spacing3} {Configuration.Spacing5} {Configuration.BoxShadowMarker};}}
        .loader-title {{
            font-size: {Configuration.FontSize11} !important; font-weight: {Configuration.FontWeight4} !important;
            font-family: {Configuration.FontFamily} !important; color: {Configuration.WhiteColor} !important; text-shadow: 0 2px 12px rgba(0,0,0,0.4);
            letter-spacing: {Configuration.LetterSpacing2} !important; line-height: {Configuration.LineHeight3} !important;
            animation: glow 2.5s ease-in-out infinite alternate;}}
        .loader-subtitle {{
            font-size: {Configuration.FontSize5} !important; font-weight: {Configuration.FontWeight3} !important;
            font-family: {Configuration.FontFamily} !important; color: {Configuration.WhiteColor} !important; opacity: 0.92;
            letter-spacing: {Configuration.LetterSpacing1} !important; text-transform: uppercase;}}
        .loader-countdown {{
            display: flex; align-items: baseline; justify-content: center; gap: {Configuration.Spacing2};
            color: {Configuration.WhiteColor} !important; margin-top: -{Configuration.Spacing2};}}
        .loader-countdown-value {{
            position: relative; display: grid; min-width: {Configuration.ScalePx(84)}px; height: {Configuration.ScalePx(44)}px;
            font-size: {Configuration.FontSize9} !important; font-weight: {Configuration.FontWeight4} !important;
            line-height: 1; text-align: center;}}
        .loader-countdown-item {{ grid-area: 1 / 1; opacity: 0; }}
        .loader-countdown-label {{
            font-size: {Configuration.FontSize4} !important; font-weight: {Configuration.FontWeight2} !important;
            opacity: 0.92; }}
        @keyframes glow {{ 0% {{ text-shadow: 0 0 12px rgba(255,255,255,{Configuration.Opacity2}); }} 100% {{ text-shadow: 0 4px 24px rgba(255,255,255,1); }} }}
        .loader-message {{
            font-size: {Configuration.FontSize7} !important; font-weight: {Configuration.FontWeight2} !important; line-height: {Configuration.LineHeight4} !important;
            font-family: {Configuration.FontFamily} !important; color: {Configuration.WhiteColor} !important; text-align: center; max-width: {loaderMessageMaxWidth}px;
            animation: fadeInUp 1s ease-out; padding: {Configuration.Spacing2}; background: {Configuration.BackgroundText}; backdrop-filter: blur(16px); border-radius: {Configuration.RadiusInput}px; border: 1px solid {Configuration.BackgroundAlpha};}}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(24px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .loader-bar-track {{width: {loaderBarWidth}px; height: {loaderBarHeight}px; background: {Configuration.BackgroundAlpha}; border-radius: {Configuration.RadiusInput}px; overflow: hidden; margin-top: {Configuration.Spacing3}; box-shadow: inset 0 2px 8px rgba(0,0,0,0.1); position: relative;}}
        .loader-bar-fill {{position: absolute; top: 0; left: -35%; width: 35%; height: 100%; border-radius: {Configuration.RadiusInput}px; background: linear-gradient(90deg, {Configuration.TertiaryColor} 0%, {Configuration.PrimaryColor} 50%, {Configuration.Palette1Light} 100%); box-shadow: 0 0 24px {Configuration.PrimaryColor}; animation: loaderSweep 1.6s ease-in-out infinite;}}
        .weather-emoji {{ font-size: 4em; animation: weatherFloat 3s ease-in-out infinite; margin-bottom: {Configuration.Spacing2}; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3)); }}
        @keyframes weatherFloat {{ 0%, 100% {{ transform: translateY(0) rotate(0deg); }} 50% {{ transform: translateY(-12px) rotate(5deg); }} }}
        @keyframes loaderSweep {{ 0% {{ left: -35%; }} 100% {{ left: 100%; }} }}
    </style>"""

def LoaderRotationCss(totalDuration, visibleUntil, fadeUntil):
    'Return CSS to rotate loader messages without rerunning Streamlit.'
    return f"""<style>
        .loader-message-rotating {{position: relative; display: grid; width: 100%; min-height: {Configuration.ScalePx(120)}px; overflow: hidden; animation: none;}}
        .loader-message-item {{grid-area: 1 / 1; opacity: 0; animation: loaderMessageRotate {totalDuration}s infinite;}}
        @keyframes loaderMessageRotate {{
            0%, {visibleUntil}% {{ opacity: 1; transform: translateY(0); }}
            {fadeUntil}%, 100% {{ opacity: 0; transform: translateY(10px); }}}}
    </style>"""

def LoaderCountdownCss():
    'Return CSS to animate a countdown from 60 to zero without rerunning Streamlit.'
    return f"""<style>
        .loader-countdown-item {{animation: loaderCountdownStep 1.12s ease-in-out both;}}
        @keyframes loaderCountdownStep {{
            0% {{ opacity: 0; transform: translateY(10px) scale(0.985); filter: blur(1.5px); }}
            18% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }}
            78% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }}
            100% {{ opacity: 0; transform: translateY(-10px) scale(1.015); filter: blur(1.5px); }}
        }}
        .loader-countdown-item-last {{animation: loaderCountdownLast 0.9s ease-out both;}}
        @keyframes loaderCountdownLast {{
            0% {{ opacity: 0; transform: translateY(10px) scale(0.985); filter: blur(1.5px); }}
            100% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }}
        }}
    </style>"""

# Loader
def RenderLoader(message = None):
    'Render a custom loading screen once and return its placeholder so the caller can clear it after loading.'
    st.markdown(HideRunningIndicatorCss(), unsafe_allow_html=True)

    logoBase64        = GetBase64Logo()
    slot              = st.empty()
    messages          = [message] if message else random.sample(Configuration.LoadingMessages, k=len(Configuration.LoadingMessages))
    messageCount      = len(messages)
    totalDuration     = messageCount * 5
    visibleUntil      = round(80 / messageCount, 4)
    fadeUntil         = round(100 / messageCount, 4)
    countdownDuration = random.randint(50, 70)
    st.markdown(LoaderCountdownCss(), unsafe_allow_html=True)

    countdownItems = ''.join(
        f"<div class='loader-countdown-item' style='animation-delay: {index}s;'>{(countdownDuration - index) // 60:02d}:{(countdownDuration - index) % 60:02d}</div>" 
        for index in range(countdownDuration)) + f"<div class='loader-countdown-item loader-countdown-item-last' style='animation-delay: {countdownDuration}s;'>00:00</div>"
    if messageCount == 1: messageHtml = f"<div class='loader-message'>{messages[0]}</div>"
    else:
        st.markdown(LoaderRotationCss(totalDuration, visibleUntil, fadeUntil), unsafe_allow_html=True)
        messageItems = ''.join(f"<div class='loader-message-item' style='animation-delay: -{index * 5}s;'>{currentMessage}</div>" for index, currentMessage in enumerate(messages))
        messageHtml = f"<div class='loader-message loader-message-rotating'>{messageItems}</div>"

    slot.markdown(f"""
            <div class='loader-container'><div class='weather-emoji'><img src="data:image/png;base64,{logoBase64}" width="{Configuration.ScalePx(80)}"></div>
            <div class='loader-title'>Domani Piove</div>
            <div class='loader-subtitle'>Attesa stimata</div>
            <div class='loader-countdown'><div class='loader-countdown-value'>{countdownItems}</div><div class='loader-countdown-label'>min:sec</div></div>
            {messageHtml}
            <div class='loader-bar-track'><div class='loader-bar-fill'></div></div></div>""", unsafe_allow_html=True)

    return slot