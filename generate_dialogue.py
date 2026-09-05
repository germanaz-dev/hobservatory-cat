import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from google import genai


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

ROOT = Path(__file__).parent
EP = ROOT / "episodes" / "001"
EP.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://germanaz-dev.github.io/sonda-h41/day-{day:03d}.html"


# --------------------------------------------------
# DOWNLOAD H41 DAYS
# --------------------------------------------------

def get_day(day: int):
    url = BASE_URL.format(day=day)

    response = requests.get(
        url,
        timeout=30,
        headers={
            "User-Agent": "H41-Podcast/1.0"
        },
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove page elements that are not part of the observation.
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text("\n", strip=True)

    # Basic cleanup.
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


# Keep an exact record of what the podcast generator read.
(EP / "source.txt").write_text(
    source_text,
    encoding="utf-8",
)


# --------------------------------------------------
# GENERATE DIALOGUE
# --------------------------------------------------

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


prompt = f"""
Eres el editor del podcast asociado a H41, una Human Observation Probe
que observa a la humanidad durante 365 días.

A continuación tienes sus CUATRO primeras observaciones.

Tu trabajo es convertirlas en un resumen y analisis en CASTELLANO

No debe resumir simplemente los textos. utiliza herramientas como (pausa) (suspiro) (tos) (gruñido)
Debe reflexionar sobre la pregunta que se hace la sonda y sus conclusiones en base a lo observado

PERSONAJES (uno presenta al otro y pregunta que ha esta semana, el otro expone y al final, el primero saluda hasta la proxima semana 

JULIÁN:

Hombre de aproximadamente 52 años.

Reflexivo, escéptico y pausado.
Tiende a buscar límites en las conclusiones de H41.
Le incomodan las explicaciones demasiado bonitas sobre la humanidad.
Tiene experiencia suficiente para desconfiar de las generalizaciones.

No necesita responder inmediatamente.
Puede dejar una idea sin cerrar.
Puede reconocer que no sabe algo.

DANI:

Hombre de aproximadamente 33 años.

Más rápido, intuitivo y provocador.
Se entusiasma con algunas conexiones de H41.
Tiende a llevar una idea más lejos.
Puede plantear consecuencias que Julián considera exageradas.

No está ahí para darle la razón a Julián.

DINÁMICA FUNDAMENTAL



No escribas reafirmándo la conclusion de h41.

Cada uno debe desarrollar una interpretación propia de lo observado
por H41.

esta permitido:

- cuestionarla
- buscar una excepción
- llevarla a una consecuencia incómoda
- señalar una contradicción
- reinterpretarla
- decir directamente que no está de acuerdo
- cambiar el marco de la discusión


No deben necesitar alcanzar consenso.

Algunas cuestiones deben quedar sin resolver.

Puede cambiar de opinión durante la lectura, pero solamente
cuando exista una razón para hacerlo.

H41 TAMPOCO TIENE RAZÓN POR DEFINICIÓN.

Pueden preguntarse si una inteligencia observadora está descubriendo
algo real sobre los humanos o simplemente imponiendo patrones sobre
lo que observa.

RELACIÓN ENTRE LOS CUATRO DÍAS

Los cuatro días NO deben aparecer como cuatro bloques.

No quiero:

"En el primer día..."
"En el segundo día..."
"En el tercer día..."

Las observaciones deben relacionarse

Una idea del DAY 004 puede contradecir algo del DAY 001.

Una observación del DAY 002 puede reaparecer mucho después.

Una idea del DAY 003 puede modificar la interpretación de otra
observación.

Busca especialmente tensiones, contradicciones y conexiones ENTRE
las cuatro observaciones.

No es necesario mencionar explícitamente el número del día.

FIDELIDAD

No inventes hechos históricos, científicos o acontecimientos que no
estén contenidos en las fuentes.

Sí puedes formular hipótesis, interpretaciones y preguntas a partir
de ellas como lo haria un humano.

Cuando una idea sea especulativa debe sonar como una interpretación
del personaje, no como un hecho establecido.

TONO

inteligente pero cotidiana.

Nada de tertulia televisiva.

Nada de profesores explicando un texto.

Nada de dos expertos intentando demostrar que son inteligentes.

Nada de frases artificialmente diseñadas para parecer profundas.

Nada de moralejas.

Nada de lenguaje promocional.

Nada de:

"bienvenidos"
"en el episodio de hoy"
"nuestros oyentes"
"este fascinante tema"

Comienza con "H41 ya lleva 4 dias observandonos..."

DURACIÓN

Escribe entre 430 y 500 palabras.

FINAL

No resolver el debate.

No terminar con una moraleja.

No terminar con:

"DAY 004"
"día cuatro"
"continuará"
"quedan 361 días"

La última intervención debe contener una idea completa.

MUY IMPORTANTE:

La última frase debe estar escrita para ser pronunciada con una
cadencia final clara.

No debe parecer que falta otra frase después.

La última palabra debe permitir una caída natural de entonación y
un cierre oral inequívoco.

FORMATO OBLIGATORIO

Devuelve ÚNICAMENTE el diálogo.

Cada intervención debe comenzar exactamente con uno de estos nombres:

Julián:
Dani:

No añadas título.

No añadas markdown.

No añadas notas.

No añadas instrucciones de interpretación.

No añadas texto antes o después del diálogo.

Ten en cuenta que puede ser usado en un TTS de GEMINI


FUENTES H41

{source_text}
"""


response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt,
)


dialogue = response.text.strip()


# --------------------------------------------------
# BASIC VALIDATION
# --------------------------------------------------

if not dialogue:
    raise RuntimeError("Gemini devolvió un diálogo vacío.")

if "Julián:" not in dialogue:
    raise RuntimeError("El diálogo no contiene intervenciones de Julián.")

if "Dani:" not in dialogue:
    raise RuntimeError("El diálogo no contiene intervenciones de Dani.")


# --------------------------------------------------
# SAVE
# --------------------------------------------------

(EP / "script.txt").write_text(
    dialogue,
    encoding="utf-8",
)


word_count = len(dialogue.split())

print()
print("--------------------------------")
print(f"Diálogo generado: {word_count} palabras")
print("--------------------------------")
print()
print(dialogue)
