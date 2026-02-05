# iOS I18n Helper Scripts

Helper scripts for iOS internationalization workflow management.

## check_missing_localizations.py

Compares localization files and reports missing translation keys.

**Usage:**
```bash
python3 check_missing_localizations.py \
  <baseline_file> \
  <compare_file1> \
  [compare_file2]
```

**Arguments:**
- `baseline_file`: Source of truth (e.g., `zh-Hans.lproj/Localizable.strings`)
- `compare_file1`: First target language to check
- `compare_file2` (optional): Second target language to check

**Example:**
```bash
python3 check_missing_localizations.py \
  Resources/Localization/zh-Hans.lproj/Localizable.strings \
  Resources/Localization/en.lproj/Localizable.strings
```

**Output:**
```
📖 读取基准文件: zh-Hans.lproj/Localizable.strings
✅ 基准文件包含 150 个键

📖 读取比较文件 1: en.lproj/Localizable.strings
✅ 比较文件 1 包含 145 个键

==================================================
en.lproj 文件缺失的键 (5 个)：
  "market.deposit"
  "market.totalassetvalue"
  "challenge.newbie.title"

==================================================
📊 总结: 共发现 5 个缺失的键
==================================================
```

## clean_unused_localizations.py

Finds and removes unused localization entries from codebase.

**Usage:**
```bash
# Auto-detect localization file
python3 clean_unused_localizations.py

# Dry run (show what would be deleted)
python3 clean_unused_localizations.py --dry-run

# Specify custom paths
python3 clean_unused_localizations.py \
  --localizable-file /path/to/Localizable.strings \
  --source-dir /path/to/source

# Verbose mode (show detailed search process)
python3 clean_unused_localizations.py --verbose
```

**What it does:**
1. Auto-detects or uses specified `Localizable.strings` file
2. Converts snake_case keys to SwiftGen camelCase format
3. Searches codebase for `L10n.camelCaseKey` or `NSLocalizedString` references
4. Reports unused entries
5. Optionally deletes unused entries (with backup and confirmation)

**Requirements:**
- Searches in `.swift`, `.m`, `.mm`, `.h` files
- Excludes `Pods`, `build`, `DerivedData`, `.git` directories
- Automatically finds localization file in common locations

**Troubleshooting:**

**Script not found:**
```bash
# Verify you're in the correct directory
pwd  # Should be: <project_root>
ls check_missing_localizations.py
ls clean_unused_localizations.py
```

**Permission denied:**
```bash
chmod +x check_missing_localizations.py
chmod +x clean_unused_localizations.py
```

## Installation

**Option 1: Use absolute path**
```bash
python3 /path/to/ios-i18n-workflow/scripts/check_missing_localizations.py \
  <baseline_file> <target_file>
```

**Option 2: Copy to project**
```bash
cp /path/to/ios-i18n-workflow/scripts/*.py <project_root>/
python3 check_missing_localizations.py <baseline_file> <target_file>
```

## Requirements

- Python 3.x
- iOS project with localization files
