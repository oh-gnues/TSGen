# Verbose Test

**Definition**  
A **very long or overly detailed** test method with lots of inline setup, multiple checks, and sometimes multiple responsibilities, making it hard to read and maintain.

---

## Symptoms
- A single test method spanning 50–100 lines.
- Inline object creation, branching, and verification steps all lumped together.
- Nested blocks or conditions that make it unclear what is actually being tested.

---

## Why It’s Bad
Excessively large tests dilute the **intent** of what’s being verified. They are harder to update, review, and can hide multiple responsibilities in one method.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Follow the Given-When-Then structure** | Break test logic into distinct phases. |
| 2 | **Use helper methods or a Builder** | Simplify complex setup, reduce duplicated code. |
| 3 | **One scenario per test** | If multiple scenarios are tested in one method, split them out. |
| 4 | **Extract repeated logic** | into `@BeforeEach` or utility methods. |

---

## Test Smell Example
```java
@Test
public void complexOrderProcessTest() {
    // 100 lines of setup and assertions
    Order order = new Order();
    order.setName("TestOrder");
    // ...

    orderService.initialize(order);
    // multiple conditions, branches, and checks

    assertNotNull(order.getId());
    // many more lines...
}
```

---

## Refactored Example
```java
@Test
public void shouldInitializeOrderCorrectly() {
    Order order = createTestOrder("TestOrder");
    orderService.initialize(order);
    
    assertNotNull(order.getId(), "Order ID should be set after initialization");
}

private Order createTestOrder(String name) {
    Order order = new Order();
    order.setName(name);
    // minimal additional setup
    return order;
}
```