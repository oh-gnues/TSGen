# Duplicate Assert

**Definition**  
Within a single test, **repeating the same assertion** on the same property more than once—-like an **exact duplicate** check—-rather than a different aspect of the object or scenario.

---

## Symptoms
- Re-checking the same field: `assertEquals("alice", user.getName());` repeated multiple times.
- Adds confusion with no additional coverage.

---

## Why It’s Bad
Duplicating the same check doesn’t add value, *bloats the test* and might complicate maintenance if expectations change later.

---

## Safe‑Fix Checklist
1. **Assert each condition only once**.
2. **Use descriptive assertion messages** if clarity is needed.
3. **Remove any exact duplicates** to reduce noise.

---

## Test Smell Example
```java
@Test
public void checkUserData() {
    User user = userService.create("alice");
    // Duplicate Asserts
    assertEquals("alice", user.getName());
    assertEquals("alice", user.getName()); // Same field re-asserted
}
```

---

## Refactored Example
```java
@Test
public void checkUserData_shouldSetUserNameCorrectly() {
    User user = userService.create("alice");
    assertEquals("alice", user.getName());
}
```