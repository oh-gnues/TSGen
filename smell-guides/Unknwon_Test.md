# Unknown Test

**Definition**  
A test method whose **name or description does not convey** what is being tested. For instance, methods named `test1()`, `checkAll()`, `tempTest()`, etc.

---

## Symptoms
- Test names that contain only numbers or random words.
- The only way to understand the purpose is by reading all the code inside the method.

---

## Why It’s Bad
It undermines clarity: tests should be **self-describing** to let readers quickly know the scenario or intention. It complicates maintenance if developers cannot tell what each test covers.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Use descriptive naming** | e.g., `shouldReturnError_whenInvalidInput()`. |
| 2 | **Prefer method names over comments** | The name itself is the documentation. |
| 3 | **Update test names** whenever the underlying functionality changes |  |

---

## Test Smell Example
```java
@Test
public void test1() {
    // Unknown Test: no clue what this verifies
}
```

---

## Refactored Example
```java
@Test
public void shouldFailLogin_whenPasswordIsIncorrect() {
    // Now it's clear what scenario is tested
}
```