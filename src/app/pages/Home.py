# Environment Setting
import base64
import folium
from pathlib import Path
import streamlit as st

import configuration.ConfigurationStreamlit as Configuration

# HTML Templates
def SectionTitleHtml(title, animationClass):
    'Returns HTML for a section title with the specified text and animation class.'
    return f'<div class="home-section-title-wrap home-enter-item {animationClass}"><h3 class="home-section-title">{title}</h3></div>'

def TextBlockHtml(content, animationClass):
    'Returns HTML for a text block with the specified content and animation class.'
    return f'<div class="home-text-block home-enter-item {animationClass}"><p class="home-text-paragraph">{content}</p></div>'

def SlideImageHtml(imageB64, animationClass):
    'Returns HTML for a slideshow image with the specified base64-encoded image data and animation class.'
    return f'<div class="home-enter-item {animationClass} home-slide-image-shell"><img class="home-slide-image" src="data:image/png;base64,{imageB64}" /></div>'

def SlideCaptionHtml(displayName, captionText, animationClass):
    'Returns HTML for a slideshow caption with the specified display name, caption text, and animation class.'
    return f"""<div class="home-enter-item {animationClass} home-slide-caption"><div class="home-slide-caption-title">{displayName}</div><div class="home-slide-caption-text">{captionText}</div></div>"""

def SlideCounterHtml(current, total, animationClass):
    'Returns HTML for a slideshow counter with the specified current and total values and animation class.'
    return f"<div class='home-enter-item {animationClass} home-slide-counter'>{current} / {total}</div>"

def MapMarkerHtml(cityName):
    'Returns HTML for a map marker popup with the specified city name.'
    return f"""<div style="font-family: {Configuration.FontFamily}; background: {Configuration.AccentColor}; 
                color: {Configuration.WhiteColor}; padding: {Configuration.Border1}; 
                border-radius: {Configuration.Border1}; font-size: {Configuration.FontSizeA};
                font-weight: {Configuration.FontWeight2}; letter-spacing: {Configuration.LetterSpacing2}; 
                white-space: 'nowrap'; box-shadow: {Configuration.BoxShadowMarker}; 
                text-align: 'center';">{cityName}</div>"""

