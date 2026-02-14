# Chapter 16. 리액티브 테스트 전략

리액티브 프로그래밍은 비동기/논블로킹 특성상 전통적인 동기 방식의 테스트와는 접근법이 다르다. `Mono`와 `Flux`는 구독(subscribe)이 일어나기 전까지 아무것도 실행되지 않으며, 데이터가 비동기적으로 흘러가므로 단순히 반환값을 `assertEquals()`로 검증하는 방식은 적합하지 않다. 이번 장에서는 리액티브 테스트의 핵심 도구인 **StepVerifier**와 **WebTestClient**를 중심으로, Embedded MongoDB, Testcontainers, MockWebServer를 활용한 다양한 테스트 전략을 체계적으로 다룬다.

---

## 16.1 StepVerifier를 활용한 단위 테스트

### 16.1.1 StepVerifier란?

`StepVerifier`는 Reactor에서 제공하는 테스트 유틸리티로, `Publisher`(Mono, Flux)가 방출하는 데이터 시퀀스를 단계별로 검증한다. `reactor-test` 모듈에 포함되어 있다.

```groovy
dependencies {
    testImplementation 'io.projectreactor:reactor-test'
}
```

기본 사용 패턴은 다음과 같다.

```java
StepVerifier.create(publisher)   // 1. Publisher를 감싼다
    .expectNext(value)            // 2. 기대하는 값을 선언한다
    .verifyComplete();            // 3. 완료 신호를 검증하고 구독을 시작한다
```

`verifyComplete()`를 호출해야 실제 구독이 시작된다. 이 호출이 없으면 테스트는 아무것도 검증하지 않고 통과한다.

### 16.1.2 expectNext, expectComplete, expectError

가장 기본적인 검증 메서드들이다.

```java
@Test
void mono_단일값_검증() {
    Mono<String> mono = Mono.just("Hello WebFlux");

    StepVerifier.create(mono)
        .expectNext("Hello WebFlux")
        .verifyComplete();
}

@Test
void flux_다중값_검증() {
    Flux<Integer> flux = Flux.just(1, 2, 3, 4, 5);

    StepVerifier.create(flux)
        .expectNext(1)
        .expectNext(2)
        .expectNext(3, 4, 5)  // 여러 값을 한 번에 검증
        .verifyComplete();
}

@Test
void flux_개수_검증() {
    Flux<String> flux = Flux.just("a", "b", "c");

    StepVerifier.create(flux)
        .expectNextCount(3)   // 값의 내용은 무시하고 개수만 확인
        .verifyComplete();
}

@Test
void mono_에러_검증() {
    Mono<String> errorMono = Mono.error(
        new IllegalArgumentException("잘못된 입력입니다"));

    StepVerifier.create(errorMono)
        .expectError(IllegalArgumentException.class)
        .verify();  // 에러로 종료되므로 verifyComplete() 대신 verify()
}

@Test
void mono_에러_메시지와_조건_검증() {
    Mono<String> errorMono = Mono.error(
        new NotFoundException("ID-001", "상품을 찾을 수 없습니다"));

    StepVerifier.create(errorMono)
        .expectErrorMatches(throwable ->
            throwable instanceof NotFoundException
            && throwable.getMessage().contains("ID-001"))
        .verify();
}
```

### 16.1.3 assertNext

`assertNext()`는 방출된 값에 대해 복잡한 단언(assertion)을 수행할 때 사용한다. `Consumer<T>`를 받으므로 AssertJ와 조합하기 좋다.

```java
@Test
void assertNext로_복잡한_검증() {
    Mono<Product> productMono = productService.findById("prod-001");

    StepVerifier.create(productMono)
        .assertNext(product -> {
            assertThat(product.getId()).isEqualTo("prod-001");
            assertThat(product.getName()).isNotBlank();
            assertThat(product.getPrice()).isPositive();
            assertThat(product.getCategory()).isIn("ELECTRONICS", "BOOKS");
        })
        .verifyComplete();
}
```

### 16.1.4 withVirtualTime

`Flux.interval()`이나 `Mono.delay()`처럼 시간에 의존하는 연산을 테스트할 때, 실제 시간 경과를 기다리면 테스트가 느려진다. `withVirtualTime()`은 가상 시간을 사용하여 시간 흐름을 즉시 시뮬레이션한다.

```java
@Test
void 가상_시간으로_지연_검증() {
    StepVerifier.withVirtualTime(
            () -> Mono.just("결과").delayElement(Duration.ofHours(1)))
        .expectSubscription()
        .expectNoEvent(Duration.ofMinutes(59))  // 59분 동안 이벤트 없음
        .thenAwait(Duration.ofMinutes(1))        // 1분 경과 시뮬레이션
        .expectNext("결과")
        .verifyComplete();
}

@Test
void 가상_시간으로_interval_검증() {
    StepVerifier.withVirtualTime(
            () -> Flux.interval(Duration.ofSeconds(1)).take(3))
        .expectSubscription()
        .thenAwait(Duration.ofSeconds(3))
        .expectNext(0L, 1L, 2L)
        .verifyComplete();
}
```

> **주의**: `withVirtualTime()`에 전달하는 `Supplier`는 반드시 람다 내부에서 `Publisher`를 생성해야 한다. 외부에서 생성한 `Publisher`를 전달하면 가상 시간 스케줄러가 올바르게 주입되지 않는다.

### 16.1.5 서비스 계층 단위 테스트 예제

Mockito로 리포지토리를 모킹하고 StepVerifier로 서비스 계층을 테스트한다.

```java
@ExtendWith(MockitoExtension.class)
class ProductServiceTest {

    @Mock
    private ProductRepository productRepository;

    @InjectMocks
    private ProductService productService;

    @Test
    void findById_존재하는_상품() {
        Product product = Product.builder()
            .id("prod-001").name("스프링 부트 가이드")
            .price(new BigDecimal("35000")).category("BOOKS").build();

        when(productRepository.findById("prod-001"))
            .thenReturn(Mono.just(product));

        StepVerifier.create(productService.findById("prod-001"))
            .assertNext(p -> {
                assertThat(p.getName()).isEqualTo("스프링 부트 가이드");
                assertThat(p.getPrice()).isEqualByComparingTo("35000");
            })
            .verifyComplete();
    }

    @Test
    void findById_존재하지_않는_상품() {
        when(productRepository.findById("unknown"))
            .thenReturn(Mono.empty());

        StepVerifier.create(productService.findById("unknown"))
            .expectError(NotFoundException.class)
            .verify();
    }

    @Test
    void create_정상_생성() {
        ProductRequest request = new ProductRequest(
            "새 상품", "설명", "ELECTRONICS", new BigDecimal("50000"));

        when(productRepository.save(any(Product.class)))
            .thenAnswer(invocation -> {
                Product p = invocation.getArgument(0);
                p.setId("generated-id");
                return Mono.just(p);
            });

        StepVerifier.create(productService.create(request))
            .assertNext(p -> {
                assertThat(p.getId()).isEqualTo("generated-id");
                assertThat(p.getName()).isEqualTo("새 상품");
            })
            .verifyComplete();
    }
}
```

### 16.1.6 StepVerifier 주요 메서드 정리

| 메서드 | 용도 |
|--------|------|
| `expectNext(T...)` | 기대하는 값을 순서대로 검증 |
| `expectNextCount(long)` | 방출 개수만 검증 |
| `assertNext(Consumer<T>)` | 복잡한 단언 로직 적용 |
| `expectError(Class)` | 특정 타입의 에러 기대 |
| `expectErrorMessage(String)` | 에러 메시지 검증 |
| `expectErrorMatches(Predicate)` | 에러 조건 검증 |
| `verifyComplete()` | 완료 신호 검증 + 구독 시작 |
| `verify()` | 구독 시작 (에러 종료 시 사용) |
| `withVirtualTime(Supplier)` | 가상 시간으로 시간 의존 테스트 |
| `thenAwait(Duration)` | 가상 시간 경과 시뮬레이션 |
| `expectNoEvent(Duration)` | 지정 시간 동안 이벤트 없음 검증 |

