import glob
import gzip
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def compress_json_files():
    """压缩data目录中的.min.json文件为同名GZ文件"""

    source_dir = BASE_DIR / "data"

    # 获取所有.min.json文件
    json_pattern = str(source_dir / "*.min.json")
    json_files = sorted(glob.glob(json_pattern))

    if not json_files:
        print(f"在 {source_dir} 中未找到 .min.json 文件")
        return

    print(f"找到 {len(json_files)} 个 .min.json 文件")

    processed_count = 0
    skipped_count = 0
    error_count = 0

    for json_file in json_files:
        try:
            file_path = Path(json_file)

            print(f"\n处理文件: {file_path.name}")

            target_path = Path(f"{json_file}.gz")
            target_file = str(target_path)

            if target_path.exists():
                print(f"⏭ 文件已存在，跳过: {target_path.name}")
                skipped_count += 1
                continue

            with open(json_file, "r", encoding="utf-8") as f:
                json_content = f.read()

            with gzip.open(target_file, "wt", encoding="utf-8") as f:
                f.write(json_content)

            original_size = os.path.getsize(json_file)
            compressed_size = os.path.getsize(target_file)
            compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0

            print(f"✓ 压缩完成: {target_path.name}")
            print(f"  原始大小: {original_size:,} 字节")
            print(f"  压缩大小: {compressed_size:,} 字节")
            print(f"  压缩率: {compression_ratio:.1f}%")

            processed_count += 1

        except Exception as e:
            print(f"✗ 处理文件出错 {json_file}: {e}")
            error_count += 1

    print(f"\n{'='*50}")
    print(f"压缩完成统计:")
    print(f"  成功处理: {processed_count} 个文件")
    print(f"  跳过文件: {skipped_count} 个文件")
    print(f"  出错文件: {error_count} 个文件")
    print(f"  总文件数: {len(json_files)} 个文件")
    print(f"压缩文件保存在: {source_dir}")

def list_compressed_files():
    """列出data目录中的GZ文件"""
    target_dir = BASE_DIR / "data"

    if not target_dir.exists():
        print("data目录不存在")
        return

    gz_files = glob.glob(str(target_dir / "*.gz"))

    print(f"\n压缩文件列表 ({len(gz_files)} 个文件):")
    print("-" * 60)

    total_size = 0
    for gz_file in sorted(gz_files):
        file_path = Path(gz_file)
        file_size = os.path.getsize(gz_file)
        total_size += file_size

        print(f"{file_path.name}")
        print(f"  大小: {file_size:,} 字节")
        print()

    print(f"总大小: {total_size:,} 字节 ({total_size/1024/1024:.2f} MB)")

if __name__ == "__main__":
    print("开始压缩JSON文件...")
    compress_json_files()
    list_compressed_files()
    print("处理完成！")
