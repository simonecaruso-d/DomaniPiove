# Environment Setting
from dotenv import load_dotenv
import os 
from pathlib import Path as _Path

# API Keys
load_dotenv()
OpenRouterKey = os.getenv("OPENROUTER_API_KEY")

# Assets
LogoPath               = _Path(__file__).resolve().parents[2] / 'files' / 'logo.png'
HomeIconPath           = _Path(__file__).resolve().parents[2] / 'files' / 'Home.png'
WeatherIconPath        = _Path(__file__).resolve().parents[2] / 'files' / 'Weather.png'
AccuracyIconPath       = _Path(__file__).resolve().parents[2] / 'files' / 'Accuracy.png'
EmailIconPath          = _Path(__file__).resolve().parents[2] / 'files' / 'Email.png'
CopyrightIconPath      = _Path(__file__).resolve().parents[2] / 'files' / 'Copyright.png'
ImagesHistoryDirectory = _Path(__file__).resolve().parents[2] / 'files' / 'ImagesHistory'

# Streamlit Page
PageTitle           = 'Domani Piove?'
PageIcon            = '🌦️'
Layout              = 'wide'
InitialSidebarState = 'collapsed'

# Pages & Icons
Pages           = ['Home', 'Previsioni', 'Accuratezza']
PageIconPaths   = {'Home': HomeIconPath, 'Previsioni': WeatherIconPath, 'Accuratezza': AccuracyIconPath}
FooterIconPaths = {'Email': EmailIconPath, 'Copyright': CopyrightIconPath}

# Colors
WhiteColor         = '#FFFFFF'
AccentColor        = '#426776'
PrimaryColor       = '#AB8674'
TertiaryColor      = '#EDE4DF'
BackgroundAlpha    = 'rgba(66, 103, 118, 0.08)'
BackgroundText     = 'rgba(255,255,255,0.2)'

Palette1VeryLight  = '#998160'
Palette1Light      = '#807d52'
Palette1Medium     = '#617a4d'
Palette1Dark       = '#3a7553'
Palette1VeryDark   = '#006f60'

Palette2VeryLight  = '#8A7C73'
Palette2Light      = '#6b5c73'
Palette2Medium     = '#4b5269'
Palette2Dark       = '#2f4858'
Palette2ByProvider = ['#886676', '#6b5c73', '#4b5269', '#2f4858']

# Fonts & Typography
FontFamily = "'Inter', sans-serif"

FontSize1  = '0.75rem'
FontSize2  = '0.8rem'
FontSize3  = '0.85rem'
FontSize4  = '0.9rem'
FontSize5  = '0.95rem'
FontSize6  = '1rem'
FontSize7  = '1.05rem'
FontSize8  = '1.1rem'
FontSize9  = '1.15rem'
FontSize10 = '1.2rem'
FontSize11 = '1.25rem'
FontSizeAA = '8px'
FontSizeA  = '10px'

FontWeight1 = '400'
FontWeight2 = '500'
FontWeight3 = '600'
FontWeight4 = '700'

LineHeight1 = '1.1'
LineHeight2 = '1.2'
LineHeight3 = '1.3'
LineHeight4 = '1.4'
LineHeight5 = '1.5'

LetterSpacing1 = '0.2px'
LetterSpacing2 = '0.3px'

Opacity0 = '0.5'
Opacity1 = '0.75'
Opacity2 = '0.85'

# Spacing & Heights
Spacing0B = '5px'
Spacing1  = '10px'
Spacing1B = '15px'
Spacing2  = '20px'
Spacing3  = '30px'
Spacing4  = '40px'
Spacing5  = '50px'
Spacing6  = '60px'
Spacing6B = '65px'

SpacingA  = '6px 12px'

HeightGraph             = 450
HeightMap               = 350
HeightSlideshowControl  = 20
HeightWhoWeAre          = 300
HeightSlideshow         = 250

# Borders & Shadows
Border1 = '15px'
Border2 = '25px'
Border3 = '50px'

BoxShadowMarker    = '0 2px 8px rgba(66, 103, 118, 0.30)'

# Liquid Layout
RadiusButton = 1000
RadiusInput  = 15
RadiusCard   = 25
WidthBorder  = 1

