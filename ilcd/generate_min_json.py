import argparse
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = BASE_DIR / "data"


def iter_source_json_files(data_dir: Path):
    for json_file in sorted(data_dir.glob("*.json")):
        if json_file.name.endswith(".min.json"):
            continue
        yield json_file


def minify_json_file(source_file: Path, target_file: Path):
    with source_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    with target_file.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, ensure_ascii=False, separators=(",", ":"))


def generate_missing_min_json(data_dir: Path):
    if not data_dir.exists():
        raise FileNotFoundError(f"目录不存在: {data_dir}")

    if not data_dir.is_dir():
        raise NotADirectoryError(f"不是目录: {data_dir}")

    created_count = 0
    skipped_count = 0

    source_files = list(iter_source_json_files(data_dir))
    if not source_files:
        print(f"在 {data_dir} 中未找到可处理的 JSON 文件")
        return

    print(f"扫描目录: {data_dir}")
    print(f"找到 {len(source_files)} 个普通 JSON 文件")

    for source_file in source_files:
        target_file = source_file.with_name(f"{source_file.stem}.min.json")

        if target_file.exists():
            print(f"跳过: {target_file.name} 已存在")
            skipped_count += 1
            continue

        minify_json_file(source_file, target_file)
        print(f"生成: {target_file.name}")
        created_count += 1

    print("\n处理完成")
    print(f"新增: {created_count} 个文件")
    print(f"跳过: {skipped_count} 个文件")


def parse_args():
    parser = argparse.ArgumentParser(
        description="为缺失对应 .min.json 的 JSON 文件生成单行压缩版本"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=str(DEFAULT_DATA_DIR),
        help="要扫描的目录，默认是 ilcd/data",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate_missing_min_json(Path(args.directory).resolve())