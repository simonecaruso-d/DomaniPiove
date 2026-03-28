# Environment Setting
import base64
import random
import streamlit as st
import threading
import time

import configuration.ConfigurationStreamlit as Configuration

# Helpers
def GetBase64Logo(logoPath = Configuration.LogoPath):
    with open(logoPath, "rb") as logoFile: return base64.b64encode(logoFile.read()).decode()

# CSS
def HideRunningIndicatorCss():
    loaderMessageMaxWidth = Configuration.ScalePx(420)
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
        @keyframes glow {{ 0% {{ text-shadow: 0 0 12px rgba(255,255,255,{Configuration.Opacity2}); }} 100% {{ text-shadow: 0 4px 24px rgba(255,255,255,1); }} }}
        .loader-message {{
            font-size: {Configuration.FontSize7} !important; font-weight: {Configuration.FontWeight2} !important; line-height: {Configuration.LineHeight4} !important;
            font-family: {Configuration.FontFamily} !important; color: {Configuration.WhiteColor} !important; text-align: center; max-width: {loaderMessageMaxWidth}px;
            animation: fadeInUp 1s ease-out; padding: {Configuration.Spacing2}; background: {Configuration.BackgroundText}; backdrop-filter: blur(16px); border-radius: {Configuration.RadiusInput}px; border: 1px solid {Configuration.BackgroundAlpha};}}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(24px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .loader-bar-track {{width: {loaderBarWidth}px; height: {loaderBarHeight}px; background: {Configuration.BackgroundAlpha}; border-radius: {Configuration.RadiusInput}px; overflow: hidden; margin-top: {Configuration.Spacing3}; box-shadow: inset 0 2px 8px rgba(0,0,0,0.1);}}
        .loader-bar-fill {{height: 100%; border-radius: {Configuration.RadiusInput}px; background: linear-gradient(90deg, {Configuration.TertiaryColor} 0%, {Configuration.PrimaryColor} 50%, {Configuration.Palette1Light} 100%); box-shadow: 0 0 24px {Configuration.PrimaryColor}; transition: width 0.8s {Configuration.AnimationEasing};}}
        .weather-emoji {{ font-size: 4em; animation: weatherFloat 3s ease-in-out infinite; margin-bottom: {Configuration.Spacing2}; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3)); }}
        @keyframes weatherFloat {{ 0%, 100% {{ transform: translateY(0) rotate(0deg); }} 50% {{ transform: translateY(-12px) rotate(5deg); }} }}
    </style>"""

# Loader
def RenderLoader(doneEvent: threading.Event, stepSeconds = 5):
    st.markdown(HideRunningIndicatorCss(), unsafe_allow_html=True)
    random.shuffle(Configuration.LoadingMessages)
    
    logoBase64 = GetBase64Logo()
    slot       = st.empty()
    startTime  = time.time()

    while not doneEvent.is_set():
        elapsed     = time.time() - startTime
        progress    = int(100 * elapsed / (elapsed + 10))
        currentStep = int(elapsed // stepSeconds)
        message     = Configuration.LoadingMessages[currentStep % len(Configuration.LoadingMessages)]
               
        slot.markdown(f"""
            <div class='loader-container'>
                <div class='weather-emoji'>
                    <img src="data:image/png;base64,{logoBase64}" width="{Configuration.ScalePx(80)}">
                </div>
                <div class='loader-title'>Domani Piove</div>
                <div class='loader-message'>{message}</div>
                <div class='loader-bar-track'>
                    <div class='loader-bar-fill' style='width:{progress}%;'></div>
                </div>
            </div>""", unsafe_allow_html=True)

        doneEvent.wait(timeout=1.0)

    slot.empty()