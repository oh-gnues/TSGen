# Default Test

**Definition**  
A tes method that is simply a **boilerplate or template** with no actual implementation. Often created by an IDE or framework, then left untouched with a name like `testMethod()` containing no real assertions.

---

## Symptoms
- An empty or nearly empty test method with a placeholder or `TODO` comment.
- No real checks or logic, resulting in zero coverage of actual behavior.

---

## Why It’s Bad
Such tests give a **false sense of coverage** without verifying anything. They do not contribute to product quality and can confuse maintainers.

---

## Safe‑Fix Checklist
1. **Remove it** if it's unused.
2. **Implement actual test logic** if that functionality needs testing.
3. **Configure IDE** to avoid auto-generating unhelpful stubs.

---

## Test Smell Example
```java
@Test
public void defaultTestMethod() {
    // TODO: auto-generated default test, does nothing
}
```

---

## Refactored Example
```java
// Either remove it entirely
// Or if you do need a test, implement it
@Test
public void shouldProcessPayment_whenCreditCardIsValid() {
    Payment payment = new Payment("VALID_CARD");
    assertTrue(paymentService.process(payment));
}
```