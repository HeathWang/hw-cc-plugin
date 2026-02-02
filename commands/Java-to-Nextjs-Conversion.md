# Java to Next.js TypeScript Conversion Workflow

## Overview
This document outlines the workflow for converting Java 1.8 classes to Next.js TypeScript interface definitions.

## Core Rules

### 🚫 File Modification Restriction
- **CRITICAL**: You must NOT modify, edit, or alter any project files
- **Output**: Output TypeScript `interface` definitions as markdown code

## Version Requirements
- **Source**: Java 1.8
- **Target**: TypeScript 5.0+ (Next.js 14+)

## Conversion Rules

### 1. Type Mapping
| Java Type | TypeScript Type |
|-----------|-----------------|
| `int` / `Integer` | `number` |
| `long` / `Long` | `number` |
| `float` / `Float` | `number` |
| `double` / `Double` | `number` |
| `boolean` / `Boolean` | `boolean` |
| `String` | `string` |
| `BigDecimal` / `decimal` | `string` (default) or `number` (with `@BigDecimalToNumber`) |
| `Date` | `string` (ISO 8601 format) |
| `Timestamp` | `number` (Unix timestamp) or `string` (ISO 8601) |
| `List<T>` | `T[]` or `Array<T>` |
| `Map<K,V>` | `Record<K, V>` or `{ [key: K]: V }` |
| `Object` / `JSONObject` | `Record<string, any>` or specific interface |

#### Special Annotation Handling

**`@BigDecimalToNumber` Annotation:**
- When `BigDecimal` or `decimal` is annotated with `@BigDecimalToNumber`, convert to `number` instead of `string`
- **Default behavior**: `BigDecimal` → `string` (preserves precision for financial calculations)
- This annotation indicates the value range is safe for JavaScript numbers
- Apply nullability rules as normal (optional vs required)

**`@TimestampFormat` Annotation:**
- `@TimestampFormat("unix")` → `number` (Unix timestamp in milliseconds)
- `@TimestampFormat("iso")` → `string` (ISO 8601 date string)
- **Default**: `string` (ISO 8601)

### 2. Nullability Rules
| Java Annotation | TypeScript Type |
|-----------------|-----------------|
| `@NonNull` / `@NotNull` | Required field (e.g., `name: string`) |
| No annotation / `@Nullable` | Optional field (e.g., `name?: string`) |

**Default:** All properties are optional unless explicitly marked as non-null.

### 3. Naming Convention Rules

#### Interface Names
Follow TypeScript/Next.js naming conventions:
- Use PascalCase for interface names
- Use descriptive, clear names that convey meaning
- Suffix response interfaces with `Data` or `Response`
- Suffix request interfaces with `Request` or `Params`
- Examples: `SaveEmailData`, `UserProfileResponse`, `LoginRequest`

#### Property Names
**⚠️ CRITICAL RULE:** Property names MUST match the server-side API field names exactly to ensure proper serialization/deserialization.

| Element | Convention | Example |
|---------|------------|---------|
| Property Names | **Keep identical to Java/server-side** | If Java has `userId`, TypeScript must use `userId` |
| Property Names | **Keep identical to Java/server-side** | If Java has `user_id`, TypeScript must use `user_id` |
| Property Names | **Do NOT convert naming styles** | Do NOT change `user_id` to `userId` |
| Property Names | **Preserve camelCase or snake_case** | Match the exact API response format |

**Rationale:** API responses use specific naming conventions. Changing property names will break data mapping unless custom transformers are added, which adds unnecessary complexity.

**Examples:**

✅ **Correct:**
```typescript
interface SaveEmailData {
  inviteCode: string;           // Matches API field name
  order: number;                // Matches API field name
  obtainBitsCount: number;      // Matches API field name
  invite_url?: string;          // Matches API field name (preserves snake_case)
}
```

❌ **Incorrect:**
```typescript
interface SaveEmailData {
  InviteCode: string;           // ❌ Changed to PascalCase
  Order: number;                // ❌ Changed to PascalCase
  obtain_bits_count: number;    // ❌ Changed to snake_case
  inviteUrl?: string;           // ❌ Changed from snake_case to camelCase
}
```

**Note:** Only interface/type names follow TypeScript conventions (PascalCase). All property names preserve the exact naming from the API contract.

### 4. Inheritance Handling Rules

When a Java class uses inheritance (`extends`):

**Step 1: Analyze Inheritance Chain**
- Identify the parent class(es)
- Read and analyze all properties from parent classes
- Trace the full inheritance hierarchy
- **Check if any parent class is `BaseReq` or `BaseResponse`**

**Step 2: Use TypeScript Interface Extension**
Unlike Swift structs, TypeScript interfaces support inheritance using the `extends` keyword:

**Option A: Interface Extension (Recommended)**
```typescript
interface BaseEntity {
  id: number;
  createdAt?: string;
}

interface Order extends BaseEntity {
  orderId: number;
  totalAmount?: string;
  currency: string;
}
```

**Option B: Flattened Interface (Alternative)**
When the inheritance structure is complex or when you want a single, self-contained interface:
```typescript
interface Order {
  // Properties from BaseEntity
  id: number;
  createdAt?: string;
  
  // Properties from Order
  orderId: number;
  totalAmount?: string;
  currency: string;
}
```

**Recommendation:** Use Option A (interface extension) when:
- The parent interface is reused across multiple child interfaces
- The inheritance hierarchy is clean and logical
- You want to maintain type relationships

