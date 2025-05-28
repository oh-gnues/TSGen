# Lazy Test

**Definition**  
Two or more test methods contain **almost identical logic**, differing only in literal
values or input parameters. The duplication makes the suite brittle and expensive to
maintain.

---

## Symptoms
- Copy‑pasted assertion blocks with only constants changed.  
- A bug fix in the production code forces edits to many nearly identical tests.  
- Naming is generic (`test1`, `testCase2`) because behaviour is not isolated.

---

## Why It’s Bad
Duplication inflates code size and risks drift: one copy gets updated while others do not.
Developers waste time synchronising tests, and reviewers must scan repetitive, low‑value
code instead of focusing on intent.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Extract shared logic** into a private helper method | Centralises behaviour and removes copy‑paste. |
| 2 | **Prefer parameterised tests** when inputs vary | Use JUnit 4 `@RunWith(Parameterized.class)` to eliminate boilerplate. |
| 3 | **Keep assertion messages meaningful** | Even after refactor, each failure should explain the expectation. |
| 4 | **Verify coverage parity** | Ensure line/branch coverage remains unchanged in CI. |

---

## Test Smell Example
```java
@Test
void addOneElement_shouldIncreaseSizeToOne() {
    FixedSizeList<String> list = new FixedSizeList<>(10);
    list.add("alpha");
    assertEquals(1, list.size());
}

@Test
void addTwoElements_shouldIncreaseSizeToTwo() {
    FixedSizeList<String> list = new FixedSizeList<>(10);
    list.add("alpha");
    list.add("beta");
    assertEquals(2, list.size());
}
```

---

## Refactored Example 1 – Helper Method
```java
private void verifySizeAfterAdds(int expectedSize, String... elements) {
    FixedSizeList<String> list = new FixedSizeList<>(10);
    for (String e : elements) {
        list.add(e);
    }
    assertEquals("Size after adds", expectedSize, list.size());
}

@Test void size_shouldBeOne_afterAddingOneElement()  { verifySizeAfterAdds(1, "alpha"); }
@Test void size_shouldBeTwo_afterAddingTwoElements() { verifySizeAfterAdds(2, "alpha", "beta"); }
```