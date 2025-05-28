# Eager Test

**Definition**  
A single test method exercises **multiple independent behaviours**. When it fails, you cannot immediately tell *which* behaviour broke, violating the single‑responsibility principle for tests.

---

## Symptoms
- A test that calls *create*, *update*, *delete* all in one method.  
- Long sequences of `assert*` statements verifying unrelated state transitions.  
- CI reports one red test, but you must read the source to locate the failing step.

---

## Why It’s Bad
Eager Tests blur intent and inflate debugging time. They discourage clear *Given‑When‑Then* structure, and as features grow they become monolithic, fragile, and hard to maintain.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Split by behaviour** | One method per scenario keeps failures local and names expressive. |
| 2 | **Extract shared setup** | Use `@BeforeEach` or helper methods to avoid duplication. |
| 3 | **Use parameterised tests** | When the logic is identical but data varies, switch to `@ParameterizedTest`. |
| 4 | **Verify coverage parity** | Ensure line/branch coverage matches the original before merging. |

---

## Test Smell Example
```java
@Test
public void listOperations_shouldBehaveCorrectly() {
    FixedSizeList<String> list = new FixedSizeList<>(10);

    // Eager Test: exercise create, update and delete at once
    list.add("alpha");               // create
    list.set(0, "beta");             // update
    list.remove("beta");             // delete

    assertTrue(list.isEmpty(), "List should be empty after create–update–delete sequence");
}
```

---

## Refactored Example
```java
private FixedSizeList<String> list;

@BeforeEach
void setUp() {
    list = new FixedSizeList<>(10);
}

@Test
void shouldAddElement() {
    list.add("alpha");
    assertEquals(1, list.size(), "Size should be 1 after adding an element");
}

@Test
void shouldUpdateElement() {
    list.add("alpha");
    list.set(0, "beta");
    assertEquals("beta", list.get(0), "Element at index 0 should be updated to 'beta'");
}

@Test
void shouldRemoveElement() {
    list.add("alpha");
    list.remove("alpha");
    assertTrue(list.isEmpty(), "List should be empty after removing the element");
}
```