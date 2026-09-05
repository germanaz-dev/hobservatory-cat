import os
import wave
from pathlib import Path

from google import genai
from google.genai import types

ROOT = Path(__file__).parent
EP = ROOT / "episodes/001"

transcript = (EP / "script.txt").read_text(
    encoding="utf-8"
)

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

prompt = f"""
Interpreta esta conversación en castellano de España.

Son dos hombres conversando después de haber leído las primeras
observaciones de H41.

Julián:
hombre de unos 50-55 años.
Voz madura.
Habla despacio.
Pausas naturales.
Reflexivo.
Nunca suena como locutor.
No dramatiza.

Dani:
hombre de unos 30-35 años.
Más vivo y espontáneo.
Habla algo más rápido.
Curioso.
Puede reaccionar con sorpresa o ironía ligera.
Tampoco es locutor.

La conversación debe sentirse cercana y real.
Deja respirar algunas frases.
No leas los nombres de los personajes.

Transcripción:

{transcript}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=
            types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[

                    types.SpeakerVoiceConfig(
                        speaker="Julián",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=
                            types.PrebuiltVoiceConfig(
                                voice_name="Gacrux"
                            )
                        ),
                    ),

                    types.SpeakerVoiceConfig(
                        speaker="Dani",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=
                            types.PrebuiltVoiceConfig(
                                voice_name="Puck"
                            )
                        ),
                    ),
                ]
            )
        ),
    ),
)

pcm = (
    response
    .candidates[0]
    .content.parts[0]
    .inline_data.data
)

with wave.open(str(EP / "voice.wav"), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(24000)
    w.writeframes(pcm)

print("Creado voice.wav")
