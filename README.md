# H41 Podcast — MVP

Primer experiment d'àudio derivat de la publicació de H41.

Source:
https://germanaz-dev.github.io/sonda-h41/

## Què fa

Genera `episodes/001/episode.wav` i `episodes/001/episode.mp3` amb dues veus en català utilitzant
`gemini-2.5-flash-preview-tts`.

## Execució local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="..."
python generate.py
```

## GitHub Actions

1. Crea un repo nou, per exemple `h41-podcast`.
2. Puja aquests fitxers.
3. Ves a **Settings → Secrets and variables → Actions**.
4. Crea el secret `GEMINI_API_KEY`.
5. Ves a **Actions → Generate episode 001 → Run workflow**.
6. Descarrega l'artefacte `h41-podcast-episode-001`. A dins hi trobaràs `episode.wav` i `episode.mp3`.

Aquest MVP encara no llegeix automàticament la web de H41: el guió de DAY 001
és a `episodes/001/script.txt`.
