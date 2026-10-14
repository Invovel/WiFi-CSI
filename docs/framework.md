# 收发框架 / System framework

> 2026-10-14 状态更新：独立固件已部署；九组记录因位置/朝向在过程中变化，归为多因素探索。下文是原始计划或历史状态，受控重复实验及干扰开关矩阵未完成。最新事实见[实测反思](../notes/2026-10-14-field-reflection.md)和[部署记录](../notes/2026-10-14-deployment.md)。
> Update: standalone firmware deployed; the nine trials are confounded by position/orientation changes. The text below retains the original plan or historical status. Controlled repetitions and interference matrices are not completed. See the linked current records.

[中文首页](../README.md) · [English home](../README.en.md)

## 中文

首轮拟采用已有学习背景较熟悉的链路：**路由器作为回应帧发射端 → 空间传播 → ESP32-S3 接收并采集 CSI → 电脑记录**。ESP32 发 Ping 是促发流量的辅助动作。发射器始终是框架的一部分。

另一种后续可选布置是独立 ESP32 发射器加 ESP32 接收器，参考官方 `csi_send` / `csi_recv`。本库尚未选定该方案的版本、配置与硬件，也未实现切换。

学习时分别观察数据是否持续到达、静止基线是否稳定、运动时是否出现变化，以及恢复静止后是否回到相似水平。没有可用数据时应记为“数据不足”，不能记为“无运动”。

拟议输出只有三类：没有明显运动相关变化、候选运动相关变化、数据不足。这是记录用语，尚未实现为分类器；“没有明显变化”不等于“空间里没有物体”。

本库不复制旧 CSI/Vision 固件作为新实现。旧接收工程带有摄像头事件交接与依赖，直接改名会造成误解。将来若补采集代码，应单独说明来源、依赖和实际验证范围。

## English

The proposed first setup follows the familiar historical arrangement: **router transmitting reply frames → propagation through space → ESP32-S3 receiving and collecting CSI → computer recording observations**. Ping requests from the ESP32 help generate traffic. A transmitter remains an explicit part of the framework.

A dedicated ESP32 transmitter and ESP32 receiver are a possible later arrangement, using the official `csi_send` / `csi_recv` examples as references. Versions, configuration, and hardware for that arrangement have not been selected or implemented here.

The observations will cover data continuity, the stationary baseline, changes during movement, and recovery after movement stops. Missing usable data must be recorded as “insufficient data,” not “no motion.”

The proposed vocabulary is: no clear motion-related change, candidate motion-related change, and insufficient data. These are reporting terms, not an implemented classifier. No clear change does not mean no object is present.

The old CSI/Vision firmware is not copied as a new implementation. It includes camera event handoff and additional dependencies. Any future acquisition code should document its origin, dependencies, and actual validation scope separately.
