# Mystery Guest

**Definition**
A test relies on **hidden external state** (files, databases, network services) without making it explicit. For example, the test code does not show what it depends on, but a file or DB record must exist externally.

---

## Symptoms
- The test only works if a certain file or DB record is present.
- Works on one machine but fails on another (or in CI).
- Hard-coded paths or credentials, no setup logic in the test code.

---

## Why It’s Bad
Tests should be **independent** and **repeatable**. If external conditions are assumed, the test is fragile. It may pass or fail unpredictably based on environment differences.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Explicitly prepare needed resources** | Use temporary files, in-memory DB, or mocks so the environment is under test control. |
| 2 | **Same configuration for local and CI** | e.g., `application-test.yml` for test environment with consistent settings. |
| 3 | **reate any required data/state in the test** or setup | Insert DB records before running queries, then clean up afterward. |

---

## Test Smell Example
```java
@Test
public void shouldReadDataFromFile() {
    // Mystery Guest: depends on D:/data/input.csv existing
    List<String> data = fileService.read("D:/data/input.csv");
    assertFalse(data.isEmpty());
}
```

---

## Refactored Example
```java
@Test
public void shouldReadDataFromTestResource() throws IOException {
    // Use a temp file or a classpath resource to control setup
    Path tempFile = Files.createTempFile("input", ".csv");
    Files.write(tempFile, Arrays.asList("line1", "line2"));

    List<String> data = fileService.read(tempFile.toString());
    assertFalse(data.isEmpty());
}
```