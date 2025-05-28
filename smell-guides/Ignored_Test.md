# Magic Number Test (MNT)

**Definition**  
Within a single test, **repeating the same assertion** on the same property more than once—-like an **exact duplicate** check—rather than a different aspect of the object or scenario.

---

## Symptoms
- `@Ignore("Broken since version 2.0")` or `@Disabled` annotation remains for a long time.
- Not run in CI, so it contributes nothing to coverage or verification.

---

## Why It’s Bad
Ignored tests can hide real bugs. They provide **no value** yet linger in the codebase, increasing clutter.

---

## Safe‑Fix Checklist
1. **Fix or re-enable** the test if possible
2. **Delete** if it’s not needed anymore
3. **Track all ignored tests**: Maintain a list or process so that they are addressed rather than forgotten.

---

## Test Smell Example
```java
@Ignore("Broken since version 2.0")
@Test
public void testLegacyFeature() {
    // ...
}
```

---

## Refactored Example
```java
@Test
public void testLegacyFeature_fixed() {
    // Re-enabled after fixing
    // ...
}

// Or remove it entirely, or track it in an issue system if it's not a priority.
```