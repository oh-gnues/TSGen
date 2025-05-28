# Dependent Test

**Definition**  
A test method that **depends** on another test method to run first (e.g., “createUser” must be successful before “updateUser” can pass). This implies an unintended order dependency, breaking test independence.

---

## Symptoms
- Comments like “Must run testCreateUser before testUpdateUser.”
- Passing only if run in a certain order; failing if run in isolation or a different sequence.
- Unreliable or inconsistent results with JUnit’s default (random) execution order.

---

## Why It’s Bad
Tests should be **independent**; the order of execution shouldn’t matter. Dependencies complicate maintenance and can produce false negatives in parallel or random runs.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Each test sets up its own required state** | If “create user” is needed, just create it inline for that test. |
| 2 | **Avoid global/shared state** | Use fresh objects or `@BeforeEach` for consistent initialization. |
| 3 | **Use helper methods** for common steps | For example, User `createAndPersistUser(String name)` to reduce duplication. |

---

## Test Smell Example
```java
@Test
public void testCreateUser() {
    // ...
    assertNotNull(user.getId());
}

@Test
public void testUpdateUser() {
    // Dependent on testCreateUser having run first
    user.setStatus("ACTIVE");
    assertEquals("ACTIVE", user.getStatus());
}
```

---

## Refactored Example
```java
@BeforeEach
public void setUp() {
    userService = new UserService();
}

@Test
public void shouldCreateUser() {
    User user = userService.create("bob");
    assertNotNull(user.getId());
}

@Test
public void shouldUpdateUser() {
    User user = userService.create("bob"); // create user independently
    userService.updateStatus(user.getId(), "ACTIVE");
    assertEquals("ACTIVE", userService.statusOf(user.getId()));
}
```