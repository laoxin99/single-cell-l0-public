# 代码载荷状态

```text
public runtime payload = INCLUDED / MINIMAL FIXTURE ONLY
source full runtime = NOT INCLUDED
private state/logs = NOT INCLUDED
experiment scripts = NOT INCLUDED
credentials/provider = NOT INCLUDED
```

本包只有四个 `.py` 文件，且四个文件都在本目录根部。它们不从目录外导入模块，不读取目录外文件，不创建日志文件。

`public_l0.py` 的职责是让审核者能在无网络环境中复现一条最小、可解释的 L0 fixture；它不是完整项目运行时，也不包含内部裁决链。

