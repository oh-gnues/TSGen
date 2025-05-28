# Constructor Initialization

**Definition**  
Initializing the test environment **inside the test class constructor**, rather than using the proper lifecycle hooks (@BeforeEach, @BeforeAll). This includes creating services, connecting to a database, etc.

---

## Symptoms
- The test class constructor is used for setting up the environment (e.g., DB connection, mocks).
- Potential conflicts with standard JUnit lifecycle methods, or unpredictable ordering issues.

---

## Why It’s Bad
The class constructor is called at **instantiation time**, which may not align with JUnit's setup sequence. This can lead to **inconsistent test states** or unexpected exceptions.

---

## Safe‑Fix Checklist
| # | Action | Rationale |
|---|---|---|
| 1 | **Use `@BeforeEach` or `@BeforeAll`** | Migrate any setup logic to these methods. |
| 2 | **Never put test logic in the constructor** | Keep only minimal field initialization in the constructor. |
| 3 | **Use builders or factory methods** | If you need to create complex objects, do so via helper methods, not the test consturctor. |

---

## Test Smell Example
```java
public class OrderServiceTest {
    private OrderService orderService;

    public OrderServiceTest() {
        // Constructor Initialization
        this.orderService = new OrderService();
        this.orderService.connectToDatabase();
    }

    @Test
    public void testOrderCreation() {
        // ...
    }
}
```

---

## Refactored Example
```java
public class OrderServiceTest {
    private OrderService orderService;

    @BeforeEach
    public void setUp() {
        this.orderService = new OrderService();
        this.orderService.connectToDatabase();
    }

    @Test
    public void testOrderCreation() {
        // ...
    }
}
```