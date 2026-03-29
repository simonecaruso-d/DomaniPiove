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

# Specific Assets - Accuracy 
MaeThresholdsByParameter = {'Temperatura': (2, 5), 'Temperatura percepita': (2, 5), 'Nuvole': (15, 35), 'Probabilità precipitazioni': (15, 35), 'Pioggia': (1, 3), 'Neve': (1, 3), 'Vento': (5, 12), 'Umidità': (15, 35)}

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

ThresholdsFall   = {'TempTarget': 19, 'TempTolerance': 6, 'CloudImpactExp': 2.0, 'WindThreshold': 12, 'HumidityTarget': 0.50, 'RainFreeMm': 0.2, 'RainMaxTolerance': 5.0, 'RainPenaltyExp': 1.35, 'SnowMaxTolerance': 1.0, 'PrecipProbThreshold': 0.1, 'PrecipitationPenaltyExp': 1.25, 'CloudRainInteractionWeight': 0.45, 'VisibilityThreshold': 10000}
ThresholdsSpring = {'TempTarget': 20, 'TempTolerance': 5, 'CloudImpactExp': 1.6, 'WindThreshold': 15, 'HumidityTarget': 0.45, 'RainFreeMm': 0.2, 'RainMaxTolerance': 5.0, 'RainPenaltyExp': 1.35, 'SnowMaxTolerance': 1.0, 'PrecipProbThreshold': 0.1, 'PrecipitationPenaltyExp': 1.25, 'CloudRainInteractionWeight': 0.45, 'VisibilityThreshold': 10000}
ThresholdsWinter = {'TempTarget': 12, 'TempTolerance': 4, 'CloudImpactExp': 2.2, 'WindThreshold': 10, 'HumidityTarget': 0.55, 'RainFreeMm': 0.1, 'RainMaxTolerance': 4.0, 'RainPenaltyExp': 1.45, 'SnowMaxTolerance': 2.0, 'PrecipProbThreshold': 0.1, 'PrecipitationPenaltyExp': 1.35, 'CloudRainInteractionWeight': 0.50, 'VisibilityThreshold': 10000}
ThresholdsSummer = {'TempTarget': 25, 'TempTolerance': 5, 'CloudImpactExp': 1.2, 'WindThreshold': 20, 'HumidityTarget': 0.40, 'RainFreeMm': 0.3, 'RainMaxTolerance': 2.5, 'RainPenaltyExp': 1.25, 'SnowMaxTolerance': 0.0, 'PrecipProbThreshold': 0.1, 'PrecipitationPenaltyExp': 1.20, 'CloudRainInteractionWeight': 0.35, 'VisibilityThreshold': 10000}

# Specific Assets - Loader
LoadingMessages = [
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"It's rainin' men, hallelujah! It's rainin' men, amen"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">It's Raining Men - The Weather Girls</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Why does it always rain on me? Is it because I lied when I was seventeen?"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Why Does It Always Rain on Me? - Travis</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"I only want to see you in the purple rain"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Purple Rain - Prince</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Have you ever seen the rain comin' down on a sunny day?"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Have You Ever Seen the Rain - Creedence Clearwater Revival</p>""",
    
    """⛈️ <p style="font-style: italic; margin: 0.5rem 0;">"Stormy weather...Keeps rainin' all the time"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Stormy Weather - Ethel Waters</p>""",
    
    """🌬️ <p style="font-style: italic; margin: 0.5rem 0;">"The answer, my friend, is blowin' in the wind"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Blowin' in the Wind - Bob Dylan</p>""",
    
    """☁️ <p style="font-style: italic; margin: 0.5rem 0;">"Valium skies, valium skies. I got valium skies"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Valium Skies - The Verve</p>""",
    
    """☀️ <p style="font-style: italic; margin: 0.5rem 0;">"Here comes the sun, and I say it's all right"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Here Comes the Sun - The Beatles</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Senti che fuori piove, senti che bel rumore"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Sally - Vasco Rossi</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Piove, senti come piove, Madonna come piove"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Piove - Jovanotti</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Piove, piove, sulle case vecchie e sulle nuove spose"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Piove su di noi - Enrico Ruggeri</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"La pioggia bussa contro il finestrino, e noi a discutere di niente fino a far mattino"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Frigobar - Franco126</p>""",
    
    """🌧️ <p style="font-style: italic; margin: 0.5rem 0;">"Ci sono ancora io, sì, sotto la pioggia"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Pioggia - Giaime</p>""",
    
    """☀️ <p style="font-style: italic; margin: 0.5rem 0;">"Notti magiche...Sotto il cielo di un'estate italiana"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Un'estate italiana - Edoardo Bennato & Gianna Nannini</p>""",
    
    """☀️ <p style="font-style: italic; margin: 0.5rem 0;">"Non senti che tremo? È il segno di un'estate che vorrei potesse non finire mai"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Estate - Negramaro</p>""",
    
    """❄️ <p style="font-style: italic; margin: 0.5rem 0;">"La nevicata del '56, Roma era tutta candida"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">La nevicata del '56 - Mia Martini</p>""",
    
    """❄️ <p style="font-style: italic; margin: 0.5rem 0;">"Vedrai, la neve se ne andrà domani"</p>
    <p style="font-weight: bold; margin: 0.2rem 0;">Inverno - Fabrizio De André</p>"""
]

