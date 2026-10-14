import argparse, collections, datetime, json, pathlib, time
import serial

p = argparse.ArgumentParser()
p.add_argument('--port', default='COM4')
p.add_argument('--output', required=True)
p.add_argument('--durations', nargs='+', type=int, default=[10,20,30])
args=p.parse_args()
out=pathlib.Path(args.output);out.mkdir(parents=True,exist_ok=True)
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
ser=serial.Serial(port=None,baudrate=115200,timeout=0.05)
ser.dtr=False;ser.rts=False;ser.port=args.port;ser.open()
results=[]
try:
 for seconds in args.durations:
  ser.reset_input_buffer();ser.write(b'HMSCMD HELLO\n')
  raw=bytearray();start=time.monotonic()
  while time.monotonic()-start<seconds: raw.extend(ser.read(ser.in_waiting or 1))
  text=raw.decode('utf-8',errors='replace');(out/f'{stamp}-{seconds}s.log').write_text(text,encoding='utf-8')
  rows=[]
  for line in text.splitlines():
   if 'HMS:{' in line:
    try: rows.append(json.loads(line[line.index('HMS:')+4:]))
    except ValueError: pass
  samples=[r for r in rows if r.get('type')=='sample'];seq=[r['seq'] for r in samples if 'seq' in r]
  res={'seconds':seconds,'samples':len(samples),'firmware':[r for r in rows if r.get('type')=='firmware'],'sequence_gaps':sum(max(0,b-a-1) for a,b in zip(seq,seq[1:])),'sequence_present':len(seq)==len(samples) and len(samples)>0,'states':dict(collections.Counter(r.get('state_name') for r in samples)),'vision_pending':text.count('Vision result pending'),'crash_markers':sum(text.count(v) for v in ['ESP-ROM:','rst:','Guru Meditation','assert failed'])}
  results.append(res);print(json.dumps(res),flush=True)
finally: ser.close()
(out/f'{stamp}-summary.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('SUMMARY='+str(out/f'{stamp}-summary.json'),flush=True)
