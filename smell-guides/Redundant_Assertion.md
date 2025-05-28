# Redundant Assertion

**Definition**  
Re-checking the **same logic** multiple times in one test or adding **unnecessary** extra assertions that do not add new coverage or clarity.

---

## Symptoms
- Multiple consecutive `assertEquals(...)` for the same condition.
- Checking “always true” statements or verifying the same property repeatedly.
- Confusion about which assertion actually matters when something fails.

---

## Why It’s Bad
Extra assertions can clutter the test. They increase the chances of confusion and complicate debugging or maintenance.

---

## Safe‑Fix Checklist
1. **Keep only the essential assertions** for each scenario.
2. **Remove any assertions with no clear purpose.**
3. **If coverage is duplicated across multiple tests**, clarify test scope or remove duplicates.

---

## Test Smell Example
```java
@Test
public void userCreationTest() {
    User user = userService.create("bob");
    
    // Redundant Assertions
    assertNotNull(user);
    assertNotNull(user.getId());      // possibly redundant if we check existence 
    assertTrue(userService.exists(user.getId())); 
    assertEquals("bob", user.getName());
    assertNotNull(user.getName());    // repeated check of name field
}
```

---

## Refactored Example
```java
@Test
public void shouldCreateUser_withValidName() {
    User user = userService.create("bob");
    
    assertNotNull(user, "User object should not be null");
    assertEquals("bob", user.getName(), "The user name should be bob");
}
```