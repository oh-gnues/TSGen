# Sleepy Test

**Definition**  
Using `Thread.sleep()` (or similar) in a test to wait for asynchronous operations or timing-based conditions. Often used as a naive solution to let background tasks finish.

---

## Symptoms
- Hard-coded sleeps, e.g., `Thread.sleep(1000)`.
- Slow tests, or flaky if the environment is slower/faster than expected.
- Increased CI runtime, sporadic test failures (“flaky tests”).

---

## Why It’s Bad
If the sleep duration is too short, the async operation might not complete in time; too long, the tests become unnecessarily slow. It also leads to non-deterministic behavior across different systems.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Replace sleep with polling or event-based logic** | For example, wait until a condition is satisfied within a certain timeout. |
| 2 | **Mock out async dependencies** | If you can simulate a fast result without real concurrency, do so. |
| 3 | **Assert actual completion condition** | Check explicit signals of readiness instead of guessing with a sleep. |

---

## Test Smell Example
```java
@Test
public void asyncOperationTest() throws InterruptedException {
    asyncService.startOperation();
    Thread.sleep(2000); // Sleepy Test: naive 2-second wait
    assertTrue(asyncService.isOperationDone());
}
```

---

## Refactored Example
```java
@Test
public void asyncOperationTest_withoutSleep() {
    asyncService.startOperation();
    await().atMost(Duration.ofSeconds(5))
           .until(() -> asyncService.isOperationDone());
    assertTrue(asyncService.isOperationDone());
}
```