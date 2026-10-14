"""Plot a labeled pilot without treating serial samples as independent trials."""
import argparse, json, pathlib, sys, statistics

p=argparse.ArgumentParser();p.add_argument('session');p.add_argument('--output',required=True);args=p.parse_args()
session=pathlib.Path(args.session);output=pathlib.Path(args.output);output.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(pathlib.Path(r'D:\PythonProject\CSI\.local\plot-deps')))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

rows=json.loads((session/'samples.json').read_text(encoding='utf-8'))
events=json.loads((session/'events.json').read_text(encoding='utf-8'))
confirmation=session/'user-confirmation.json'
confirmed=json.loads(confirmation.read_text()).get('confirmed') if confirmation.exists() else None
deviation=session/'protocol-deviation.json'
confounded=deviation.exists()
labels=('stationary','small','large');colors={'stationary':'#64748b','small':'#0284c7','large':'#e87924'}
stats=[]
fig,axes=plt.subplots(3,3,figsize=(13,9),sharey=True)
for ev in [e for e in events if e['phase']=='record']:
 r=[v for v in rows if v['trial']==ev['trial'] and v['phase']=='record']
 if len(r)<2: raise ValueError(f'Insufficient data in trial {ev["trial"]}')
 t=np.array([v['ts_ms'] for v in r],dtype=float)/1000;t-=t[0]
 j=np.array([v['jitter_value'] for v in r]);dt=np.diff(t);valid=(dt>0)&(dt<=.25)
 active=np.array([v.get('motion_status',False) for v in r]);elapsed=float(dt[valid].sum())
 ratio=float(dt[valid & active[:-1]].sum()/elapsed) if elapsed else None
 gaps=sum(max(0,b['seq']-a['seq']-1) for a,b in zip(r,r[1:]))
 # All statistics are descriptive at trial level, not independent per-sample inference.
 summary={'trial':ev['trial'],'condition':ev['condition'],'duration_s':ev['duration'],'samples':len(r),'median_jitter':float(np.median(j)),'p95_jitter':float(np.percentile(j,95)),'iqr_jitter':float(np.percentile(j,75)-np.percentile(j,25)),'active_fraction':ratio,'sequence_gaps':gaps,'max_gap_ms':float(dt.max()*1000),'invalid_gap_count':int((~valid).sum())}
 stats.append(summary)
 ax=axes[(10,20,30).index(ev['duration']),labels.index(ev['condition'])]
 ax.plot(t,j,color=colors[ev['condition']],lw=.9)
 ax.set_title(f'Trial {ev["trial"]} | {ev["duration"]} s | prompt: {ev["condition"]}')
 ax.set_xlabel('Device time within trial (s)');ax.set_ylabel('jitter_value (derived metric)');ax.grid(alpha=.2)
 ax.set_xlim(0,ev['duration'])
fig.suptitle('CSI exploratory recording — position/orientation changed\nTrial labels are prompts, NOT controlled movement conditions' if confounded else 'CSI movement pilot — one trial per condition and duration\nLabels: '+('user confirmed' if confirmed is True else 'UNCONFIRMED prompts'),fontsize=14)
fig.tight_layout(rect=(0,0,1,.93));fig.savefig(output/'time-series.png',dpi=170);fig.savefig(output/'time-series.svg');plt.close(fig)
fig,axes=plt.subplots(1,3,figsize=(13,4),sharey=True)
for ax,duration in zip(axes,(10,20,30)):
 data=[]
 for cond in labels:
  trial=next(s['trial'] for s in stats if s['condition']==cond and s['duration_s']==duration)
  data.append([v['jitter_value'] for v in rows if v['phase']=='record' and v['trial']==trial])
 ax.boxplot(data,tick_labels=['prompt: '+v for v in labels],showfliers=True);ax.set_title(f'{duration} s');ax.grid(axis='y',alpha=.2)
axes[0].set_ylabel('jitter_value');fig.suptitle('Exploratory distributions: position/orientation confounded; labels are prompts' if confounded else 'Within-trial distributions (samples are temporally correlated)');fig.tight_layout();fig.savefig(output/'distributions.png',dpi=170);fig.savefig(output/'distributions.svg');plt.close(fig)
for s in stats:
 s['prompt_condition']=s.pop('condition')
(output/'trial-statistics.json').write_text(json.dumps({'initial_checkbox_confirmation':confirmed,'controlled_labels_valid':confirmed is True and not confounded,'position_orientation_confounded':confounded,'trials':stats},indent=2),encoding='utf-8')
lines=['# 多因素探索记录 / Exploratory recording','',f'初始页面确认 / Initial checkbox confirmation: {confirmed}','',
'**操作者随后确认：九组过程中改变了位置或朝向。原先页面确认不能证明受控标签有效。下表与图中动作名仅为页面提示，不能用来推断大小动作、位置、朝向或时长的独立影响。**' if confounded else '',
'**The operator subsequently reported position/orientation changes within the nine trials. The original checkbox does not establish controlled labels. Condition names are prompts only; no isolated movement, location, orientation or duration effect can be inferred.**' if confounded else '',
'本轮每种动作×时长只有一次，属于初测，不能证明稳定区分能力或准确率。记录的是 jitter 派生指标，不是位移。',
'One trial per condition/duration: descriptive pilot only, not a repeatability or accuracy claim. Jitter is a derived diagnostic, not displacement.','',
'![时间曲线 / Time series](time-series.png)','', '![分布 / Distributions](distributions.png)','',
'|页面提示 / Prompt only|时长 s|中位数 / Median|P95|ACTIVE 时间占比|序号缺口|', '|---|---:|---:|---:|---:|---:|']
for s in sorted(stats,key=lambda s:(s['duration_s'],labels.index(s['prompt_condition']))):
 lines.append(f'|{s["prompt_condition"]}|{s["duration_s"]}|{s["median_jitter"]:.6f}|{s["p95_jitter"]:.6f}|{s["active_fraction"]:.1%}|{s["sequence_gaps"]}|')
lines+=['','## 解释边界 / Interpretation limits','',
'- 若动作标签未确认，以上只按提示时段分组，不解释为真实动作差异。 / Unconfirmed prompts are not ground truth.',
'- 原计划要求相同部位和节奏，但本轮存在位置/朝向变化，不能隔离动作大小效应。 / Speed, direction and adaptive baseline remain potential influences.',
'- ACTIVE 时间占比按有效的相邻设备时间间隔加权；超过 250 ms 或非正间隔不计入分母，缺口在统计文件中单列。 / ACTIVE time fraction excludes invalid timing gaps.',
'- 本轮没有受控干扰开关，不能据此归因外界噪声；也不能把较长窗口的更高峰值单独解释为噪声增加。 / No controlled interference comparison was performed.',
'- 稳定区分需要重复实验；自动分类需要独立验证轮次。 / Repeatability needs repeated trials; classification needs held-out validation.','']
(output/'report.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'labels_confirmed':confirmed,'trials':stats},indent=2))
