# 独立 CSI 部署与对照实验流程 / Standalone CSI deployment and comparison plan

> 2026-10-14 状态更新：独立固件已部署；九组记录因位置/朝向在过程中变化，归为多因素探索。下文是原始计划或历史状态，受控重复实验及干扰开关矩阵未完成。最新事实见[实测反思](../notes/2026-10-14-field-reflection.md)和[部署记录](../notes/2026-10-14-deployment.md)。
> Update: standalone firmware deployed; the nine trials are confounded by position/orientation changes. The text below retains the original plan or historical status. Controlled repetitions and interference matrices are not completed. See the linked current records.

日期 / Date: 2026-10-13

状态：流程计划已制定；以下固件改造、重新烧录和带动作标签的实验尚未执行。

Status: plan prepared; firmware adaptation, reflashing, and labeled experiments below are not yet performed.

## 1. 目标与现有证据 / Objective and evidence

目标是判断：在固定摆放和约定动作下，大幅与小幅运动是否产生可重复区分的连续指标，而不只是都输出 ACTIVE；同时观察 10/20/30 秒记录和环境干扰对结论的影响。不预设一定能够分类，不追求新算法研究。

现有串口测试证明 COM4 持续输出诊断，且仍运行等待 Vision 回包的逻辑。旧数据没有现场动作标签，只能用于接收检查，不能作为大小动作的训练或验证集。`jitter_value` 是固件派生指标，不是物体位移、速度或原始 CSI 幅度。

本地项目：`D:\PythonProject\CSI`，远端 `Invovel/WiFi-CSI`，分支 main。2026-10-13 核对旧完整工程位于 `D:\Documents\Codex\2026-09-23\d-esp32\work\csi-sense-phase1-source`，包含 components、managed_components 和 dependencies.lock。历史构建描述指向 ESP-IDF v6.0（v6.0-dirty）；工具路径混有 v6.1 目录，因此路径名不能代替版本核验。旧构建成功不等于新工程可复现。

## 2. 固件准备与部署 / Firmware preparation and deployment

1. 在新库建立独立 firmware 工程，从完整旧工程选取必要代码与组件，保留来源及许可证。冻结实际 IDF 版本、工具版本、依赖锁定文件和组件修改；不直接复制旧 build 缓存。私有 Wi-Fi 配置、镜像和设备标识仅本地保留。
2. 移除 phase1_link 初始化、UART Vision 发送与等待、Fake 事件交接及相关依赖。保留 AP 采集、Ping 促发、运动状态机、诊断输出和配置查询。首版保持感知算法及参数不变，避免把算法变化与解除摄像头依赖混淆。
3. 输出至少包含设备时间、递增记录序号、peer、jitter、平滑值、进入/退出阈值、状态及初始化状态。HELLO 加入固件版本、构建标识及可获得的应用摘要。记录输出序号只衡量诊断记录完整性，不宣称原始 CSI 无丢样。
4. 先编译并保存构建记录。上板前重新确认 COM 设备身份、芯片、Flash 与分区表；备份当前应用及必要恢复信息并校验备份。不要直接套用历史 0x20000 偏移；以当前设备分区和本次构建为准。
5. 按核实后的分区烧录兼容应用并校验，保留网络配置；无需例行擦除整片 Flash。若构建、身份、分区或备份任一项不成立，先解决再刷写。
6. 启动后查询版本，并跑 10/20/30 秒接收冒烟检查：记录持续到达、时间递增、无重启/崩溃、无 Vision 等待或事件丢弃。短测通过只代表进入实验的条件具备。

产物：可构建工程、版本与依赖记录、本地备份、烧录校验及冒烟检查记录。失败时用已核实备份恢复；恢复成功也需检查版本与接收状态。

## 3. 实验准备 / Setup

