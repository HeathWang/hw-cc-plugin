---
name: java-to-swift
description: Use when converting Java 1.8 classes to Swift 5.0+ Codable structs - handling type mapping, nullability, inheritance flattening, BaseReq exclusions, and property naming conventions.
---

# Java to Swift Conversion

## Overview

Converts Java 1.8 classes to Swift 5.0+ `struct` objects conforming to `Codable`. Output as markdown code blocks only — **never modify project files**.

## Core Constraint

**CRITICAL**: Output Swift `struct` definitions as markdown code blocks only. Do NOT modify, edit, or alter any project files.

## Type Mapping

| Java Type | Swift Type |
|-----------|------------|
| `int` / `Integer` | `Int` |
| `long` / `Long` | `Int64` |
| `float` / `Float` | `Float` |
| `double` / `Double` | `Double` |
| `boolean` / `Boolean` | `Bool` |
| `String` | `String` |
| `BigDecimal` / `decimal` | `Double` (default) or `String` (with `@BigDecimalToString`) |
| `Date` | `Date` |
| `Timestamp` | `TimeInterval` |
| `List<T>` | `[T]` |
| `Map<K,V>` | `[K: V]` |

## Nullability Rules

| Java Annotation | Swift Type |
|-----------------|------------|
| `@NonNull` / `@NotNull` | Non-optional (`String`) |
| No annotation / `@Nullable` | Optional (`String?`) |

**Default:** All properties are optional unless explicitly marked non-null.

## Naming Conventions

**Struct names:** PascalCase (`OrderDetails`, `UserProfile`, `PaymentRequest`)

**Property names:** ⚠️ KEEP IDENTICAL TO JAVA/SERVER-SIDE — preserves Codable serialization.

```swift
// ✅ Correct
struct OrderRequest: Codable {
    let orderId: String        // matches Java field name
    let total_amount: String?  // preserves snake_case
}
```

Swift's `Codable` maps property names directly to JSON keys — changing names breaks serialization.

## Inheritance Handling

Swift structs don't support inheritance. **Always flatten** the hierarchy:

1. Trace full inheritance chain — read all parent class files
2. **If any parent is `BaseReq`** → **EXCLUDE** all `BaseReq` properties (handled by network layer)
3. Combine all remaining properties from parent + child into one struct
4. Document property source with inline comments

```swift
struct OrderRequest: Codable {
    // From ApiRequest
    let userId: String

    // From OrderRequest
    let orderId: Int64

    // Note: BaseReq properties (token, timestamp) excluded — handled by network layer
}
```

## Documentation

Migrate Java comments to Swift using `///` triple-slash format:
- Preserve original language (Chinese stays Chinese, English stays English)
- Place comments immediately above each property
- For properties without Java comments, add brief descriptive comment

## Structure Requirements

All converted structs must:
- Be defined as `struct` (not `class`)
- Conform to `Codable` protocol
- Use `let` for all properties (immutable)
- Flatten all inherited properties into a single struct

## Step-by-Step Workflow

1. Analyze Java class — properties, annotations, types, inheritance
2. If inheritance detected → request/read parent class files
3. Handle `BaseReq` exclusion if applicable
4. Create Swift struct with `Codable` conformance
5. Apply type mapping (including `@BigDecimalToString`)
6. Apply nullability (`@NonNull` → non-optional, else optional)
7. Use `let` for all properties
8. Keep property names identical to Java/server-side
9. Migrate comments with `///` preserving original language

## Validation Checklist

- [ ] `@NonNull`/`@NotNull` properties are non-optional
- [ ] All other properties are optional (`?`)
- [ ] Struct conforms to `Codable`
- [ ] All properties use `let`
- [ ] Inheritance detected and parent classes analyzed
- [ ] All inherited properties flattened into single struct
- [ ] `BaseReq` properties excluded if applicable
- [ ] Property names identical to server-side model
- [ ] Output is markdown code block only (no file modifications)
