import argparse
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "data" / "ISICClassification_zh.json"


def convert_json_unicode(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="将 JSON 中的 Unicode 转义中文转换为可读中文")
    parser.add_argument(
        "input",
        nargs="?",
        default=str(DEFAULT_INPUT),
        help="输入 JSON 文件路径，默认处理 ilcd/data/ISICClassification_zh.json",
    )
    parser.add_argument("-o", "--output", help="输出文件路径；不指定时原地覆盖输入文件")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve() if args.output else input_path

    if not input_path.exists():
        raise FileNotFoundError(f"未找到输入文件: {input_path}")

    convert_json_unicode(input_path, output_path)
    print(f"转换完成: {output_path}")


if __name__ == "__main__":
    main()