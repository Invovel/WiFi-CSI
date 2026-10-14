# 独立接收固件 / Standalone receiver firmware

版本 `standalone-0.1.0` 已在 COM4 ESP32-S3 编译、烧录并通过接收检查。移除 phase1_link 摄像头交接，保留 AP/Ping 感知算法与参数；增加诊断 seq 和 firmware 身份消息。seq 是诊断消息序号，不是原始 CSI 包序号。

Version `standalone-0.1.0` was built, flashed and checked on COM4 ESP32-S3. Camera handoff was removed; AP/Ping sensing and settings were retained. Added diagnostic sequence numbers and firmware identity messages. Sequence numbers do not represent raw CSI packets.

## 复现边界 / Reproducibility boundary

本次使用本机 ESP-IDF v6.0-dirty 和旧完整工程中的本地组件。公开目录提供应用源码；components、managed_components、私有 sdkconfig、凭据和完整镜像未上传。仅克隆本库不能直接重现本次构建；main/idf_component.yml 也不是完整依赖锁定。本机组件哈希记录保存在 .local/source-component-hashes.json。复现前需要核对具体组件版本及修改、私有网络配置和设备分区。

This build used local ESP-IDF v6.0-dirty and components from the complete historical project. The public tree contains application sources, not local components, private configuration, credentials or full flash images. A fresh clone is not sufficient to reproduce the build; the component manifest is not a complete lock. Local component hashes are retained privately. Component versions/modifications, network configuration and actual partitions must be resolved before reproducing it.

本机构建脚本为 tools/build_csi.ps1，路径依赖当前电脑，不自动烧录。不可直接沿用历史端口或应用偏移到其他设备。

tools/build_csi.ps1 records the local build environment and does not flash automatically. Do not reuse port numbers or partition offsets on another device without verification.

源码保留原 SPDX 声明；参考上游 [Espressif ESP-CSI](https://github.com/espressif/esp-csi)。
Existing SPDX notices are preserved. Upstream: Espressif ESP-CSI.