Use Option B (flattened) when:
- The interface is used independently
- You want to avoid interface dependencies
- The parent properties are minimal

**Step 3: Property Documentation**
Migrate property comments from Java to TypeScript, adapting them to JSDoc standards:

**Documentation Rules:**
- Use JSDoc (`/** */`) documentation format for interfaces
- Use single-line comments (`//`) for inline property descriptions
- Place documentation comments immediately above each property
- Preserve the original meaning and intent from Java comments
- **⚠️ CRITICAL: Keep the original language - DO NOT translate comments**
  - If Java comments are in English, keep TypeScript comments in English
  - If Java comments are in Chinese, keep TypeScript comments in Chinese
  - Preserve the exact terminology and phrasing from the original
- Adapt Java doc tags to JSDoc conventions:
  - Java `@param` → `@property` in TypeScript
  - Java `@return` → Not applicable for interfaces
  - Keep descriptive text and business logic explanations

**Examples:**

**Java (中文注释):**
```java
public class Order {
    /**
     * 订单唯一标识符
     */
    @NonNull
    private String orderId;
    
    // 订单总金额（美元）
    private BigDecimal totalAmount;
}
```

**TypeScript (保持中文):**
```typescript
interface Order {
  /**
   * 订单唯一标识符
   */
  orderId: string;
  
  // 订单总金额（美元）
  totalAmount?: string;
}
```

**Important:** Always request or read parent class files when inheritance is detected.

#### Special Case: `BaseReq` / `BaseResponse` Inheritance

**Rule:** If any parent class in the inheritance chain is `BaseReq` or `BaseResponse`, **DO NOT** include properties from these base classes in the TypeScript conversion.

**Reason:** 
- `BaseReq` properties (like `token`, `timestamp`, `deviceId`) are handled by HTTP interceptors/middleware
- `BaseResponse` properties (like `code`, `message`, `success`) are handled by the API response wrapper layer

**Example:**
```java
// Java class hierarchy
public class BaseResponse<T> {
    private Integer code;
    private String message;
    private Boolean success;
    private T data;
}

public class ApiResponse extends BaseResponse<UserData> {
    // Inherits code, message, success, data
}

public class UserData {
    @NonNull
    private Long userId;
    private String email;
}
```

**TypeScript Conversion (Correct):**
```typescript
// Only convert the data payload, not the wrapper
interface UserData {
  userId: number;
  email?: string;
}

// If you need the full response structure:
interface ApiResponse<T = any> {
  code: number;
  message: string;
  success: boolean;
  data: T;
}

// Usage
type UserResponse = ApiResponse<UserData>;
```

### 5. Structure Requirements
All converted interfaces must:
- Be defined as `interface` (not `type` or `class`)
- Use clear, descriptive names with appropriate suffixes
- Use the correct nullability markers (`?` for optional)
- Follow consistent naming conventions
- Export interfaces when they're used across files

### 6. Additional TypeScript Features

#### Union Types
For properties with multiple possible types:
```typescript
interface PaymentData {
  amount: string | number;  // Can be string for precision or number
  status: 'pending' | 'completed' | 'failed';  // Literal union type
}
```

#### Generic Types
For reusable response structures:
```typescript
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

// Usage
type UserList = PaginatedResponse<UserData>;
```

#### Index Signatures
For dynamic property names:
```typescript
interface DynamicConfig {
  [key: string]: string | number | boolean;
}
```

## Step-by-Step Workflow

1. **Analyze Java Class**
   - Identify all properties and their types
   - Check for nullability annotations (`@NonNull`, `@NotNull`)
   - Note special types (`BigDecimal`, `Date`, `Timestamp`)
   - **Check for inheritance (`extends`) keyword**
   - **If inheritance exists, request or read parent class files**

2. **Handle Inheritance (if applicable)**
   - Read all parent classes in the inheritance chain
   - Decide between interface extension or flattening
   - If extending, create parent interfaces first
   - If flattening, collect all properties from parent classes
   - **Exclude properties from `BaseReq`/`BaseResponse` if present**

3. **Create TypeScript Interface**
   - Define interface with appropriate name and suffix
   - Choose between extension or flattening approach
   - Use PascalCase for interface names

4. **Apply Type Conversion**
   - Convert types according to mapping table
   - Handle special cases (`BigDecimal`, `Date`, `Timestamp`)
   - Convert collections (`List` → `Array`, `Map` → `Record`)
   - Apply generic types where appropriate

5. **Apply Nullability Rules**
   - Properties with `@NonNull`/`@NotNull` → required (no `?`)
   - Properties without annotations → optional (add `?`)

6. **Preserve Naming Conventions**
   - **Keep property names exactly as they appear in Java/API**
   - Do NOT convert between camelCase and snake_case
   - Do NOT change capitalization
   - Ensure compatibility with API contract

7. **Add Documentation**
   - Migrate relevant comments from Java
   - Use JSDoc for complex interfaces
   - Use inline comments for property descriptions

## Validation Checklist
- [ ] Properties with `@NonNull`/`@NotNull` are required (no `?`)
- [ ] All other properties are optional (have `?`)
- [ ] Interface uses PascalCase naming
- [ ] **Property names match API contract exactly**
- [ ] **Inheritance detected and parent classes analyzed**
- [ ] **Correct approach chosen (extension vs flattening)**
- [ ] **`BaseReq`/`BaseResponse` properties excluded if applicable**
- [ ] Type mappings are correct (especially `BigDecimal`, `Date`, arrays)
- [ ] Generic types used where appropriate
- [ ] Documentation migrated from Java comments
