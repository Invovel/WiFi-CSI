# 我的技术理解 / My perspective

[中文首页](../README.md) · [English home](../README.en.md)

## 中文

### 我为什么学习 CSI

我感兴趣的是：一个原本用于通信的系统，为什么还能帮助我们感知环境？把发射、传播和接收连起来看，让我更容易理解无线通信与环境之间的联系。这也是本仓库想表达的核心见解。

### 我如何理解“检测运动”

我的理解分成三步：接收到数据；观察到数据变化；通过对照实验判断变化是否与运动有关。这三步不能合并成“收到 CSI 就能检测物体”。丢包、设备摆放或背景环境变化，都需要在解释中考虑。

因此，我会先使用“观察到与运动一致的变化”这样的表述。只有当重复实验提供支持时，才描述特定条件下的候选运动判断。物体类别、精确位置以及完全静止的物体是否存在，不是这个简单实验能直接回答的问题。

### 我为什么以接收端为中心

发射器提供流量，接收端是我理解数据的入口。我想讲清楚数据从哪里来、如何记录、如何比较，以及什么情况下不应该下结论。这样的范围让我能够把技术讲明白，也为以后看更复杂的系统建立基础。

### 我怎样表达自己的见解

每篇记录都区分：我原先的理解、实际观察、我对现象的解释、尚未回答的问题。出现不符合预期的结果也值得保留。对我来说，能够说明为什么暂时不能下结论，也是学习成果。

这些是根据本项目学习定位整理的初稿；具体实验感受需在实际操作后补充。

## English

### Why I am learning CSI

What interests me is how a system designed for communication can also help us sense its surroundings. Looking at transmission, propagation, and reception together helps me understand the relationship between wireless communication and the environment. This is the central perspective I want to present.

### How I understand motion detection

I separate three steps: receiving data, observing a change, and using controlled comparisons to assess whether the change is related to motion. Receiving CSI alone does not establish object detection. Packet loss, device placement, and background changes need consideration when interpreting the observations.

I would initially describe a result as “a change consistent with motion.” A candidate motion decision under specific conditions needs support from repeated experiments. Object identity, precise position, and the presence of a completely stationary object are beyond what this simple experiment can directly establish.

### Why I focus on the receiver

The transmitter supplies traffic, while the receiver is my entry point for understanding the data. I want to explain where the data comes from, how I record and compare it, and when a conclusion is premature. This scope gives me a foundation for understanding more complex systems later.

### How I express my perspective

Each note separates my initial understanding, actual observations, interpretation, and remaining questions. Unexpected results also deserve a place in the record. Being able to explain why a conclusion is not yet justified is part of learning.

This is an initial draft based on the project's learning focus; reflections on hands-on work will be added after experiments.
