import os
import wave
from pathlib import Path

from google import genai
from google.genai import types

types.SpeakerVoiceConfig(
    speaker="Julián",
    voice_config=types.VoiceConfig(
        prebuilt_voice_config=types.PrebuiltVoiceConfig(
            voice_name="Algenib"
        )
    ),
),

types.SpeakerVoiceConfig(
    speaker="Dani",
    voice_config=types.VoiceConfig(
        prebuilt_voice_config=types.PrebuiltVoiceConfig(
            voice_name="Orus"
        )
    ),
),

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

PERFIL DE AUDIO

Julián es un HOMBRE de unos 52 años.
Voz masculina madura, grave, algo áspera.
Habla despacio y con seguridad.
Piensa mientras habla.
A veces deja una pequeña pausa antes de responder.
No es solemne ni radiofónico.
Cuando discrepa, no eleva necesariamente la voz: se vuelve más preciso.

Dani es un HOMBRE de unos 33 años.
Voz inequívocamente masculina, adulta y más joven que Julián.
Más energía y velocidad.
Más reactivo, inquisitivo y espontáneo.
Puede mostrar incredulidad, ironía o entusiasmo.
No es alegre por defecto y NO suena como presentador.

ESCENA

Dos hombres están sentados hablando después de haber leído cuatro
observaciones extrañas sobre la humanidad.

están grabando un programa de radio.
Están discutiendo.

A veces uno piensa que el otro está equivocado.
Una pregunta puede incomodar.
Una respuesta puede ser seca.
Puede haber pequeñas risas, dudas, respiraciones y pausas.
No sobreactuar. Ritmo suave pero que no duerma al oyente. 

DIRECCIÓN

No leer los nombres de los personajes.

No mantener una entonación uniforme.
Las preguntas deben sonar realmente como preguntas.
Las objeciones deben sonar como objeciones.
Las frases sorprendentes pueden tener énfasis.
Las frases reflexivas pueden desacelerarse.

MUY IMPORTANTE:
la última intervención NO debe sonar como una frase cortada ni como
texto que simplemente se termina.
Debe tener una cadencia final clara, natural y deliberada.
La última palabra debe recibir la entonación necesaria para cerrar
la conversación.

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