# CSS Templates
def PageStylesCss(animate):
    'Returns CSS styles for the home page, with optional animation for entering elements.'
    if animate:
        enterItemCss  = f'opacity: 0; transform: translateY(28px); animation: homeEnterUp {Configuration.AnimationDuration} {Configuration.AnimationEasing} forwards; will-change: opacity, transform;'
        delay1Css     = f'animation-delay: {Configuration.AnimationDelay1};'
        delay2Css     = f'animation-delay: {Configuration.AnimationDelay2};'
        buttonAnimCss = f'opacity: 0; transform: translateY(28px); animation: homeEnterUp {Configuration.AnimationDuration} {Configuration.AnimationEasing} {Configuration.AnimationDelay1} forwards;'
    else:
        enterItemCss  = 'opacity: 1; transform: none;'
        delay1Css     = delay2Css = buttonAnimCss = ''

    return f"""<style>
        .home-enter-item      {{ {enterItemCss} }}
        .home-enter-delay-1   {{ {delay1Css} }}
        .home-enter-delay-2   {{ {delay1Css} }}
        .home-enter-delay-3   {{ {delay2Css} }}
        @keyframes homeEnterUp {{ from {{ opacity: 0; transform: translateY(28px); }}
                                  to   {{ opacity: 1; transform: translateY(0); }} }}
        .home-section-title-wrap  {{ display: flex; align-items: flex-start; margin-bottom: {Configuration.Spacing1}; }}
        .home-section-title       {{ margin: 0; color: {Configuration.AccentColor} !important; font-size: {Configuration.FontSize7} !important; line-height: {Configuration.LineHeight2}; font-weight: {Configuration.FontWeight4}; font-family: {Configuration.FontFamily}; text-shadow: none !important; }}
        .home-text-block          {{ height: {Configuration.HeightWhoWeAre}px; color: {Configuration.AccentColor}; font-family: {Configuration.FontFamily}; background: {Configuration.BackgroundText}; border-radius: {Configuration.Border2}; padding: {Configuration.Spacing1B}; box-sizing: border-box; }}
        .home-text-paragraph      {{ margin: 0; font-size: {Configuration.FontSize4} !important; line-height: {Configuration.LineHeight5}; color: {Configuration.AccentColor}; }}
        .home-slide-image-shell   {{ height: {Configuration.HeightSlideshow}px; border-radius: {Configuration.Border3}; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
        .home-slide-image         {{ width: 100%; height: 100%; object-fit: cover; border-radius: {Configuration.Border3}; }}
        .home-slide-caption       {{ height: {Configuration.HeightSlideshow}px; max-height: {Configuration.HeightSlideshow}px; overflow: hidden; border-radius: {Configuration.Border2}; padding: {Configuration.Border1}; background: {Configuration.BackgroundAlpha}; font-family: {Configuration.FontFamily}; color: {Configuration.AccentColor}; }}
        .home-slide-caption-title {{ font-size: {Configuration.FontSize3}; font-weight: {Configuration.FontWeight4}; margin-bottom: {Configuration.Spacing3}; color: {Configuration.AccentColor}; }}
        .home-slide-caption-text  {{ font-size: {Configuration.FontSize2}; line-height: {Configuration.LineHeight4}; }}
        .home-slide-counter       {{ height: {Configuration.HeightSlideshowControl}px; display: flex; align-items: center; justify-content: center; color: {Configuration.AccentColor}; font-size: {Configuration.FontSize2}; font-weight: {Configuration.FontWeight3}; }}
        div[data-testid="stButton"] > button[kind="secondary"] {{ color: {Configuration.AccentColor} !important; border: 1px solid {Configuration.AccentColor} !important; background: {Configuration.BackgroundAlpha} !important; box-shadow: none !important; font-weight: {Configuration.FontWeight4} !important; {buttonAnimCss} }}
        div[data-testid="stButton"] > button[kind="secondary"] {{ ... }}
        div[data-testid="stMarkdownContainer"]:has(.home-slide-image-shell) {{ margin-top: 0 !important; padding-top: 0 !important; }}
        div[data-testid="stMarkdownContainer"]:has(.home-slide-caption)      {{ margin-top: 0 !important; padding-top: 0 !important; }}
        div[data-testid="stColumn"]:has(.home-slide-image-shell) {{ padding-top: 0 !important; }}
        div[data-testid="stColumn"]:has(.home-slide-caption)     {{ padding-top: 0 !important; }}
    </style>"""

def TitleCss():
    'Returns CSS styles for the fixed title on the home page, adjusting position based on sidebar state.'
    return f"""<style>
        .home-title-fixed {{
            position: fixed; top: {Configuration.TitleTopPx}; left: {Configuration.TitleLeftCollapsedPx};
            margin: 0 !important; padding: 0 !important;
            color: {Configuration.PrimaryColor} !important; font-size: {Configuration.FontSize11} !important;
            line-height: {Configuration.LineHeight1} !important; font-weight: {Configuration.FontWeight4} !important;
            letter-spacing: {Configuration.LetterSpacing1} !important; font-family: {Configuration.FontFamily} !important;
            text-shadow: none !important; z-index: {Configuration.TitleZIndex}; }}
        body:has([data-testid="stSidebar"][aria-expanded="true"])  .home-title-fixed {{ left: {Configuration.TitleLeftExpandedPx}; }}
        body:has([data-testid="stSidebar"][aria-expanded="false"]) .home-title-fixed {{ left: {Configuration.TitleLeftCollapsedPx}; }}
    </style><div class="home-title-fixed">Home</div>"""

def MapContainerCss(animate):
    'Returns CSS styles for the map container on the home page, with optional animation for entering elements.'
    mapEnterCss = (f'opacity: 0; transform: translateY(28px); animation: homeMapEnterUp {Configuration.AnimationDuration} {Configuration.AnimationEasing} {Configuration.AnimationDelay3} forwards; will-change: opacity, transform;' if animate else 'opacity: 1; transform: none;')
    
    return f"""<style> html, body {{ margin: 0; padding: 0; overflow: hidden; background: transparent; }}
        .home-map-enter {{ {mapEnterCss} border-radius: {Configuration.Border2}; overflow: hidden; }}
        @keyframes homeMapEnterUp {{ from {{ opacity: 0; transform: translateY(28px); }}
                                     to   {{ opacity: 1; transform: translateY(0); }} }}
    </style>"""

