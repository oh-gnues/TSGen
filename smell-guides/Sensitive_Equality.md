# Sensitive Equality

**Definition**  
Using direct `assertEquals` on **floating-point (double/float)** or **date/time** objects, which can cause precision or timezone issues.

---

## Symptoms
- `assertEquals(0.3, calculator.add(0.1, 0.2))` leading to sporadic failures.
- Time-based tests failing due to timezone or milliseconds differences.
- Flaky tests that pass locally but fail in CI or vice versa.

---

## Why It’s Bad
Floating-point arithmetic is subject to **rounding errors**, and date/time can vary across systems. This makes tests unstable and prone to false negatives.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Use a tolerance/delta for floating-point** | `assertEquals(expected, actual, delta)` |
| 2 | **Compare dates by format or fixed clock** | e.g., freeze time with a controllable `Clock` object or assert differences within a range |
| 3 | **Use libraries** (like AssertJ) that provide flexible matching | e.g., `assertThat(value).isCloseTo(expected, offset(0.0001))` |

---

## Test Smell Example
```java
@Test
public void floatingPointCalculation() {
    double result = calculator.add(0.1, 0.2);
    // Sensitive Equality
    assertEquals(0.3, result);
}
```

---

## Refactored Example
```java
@Test
public void floatingPointCalculation_withTolerance() {
    double result = calculator.add(0.1, 0.2);
    assertEquals(0.3, result, 0.000001);
}
```