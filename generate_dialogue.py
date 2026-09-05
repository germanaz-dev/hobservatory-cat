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

PERSONAJES

JULIÁN:
- aproximadamente 50-55 años
- voz y pensamiento pausados
- reflexivo
- cómodo con los silencios
- no necesita terminar rápidamente una idea
- cierta experiencia vital
- puede ser escéptico, pero no cínico

DANI:
- aproximadamente 30-35 años
- más animado
- curioso
- pensamiento rápido
- encuentra conexiones inesperadas
- puede interrumpir ligeramente o lanzar preguntas
- nunca debe parecer un presentador de radio

ESTILO

Esto NO es un informativo.
NO es divulgación convencional.
NO quiero que enumeren DAY 001, DAY 002, DAY 003 y DAY 004.

Los cuatro textos deben convertirse en material para pensar.

Quiero que las ideas se crucen entre sí.
Que uno pueda recordar algo del primer día mientras hablan del cuarto.
Que haya preguntas que queden parcialmente abiertas.
Que discrepen ocasionalmente.
Que existan pequeñas pausas naturales.

No expliquéis qué es H41 más de lo necesario.
El oyente puede ir descubriéndolo.

No utilizar frases promocionales.
No terminar con moraleja.
No decir "en el episodio de hoy".
No pedir suscripciones.
No inventar hechos que no aparezcan en las fuentes.

DURACIÓN

Objetivo hablado: aproximadamente 3 minutos.

Escribe aproximadamente 400-450 palabras.

FORMATO OBLIGATORIO

Sólo diálogo.

Cada intervención debe comenzar exactamente con:

Julián:
Dani:

No añadas títulos, instrucciones, markdown ni comentarios.

FUENTES H41:

{source_text}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)
dialogue = response.text.strip()

(EP / "script.txt").write_text(
    dialogue,
    encoding="utf-8"
)

print("\n--- SCRIPT ---\n")
print(dialogue)
