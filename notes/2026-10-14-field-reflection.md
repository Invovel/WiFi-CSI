# 实测反馈与个人判断 / Field observations and my interpretation

整理日期 / Updated: 2026-10-14；采集日期 / Recording: 2026-10-13

**操作者已确认九组过程中改变过位置或朝向。这是一轮多因素探索，不能当成固定摆放下的大小动作对照；初始页面确认已由这条补充说明修正。**

**The operator confirmed position/orientation changes during the nine trials. This is a confounded exploratory recording, not a controlled small/large comparison; this clarification supersedes the initial checkbox interpretation.**

这份记录以操作者的现场反馈为依据；未标注时间段的观察不补造数值。九组页面采集的统计另见[初测图表](../reports/motion-pilot-2026-10-13/report.md)。它与下面的远近、正反和声音观察不是自动对应的同一组标签。

This note records the operator's field observations. No numerical values are invented for observations without timestamped labels. See the separate [pilot plots](../reports/motion-pilot-2026-10-13/report.md); those prompted trial labels do not automatically identify the near/far, orientation, or sound observations below.

## 我实际观察到的现象 / What I observed

| 对照 | 我的观察 | 证据边界 |
| --- | --- | --- |
| 靠近发射源端 / 靠近接收端 | 发射源附近引起的显示波动明显小于接收端附近 | 定性反馈，没有已对应的距离和重复次数；不能推为普遍距离规律 |
| 接收器正面 / 反面 | 正面响应明显高于反面 | 正反按本次实物摆放定义；没有角度标定，不能确定单一原因 |
| 声音及现场所称外界噪声 | 未看到明显影响 | 声源、声强、频率和噪声种类未量化；不代表对所有无线或机械干扰免疫 |

| Comparison | My observation | Evidence boundary |
| --- | --- | --- |
| Near transmitter / near receiver | Displayed fluctuations were smaller near the transmitter | Qualitative feedback; no mapped distance/repetition measurements; not a universal distance law |
| Receiver front / rear | Front-side response was stronger | Orientation refers to the physical setup; no angular calibration or isolated causal explanation |
| Sound and ambient noise tested | No clear effect was apparent | Sources, levels and frequency ranges were not quantified; this does not establish immunity to RF or mechanical interference |

“幅度”在这里指观察界面中的响应幅度，不是已经标定为毫米的物体位移。

Here, amplitude means the displayed response, not calibrated object displacement in millimetres.

## 我的判断 / My interpretation

我认为这项技术在观察运动或状态变化方面有一定可行性。但对当前单链路 ESP32-S3 装置而言，位置、朝向和动作造成的响应混在一起：较大波动未必就是较大动作，也可能与更敏感的位置或朝向有关。因此，我无法仅凭这套输出判断运动发生在发射端还是接收端，也尚不能可靠区分动作大小。

这使我更倾向于把当前项目定位为受控条件下的变化观察与学习，而不把它描述为可精确识别多种位置、动作和物体特征的系统。这是对本项目配置与证据的判断，不是对所有 CSI 系统的能力上限下结论。下一步的价值首先在于理解限制，而非继续扩展功能。

I see feasibility for observing motion or changes in state. In this single-link ESP32-S3 setup, however, position, orientation and action affect the response together. A larger response need not mean a larger movement; it may reflect a more sensitive location or orientation. These outputs do not let me reliably identify whether motion occurred near the transmitter or receiver, or reliably classify movement magnitude.

I therefore position this project as a learning exercise in observing changes under controlled conditions, rather than a system for precise multi-feature recognition. This is a judgment about this setup and its evidence, not a universal limit on CSI. Understanding the limitations is more valuable here than adding more features.

## 关于振动与损伤检测的设想 / Vibration-based damage hypothesis

我所说的损伤检测不是检测静止物体。我设想对物体施加可重复的小幅机械激励，观察不同部位的振动响应，并与健康状态比较，探索响应变化是否能提供损伤线索。这是主动激励下的动态检测设想，当前尚未验证。

更准确的信号链是：**可控激励 → 物体振动 → 随时间变化的 CSI 幅相 → 估计振动特征 → 与基准对照**。振动频率与振动幅度是不同量，知道频率不能直接推出幅度。Wi-Fi 子载波的频率也不是物体某个部位的振动频率，单条混合接收链路不能自动分离各部位。

已有研究演示了结合专门机械增强结构的 Wi-Fi 振动测量，说明这个方向可以作为研究设想，但不能作为本板已具备该能力的证据。[原始研究](https://www.nature.com/articles/s44172-024-00190-8)；CSI 描述信道的幅相等信息，参见[官方说明](https://docs.espressif.com/projects/esp-techpedia/en/latest/esp-friends/solution-introduction/esp-csi/esp-csi-solution.html)。

My damage-detection idea concerns a vibrating object, not a stationary inspection. I propose applying a repeatable small mechanical excitation, observing responses at different locations, and comparing them with a healthy reference to investigate possible damage indicators. This remains an untested hypothesis.

The intended chain is **controlled excitation → mechanical vibration → time-varying CSI amplitude/phase → estimated vibration features → reference comparison**. Vibration frequency and displacement amplitude are different quantities; frequency alone does not establish amplitude. Wi-Fi subcarrier frequencies are not the vibration frequencies of individual object parts, and one mixed receiving link does not automatically separate those parts.

Research has demonstrated Wi-Fi vibration sensing with a specialized mechanical enhancement structure. It supports investigating the idea, not claiming that this board already implements it. [Original research](https://www.nature.com/articles/s44172-024-00190-8); [official CSI overview](https://docs.espressif.com/projects/esp-techpedia/en/latest/esp-friends/solution-introduction/esp-csi/esp-csi-solution.html).

### 从设想到结论还缺什么 / What remains unproven

- 可重复的激励、固定支撑/装夹条件，以及健康与已知异常的对照；否则装夹和载荷变化也可能改变响应。
- 经独立参考测量标定的振动幅度、频率；当前 jitter 是派生诊断指标，不能直接换算位移。
- 足够且经过验证的原始 CSI 时间分辨率与信号处理；当前约 17 条/秒的诊断输出不是原始 CSI 采样率，也不能据此声称能分析目标振动频段。
- 不同部位的观测或分离办法，以及重复验证；当前实验没有损伤样本、参考位移或振动频谱。

- Repeatable excitation and mounting, plus healthy/known-abnormal references, to distinguish damage from load or support changes.
- Independent calibration of displacement and frequency; current jitter diagnostics are not displacement measurements.
- Verified raw CSI timing and processing suitable for the target vibration band; roughly 17 diagnostic reports/s is not the raw CSI acquisition rate.
- A method to observe or separate different parts and repeated validation. No damage samples, reference displacement, or vibration spectra were obtained here.

本项目暂不把上述设想扩展为已完成的损伤检测功能，也不因本轮声音影响不明显而否定机械振动检测的可能性。

This project does not claim a completed damage detector. The lack of an obvious response to the tested sounds also does not establish whether controlled mechanical vibration can be measured.
