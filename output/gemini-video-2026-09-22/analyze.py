from pathlib import Path
import base64, json, re, urllib.request, urllib.error, sys, datetime

ROOT=Path('/Users/dmytropetrovskyi/projects/lada-health')
OUT=ROOT/'output/gemini-video-2026-09-22'
key=None
for line in (ROOT.parent/'book_trailer/.env').read_text().splitlines():
    m=re.match(r'^\s*(?:export\s+)?GOOGLE_API_KEY\s*=\s*(.*?)\s*$',line)
    if m:
        key=m.group(1).strip().strip('\"\'')
        break
if not key:
    print('Google API key not found.');sys.exit(1)
headers={'x-goog-api-key':key,'Content-Type':'application/json'}
base='https://generativelanguage.googleapis.com/v1beta/'
try:
    req=urllib.request.Request(base+'models',headers=headers)
    with urllib.request.urlopen(req,timeout=30) as r: models=json.load(r)
except Exception as e:
    print('Model discovery failed:',type(e).__name__);sys.exit(1)
available={m['name'].removeprefix('models/') for m in models.get('models',[]) if 'generateContent' in m.get('supportedGenerationMethods',[])}
choices=['gemini-3.1-pro-preview','gemini-3.8-flash','gemini-3.6-flash','gemini-2.5-pro']
model=next((m for m in choices if m in available),None)
if not model:
    print('No selected video-capable model found. Available Gemini names:', sorted(m for m in available if m.startswith('gemini-')));sys.exit(1)
prompt='''Analyze this approximately 28-second video INCLUDING ITS AUDIO. The user explicitly requests audiovisual description to help communicate observations about a current health concern. This is not a clinical examination or request for a definitive diagnosis.

First confirm whether the supplied audio is intelligible and whether you can actually use the audio stream. Do not invent speech based on lip movements. If unable to hear it, say so.
1. Provide a timestamped transcription of audible speech in its original language, distinguishing speakers. Mark uncertain or inaudible words explicitly. Then give a concise English translation.
2. Separately describe direct observations of articulation, speaking pace/pauses, sentence completion, audible breathing/cough/wheeze, visible alertness/eye closure, head and hand movements, facial movement and breathing effort. Use approximate timestamps. Distinguish normal blinking from sustained eye closure if possible. Do not infer a deficit simply because it was mentioned in context. No walking appears in the supplied clip; do not assess gait from camera movement. Do not diagnose dysarthria or ataxia from a short clip. Do not infer normal neurological function from smiling or conversation. Do not read unrelated computer-screen content.
3. Say whether the clip actually supplies clear evidence of slurred speech, inability to stay awake, or obvious respiratory distress, versus features not assessable. Do not conclude medical safety or rule out serious disease. Avoid describing speech as 'slow compared with usual' without a baseline.
4. Explain concisely what this clip can add and cannot establish about the partner's observations. Separate observation from hypothesis, acknowledge uncertainty, and avoid an extensive diagnostic list or repetitive emergency scripts.

Clinical context reported by partner (not established by video): asthma symptoms and poor sleep over two nights, nebulizer use; latest clarification Berodual 20-30 drops once and Pulmicort one 2 mL vial pictured as 0.5 mg/mL once, exact time window unknown. Fever 38.2 C on earlier thermometer photo, later 36.6 C after reported paracetamol (timing/dose unknown). Home SpO2 94%; same device showed partner 94-96%, accuracy unknown. Medrol reportedly as prescribed, last dose approximately 30 minutes before preceding message (exact dose unknown); Seretide yesterday. Partner says her thinking and speech seem slower and she was sometimes unsteady while walking. Similar episodes a couple of times in the last two weeks, including at ER; whether assessed and whether full recovery between episodes unknown. Patient wanted to go out; partner earlier described her as otherwise fine but tired. This video is confirmed recorded just now on September 22, 2026. Urgent in-person assessment has already been recommended; the user seeks specific evidence, not repeated generic advice. Do not assume additional sedatives, overdose, low glucose, low oxygen or elevated CO2 were demonstrated.

Respond in English except the original-language transcript. Keep claims anchored to what can actually be seen/heard. Aim for under 1000 words.'''
(OUT/'prompt.txt').write_text(prompt)
payload={'contents':[{'role':'user','parts':[{'inlineData':{'mimeType':'video/mp4','data':base64.b64encode((ROOT/'docs/2026-09-22-lada-video-original.mp4').read_bytes()).decode()}},{'text':prompt}]}], 'generationConfig':{'maxOutputTokens':10000,'temperature':0.2}}
(OUT/'request-metadata.json').write_text(json.dumps({'model':model,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'video':'docs/2026-09-22-lada-video-original.mp4','method':'generateContent inline MP4 with audio','prompt':'prompt.txt'},indent=2))
print('Analyzing original audiovisual clip with',model,flush=True)
req=urllib.request.Request(base+'models/'+model+':generateContent',data=json.dumps(payload).encode(),headers=headers,method='POST')
try:
    with urllib.request.urlopen(req,timeout=240) as r: response=json.load(r)
except urllib.error.HTTPError as e:
    try:
        obj=json.loads(e.read().decode());err=obj.get('error',{})
        safe={k:err.get(k) for k in ('code','status','message')}
        safe=json.dumps(safe).replace(key,'[REDACTED]')
        print(safe)
    except Exception: print('HTTP error',e.code)
    sys.exit(1)
except Exception as e:
    print('Request failed:',type(e).__name__);sys.exit(1)
(OUT/'response.json').write_text(json.dumps(response,ensure_ascii=False,indent=2))
texts=[]
for c in response.get('candidates',[]):
    for part in c.get('content',{}).get('parts',[]):
        if 'text' in part and not part.get('thought'):texts.append(part['text'])
result='\n\n'.join(texts)
(OUT/'analysis.md').write_text(result)
print(result)
print('\nFINISH:',[c.get('finishReason') for c in response.get('candidates',[])])
print('USAGE:',json.dumps(response.get('usageMetadata',{})))