- 路由器作为发射来源，固定接收板、路由器、天线朝向和工作信道；记录距离、位置草图、固件及参数。电脑只采集和记录，不在组间改变算法或阈值。
- 先记录至少 60 秒静止背景。若初始化未稳定、持续断流或时间异常，则延长检查并排障，不把无数据解释为静止。记录自适应基线行为；即使参数不变，内部阈值也可能随时间变化。
- 小/大幅运动主实验用同一人、同一位置、同一身体部位、相同节奏，例如前臂约 10 cm 与约 40 cm 往复摆动。固定周期会使幅度与速度关联，结论仅适用于这两种约定动作，不声称测得纯粹的幅度效应。
- 全身走动可以另做演示，但不与挥手直接合并解释为单一幅度差异。两者位置、反射面积和运动方式都不同。
- 每轮采集前倒计时，操作者按提示开始/结束动作。保存实际动作标记；错过提示、旁人进入或动作变化时标记该轮偏离并重做。计划时间不能冒充实际动作标签。

## 4. 实验矩阵 / Experiment matrix

### A：动作与时长

静止、小幅、大幅 × 10/20/30 秒 × 各 3 次，共 27 轮，正式观察窗口合计 9 分钟。每轮额外记录 5 秒前背景和至少 5 秒后背景；若尚未恢复稳定则延长等待并记录。初始基线、休息和重做时间另计。

提前生成并保存随机顺序，在各轮间交错条件，避免先全部静止、再全部小幅、最后全部大幅造成时间漂移混淆。27 轮是学习性探索，不是足以证明普遍准确率的数据规模。

### B：背景干扰与时长

保持人和目标静止，选择一种可控干扰。优先单独测试同一 AP 下另一设备固定流量任务的关闭/开启；也可另开一组测试风扇关闭/开启，但不能同时改变无线流量与机械运动。

关闭/开启 × 10/20/30 秒 × 各 3 次，共 18 轮，正式窗口合计 6 分钟，前后背景另计。记录实际干扰启停与流量条件；不要用发送端断流代替噪声实验。若没有可控干扰源，明确记为未测，不根据自然波动猜测噪声来源。

该组先判断静止条件下的干扰影响。若要声明“有干扰时仍能区分大小动作”，必须额外在干扰开启条件下重复 A；本计划基础两组不支持此声明。

“噪声”在此指无线或环境扰动，并非麦克风声音强度。如另测音乐，需记录扬声器振动与人员活动，不能将所有变化归因于声压。

## 5. 数据与图表 / Data and figures

每次实验保留 session_id、trial_id、动作标签、正式窗口时长、重复编号、干扰条件、设备/主机时间、实际动作标记、配置与连续指标。原始记录保持不变，清洗后数据和排除理由另存；截取窗口边缘的半条串口消息不直接计为固件丢包。

最终至少交付以下四项，配中英文解释：

1. 静止/小幅/大幅的同尺度时间曲线，叠加实际动作区间、状态和动态阈值，展示每轮而不只选最好的一轮。
2. 每轮 jitter 的中位数、P95、离散程度，以及三类分布重叠。以实验轮次为重复单位，不把高度相关的数百条记录当成数百次独立实验。
3. 10/20/30 秒的单位时间误触发次数、静止 ACTIVE 时间占比、响应/恢复延迟；未触发时保留“未触发”，不将其当作零延迟。用相邻时间戳估计状态持续时间并标明缺失区段。
4. 干扰开/关的分布及基线随时间变化；报告窗口越长峰值越可能变大的统计影响，不只比较最大值或累计触发数。

原始诊断采样与到达间隔可作为数据质量附表，但不能成为主结论。数据中断轮次报告为无效/数据不足；异常值不能因为不符合预期而删除。

## 6. 结论规则 / Decision rules

- 重复各轮差异方向一致、分布重叠较少：称为“当前布置下存在区分潜力”，尚非可靠分类器。
- 平均值有差异但重叠明显或轮间反转：称为“有趋势，无法稳定区分”。
- 没有可重复差异：称为“当前配置只能观察活动变化，未证实可区分大小动作”。

