from pathlib import Path
import json,base64,re,urllib.request,urllib.error,sys
root=Path('/Users/dmytropetrovskyi/projects/lada-health');out=root/'output/gemini-video-2026-09-22'
key=next(re.match(r'^\s*(?:export\s+)?GOOGLE_API_KEY\s*=\s*(.*?)\s*$',line).group(1).strip().strip('\"\'') for line in (root.parent/'book_trailer/.env').read_text().splitlines() if re.match(r'^\s*(?:export\s+)?GOOGLE_API_KEY\s*=',line))
model=json.loads((out/'request-metadata.json').read_text())['model']
prompt='''Transcribe this approximately 28-second audio recording verbatim in its original language with approximate timestamps. Do not paraphrase or correct grammar. Preserve hesitations and repetitions. Mark unclear words [unclear] and give alternatives only if supported by sound. Use no external context and do not infer medical diagnoses or judge safety. Then provide a short English translation. Specifically distinguish what is actually audible from guesses. No video is supplied for this transcription check.'''
(out/'audio-prompt.txt').write_text(prompt)
payload={'contents':[{'role':'user','parts':[{'inlineData':{'mimeType':'audio/wav','data':base64.b64encode((out/'audio.wav').read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':0.1,'maxOutputTokens':6000}}
req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/'+model+':generateContent',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','x-goog-api-key':key},method='POST')
print('Checking transcript from audio-only input.',flush=True)
try:
 with urllib.request.urlopen(req,timeout=180) as r:resp=json.load(r)
except urllib.error.HTTPError as e:
 try:print(e.read().decode().replace(key,'[REDACTED]'))
 except Exception:print('HTTP error',e.code)
 sys.exit(1)
except Exception as e:print(type(e).__name__);sys.exit(1)
(out/'audio-response.json').write_text(json.dumps(resp,ensure_ascii=False,indent=2))
text='\n\n'.join(p['text'] for c in resp.get('candidates',[]) for p in c.get('content',{}).get('parts',[]) if p.get('text') and not p.get('thought'))
(out/'audio-transcript.md').write_text(text)
print(text)
print('FINISH:',[c.get('finishReason') for c in resp.get('candidates',[])])