---

## 16.2 WebTestClient를 활용한 통합 테스트

### 16.2.1 WebTestClient란?

`WebTestClient`는 Spring WebFlux 애플리케이션의 HTTP 엔드포인트를 테스트하기 위한 논블로킹 테스트 클라이언트다. 서버를 실행하지 않고 컨트롤러에 직접 바인딩하거나, 실제 HTTP 요청을 보내는 방식 모두 지원한다.

### 16.2.2 바인딩 방식

**bindToController** -- 특정 컨트롤러만 격리하여 테스트한다. Spring 컨텍스트를 로드하지 않으므로 빠르다.

```java
@BeforeEach
void setUp() {
    ProductService mockService = mock(ProductService.class);
    ProductController controller = new ProductController(mockService);

    webTestClient = WebTestClient
        .bindToController(controller)
        .controllerAdvice(new GlobalExceptionHandler())
        .build();
}
```

**bindToApplicationContext** -- 전체 애플리케이션 컨텍스트를 로드하여 테스트한다.

```java
@SpringBootTest
@AutoConfigureWebTestClient
class ProductIntegrationTest {

    @Autowired
    private WebTestClient webTestClient;
}
```

**bindToRouterFunction** -- 함수형 엔드포인트를 테스트할 때 사용한다.

```java
webTestClient = WebTestClient
    .bindToRouterFunction(ProductRouter.route(handler))
    .build();
```

### 16.2.3 GET/POST/PUT/DELETE 테스트

```java
@WebFluxTest(ProductController.class)
class ProductControllerTest {

    @Autowired
    private WebTestClient webTestClient;

    @MockBean
    private ProductService productService;

    @Test
    void 상품_단건_조회_성공() {
        Product product = Product.builder()
            .id("prod-001").name("스프링 부트 가이드")
            .price(new BigDecimal("35000")).category("BOOKS").build();

        when(productService.findById("prod-001"))
            .thenReturn(Mono.just(product));

        webTestClient.get()
            .uri("/api/products/{id}", "prod-001")
            .accept(MediaType.APPLICATION_JSON)
            .exchange()
            .expectStatus().isOk()
            .expectHeader().contentType(MediaType.APPLICATION_JSON)
            .expectBody()
            .jsonPath("$.id").isEqualTo("prod-001")
            .jsonPath("$.name").isEqualTo("스프링 부트 가이드")
            .jsonPath("$.price").isEqualTo(35000);
    }

    @Test
    void 상품_목록_조회() {
        when(productService.findAll())
            .thenReturn(Flux.just(
                Product.builder().id("1").name("상품1").build(),
                Product.builder().id("2").name("상품2").build()));

        webTestClient.get()
            .uri("/api/products")
            .exchange()
            .expectStatus().isOk()
            .expectBodyList(Product.class)
            .hasSize(2)
            .value(products -> {
                assertThat(products.get(0).getName()).isEqualTo("상품1");
                assertThat(products.get(1).getName()).isEqualTo("상품2");
            });
    }

    @Test
    void 상품_생성_성공() {
        ProductRequest request = new ProductRequest(
            "새 상품", "설명", "ELECTRONICS", new BigDecimal("50000"));
        Product created = Product.builder()
            .id("new-id").name("새 상품")
            .price(new BigDecimal("50000")).build();

        when(productService.create(any(ProductRequest.class)))
            .thenReturn(Mono.just(created));

        webTestClient.post()
            .uri("/api/products")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(request)
            .exchange()
            .expectStatus().isCreated()
            .expectBody()
            .jsonPath("$.id").isEqualTo("new-id")
            .jsonPath("$.name").isEqualTo("새 상품");
    }

    @Test
    void 상품_수정_성공() {
        ProductRequest updateRequest = new ProductRequest(
            "수정된 상품", "설명", "ELECTRONICS", new BigDecimal("60000"));
        Product updated = Product.builder()
            .id("prod-001").name("수정된 상품")
            .price(new BigDecimal("60000")).build();

        when(productService.update(eq("prod-001"), any()))
            .thenReturn(Mono.just(updated));

        webTestClient.put()
            .uri("/api/products/{id}", "prod-001")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(updateRequest)
            .exchange()
            .expectStatus().isOk()
            .expectBody()
            .jsonPath("$.name").isEqualTo("수정된 상품");
    }

    @Test
    void 상품_삭제_성공() {
        when(productService.delete("prod-001")).thenReturn(Mono.empty());

        webTestClient.delete()
            .uri("/api/products/{id}", "prod-001")
            .exchange()
            .expectStatus().isNoContent()
            .expectBody().isEmpty();
    }

    @Test
    void 존재하지_않는_상품_404() {
        when(productService.findById("unknown"))
            .thenReturn(Mono.error(new NotFoundException("상품을 찾을 수 없습니다")));

        webTestClient.get()
            .uri("/api/products/{id}", "unknown")
            .exchange()
            .expectStatus().isNotFound()
            .expectBody()
            .jsonPath("$.message").isEqualTo("상품을 찾을 수 없습니다");
    }
}
```

### 16.2.4 JSON 검증 심화

```java
@Test
void JSON_상세_검증() {
    when(productService.findById("prod-001"))
        .thenReturn(Mono.just(sampleProduct()));

    webTestClient.get()
        .uri("/api/products/{id}", "prod-001")
        .exchange()
        .expectStatus().isOk()
        .expectBody()
        .jsonPath("$.id").exists()
        .jsonPath("$.name").isNotEmpty()
        .jsonPath("$.price").isNumber()
        .jsonPath("$.tags").isArray()
        .jsonPath("$.tags.length()").isEqualTo(3)
        .jsonPath("$.tags[0]").isEqualTo("spring")
        // JSON 문자열 전체 비교 (false = 느슨한 비교, 추가 필드 허용)
        .json("""
            {"id": "prod-001", "name": "스프링 부트 가이드", "category": "BOOKS"}
            """, false);
}

@Test
void 응답을_객체로_역직렬화하여_검증() {
    when(productService.findById("prod-001"))
        .thenReturn(Mono.just(sampleProduct()));

    webTestClient.get()
        .uri("/api/products/{id}", "prod-001")
        .exchange()
        .expectBody(Product.class)
        .value(product -> {
            assertThat(product.getId()).isEqualTo("prod-001");
            assertThat(product.getPrice()).isGreaterThan(BigDecimal.ZERO);
        });
}
```

---

## 16.3 Embedded MongoDB를 활용한 리포지토리 테스트

### 16.3.1 Embedded MongoDB 설정

실제 MongoDB 서버 없이 JVM 내에서 MongoDB를 실행하여 리포지토리를 테스트한다.

```groovy
dependencies {
    testImplementation 'de.flapdoodle.embed:de.flapdoodle.embed.mongo.spring3x:4.11.0'
}
```

### 16.3.2 @DataMongoTest

`@DataMongoTest`는 MongoDB 관련 컴포넌트만 로드하는 테스트 슬라이스 어노테이션이다.

| 로드되는 컴포넌트 | 로드되지 않는 컴포넌트 |
|-------------------|---------------------|
| `@Document` 엔티티 | `@Controller`, `@Service` |
| `ReactiveMongoRepository` | `@RestController` |
| `ReactiveMongoTemplate` | `WebFilter`, Security 설정 |

