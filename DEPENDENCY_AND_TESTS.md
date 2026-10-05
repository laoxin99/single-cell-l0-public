# 依赖、运行命令与测试记录

## 依赖

- Python 3.10+；
- 仅使用 Python 标准库；
- 本目录内的 `cell_env.py` 与 `l0_sensing.py` 是唯一运行时本地模块依赖；
- 不调用网络、provider、API key、环境外文件或外部服务。

## 运行命令

```powershell
python -B public_l0.py
```

## 测试命令

```powershell
python -B -m unittest -v test_public_l0.py
```

## 本次审核运行结果

```text
Ran 3 tests
OK

fixture=l0-public-minimal
dependencies=python-standard-library+2-local-modules
runs=20
division=20/20
median_first_division=21
boundary=fixture-only; not a full project runtime
```

结果是在审核包目录内、无网络条件下运行得到的；没有把源项目日志或缓存带入包内。

