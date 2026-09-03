import json,wave,os
from pathlib import Path
import numpy as np
EP=Path(__file__).parent/"episodes/001"; c=json.loads((EP/"music.json").read_text())
duration=float(os.environ.get("AUDIO_DURATION","90"))+1; sr=44100; n=int(duration*sr); t=np.arange(n)/sr
rng=np.random.default_rng(c["seed"]); audio=np.zeros(n)
for i,(r,a) in enumerate(zip(c["intervals"],[.15,.085,.045])):
 f=c["root_hz"]*r; breath=.72+.28*np.sin(2*np.pi*c["movement"]*(i+1)*t+i*1.7)
 audio+=a*breath*(np.sin(2*np.pi*f*t)+c["brightness"]*.22*np.sin(2*np.pi*2*f*t+.4))
pulse=np.zeros(n); beat=60/c["bpm"]
for bt in np.arange(0,duration,beat*2):
 if rng.random()>c["density"]+.45: continue
 s=int(bt*sr); L=min(int(.32*sr),n-s)
 if L>0:
  x=np.arange(L)/sr; pulse[s:s+L]+=c["pulse"]*np.exp(-x*11)*np.sin(2*np.pi*(c["root_hz"]/2)*x)
raw=rng.normal(0,1,n); k=np.ones(1200)/1200; noise=np.convolve(raw,k,mode="same"); noise/=max(np.max(np.abs(noise)),1e-9)
audio+=pulse+c["noise"]*noise
fn=int(min(4,duration/5)*sr); fade=np.ones(n); fade[:fn]=np.linspace(0,1,fn); fade[-fn:]=np.linspace(1,0,fn); audio*=fade
audio=audio/max(np.max(np.abs(audio)),1e-9)*.72; pcm=(audio*32767).astype(np.int16)
with wave.open(str(EP/"music.wav"),"wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