# Animation
AnimationDuration       = '1400ms'
AnimationEasing         = 'cubic-bezier(0.22, 1, 0.36, 1)'
AnimationDelay1         = '0s'
AnimationDelay2         = '0s'
AnimationDelay3         = '0s'

# Specific Assets - Title
TitleTopPx              = '80px'
TitleLeftExpandedPx     = '270px'
TitleLeftCollapsedPx    = '100px'
TitleZIndex             = '999997'

# Specific Assets - Accuracy 
MaeThresholdsByParameter = {'Temperatura':                (2, 5),
                            'Temperatura percepita':      (2, 5),
                            'Nuvole':                     (15, 35),
                            'Probabilità precipitazioni': (15, 35),
                            'Pioggia':                    (1, 3),
                            'Neve':                       (1, 3),
                            'Vento':                      (5, 12),
                            'Umidità':                    (15, 35)}

# Specific Assets - Measures
Parameters             = ['Temperatura', 'Temperatura percepita', 'Nuvole', 'Probabilità precipitazioni', 'Pioggia', 'Neve', 'Vento', 'Umidità']
ParametersEng          = {'Temperatura': 'Temperature', 'Temperatura percepita': 'FeltTemperature', 'Nuvole': 'CloudCover', 'Probabilità precipitazioni': 'PrecipitationProb', 'Pioggia': 'Rain', 'Neve': 'Snowfall', 'Vento': 'WindSpeed', 'Umidità': 'Humidity',}
ParametersEng2         = {'Temperatura': 'Temperature', 'Temperatura percepita': 'FeltTemperature', 'Nuvole': 'CloudCover', 'Probabilità precipitazioni': 'PrecipitationProbability', 'Pioggia': 'Rain', 'Neve': 'Snowfall', 'Vento': 'WindSpeed', 'Umidità': 'Humidity',}
ParametersMeasureUnits = {'Umidità': '%', 'Nuvole': '%', 'Probabilità precipitazioni': '%', 'Vento': ' km/h', 'Pioggia': ' mm', 'Neve': ' mm', 'Temperatura': ' °C', 'Temperatura percepita': ' °C',}
ParametersScale        = {'Umidità': 100, 'Nuvole': 100, 'Probabilità precipitazioni': 100}

# Specific Assets - Filters
PartOfDayOrder = ['Morning', 'Lunch', 'Afternoon', 'Dinner', 'Night']
PartOfDayToIta = {'Morning': 'Mattina', 'Lunch': 'Pranzo', 'Afternoon': 'Pomeriggio', 'Dinner': 'Cena', 'Night': 'Notte'}
PartOfDayToEng = {v: k for k, v in PartOfDayToIta.items()}

# Specific Assets - Table for Advice
ScoresWeights    = {'ScoreFeltTemperature': 0.3, 'ScoreCloudCover': 0.25, 'ScorePrecipitationProbability': 0.25, 'ScoreWind': 0.1, 'ScoreVisibility': 0.05, 'ScoreHumidity': 0.05}

ThresholdsFall   = {'TempTarget': 19, 'TempTolerance': 6, 'CloudImpactExp': 2.0, 'WindThreshold': 12, 'HumidityTarget': 0.50, 'RainMaxTolerance': 7.0, 'SnowMaxTolerance': 1.0, 'PrecipProbThreshold': 0.1, 'VisibilityThreshold': 10000}
ThresholdsSpring = {'TempTarget': 20, 'TempTolerance': 5, 'CloudImpactExp': 1.5, 'WindThreshold': 15, 'HumidityTarget': 0.45, 'RainMaxTolerance': 7.0, 'SnowMaxTolerance': 1.0, 'PrecipProbThreshold': 0.1, 'VisibilityThreshold': 10000}
ThresholdsWinter = {'TempTarget': 12, 'TempTolerance': 4, 'CloudImpactExp': 2.0, 'WindThreshold': 10, 'HumidityTarget': 0.55, 'RainMaxTolerance': 6.0, 'SnowMaxTolerance': 2.0, 'PrecipProbThreshold': 0.1, 'VisibilityThreshold': 10000}
ThresholdsSummer = {'TempTarget': 25, 'TempTolerance': 5, 'CloudImpactExp': 1.0, 'WindThreshold': 20, 'HumidityTarget': 0.40, 'RainMaxTolerance': 3.0, 'SnowMaxTolerance': 0.0, 'PrecipProbThreshold': 0.1, 'VisibilityThreshold': 10000}

