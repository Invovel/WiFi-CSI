# 我的探索与技术见解 / My exploration and technical perspective

[中文首页](../README.md) · [English home](../README.en.md)

## 从什么问题开始

我最初想知道：在一个有发射源和接收器的空间中，物体运动会怎样反映到接收数据里？进一步说，大幅运动与小幅运动能不能有可辨别的差异？我不满足于“收到多少条数据”的报告，因为它只能说明链路在工作，不能说明这些数据意味着什么。

我把 CSI 从摄像头联动项目中拆出，用独立的 ESP32-S3 接收固件观察连续数据。10、20、30 秒窗口给了我观察变化的机会，随后我在实际操作中改变了位置、接收器方向，并尝试声音和外界噪声。

## 哪些观察影响了我的判断

靠近发射源时，波动明显小于靠近接收器时；在接收器正面，响应明显超过反面。声音及本次尝试的外界噪声则几乎没有明显影响。

这些现象对我的意义在于：显示值不仅取决于动作本身。位置和方向会影响结果，所以一个更大的波动无法直接告诉我“动作更大了”。同样，我看到了远近位置的响应差异，但这不等于我能在未知位置时，反过来从一段信号准确判断它来自哪一端。

我还区分了两种说法：“本次没有看到声音影响”，与“外界干扰不会影响 CSI”。前者是我的观察，后者超出了这次测试能说明的范围。

## 我目前仍保持的基本判断

我认为这项技术有一定可行性，适合继续考虑在条件明确的对象或场景中观察运动、振动及状态变化。但面对影响因素很多的空间，当前装置还不足以详细、准确地同时分辨位置、动作大小和其他多种特征。

我对它的兴趣更多地落在“能否观察到状态变化”上，而不是把波动包装成一个全面、精确的识别结果。这也是我选择把项目作为技术学习和个人见解记录的原因。

## 为什么这轮是探索，而不是分类验证

我在九组采集过程中改变过位置或朝向。因此，这次尝试发现了值得关注的现象，却没有隔离动作幅度、位置、方向和观察时长的作用。

这既不能证明大小动作已经可以稳定分类，也不能证明 CSI 在所有配置下都无法分类。它支持我对当前装置的谨慎判断：不能把这些因素混在一起后，再只根据输出大小解释物理动作。[曲线与记录](../reports/motion-pilot-2026-10-13/report.md)保留页面提示，并明确它们不是受控标签。

## 从运动观察延伸出的振动设想

我的损伤检测设想是动态的：先让物体产生小幅、可重复的振动，再观察不同部位的响应，尝试与健康状态比较，寻找异常变化。

我想了解的是物体的振动特征，而不是只看接收到的 Wi-Fi 频率。频率与幅度要分别测量、标定；不同部位的响应也需要办法区分。现有系统还没有做到这些，所以我把它作为可能的应用方向保留，而不是本项目的已验证成果。[详细设想与依据](../notes/2026-10-14-field-reflection.md)。

## English

### The question I started with

I wanted to understand how movement in a space containing a transmitter and receiver appears in received data, and whether large and small movements produce distinguishable responses. A count of received records was not enough: it establishes a working link, but does not explain what the data means.

I separated CSI from the camera workflow and used standalone ESP32-S3 firmware to observe continuous data. The 10-, 20- and 30-second windows gave me opportunities to observe changes. During the trials, I also changed location and receiver orientation and tried sound and ambient noise.

### Observations that shaped my judgment

Responses near the transmitter were noticeably smaller than those near the receiver, and the front of the receiver produced a stronger response than the rear. Sound and the ambient noise I tried had little obvious effect.

What matters to me is that the displayed value does not depend on the action alone. A larger fluctuation does not directly establish a larger movement. Observing different responses at known near/far positions is also different from being able to infer an unknown position from a signal.

I distinguish “no obvious effect from the sounds I tried” from “environmental interference does not affect CSI.” Only the first describes my observation.

### My current position

I see some feasibility for observing motion, vibration or changes of state in defined objects and settings. In a space with many interacting factors, however, this setup does not establish detailed, accurate identification of position, movement magnitude and multiple other characteristics at once.

My interest is in whether a change can be observed, rather than presenting fluctuations as comprehensive recognition. This is why I keep the project focused on learning and personal interpretation.

### Exploration rather than classification validation

I changed position or orientation during the nine trials. The exploration revealed useful observations but did not isolate movement magnitude, location, direction or observation duration.

It neither proves stable small/large classification nor establishes that every CSI configuration is incapable of it. It supports a cautious interpretation of this setup: mixed influences cannot be reduced to a direct physical-action label. The [recorded plots](../reports/motion-pilot-2026-10-13/report.md) preserve interface prompts while identifying them as uncontrolled labels.

### A vibration idea arising from the exploration

My damage-detection idea is dynamic: induce a repeatable small vibration, observe responses at different parts of the object and compare with a healthy reference to look for abnormal changes.

The target is mechanical vibration characteristics, not simply received Wi-Fi frequencies. Frequency and amplitude need separate measurement and calibration, and responses from different parts must be distinguishable. This system has not demonstrated those steps, so the idea remains a possible application rather than an achieved result. See the [detailed hypothesis and references](../notes/2026-10-14-field-reflection.md).
