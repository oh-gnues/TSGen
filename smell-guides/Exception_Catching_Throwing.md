# Exception Catching Throwing

**Definition**  
A test method manually wraps code‑under‑test in a `try–catch` block—often re‑throwing or calling `fail()`—instead of using the testing framework’s built‑in *expected‑exception* support.

---

## Symptoms
- Pattern `try { … fail(); } catch (SomeException e) { … }`.  
- `catch` block re‑throws, is empty, or performs no meaningful assertion.  
- The test passes even if a *different* statement throws the exception.

---

## Why It’s Bad
Manual handling is verbose, obscures the assertion’s intent, and can hide or mis‑identify exceptions; this increases false positives and maintenance cost.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Use built‑in expected‑exception features** | Prefer JUnit 5 `assertThrows`, AssertJ `assertThatThrownBy`, or JUnit 4 `@Test(expected = …)` instead of raw `try–catch`. |
| 2 | **Isolate the throwing statement** | Place only the line expected to throw inside the lambda / method reference. |
| 3 | **Assert message or cause** | Where relevant, verify `getMessage()` or nested cause to ensure the correct error path. |
| 4 | **Maintain coverage parity** | After refactor, confirm line/branch coverage is unchanged in CI. |

---

## Test Smell Example
```java
@Test
public void parse_with_null_shouldThrow() {
    try {
        parser.parse(null);
        fail("Expected IllegalArgumentException");
    } catch (IllegalArgumentException e) {
        // no further assertion -> Exception Catching Throwing
    }
}
```

---

## Refactored Example (camelCase)
```java

// AssertJ (works with JUnit 4 & 5)
@Test
public void parse_withEmptyString_shouldThrowIAE() {
    assertThatThrownBy(() -> parser.parse(""))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessageContaining("cannot be empty");
}
```