```java
@DataMongoTest
class ProductRepositoryTest {

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private ReactiveMongoTemplate mongoTemplate;

    @BeforeEach
    void setUp() {
        mongoTemplate.dropCollection(Product.class).block();
    }

    @Test
    void save_and_findById() {
        Product product = Product.builder()
            .name("테스트 상품").category("ELECTRONICS")
            .price(new BigDecimal("25000"))
            .tags(List.of("test", "electronics")).build();

        StepVerifier.create(
            productRepository.save(product)
                .flatMap(saved -> productRepository.findById(saved.getId())))
            .assertNext(found -> {
                assertThat(found.getName()).isEqualTo("테스트 상품");
                assertThat(found.getPrice()).isEqualByComparingTo("25000");
                assertThat(found.getTags()).containsExactly("test", "electronics");
            })
            .verifyComplete();
    }

    @Test
    void findByCategory() {
        Flux<Product> setup = productRepository.saveAll(List.of(
            Product.builder().name("노트북").category("ELECTRONICS")
                .price(new BigDecimal("1500000")).build(),
            Product.builder().name("키보드").category("ELECTRONICS")
                .price(new BigDecimal("150000")).build(),
            Product.builder().name("스프링 인 액션").category("BOOKS")
                .price(new BigDecimal("40000")).build()
        ));

        StepVerifier.create(
            setup.thenMany(productRepository.findByCategory("ELECTRONICS")))
            .expectNextCount(2)
            .verifyComplete();
    }

    @Test
    void findByPriceRange() {
        Flux<Product> setup = productRepository.saveAll(List.of(
            Product.builder().name("저가").category("ETC")
                .price(new BigDecimal("5000")).build(),
            Product.builder().name("중가").category("ETC")
                .price(new BigDecimal("50000")).build(),
            Product.builder().name("고가").category("ETC")
                .price(new BigDecimal("500000")).build()
        ));

        StepVerifier.create(
            setup.thenMany(productRepository.findByPriceRange(
                new BigDecimal("10000"), new BigDecimal("100000"))))
            .assertNext(p -> assertThat(p.getName()).isEqualTo("중가"))
            .verifyComplete();
    }
}
```

### 16.3.3 테스트 데이터 준비 전략

**팩토리 메서드 패턴**으로 테스트 데이터를 일관성 있게 준비한다.

```java
public class TestDataFactory {

    public static Product createProduct(String id, String name, String category) {
        return Product.builder()
            .id(id).name(name).category(category)
            .price(new BigDecimal("10000"))
            .tags(List.of("test"))
            .createdAt(LocalDateTime.now())
            .build();
    }

    public static Review createReview(String productId, int rating) {
        return Review.builder()
            .productId(productId).userId("test-user")
            .rating(rating).content("테스트 리뷰")
            .createdAt(LocalDateTime.now())
            .build();
    }
}
```

### 16.3.4 ReactiveMongoTemplate 테스트

리포지토리 인터페이스로 표현하기 어려운 복잡한 쿼리를 테스트한다.

```java
@DataMongoTest
class ProductCustomRepositoryTest {

    @Autowired
    private ReactiveMongoTemplate mongoTemplate;

    @BeforeEach
    void setUp() {
        mongoTemplate.dropCollection(Product.class).block();
        mongoTemplate.insertAll(List.of(
            Product.builder().name("상품A").category("ELECTRONICS")
                .price(new BigDecimal("100000")).build(),
            Product.builder().name("상품B").category("ELECTRONICS")
                .price(new BigDecimal("200000")).build(),
            Product.builder().name("상품C").category("BOOKS")
                .price(new BigDecimal("30000")).build()
        )).blockLast();
    }

    @Test
    void Criteria_쿼리_테스트() {
        Query query = Query.query(
            Criteria.where("category").is("ELECTRONICS")
                .and("price").gte(new BigDecimal("150000"))
        ).with(Sort.by(Sort.Direction.DESC, "price"));

        StepVerifier.create(mongoTemplate.find(query, Product.class))
            .assertNext(p -> {
                assertThat(p.getName()).isEqualTo("상품B");
                assertThat(p.getPrice()).isEqualByComparingTo("200000");
            })
            .verifyComplete();
    }

    @Test
    void Aggregation_테스트() {
        Aggregation aggregation = Aggregation.newAggregation(
            Aggregation.group("category").count().as("count"),
            Aggregation.sort(Sort.Direction.ASC, "_id")
        );

        StepVerifier.create(
            mongoTemplate.aggregate(aggregation, "products", Document.class))
            .assertNext(doc -> {
                assertThat(doc.getString("_id")).isEqualTo("BOOKS");
                assertThat(doc.getInteger("count")).isEqualTo(1);
            })
            .assertNext(doc -> {
                assertThat(doc.getString("_id")).isEqualTo("ELECTRONICS");
                assertThat(doc.getInteger("count")).isEqualTo(2);
            })
            .verifyComplete();
    }
}
```

---

## 16.4 Testcontainers로 MongoDB 테스트 환경 구성

### 16.4.1 Testcontainers란?

Embedded MongoDB는 편리하지만 실제 MongoDB와 동작이 미묘하게 다를 수 있다. **Testcontainers**는 Docker 컨테이너를 활용하여 실제 MongoDB 인스턴스를 테스트 환경에서 실행한다.

```groovy
dependencies {
    testImplementation 'org.testcontainers:testcontainers:1.19.3'
    testImplementation 'org.testcontainers:mongodb:1.19.3'
    testImplementation 'org.testcontainers:junit-jupiter:1.19.3'
}
```

### 16.4.2 @Testcontainers, @Container, DynamicPropertySource

```java
@DataMongoTest
@Testcontainers
class ProductRepositoryTestcontainersTest {

    @Container
    static MongoDBContainer mongoDBContainer =
        new MongoDBContainer("mongo:7.0")
            .withExposedPorts(27017);

    @DynamicPropertySource
    static void setProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.mongodb.uri",
            mongoDBContainer::getReplicaSetUrl);
    }

    @Autowired
    private ProductRepository productRepository;

    @BeforeEach
    void setUp() {
        productRepository.deleteAll().block();
    }

    @Test
    void save_and_findById() {
        Product product = Product.builder()
            .name("Testcontainers 상품").category("ELECTRONICS")
            .price(new BigDecimal("99000")).build();

        StepVerifier.create(
            productRepository.save(product)
                .flatMap(saved -> productRepository.findById(saved.getId())))
            .assertNext(found -> {
                assertThat(found.getName()).isEqualTo("Testcontainers 상품");
                assertThat(found.getPrice()).isEqualByComparingTo("99000");
            })
            .verifyComplete();
    }
}
```

| 어노테이션 | 역할 |
|-----------|------|
| `@Testcontainers` | JUnit 5에 Testcontainers 생명주기 관리를 위임 |
| `@Container` | 컨테이너 인스턴스를 JUnit이 관리. `static`이면 클래스 단위, 인스턴스 필드면 메서드 단위 |
| `@DynamicPropertySource` | 컨테이너 시작 후 동적으로 결정된 속성(포트 등)을 Spring 환경에 주입 |

### 16.4.3 컨테이너 재사용으로 테스트 속도 개선

테스트 클래스마다 컨테이너를 새로 띄우면 시간이 오래 걸린다. 추상 클래스로 컨테이너를 공유한다.

```java
public abstract class AbstractMongoTestcontainer {

    static final MongoDBContainer MONGO_CONTAINER;

    static {
        MONGO_CONTAINER = new MongoDBContainer("mongo:7.0")
            .withReuse(true);
        MONGO_CONTAINER.start();
    }

    @DynamicPropertySource
    static void setProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.mongodb.uri",
            MONGO_CONTAINER::getReplicaSetUrl);
    }
}
```

```java
@DataMongoTest
class ProductRepositoryTest extends AbstractMongoTestcontainer {

    @Autowired
    private ProductRepository productRepository;

    @Test
    void 기본_CRUD_테스트() {
        // MONGO_CONTAINER가 이미 실행 중이므로 빠르게 시작
        StepVerifier.create(productRepository.save(
                Product.builder().name("공유 컨테이너 테스트")
                    .category("BOOKS").price(new BigDecimal("15000")).build()))
            .assertNext(p -> assertThat(p.getId()).isNotNull())
            .verifyComplete();
    }
}
```

### 16.4.4 트랜잭션 테스트 (Replica Set)

Testcontainers의 `MongoDBContainer`는 기본적으로 단일 노드 Replica Set으로 시작하므로 트랜잭션 테스트가 가능하다.