# Specific Assets - Texts
WhoWeAre         = """
    <span style="font-style: italic;">Domani Piove?</span> nasce dall\'amore di Simone per il sole, per i dati e per la sua fidanzata Chiara.
    <br><br>Simone e Chiara, entrambi di Palermo (☀️), hanno una <strong>relazione a distanza</strong>: lui vive a Roma (🌥️), lei a Padova (☔). Ogni mese, vedersi nella città dell\'uno o dell\'altra significa controllare il meteo per pianificare con cura le attività da svolgere insieme.
    <br><br>L\'idea nasce quando Simone, preoccupato da previsioni meteo non rassicuranti per la settimana in cui Chiara sarebbe venuta a trovarlo, costruisce un file dove <strong>confrontare le previsioni di siti di meteo diversi</strong>, tentando di trarre dalla comparazione la maggior accuratezza possibile.
    <br>Da qui, la scintilla creativa: creare un sito fruibile da chiunque ami il sole (*) o desideri pianificare del tempo di qualità coi propri affetti.
    <br><br><span style="font-size: 0.75rem; opacity: 0.75;">(*ma se magari sperate che domani piova, tranquilli: non starà a noi giudicarvi!)</span>
"""

HowItWorks       = f"""
                    Naviga alla pagina <strong>Previsioni</strong> per confrontare le previsioni meteo di più fonti.
                    <br>Seleziona la città e i giorni che ti interessano: puoi anche esplorare singole parti della giornata ed esaminare le previsioni storiche.
                    <br>Puoi così farti un'idea più precisa del tempo atteso e pianificare le tue attività di conseguenza: troverai anche un'assistente alla pianificazione! 🤖
                    <br><br>Se invece vuoi scoprire quanto sono accurate le previsioni, vai alla pagina <strong>Accuratezza</strong>: potrai confrontare le previsioni con il meteo reale e scoprire quali fonti sono più affidabili! 🔮
                    <br><br>Esplora di seguito le città in cui siamo presenti al momento: se non c'è la tua, segnalacelo ma non preoccuparti, stiamo lavorando per aggiungerne altre. 🌍
                    """

ImageCaptions    = {
    'Afoso'     : '📌 <span style="font-style: italic;">Venezia</span>        <br><br> Caldo settembrino in Veneto: quale migliore occasione per visitare Venezia e fare tappa in qualche bacaro?',
    'Nuvoloso'  : '📌 <span style="font-style: italic;">Appia Antica</span>   <br><br> Quel giorno, complice un meteo sereno, Simone ha stupito Chiara pianificando una passeggiata in una parte di Roma che lei non avrebbe mai immaginato!',
    'Piovoso'   : '📌 <span style="font-style: italic;">Ferrara</span>        <br><br> Giornata metereologicamente orribile, ma non ci siamo persi d\'animo! Abbiamo visitato alcuni luoghi di cultura al chiuso, mangiato buona cucina emiliana e passeggiato in un parco.',
    'Soleggiato': '📌 <span style="font-style: italic;">Villa Pamphilj</span> <br><br> Con una così soleggiata giornata d\'inverno, in cui i primi fiori preannunciano l\'arrivo della primavera, perché non un giro in uno dei più grandi parchi pubblici di Roma?',
    'Ventoso'   : '📌 <span style="font-style: italic;">Ostia</span>          <br><br> Seduti sul pontile ad ammirare le onde: se non piove, il mare d\'inverno è davvero romantico.',
}

