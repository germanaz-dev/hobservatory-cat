import os
import wave
from pathlib import Path

from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash-preview-tts"
VOICE_A = "Gacrux"
VOICE_B = "Sulafat"

ROOT = Path(__file__).parent
SCRIPT_PATH = ROOT / "episodes/001/script.txt"
OUT_PATH = ROOT / "episodes/001/episode.wav"

def save_wav(filename, pcm, channels=1, rate=24000, sample_width=2):
    filename.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(filename), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY")

    transcript = SCRIPT_PATH.read_text(encoding="utf-8")

    prompt = f"""
Interpreta aquesta conversa en català entre Laia i Marc.

Escena: dues persones acaben de llegir el primer informe publicat per H41,
una sonda artificial que observarà la humanitat durant 365 dies.
No són locutors de ràdio. Parlen amb naturalitat, curiositat i una lleugera
incomoditat intel·lectual. Ritme tranquil. Petites pauses naturals.
No facis una veu promocional ni exagerada.

Laia: càlida, reflexiva, curiosa.
Marc: contingut, analític, lleugerament escèptic.

Transcripció:
{transcript}
"""

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker="Laia",
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=VOICE_A
                                )
                            ),
                        ),
                        types.SpeakerVoiceConfig(
                            speaker="Marc",
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=VOICE_B
                                )
                            ),
                        ),
                    ]
                )
            ),
        ),
    )

    pcm = response.candidates[0].content.parts[0].inline_data.data
    save_wav(OUT_PATH, pcm)
    print(f"Creat: {OUT_PATH}")

if __name__ == "__main__":
    main()