```java
@DataMongoTest
@Testcontainers
class TransactionTest {

    @Container
    static MongoDBContainer mongoDBContainer = new MongoDBContainer("mongo:7.0");

    @DynamicPropertySource
    static void setProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.mongodb.uri",
            mongoDBContainer::getReplicaSetUrl);
    }

    @Autowired
    private ReactiveMongoTemplate mongoTemplate;

    @Autowired
    private ProductRepository productRepository;

    @Test
    void 트랜잭션_롤백_테스트() {
        productRepository.save(Product.builder()
            .name("트랜잭션 테스트").category("TEST")
            .price(new BigDecimal("10000")).build()).block();

        ReactiveMongoTransactionManager txManager =
            new ReactiveMongoTransactionManager(
                mongoTemplate.getMongoDatabaseFactory());
        TransactionalOperator txOperator =
            TransactionalOperator.create(txManager);

        // 트랜잭션 내에서 업데이트 후 의도적으로 에러 발생
        Mono<Product> txMono = productRepository.findAll().next()
            .flatMap(p -> {
                p.setPrice(new BigDecimal("99999"));
                return productRepository.save(p);
            })
            .then(Mono.error(new RuntimeException("의도된 에러")))
            .cast(Product.class)
            .as(txOperator::transactional);

        StepVerifier.create(txMono)
            .expectError(RuntimeException.class)
            .verify();

        // 가격이 원래 값으로 유지되는지 확인 (롤백 검증)
        StepVerifier.create(productRepository.findAll().next())
            .assertNext(p ->
                assertThat(p.getPrice()).isEqualByComparingTo("10000"))
            .verifyComplete();
    }
}
```

### 16.4.5 Embedded MongoDB vs Testcontainers

| 기준 | Embedded MongoDB | Testcontainers |
|------|-----------------|----------------|
| **Docker 필요** | 불필요 | 필요 |
| **시작 속도** | 빠름 | 느림 (컨테이너 시작) |
| **MongoDB 버전 일치** | 제한적 | 프로덕션과 동일 버전 가능 |
| **기능 호환성** | 일부 미지원 | 완벽한 호환성 |
| **트랜잭션 지원** | 제한적 | 완벽 지원 |
| **권장 용도** | 단순 CRUD 테스트 | 프로덕션과 동일한 검증 |

---

## 16.5 MockWebServer를 활용한 외부 API 모킹

### 16.5.1 MockWebServer란?

`MockWebServer`는 OkHttp 라이브러리에서 제공하는 가벼운 HTTP 서버로, `WebClient`를 통해 호출하는 외부 API를 로컬에서 모킹한다.

```groovy
dependencies {
    testImplementation 'com.squareup.okhttp3:mockwebserver:4.12.0'
}
```

### 16.5.2 MockResponse와 기본 사용법

```java
class ExternalApiClientTest {

    private MockWebServer mockWebServer;
    private ExternalApiClient apiClient;

    @BeforeEach
    void setUp() throws IOException {
        mockWebServer = new MockWebServer();
        mockWebServer.start();

        WebClient webClient = WebClient.builder()
            .baseUrl(mockWebServer.url("/").toString())
            .build();
        apiClient = new ExternalApiClient(webClient);
    }

    @AfterEach
    void tearDown() throws IOException {
        mockWebServer.shutdown();
    }

    @Test
    void 정상_응답_테스트() {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setHeader("Content-Type", "application/json")
            .setBody("""
                {"id": "ext-001", "name": "외부 데이터", "value": 42}
                """));

        StepVerifier.create(apiClient.getData("ext-001"))
            .assertNext(data -> {
                assertThat(data.getId()).isEqualTo("ext-001");
                assertThat(data.getName()).isEqualTo("외부 데이터");
            })
            .verifyComplete();
    }

    @Test
    void 지연_응답으로_타임아웃_테스트() {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody("{\"status\": \"ok\"}")
            .setHeader("Content-Type", "application/json")
            .setBodyDelay(2, TimeUnit.SECONDS));

        StepVerifier.create(apiClient.getDataWithTimeout("001"))
            .expectError(TimeoutException.class)
            .verify();
    }

    @Test
    void 재시도_후_성공() {
        mockWebServer.enqueue(new MockResponse().setResponseCode(503));
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setHeader("Content-Type", "application/json")
            .setBody("{\"id\": \"001\", \"name\": \"성공\"}"));

        StepVerifier.create(apiClient.getDataWithRetry("001"))
            .assertNext(data -> assertThat(data.getName()).isEqualTo("성공"))
            .verifyComplete();

        assertThat(mockWebServer.getRequestCount()).isEqualTo(2);
    }
}
```

### 16.5.3 RecordedRequest로 요청 검증

`MockWebServer`는 수신한 요청을 기록하므로, 클라이언트가 올바른 요청을 보냈는지 검증할 수 있다.

```java
@Test
void 요청_내용_검증() throws InterruptedException {
    mockWebServer.enqueue(new MockResponse()
        .setResponseCode(201)
        .setHeader("Content-Type", "application/json")
        .setBody("{\"id\": \"new-001\"}"));

    CreateRequest request = new CreateRequest("새 데이터", 100);
    StepVerifier.create(apiClient.createData(request))
        .assertNext(result -> assertThat(result.getId()).isEqualTo("new-001"))
        .verifyComplete();

    RecordedRequest recorded = mockWebServer.takeRequest();
    assertThat(recorded.getMethod()).isEqualTo("POST");
    assertThat(recorded.getPath()).isEqualTo("/api/data");
    assertThat(recorded.getHeader("Content-Type"))
        .contains("application/json");

    String body = recorded.getBody().readUtf8();
    assertThat(body).contains("\"name\":\"새 데이터\"");
    assertThat(body).contains("\"value\":100");
}
```

### 16.5.4 실전 예제: 외부 결제 API 모킹

```java
class PaymentGatewayClientTest {

    private MockWebServer mockWebServer;
    private PaymentGatewayClient paymentClient;

    @BeforeEach
    void setUp() throws IOException {
        mockWebServer = new MockWebServer();
        mockWebServer.start();
        WebClient webClient = WebClient.builder()
            .baseUrl(mockWebServer.url("/").toString()).build();
        paymentClient = new PaymentGatewayClient(webClient);
    }

    @AfterEach
    void tearDown() throws IOException { mockWebServer.shutdown(); }

    @Test
    void 결제_승인_성공() throws InterruptedException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setHeader("Content-Type", "application/json")
            .setBody("""
                {"transactionId": "TXN-12345", "status": "APPROVED",
                 "approvedAmount": 50000}
                """));

        PaymentRequest request = PaymentRequest.builder()
            .orderId("ORD-001").amount(new BigDecimal("50000")).build();

        StepVerifier.create(paymentClient.processPayment(request))
            .assertNext(response -> {
                assertThat(response.getTransactionId()).isEqualTo("TXN-12345");
                assertThat(response.getStatus()).isEqualTo("APPROVED");
            })
            .verifyComplete();

        RecordedRequest recorded = mockWebServer.takeRequest();
        assertThat(recorded.getMethod()).isEqualTo("POST");
        assertThat(recorded.getPath()).isEqualTo("/api/payments/approve");
    }

    @Test
    void 결제_게이트웨이_장애_시_재시도() {
        mockWebServer.enqueue(new MockResponse().setResponseCode(500));
        mockWebServer.enqueue(new MockResponse().setResponseCode(500));
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setHeader("Content-Type", "application/json")
            .setBody("""
                {"transactionId": "TXN-12347", "status": "APPROVED",
                 "approvedAmount": 30000}
                """));

        PaymentRequest request = PaymentRequest.builder()
            .orderId("ORD-003").amount(new BigDecimal("30000")).build();

        StepVerifier.create(paymentClient.processPaymentWithRetry(request))
            .assertNext(r -> assertThat(r.getStatus()).isEqualTo("APPROVED"))
            .verifyComplete();

        assertThat(mockWebServer.getRequestCount()).isEqualTo(3);
    }
}
```

---

## 16.6 테스트 슬라이스

### 16.6.1 테스트 슬라이스란?

