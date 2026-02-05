# iOS I18n Advanced Usage

Advanced workflows and integration patterns for iOS internationalization.

## Custom Language Support

To add support for additional languages:

1. Add the new language code to `target_languages` in configuration
2. Create the corresponding `.lproj` directory
3. Run Phase 2/3 workflow for the new language

**Example: Adding Japanese support**

```bash
# Create directory
mkdir -p Resources/Localization/ja.lproj

# Copy baseline as starting point
cp Resources/Localization/zh-Hans.lproj/Localizable.strings \
   Resources/Localization/ja.lproj/Localizable.strings

# Check missing keys
python3 scripts/check_missing_localizations.py \
  Resources/Localization/zh-Hans.lproj/Localizable.strings \
  Resources/Localization/ja.lproj/Localizable.strings

# Translate and run swiftgen
swiftgen
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: iOS Build

on: [push, pull_request]

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check Localizations
        run: |
          python3 skills/ios-i18n-workflow/scripts/check_missing_localizations.py \
            Resources/Localization/zh-Hans.lproj/Localizable.strings \
            Resources/Localization/en.lproj/Localizable.strings

          if [ $? -ne 0 ]; then
            echo "❌ Missing translations detected"
            exit 1
          fi

      - name: Generate Swift Code
        run: swiftgen

      - name: Build App
        run: xcodebuild build -scheme MyApp
```

### Fastlane Example

```ruby
desc "Ensure translations are complete before building"
lane :check_localizations do
  baseline = "Resources/Localization/zh-Hans.lproj/Localizable.strings"
  targets = ["en", "zh-Hant", "ja"]

  targets.each do |lang|
    target_file = "Resources/Localization/#{lang}.lproj/Localizable.strings"

    result = sh("python3", "scripts/check_missing_localizations.py",
                baseline, target_file)

    if !result.success?
      UI.error("Missing translations in #{lang}")
      raise "Translation check failed"
    end
  end

  sh("swiftgen")
end
```

## Batch Translation Workflow

For translating multiple languages at once:

```bash
#!/bin/bash
# check-all-languages.sh

BASELINE="Resources/Localization/zh-Hans.lproj/Localizable.strings"
TARGET_LANGUAGES=("zh-Hant" "en" "ja" "ko")

TOTAL_MISSING=0

for lang in "${TARGET_LANGUAGES[@]}"; do
  echo "======================================"
  echo "Checking $lang..."
  echo "======================================"

  python3 scripts/check_missing_localizations.py \
    $BASELINE \
    Resources/Localization/$lang.lproj/Localizable.strings

  RESULT=$?
  TOTAL_MISSING=$((TOTAL_MISSING + RESULT))

  echo ""
done

echo "======================================"
echo "Summary: Total missing keys across all languages: $TOTAL_MISSING"
echo "======================================"

if [ $TOTAL_MISSING -gt 0 ]; then
  exit 1
fi
```

**Usage:**
```bash
chmod +x check-all-languages.sh
./check-all-languages.sh
```

## Automated Translation Script

For teams using translation services or APIs:

```bash
#!/bin/bash
# export-missing-keys.sh

BASELINE="Resources/Localization/zh-Hans.lproj/Localizable.strings"
TARGET="Resources/Localization/en.lproj/Localizable.strings"
OUTPUT_FILE="missing_keys_for_translation.txt"

# Run check script and capture output
python3 scripts/check_missing_localizations.py \
  $BASELINE \
  $TARGET | grep '"' | sed 's/.*"//' | sed 's/".*$//' > $OUTPUT_FILE

echo "Extracted $(wc -l < $OUTPUT_FILE) missing keys to $OUTPUT_FILE"
echo "Send this file to translators for translation"
```

## SwiftGen Configuration Reference

Ensure your `swiftgen.yml` is properly configured:

```yaml
strings:
  inputs:
    - Resources/Localization
  outputs:
    templateName: structured-swift5
    output: Generated/Strings.swift
    params:
      enumName: L10n
```

**Key points:**
- `inputs` should point to the directory containing `*.lproj` folders
- `enumName: L10n` matches the references in this skill
- Output path should be in your project's generated code directory

## Localization File Maintenance

### Periodic Cleanup Workflow

```bash
#!/bin/bash
# cleanup-localizations.sh

# 1. Check for unused keys (dry run first)
echo "Step 1: Checking for unused localizations..."
python3 scripts/clean_unused_localizations.py --dry-run

# 2. Prompt for confirmation
read -p "Continue with cleanup? (y/N) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
  # 3. Run actual cleanup
  python3 scripts/clean_unused_localizations.py

  # 4. Regenerate Swift code
  swiftgen

  echo "Cleanup complete!"
else
  echo "Cleanup cancelled"
fi
```

### Syncing with Development Team

When multiple developers add localizations:

1. **Before committing**: Run `check_missing_localizations.py` to ensure all languages are in sync
2. **After pulling**: Check if new keys were added by others
3. **Conflict resolution**: Resolve conflicts in `.strings` files manually, then run `swiftgen`

## Performance Optimization

For large projects with many localizations:

**Option 1: Incremental SwiftGen**
```bash
# Only regenerate strings (faster for large projects)
swiftgen config run --config swiftgen.yml --targets strings
```

**Option 2: Parallel Language Checking**
```bash
# Check all languages in parallel (requires GNU parallel or similar)
for lang in zh-Hant en ja ko; do
  echo "Checking $lang..." &
  python3 scripts/check_missing_localizations.py \
    Resources/Localization/zh-Hans.lproj/Localizable.strings \
    Resources/Localization/$lang.lproj/Localizable.strings &
done
wait
```

## Testing Localizations

### Unit Test Example

```swift
import XCTest

class LocalizationTests: XCTestCase {
    func testAllLocalizationsHaveKeys() {
        // Ensure all referenced keys exist in L10n
        // This test will fail at compile time if a key is missing
        _ = L10n.Common.ok
        _ = L10n.Market.back
        // ... add all critical keys
    }

    func testFormatStrings() {
        // Test format strings have correct parameters
        let stageText = "Phase 1"
        let statusText = "In Progress"
        let formatted = L10n.Challenge.Progress.stage(stageText, statusText)

        XCTAssertFalse(formatted.isEmpty)
        XCTAssertTrue(formatted.contains(stageText))
        XCTAssertTrue(formatted.contains(statusText))
    }
}
```