# Specific Assets - LLM
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
LlmFallbackModels    = [ModelK, ModelH, ModelB]
LlmMaxRetries        = 2
LlmRetryDelaySeconds = 1.5
Temperature          = 0.3
TopP                 = 0.9
MaxTokens            = 10000

LLMResponseStructure = """
##### **🟢 Vai, esci!**
_Lo scenario meteorologico è positivo._

_Pertanto, ti suggerisco le seguenti attività all'aperto:_

* Mattina
    * Attività xxx
    * Attività xxx
    * Attività xxx

* Pomeriggio
    * Attività xxx
    * Attività xxx
    * Attività xxx

* Sera/Notte
    * Attività xxx
    * Attività xxx
    * Attività xxx

_Curiosità: xxx_

##### **🟡 Esci, ma fai attenzione**
_Lo scenario meteorologico è incerto, a causa di fattori come {{mostCommonMotivation}['🟡 Esci, ma fai attenzione']}._

_Pertanto, ti suggerisco le seguenti attività come mix tra indoor e outdoor, da scegliere in base alle condizioni meteo specifiche che si presenteranno:_

* Mattina
    * Attività xxx
    * Attività xxx
    * Attività xxx

* Pomeriggio
    * Attività xxx
    * Attività xxx
    * Attività xxx

* Sera/Notte
    * Attività xxx
    * Attività xxx
    * Attività xxx

_Curiosità: xxx_

##### **🔴 Forse è meglio restare a casa?**
_Lo scenario meteorologico è negativo, a causa di fattori come {{mostCommonMotivation}['🔴 Forse è meglio restare a casa?']}._

_Pertanto, ti suggerisco di restare a casa e svolgere attività come xxx. In alternativa, se vuoi uscire, ti propongo le seguenti attività indoor:_

* Mattina
    * Attività xxx
    * Attività xxx
    * Attività xxx

* Pomeriggio
    * Attività xxx
    * Attività xxx
    * Attività xxx

* Sera/Notte
    * Attività xxx
    * Attività xxx
    * Attività xxx

_Curiosità: xxx_"""