# Specific Assets - Loader
LoadingMessages = [
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"It's rainin' men, hallelujah! It's rainin' men, amen"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">It's Raining Men – The Weather Girls</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Why does it always rain on me? Is it because I lied when I was seventeen?"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Why Does It Always Rain on Me? – Travis</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"I only want to see you in the purple rain"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Purple Rain – Prince</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Have you ever seen the rain comin' down on a sunny day?"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Have You Ever Seen the Rain – Creedence Clearwater Revival</p>""",
    
    """⛈️ <p style="font-style: italic; margin: 0.5rem 0;">"Stormy weather...Keeps rainin' all the time"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Stormy Weather – Ethel Waters</p>""",
    
    """🌬️ <p style="font-style: italic; margin: 0.5rem 0;">"The answer, my friend, is blowin' in the wind"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Blowin' in the Wind – Bob Dylan</p>""",
    
    """☁️ <p style="font-style: italic; margin: 0.5rem 0;">"Valium skies, valium skies. I got valium skies"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Valium Skies – The Verve</p>""",
    
    """☀️ <p style="font-style: italic; margin: 0.5rem 0;">"Here comes the sun, and I say it's all right"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Here Comes the Sun – The Beatles</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Senti che fuori piove, senti che bel rumore"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Sally – Vasco Rossi</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Piove, senti come piove, Madonna come piove"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Piove – Jovanotti</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Piove, piove, sulle case vecchie e sulle nuove spose"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Piove su di noi – Enrico Ruggeri</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"La pioggia bussa contro il finestrino, e noi a discutere di niente fino a far mattino"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Frigobar – Franco126</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Ci sono ancora io, sì, sotto la pioggia"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Pioggia – Giaime</p>""",
    
    """☀️ <p style="font-style: italic; margin: 0.5rem 0;">"Notti magiche...Sotto il cielo di un'estate italiana"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Un'estate italiana – Edoardo Bennato & Gianna Nannini</p>""",
    
    """☀️ <p style="font-style: italic; margin: 0.5rem 0;">"Non senti che tremo? È il segno di un'estate che vorrei potesse non finire mai"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Estate – Negramaro</p>""",
    
    """❄️ <p style="font-style: italic; margin: 0.5rem 0;">"La nevicata del '56, Roma era tutta candida"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">La nevicata del '56 – Mia Martini</p>""",
    
    """❄️ <p style="font-style: italic; margin: 0.5rem 0;">"Vedrai, la neve se ne andrà domani"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Inverno – Fabrizio De André</p>"""
]

# Specific Assets - Texts
WhoWeAre         = f"""
    <span style="font-style: italic;">Domani piove?</span> nasce dall\'amore di Simone per il sole, per i dati e per la sua fidanzata Chiara.
    <br><br>Simone e Chiara, entrambi di Palermo (☀️), hanno una <strong>relazione a distanza</strong>: lui vive a Roma (🌥️), lei a Padova (☔). Ogni mese, vedersi nella città dell\'uno o dell\'altra significa controllare il meteo per pianificare con cura le attività da svolgere insieme.
    <br><br>L\'idea nasce quando Simone, preoccupato da previsioni meteo non rassicuranti per la settimana in cui Chiara sarebbe venuto a trovarlo, costruisce un file Excel dove <strong>confrontare le previsioni di siti di meteo diversi</strong>, tentando di trarre dalla comparazione la maggior accuratezza possibile.
    <br>Da qui, la scintilla creativa: creare un sito fruibile da chiunque ami il sole (*) o desideri pianificare del tempo di qualità coi propri affetti.
    <br><br><span style="font-size: {FontSize1}; opacity: {Opacity1};">(*ma se magari sperate che domani piova, tranquilli: non starà a noi giudicarvi!)</span>
"""

