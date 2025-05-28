# Empty Test

**Definition**  
A test method that is **completely empty**, with no body or comments at all. Similar to Default Test, but with literally nothing in the method.

---

## Symptoms
- `@Test` annotation present but zero code inside the method.
- Test reports "0 Assertions" or shows a warning.

---

## Why It’s Bad
This is not a real test--just an empty shell that does not validate anything and potentially causes confusion.

---

## Safe‑Fix Checklist
1. **Delete it** if unnecessary.
2. **Add logic** if there is supposed to be a test scenario.
3. **Review auto-generated files** for placholders.

---

## Test Smell Example
```java
@Test
public void doSomething_testIsEmpty() {
    // Empty Test: no content
}
```

---

## Refactored Example
```java
@Test
public void doSomething_shouldReturnExpectedValue() {
    int result = doSomething();
    assertEquals(42, result, "Result should be 42");
}
```