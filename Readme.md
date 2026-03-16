# tiangong-lca-public-data-gen

该仓库用于维护和分发一组 LCIA Method（ILCD LCIAMethodDataSet）JSON 数据，以及与之配套的索引文件、压缩文件和 flow 因子聚合产物。

## 仓库结构

仓库根目录结构如下：

```text
.
|-- Readme.md
`-- lcia/
    |-- compress_json.py
    |-- update_list.py
    |-- get_all_flow_factors.py
    `-- data/
        |-- json/                 原始 ILCD LCIAMethodDataSet JSON（文件名为 UUID.json）
        |-- json_compressed/      压缩后的方法文件（UUID_版本号.json.gz）
        |-- list_order.txt        list.json 的排序文件（按压缩文件名逐行列出）
        |-- list.json             方法文件索引（metadata + files[]）
        |-- flow_factors.json     全量 characterisationFactors 聚合表
        `-- flow_factors.json.gz  flow_factors.json 的 gzip 压缩版
```

## 环境要求

- Python 3.9+
- 仅使用标准库，无额外依赖

## 使用说明

注意：三个维护脚本内部都使用相对路径 `data/...`，因此需要在 `lcia/` 目录下执行。

Windows PowerShell：

```powershell
cd .\lcia
```

macOS / Linux：

```bash
cd ./lcia
```

### 1. 生成压缩方法文件

将 `data/json/*.json` 压缩为 `data/json_compressed/*.json.gz`

```bash
python compress_json.py
```

脚本行为：

- 从每个原始方法文件中读取 `common:dataSetVersion`
- 按 `UUID_版本号.json.gz` 命名输出文件
- 若目标压缩文件已存在，则跳过该文件

### 2. 生成或更新方法索引

根据 `data/json/` 和 `data/json_compressed/` 重新生成 `data/list.json`

```bash
python update_list.py
```

脚本会提取以下信息：

- 方法 UUID
- 数据集版本号
- 方法名称 `common:name`
- 影响模型名称 `impactModel.modelName`
- 参考计量单位 `quantitativeReference.referenceQuantity`
- 压缩文件大小

若存在 `data/list_order.txt`，输出顺序会优先按该文件排列。

### 3. 生成或更新 flow 因子聚合表

汇总所有方法中的 `characterisationFactors.factor`，生成：

- `data/flow_factors.json`
- `data/flow_factors.json.gz`

```bash
python get_all_flow_factors.py
```

脚本行为：

- 从每个方法中提取 `referenceToFlowDataSet`、`exchangeDirection`、`meanValue`
- 按 flow 和交换方向聚合不同方法的因子
- 若旧的 `flow_factors.json` 或 `flow_factors.json.gz` 存在，会先删除再重建

## 产物格式

### `lcia/data/list.json`

`metadata` 字段包含：

- `description`: 索引说明
- `totalFiles`: 方法文件总数
- `format`: 文件格式说明
- `lastUpdated`: 生成日期
- `compressionRatio`: 总压缩率（如果计算成功）
- `originalSize`: 原始总大小（如果计算成功）
- `totalSize`: 压缩后总大小（如果计算成功）

`files[]` 中每个条目通常包含：

- `filename`: `UUID_版本号.json.gz`
- `id`: 方法 UUID
- `version`: 版本号
- `size`: 文件大小，优先使用压缩文件大小
- `description`: 方法名称，可能为多语言数组
- `impactModel`: 模型名称
- `referenceQuantity`: 参考计量单位对象（如存在）

### `lcia/data/flow_factors.json`

该文件是一个对象映射，结构如下：

- key: `@refObjectId:EXCHANGEDIRECTION`
- value: 一个对象，包含：
- `@refObjectId`
- `@version`
- `exchangeDirection`
- `factor`

其中 `factor` 为数组，每条记录形如：

```json
{
  "key": "<methodUUID>",
  "value": <meanValue>
}
```

## 数据维护流程

1. 将新的 ILCD 方法 JSON 放入 `lcia/data/json/`，命名为 `<UUID>.json`。
2. 进入 `lcia/` 目录，运行 `python compress_json.py` 生成对应压缩文件。
3. 如需控制展示顺序，更新 `lcia/data/list_order.txt`。
4. 运行 `python update_list.py` 重新生成 `lcia/data/list.json`。
5. 运行 `python get_all_flow_factors.py` 重新生成聚合因子文件。

## 注意事项

- `update_list.py` 会覆盖写入 `lcia/data/list.json`
- `flow_factors.json` 可能很大，日常使用建议优先读取 `flow_factors.json.gz`。
- 压缩文件命名中的版本号来自 `LCIAMethodDataSet.administrativeInformation.publicationAndOwnership.common:dataSetVersion`。
- 如果你想从仓库根目录执行脚本，需要先切换到 `lcia/`，否则脚本中的相对路径不会命中 `lcia/data/`。
