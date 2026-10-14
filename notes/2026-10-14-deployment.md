# 独立固件部署记录 / Standalone deployment

整理 2026-10-14；部署及检查 2026-10-13。Updated October 14; deployment/checks October 13.

- 固件 / Firmware: `wifi-csi-standalone`, `standalone-0.1.0`, IDF `v6.0-dirty`.
- 应用大小 / Application size: 836496 bytes, 1 MiB factory partition, about 20% free.
- 应用 SHA-256 / Binary SHA-256: `84b6704823765311e2ea402bbaa58f99507eee0b24330c5b36e9c7f2ee884dd6`.
- 先读取并校验完整 8 MiB Flash；设备分区表与构建匹配后，仅写入核验过的 0x20000 应用区，写入哈希校验通过。Full 8 MiB backup verified; device/build partition tables matched; only the verified application partition was written and its hash verified.
- 启动查询返回 `vision_enabled=false`，版本与构建对应。Firmware query confirmed version and disabled Vision integration.

|时长 / Seconds|完整诊断 / Samples|序号缺口 / Sequence gaps|Vision 等待 / Waits|重启/崩溃标记 / Reset/crash markers|
|---|---:|---:|---:|---:|
|10|171|0|0|0|
|20|338|0|0|0|
|30|509|0|0|0|

这些检查证明所测时段的接收和独立运行，不证明运动分类准确率。备份、私有配置及原始日志不公开。These checks establish observed reception/standalone operation, not movement classification accuracy. Backups, private configuration and raw logs are not published.