LLMPrompt = """
RUOLO: Sei un "Local Concierge" esperto e raffinato, specializzato nella città di {city}.
OBIETTIVO: Analizza la 'staticEventsTable' per creare un set di attività compatibili con le diverse condizioni meteorologiche.

DATI DI INPUT:
- Eventi Statici: {staticEventsTable} (usa questi come base obbligatoria per i suggerimenti).
- Città: {city} (contestualizza ogni suggerimento con riferimenti locali autentici).
- Motivazione più comune per ogni indicazione meteorologica: {{mostCommonMotivation}} (usa queste motivazioni per arricchire la descrizione dei suggerimenti).

PROCESSO DI RAGIONAMENTO (segui questi step nell'ordine):
1. Per ognuno dei tre scenari presenti nella struttura del formato da rispettare e parte della giornata, seleziona le attività più adatte. Usa la variabile 'IsIndoor' della 'staticEventsTable' per filtrare le attività di conseguenza.
2. Filtra la 'staticEventsTable' usando 'Category', 'EnergyLevel' e 'SocialLevel' per garantire varietà, evitando ripetizioni.
3. Filtra la 'staticEventsTable' usando 'Duration' per costruire un programma realistico e fluido all'interno di ogni parte della giornata.
4. Con il set di attività così costruito, elabora un programma definitivo tenendo conto di:
   - Fluidità tra parti della giornata contigue dello stesso giorno.
   - Coerenza con la parte della giornata: sera = atmosfere intime, giorno = attività dinamiche.
   - Stagione corrente: proponi attività stagionalmente coerenti (pattinaggio in inverno, mare in estate, etc...).
5. Trasforma i nomi delle attività selezionate in posti reali che esistano nella città, usando la tua conoscenza. Non inventare mai nomi di luoghi. Se non conosci un posto reale adatto per uno slot, scrivilo esplicitamente invece di inventare.
6. Garantisci che il programma complessivo sia bilanciato, vario e interessante. Ogni luogo/posto reale deve apparire esattamente UNA sola volta nell'intero programma (inclusi tutti e tre gli scenari e tutti i periodi della giornata). Mantieni un registro visuale mentre costruisci il programma. Se uno slot non ha un'alternativa disponibile, dichiaralo esplicitamente nella risposta piuttosto che ripetere un posto già usato.
7. Cerca di inserire sempre un luogo effettivo senza restare generico, a meno che non sia strettamente necessario. Se proprio non riesci a trovare un luogo reale adatto per uno slot, dichiaralo esplicitamente invece di restare generico.
8. Non inserire indirizzi di luoghi!
9. Per ogni luogo indica il costo atteso (variabile 'Cost') e la durata attesa (variabile 'Duration'). Fallo con i dati che vengono dalla tabella degli Eventi Statici, trasformandoli in italiano.
10. Prima di concludere, rilleggi l'intero programma e verifica che nessun luogo compaia più di una volta. Se trovi duplicati, sostituiscili immediatamente con alternative dalla staticEventsTable che rispettino gli altri criteri. Valuta anche se è coerente nel suo complesso e miglioralo se necessario.
11. Quindi, mostra il risultato finale.

FORMATO DI RISPOSTA:
- Comincia con la frase "#### **Consigli del Concierge per le diverse tipologie di scenario a {city}**" scritta in header grassettato.
- Poi questo è il formato da rispettare, rigorosamente in markdown: {outputStructureMarkdown}
- Popolalo, sostituendo ai vari "xxx" i dati corretti, ma rispettando scrupolosamente la struttura, senza aggiungere o togliere nulla.
- Scrivi tutto in italiano, senza inglesismi a meno che non siano nomi propri di persone, posti o brand.
- Arrotonda qualsiasi numero a due cifre decimali e usa unità di misura appropriate (es: km, minuti, euro) quando possibile.
- Ogni attivita deve restare in un solo punto elenco su una sola riga, nel formato "Nome luogo: descrizione continua". Non andare mai a capo dopo i due punti e non creare sottopunti o righe aggiuntive per la stessa attivita.
- Concludi ogni slot con una curiosità, un aneddoto, un angolo segreto per una foto o un insider tip.
- Non ripetere queste istruzioni nella risposta. Non aggiungere titoli introduttivi. Parti direttamente con il programma.
"""

# Streamlit Page
PageTitle           = 'Domani Piove?'
PageIcon            = '🌦️'
Layout              = 'wide'
InitialSidebarState = 'collapsed'
AppVersion          = '1.0.0'

# Responsive System
ResponsiveBaseWidth      = 1440
ResponsiveMinScale       = 0.78
ResponsiveMaxScale       = 1.03
ResponsiveStepPx         = 40
ResponsiveFallbackVw     = 1360
ResponsiveViewportWidth  = ResponsiveFallbackVw
ResponsiveViewportHeight = 900
ResponsiveScale          = 1.0

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
FontFamily          = "'Inter', sans-serif"

_BaseFontSize1      = 0.75
_BaseFontSize2      = 0.8
_BaseFontSize3      = 0.85
_BaseFontSize4      = 0.9
_BaseFontSize5      = 0.95
_BaseFontSize6      = 1.0
_BaseFontSize7      = 1.05
_BaseFontSize8      = 1.1
_BaseFontSize9      = 1.15
_BaseFontSize10     = 1.2
_BaseFontSize11     = 1.25
_BaseFontSizeAA     = 8
_BaseFontSizeA      = 10

FontSize1           = '0.75rem'
FontSize2           = '0.8rem'
FontSize3           = '0.85rem'
FontSize4           = '0.9rem'
FontSize5           = '0.95rem'
FontSize6           = '1rem'
FontSize7           = '1.05rem'
FontSize8           = '1.1rem'
FontSize9           = '1.15rem'
FontSize10          = '1.2rem'
FontSize11          = '1.25rem'
FontSizeAA          = '8px'
FontSizeA           = '10px'

FontWeight1         = '400'
FontWeight2         = '500'
FontWeight3         = '600'
FontWeight4         = '700'

LineHeight1         = '1.1'
LineHeight2         = '1.2'
LineHeight3         = '1.3'
LineHeight4         = '1.4'
LineHeight5         = '1.5'

