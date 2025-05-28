# General Fixture

**Definition**  
A **large common fixture** is set up for all tests, even though some tests do not require all of it. For instance, `@BeforeEach` creates lots of objects and data, but only a subset of tests actually needs them.

---

## Symptoms
- `@BeforeEach` or `@BeforeAll` with too many objects, data, or connections.
- Some tests never use certain parts of the setup.
- Unnecessary overhead, causing slow tests.

---

## Why It’s Bad
Excessive fixture makes tests **hard to read** and increases **execution time**. It’s unclear which tests need which resources, complicating maintenance.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Initialize only what each test needs** | Keep the fixture minimal; create objects on-demand if needed. |
| 2 | **Minimize global setup** | Only share truly common items across tests. |
| 3 | **Use specialized setup methods** | Group similar tests that share partial setup into a helper. |

---

## Test Smell Example
```java
@BeforeEach
public void setUp() {
    // General Fixture: large initialization for every test
    user = new User("commonUser");
    order = new Order("commonOrder");
    product = new Product("commonProduct");
    db.initTestData(); // big data load
    // ...
}

@Test public void testUserCreation() { ... }  // doesn’t use product or db
@Test public void testOrderProcessing() { ... }  // only needs user
```

---

## Refactored Example
```java
@Test
public void testUserCreation() {
    User user = new User("testUser"); // Create only what's needed
    // ...
}

@Test
public void testOrderProcessing() {
    Order order = new Order("testOrder");
    // ...
}

// Or if some setup is common, keep it minimal in @BeforeEach
@BeforeEach
public void setUpUserAndOrder() {
    user = new User("commonUser");
    order = new Order("commonOrder");
}
```