# Rendering Functions
def RenderPageStyles(animate = True):
    'Renders the page styles for the home page, applying animations if specified.'
    st.markdown(PageStylesCss(animate), unsafe_allow_html=True)

def RenderTitle():
    'Renders the fixed title for the home page.'
    st.markdown(TitleCss(), unsafe_allow_html=True)

def RenderSectionTitle(title, animationClass):
    'Renders a section title with optional animation class.'
    st.markdown(SectionTitleHtml(title, animationClass), unsafe_allow_html=True)

def RenderWhoWeAre():
    'Renders the "Chi siamo" section of the home page with a title and text block.'
    RenderSectionTitle('‎ ‎ ‎ Chi siamo', animationClass='home-enter-delay-1')
    st.markdown(TextBlockHtml(Configuration.WhoWeAre, animationClass='home-enter-delay-1'), unsafe_allow_html=True)

def RenderHowItWorks():
    'Renders the "Come funziona & Dove siamo" section of the home page with a title and text block.'
    RenderSectionTitle('‎ ‎ ‎ Come funziona & Dove siamo', animationClass='home-enter-delay-3')
    st.markdown(TextBlockHtml(Configuration.HowItWorks, animationClass='home-enter-delay-3'), unsafe_allow_html=True)

def GetImageCaption(imageStem):
    'Returns the caption for a given image stem, or a default caption if not found.'
    return Configuration.ImageCaptions.get(imageStem, f'Scenario meteorologico: {imageStem.replace("_", " ").title()}.')

@st.cache_data(ttl=3600, show_spinner=False)
def LoadSlideshowData(imagesDirectory=str(Configuration.ImagesHistoryDirectory)):
    'Loads slideshow data from the specified images directory. Caches the result for 1 hour to improve performance.'
    imagesDirectory = Path(imagesDirectory)
    slideshowData   = []

    for imagePath in sorted(imagesDirectory.iterdir()):
        with open(imagePath, 'rb') as imageFile: imageB64 = base64.b64encode(imageFile.read()).decode()
        slideshowData.append({'stem': imagePath.stem, 'display_name': imagePath.stem.replace('_', ' ').title(), 'caption': GetImageCaption(imagePath.stem), 'base64': imageB64})
    return slideshowData

def SlideshowHtml(slides):
    'Builds a self-contained HTML/JS slideshow with all images embedded for zero-round-trip client-side navigation.'
    total        = len(slides)
    imgHeight    = Configuration.HeightSlideshow
    ctrlHeight   = Configuration.HeightSlideshowControl
    buttonHeight = max(ctrlHeight, 34)

    imgDivs     = ''.join(f"""<div class="slide-img" style="display:{"block" if i == 0 else "none"}"><img src="data:image/png;base64,{s["base64"]}" /></div>""" for i, s in enumerate(slides))
    captionDivs = ''.join(f"""<div class="slide-cap" style="display:{"block" if i == 0 else "none"}"><div class="cap-title">{s["display_name"]}</div><div class="cap-text">{s["caption"]}</div></div>""" for i, s in enumerate(slides))

    return f"""<!DOCTYPE html><html><head><style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ background: transparent; overflow: hidden; }}
        .slideshow  {{ width: 100%; font-family: {Configuration.FontFamily}; }}
        .slide-row  {{ display: grid; grid-template-columns: 3fr 2fr; gap: 8px; }}
        .slide-img  {{ height: {imgHeight}px; border-radius: {Configuration.Border3}; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
        .slide-img img {{ width: 100%; height: 100%; object-fit: cover; border-radius: {Configuration.Border3}; }}
        .slide-cap  {{ height: {imgHeight}px; overflow: hidden; border-radius: {Configuration.Border2}; padding: {Configuration.Border1}; background: {Configuration.BackgroundAlpha}; color: {Configuration.AccentColor}; }}
        .cap-title  {{ font-size: {Configuration.FontSize3}; font-weight: {Configuration.FontWeight4}; margin-bottom: {Configuration.Spacing3}; color: {Configuration.AccentColor}; }}
        .cap-text   {{ font-size: {Configuration.FontSize2}; line-height: {Configuration.LineHeight4}; }}
        .controls   {{ display: grid; grid-template-columns: 1fr 2fr 1fr; gap: 8px; margin-top: {Configuration.Spacing2}; align-items: center; }}
        .ctrl-btn   {{ height: {buttonHeight}px; min-height: {buttonHeight}px; background: {Configuration.BackgroundAlpha}; color: {Configuration.AccentColor}; border: 1px solid {Configuration.AccentColor}; border-radius: {Configuration.Border2}; cursor: pointer; font-weight: {Configuration.FontWeight4}; font-family: {Configuration.FontFamily}; font-size: {Configuration.FontSize2}; transition: opacity 0.15s; }}
        .ctrl-btn:hover {{ opacity: 0.75; }}
        .ctrl-counter {{ height: {ctrlHeight}px; display: flex; align-items: center; justify-content: center; color: {Configuration.AccentColor}; font-size: {Configuration.FontSize2}; font-weight: {Configuration.FontWeight3}; font-family: {Configuration.FontFamily}; }}
    </style></head><body>
    <div class="slideshow">
        <div class="slide-row"><div id="imgs">{imgDivs}</div><div id="caps">{captionDivs}</div>
        </div>
        <div class="controls"><button class="ctrl-btn" onclick="move(-1)">&#9664;</button><div class="ctrl-counter" id="counter">1 / {total}</div><button class="ctrl-btn" onclick="move(1)">&#9654;</button>
        </div>
    </div>
    <script>
        var idx = 0, total = {total};
        function move(dir) {{
            var imgs = document.querySelectorAll('.slide-img');
            var caps = document.querySelectorAll('.slide-cap');
            imgs[idx].style.display = 'none';
            caps[idx].style.display = 'none';
            idx = (idx + dir + total) % total;
            imgs[idx].style.display = 'block';
            caps[idx].style.display = 'block';
            document.getElementById('counter').textContent = (idx + 1) + ' / ' + total;
        }}
    </script>
    </body></html>"""