Spring Boot의 **테스트 슬라이스(Test Slice)**는 애플리케이션의 특정 계층만 로드하여 테스트하는 기법이다. 전체 컨텍스트를 로드하는 `@SpringBootTest`보다 빠르고, 테스트 대상 계층에 집중할 수 있다.

| 어노테이션 | 테스트 대상 | 로드 범위 |
|-----------|-----------|----------|
| `@WebFluxTest` | 컨트롤러 (웹 계층) | WebFlux 관련 빈만 |
| `@DataMongoTest` | MongoDB 리포지토리 | MongoDB 관련 빈만 |
| `@SpringBootTest` | 전체 통합 | 모든 빈 |

### 16.6.2 @WebFluxTest

`@WebFluxTest`는 웹 계층만 로드한다. 서비스와 리포지토리는 로드하지 않으므로 `@MockBean`으로 모킹해야 한다.

```java
@WebFluxTest(controllers = ProductController.class)
class ProductControllerSliceTest {

    @Autowired
    private WebTestClient webTestClient;

    @MockBean
    private ProductService productService;

    @Test
    void 상품_조회_컨트롤러_테스트() {
        when(productService.findById("prod-001"))
            .thenReturn(Mono.just(Product.builder()
                .id("prod-001").name("테스트 상품")
                .price(new BigDecimal("25000")).build()));

        webTestClient.get()
            .uri("/api/products/{id}", "prod-001")
            .exchange()
            .expectStatus().isOk()
            .expectBody()
            .jsonPath("$.name").isEqualTo("테스트 상품");

        verify(productService).findById("prod-001");
    }
}
```

### 16.6.3 @SpringBootTest 전체 통합 테스트

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class FullIntegrationTest {

    @Container
    static MongoDBContainer mongoDBContainer = new MongoDBContainer("mongo:7.0");

    @DynamicPropertySource
    static void setProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.mongodb.uri",
            mongoDBContainer::getReplicaSetUrl);
    }

    @Autowired
    private WebTestClient webTestClient;

    @Autowired
    private ProductRepository productRepository;

    @BeforeEach
    void setUp() { productRepository.deleteAll().block(); }

    @Test
    void 상품_CRUD_전체_흐름() {
        // CREATE
        Product created = webTestClient.post()
            .uri("/api/products")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(new ProductRequest(
                "CRUD 테스트", "설명", "BOOKS", new BigDecimal("30000")))
            .exchange()
            .expectStatus().isCreated()
            .expectBody(Product.class)
            .returnResult().getResponseBody();

        assertThat(created).isNotNull();

        // READ
        webTestClient.get()
            .uri("/api/products/{id}", created.getId())
            .exchange()
            .expectStatus().isOk()
            .expectBody()
            .jsonPath("$.name").isEqualTo("CRUD 테스트");

        // UPDATE
        webTestClient.put()
            .uri("/api/products/{id}", created.getId())
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(new ProductRequest(
                "수정됨", "설명", "BOOKS", new BigDecimal("35000")))
            .exchange()
            .expectStatus().isOk()
            .expectBody()
            .jsonPath("$.name").isEqualTo("수정됨");

        // DELETE
        webTestClient.delete()
            .uri("/api/products/{id}", created.getId())
            .exchange()
            .expectStatus().isNoContent();

        webTestClient.get()
            .uri("/api/products/{id}", created.getId())
            .exchange()
            .expectStatus().isNotFound();
    }
}
```

### 16.6.4 Mockito와 @MockBean 활용 팁

리액티브 환경에서 Mockito를 사용할 때 주의할 점을 정리한다.

```java
@WebFluxTest(OrderController.class)
class OrderControllerTest {

    @Autowired
    private WebTestClient webTestClient;

    @MockBean
    private OrderService orderService;

    @Test
    void Mono_반환_모킹() {
        when(orderService.findById("order-001"))
            .thenReturn(Mono.just(OrderResponse.builder()
                .id("order-001").status("COMPLETED").build()));

        webTestClient.get()
            .uri("/api/orders/{id}", "order-001")
            .exchange()
            .expectStatus().isOk()
            .expectBody()
            .jsonPath("$.status").isEqualTo("COMPLETED");
    }

    @Test
    void Mono_Void_반환_모킹() {
        when(orderService.cancel("order-001")).thenReturn(Mono.empty());

        webTestClient.delete()
            .uri("/api/orders/{id}", "order-001")
            .exchange()
            .expectStatus().isNoContent();

        verify(orderService).cancel("order-001");
    }

    @Test
    void ArgumentCaptor_활용() {
        when(orderService.create(any(OrderRequest.class)))
            .thenReturn(Mono.just(OrderResponse.builder()
                .id("new-order").status("PENDING").build()));

        webTestClient.post()
            .uri("/api/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(OrderRequest.builder()
                .productId("prod-001").quantity(2)
                .shippingAddress("서울시 강남구").build())
            .exchange()
            .expectStatus().isCreated();

        ArgumentCaptor<OrderRequest> captor =
            ArgumentCaptor.forClass(OrderRequest.class);
        verify(orderService).create(captor.capture());
        assertThat(captor.getValue().getProductId()).isEqualTo("prod-001");
    }
}
```

### 16.6.5 테스트 전략 종합 정리

```
┌─────────────────────────────────────────────────────────┐
│             @SpringBootTest (전체 통합 테스트)            │
│    - 전체 흐름 검증, E2E 시나리오                        │
│    - Testcontainers로 실제 MongoDB 사용                 │
├────────────────────────┬────────────────────────────────┤
│   @WebFluxTest         │    @DataMongoTest              │
│   (컨트롤러 슬라이스)    │    (리포지토리 슬라이스)         │
│   - HTTP 요청/응답 검증 │    - 쿼리 메서드 검증           │
│   - @MockBean 서비스   │    - Embedded MongoDB 또는     │
│     모킹              │      Testcontainers 사용       │
├────────────────────────┴────────────────────────────────┤
│          StepVerifier + Mockito (순수 단위 테스트)        │
│   - 서비스 계층 비즈니스 로직 검증                        │
│   - Spring 컨텍스트 로드 없음, 가장 빠름                  │
├─────────────────────────────────────────────────────────┤
│           MockWebServer (외부 API 모킹)                  │
│   - WebClient를 통한 외부 API 호출 검증                   │
└─────────────────────────────────────────────────────────┘
```

| 테스트 유형 | 속도 | 신뢰성 | 사용 시점 |
|------------|------|--------|----------|
| StepVerifier + Mockito | 매우 빠름 | 낮음 | 비즈니스 로직 단위 검증 |
| @WebFluxTest | 빠름 | 중간 | 컨트롤러 요청/응답 검증 |
| @DataMongoTest | 보통 | 중간 | 쿼리 메서드 검증 |
| MockWebServer | 빠름 | 중간 | 외부 API 연동 검증 |
| @SpringBootTest | 느림 | 높음 | 전체 흐름 E2E 검증 |

권장하는 테스트 비율(테스트 피라미드)은 다음과 같다.

- **단위 테스트(StepVerifier + Mockito)**: 70% -- 빠르게 많이 작성
- **슬라이스 테스트(@WebFluxTest, @DataMongoTest)**: 20% -- 계층별 검증
- **통합 테스트(@SpringBootTest)**: 10% -- 핵심 시나리오만

### 16.6.6 테스트 작성 시 주의사항

**1. block()은 테스트 준비 단계에서만 사용한다**

```java
// 올바른 사용: @BeforeEach에서만 block()
@BeforeEach
void setUp() {
    productRepository.deleteAll().block();
}

// 잘못된 사용: 검증 로직에서 block()
@Test
void 잘못된_테스트() {
    Product result = productService.findById("001").block();  // 안티패턴
    assertThat(result.getName()).isEqualTo("상품");
}

