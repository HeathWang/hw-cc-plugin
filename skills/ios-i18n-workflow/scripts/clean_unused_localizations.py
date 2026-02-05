#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理未使用的国际化字符串脚本

这个脚本会：
1. 解析 Localizable.strings 文件，提取所有的国际化键值对
2. 将原始键（snake_case）转换为 SwiftGen 生成的 camelCase 格式
3. 在项目代码中搜索每个 L10n.camelCaseKey 的引用
4. 删除未使用的国际化条目
5. 生成清理报告

使用方法:
python3 clean_unused_localizations.py [--dry-run] [--verbose]

参数：
--dry-run: 只显示会删除的条目，不实际修改文件
--verbose: 显示详细的搜索过程
"""

import re
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set
import subprocess

class LocalizationCleaner:
    def __init__(self, project_root: str, localizable_file: str = None, source_dir: str = None,
                 dry_run: bool = False, verbose: bool = False):
        self.project_root = Path(project_root)
        self.dry_run = dry_run
        self.verbose = verbose

        # Use provided paths or fall back to defaults
        if localizable_file:
            self.localizable_file = Path(localizable_file)
        else:
            # Default: search for Localizable.strings in common locations
            self.localizable_file = self._find_localizable_file()

        if source_dir:
            self.source_dir = Path(source_dir)
        else:
            # Default: use project root or common subdirectory
            self.source_dir = self._find_source_dir()

        # 需要搜索的文件扩展名
        self.search_extensions = ['.swift', '.m', '.mm', '.h']

    def _find_localizable_file(self) -> Path:
        """Search for Localizable.strings in common locations"""
        common_paths = [
            self.project_root / "Resources" / "Localization" / "en.lproj" / "Localizable.strings",
            self.project_root / "Resources" / "Localization" / "zh-Hans.lproj" / "Localizable.strings",
            self.project_root / "Localization" / "en.lproj" / "Localizable.strings",
        ]

        for path in common_paths:
            if path.exists():
                print(f"Found localization file: {path}")
                return path

        # If not found, raise error with helpful message
        raise FileNotFoundError(
            f"Cannot find Localizable.strings automatically. "
            f"Please specify using --localizable-file parameter. "
            f"Common locations checked: {[str(p) for p in common_paths]}"
        )

    def _find_source_dir(self) -> Path:
        """Find the source code directory"""
        common_dirs = [
            self.project_root,
            self.project_root / "Sources",
            self.project_root / "App",
        ]

        for dir_path in common_dirs:
            if dir_path.exists() and any(dir_path.rglob(f'*{self.search_extensions[0]}')):
                print(f"Using source directory: {dir_path}")
                return dir_path

        # Default to project root
        print(f"Using project root as source directory: {self.project_root}")
        return self.project_root
        
    def snake_to_camel(self, snake_str: str) -> str:
        """
        将键名转换为 SwiftGen 生成的格式

        SwiftGen 的命名规则（基于 .claude/commands/translate-cn.md）：
        1. 键名按点号分割：common.ok → ['common', 'ok']
        2. 除最后一个部分外，每个部分首字母大写（Title Case）：['Common', 'ok']
        3. 最后一个部分如果是 snake_case（包含下划线），转换为 camelCase
        4. 用点号连接：Common.ok
        5. 最终在代码中使用：L10n.Common.ok

        示例（来自 translate-cn.md）：
        - common.ok → L10n.Common.ok
        - market.back → L10n.Market.back
        - market.header.name → L10n.Market.Header.name
        - addbalance.flashexchange.subtitle → L10n.Addbalance.Flashexchange.subtitle
        - futuresrecords.header.amount_usdt → L10n.Futuresrecords.Header.amountUsdt

        重要说明：
        - 复合词（flashexchange）只首字母大写：Flashexchange，而非 FlashExchange
        - 嵌套键（inprogress）只首字母大写：Inprogress，而非 InProgress
        - 最后一级的 snake_case 转换为 camelCase：amount_usdt → amountUsdt
        """
        # 先按点号分割
        parts = snake_str.split('.')

        # 对除最后一个部分外的所有部分进行首字母大写（Title Case）
        result_parts = []
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # 最后一个部分需要特殊处理
                # 如果包含下划线（snake_case），转换为 camelCase
                if '_' in part:
                    # snake_case → camelCase
                    sub_parts = part.split('_')
                    camel_case = sub_parts[0] + ''.join(word.capitalize() for word in sub_parts[1:])
                    result_parts.append(camel_case)
                else:
                    # 没有下划线，保持原样
                    result_parts.append(part)
            else:
                # 其他部分首字母大写（Title Case，只大写首字母）
                result_parts.append(part[0].upper() + part[1:] if part else part)

        return '.'.join(result_parts)
    
    def parse_localizable_strings(self) -> Dict[str, Tuple[str, str]]:
        """
        解析 Localizable.strings 文件
        返回: {original_key: (camel_case_key, value)}
        """
        if not self.localizable_file.exists():
            raise FileNotFoundError(f"Localizable.strings 文件不存在: {self.localizable_file}")
            
        localizations = {}
        
        with open(self.localizable_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 匹配 "key" = "value"; 格式的行
        # 支持键名中的点号（如 common.ok）和值中的转义字符
        pattern = r'^\s*"([a-zA-Z0-9_.-]+)"\s*=\s*"((?:[^"\\]|\\.)*)"\s*;\s*$'
        
        for line_num, line in enumerate(content.splitlines(), 1):
            line = line.strip()
            
            # 跳过注释和空行
            if not line or line.startswith('//'):
                continue
                
            match = re.match(pattern, line)
            if match:
                original_key = match.group(1)
                value = match.group(2)
                camel_case_key = self.snake_to_camel(original_key)
                localizations[original_key] = (camel_case_key, value)
                
                if self.verbose:
                    print(f"解析: {original_key} -> L10n.{camel_case_key}")
            else:
                # 检查是否是有效的本地化行但格式不匹配
                if '"' in line and '=' in line and ';' in line:
                    print(f"警告: 第{line_num}行格式可能有问题: {line}")
        
        print(f"总共解析了 {len(localizations)} 个国际化条目")
        return localizations
    
    def find_swift_files(self) -> List[Path]:
        """查找所有需要搜索的源码文件"""
        files = []
        for ext in self.search_extensions:
            files.extend(self.source_dir.rglob(f'*{ext}'))
        
        # 排除一些不需要搜索的目录
        excluded_dirs = {'Pods', 'build', 'DerivedData', '.git'}
        filtered_files = []
        
        for file in files:
            # 检查文件路径是否包含排除的目录
            if not any(excluded_dir in file.parts for excluded_dir in excluded_dirs):
                filtered_files.append(file)
        
        return filtered_files
    
    def search_in_file(self, file_path: Path, search_term: str) -> bool:
        """在文件中搜索指定的字符串"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                return search_term in content
        except Exception as e:
            if self.verbose:
                print(f"读取文件 {file_path} 时出错: {e}")
            return False
    
    def is_localization_used(self, original_key: str, camel_case_key: str, swift_files: List[Path]) -> Tuple[bool, List[Path], str]:
        """
        检查本地化键是否在代码中被使用。
        优化：找到任何一个使用实例后立即返回，提高效率。
        返回: (是否使用, 使用的文件列表, 使用方式)
        """
        # 1. 首先检查 SwiftGen 方式: L10n.camelCaseKey
        swiftgen_term = f"L10n.{camel_case_key}"
        for file_path in swift_files:
            if self.search_in_file(file_path, swiftgen_term):
                return True, [file_path], "SwiftGen"

        # 2. 如果 SwiftGen 方式没有找到，再检查原生方式
        # Objective-C: NSLocalizedString(@"key"
        native_term_oc = f'NSLocalizedString(@"{original_key}"'
        # Swift: NSLocalizedString("key"
        native_term_swift = f'NSLocalizedString("{original_key}"'

        for file_path in swift_files:
            # 根据文件类型选择不同的搜索模式
            if file_path.suffix in ['.m', '.mm', '.h']:
                if self.search_in_file(file_path, native_term_oc):
                    return True, [file_path], "NSLocalizedString"
            elif file_path.suffix == '.swift':
                if self.search_in_file(file_path, native_term_swift):
                    return True, [file_path], "NSLocalizedString"
                # Swift 文件也可能包含 OC 的格式，以防万一
                if self.search_in_file(file_path, native_term_oc):
                    return True, [file_path], "NSLocalizedString"
        
        return False, [], ""
    
    def find_unused_localizations(self, localizations: Dict[str, Tuple[str, str]]) -> Tuple[Dict[str, Tuple[str, str]], Dict[str, Tuple[str, str, str]]]:
        """
        找出未使用的本地化条目
        返回: (未使用的条目, 已使用的条目详情)
        """
        unused = {}
        used_details = {}  # {original_key: (camel_case_key, value, usage_type)}
        total = len(localizations)
        
        print("开始搜索未使用的国际化条目...")
        swift_files = self.find_swift_files()
        
        for i, (original_key, (camel_case_key, value)) in enumerate(localizations.items(), 1):
            if self.verbose:
                print(f"检查 ({i}/{total}): L10n.{camel_case_key} / NSLocalizedString(\"{original_key}\"")
            else:
                # 显示进度
                if i % 50 == 0 or i == total:
                    print(f"进度: {i}/{total}")
            
            is_used, used_files, usage_type = self.is_localization_used(original_key, camel_case_key, swift_files)
            
            if not is_used:
                unused[original_key] = (camel_case_key, value)
                if self.verbose:
                    print(f"  ❌ 未使用: {original_key}")
            else:
                used_details[original_key] = (camel_case_key, value, usage_type)
                if self.verbose:
                    # 因为 is_localization_used 只返回第一个找到的文件，所以 used_files[0] 是安全的
                    print(f"  ✅ 已使用: {original_key} (方式: {usage_type}, 在 {used_files[0].name} 中找到)")
        
        return unused, used_details
    
    def remove_unused_localizations(self, unused_keys: Set[str]) -> bool:
        """从 Localizable.strings 文件中删除未使用的条目"""
        if not unused_keys:
            print("没有找到未使用的国际化条目")
            return True
            
        if self.dry_run:
            print(f"[DRY RUN] 将会删除 {len(unused_keys)} 个未使用的条目")
            return True
        
        try:
            with open(self.localizable_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 创建备份
            backup_file = self.localizable_file.with_suffix('.strings.backup')
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"已创建备份文件: {backup_file}")
            
            # 过滤掉未使用的条目
            filtered_lines = []
            removed_count = 0
            
            for line in lines:
                line_stripped = line.strip()
                
                # 如果是空行或注释，保留
                if not line_stripped or line_stripped.startswith('//'):
                    filtered_lines.append(line)
                    continue
                
                # 检查是否是要删除的本地化条目
                match = re.match(r'^\s*"([a-zA-Z0-9_.-]+)"\s*=\s*"(?:[^"\\]|\\.)*"\s*;\s*$', line_stripped)
                if match:
                    key = match.group(1)
                    if key in unused_keys:
                        removed_count += 1
                        if self.verbose:
                            print(f"删除: {line_stripped}")
                        continue
                
                filtered_lines.append(line)
            
            # 写回文件
            with open(self.localizable_file, 'w', encoding='utf-8') as f:
                f.writelines(filtered_lines)
            
            print(f"成功删除了 {removed_count} 个未使用的国际化条目")
            return True
            
        except Exception as e:
            print(f"删除未使用条目时出错: {e}")
            return False
    
    def generate_report(self, localizations: Dict[str, Tuple[str, str]], unused: Dict[str, Tuple[str, str]], used_details: Dict[str, Tuple[str, str, str]]):
        """生成清理报告"""
        report_file = self.project_root / "localization_cleanup_report.txt"
        
        # 统计使用方式
        swiftgen_count = sum(1 for details in used_details.values() if details[2] == "SwiftGen")
        nslocalizedstring_count = sum(1 for details in used_details.values() if details[2] == "NSLocalizedString")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("国际化字符串清理报告\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"项目路径: {self.project_root}\n")
            f.write(f"本地化文件: {self.localizable_file}\n")
            f.write(f"扫描时间: {__import__('datetime').datetime.now()}\n\n")
            
            f.write("统计信息:\n")
            f.write("-" * 20 + "\n")
            f.write(f"总计国际化条目: {len(localizations)}\n")
            f.write(f"已使用条目: {len(used_details)}\n")
            f.write(f"  - SwiftGen 方式 (L10n.xxx): {swiftgen_count}\n")
            f.write(f"  - 原生方式 (NSLocalizedString): {nslocalizedstring_count}\n")
            f.write(f"未使用条目: {len(unused)}\n")
            f.write(f"使用率: {((len(localizations) - len(unused)) / len(localizations) * 100):.1f}%\n\n")
            
            if unused:
                f.write("\n完全未使用的国际化条目:\n")
                f.write("=" * 30 + "\n")
                for original_key, (camel_case_key, value) in unused.items():
                    f.write(f'"{original_key}" = "{value}";\n')
            else:
                f.write("\n恭喜！没有发现未使用的国际化条目。\n")
        
        print(f"已生成清理报告: {report_file}")
        
        # 控制台输出使用方式统计
        if used_details:
            print(f"\n使用方式统计:")
            print(f"  SwiftGen 方式: {swiftgen_count} 个")
            print(f"  NSLocalizedString 方式: {nslocalizedstring_count} 个")
            
            if nslocalizedstring_count > 0:
                print(f"\n💡 建议: 发现 {nslocalizedstring_count} 个使用原生 NSLocalizedString 的条目")
                print("   为了保持代码一致性，建议将它们改为使用 SwiftGen 生成的 L10n.xxx 形式")
    
    def run(self):
        """执行清理流程"""
        print(f"开始清理国际化字符串...")
        print(f"项目路径: {self.project_root}")
        print(f"本地化文件: {self.localizable_file}")
        print(f"模式: {'DRY RUN' if self.dry_run else 'REAL RUN'}")
        print()
        
        # 1. 解析本地化文件
        try:
            localizations = self.parse_localizable_strings()
        except Exception as e:
            print(f"解析本地化文件失败: {e}")
            return False
        
        if not localizations:
            print("没有找到任何国际化条目")
            return False
        
        # 2. 查找未使用的条目
        unused, used_details = self.find_unused_localizations(localizations)
        
        # 3. 生成报告
        self.generate_report(localizations, unused, used_details)
        
        # 4. 显示结果
        print(f"\n清理结果:")
        print(f"总计条目: {len(localizations)}")
        print(f"未使用条目: {len(unused)}")
        print(f"使用率: {((len(localizations) - len(unused)) / len(localizations) * 100):.1f}%")
        
        if unused:
            print(f"\n发现 {len(unused)} 个未使用的条目:")
            for original_key, (camel_case_key, value) in unused.items():
                print(f'  "{original_key}" = "{value}";')
        
        # 5. 删除未使用的条目
        if unused:
            if self.dry_run:
                print(f"\n[DRY RUN] 如果执行清理，将删除 {len(unused)} 个未使用的条目")
            else:
                confirm = input(f"\n确定要删除这 {len(unused)} 个未使用的条目吗? (y/N): ")
                if confirm.lower() == 'y':
                    success = self.remove_unused_localizations(set(unused.keys()))
                    if success:
                        print("清理完成！请记得运行 SwiftGen 重新生成 Strings.swift 文件:")
                        print("swiftgen config run --config swiftgen.yml")
                    return success
                else:
                    print("取消清理操作")
        else:
            print("\n没有未使用的国际化条目，无需清理")
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description='清理未使用的国际化字符串',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 自动查找 Localizable.strings（在常见位置）
  python3 clean_unused_localizations.py

  # 指定本地化文件路径
  python3 clean_unused_localizations.py --localizable-file /path/to/Localizable.strings

  # 指定项目根目录和源码目录
  python3 clean_unused_localizations.py --project-root /path/to/project --source-dir /path/to/project/Sources

  # 预览模式（不实际修改文件）
  python3 clean_unused_localizations.py --dry-run
        """
    )
    parser.add_argument('--dry-run', action='store_true', help='只显示会删除的条目，不实际修改文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细的搜索过程')
    parser.add_argument('--project-root', default='.', help='项目根目录路径 (默认: 当前目录)')
    parser.add_argument('--localizable-file', help='Localizable.strings 文件的完整路径 (可选，自动查找)')
    parser.add_argument('--source-dir', help='源代码目录路径 (可选，默认自动查找)')

    args = parser.parse_args()

    # 检查项目根目录
    project_root = Path(args.project_root).resolve()
    if not project_root.exists():
        print(f"错误: 项目路径不存在: {project_root}")
        sys.exit(1)

    # 创建清理器并执行
    try:
        cleaner = LocalizationCleaner(
            project_root=str(project_root),
            localizable_file=args.localizable_file,
            source_dir=args.source_dir,
            dry_run=args.dry_run,
            verbose=args.verbose
        )

        success = cleaner.run()
        sys.exit(0 if success else 1)
    except FileNotFoundError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
