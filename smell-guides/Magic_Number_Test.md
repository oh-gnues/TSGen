# Magic Number Test

**Definition**  
A test uses **unexplained numeric (or string) literals**, obscuring intent and harming readability.

---

## Symptoms
- Raw numbers like `42`, `0.01`, `1000` appear directly inside `assert*` or setup code.  
- Another developer must search production code or domain docs to understand the value’s meaning.  
- Multiple tests repeat the same literal, risking inconsistency if the requirement changes.

---

## Why It’s Bad
Readers cannot see *why* the literal is expected, causing cognitive load and hidden coupling between test and implementation. If the domain value changes, every duplicated literal must be updated—an error‑prone chore.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Replace literals with a named constant** | `private static final` constants document intent and centralise changes. |
| 2 | **Reference production constants when possible** | Avoid drift by using the same source of truth. |
| 3 | **Add a descriptive assertion message** | Failure output then conveys the domain meaning, not just numbers. |
| 4 | **Verify coverage parity** | After refactor, ensure test coverage remains unchanged in CI. |

---

## Test Smell Example
```java
@Test
public void capacity_shouldEqual50_afterInitialization() {
    FixedSizeList<String> list = new FixedSizeList<>();
    list.add("hello");

    // ❌  Magic numbers hide intent
    assertEquals(50, list.capacity());
}
```

---

## Refactored Example
```java
// ✅  Named constants document intent
private static final int DEFAULT_CAPACITY = 50;

@Test
public void capacity_shouldMatch_defaultAfterInitialization() {
    FixedSizeList<String> list = new FixedSizeList<>();
    list.add("hello");

    assertEquals("Capacity should match DEFAULT_CAPACITY",
                 DEFAULT_CAPACITY, list.capacity());
}
```