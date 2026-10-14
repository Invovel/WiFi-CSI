# 拆分来源与状态 / Origin and status

> 2026-10-14 状态更新：独立固件已部署；九组记录因位置/朝向在过程中变化，归为多因素探索。下文是原始计划或历史状态，受控重复实验及干扰开关矩阵未完成。最新事实见[实测反思](../notes/2026-10-14-field-reflection.md)和[部署记录](../notes/2026-10-14-deployment.md)。
> Update: standalone firmware deployed; the nine trials are confounded by position/orientation changes. The text below retains the original plan or historical status. Controlled repetitions and interference matrices are not completed. See the linked current records.

[中文首页](../README.md) · [English home](../README.en.md)

## 中文

本库于 2026-10-13 从原嵌入式学习资料中的 CSI 主题拆分，重新定位为个人技术学习与见解展示。原路线为“路由器回应 → CSI 感知端 → UART → 摄像头识别”；本库收缩为“发射器 → 空间 → 接收与观察”。

本次阅读的本地材料来自 `embedded-learning-lab`：`docs/04-vision-csi.md`、`projects/csi-vision-reference/README.md` 和 `sources/evidence/csi-deployment.md`。原库本地 HEAD 为 `3c2c9080413839ac4cd90e59c4665adb6d1e2879`；存在其他未提交工作，本次没有将其一并搬入新库。

历史公开来源入口：[embedded-learning-lab](https://github.com/Invovel/embedded-learning-lab)。[部署记录的历史版本](https://github.com/Invovel/embedded-learning-lab/blob/3c2c9080413839ac4cd90e59c4665adb6d1e2879/sources/evidence/csi-deployment.md)对应本地所查的仓库基线；远端可用性以 GitHub 实际内容为准。

| 内容 | 状态 |
| --- | --- |
| 双语介绍、个人理解、框架、实验模板 | 本库已整理 |
| 路由器连接、CSI 基础采样、Fake 入口 | 旧记录报告通过，本次未复测 |
| 新框架下的静止/运动对照 | 未执行 |
| 可靠运动检测、类别识别、位置判断 | 未验证或不在本库目标中 |
| 新固件、模型或实测数据 | 本库未提供 |

没有搬入私有网络配置、设备标识、Flash 镜像、聊天原文或旧依赖。旧工程、历史证据及设备固件未修改。本库文字中的第一人称见解是学习表达初稿，不代表尚未进行的实验已经产生个人实测体验。

## English

On 2026-10-13, the CSI topic was separated from the embedded learning material and reframed around personal understanding. The former router reply → CSI sensing node → UART → camera recognition workflow is reduced here to transmitter → space → reception and observation.

The local source materials were `docs/04-vision-csi.md`, `projects/csi-vision-reference/README.md`, and `sources/evidence/csi-deployment.md` in `embedded-learning-lab`. Its local HEAD was `3c2c9080413839ac4cd90e59c4665adb6d1e2879`; unrelated uncommitted work was not imported.

Public source entry: [embedded-learning-lab](https://github.com/Invovel/embedded-learning-lab). The [historical deployment record](https://github.com/Invovel/embedded-learning-lab/blob/3c2c9080413839ac4cd90e59c4665adb6d1e2879/sources/evidence/csi-deployment.md) uses the inspected local repository baseline; remote availability depends on the content actually hosted by GitHub.

| Item | Status |
| --- | --- |
| Bilingual introduction, perspective, framework, experiment template | Prepared in this repository |
| Router connection, basic CSI sampling, Fake entry point | Reported in old records; not retested here |
| Stationary/moving comparisons for the new framework | Not performed |
| Reliable motion detection, identity, position | Unverified or outside scope |
| New firmware, models, or measured data | Not provided here |

Private network configuration, device identifiers, flash images, raw conversations, and old dependencies were not imported. Historical projects, evidence, and device firmware remain unchanged. First-person reflections are an initial learning narrative, not claims of hands-on experience from experiments that have not occurred.
