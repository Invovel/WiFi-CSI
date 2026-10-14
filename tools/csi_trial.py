"""Local, user-started CSI comparison. Conditions are prompted, then user-confirmed."""
import collections, datetime, json, pathlib, threading, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import serial

ROOT=pathlib.Path(r'D:\PythonProject\CSI\data\raw')
ROOT.mkdir(parents=True,exist_ok=True)
OUT=ROOT/('motion-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
OUT.mkdir()
lock=threading.Lock()
state={'phase':'ready','label':'准备就绪','remaining':0,'trial':0,'total':9,'running':False,'finished':False,'confirmed':None,'samples':0,'latest':None,'error':None,'output':str(OUT)}
trials=[(10,'stationary'),(10,'small'),(10,'large'),(20,'large'),(20,'stationary'),(20,'small'),(30,'small'),(30,'large'),(30,'stationary')]
names={'stationary':'保持静止','small':'小幅摆臂：约 10 cm','large':'大幅摆臂：约 40 cm'}
rows=[];events=[]
def update(**values):
 with lock: state.update(values)
def run():
 ser=serial.Serial(port=None,baudrate=115200,timeout=0.05);ser.dtr=False;ser.rts=False;ser.port='COM4'
 pending=bytearray()
 try:
  ser.open();ser.reset_input_buffer();ser.write(b'HMSCMD HELLO\n')
  with (OUT/'serial.log').open('wb') as raw:
   def stage(phase,label,duration,trial,condition):
    start=time.monotonic();end=start+duration
    events.append({'phase':phase,'condition':condition,'trial':trial,'host_start':start,'duration':duration})
    update(phase=phase,label=label,trial=trial)
    while time.monotonic()<end:
     update(remaining=max(0,round(end-time.monotonic(),1)))
     block=ser.read(ser.in_waiting or 1);raw.write(block);pending.extend(block)
     while b'\n' in pending:
      line,_,rest=pending.partition(b'\n');pending[:]=rest
      pos=line.find(b'HMS:{')
      if pos<0: continue
      try: r=json.loads(line[pos+4:])
      except ValueError: continue
      if r.get('type')=='sample':
       r.pop('mac',None);r.update(host_time=time.monotonic(),phase=phase,condition=condition,trial=trial)
       rows.append(r);update(samples=len(rows),latest=r)
   stage('baseline','保持静止，记录初始背景',15,0,'stationary')
   for i,(duration,condition) in enumerate(trials,1):
    stage('prepare','准备：'+names[condition],5,i,condition)
    stage('record',names[condition],duration,i,condition)
   stage('recovery','结束动作，保持静止',5,9,'stationary')
  (OUT/'samples.json').write_text(json.dumps(rows),encoding='utf-8')
  (OUT/'events.json').write_text(json.dumps(events,indent=2),encoding='utf-8')
  update(finished=True,phase='done',label='采集完成，请确认是否按提示完成动作',remaining=0)
  print('CAPTURE_COMPLETE '+str(OUT),flush=True)
 except Exception as e:
  update(error=str(e),phase='error',label='采集失败',finished=True)
  print('CAPTURE_ERROR '+str(e),flush=True)
 finally:
  if ser.is_open: ser.close()
  update(running=False)

HTML='''<!doctype html><meta charset="utf-8"><title>CSI 动作对比</title><style>body{font:20px system-ui;background:#101827;color:#eff4ff;max-width:880px;margin:40px auto;padding:20px}h1{font-size:32px}#label{font-size:38px;color:#67e8f9}#count{font-size:64px}button{padding:15px 24px;margin:8px;font-size:20px;cursor:pointer}small{color:#b8c6da}canvas{width:100%;height:160px;background:#18253b}</style><h1>WiFi-CSI：静止 / 小幅 / 大幅运动</h1><p>站在固定位置，用同一只前臂、相同节奏，分别做约 10 cm 与 40 cm 往复摆动。不要挪动板子。只有蓝色提示开始记录后才做动作。</p><p>九组正式记录共 3 分钟，加准备与背景约 4 分钟。每组依次为 10、20、30 秒；画面会告诉你具体动作。</p><button id="start" onclick="start()">我已就位，开始</button><div id="label">准备就绪</div><div id="count">—</div><div id="progress"></div><canvas id="chart" width="850" height="160"></canvas><small>曲线是 jitter 派生指标；不等于物理位移。准备阶段会提示下一动作。</small><div id="confirm" hidden><p>刚才是否全程按提示动作、且没有其他人走动？未确认的数据不会当作真实标签。</p><button onclick="confirmRun(true)">是，已按提示完成</button><button onclick="confirmRun(false)">有偏差，需要说明或重测</button></div><div id="error"></div><script>
let ctx,previous='',values=[];const canvas=document.querySelector('#chart'),g=canvas.getContext('2d');
function beep(){if(!ctx)return;let o=ctx.createOscillator(),a=ctx.createGain();a.gain.value=.15;o.connect(a);a.connect(ctx.destination);o.frequency.value=660;o.start();o.stop(ctx.currentTime+.2)}
async function start(){ctx=new AudioContext();await ctx.resume();await fetch('/start',{method:'POST'});document.querySelector('#start').disabled=true}
async function confirmRun(ok){await fetch('/confirm',{method:'POST',body:JSON.stringify({confirmed:ok})});document.querySelector('#confirm').innerHTML=ok?'已确认，正在等待分析。':'已记录偏差；请在聊天中说明发生在哪一组。'}
setInterval(async()=>{let s=await(await fetch('/state')).json();document.querySelector('#label').textContent=s.label;document.querySelector('#count').textContent=s.remaining?s.remaining.toFixed(1)+' s':'—';document.querySelector('#progress').textContent=`第 ${s.trial} / ${s.total} 组 · 记录 ${s.samples} 条`;document.querySelector('#error').textContent=s.error||'';document.querySelector('#start').disabled=s.running||s.finished;document.querySelector('#confirm').hidden=!s.finished||s.confirmed!==null||!!s.error;if(s.phase+':'+s.trial!==previous){if(s.phase==='record')beep();previous=s.phase+':'+s.trial}if(s.latest){values.push(s.latest.jitter_value);if(values.length>300)values.shift();g.clearRect(0,0,850,160);let max=Math.max(.05,...values);g.strokeStyle='#67e8f9';g.beginPath();values.forEach((v,i)=>{let x=i*850/300,y=150-v/max*140;i?g.lineTo(x,y):g.moveTo(x,y)});g.stroke();}},250);
</script>'''
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*a): pass
 def do_GET(self):
  if self.path=='/state':
   with lock: data=json.dumps(state,ensure_ascii=False).encode()
   ctype='application/json; charset=utf-8'
  else: data=HTML.encode();ctype='text/html; charset=utf-8'
  self.send_response(200);self.send_header('Content-Type',ctype);self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
 def do_POST(self):
  if self.headers.get('Origin') not in (None,'http://127.0.0.1:8765','http://localhost:8765'):
   self.send_error(403);return
  if self.path=='/start':
   with lock:
    if state['running'] or state['finished']: self.send_error(409);return
    state['running']=True
   threading.Thread(target=run,daemon=True).start()
  elif self.path=='/confirm':
   data=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))))
   if not state['finished'] or not isinstance(data.get('confirmed'),bool): self.send_error(400);return
   (OUT/'user-confirmation.json').write_text(json.dumps(data),encoding='utf-8');update(confirmed=data['confirmed'])
  else: self.send_error(404);return
  self.send_response(200);self.end_headers();self.wfile.write(b'OK')
print('READY http://127.0.0.1:8765 '+str(OUT),flush=True)
ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
