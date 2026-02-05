# Translation Guidelines

Guidelines for translating iOS app localization strings across multiple languages.

## General Principles (All Languages)

- **Preserve all placeholders** (`%@`, `%d`, `%lld`) exactly as in source
- **Consider UI context** (button labels should be brief and action-oriented)
- **Maintain consistency** with existing translations
- **Preserve file structure**, MARK comments, and formatting

## Language-Specific Guidelines

### English (en)

- Use professional, concise language
- For financial/trading apps, use industry-standard terminology
- Use American English spelling conventions

**Examples:**
- "Color" not "Colour"
- "Center" not "Centre"
- "Organization" not "Organisation"

### Traditional Chinese (zh-Hant)

- Convert Simplified Chinese characters to Traditional Chinese
- Maintain terminology consistency
- Consider regional usage differences if applicable

**Common conversions:**
- "资产" → "資產"
- "交易" → "交易"
- "确认" → "確認"

### Other Languages

- Follow locale-specific conventions
- Consider cultural context and idioms
- Consult native speakers when possible

## Format String Translation

When translating strings with format specifiers, preserve placeholders exactly:

**Source (zh-Hans):**
```
"challenge.progress.stage" = "第%@阶段: %@";
```

**English translation:**
```
"challenge.progress.stage" = "Phase %@: %@";
```

**Key points:**
- Keep `%@`, `%d`, `%lld` in the same order
- Maintain the same number of placeholders
- Don't localize the format specifiers themselves

## UI Context Considerations

### Button Labels
- Keep brief (1-2 words when possible)
- Use action-oriented language
- **Examples:** "Confirm", "Cancel", "Submit"

### Error Messages
- Be clear and specific
- Provide actionable guidance when possible
- **Examples:** "Network error. Please check your connection."

### Long Text
- Maintain readability
- Consider line breaks and UI constraints
- Test in actual interface when possible

## Common Translation Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Translating placeholders like %@ | Breaks code functionality | Preserve placeholders exactly |
| Word-for-word translation | Loses meaning and context | Translate meaning, not words |
| Ignoring UI space constraints | Text gets truncated in UI | Keep translations similar in length |
| Mixing terminology | Confuses users | Use consistent terminology |
| Forgetting to update all languages | Creates missing keys | Update all target languages together |

## Quality Checklist

Before considering translation complete:

- [ ] All placeholders preserved exactly
- [ ] Terminology is consistent with existing translations
- [ ] Text fits UI constraints (test if possible)
- [ ] Cultural context is appropriate
- [ ] Spelling and grammar verified
- [ ] Format strings tested with actual parameters

## Professional Translation

For production apps, consider:
- Professional translation services
- Native speaker review
- Localization testing with native users
- Context documentation for translators

**Providing context to translators:**
```markdown
## Screen: Login
## Context: User sees this after entering invalid credentials

"login.error.invalid" = "Invalid username or password";

## Notes:
- This appears in a red error banner
- Keep it brief (it's a small banner)
- Should be polite but clear
```
