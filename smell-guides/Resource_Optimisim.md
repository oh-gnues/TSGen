# Resource Optimism

**Definition**  
A test that **naively assumes** external resources (DB, file, network) are always available and doesn’t handle exceptions or readiness checks. For example, it just calls the DB and fails outright if the DB isn’t ready.

---

## Symptoms
- A test that fails immediately if the DB is not running.
- File read attempts with no fallback or setup.
- Lacks any exception handling or pre-checks.


---

## Why It’s Bad
External resources can fail, be unavailable, or have missing data. Such “optimistic” tests may break CI pipelines unpredictably, reducing the **robustness** of the test suite.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Prepare resources explicitly before tests** | Connect to DB, create schema, set up test data. |
| 2 | **Add fallback or error handling** | Consider retry, timeouts, or at least informative failure. |
| 3 | **Use mocks/stubs** if actual resource usage is not mandatory |  |

---

## Test Smell Example
```java
@Test
public void testDataRetrieval() {
    // Resource Optimism: assumes DB is already there
    List<Record> records = dbService.fetchAllRecords();
    assertFalse(records.isEmpty());
}
```

---

## Refactored Example
```java
@BeforeEach
public void setUpDB() {
    // Explicitly connect and prepare test data
    dbService.connect();
    dbService.prepareTestData();
}

@Test
public void testDataRetrieval() {
    List<Record> records = dbService.fetchAllRecords();
    assertFalse(records.isEmpty());
}
```