// 올바른 사용: StepVerifier로 검증
@Test
void 올바른_테스트() {
    StepVerifier.create(productService.findById("001"))
        .assertNext(p -> assertThat(p.getName()).isEqualTo("상품"))
        .verifyComplete();
}
```

**2. verify() 호출을 잊지 않는다**

```java
// 이 테스트는 항상 통과한다 -- 구독이 시작되지 않음!
@Test
void 잘못된_테스트() {
    StepVerifier.create(productService.findById("unknown"))
        .expectError(NotFoundException.class);
    // verify() 호출 누락!
}
```

**3. @MockBean과 @Mock의 차이를 이해한다**

| 어노테이션 | 컨텍스트 | 사용 위치 |
|-----------|---------|----------|
| `@Mock` | Spring 컨텍스트 없음 | `@ExtendWith(MockitoExtension.class)` 테스트 |
| `@MockBean` | Spring 컨텍스트 내 빈 대체 | `@WebFluxTest`, `@SpringBootTest` 등 |

---

## 요약

이번 장에서는 리액티브 애플리케이션의 테스트 전략을 계층별로 다루었다.

| 주제 | 핵심 내용 |
|------|----------|
| **StepVerifier** | `expectNext`, `assertNext`, `expectError`로 Mono/Flux 시퀀스를 단계별 검증. `withVirtualTime()`으로 시간 의존 테스트 |
| **WebTestClient** | `bindToController`(격리), `bindToApplicationContext`(통합)으로 HTTP 엔드포인트 테스트. `jsonPath()`로 JSON 검증 |
| **Embedded MongoDB** | `@DataMongoTest`로 리포지토리 슬라이스 테스트. JVM 내 MongoDB 인스턴스로 빠른 테스트 |
| **Testcontainers** | `@Testcontainers`, `@Container`, `@DynamicPropertySource`로 실제 MongoDB Docker 컨테이너 사용. 프로덕션 호환성 보장 |
| **MockWebServer** | `MockResponse`로 외부 API 응답 시뮬레이션. `RecordedRequest`로 전송된 요청 검증 |
| **테스트 슬라이스** | `@WebFluxTest`(웹), `@DataMongoTest`(DB), `@SpringBootTest`(전체). Mockito로 의존성 모킹 |

리액티브 테스트에서 가장 중요한 원칙은 **`block()`으로 동기 변환하지 않고 `StepVerifier`로 비동기 시퀀스를 검증하는 것**이다. 각 계층에 적합한 테스트 도구를 선택하여 빠르면서도 신뢰성 높은 테스트 스위트를 구축하자.

다음 장에서는 SpringDoc OpenAPI를 활용한 리액티브 API 문서화와 버전 관리 전략을 다룬다.
# Chapter 17. 문서화와 API 관리

API를 잘 만드는 것 못지않게 중요한 것이 **잘 문서화하는 것**이다. 아무리 훌륭한 리액티브 API를 설계하더라도, 소비자(프론트엔드 개발자, 외부 파트너, 내부 팀)가 그 사용법을 쉽게 파악할 수 없다면 실용적 가치가 반감된다. 이번 장에서는 Spring WebFlux 환경에서 SpringDoc OpenAPI(Swagger)를 활용한 API 문서 자동 생성, `Mono`/`Flux` 반환 타입과 `RouterFunction`의 문서화, 그리고 API 버전 관리 전략까지 실전에서 필요한 내용을 다룬다.

---

## 17.1 SpringDoc OpenAPI(Swagger) 연동

### 17.1.1 SpringDoc OpenAPI란?

SpringDoc OpenAPI는 Spring Boot 애플리케이션에서 **OpenAPI 3.0/3.1 명세**를 자동으로 생성해주는 라이브러리다. 과거에는 Springfox(Swagger 2)가 널리 사용되었지만, Spring Boot 3.x 이후로는 SpringDoc이 사실상 표준으로 자리잡았다.

| 구분 | Springfox | SpringDoc |
|------|-----------|-----------|
| **OpenAPI 버전** | Swagger 2.0 | OpenAPI 3.0/3.1 |
| **Spring Boot 3 지원** | 미지원 | 지원 |
| **WebFlux 지원** | 제한적 | 네이티브 지원 |
| **유지보수 상태** | 사실상 중단 | 활발히 유지보수 |
| **RouterFunction 지원** | 미지원 | 지원 |

### 17.1.2 의존성 설정

WebFlux 환경에서는 `springdoc-openapi-starter-webflux-ui` 의존성을 추가한다. 일반 MVC용인 `springdoc-openapi-starter-webmvc-ui`와 혼동하지 않도록 주의한다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    implementation 'org.springframework.boot:spring-boot-starter-data-mongodb-reactive'

    // SpringDoc OpenAPI - WebFlux 전용
    implementation 'org.springdoc:springdoc-openapi-starter-webflux-ui:2.8.4'
}
```

의존성을 추가하는 것만으로 다음 두 엔드포인트가 자동으로 활성화된다.

| 엔드포인트 | 설명 |
|-----------|------|
| `/v3/api-docs` | OpenAPI 3.0 JSON 명세 |
| `/swagger-ui.html` | Swagger UI 웹 인터페이스 |

### 17.1.3 기본 설정

`application.yml`에서 SpringDoc의 동작을 세밀하게 제어할 수 있다.

```yaml
springdoc:
  api-docs:
    path: /v3/api-docs
    enabled: true
  swagger-ui:
    path: /swagger-ui.html
    enabled: true
    operations-sorter: method
    tags-sorter: alpha
    display-request-duration: true
  default-produces-media-type: application/json
  default-consumes-media-type: application/json
  show-actuator: false
```

운영 환경에서는 보안상 Swagger UI를 비활성화하는 것이 일반적이다.

```yaml
# application-prod.yml
springdoc:
  api-docs:
    enabled: false
  swagger-ui:
    enabled: false
```

### 17.1.4 OpenAPI 전역 설정 빈

API 문서의 제목, 설명, 버전 등 전역 정보를 `OpenAPI` 빈으로 정의한다.

```java
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("상품 관리 API")
                .description("Spring WebFlux + MongoDB 기반 리액티브 상품 관리 시스템")
                .version("1.0.0")
                .contact(new Contact()
                    .name("개발팀")
                    .email("dev@example.com"))
                .license(new License()
                    .name("Apache 2.0")
                    .url("https://www.apache.org/licenses/LICENSE-2.0")))
            .externalDocs(new ExternalDocumentation()
                .description("프로젝트 위키")
                .url("https://wiki.example.com/product-api"));
    }
}
```

### 17.1.5 @Operation과 @ApiResponse

컨트롤러 메서드에 `@Operation`을 붙여 개별 API의 설명을 추가하고, `@ApiResponse`로 응답 코드별 설명을 명시한다.

```java
@RestController
@RequestMapping("/api/v1/products")
@Tag(name = "상품", description = "상품 CRUD API")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @Operation(summary = "상품 목록 조회",
               description = "등록된 모든 상품을 페이징하여 조회한다.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "조회 성공",
            content = @Content(mediaType = "application/json",
                array = @ArraySchema(schema = @Schema(implementation = ProductResponse.class))))
    })
    @GetMapping
    public Flux<ProductResponse> getAllProducts(
            @Parameter(description = "페이지 번호 (0부터 시작)", example = "0")
            @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "페이지 크기", example = "20")
            @RequestParam(defaultValue = "20") int size) {
        return productService.findAll(page, size);
    }

    @Operation(summary = "상품 단건 조회",
               description = "상품 ID로 단건 조회한다. 존재하지 않으면 404를 반환한다.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "조회 성공"),
        @ApiResponse(responseCode = "404", description = "상품을 찾을 수 없음",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @GetMapping("/{id}")
    public Mono<ProductResponse> getProduct(
            @Parameter(description = "상품 ID", required = true,
                       example = "665a1b2c3d4e5f6a7b8c9d0e")
            @PathVariable String id) {
        return productService.findById(id);
    }

    @Operation(summary = "상품 등록")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "등록 성공"),
        @ApiResponse(responseCode = "400", description = "유효성 검증 실패")
    })
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<ProductResponse> createProduct(
            @Valid @RequestBody ProductCreateRequest request) {
        return productService.create(request);
    }
}
```

