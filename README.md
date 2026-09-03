# H41 Podcast — Procedural MVP

DAY 001 — Unfinished Architects

Pipeline: `script.txt` → Gemini TTS → `voice.wav`; `music.json` → sintetizador Python → `music.wav`; ffmpeg → `episode.mp3`.

La música de DAY 001 es procedural: 58 BPM, drone abierto, baja densidad y pulsos escasos. No usa música externa ni una API musical.

En este MVP `music.json` está definido manualmente. La siguiente versión podrá generarlo con Gemini a partir de cada observación de H41.

Añade `GEMINI_API_KEY` como GitHub Actions secret y ejecuta **Generate H41 episode 001**.
