# tiangong-lca-public-data-gen

该仓库用于维护和分发两类公开数据：

- ilcd：ILCD 分类与位置相关数据
- lcia：LCIA Method（ILCD LCIAMethodDataSet）数据及其索引、压缩产物与聚合结果

当前仓库中：

- ilcd/data/ 包含 5 类数据集，每类通常包含英文版、中文版、.min.json 与 .min.json.gz 派生产物
- lcia/data/json/ 当前维护 25 个方法文件，配套生成 list.json、flow_factors.json 与压缩文件目录

## 仓库结构

```text
.
|-- Readme.md
|-- ilcd/
|   |-- compress_json.py          压缩 ilcd/data/*.min.json 为 .gz
|   |-- decode_unicode_json.py    JSON Unicode 转中文文本辅助脚本
|   |-- generate_min_json.py      生成精简版 .min.json 辅助脚本
|   `-- data/
|       |-- CPCClassification*.json
|       |-- ILCDClassification*.json
|       |-- ILCDFlowCategorization*.json
|       |-- ILCDLocations*.json
|       `-- ISICClassification*.json
`-- lcia/
  |-- compress_json.py          压缩 data/json/*.json 到 json_compressed/
  |-- update_list.py            生成方法索引 list.json
  |-- get_all_flow_factors.py   生成 flow_factors.json 与 .gz
    `-- data/
    |-- json/
    |   |-- <UUID>.json
    |   `-- ...
    |-- json_compressed/
    |   |-- <UUID>_<version>.json.gz
    |   `-- ...
    |-- list_order.txt        list.json 的排序文件（按压缩文件名逐行列出）
    |-- list.json             方法文件索引（metadata + files[]）
    |-- flow_factors.json     全量 characterisationFactors 聚合表
    `-- flow_factors.json.gz  flow_factors.json 的 gzip 压缩版
```

说明：

- ilcd/data/ 下每类数据通常同时包含原始 JSON、精简版 .min.json、压缩版 .min.json.gz，以及对应的中文版本 _zh 文件。
- lcia/data/json/ 存放原始方法文件；其余文件多为由维护脚本生成的派生产物。

## 环境要求

- Python 3.9+
- 仅使用标准库，无额外依赖

## 快速开始

如果只是做日常数据维护，通常按下面顺序执行：

1. 新增或替换 lcia/data/json/ 下的原始方法文件。
2. 进入 lcia/ 目录，运行 compress_json.py 生成或补齐压缩方法文件。
3. 运行 update_list.py 刷新方法索引。
4. 运行 get_all_flow_factors.py 刷新聚合因子文件。
5. 如 ilcd/data/ 下的 .min.json 有新增或变更，再回到仓库根目录运行 ilcd/compress_json.py。

如果只更新文档或只替换已有压缩产物，并不一定需要执行全部脚本。

## 使用说明

### 一、ILCD 数据压缩（ilcd）

用途：将 ilcd/data/ 下的所有 .min.json 文件逐个压缩为同名 .min.json.gz 文件。

执行位置：仓库根目录。

执行方式：

```bash
python ilcd/compress_json.py
```

脚本行为：

- 基于脚本自身所在目录定位 ilcd/data/，可在仓库根目录直接执行
- 扫描 ilcd/data/*.min.json
- 为每个文件生成同名 gzip 文件，例如 ILCDFlowCategorization.min.json.gz
- 若目标 gzip 文件已存在，则跳过
- 执行结束后会输出当前 data/ 下所有 .gz 文件及其大小

当前覆盖的数据集包括：

- CPCClassification
- ILCDClassification
- ILCDFlowCategorization
- ILCDLocations
- ISICClassification

每类数据均包含英文版与中文版（_zh）。

### 二、LCIA 方法文件维护（lcia）

注意：lcia 下三个维护脚本内部均使用相对路径 data/...，必须先进入 lcia/ 目录再执行。

执行位置对照：

- ilcd/compress_json.py：在仓库根目录执行
- lcia/compress_json.py：先进入 lcia/，再执行
- lcia/update_list.py：先进入 lcia/，再执行
- lcia/get_all_flow_factors.py：先进入 lcia/，再执行

Windows PowerShell：

```powershell
cd .\lcia
```

macOS / Linux：

```bash
cd ./lcia
```

#### 1. 生成压缩方法文件

将 data/json/*.json 压缩为 data/json_compressed/*.json.gz。

```bash
python compress_json.py
```

脚本行为：

- 读取每个原始方法文件中的 common:dataSetVersion
- 按 UUID_版本号.json.gz 规则命名输出文件
- 若目标压缩文件已存在，则跳过
- 执行结束后会输出压缩目录中的文件列表、UUID、版本号与大小

输出目录：data/json_compressed/

#### 2. 生成或更新方法索引

根据 data/json/ 与 data/json_compressed/ 重新生成 data/list.json。

```bash
python update_list.py
```

脚本会提取以下信息：

- 方法 UUID
- 数据集版本号
- 方法名称 common:name
- 影响模型名称 impactModel.modelName
- 参考计量单位 quantitativeReference.referenceQuantity
- 文件大小：优先使用压缩文件大小，若压缩文件不存在则退回原始 JSON 文件大小

排序规则：

- 若存在 data/list_order.txt，则优先按该文件中的压缩文件名顺序输出
- 若有未出现在 list_order.txt 中的文件，会在末尾追加
- 若不存在 list_order.txt，则按文件名默认排序

脚本还会在 metadata 中写入：

- description
- totalFiles
- format
- lastUpdated
- compressionRatio
- originalSize
- totalSize

输出文件：data/list.json

#### 3. 生成或更新 flow 因子聚合表

汇总所有方法中的 characterisationFactors.factor，生成：

- data/flow_factors.json
- data/flow_factors.json.gz

```bash
python get_all_flow_factors.py
```

脚本行为：

- 从每个方法中提取 referenceToFlowDataSet、exchangeDirection、meanValue
- 兼容 factor 为数组或单个对象两种情况
- 按 flow 引用与交换方向聚合同一 flow 在不同方法中的因子
- 若旧的 flow_factors.json 或 flow_factors.json.gz 存在，会先删除再重建

输出文件：

- data/flow_factors.json
- data/flow_factors.json.gz

## 产物格式

### lcia/data/list.json

顶层结构：

```json
{
  "metadata": { ... },
  "files": [ ... ]
}
```

metadata 字段通常包含：

- description：索引说明
- totalFiles：方法文件总数
- format：文件格式说明
- lastUpdated：生成日期
- compressionRatio：总压缩率（如果计算成功）
- originalSize：原始总大小（如果计算成功）
- totalSize：压缩后总大小（如果计算成功）

files[] 中每个条目通常包含：

- filename：UUID_版本号.json.gz
- id：方法 UUID
- version：版本号
- size：文件大小字符串，如 12.4KB 或 3.8MB
- description：方法名称，通常直接保留原始 common:name 结构；当前数据中通常为多语言数组
- impactModel：模型名称
- referenceQuantity：参考计量单位对象，仅在源数据存在时写入

当前仓库中的 metadata 示例特征：

- totalFiles 为 25
- format 为 gzip compressed JSON
- lastUpdated 为脚本执行当天日期
- compressionRatio、originalSize、totalSize 由原始 JSON 与压缩文件总大小计算得到

### lcia/data/flow_factors.json

该文件是一个对象映射，而不是数组。结构如下：

- key：@refObjectId:EXCHANGEDIRECTION
- value：对应 flow 的聚合对象

value 对象包含：

- @refObjectId
- @version
- exchangeDirection
- factor

其中 factor 为数组，每条记录形如：

```json
{
  "key": "<methodUUID>",
  "value": <meanValue>
}
```

也就是说，同一个 flow 在不同方法中的表征因子会被聚合到同一个 value.factor 数组中。

## 数据维护流程

1. 将新的 LCIA 方法 JSON 放入 lcia/data/json/，命名为 <UUID>.json。
2. 进入 lcia/ 目录，运行 python compress_json.py 生成对应压缩文件。
3. 如需控制展示顺序，更新 lcia/data/list_order.txt。
4. 运行 python update_list.py 重新生成 lcia/data/list.json。
5. 运行 python get_all_flow_factors.py 重新生成聚合因子文件。
6. 如有新增或修改的 ilcd 精简文件，可在仓库根目录运行 python ilcd/compress_json.py 重新生成对应 .gz 文件。

推荐检查点：

- 确认 lcia/data/json_compressed/ 中已生成对应版本号的压缩文件
- 确认 lcia/data/list.json 中 totalFiles 与 data/json/ 中方法文件数量一致
- 确认 lcia/data/flow_factors.json.gz 已重新生成

## 注意事项

- update_list.py 会覆盖写入 lcia/data/list.json
- get_all_flow_factors.py 会删除并重建 lcia/data/flow_factors.json 与 lcia/data/flow_factors.json.gz
- flow_factors.json 可能较大，日常使用建议优先读取 flow_factors.json.gz
- 压缩文件命名中的版本号来自 LCIAMethodDataSet.administrativeInformation.publicationAndOwnership.common:dataSetVersion
- 若未先切换到 lcia/ 目录执行 lcia 脚本，脚本中的相对路径将无法命中 lcia/data/
- 若 data/list_order.txt 中缺少新文件名，update_list.py 会将这些未排序文件追加到末尾
