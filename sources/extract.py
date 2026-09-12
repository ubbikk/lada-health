import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
x=json.loads(Path('sources/stream-0.json').read_text())
def dec(i):
 if i<0:return None
 v=x[i]
 if isinstance(v,dict): return {x[int(k[1:])]:dec(n) for k,n in v.items()}
 if isinstance(v,list):return [dec(n) for n in v]
 return v
nodes=dec(86)
Path('sources/conversation.json').write_text(json.dumps(nodes,ensure_ascii=False,indent=2))
msgs=[]
for n in nodes:
 m=n.get('message') or {}; role=(m.get('author') or {}).get('role'); c=m.get('content') or {}
 if role not in ['user','assistant'] or c.get('content_type') not in ['text','multimodal_text']: continue
 if m.get('channel') not in [None,'final']:continue
 parts=c.get('parts',[]); txt='\n'.join(p if isinstance(p,str) else '[Attachment: '+str(p.get('content_type','unknown'))+']' for p in parts)
 if not txt.strip():continue
 ts=m.get('create_time'); date=datetime.fromtimestamp(ts,ZoneInfo('Europe/Kyiv')).isoformat() if ts else 'undated'
 msgs.append({'id':m.get('id'),'role':role,'date':date,'text':txt,'content':c})
Path('sources/messages.json').write_text(json.dumps(msgs,ensure_ascii=False,indent=2))
for roles,name in [(['user','assistant'],'transcript.md'),(['user'],'user-messages.md')]:
 out=['# Shared conversation archive\n\nSource: https://chatgpt.com/share/6a9dc4fb-8bc8-83eb-a19d-86653e944874\n\nMessage dates use Europe/Kyiv. Attachments are placeholders; original image contents are not transcribed. Assistant responses are historical AI output, not verified medical advice.\n']
 for j,m in enumerate(msgs,1):
  m['ref']=f'M{j:03}'
  if m['role'] in roles:out.append(f"## {m['ref']} — {m['role']} — {m['date']}\n\n{m['text']}\n")
 Path('sources/'+name).write_text('\n'.join(out))
Path('sources/messages.json').write_text(json.dumps(msgs,ensure_ascii=False,indent=2))
print('nodes',len(nodes),'messages',len(msgs),'user',sum(m['role']=='user' for m in msgs))
