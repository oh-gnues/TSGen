# Assertion Roulette

**Definition**  
Multiple `assert*` statements live in a single test method **without individual failure
messages** or logical grouping, so when the test goes red you cannot immediately tell
*which* condition failed.

---

## Symptoms
- Two or more assertions in one test **without** a message parameter.  
- CI output shows only *expected X but was Y* with no extra context.  
- Long sequences of heterogeneous assertions verifying unrelated states.

---

## Why It’s Bad
Without clear messages developers must open the source to learn *which* assertion failed,
wasting debugging time and discouraging granular, single‑purpose tests.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Add a descriptive message** to every assertion | The failing output now pinpoints the exact invariant that broke. |
| 2 | **Or split the test** into multiple focused methods | One behaviour per test keeps names and failures self‑explanatory. |
| 3 | **Parameterise** when logic is identical but data varies | Replace copy‑pasted asserts with `@ParameterizedTest`. |

---

## Test Smell Example
```java
@Test
public void calculateValues() {
    assertEquals(2, myList.size());
    assertEquals(5, sum);
    assertTrue(result > 0);
}
```

---

## Refactored Example (camelCase)
```java
@Test
public void listSize_shouldBeTwo_afterAddingTwoElements() {
    assertEquals("List must contain exactly two elements", 2, myList.size());
}

@Test
public void sum_shouldBeFive_whenAddingTwoAndThree() {
    assertEquals("2 + 3 must equal 5", 5, sum);
}

@Test
public void result_shouldBePositive() {
    assertTrue("Result must be positive", result > 0);
}
```