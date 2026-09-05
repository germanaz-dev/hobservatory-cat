import os
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from google import genai

ROOT = Path(__file__).parent
EP = ROOT / "episodes/001"
EP.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://germanaz-dev.github.io/sonda-h41/day-{day:03d}.html"

def get_day(day):
    url = BASE_URL.format(day=day)

    r = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "H41-Podcast/1.0"}
    )
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # Quitamos elementos de navegación/código que no pertenecen al texto.
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text("\n", strip=True)

    # Limpieza básica
    text = re.sub(r"\n{3,}", "\n\n", text)

    return url, text


sources = []

for day in range(1, 5):
    url, text = get_day(day)

    print(f"DAY {day:03d}: {len(text)} caracteres")

    sources.append(
        f"""
========================
DAY {day:03d}
SOURCE: {url}
========================

{text}
"""
    )

source_text = "\n".join(sources)

# Guardamos lo que realmente leyó el sistema.
(EP / "source.txt").write_text(
    source_text,
    encoding="utf-8"
)

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

prompt = f"""
Eres el editor del podcast asociado a H41, una Human Observation Probe
que observa a la humanidad durante 365 días.

A continuación tienes sus CUATRO primeras observaciones.

Quiero que escribas una conversación en CASTELLANO entre dos hombres
que acaban de leerlas.

"""
PERSONAJES

JULIÁN:
52 años aproximadamente.
Reflexivo, escéptico y pausado.
Tiende a buscar límites en las conclusiones de H41.
Le incomodan las explicaciones demasiado bonitas sobre la humanidad.
Tiene experiencia suficiente para desconfiar de las generalizaciones.

DANI:
33 años aproximadamente.
Más rápido, intuitivo y provocador.
Se entusiasma con algunas conexiones de H41.
Pero tampoco está ahí para darle la razón a Julián.
Puede llevar una idea mucho más lejos de lo que Julián considera justificable.

DINÁMICA FUNDAMENTAL

ESTO ES UN DEBATE.

No escribas dos personas reafirmándose mutuamente.

Cada uno debe tener una interpretación propia de lo observado por H41.

Cuando uno formule una interpretación interesante, el otro debe
frecuentemente hacer al menos una de estas cosas:

- cuestionarla
- buscar una excepción
- llevarla a una consecuencia incómoda
- señalar una contradicción
- reinterpretarla
- decir directamente que no está de acuerdo
- cambiar el marco de la discusión

EVITAR especialmente esta estructura:

A: propone una idea.
B: "sí", la reformula.
A: "exacto", la amplía.
B: concluye.

Eso está PROHIBIDO.

No necesitan alcanzar consenso.

De hecho, algunas cuestiones deben quedar sin resolver.

H41 tampoco tiene razón por definición.
Pueden cuestionar su interpretación.
Pueden preguntarse si una inteligencia observadora está viendo algo
real o simplemente imponiendo patrones sobre los humanos.

Los cuatro días NO deben aparecer como cuatro bloques.

Una idea del DAY 004 puede contradecir algo del DAY 001.
Una observación del DAY 002 puede reaparecer mucho después.
Buscad tensiones ENTRE las observaciones.

TONO

Conversación inteligente pero cotidiana.
Nada de tertulia televisiva.
Nada de profesores explicando un texto.
Nada de frases diseñadas para parecer profundas.
Nada de moralejas.

Intervenciones generalmente cortas:
una o dos frases.

Ocasionalmente una intervención más larga cuando alguien desarrolla
un argumento.

Permitidas:
preguntas,
interrupciones naturales,
"no",
"espera",
"eso no lo veo",
"pero ahí estás suponiendo que...",
"¿por qué?",
"no necesariamente".

No abusar de ellas.

DURACIÓN

Entre 430 y 500 palabras.
Aproximadamente tres minutos.

FINAL

No resolver el debate.

La última intervención debe contener una idea completa y tener
una frase final que oralmente pueda cerrarse con claridad.

No terminar con:
"Dia cuatro",
"continuará",
"quedan 361 días",
ni ninguna fórmula de podcast.

FORMATO OBLIGATORIO

Sólo diálogo.

Julián:
Dani:

Sin títulos.
Sin markdown.
Sin instrucciones.
"""

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt,
)
dialogue = response.text.strip()

(EP / "script.txt").write_text(
    dialogue,
    encoding="utf-8"
)

print("\n--- SCRIPT ---\n")
print(dialogue)