def RenderSlideshow():
    'Renders the slideshow as a self-contained HTML component with client-side navigation (no server round-trip on slide change).'
    slides      = LoadSlideshowData()
    totalHeight = Configuration.HeightSlideshow + max(Configuration.HeightSlideshowControl, 34) + 28
    st.components.v1.html(SlideshowHtml(slides), height=totalHeight, scrolling=False)

def RenderMap(cities, animate=True):
    'Renders a map with markers for the specified cities, applying optional animation for entering elements.'
    map = folium.Map(location=[42.5, 12.5], zoom_start=5, tiles='CartoDB positron', prefer_canvas=True)

    for _, row in cities.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']],
                      popup=folium.Popup(MapMarkerHtml(row['City']), max_width=150, min_width=120),
                      icon=folium.Icon(color='cadetblue', icon_color=Configuration.WhiteColor, prefix='fa', icon='circle'),).add_to(map)

    st.components.v1.html(f"{MapContainerCss(animate)}<div class='home-map-enter'>{map._repr_html_()}</div>", height=Configuration.HeightMap)

# Wrapper
def RenderHomeContent(cities):
    animate                           = not st.session_state.get('_home_entered', False)
    st.session_state['_home_entered'] = True
    RenderPageStyles(animate=animate)

    viewportWidth             = Configuration.ResponsiveViewportWidth
    if viewportWidth <= 1300  : leftSectionGap = f"{Configuration.ScalePx(65)}px"
    elif viewportWidth <= 1380: leftSectionGap = f"{Configuration.ScalePx(120)}px"
    else                      : leftSectionGap = Configuration.Spacing15
    if viewportWidth <= 1300  : rightSectionGap = f"{Configuration.ScalePx(165)}px"
    elif viewportWidth <= 1380: rightSectionGap = f"{Configuration.ScalePx(105)}px"
    else                      : rightSectionGap = Configuration.Spacing3

    colLeft, colRight = st.columns([1.2, 1])
    with colLeft      :
        RenderWhoWeAre()
        st.markdown(f'<div style="height: {leftSectionGap};"></div>', unsafe_allow_html=True)
        RenderSlideshow()
    with colRight     :
        RenderHowItWorks()
        st.markdown(f'<div style="height: {rightSectionGap};"></div>', unsafe_allow_html=True)
        RenderMap(cities, animate=animate)