### 17.1.6 @Schema를 활용한 모델 문서화

요청/응답 DTO에 `@Schema`를 적용하면 Swagger UI에서 각 필드의 의미, 필수 여부, 예시 값을 확인할 수 있다.

```java
@Schema(description = "상품 등록 요청")
public record ProductCreateRequest(

    @Schema(description = "상품명", example = "무선 키보드",
            requiredMode = RequiredMode.REQUIRED)
    @NotBlank(message = "상품명은 필수입니다")
    String name,

    @Schema(description = "가격 (원)", example = "45000", minimum = "0")
    @NotNull @Positive
    Integer price,

    @Schema(description = "카테고리", example = "ELECTRONICS",
            allowableValues = {"ELECTRONICS", "CLOTHING", "FOOD", "BOOKS"})
    @NotNull
    Category category,

    @Schema(description = "태그 목록", example = "[\"bluetooth\", \"keyboard\"]")
    List<String> tags
) {}
```

```java
@Schema(description = "상품 응답")
public record ProductResponse(

    @Schema(description = "상품 ID", example = "665a1b2c3d4e5f6a7b8c9d0e")
    String id,

    @Schema(description = "상품명", example = "무선 키보드")
    String name,

    @Schema(description = "가격 (원)", example = "45000")
    Integer price,

    @Schema(description = "카테고리")
    Category category,

    @Schema(description = "등록일시", example = "2025-01-15T10:30:00")
    LocalDateTime createdAt
) {}
```

---

## 17.2 리액티브 API 문서 자동 생성

### 17.2.1 Mono/Flux 반환 타입 처리

SpringDoc은 리액티브 타입을 자동으로 인식하여, 래핑된 내부 타입을 기준으로 스키마를 생성한다.

| 메서드 반환 타입 | OpenAPI 스키마 |
|----------------|---------------|
| `Mono<Product>` | `Product` (단일 객체) |
| `Flux<Product>` | `Product[]` (배열) |
| `Mono<Void>` | 응답 본문 없음 |
| `Mono<ResponseEntity<Product>>` | `Product` + 상태 코드 |
| `Flux<ServerSentEvent<Product>>` | SSE 스트림으로 표현 |

**스트리밍 응답**의 경우 `produces` 미디어 타입을 명시하는 것이 좋다.

```java
@Operation(summary = "상품 실시간 스트림")
@GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ProductResponse> streamProducts() {
    return productService.streamAll();
}
```

### 17.2.2 RouterFunction 문서화

함수형 라우터(`RouterFunction`)는 리플렉션으로 메타데이터를 추출할 수 없다. SpringDoc은 `@RouterOperation` 어노테이션과 `OpenApiCustomizer` 두 가지 방식을 제공한다.

**방법 1: @RouterOperation 어노테이션**

```java
@Configuration
public class ProductRouter {

    @RouterOperations({
        @RouterOperation(
            path = "/api/v1/products", method = RequestMethod.GET,
            beanClass = ProductHandler.class, beanMethod = "getAllProducts",
            operation = @Operation(
                operationId = "getAllProducts", summary = "상품 목록 조회",
                tags = {"상품"},
                responses = @ApiResponse(responseCode = "200",
                    description = "조회 성공",
                    content = @Content(array = @ArraySchema(
                        schema = @Schema(implementation = ProductResponse.class)))))),
        @RouterOperation(
            path = "/api/v1/products/{id}", method = RequestMethod.GET,
            beanClass = ProductHandler.class, beanMethod = "getProduct",
            operation = @Operation(
                operationId = "getProduct", summary = "상품 단건 조회",
                tags = {"상품"},
                parameters = @Parameter(in = ParameterIn.PATH, name = "id",
                    description = "상품 ID", required = true),
                responses = {
                    @ApiResponse(responseCode = "200", description = "조회 성공"),
                    @ApiResponse(responseCode = "404", description = "상품을 찾을 수 없음")}))
    })
    @Bean
    public RouterFunction<ServerResponse> productRoutes(ProductHandler handler) {
        return RouterFunctions.route()
            .path("/api/v1/products", builder -> builder
                .GET("", handler::getAllProducts)
                .GET("/{id}", handler::getProduct))
            .build();
    }
}
```

**방법 2: OpenApiCustomizer 프로그래밍 방식**

라우트가 많거나, 문서 정보를 코드로 관리하고 싶을 때는 `OpenApiCustomizer` 빈에서 `openApi.getPaths().addPathItem()`을 호출하여 경로와 오퍼레이션을 프로그래밍 방식으로 등록한다.

### 17.2.3 SecurityScheme 설정

JWT 인증을 사용하는 API의 경우, Swagger UI에서 토큰을 입력하여 인증된 요청을 테스트할 수 있도록 `SecurityScheme`을 설정한다.

```java
@Bean
public OpenAPI customOpenAPI() {
    final String securitySchemeName = "bearerAuth";

    return new OpenAPI()
        .info(new Info().title("상품 관리 API").version("1.0.0"))
        .addSecurityItem(new SecurityRequirement().addList(securitySchemeName))
        .components(new Components()
            .addSecuritySchemes(securitySchemeName,
                new SecurityScheme()
                    .name(securitySchemeName)
                    .type(SecurityScheme.Type.HTTP)
                    .scheme("bearer")
                    .bearerFormat("JWT")
                    .description("JWT 토큰을 입력하세요.")));
}
```

특정 엔드포인트에만 보안을 적용하거나 제외하려면 `@SecurityRequirement`를 메서드 레벨에서 사용한다.

```java
// 인증이 필요한 엔드포인트
@Operation(summary = "상품 등록",
           security = @SecurityRequirement(name = "bearerAuth"))
@PostMapping
public Mono<ProductResponse> createProduct(@Valid @RequestBody ProductCreateRequest req) {
    return productService.create(req);
}

// 인증이 필요 없는 엔드포인트 (전역 보안 설정 무시)
@Operation(summary = "상품 목록 조회", security = {})
@GetMapping
public Flux<ProductResponse> getAllProducts() {
    return productService.findAll();
}
```

### 17.2.4 그룹(Group)별 문서 분리

대규모 프로젝트에서는 API를 도메인별로 그룹화하여 별도의 문서로 분리한다.

```java
@Configuration
public class OpenApiGroupConfig {

    @Bean
    public GroupedOpenApi productApi() {
        return GroupedOpenApi.builder()
            .group("product-api").displayName("상품 API")
            .pathsToMatch("/api/v1/products/**")
            .build();
    }

    @Bean
    public GroupedOpenApi orderApi() {
        return GroupedOpenApi.builder()
            .group("order-api").displayName("주문 API")
            .pathsToMatch("/api/v1/orders/**")
            .build();
    }
}
```

Swagger UI 상단의 드롭다운에서 그룹을 선택하면 해당 그룹의 API만 표시된다.

---

## 17.3 API 버전 관리 전략

### 17.3.1 왜 API 버전 관리가 필요한가?

API는 한번 공개되면 소비자가 존재한다. 기존 소비자의 코드를 깨뜨리지 않으면서 새로운 기능을 추가하거나 구조를 변경해야 하는 상황이 반드시 발생한다. 체계적인 버전 관리 전략이 없으면 기존 클라이언트가 예기치 않게 동작을 멈추고, 어떤 필드가 언제 변경되었는지 추적이 불가능해진다.

### 17.3.2 URL 경로 기반 버전 관리

가장 직관적이고 널리 사용되는 방식이다. URL 경로에 버전 번호를 포함한다.

```java
@RestController
@RequestMapping("/api/v1/products")
@Tag(name = "상품 V1")
public class ProductV1Controller {

    private final ProductService productService;

    public ProductV1Controller(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping("/{id}")
    public Mono<ProductV1Response> getProduct(@PathVariable String id) {
        return productService.findById(id).map(ProductV1Response::from);
    }
}

@RestController
@RequestMapping("/api/v2/products")
@Tag(name = "상품 V2", description = "카테고리 구조 변경")
public class ProductV2Controller {

    private final ProductService productService;

    public ProductV2Controller(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping("/{id}")
    public Mono<ProductV2Response> getProduct(@PathVariable String id) {
        return productService.findById(id).map(ProductV2Response::from);
    }
}
```

