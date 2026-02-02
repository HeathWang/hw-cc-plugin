# Java to Swift Conversion Workflow

## Overview
This document outlines the workflow for converting Java 1.8 classes to Swift 5.0+ struct objects.

## Core Rules

### 🚫 File Modification Restriction
- **CRITICAL**: You must NOT modify, edit, or alter any project files
- **Output**: Output `Swift`  struct as markdown code

## Version Requirements
- **Source**: Java 1.8
- **Target**: Swift 5.0+

## Conversion Rules

### 1. Type Mapping
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

#### Special Annotation Handling

**`@BigDecimalToString` Annotation:**
- When `BigDecimal` or `decimal` is annotated with `@BigDecimalToString`, convert to `String` instead of `Double`
- This preserves exact decimal precision required for financial calculations
- Apply nullability rules as normal (optional vs non-optional)


### 2. Nullability Rules
| Java Annotation | Swift Type |
|-----------------|------------|
| `@NonNull` / `@NotNull` | Non-optional (e.g., `String`) |
| No annotation / `@Nullable` | Optional (e.g., `String?`) |

**Default:** All properties are optional unless explicitly marked as non-null.

### 3. Naming Convention Rules

#### Struct Names
Follow Swift's standard naming conventions:
- Use PascalCase for struct names
- Use descriptive, clear names that convey meaning
- Example: `OrderDetails`, `UserProfile`, `PaymentRequest`

#### Property Names
**⚠️ CRITICAL RULE:** Property names MUST match the server-side model field names exactly to ensure Codable serialization/deserialization works correctly.

| Element | Convention | Example |
|---------|------------|---------|
| Property Names | **Keep identical to Java/server-side** | If Java has `orderId`, Swift must use `orderId` |
| Property Names | **Keep identical to Java/server-side** | If Java has `user_id`, Swift must use `user_id` |
| Property Names | **Do NOT convert naming styles** | Do NOT change `user_id` to `userId` |

**Rationale:** Swift's `Codable` protocol maps property names directly to JSON keys. Changing property names will break serialization unless custom `CodingKeys` are added, which adds unnecessary complexity.

**Examples:**

✅ **Correct:**
```swift
struct OrderRequest: Codable {
    let orderId: String        // Matches Java field name
    let total_amount: String?  // Matches Java field name (even with underscore)
    let userID: String         // Matches Java field name (preserves capitalization)
}
```

**Note:** Only struct/type names follow Swift conventions (PascalCase). All property names preserve the exact naming from the server-side model.

### 4. Inheritance Handling Rules

When a Java class uses inheritance (`extends`):

**Step 1: Analyze Inheritance Chain**
- Identify the parent class(es)
- Read and analyze all properties from parent classes
- Trace the full inheritance hierarchy
- **Check if any parent class is `BaseReq`**

**Step 2: Flatten Properties**
Since Swift structs don't support inheritance, flatten the hierarchy by:
- Combining all properties from parent and child classes into a single struct
- Maintaining all properties from the inheritance chain
- Preserving the type mappings and nullability rules for all properties
- **EXCEPTION: If the inheritance chain includes `BaseReq`, exclude all properties from `BaseReq`**

**Step 3: Property Documentation**
Migrate property comments from Java to Swift, adapting them to Swift's documentation standards:

**Documentation Rules:**
- Use Swift's triple-slash (`///`) documentation format
- Place documentation comments immediately above each property
- Preserve the original meaning and intent from Java comments
- Adapt Java doc tags to Swift documentation conventions:
  - Java `@param` → Not applicable (properties don't have parameters)
  - Java `@return` → Not applicable (properties don't return values)
  - Keep descriptive text and business logic explanations
- Use clear, concise language appropriate for Swift developers

**Best Practices:**
- If a Java property has no comment, add a brief descriptive comment in Swift
- For complex business logic, preserve detailed explanations
- Use Swift markdown formatting for better readability (`-`, `*`, code blocks)
- Keep documentation concise but informative

**Important:** Always request or read parent class files when inheritance is detected.

#### Special Case: `BaseReq` Inheritance

**Rule:** If any parent class in the inheritance chain is `BaseReq`, **DO NOT** include properties from `BaseReq` in the Swift conversion.

**Reason:** The underlying network request layer already handles `BaseReq` parameters automatically.

**Example:**
```java
// Java class hierarchy
public class BaseReq {
    private String token;
    private Long timestamp;
}

public class ApiRequest extends BaseReq {
    @NonNull
    private String userId;
}

public class OrderRequest extends ApiRequest {
    @NonNull
    private Long orderId;
}
```

**Swift Conversion (Correct):**
```swift
struct OrderRequest: Codable {
    // From ApiRequest
    let userId: String
    
    // From OrderRequest
    let orderId: Int64
    
    // Note: BaseReq properties (token, timestamp) are excluded
    // as they are handled by the network layer
}
```

**Swift Conversion (Incorrect - Don't do this):**
```swift
struct OrderRequest: Codable {
    // ❌ Don't include these from BaseReq
    let token: String?
    let timestamp: String?
    
    let userId: String
    let orderId: String
}
```

### 5. Structure Requirements
All converted objects must:
- Be defined as `struct` (not `class`)
- Conform to `Codable` protocol
- Use `let` for all properties (immutable)
- Flatten all inherited properties into a single struct

## Conversion Examples


### Example 2: Inheritance Conversion
**Java (1.8):**
```java
public class BaseEntity {
    @NonNull
    private Long id;
    
    private Date createdAt;
}

public class Order extends BaseEntity {
    @NonNull
    private Long orderId;
    
    private BigDecimal totalAmount;
    
    @NonNull
    private String currency;
}
```

**Swift (5.0+):**
```swift
struct Order: Codable {
    // Properties from BaseEntity
    let id: Int64
    let createdAt: Date?
    
    // Properties from Order
    let orderId: Int64
    let totalAmount: Double?
    let currency: String
}
```

## Step-by-Step Workflow

1. **Analyze Java Class**
   - Identify all properties and their types
   - Check for nullability annotations (`@NonNull`, `@NotNull`)
   - Note `long` and `decimal` types
   - **Check for inheritance (`extends`) keyword**
   - **If inheritance exists, request or read parent class files**

2. **Handle Inheritance (if applicable)**
   - Read all parent classes in the inheritance chain
   - Collect all properties from parent classes
   - Note the origin of each property for documentation

3. **Create Swift Struct**
   - Define struct with `Codable` conformance
   - **Apply Swift naming conventions to type and property names**
   - Flatten all inherited properties into the struct

4. **Apply Type Conversion**
   - Convert types according to mapping table
   - Convert collections (`List` → `Array`, `Map` → `Dictionary`)

5. **Apply Nullability Rules**
   - Properties with `@NonNull`/`@NotNull` → non-optional
   - Properties without annotations → optional (add `?`)
   - Use `let` for all properties

6. **Apply Naming Conventions**
   - Convert property names to proper Swift style
   - Handle acronyms correctly (capitalize as words)
   - Ensure boolean properties read naturally

## Validation Checklist
- [ ] Properties with `@NonNull`/`@NotNull` are non-optional
- [ ] All other properties are optional (have `?`)
- [ ] Struct conforms to `Codable`
- [ ] All properties use `let` instead of `var`
- [ ] **Inheritance detected and parent classes analyzed**
- [ ] **All inherited properties flattened into single struct**
- [ ] **Swift naming conventions applied (camelCase, acronym handling)**
- [ ] **Property names follow Swift style guidelines**

## Notes
- When inheritance is detected but parent class is not provided, explicitly request the parent class files
- Document the source of properties from parent classes with comments for clarity
- Maintain consistent naming style throughout the converted Swift code
- Prioritize readability and Swift idioms over literal Java translation