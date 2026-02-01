# tiangong-lcia-data

该仓库用于维护/分发一组 **LCIA Method（ILCD LCIAMethodDataSet）** 的 JSON 数据，以及配套的索引文件与辅助产物（压缩包、因子聚合表）。

## 目录结构

```
data/
	json/                 原始 ILCD LCIAMethodDataSet JSON（文件名为 UUID.json）
	json_compressed/      压缩后的方法文件（UUID_版本号.json.gz）
	list_order.txt        list.json 的文件顺序（按压缩文件名逐行列出）
	list.json             方法文件索引（metadata + files[]）
	flow_factors.json     全量 characterisationFactors 聚合表（可能很大）
	flow_factors.json.gz  flow_factors.json 的 gzip 压缩版
```

### `data/list.json` 字段约定（简述）

- `metadata`: 描述、总数、格式、更新时间等
- `files[]`: 每个方法文件的摘要信息
	- `filename`: `UUID_版本号.json.gz`
	- `id`: 方法 UUID
	- `version`: 版本号（来自 `common:dataSetVersion`）
	- `size`: 文件大小（优先读取压缩文件大小）
	- `description`: 方法名称（通常为 `common:name`，可能包含多语言数组）
	- `impactModel`: 模型名称（来自 `impactModel.modelName`）
	- `referenceQuantity`（如存在）: 参考计量单位（来自 `quantitativeReference.referenceQuantity`）

### `data/flow_factors.json` 结构（简述）

该文件将所有方法内的 `characterisationFactors.factor` 按 flow 聚合：

- key: `@refObjectId:EXCHANGEDIRECTION`（例如 `fe0acd60-...:OUTPUT`）
- value: 一个对象，包含 `@refObjectId`、`@version`、`exchangeDirection`，以及 `factor[]`
- `factor[]` 中每条记录形如 `{ "key": <methodUUID>, "value": <meanValue> }`

## 环境要求

- Python 3.9+（标准库即可，无额外依赖）

## 快速开始

在仓库根目录运行（Windows / macOS / Linux 均可）：

1) 生成压缩方法文件（输出到 `data/json_compressed/`）

```bash
python compress_json.py
```

2) 生成/更新索引文件（写入 `data/list.json`）

```bash
python update_list.py
```

3) 生成/更新 flow 因子聚合表（写入 `data/flow_factors.json` 与 `data/flow_factors.json.gz`）

```bash
python get_all_flow_factors.py
```

## 数据维护流程（新增/更新方法文件）

1. 将新的 ILCD 方法 JSON 放入 `data/json/`，命名为 `<UUID>.json`
2. 运行 `python compress_json.py` 生成对应的 `UUID_版本号.json.gz`
3. 如需控制展示/分发顺序，更新 `data/list_order.txt`（按压缩文件名逐行列出）
4. 运行 `python update_list.py` 重新生成 `data/list.json`
5. 运行 `python get_all_flow_factors.py` 重新生成聚合因子文件

## 注意事项

- `update_list.py` 会覆盖写入 `data/list.json`：如果你对 `list.json` 做过手工扩展字段，请先确认脚本是否已覆盖到这些字段。
- `flow_factors.json` 可能非常大；日常使用建议优先读取 `flow_factors.json.gz`。
- 压缩文件命名中的版本号来自方法 JSON 的 `LCIAMethodDataSet.administrativeInformation.publicationAndOwnership.common:dataSetVersion`。