若进一步需要输出自动 small/large 标签，再用独立追加的实验轮次做验证；开发规则与测试轮次分离，报告按轮次的混淆矩阵与失败情形。不在同一批数据上调阈值后宣称准确。此分类扩展不是学习流程的前置要求。

## 7. 完成与协作 / Completion and coordination

计划阶段完成条件：来源工程可定位、固件改动与安全部署步骤明确、实验条件/时长/重复/标签有定义、图表与结论规则齐全。本文件完成该阶段，不表示部署或实验已完成。

执行阶段完成条件：独立固件构建并核验上板；A 与 B 完整执行且有真实标签；输出全部对比图、数据质量说明及支持程度匹配的结论。若干扰实验或动作配合未完成，必须标记未完成。

助手负责准备工程、采集和分析工具、构建/部署检查、图表及双语报告。用户负责布置设备、执行动作、确认实际动作时间与干扰条件。正式实验前协调一个连续可配合的时间段；不擅自把无人配合的串口读取当成已标注实验。

## English workflow

The question is whether defined small and large movements produce repeatably different continuous diagnostics, even when both yield ACTIVE. Compare recording durations and controlled interference separately. Do not assume a classifier will succeed. Previous unlabelled captures demonstrate reception only.

**Firmware:** derive a standalone project from the complete historical source, preserve licenses and lock actual tools/components, remove Vision UART handoff and Fake handoff, and retain the AP/Ping sensing algorithm and settings initially. Add reproducible firmware identification and record sequence numbers alongside timestamps, jitter, thresholds and states. Diagnostic sequence numbers do not prove raw CSI completeness. Verify device identity and actual partitions, back up and validate the existing application, then flash and verify a compatible application without routine full-chip erasure. Repeat 10/20/30-second reception checks, requiring no resets or Vision waits. Historical build metadata points to IDF v6.0-dirty; verify the real environment rather than infer it from directory names.

**Setup:** fix router/receiver placement and configuration, record at least 60 seconds of stationary baseline, and wait for stable acquisition. Use the same person, position, body part and cadence for approximately 10 cm versus 40 cm forearm movements. Fixed cadence couples amplitude and speed, so conclusions concern these defined actions, not an isolated displacement effect. Walking is a separate demonstration. Keep actual motion annotations and flag deviations; scheduled prompts alone are not ground truth.

**A:** stationary/small/large × 10/20/30 seconds × three repetitions = 27 trials and nine minutes of formal windows. Add five seconds of background before and at least five seconds after each trial, extending recovery as needed. Save a randomized interleaved order. This is exploratory evidence, not a general accuracy benchmark.

**B:** with people/target stationary, controlled interference off/on × 10/20/30 seconds × three repetitions = 18 trials and six minutes of formal windows, plus background. Change only one factor, such as a defined traffic task on another device connected to the AP. Fan motion is a separate experiment. Mark this stage untested if no controllable source is available. These stationary comparisons do not establish small/large discrimination under interference; that would require repeating A under interference.

**Analysis:** retain raw data, session/trial identifiers, conditions, versions, actual labels and timing. Show all trials with common plot scales, motion intervals and thresholds. Compare trial-level medians, P95, dispersion and distribution overlap; correlated samples are not independent repetitions. Report false events per unit time, stationary ACTIVE time fraction, response/recovery latency, missing data and baseline drift. A longer window can contain a larger maximum simply by offering more opportunities. Do not drop unexpected results. Serial boundary fragments are not automatically firmware packet loss.

**Conclusions:** distinguish repeatable separation potential, overlapping trends, and no reproducible distinction. A reliable automatic small/large classifier requires extra held-out trials, a frozen rule and trial-level error reporting. It is not necessary to build such a classifier to answer the learning question honestly.

**Deliverables:** reproducible standalone firmware with deployment checks; labelled A/B trials; time-series and distribution plots; duration/interference comparisons; bilingual interpretation with limitations. The assistant prepares acquisition and analysis; the user performs and labels physical actions and interference changes. Planning is complete when these steps and gates are specified; execution is complete only when evidence exists for them. No experiment is claimed completed by this plan.
