# -*- coding: utf-8 -*-
"""
此脚本用于检查本地化字符串文件之间缺失的键。

使用方法:
python3 check_missing_localizations.py <base_file_path> <compare_file1_path> [compare_file2_path]

参数说明:
  base_file_path:    基础语言环境的 .strings 文件路径 (例如: en.lproj/Localizable.strings)。
                     脚本会将这个文件中的键作为基准。
  compare_file1_path: 第一个需要比较的 .strings 文件路径 (例如: zh-Hans.lproj/Localizable.strings)。
                      脚本会检查此文件相对于 base_file 缺少了哪些键。
  compare_file2_path: (可选) 第二个需要比较的 .strings 文件路径 (例如: zh-Hant.lproj/Localizable.strings)。
                      脚本会检查此文件相对于 base_file 缺少了哪些键。

示例:
python3 check_missing_localizations.py Bitfull/Resources/Localization/zh-Hans.lproj/Localizable.strings Bitfull/Resources/Localization/en.lproj/Localizable.strings
python3 check_missing_localizations.py Astro/Resource/en.lproj/Localizable.strings Astro/Resource/zh-Hans.lproj/Localizable.strings Astro/Resource/zh-Hant.lproj/Localizable.strings

脚本会输出 compare_file1 和 compare_file2 (如果提供) 中分别相对于 base_file 缺失的键列表。
"""
import re
import argparse
import os

def parse_strings_file_content(content):
    """
    Parses the content of a .strings file and returns a set of keys.
    """
    keys = set()
    # Regex to find lines like "KEY" = "VALUE";
    # It captures the KEY part.
    # It handles spaces around '=' and at the end before ';'
    # It also correctly handles escaped quotes within the value if any, though we only care about the key.
    pattern = re.compile(r'^"((?:[^"\\]|\\.)*)"\s*=\s*".*?";', re.UNICODE)
    
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        
        match = pattern.match(line)
        if match:
            keys.add(match.group(1))
    return keys

def read_file_content(file_path):
    """
    Reads and returns the content of a file.
    Returns None if the file cannot be read.
    """
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在 - {file_path}")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"错误: 读取文件失败 {file_path}: {e}")
        return None

def compare_and_display_missing_keys(base_keys, compare_keys, compare_name):
    """
    Compares base keys with compare keys and displays missing keys.
    """
    missing_keys = base_keys - compare_keys
    
    if missing_keys:
        print(f"{compare_name} 文件缺失的键 ({len(missing_keys)} 个)：")
        for key in sorted(list(missing_keys)):
            print(f'  "{key}"')
    else:
        print(f"✅ {compare_name} 文件没有缺失的键。")
    
    return len(missing_keys)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='检查本地化字符串文件之间缺失的键。',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 check_missing_localizations.py base.strings compare1.strings
  python3 check_missing_localizations.py base.strings compare1.strings compare2.strings
        """
    )
    parser.add_argument('base_file', help='基准本地化文件路径 (例如: en.lproj/Localizable.strings)')
    parser.add_argument('compare_file1', help='第一个比较文件路径 (例如: zh-Hans.lproj/Localizable.strings)')
    parser.add_argument('compare_file2', nargs='?', help='(可选) 第二个比较文件路径 (例如: zh-Hant.lproj/Localizable.strings)')
    
    args = parser.parse_args()
    
    # Read and validate base file
    print(f"📖 读取基准文件: {args.base_file}")
    base_content = read_file_content(args.base_file)
    if base_content is None:
        return 1
    
    base_keys = parse_strings_file_content(base_content)
    if not base_keys:
        print(f"警告: 基准文件中没有找到任何键")
        return 1
    
    print(f"✅ 基准文件包含 {len(base_keys)} 个键\n")
    
    # Get file names for display
    base_name = os.path.basename(os.path.dirname(args.base_file))
    compare1_name = os.path.basename(os.path.dirname(args.compare_file1))
    
    # Read and compare first file
    print(f"📖 读取比较文件 1: {args.compare_file1}")
    compare1_content = read_file_content(args.compare_file1)
    if compare1_content is None:
        return 1
    
    compare1_keys = parse_strings_file_content(compare1_content)
    print(f"✅ 比较文件 1 包含 {len(compare1_keys)} 个键\n")
    
    # Compare and display results for file 1
    print("=" * 50)
    total_missing = compare_and_display_missing_keys(base_keys, compare1_keys, compare1_name)
    
    # Process second file if provided
    if args.compare_file2:
        print("\n" + "=" * 50 + "\n")
        
        compare2_name = os.path.basename(os.path.dirname(args.compare_file2))
        print(f"📖 读取比较文件 2: {args.compare_file2}")
        compare2_content = read_file_content(args.compare_file2)
        
        if compare2_content is not None:
            compare2_keys = parse_strings_file_content(compare2_content)
            print(f"✅ 比较文件 2 包含 {len(compare2_keys)} 个键\n")
            
            print("=" * 50)
            total_missing += compare_and_display_missing_keys(base_keys, compare2_keys, compare2_name)
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 总结: 共发现 {total_missing} 个缺失的键")
    print("=" * 50)
    
    return 0 if total_missing == 0 else 1

if __name__ == "__main__":
    main()
