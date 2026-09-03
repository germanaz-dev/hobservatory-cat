import os,wave
from pathlib import Path
from google import genai
from google.genai import types
EP=Path(__file__).parent/"episodes/001"
text=(EP/"script.txt").read_text()
client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
prompt=f"""Interpreta aquesta conversa en català. No són locutors: natural, reflexiva, amb petites pauses.
Laia és càlida i curiosa. Marc és contingut, analític i lleugerament escèptic.
Transcripció:
{text}"""
r=client.models.generate_content(model="gemini-2.5-flash-preview-tts",contents=prompt,config=types.GenerateContentConfig(response_modalities=["AUDIO"],speech_config=types.SpeechConfig(multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(speaker_voice_configs=[
types.SpeakerVoiceConfig(speaker="Laia",voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Gacrux"))),
types.SpeakerVoiceConfig(speaker="Marc",voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Sulafat")))]))))
pcm=r.candidates[0].content.parts[0].inline_data.data
with wave.open(str(EP/"voice.wav"),"wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
