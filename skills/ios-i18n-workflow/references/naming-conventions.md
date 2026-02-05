# iOS I18n Naming Conventions

Complete reference for localization key naming and L10n code reference rules in SwiftGen-based iOS projects.

## Localization Key Naming Convention

**Domain-like naming convention with up to 3-level hierarchy, all in lowercase.**

### Key Rules

**CRITICAL:** All key segments MUST start with a letter (a-z), NOT a number.

- Use only lowercase letters, numbers (after the first character of each segment), dots (`.`)
- Maximum 3 levels of hierarchy
- Use domain-like naming for clarity

### Valid Examples

```
common.ok
market.back
market.header.name
trade.confirm.title
challenge.status.inprogress.full
```

### Invalid Keys (DO NOT USE)

| Invalid Key | Reason | Valid Alternative |
|-------------|--------|-------------------|
| `3dsecure.confirm` | First segment starts with a number | `secure3d.confirm` |
| `symboldetail.24h.high` | Middle segment starts with a number | `symboldetail.twenty4h.high` |
| `2fa.enabled` | Starts with a number | `twofa.enabled` |
| `secure.3d.confirm` | Any segment starts with a number | `secure.threed.confirm` |

### Fix Strategy

Spell out numbers or rephrase:
- `3dsecure` → `secure3d` or `threedsecure`
- `24h` → `twenty4h` or `daily`
- `2fa` → `twofa` or `twofactorauth`

## L10n Code Reference Rules

When referencing localized strings in code using `L10n`, SwiftGen applies specific transformation rules.

### Transformation Rules

**All keys except the last level:**
- Capitalize ONLY the first letter (Title Case), NOT PascalCase

**Last-level key:**
- If it contains underscores (snake_case), convert to camelCase
- If it's a single lowercase word, keep it as-is
- Compound words without underscores stay lowercase

### Examples

| Localization Key | L10n Code Reference | Transformation Notes |
|-----------------|-------------------|---------------------|
| `common.ok` | `L10n.Common.ok` | Single level → Title Case |
| `market.back` | `L10n.Market.back` | Two levels → Both Title Case |
| `market.header.name` | `L10n.Market.Header.name` | Three levels → All Title Case |
| `addbalance.flashexchange.subtitle` | `L10n.Addbalance.Flashexchange.subtitle` | Compound word (flashexchange → Flashexchange, NOT FlashExchange) |
| `challenge.status.inprogress.full` | `L10n.Challenge.Status.Inprogress.full` | Nested keys (inprogress → Inprogress, NOT InProgress) |
| `paybridge.error.missingproductid` | `L10n.Paybridge.Error.missingproductid` | Compound key stays lowercase |
| `futuresrecords.header.amount_usdt` | `L10n.Futuresrecords.Header.amountUsdt` | **snake_case → camelCase** |

### Last-Level snake_case → camelCase Conversion

**IMPORTANT:** SwiftGen automatically converts **last-level** keys from snake_case to camelCase.

#### Conversion Rules

- If the last-level key contains underscores (`_`), convert to camelCase
- Each word after the first is capitalized: `word_one_two` → `wordOneTwo`
- If the last-level key has no underscores, it stays as-is

#### Examples

| Localization Key | Last-Level Conversion | Final L10n Reference |
|-----------------|---------------------|---------------------|
| `futuresrecords.header.amount_usdt` | `amount_usdt` → `amountUsdt` | `L10n.Futuresrecords.Header.amountUsdt` |
| `withdraw.format.fee_amount` | `fee_amount` → `feeAmount` | `L10n.Withdraw.Format.feeAmount` |
| `trade.confirm.order_id` | `order_id` → `orderId` | `L10n.Trade.Confirm.orderId` |
| `market.header.name` | `name` → `name` (no change) | `L10n.Market.Header.name` |

#### Common Mistake

```swift
// ❌ WRONG - Using snake_case directly
label.text = L10n.Futuresrecords.Header.amount_usdt

// ✅ CORRECT - Using camelCase
label.text = L10n.Futuresrecords.Header.amountUsdt
```

## Format Strings (with Parameters)

**When localization strings contain format specifiers (`%@`, `%d`, `%%`, etc.), SwiftGen generates a FUNCTION instead of a static property.**

### How Format Strings Work

Given this localization entry:
```
"challenge.progress.stage" = "第%@阶段: %@";
```

SwiftGen generates:
```swift
public static func stage(_ p1: Any, _ p2: Any) -> String {
  return L10n.tr("Localizable", "challenge.progress.stage", String(describing: p1), String(describing: p2), fallback: "Phase %@: %@")
}
```

### Usage Examples

#### CORRECT Usage
```swift
// Call the generated function directly with parameters
tag.text = L10n.Challenge.Progress.stage(
    L10n.Challenge.Progress.Number.one,
    L10n.Challenge.Status.inprogress
)
```