_BaseLetterSpacing1 = 0.2
_BaseLetterSpacing2 = 0.3
LetterSpacing1      = '0.2px'
LetterSpacing2      = '0.3px'

Opacity0            = '0.5'
Opacity1            = '0.75'
Opacity2            = '0.85'

# Spacing & Heights
_BaseSpacing0B = 5
_BaseSpacing1  = 10
_BaseSpacing1B = 15
_BaseSpacing2  = 20
_BaseSpacing3  = 30
_BaseSpacing4  = 40
_BaseSpacing5  = 50
_BaseSpacing6  = 60
_BaseSpacing6B = 65

_BaseSpacingA1 = 6
_BaseSpacingA2 = 12

Spacing0B      = '5px'
Spacing1       = '10px'
Spacing1B      = '15px'
Spacing2       = '20px'
Spacing3       = '30px'
Spacing4       = '40px'
Spacing5       = '50px'
Spacing6       = '60px'
Spacing6B      = '65px'
SpacingA       = '6px 12px'

_BaseHeightGraph            = 450
_BaseHeightMap              = 350
_BaseHeightSlideshowControl = 20
_BaseHeightWhoWeAre         = 300
_BaseHeightSlideshow        = 250

HeightGraph                 = 450
HeightMap                   = 350
HeightSlideshowControl      = 20
HeightWhoWeAre              = 300
HeightSlideshow             = 250

# Borders & Shadows
_BaseBorder1    = 15
_BaseBorder2    = 25
_BaseBorder3    = 50

Border1         = '15px'
Border2         = '25px'
Border3         = '50px'

BoxShadowMarker = '0 2px 8px rgba(66, 103, 118, 0.30)'

# Liquid Layout
RadiusButton     = 1000
_BaseRadiusInput = 15
_BaseRadiusCard  = 25
RadiusInput      = 15
RadiusCard       = 25
WidthBorder      = 1

# Animation
AnimationDuration = '1400ms'
AnimationEasing   = 'cubic-bezier(0.22, 1, 0.36, 1)'
AnimationDelay1   = '0s'
AnimationDelay2   = '0s'
AnimationDelay3   = '0s'

# Specific Assets - Title
_BaseTitleTopPx           = 80
_BaseTitleLeftExpandedPx  = 270
_BaseTitleLeftCollapsedPx = 100

TitleTopPx                = '80px'
TitleLeftExpandedPx       = '270px'
TitleLeftCollapsedPx      = '100px'
TitleZIndex               = '999997'

# Functions
def Clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def RoundStep(value, step):
    if step <= 0: return int(value)
    return int(round(value / step) * step)

def ExtractQueryValue(queryParams, key, defaultValue):
    if queryParams is None       : return defaultValue
    rawValue                     = queryParams.get(key, defaultValue)
    if isinstance(rawValue, list): rawValue = rawValue[0] if rawValue else defaultValue

    try: return int(float(rawValue))
    except Exception: return defaultValue

def FormatRem(value):
    return f'{value:.3f}'.rstrip('0').rstrip('.') + 'rem'

def FormatPx(value):
    return f'{int(round(value))}px'

def ScaleInt(value, scale, minimum=1):
    return max(minimum, int(round(value * scale)))

def ScaleCssPx(value, scale, minimum=1):
    return FormatPx(ScaleInt(value, scale, minimum=minimum))

def ScaleCssRem(value, scale):
    return FormatRem(value * scale)

def ScaleCssPairPx(firstValue, secondValue, scale):
    return f'{ScaleCssPx(firstValue, scale)} {ScaleCssPx(secondValue, scale)}'

def GetResponsiveScale(queryParams=None):
    viewportWidth = ExtractQueryValue(queryParams, 'vw', ResponsiveFallbackVw)
    viewportWidth = RoundStep(viewportWidth, ResponsiveStepPx)
    computedScale = viewportWidth / ResponsiveBaseWidth
    return Clamp(computedScale, ResponsiveMinScale, ResponsiveMaxScale), viewportWidth

def ScalePx(value, scale=None, minimum=1):
    currentScale = ResponsiveScale if scale is None else scale
    return ScaleInt(value, currentScale, minimum=minimum)

