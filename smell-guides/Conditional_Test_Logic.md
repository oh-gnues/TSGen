# Conditional Test Logic

**Definition**  
Having `if-else`, `switch`, or other branching statements **inside the test method** so that the test behavior changes based on conditions. For example, a single test method might handle different scenarios in a branched manner.

---

## Symptoms
- Presence of `if (someCondition) ... else ...` in the test code.
- Attempting to verify multiple paths in one test method, causing complexity.
- It's difficult to tell which branch was actually executed or failed during debugging.

---

## Why It’s Bad
When tests contain branching logic, it becomes harder to **test each branch independently**. A branch might never get executed, leaving that code path effectively untested. It also breaks the single-responsibility principle for tests and obscures which scenario fails when errors occur.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Split branches into separate test methods** | Each scenario should be in its own test, focusing on a single outcome. |
| 2 | **Use parameterized tests** | Simplify by enumerating input-output pairs instead of manually branching. |
| 3 | **Extract common setup** into `@BeforeEach` or helper methods | Ensure each branch scenario is still easy to set up without repetition. |
| 4 | **Move branching logic to production code** (if appropriate) | Keep tests straightforward; let the implementations handle logical routes. |

---

## Test Smell Example
```java
@Test
public void processOrder_basedOnStatus() {
    // Conditional Test Logic
    if (order.getStatus() == Status.NEW) {
        assertTrue(orderService.process(order));
    } else {
        assertFalse(orderService.processs(order));
    }
}
```

---

## Refactored Example
```java
@Test
public void shouldProcessOrder_whenStatusIsNew() {
    Order newOrder = new Order(Status.NEW);
    assertTrue(orderService.process(newOrder));
}

@Test
public void shouldNotProcessOrder_whenStatusIsShipped() {
    Order shippedOrder = new Order(Status.SHIPPED);
    assertFalse(orderService.process(shippedOrder));
}
```