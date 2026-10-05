# L0 单细胞最小公开运行 fixture

这是从 `cell_l0_demo` 的环境与感觉层概念中抽取并重新整理的、可独立运行的最小公开代码包。

它展示一条受限的生理流程：

```text
局部物理信号 → 感觉采样 → 生理输入 → 受限行为 → 状态更新
```

公开代码只包含：

- `cell_env.py`：固定二维物理场；
- `l0_sensing.py`：前、左、右探针与生理输入转换；
- `public_l0.py`：无界面、确定性的最小运行 fixture；
- `test_public_l0.py`：本包的独立测试。

## 运行

要求：Python 3.10 或更高版本；不需要第三方依赖、网络、API key 或外部服务。

在本目录执行：

```powershell
python -B public_l0.py
python -B -m unittest -v test_public_l0.py
```

固定 fixture 的当前结果：

```text
runs=20
division=20/20
median_first_division=21
```

## 如何理解结果

这些数字只表示本包固定输入下的可重复 fixture 结果，不是现实生物学结论，不是完整项目 runtime 的复现，也不代表数字生命、通用智能或生产级系统已经完成。

本 fixture 验证的是物理信号到行为标签的最小链路，不验证二维空间导航或真实转向动力学。

本包与 `CognitiveBridge` 仓库、后续私有主线和任何未审核代码保持独立。审核说明、清单和许可证状态文件只用于本次审核，不属于运行依赖。

## 许可证

本包当前不包含 `LICENSE`。公开查看不等于获得复制、修改、再发布或商业使用许可；许可证需另行决定。