#### INCORRECT Usage
```swift
// DO NOT use String(format:) - L10n.Challenge.Progress.stage is a function, not a string!
tag.text = String(format: L10n.Challenge.Progress.stage, ...) // ❌ WRONG
```

### Format String Examples

| Localization Entry | Generated Type | Correct Usage | Note |
|-------------------|---------------|---------------|------|
| `"common.ok" = "确定";` | Static property | `L10n.Common.ok` | No format specifiers → static property |
| `"challenge.progress.stage" = "第%@阶段: %@";` | Function | `L10n.Challenge.Progress.stage(phaseText, statusText)` | Multiple %@ parameters |
| `"futurestrading.orderbook.fundingrate" = "Funding Rate (%dh)";` | Function | `L10n.Futurestrading.Orderbook.fundingrate(8)` | %d integer parameter |
| `"futurestrading.operation.price" = "价格(%@)";` | Function | `L10n.Futurestrading.Operation.price("USDT")` | Single %@ parameter |
| `"withdraw.format.fee" = "手续费: %@ %@";` | Function | `L10n.Withdraw.Format.fee(amountText)` | Multiple %@ parameters |
| `"asset.header.approximate" = "≈%@ %@";` | Function | `L10n.Asset.Header.approximate(value, symbol)` | Multiple %@ parameters |
| `"withdraw.validation.amountbelowminimum" = "Minimum withdrawal: %@ USDT";` | Function | `L10n.Withdraw.Validation.amountbelowminimum(minAmount)` | %@ parameter in English string |

### How to Identify Format Strings

Check if the localization string contains any format specifiers:
- `%@` - Any object (String, etc.)
- `%d` / `%i` - Integer
- `%f` - Float/Double
- `%.0f` / `%.2f` - Formatted float
- `%%` - Literal percent sign (does NOT create a parameter)

If format specifiers exist (except `%%`), use the function call syntax instead of property access.

### Complete Example

#### Before Internationalization (hardcoded strings)
```swift
button.setTitle("确定", for: .normal)
label.text = "名称"
statusLabel.text = "第1阶段: 进行中"
```

#### After Internationalization (using L10n)
```swift
// Static property (no format specifiers)
button.setTitle(L10n.Common.ok, for: .normal)
label.text = L10n.Market.Header.name

// Function call (with format specifiers)
statusLabel.text = L10n.Challenge.Progress.stage(
    L10n.Challenge.Progress.Number.one,
    L10n.Challenge.Status.inprogress
)
```

## Quick Reference Card

### Key Naming Checklist
- [ ] All segments start with a letter (not a number)
- [ ] Maximum 3 levels of hierarchy
- [ ] Lowercase letters, numbers, and dots only
- [ ] Domain-like naming for clarity

### L10n Reference Transformation
- [ ] All levels except last: Title Case
- [ ] Last level with underscores: camelCase
- [ ] Last level without underscores: lowercase

### Format String Usage
- [ ] Check for `%@`, `%d`, `%f` format specifiers
- [ ] If present: Use function call syntax
- [ ] If absent: Use property access syntax
- [ ] Never use `String(format:)` with L10n functions

## Troubleshooting

### Compilation Error: "Cannot convert value of type '() -> String' to type 'String'"

**Cause:** You're treating a format function as a property.

**Solution:**
```swift
// ❌ WRONG
label.text = L10n.Challenge.Progress.stage

// ✅ CORRECT
label.text = L10n.Challenge.Progress.stage(param1, param2)
```

### Runtime Error: L10n Reference Not Found

**Cause:** Wrong case in L10n reference (e.g., using snake_case instead of camelCase).

**Solution:**
```swift
// ❌ WRONG
label.text = L10n.Futuresrecords.Header.amount_usdt

// ✅ CORRECT
label.text = L10n.Futuresrecords.Header.amountUsdt
```

### Key Not Found in Localizable.strings

**Cause:** Typo in key name or key doesn't exist in baseline file.

**Solution:**
1. Verify key exists in `zh-Hans.lproj/Localizable.strings`
2. Check key spelling and case (all lowercase)
3. Run `swiftgen` to regenerate code

## Best Practices

1. **Be consistent** with domain naming across the app
2. **Use descriptive keys** that reflect the UI hierarchy
3. **Group related keys** using the 3-level hierarchy
4. **Avoid abbreviations** unless they're widely understood
5. **Test format strings** with actual parameter values
6. **Run swiftgen** immediately after updating `.strings` files

## Migration Guide

### Converting Old Keys to New Convention

If you have existing keys that don't follow the naming convention:

```bash
# Example migration
"3dsecure.title" = "3D Secure";     # ❌ Old
"secure3d.title" = "3D Secure";     # ✅ New

"symboldetail.24h.high" = "24H High";   # ❌ Old
"symboldetail.daily.high" = "24H High"; # ✅ New
```

**Migration steps:**
1. Rename keys in `Localizable.strings`
2. Update all `L10n` references in code
3. Run `swiftgen` to regenerate
4. Test all affected screens
