# COM4 实机检查 / Live board inspection

日期 / Date: 2026-10-13

## 中文

结论：当前固件可作为 CSI 接收与变化观察的学习起点，但尚不满足已经验证的独立运动判断演示。

本次通过 115200 串口读取约 18 秒，发送只读查询 `HMSCMD HELLO` 和 `HMSCMD GET_RUNTIME`。未烧录、未重置基线、未修改检测参数；采集期间没有看到重启标记。现场运动未标注，因此 ACTIVE 不能作为真实运动或误报的判定依据。

查询返回 `target=esp32s3`、`peers=[AP]`、`stream_period_ms=50`、`amplitude_log_enabled=true`。运行日志包含 `wifi_sensing_demo` 与 `phase1_link`，表明旧 CSI/Vision 事件链仍在运行。查询接口未给出应用版本或镜像 SHA；本次没有读取 Flash，因此不能证明当前镜像与历史部署哈希完全一致。

| 实测项目 | 结果 |
| --- | --- |
| 完整 sample 消息 | 310 条，设备时间跨度 17.961 秒 |
| 上层诊断输出速率 | 约 17.2 条/秒，不是原始 CSI 回调速率 |
| 初始化状态 | 310 条均为 STABLE |
| 状态分布 | IDLE 286；DEBOUNCE_ACTIVE 7；ACTIVE 17 |
| jitter_value 范围 | 0.000672–0.336877 |
| Vision 等待导致的事件丢弃 | 4 次 |
| train_thresholds_valid | 全部 false；训练计数为 0 |
| 配置 | sensitivity 0.5；presence_sensitivity 0.25；active_jitter_min 0.01；active_filter_ms 300 |

不足与下一步：

1. 仍等待摄像头结果，独立学习版应将运动观察输出与 Vision 回执逻辑分离。事件被丢弃时，sample 输出仍持续，不等于 CSI 采集中断。
2. 训练阈值未有效，尚无带动作标签的静止/运动对照；需要记录已知动作和背景条件。无训练阈值并不表示整个自适应运动算法未运行。
3. 当前识别的是 AP 链路；历史源码通过 Ping 请求促使路由器发包。可用路由器作为发射端，但不能称为完全不发射的被动接收器。本次未独立测量无线发包。
4. 单链路状态不支持证明物体位于收发器之间的直线上，更不支持类别或位置识别。
5. 缺少固件版本/哈希查询，复现时还需补全旧工程依赖或建立最小采集工程。

原始记录仅本地保存在被 Git 忽略的 `data/raw/com4-inspection-2026-10-13.log`，其中可能包含设备标识。统计文件为同目录 `.summary.json`。本记录不包含设备标识。

项目已迁移到 `D:\PythonProject\CSI`，保留原有 `.vscode`；Git 的 `main` 跟踪 `origin/main`，远端为 `Invovel/WiFi-CSI`。历史源码和硬件固件未修改。

## English

The running firmware is a usable starting point for learning CSI reception and observing changes, but it is not yet a validated standalone motion demonstration.

An approximately 18-second serial capture at 115200 baud included read-only `HELLO` and `GET_RUNTIME` queries. No firmware was flashed, no baseline was reset, and no detector settings were changed. No reboot markers were observed. Physical movement was not annotated, so ACTIVE states cannot establish true detections or false alarms.

The replies identify an `esp32s3` target with the AP peer, a configured 50 ms reporting interval, and amplitude logging enabled. `wifi_sensing_demo` and `phase1_link` logs show the earlier CSI/Vision event workflow remains active. The protocol does not report an application version or image hash; Flash was not read, so exact identity with the historical image is unconfirmed.

There were 310 complete sample messages over 17.961 seconds of device time, about 17.2 diagnostic records per second, not a raw CSI sampling rate. All reported STABLE initialization. States were IDLE 286, DEBOUNCE_ACTIVE 7, and ACTIVE 17. Jitter ranged from 0.000672 to 0.336877. Four events were dropped while awaiting Vision results. Training thresholds were invalid throughout and training counts were zero.

The next steps are to separate observation output from camera acknowledgements, record labeled stationary/moving comparisons, and make firmware identity and dependencies reproducible. Samples continued during dropped events. Invalid training thresholds do not mean the adaptive motion algorithm was inactive. The AP-based design can use a router as the transmitter, but historical source uses Ping requests and is not receive-only radio operation. No over-the-air traffic measurement was performed here. Single-link changes do not establish object position or identity.

Raw logs and summary statistics are retained only in Git-ignored `data/raw/`. The local repository is now `D:\PythonProject\CSI`, with `main` tracking `origin/main` in `Invovel/WiFi-CSI`; existing `.vscode` files were retained. Historical source and device firmware were not modified.
