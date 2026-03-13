---
name: java-to-nextjs
description: Use when converting Java 1.8 classes to Next.js TypeScript interface definitions - handling type mapping, nullability, inheritance, naming conventions, and BaseReq/BaseResponse exclusions.
---

# Java to Next.js TypeScript Conversion

## Overview

Converts Java 1.8 classes to TypeScript 5.0+ interface definitions for Next.js 14+. Output as markdown code blocks only — **never modify project files**.

## Core Constraint

**CRITICAL**: Output TypeScript `interface` definitions as markdown code blocks only. Do NOT modify, edit, or alter any project files.

## Type Mapping

| Java Type | TypeScript Type |
|-----------|-----------------|
| `int` / `Integer` / `long` / `Long` | `number` |
| `float` / `Float` / `double` / `Double` | `number` |
| `boolean` / `Boolean` | `boolean` |
| `String` | `string` |
| `BigDecimal` / `decimal` | `string` (default) or `number` (with `@BigDecimalToNumber`) |
| `Date` | `string` (ISO 8601) |
| `Timestamp` | `number` (unix) or `string` (ISO, with `@TimestampFormat`) |
| `List<T>` | `T[]` |
| `Map<K,V>` | `Record<K, V>` |
| `Object` / `JSONObject` | `Record<string, any>` |

## Nullability Rules

| Java Annotation | TypeScript |
|-----------------|------------|
| `@NonNull` / `@NotNull` | Required field (`name: string`) |
| No annotation / `@Nullable` | Optional field (`name?: string`) |

**Default:** All properties are optional unless explicitly marked non-null.

## Naming Conventions

**Interface names:** PascalCase with meaningful suffixes (`SaveEmailData`, `LoginRequest`, `UserProfileResponse`)

**Property names:** ⚠️ KEEP IDENTICAL TO JAVA/API — do NOT convert between camelCase and snake_case.

```typescript
// ✅ Correct
interface SaveEmailData {
  inviteCode: string;     // matches API
  invite_url?: string;    // preserves snake_case
}

// ❌ Wrong
interface SaveEmailData {
  InviteCode: string;     // changed to PascalCase
  inviteUrl?: string;     // changed snake_case to camelCase
}
```

## Inheritance Handling

1. Identify parent classes and trace the full chain
2. **If parent is `BaseReq` or `BaseResponse`** → **EXCLUDE** all their properties (handled by HTTP middleware)
3. Choose approach:
   - **Interface Extension (recommended):** use `extends` when parent is reused across multiple children
   - **Flattened Interface:** copy all properties into one interface when standalone

## Documentation

Migrate Java comments to TypeScript preserving original language:
- Chinese comments → keep Chinese
- English comments → keep English
- Use JSDoc (`/** */`) for interfaces, inline `//` for properties

## Step-by-Step Workflow

1. Analyze Java class — properties, annotations, types, inheritance
2. If inheritance exists → read parent class files
3. Handle `BaseReq`/`BaseResponse` exclusion if applicable
4. Create interface with PascalCase name
5. Apply type mapping (including `@BigDecimalToNumber`, `@TimestampFormat`)
6. Apply nullability (`@NonNull` → required, else optional)
7. Preserve property names exactly as in API
8. Migrate comments preserving original language

## Validation Checklist

- [ ] `@NonNull`/`@NotNull` properties are required (no `?`)
- [ ] All other properties are optional (`?`)
- [ ] Interface uses PascalCase naming
- [ ] Property names match API contract exactly
- [ ] Inheritance detected and parent classes analyzed
- [ ] `BaseReq`/`BaseResponse` properties excluded if applicable
- [ ] Type mappings correct (especially `BigDecimal`, `Date`, arrays)
- [ ] Documentation migrated in original language
- [ ] Output is markdown code block only (no file modifications)