HowItWorks       = f"""
                    Naviga alla pagina <strong>Previsioni</strong> per confrontare le previsioni meteo di più fonti.
                    <br>Seleziona la città e i giorni che ti interessano: puoi anche esplorare singole parti della giornata ed esaminare le previsioni storiche.
                    <br>Puoi così farti un'idea più precisa del tempo atteso e pianificare le tue attività di conseguenza: troverai anche un'assistente alla pianificazione! 🤖
                    <br><br>Se invece vuoi scoprire quanto sono accurate le previsioni, vai alla pagina <strong>Accuratezza</strong>: potrai confrontare le previsioni con il meteo reale e scoprire quali fonti sono più affidabili! 🔮
                    <br><br>Esplora di seguito le città in cui siamo presenti al momento: se non c'è la tua, segnalacelo ma non preoccuparti, stiamo lavorando per aggiungerne altre 🌍
                    """

ImageCaptions    = {
    'Afoso'     : '📌 <span style="font-style: italic;">Venezia</span>        <br><br> Caldo settembrino in Veneto: quale migliore occasione per visitare Venezia e fare tappa in qualche bacaro?',
    'Nuvoloso'  : '📌 <span style="font-style: italic;">Appia Antica</span>   <br><br> Quel giorno Simo ha stupito Chiara pianificando una passeggiata in una parte di Roma che lei non avrebbe mai immaginato!',
    'Piovoso'   : '📌 <span style="font-style: italic;">Ferrara</span>        <br><br> Giornata metereologicamente orribile, ma non ci siamo persi d\'animo! Abbiamo visitato alcuni luoghi di cultura al chiuso, mangiato buona cucina emiliana nella più antica osteria del mondo e addirittura passeggiato in un parco',
    'Soleggiato': '📌 <span style="font-style: italic;">Villa Pamphili</span> <br><br> Con una giornata d\'inverno così soleggiata in cui i primi fiori preannunciano l\'arrivo della primavera, perché non un giro in uno dei più grandi parchi pubblici di Roma?',
    'Ventoso'   : '📌 <span style="font-style: italic;">Ostia</span>          <br><br> Seduti sul pontile ad ammirare le onde: se non piove, il mare d\'inverno è davvero romantico',
}

# Specific Assets - LLM
MaxTokens   = 10000
ModelA      = 'nvidia/nemotron-3-super-120b-a12b:free' # Buono ma lento
ModelB      = 'liquid/lfm-2.5-1.2b-thinking:free' # Il più veloce
ModelC      = 'nvidia/nemotron-3-nano-30b-a3b:free' # Scarsino ma veloce
ModelD      = 'nvidia/nemotron-nano-9b-v2:free' # Scarso e lento
ModelE      = 'cognitivecomputations/dolphin-mistral-24b-venice-edition:free' #rotto quando ho provato
ModelF      = 'google/gemma-3n-e2b-it:free' # il migliore ma ha un limite naturale a 2k token
ModelG      = 'bytedance-seed/seedream-4.5' # non ha funzionato
ModelH      = 'z-ai/glm-4.5-air:free' # mediocre
ModelI      = 'stepfun/step-3.5-flash:free' # 10k token non bastano
ModelJ      = 'nvidia/nemotron-3-super-120b-a12b:free' # 10k token non bastano
ModelK      = 'arcee-ai/trinity-mini:free' # IL VINCITORE
Temperature = 0.3
TopP        = 0.9

LLMResponseStructure = f"""
##### _Giorno n - dd/mm/yyyy_
###### _Mattina_ 🌞
Lo scenario meteo previsto suggerisce di ...
Pertanto, ti suggerisco le seguenti attività:
* Attività 1,
* Attività 2
* Attività 3

> Curiosità: 

###### _Pranzo_ 🍝
Lo scenario meteo previsto suggerisce di ...
Pertanto, ti suggerisco le seguenti attività:
* Attività 1,
* Attività 2
* Attività 3

> Curiosità: 

###### _Pomeriggio_ 🍵
Lo scenario meteo previsto suggerisce di ...
Pertanto, ti suggerisco le seguenti attività:
* Attività 1,
* Attività 2
* Attività 3

> Curiosità: 

###### _Cena_ 🍕
Lo scenario meteo previsto suggerisce di ...
Pertanto, ti suggerisco le seguenti attività:
* Attività 1,
* Attività 2
* Attività 3

> Curiosità: 

###### _Notte_ 🌖
Lo scenario meteo previsto suggerisce di ...
Pertanto, ti suggerisco le seguenti attività:
* Attività 1,
* Attività 2
* Attività 3

> Curiosità: 
"""