버전별 응답 DTO를 분리하여 관리한다.

```java
// V1: 카테고리를 단일 문자열로 표현
public record ProductV1Response(String id, String name, int price, String category) {
    public static ProductV1Response from(Product p) {
        return new ProductV1Response(p.getId(), p.getName(), p.getPrice(),
            p.getCategory().name());
    }
}

// V2: 카테고리를 계층 구조 객체로 표현
public record ProductV2Response(String id, String name, int price,
                                CategoryInfo category, List<String> tags) {
    public record CategoryInfo(String code, String displayName, String parentCode) {}

    public static ProductV2Response from(Product p) {
        return new ProductV2Response(p.getId(), p.getName(), p.getPrice(),
            new CategoryInfo(p.getCategory().name(),
                p.getCategory().getDisplayName(),
                p.getCategory().getParentCode()),
            p.getTags());
    }
}
```

| 장점 | 단점 |
|------|------|
| 직관적이고 이해하기 쉬움 | 컨트롤러가 버전만큼 증가 |
| URL만 보면 버전 파악 가능 | 공통 로직 중복 가능성 |
| 캐싱, 라우팅, 로깅에서 구분 용이 | URL이 길어짐 |

### 17.3.3 헤더 기반 버전 관리

URL을 깨끗하게 유지하면서 커스텀 헤더로 버전을 지정하는 방식이다.

```
GET /api/products
X-API-Version: 2
```

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @Operation(summary = "상품 조회",
        parameters = @Parameter(name = "X-API-Version", in = ParameterIn.HEADER,
            description = "API 버전", required = false,
            schema = @Schema(type = "integer", defaultValue = "1")))
    @GetMapping("/{id}")
    public Mono<?> getProduct(
            @PathVariable String id,
            @RequestHeader(value = "X-API-Version", defaultValue = "1") int version) {
        return productService.findById(id)
            .map(product -> switch (version) {
                case 2 -> ProductV2Response.from(product);
                default -> ProductV1Response.from(product);
            });
    }
}
```

| 장점 | 단점 |
|------|------|
| URL이 깔끔하게 유지됨 | 브라우저에서 직접 테스트 어려움 |
| 동일 리소스에 대한 단일 URL | 캐싱 설정 복잡 (Vary 헤더 필요) |
| 컨트롤러 중복 감소 | 문서화 시 헤더 명시 필요 |

### 17.3.4 미디어 타입(Content Negotiation) 기반 버전 관리

`Accept` 헤더에 버전 정보를 포함하는 방식이다. GitHub API가 대표적으로 이 방식을 사용한다.

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping(value = "/{id}", produces = "application/vnd.example.v1+json")
    @Operation(summary = "상품 조회 (V1)")
    public Mono<ProductV1Response> getProductV1(@PathVariable String id) {
        return productService.findById(id).map(ProductV1Response::from);
    }

    @GetMapping(value = "/{id}", produces = "application/vnd.example.v2+json")
    @Operation(summary = "상품 조회 (V2)")
    public Mono<ProductV2Response> getProductV2(@PathVariable String id) {
        return productService.findById(id).map(ProductV2Response::from);
    }
}
```

커스텀 미디어 타입을 Spring이 JSON으로 처리하도록 `WebFluxConfigurer`의 `configureHttpMessageCodecs`에서 `Jackson2JsonEncoder`와 `Jackson2JsonDecoder`에 해당 미디어 타입을 등록해야 한다.

| 장점 | 단점 |
|------|------|
| RESTful 원칙에 가장 부합 | 구현 복잡도 높음 |
| URL과 헤더 모두 깨끗 | 클라이언트가 Accept 헤더를 올바르게 설정해야 함 |
| HTTP 콘텐츠 협상 표준 활용 | 코덱 설정 필요 |

### 17.3.5 하위 호환성 유지 전략

버전 관리 방식과 관계없이, **하위 호환성(Backward Compatibility)**을 최대한 유지하는 것이 가장 좋은 전략이다. 새 버전을 만드는 것은 최후의 수단으로 남겨두어야 한다.

**하위 호환이 유지되는 변경 (Non-Breaking)**

| 변경 유형 | 예시 |
|----------|------|
| 응답 필드 추가 | `tags` 필드 추가 (기존 클라이언트는 무시) |
| 선택적 요청 파라미터 추가 | `?sortBy=name` (기존 요청에 영향 없음) |
| 새 엔드포인트 추가 | `POST /api/v1/products/bulk` |

**하위 호환이 깨지는 변경 (Breaking)**

| 변경 유형 | 예시 |
|----------|------|
| 응답 필드 제거/타입 변경 | `price: int` -> `price: object` |
| 필수 파라미터 추가 | `?category` 필수로 변경 |
| URL 구조 변경 | `/products/{id}` -> `/items/{id}` |

**Deprecation 정책 구현**

API 필드나 엔드포인트를 제거할 때는 충분한 유예 기간을 두고 사전 고지한다.

```java
@GetMapping("/{id}")
public Mono<ResponseEntity<ProductV1Response>> getProductV1(@PathVariable String id) {
    return productService.findById(id)
        .map(ProductV1Response::from)
        .map(response -> ResponseEntity.ok()
            .header("Deprecation", "true")
            .header("Sunset", "2026-06-01T00:00:00Z")
            .header("Link", "</api/v2/products>; rel=\"successor-version\"")
            .body(response));
}
```

### 17.3.6 버전 관리 전략 비교 및 권장사항

| 기준 | URL 경로 | 헤더 | 미디어 타입 |
|------|---------|------|-----------|
| **구현 난이도** | 쉬움 | 보통 | 어려움 |
| **직관성** | 높음 | 낮음 | 낮음 |
| **RESTful 준수** | 보통 | 보통 | 높음 |
| **캐싱 용이성** | 높음 | 낮음 | 보통 |
| **대표 사용 사례** | Stripe, Twitter | Azure | GitHub |

**실전 권장 가이드라인**

1. **URL 경로 기반을 기본으로 사용한다.** 가장 직관적이고, 디버깅과 모니터링이 쉽다.
2. **하위 호환 변경은 버전을 올리지 않는다.** 필드 추가, 선택 파라미터 추가 등은 기존 버전에 적용한다.
3. **Breaking Change가 불가피할 때만 새 버전을 생성한다.**
4. **이전 버전은 최소 6개월 이상 유지한다.** Sunset 헤더로 종료 일자를 사전 고지한다.
5. **동시에 유지하는 버전은 최대 2개로 제한한다.** 3개 이상은 유지보수 비용이 기하급수적으로 증가한다.

---

## 17.4 정리

이번 장에서 다룬 핵심 내용을 요약한다.

| 주제 | 핵심 내용 |
|------|----------|
| **SpringDoc 연동** | `springdoc-openapi-starter-webflux-ui` 의존성 추가만으로 자동 문서 생성 |
| **어노테이션 활용** | `@Operation`, `@Parameter`, `@ApiResponse`, `@Schema`로 상세 문서화 |
| **리액티브 타입** | `Mono`/`Flux`를 자동 인식하여 내부 타입 기준으로 스키마 생성 |
| **RouterFunction** | `@RouterOperation` 또는 `OpenApiCustomizer`로 문서화 |
| **SecurityScheme** | JWT Bearer 인증을 Swagger UI에서 테스트 가능하도록 설정 |
| **버전 관리** | URL 경로 기반이 가장 실용적, 하위 호환성 유지가 최우선 |

API 문서화와 버전 관리는 기술적 완성도보다 **개발 조직의 규율과 일관성**이 더 중요한 영역이다. 도구가 아무리 좋아도 팀 전체가 문서화 원칙을 지키지 않으면 무용지물이다. 다음 장에서는 프로덕션 환경에서 애플리케이션의 상태를 모니터링하고 관찰하기 위한 **Observability** 전략을 다룬다.
