# Print Statement

**Definition**  
Using `System.out.println` or debug logs directly in a test **to observe outcomes** instead of using proper assertions. This may also lead to excessive logging output in CI.

---

## Symptoms
- Multiple `System.out.println("value: " + value);` statements.
- The test has no real assertion; the developer checks logs to confirm correctness.
- CI logs are overly long, making it harder to find actual problems.

---

## Why It’s Bad
Tests should rely on **automated assertions** rather than manual log inspection. Excessive logging can obscure real issues and slow down review.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Replace print statements with assertions** | e.g., `assertEquals(...)`, `assertTrue(...)` |
| 2 | **Minimize logging** | Only log essential info that helps when something fails. |
| 3 | **Avoid spamming CI logs** | Remove or lower verbosity to keep logs readable. |

---

## Test Smell Example
```java
@Test
public void calculateSum() {
    int sum = calculator.sum(2, 3);
    System.out.println("Sum result: " + sum); // Print Statement
}
```

---

## Refactored Example
```java
@Test
public void calculateSum_shouldReturnFive() {
    int sum = calculator.sum(2, 3);
    assertEquals(5, sum);
}
```