LLMPrompt = """
RUOLO: Sei un "Local Concierge" esperto e raffinato, specializzato nella città di {city}.
OBIETTIVO: Analizza la 'weatherConditionTable' e la 'staticEventsTable' per creare un itinerario di attività personalizzato.

DATI DI INPUT:
- Tabella Meteo: {weatherConditionTable} (usa tutte le colonne come guida, in particolare 'Indicazione' e 'Punteggio').
- Eventi Statici: {staticEventsTable} (usa questi come base obbligatoria per i suggerimenti).
- Città: {city} (contestualizza ogni suggerimento con riferimenti locali autentici).
- Data di inizio {startDate} e Data di fine {endDate} da rispettare fedelissimamente (considera la stagione e gli eventi locali).

PROCESSO DI RAGIONAMENTO (segui questi step nell'ordine):
1. Per ogni giorno e parte della giornata, analizza il meteo dalla 'weatherConditionTable' e determina se le condizioni sono adatte a stare dentro o fuori. Usa la variabile 'IsIndoor' della 'staticEventsTable' per filtrare le attività di conseguenza.
2. Filtra la 'staticEventsTable' usando 'Category', 'EnergyLevel' e 'SocialLevel' per garantire varietà sia all'interno della stessa giornata che tra giorni diversi, evitando ripetizioni.
3. Filtra la 'staticEventsTable' usando 'Duration' per costruire un programma realistico e fluido all'interno di ogni parte della giornata.
4. Con il set di attività così costruito, elabora un programma definitivo tenendo conto di:
   - Fluidità tra parti della giornata contigue dello stesso giorno.
   - Giorno della settimana: nei giorni feriali proponi massimo 1-2 attività per parte della giornata, nel weekend puoi essere più ricco. Ma includi SEMPRE tutti i giorni presenti nella {weatherConditionTable}, senza saltarne nessuno.
   - Coerenza con la parte della giornata: sera = atmosfere intime, giorno = attività dinamiche.
   - Stagione corrente: proponi attività stagionalmente coerenti (pattinaggio in inverno, mare in estate, etc...).
   - Grandi eventi o festività (Pasqua, Natale, Carnevale, Ferragosto, etc...) per esperienze uniche e contestualizzate.
5. Trasforma i nomi delle attività selezionate in posti reali che esistano nella città, usando la tua conoscenza. Non inventare mai nomi di luoghi. Se non conosci un posto reale adatto per uno slot, scrivilo esplicitamente invece di inventare.
6. Considera la distanza tra i luoghi che suggerisci nella stessa giornata, se a te nota, per costruire un itinerario logisticamente sensato.

FORMATO DI RISPOSTA:
- Comincia con il titolo in grassetto "Consigli del Concierge per i giorni dal {startDate} al {endDate} a {city}"
- Poi questo è il formato da rispettare: {outputStructureMarkdown}
- Popolalo ripetendolo esattamente identico per tutti i giorni che vedi dalla tabella, sostituendo "Giorno n" e "dd/mm/yyyy" con i dati corretti, e inserendo le attività suggerite per ogni slot: non saltare nessun giorno e non cambiare il formato da un giorno all'altro, deve essere tutto identico!
- Scrivi tutto in italiano, senza inglesismi a meno che non siano nomi propri di persone, posti o brand.
- Arrotonda qualsiasi numero a due cifre decimali e usa unità di misura appropriate (es: km, minuti, euro) quando possibile.
- Per ogni attività indica il costo atteso (variabile 'Cost') e la durata attesa (variabile 'Duration').
- Concludi ogni slot con una curiosità, un aneddoto, un angolo segreto per una foto o un insider tip.
- Non ripetere queste istruzioni nella risposta. Non aggiungere titoli introduttivi. Parti direttamente con il programma.
"""