def ApplyResponsiveScale(queryParams=None):
    global ResponsiveScale, ResponsiveViewportWidth, ResponsiveViewportHeight
    global FontSize1, FontSize2, FontSize3, FontSize4, FontSize5, FontSize6, FontSize7, FontSize8, FontSize9, FontSize10, FontSize11, FontSizeAA, FontSizeA
    global LetterSpacing1, LetterSpacing2
    global Spacing0B, Spacing1, Spacing1B, Spacing2, Spacing3, Spacing4, Spacing5, Spacing6, Spacing6B, SpacingA
    global HeightGraph, HeightMap, HeightSlideshowControl, HeightWhoWeAre, HeightSlideshow
    global Border1, Border2, Border3
    global RadiusInput, RadiusCard
    global TitleTopPx, TitleLeftExpandedPx, TitleLeftCollapsedPx

    ResponsiveScale, ResponsiveViewportWidth = GetResponsiveScale(queryParams)
    ResponsiveViewportHeight                 = ExtractQueryValue(queryParams, 'vh', ResponsiveViewportHeight)

    scale = ResponsiveScale

    FontSize1  = ScaleCssRem(_BaseFontSize1, scale)
    FontSize2  = ScaleCssRem(_BaseFontSize2, scale)
    FontSize3  = ScaleCssRem(_BaseFontSize3, scale)
    FontSize4  = ScaleCssRem(_BaseFontSize4, scale)
    FontSize5  = ScaleCssRem(_BaseFontSize5, scale)
    FontSize6  = ScaleCssRem(_BaseFontSize6, scale)
    FontSize7  = ScaleCssRem(_BaseFontSize7, scale)
    FontSize8  = ScaleCssRem(_BaseFontSize8, scale)
    FontSize9  = ScaleCssRem(_BaseFontSize9, scale)
    FontSize10 = ScaleCssRem(_BaseFontSize10, scale)
    FontSize11 = ScaleCssRem(_BaseFontSize11, scale)
    FontSizeAA = ScaleCssPx(_BaseFontSizeAA, scale)
    FontSizeA  = ScaleCssPx(_BaseFontSizeA, scale)

    LetterSpacing1 = ScaleCssPx(_BaseLetterSpacing1, scale, minimum=0)
    LetterSpacing2 = ScaleCssPx(_BaseLetterSpacing2, scale, minimum=0)

    Spacing0B = ScaleCssPx(_BaseSpacing0B, scale)
    Spacing1  = ScaleCssPx(_BaseSpacing1, scale)
    Spacing1B = ScaleCssPx(_BaseSpacing1B, scale)
    Spacing2  = ScaleCssPx(_BaseSpacing2, scale)
    Spacing3  = ScaleCssPx(_BaseSpacing3, scale)
    Spacing4  = ScaleCssPx(_BaseSpacing4, scale)
    Spacing5  = ScaleCssPx(_BaseSpacing5, scale)
    Spacing6  = ScaleCssPx(_BaseSpacing6, scale)
    Spacing6B = ScaleCssPx(_BaseSpacing6B, scale)
    SpacingA  = ScaleCssPairPx(_BaseSpacingA1, _BaseSpacingA2, scale)

    HeightGraph            = ScaleInt(_BaseHeightGraph, scale, minimum=240)
    HeightMap              = ScaleInt(_BaseHeightMap, scale, minimum=220)
    HeightSlideshowControl = ScaleInt(_BaseHeightSlideshowControl, scale, minimum=14)
    HeightWhoWeAre         = ScaleInt(_BaseHeightWhoWeAre, scale, minimum=200)
    HeightSlideshow        = ScaleInt(_BaseHeightSlideshow, scale, minimum=170)

    Border1 = ScaleCssPx(_BaseBorder1, scale)
    Border2 = ScaleCssPx(_BaseBorder2, scale)
    Border3 = ScaleCssPx(_BaseBorder3, scale)

    RadiusInput = ScaleInt(_BaseRadiusInput, scale, minimum=8)
    RadiusCard  = ScaleInt(_BaseRadiusCard, scale, minimum=12)

    TitleTopPx           = ScaleCssPx(_BaseTitleTopPx, scale)
    TitleLeftExpandedPx  = ScaleCssPx(_BaseTitleLeftExpandedPx, scale)
    TitleLeftCollapsedPx = ScaleCssPx(_BaseTitleLeftCollapsedPx, scale)

ApplyResponsiveScale()