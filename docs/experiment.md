# 简单实验 / Simple experiment

> 2026-10-14 状态更新：独立固件已部署；九组记录因位置/朝向在过程中变化，归为多因素探索。下文是原始计划或历史状态，受控重复实验及干扰开关矩阵未完成。最新事实见[实测反思](../notes/2026-10-14-field-reflection.md)和[部署记录](../notes/2026-10-14-deployment.md)。
> Update: standalone firmware deployed; the nine trials are confounded by position/orientation changes. The text below retains the original plan or historical status. Controlled repetitions and interference matrices are not completed. See the linked current records.

[中文首页](../README.md) · [English home](../README.en.md)

## 中文

**状态：计划，尚未执行。** 目的只是用少量对照支持技术理解。以下时长是建议的记录安排，不是经过验证的检测参数。

1. 固定收发器位置与朝向，记录距离、房间简图、设备和软件版本、流量产生方式。
2. 先检查数据能否持续接收，写明记录的是原始 CSI 还是上层诊断。时间戳、记录数与缺失情况分别保存。
3. 记录 60 秒静止条件作为基线，注明风扇、门窗等背景状态。
4. 保持设备不动，让人或物体在收发器连线附近移动约 20 秒，随后静止约 40 秒；独立记下运动起止时间，重复三次。
5. 在连线侧方再做同样的对照，观察空间影响是否超出直线路径。
6. 比较静止、运动及恢复阶段，保留不明显或相反的结果。用[模板](../notes/observation-template.md)写一次短复盘。

若数据本身不连续，本轮结论就是采集条件不足。若只有上层状态日志，就只讨论该状态与运动时间的对应，不宣称已经分析原始幅相。第一轮不要求复杂模型或准确率；若以后报告比例，需先定义标签、判定规则、样本单位与计数。

完成标准：能画出收发关系，展示实际记录，并用自己的话解释“观察到了什么、哪些原因仍不能排除”。当前没有实验曲线或实测结论可展示。

## English

**Status: planned, not performed.** The aim is a small set of comparisons that supports understanding. The durations below are suggested recording intervals, not validated detector parameters.

1. Fix device positions and orientations. Record distance, a room sketch, hardware and software versions, and how traffic is generated.
2. Check data continuity and identify whether the output is raw CSI or application-level diagnostics. Keep timestamps, record counts, and gaps separate.
3. Record a 60-second stationary baseline and note background conditions such as fans, doors, and windows.
4. Without moving the devices, move a person or object near the line between them for about 20 seconds, then stop for about 40 seconds. Independently mark motion start and end times and repeat three times.
5. Repeat to the side of the line to examine whether the observed influence extends beyond the direct path.
6. Compare stationary, moving, and recovery periods, retaining weak or unexpected results. Write a short reflection using the [template](../notes/observation-template.md).

If data is discontinuous, the conclusion is that acquisition conditions were insufficient. With application-level logs alone, discuss their timing relative to motion without claiming raw amplitude or phase analysis. No complex model or accuracy score is required initially. Any future reported rate needs defined labels, decision rules, sample units, and counts.

Completion means being able to draw the setup, show actual records, and explain what was observed and which alternative causes remain. There are currently no experimental plots or measured conclusions to present.
