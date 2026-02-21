# Chapter 8. MongoDB 리액티브 데이터 접근 심화

Chapter 6에서 `ReactiveMongoRepository`의 기본 CRUD 구현을 다뤘으니, 이제 더 복잡한 실무 요구사항에 대응할 차례다. 이 장에서 중심을 두는 것은 `ReactiveMongoTemplate`인데, 이것이 있어야만 MongoDB의 고급 기능을 리액티브 방식으로 제대로 활용할 수 있다. 동적 쿼리 구성(Criteria API), 복잡한 통계 작업(Aggregation Pipeline), 데이터 변경 감시(Change Streams), 트랜잭션 처리, 인덱스 설계와 성능 최적화 같은 실전 주제들을 다루면서, 프로덕션 환경에서 실제로 마주치는 시나리오에 집중해보자.

---

## 8.1 ReactiveMongoTemplate 활용

### 8.1.1 ReactiveMongoTemplate vs ReactiveMongoRepository

`ReactiveMongoRepository`는 정말 편하다. 메서드 이름만 써도 쿼리가 자동으로 생성되고 기본 CRUD도 다 제공한다. 하지만 복잡한 조건의 쿼리, 특정 필드만 선택적으로 수정해야 하는 경우, 통계나 집계, 그리고 데이터 변경을 실시간으로 감시해야 하는 요구사항이 생기면 `ReactiveMongoTemplate`이 필요해진다. 필자의 경험상 프로덕션 시스템에서는 이 둘을 조합해서 쓰는 것이 가장 효율적이다.

| 비교 항목 | ReactiveMongoRepository | ReactiveMongoTemplate |
|-----------|------------------------|----------------------|
| **추상화 수준** | 높음 (인터페이스 선언만으로 사용) | 낮음 (직접 Query/Update 객체 구성) |
| **기본 CRUD** | 자동 제공 | 직접 구현 |
| **부분 업데이트** | 미지원 (전체 도큐먼트 교체) | `Update` 객체로 특정 필드만 수정 |
| **Upsert / Aggregation** | 미지원 | `upsert()`, `aggregate()` 제공 |
| **Change Streams** | 미지원 | `changeStream()` 메서드 제공 |
| **동적 쿼리** | 제한적 (`@Query` + SpEL) | `Criteria`로 자유롭게 조합 |

실제로 프로젝트에서 두 가지를 함께 사용할 때 패턴이 명확해진다. 간단한 CRUD 작업은 `ReactiveMongoRepository`로 깔끔하게 처리하고, 복잡한 쿼리나 특수한 요구사항이 있는 부분에서만 `ReactiveMongoTemplate`을 주입받아 사용하는 식이다.

### 8.1.2 ReactiveMongoTemplate 기본 CRUD

좋은 소식은 `ReactiveMongoTemplate`이 Spring Boot의 자동 설정에 포함되어 있다는 것이다. 따라서 특별한 설정 없이 주입받기만 하면 바로 사용할 수 있다.

```java
@Service
@RequiredArgsConstructor
public class ProductQueryService {

    private final ReactiveMongoTemplate mongoTemplate;

    public Flux<Product> findAll() {
        return mongoTemplate.findAll(Product.class);
    }

    public Mono<Product> findById(String id) {
        return mongoTemplate.findById(id, Product.class);
    }

    public Flux<Product> findByCategory(String category) {
        Query query = Query.query(Criteria.where("category").is(category));
        return mongoTemplate.find(query, Product.class);
    }

    public Mono<Product> insert(Product product) {
        return mongoTemplate.insert(product);
    }

    public Mono<DeleteResult> deleteById(String id) {
        Query query = Query.query(Criteria.where("id").is(id));
        return mongoTemplate.remove(query, Product.class);
    }
}
```

### 8.1.3 Query와 Update 객체

실제 쿼리를 작성할 때는 `Query` 객체와 `Update` 객체를 다루게 된다. 전자는 "어떤 도큐먼트를 찾을 것인가"를 정의하고, 후자는 "어떤 필드를 어떻게 수정할 것인가"를 담당한다.

```java
// 특정 필드만 업데이트 (부분 업데이트)
public Mono<UpdateResult> updatePrice(String productId, BigDecimal newPrice) {
    Query query = Query.query(Criteria.where("id").is(productId));
    Update update = new Update()
        .set("price", newPrice)
        .set("updatedAt", LocalDateTime.now());
    return mongoTemplate.updateFirst(query, update, Product.class);
}

// 조건에 맞는 모든 도큐먼트 업데이트
public Mono<UpdateResult> applyDiscount(String category, int discountPercent) {
    Query query = Query.query(Criteria.where("category").is(category));
    Update update = new Update()
        .mul("price", (100 - discountPercent) / 100.0)
        .set("updatedAt", LocalDateTime.now());
    return mongoTemplate.updateMulti(query, update, Product.class);
}
```

`Update` 객체의 주요 메서드는 다음과 같다.

| 메서드 | MongoDB 연산자 | 설명 |
|--------|---------------|------|
| `set(key, value)` | `$set` | 필드 값 설정 |
| `unset(key)` | `$unset` | 필드 제거 |
| `inc(key, value)` | `$inc` | 숫자 증가/감소 |
| `push(key, value)` | `$push` | 배열에 요소 추가 |
| `pull(key, value)` | `$pull` | 배열에서 요소 제거 |
| `addToSet(key, value)` | `$addToSet` | 배열에 중복 없이 추가 |
| `min(key, value)` / `max(key, value)` | `$min` / `$max` | 현재 값과 비교하여 갱신 |

### 8.1.4 Upsert와 findAndModify

여기서 정말 유용한 두 가지 패턴을 소개하려고 한다. 먼저 `upsert`는 "있으면 수정하고, 없으면 생성해"라는 요구사항을 한 번에 처리할 수 있는 원자적 연산이다. `findAndModify()`는 다르게, 도큐먼트를 수정한 후 그 결과를 바로 반환하기 때문에 "방금 수정한 상태"를 즉시 확인해야 할 때 쓸모가 있다. 필자의 경험상 이 두 메서드는 재고 관리나 카운터 증감 같은 시나리오에서 정말 자주 사용된다.

```java
// Upsert: 조회수 카운터 — 없으면 생성, 있으면 증가
public Mono<UpdateResult> incrementViewCount(String productId) {
    Query query = Query.query(Criteria.where("productId").is(productId));
    Update update = new Update()
        .inc("viewCount", 1)
        .setOnInsert("productId", productId)
        .setOnInsert("createdAt", LocalDateTime.now());
    return mongoTemplate.upsert(query, update, "product_views");
}

// findAndModify: 재고 차감 — 원자적으로 수행하고 수정된 결과 반환
public Mono<Product> decrementStock(String productId, int quantity) {
    Query query = Query.query(
        Criteria.where("id").is(productId).and("stock").gte(quantity)
    );
    Update update = new Update().inc("stock", -quantity);
    FindAndModifyOptions options = FindAndModifyOptions.options()
        .returnNew(true)
        .upsert(false);
    return mongoTemplate.findAndModify(query, update, options, Product.class);
}
```

`setOnInsert()`는 도큐먼트가 새로 삽입될 때만 적용되는 필드를 지정한다. MongoDB의 `$setOnInsert` 연산자에 대응한다.

---

## 8.2 커스텀 쿼리와 Criteria API

### 8.2.1 Criteria 기본 사용법

이제 본격적으로 동적 쿼리를 만들어보자. `Criteria`라는 클래스를 사용하면, MongoDB의 복잡한 쿼리 문법을 자바스럽게 빌더 패턴으로 구성할 수 있다.

```java
Criteria.where("category").is("electronics");       // 등호
Criteria.where("price").gte(10000).lte(50000);       // 범위
Criteria.where("description").exists(true);           // 존재 여부
Criteria.where("deletedAt").isNull();                 // null 체크
```

주요 비교 메서드는 다음과 같다.

| 메서드 | MongoDB 연산자 | 의미 |
|--------|---------------|------|
| `is` / `ne` | `$eq` / `$ne` | 같음 / 같지 않음 |
| `gt` / `gte` / `lt` / `lte` | `$gt` / `$gte` / `$lt` / `$lte` | 비교 연산 |
| `in` / `nin` | `$in` / `$nin` | 포함 / 미포함 |
| `regex(pattern)` | `$regex` | 정규표현식 매칭 |
| `exists(boolean)` | `$exists` | 필드 존재 여부 |

### 8.2.2 복잡한 조건 조합 (and/or/in/regex)

실무에서는 사용자의 검색 조건이 복합적이어서 여러 논리 연산자를 조합해야 한다. 다음 예제들이 자주 나타나는 패턴들이다.

```java
// AND 조건 — 체이닝
Query query = Query.query(
    Criteria.where("category").is("electronics")
        .and("price").gte(10000).and("stock").gt(0)
);

// OR 조건
Query query = Query.query(
    new Criteria().orOperator(
        Criteria.where("category").is("electronics"),
        Criteria.where("category").is("books")
    )
);

// AND + OR 혼합
Query query = Query.query(
    new Criteria().orOperator(
        new Criteria().andOperator(
            Criteria.where("category").is("electronics"),
            Criteria.where("price").gte(10000)),
        new Criteria().andOperator(
            Criteria.where("category").is("books"),
            Criteria.where("price").gte(5000))
    )
);

// in, regex, elemMatch
Criteria.where("category").in("electronics", "books", "clothing");
Criteria.where("name").regex("갤럭시", "i");  // 대소문자 무시
Criteria.where("tags").elemMatch(
    Criteria.where("name").is("sale").and("active").is(true)
);
```

### 8.2.3 정렬, 페이징, Projection

검색 결과를 정렬하고 페이징하는 것은 기본이다. 그리고 때론 모든 필드가 필요한 게 아니라 특정 필드만 가져오면 되는 경우도 있는데, 이때 Projection을 사용하면 네트워크 트래픽과 메모리 사용량을 줄일 수 있다.

```java
// 정렬 + 페이징
public Flux<Product> findWithPaging(String category, int page, int size) {
    Query query = Query.query(Criteria.where("category").is(category))
        .with(Sort.by(Sort.Direction.DESC, "createdAt"))
        .skip((long) page * size)
        .limit(size);
    return mongoTemplate.find(query, Product.class);
}

// 전체 건수 조회 (페이징 UI용)
public Mono<Long> countByCategory(String category) {
    Query query = Query.query(Criteria.where("category").is(category));
    return mongoTemplate.count(query, Product.class);
}

// Projection — 필요한 필드만 선택
public Flux<ProductSummary> findSummaries() {
    Query query = new Query();
    query.fields().include("name").include("price").include("category");
    return mongoTemplate.find(query, ProductSummary.class, "products");
}
```

### 8.2.4 동적 쿼리 구성

이 부분이 정말 중요하다. 실무에서는 사용자가 모든 필터를 입력하지 않는다. 카테고리만 선택할 수도 있고, 가격 범위만 선택할 수도 있고, 검색어만 입력할 수도 있다. 따라서 쿼리를 동적으로 구성해야 한다.

```java
@Service
@RequiredArgsConstructor
public class ProductSearchService {

    private final ReactiveMongoTemplate mongoTemplate;

    public Flux<Product> search(ProductSearchCriteria sc) {
        Query query = new Query();

        if (sc.getCategory() != null) {
            query.addCriteria(Criteria.where("category").is(sc.getCategory()));
        }
        if (sc.getMinPrice() != null || sc.getMaxPrice() != null) {
            Criteria price = Criteria.where("price");
            if (sc.getMinPrice() != null) price = price.gte(sc.getMinPrice());
            if (sc.getMaxPrice() != null) price = price.lte(sc.getMaxPrice());
            query.addCriteria(price);
        }
        if (sc.getKeyword() != null) {
            query.addCriteria(Criteria.where("name").regex(sc.getKeyword(), "i"));
        }
        if (Boolean.TRUE.equals(sc.getInStockOnly())) {
            query.addCriteria(Criteria.where("stock").gt(0));
        }

        query.with(Sort.by(
            Sort.Direction.fromString(
                sc.getSortDirection() != null ? sc.getSortDirection() : "DESC"),
            sc.getSortBy() != null ? sc.getSortBy() : "createdAt"
        ));
        query.skip((long) sc.getPage() * sc.getSize()).limit(sc.getSize());

        return mongoTemplate.find(query, Product.class);
    }
}
```

```java
@Data
@Builder
public class ProductSearchCriteria {
    private String category;
    private BigDecimal minPrice;
    private BigDecimal maxPrice;
    private String keyword;
    private Boolean inStockOnly;
    private String sortBy;
    private String sortDirection;
    @Builder.Default private int page = 0;
    @Builder.Default private int size = 20;
}
```

---

## 8.3 Aggregation Pipeline 사용

### 8.3.1 Aggregation Pipeline 개념

이제 정말 흥미로운 부분이다. Aggregation Pipeline은 MongoDB의 강력한 기능으로, 도큐먼트들을 여러 단계를 거쳐 변환하고 집계한다. 마치 데이터가 파이프라인을 따라 흐르면서 각 단계에서 필터링, 그룹핑, 정렬 등을 거치는 것 같다고 생각하면 된다. Spring Data MongoDB는 이 과정을 자바로 깔끔하게 표현할 수 있게 `Aggregation` 클래스를 제공한다.

| 단계 | MongoDB 연산자 | Spring Data 메서드 | 설명 |
|------|---------------|-------------------|------|
| Match | `$match` | `Aggregation.match()` | 도큐먼트 필터링 |
| Group | `$group` | `Aggregation.group()` | 그룹별 집계 |
| Sort | `$sort` | `Aggregation.sort()` | 결과 정렬 |
| Project | `$project` | `Aggregation.project()` | 필드 선택/변환 |
| Unwind | `$unwind` | `Aggregation.unwind()` | 배열 분해 |
| Lookup | `$lookup` | `Aggregation.lookup()` | 컬렉션 조인 |

### 8.3.2 기본 집계: 카테고리별 통계

가장 단순하면서도 유용한 예제부터 보자. 활성 상태의 상품들을 카테고리별로 그룹핑해서 통계를 낸다.

```java
public Flux<CategoryStats> getCategoryStats() {
    Aggregation aggregation = Aggregation.newAggregation(
        Aggregation.match(Criteria.where("active").is(true)),
        Aggregation.group("category")
            .count().as("productCount")
            .avg("price").as("avgPrice")
            .min("price").as("minPrice")
            .max("price").as("maxPrice")
            .sum("stock").as("totalStock"),
        Aggregation.sort(Sort.Direction.DESC, "productCount"),
        Aggregation.project()
            .and("_id").as("category")
            .andInclude("productCount", "avgPrice", "minPrice", "maxPrice", "totalStock")
    );
    return mongoTemplate.aggregate(aggregation, "products", CategoryStats.class);
}
```

```java
@Data
public class CategoryStats {
    private String category;
    private long productCount;
    private double avgPrice;
    private double minPrice;
    private double maxPrice;
    private long totalStock;
}
```

### 8.3.3 TypedAggregation

작은 팁이지만 실무에서는 꽤 유용하다. `TypedAggregation`을 사용하면 도메인 클래스를 첫 번째 인자로 전달해서 컬렉션 이름을 자동으로 추론할 수 있다. `Aggregation.newAggregation(Product.class, ...)`처럼 쓰면 되고, `aggregate()` 호출할 때 컬렉션 이름을 명시하지 않아도 된다는 뜻이다. 코드가 조금 더 깔끔해진다.

### 8.3.4 Unwind와 Lookup

두 가지 고급 스테이지가 있다. **Unwind**는 배열 필드를 개별 도큐먼트로 분해해서, 배열의 각 요소에 대해 별도의 행이 생기도록 한다. **Lookup**은 SQL의 JOIN처럼 다른 컬렉션과 조인하는 역할을 한다.

```java
// 태그별 상품 수 집계 (Unwind)
public Flux<TagStats> getTagStats() {
    Aggregation aggregation = Aggregation.newAggregation(
        Aggregation.unwind("tags"),
        Aggregation.group("tags").count().as("count").avg("price").as("avgPrice"),
        Aggregation.sort(Sort.Direction.DESC, "count"),
        Aggregation.limit(10)
    );
    return mongoTemplate.aggregate(aggregation, "products", TagStats.class);
}

// 주문 + 사용자 조인 (Lookup)
public Flux<OrderWithUser> getOrdersWithUserInfo() {
    Aggregation aggregation = Aggregation.newAggregation(
        Aggregation.lookup("users", "userId", "_id", "userInfo"),
        Aggregation.unwind("userInfo"),
        Aggregation.project()
            .andInclude("orderDate", "totalAmount", "status")
            .and("userInfo.name").as("userName")
            .and("userInfo.email").as("userEmail")
    );
    return mongoTemplate.aggregate(aggregation, "orders", OrderWithUser.class);
}
```

### 8.3.5 실전 통계 API: 일별 매출 집계

이제 실제로 대시보드에 쓸 수 있는 통계를 만들어보자. 일정 기간 동안 완료된 주문들의 일별 매출, 주문 건수, 평균 주문액을 조회한다.

```java
@Service
@RequiredArgsConstructor
public class SalesStatisticsService {

    private final ReactiveMongoTemplate mongoTemplate;

    public Flux<DailySales> getDailySales(LocalDateTime from, LocalDateTime to) {
        Aggregation aggregation = Aggregation.newAggregation(
            Aggregation.match(
                Criteria.where("orderDate").gte(from).lte(to)
                    .and("status").is("COMPLETED")),
            Aggregation.project()
                .andExpression("dateToString('%Y-%m-%d', orderDate)").as("date")
                .andInclude("totalAmount"),
            Aggregation.group("date")
                .sum("totalAmount").as("totalSales")
                .count().as("orderCount")
                .avg("totalAmount").as("avgOrderAmount"),
            Aggregation.sort(Sort.Direction.ASC, "_id"),
            Aggregation.project()
                .and("_id").as("date")
                .andInclude("totalSales", "orderCount", "avgOrderAmount")
        );
        return mongoTemplate.aggregate(aggregation, "orders", DailySales.class);
    }
}
```

```java
@RestController
@RequestMapping("/api/statistics")
@RequiredArgsConstructor
public class StatisticsController {

    private final SalesStatisticsService salesStatisticsService;

    @GetMapping("/daily-sales")
    public Flux<DailySales> getDailySales(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime from,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime to) {
        return salesStatisticsService.getDailySales(from, to);
    }
}
```

---

## 8.4 변경 스트림(Change Streams) 활용

### 8.4.1 Change Streams 개념

MongoDB의 Change Streams라는 기능이 있는데, 이걸 쓰면 컬렉션의 모든 데이터 변경(삽입, 수정, 삭제)을 실시간으로 감시할 수 있다. 내부적으로는 MongoDB의 oplog를 기반으로 동작한다. 주의할 점은 **Replica Set 또는 Sharded Cluster 환경에서만 사용 가능**하다는 것인데, 로컬 개발 환경에서도 Docker로 단일 노드 Replica Set을 구성하면 테스트할 수 있다. 실시간 알림, 이벤트 발행, 데이터 동기화, 캐시 무효화 같은 작업에 유용하다.

### 8.4.2 ReactiveMongoTemplate으로 Change Streams 구독

`ReactiveMongoTemplate`의 `changeStream()` 메서드를 사용하면 특정 컬렉션의 변경을 Flux로 수신할 수 있다. 여러 필터를 조합해서 원하는 이벤트만 감시할 수 있다.

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderChangeStreamService {

    private final ReactiveMongoTemplate mongoTemplate;

    // INSERT 이벤트 실시간 감시
    public Flux<ChangeStreamEvent<Order>> watchNewOrders() {
        return mongoTemplate.changeStream("orders",
                ChangeStreamOptions.builder()
                    .filter(Aggregation.newAggregation(
                        Aggregation.match(
                            Criteria.where("operationType").is("insert"))))
                    .build(),
                Order.class)
            .doOnNext(event -> log.info("새 주문 감지: orderId={}",
                event.getBody().getId()));
    }

    // UPDATE 이벤트 감시 (전체 도큐먼트 수신)
    public Flux<ChangeStreamEvent<Order>> watchOrderStatusChanges() {
        return mongoTemplate.changeStream("orders",
                ChangeStreamOptions.builder()
                    .filter(Aggregation.newAggregation(
                        Aggregation.match(
                            Criteria.where("operationType").is("update")
                                .and("updateDescription.updatedFields.status").exists(true))))
                    .returnFullDocumentOnUpdate()
                    .build(),
                Order.class);
    }
}
```

한 가지 중요한 옵션이 `returnFullDocumentOnUpdate()`인데, 이걸 호출하면 UPDATE 이벤트가 발생했을 때 변경된 필드만 받는 대신 전체 도큐먼트를 받을 수 있다. 상황에 따라 필요한 쪽을 선택해서 사용하면 된다.

### 8.4.3 Change Streams + SSE 연동

Change Streams로 감시한 이벤트를 Server-Sent Events(SSE)로 클라이언트에게 실시간으로 푸시할 수 있다. 이렇게 하면 웹 클라이언트가 새로운 주문, 상태 변경 같은 이벤트를 즉시 받을 수 있다.

```java
@RestController
@RequestMapping("/api/notifications")
@RequiredArgsConstructor
public class NotificationController {

    private final OrderChangeStreamService changeStreamService;

    @GetMapping(value = "/orders", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<Order>> streamNewOrders() {
        return changeStreamService.watchNewOrders()
            .map(event -> ServerSentEvent.<Order>builder()
                .id(event.getResumeToken().toJson())
                .event("new-order")
                .data(event.getBody())
                .build());
    }
}
```

### 8.4.4 Resume Token을 이용한 재연결

실시간 시스템의 가장 까다로운 부분은 네트워크가 끊어졌을 때 처리다. Change Streams는 이런 상황에 대비해 `resume token`이라는 것을 제공한다. 이 토큰을 저장해두면 연결이 끊어진 후에도 마지막 이벤트부터 이어서 수신할 수 있다. 아주 유용한 기능이다.

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class ResilientChangeStreamService {

    private final ReactiveMongoTemplate mongoTemplate;
    private final ResumeTokenStore tokenStore;

    public Flux<ChangeStreamEvent<Order>> watchWithResume(String streamId) {
        return tokenStore.getLastToken(streamId)
            .flatMapMany(lastToken -> {
                ChangeStreamOptions.ChangeStreamOptionsBuilder builder =
                    ChangeStreamOptions.builder();
                if (lastToken != null) {
                    builder.resumeAfter(lastToken);
                }
                return mongoTemplate.changeStream("orders", builder.build(), Order.class);
            })
            .doOnNext(event ->
                tokenStore.saveToken(streamId, event.getResumeToken()).subscribe())
            .retryWhen(Retry.backoff(Long.MAX_VALUE, Duration.ofSeconds(1))
                .maxBackoff(Duration.ofMinutes(1))
                .doBeforeRetry(signal ->
                    log.warn("Change Stream 재연결 시도: attempt={}",
                        signal.totalRetries())));
    }
}
```

`ResumeTokenStore` 컴포넌트는 resume token을 MongoDB에 저장하고 조회하는 역할을 한다. 보통 `upsert`를 활용해서 구현한다. 이벤트를 처리할 때마다 토큰을 저장해두면 애플리케이션이 재시작되더라도 유실 없이 그 다음부터의 이벤트를 이어서 수신할 수 있다. 필자의 경험상 이런 안정성 기능은 프로덕션 환경에서 정말 중요하다.

---

## 8.5 트랜잭션 처리 (ReactiveMongoTransactionManager)

### 8.5.1 MongoDB 트랜잭션의 전제 조건

MongoDB의 트랜잭션은 꽤 최근에 지원되기 시작했고, 중요한 제약이 하나 있다. **Replica Set 환경에서만 사용할 수 있다**는 것이다. 다행히 Docker Compose로 단일 노드 Replica Set을 구성할 수 있어서 로컬 개발 환경에서도 충분히 테스트할 수 있다.

```yaml
# docker-compose.yml
services:
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    command: ["--replSet", "rs0", "--bind_ip_all"]
    healthcheck:
      test: echo "try { rs.status() } catch (err) { rs.initiate() }" | mongosh
      interval: 5s
      timeout: 30s
      retries: 5
```

### 8.5.2 ReactiveMongoTransactionManager 설정

```java
@Configuration
public class MongoTransactionConfig {

    @Bean
    public ReactiveMongoTransactionManager transactionManager(
            ReactiveMongoDatabaseFactory dbFactory) {
        return new ReactiveMongoTransactionManager(dbFactory);
    }
}
```

### 8.5.3 @Transactional 어노테이션 사용

가장 간단한 방법은 서비스 메서드에 `@Transactional`을 붙이는 것이다. Spring이 자동으로 트랜잭션 경계를 관리해주고, 예외가 발생하면 모든 변경사항을 자동으로 롤백한다.

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final ReactiveMongoTemplate mongoTemplate;
    private final ProductService productService;

    @Transactional
    public Mono<Order> createOrder(OrderRequest request) {
        return Flux.fromIterable(request.getItems())
            .flatMap(item ->
                productService.decrementStock(item.getProductId(), item.getQuantity())
                    .switchIfEmpty(Mono.error(new InsufficientStockException(
                        "재고 부족: productId=" + item.getProductId()))))
            .collectList()
            .flatMap(products -> {
                Order order = Order.builder()
                    .userId(request.getUserId())
                    .items(request.getItems())
                    .totalAmount(calculateTotal(request.getItems(), products))
                    .status("CREATED")
                    .orderDate(LocalDateTime.now())
                    .build();
                return mongoTemplate.insert(order);
            });
    }
}
```

### 8.5.4 TransactionalOperator 프로그래밍 방식

선언적 방식 외에도 프로그래밍 방식으로 트랜잭션 경계를 세밀하게 제어할 수 있다. `TransactionalOperator`를 사용하면 더 유연해진다. 예를 들어 특정 조건에서만 트랜잭션을 적용하거나, 여러 개의 독립적인 트랜잭션을 순서대로 실행할 때 유용하다.

```java
@Service
@RequiredArgsConstructor
public class TransferService {

    private final ReactiveMongoTemplate mongoTemplate;
    private final TransactionalOperator transactionalOperator;

    public Mono<TransferResult> transferPoints(
            String fromUserId, String toUserId, int amount) {

        Mono<TransferResult> transferMono = deductPoints(fromUserId, amount)
            .then(addPoints(toUserId, amount))
            .then(createTransferLog(fromUserId, toUserId, amount))
            .map(log -> new TransferResult("SUCCESS", log.getId()));

        return transactionalOperator.transactional(transferMono);
    }

    private Mono<UpdateResult> deductPoints(String userId, int amount) {
        Query query = Query.query(
            Criteria.where("id").is(userId).and("points").gte(amount));
        Update update = new Update().inc("points", -amount);
        return mongoTemplate.updateFirst(query, update, User.class)
            .flatMap(result -> result.getModifiedCount() == 0
                ? Mono.error(new InsufficientPointsException("포인트 부족"))
                : Mono.just(result));
    }

    private Mono<UpdateResult> addPoints(String userId, int amount) {
        Query query = Query.query(Criteria.where("id").is(userId));
        return mongoTemplate.updateFirst(query, new Update().inc("points", amount), User.class);
    }

    private Mono<TransferLog> createTransferLog(
            String fromUserId, String toUserId, int amount) {
        return mongoTemplate.insert(TransferLog.builder()
            .fromUserId(fromUserId).toUserId(toUserId)
            .amount(amount).transferredAt(LocalDateTime.now()).build());
    }
}
```

### 8.5.5 @Transactional vs TransactionalOperator 선택 기준

| 비교 항목 | @Transactional | TransactionalOperator |
|-----------|---------------|----------------------|
| **사용 방식** | 선언적 (어노테이션) | 프로그래밍 방식 |
| **적합한 곳** | 서비스 계층 메서드 단위 | 함수형 엔드포인트, 세밀한 제어 |
| **트랜잭션 범위** | 메서드 전체 | `transactional()` 호출 범위 |
| **유연성** | 제한적 | 높음 (조건부 트랜잭션 등) |

---

## 8.6 인덱스 관리와 쿼리 성능 최적화

### 8.6.1 @Indexed 어노테이션

이제 성능 최적화 부분으로 넘어가자. 인덱스 없이 운영하는 MongoDB 시스템은 결국 느려진다. Spring Data MongoDB는 `@Indexed` 어노테이션으로 단순하게 인덱스를 선언할 수 있게 해준다.

```java
@Document(collection = "products")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class Product {

    @Id
    private String id;
    private String name;

    @Indexed
    private String category;

    private BigDecimal price;

    @Indexed(unique = true)
    private String sku;

    @Indexed(direction = IndexDirection.DESCENDING)
    private LocalDateTime createdAt;

    private int stock;
    private boolean active;
    private List<String> tags;
}
```

> **주의**: Spring Boot 3.x부터 `auto-index-creation`이 기본값 `false`다. `@Indexed`가 동작하려면 명시적으로 활성화해야 한다.

```yaml
spring:
  data:
    mongodb:
      auto-index-creation: true
```

### 8.6.2 @CompoundIndex 복합 인덱스

실무에서는 단일 필드 인덱스만으로는 부족하다. 여러 필드를 조합해서 인덱스를 만들어야 하는 경우가 많은데, 이때는 `@CompoundIndex`를 사용한다.

```java
@Document(collection = "products")
@CompoundIndex(name = "category_price_idx", def = "{'category': 1, 'price': -1}")
@CompoundIndex(name = "category_active_created_idx",
               def = "{'category': 1, 'active': 1, 'createdAt': -1}")
public class Product { /* ... */ }
```

복합 인덱스의 필드 순서는 정말 중요한데, **ESR (Equality, Sort, Range) 규칙**을 따르면 최적화된다.

1. **Equality**: 등호(`=`) 조건 필드를 먼저 배치
2. **Sort**: 정렬 필드를 다음에 배치
3. **Range**: 범위 조건(`>=`, `<=`) 필드를 마지막에 배치

```java
// 쿼리: category = ? AND active = ?, 정렬: createdAt DESC, 조건: price >= ?
// 최적 인덱스: { category: 1, active: 1, createdAt: -1, price: 1 }
@CompoundIndex(name = "optimized_search_idx",
               def = "{'category': 1, 'active': 1, 'createdAt': -1, 'price': 1}")
```

### 8.6.3 TTL 인덱스

TTL 인덱스는 흥미로운 기능이다. 지정된 시간이 지나면 도큐먼트를 자동으로 삭제해주는데, 세션 데이터, 임시 토큰, 로그 같은 일시적 데이터를 관리할 때 정말 유용하다. 수동으로 정리 작업을 구현할 필요가 없어진다.

```java
@Document(collection = "sessions")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class Session {

    @Id
    private String id;
    private String userId;
    private String token;

    @Indexed(expireAfterSeconds = 3600)  // 1시간 후 자동 삭제
    private LocalDateTime createdAt;
}
```

대상 필드는 반드시 `Date` 또는 `LocalDateTime` 타입이어야 한다. MongoDB 백그라운드 태스크가 60초 간격으로 만료 도큐먼트를 삭제하므로, 실제 삭제 시점은 약간의 지연이 있을 수 있다.

### 8.6.4 프로그래밍 방식 인덱스 생성과 Partial Index

어노테이션으로 인덱스를 선언하는 것도 좋지만, 때론 애플리케이션 시작 시에 동적으로 인덱스를 생성해야 할 수도 있다. `ReactiveMongoTemplate`의 `indexOps()`를 사용하면 이게 가능하다. 또한 **Partial Index**라는 개념도 있는데, 특정 조건을 만족하는 도큐먼트에만 인덱스를 적용하는 기법이다. 이렇게 하면 저장 공간도 절약하고 쓰기 성능도 개선된다.

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class IndexInitializer implements ApplicationRunner {

    private final ReactiveMongoTemplate mongoTemplate;

    @Override
    public void run(ApplicationArguments args) {
        ReactiveIndexOperations indexOps = mongoTemplate.indexOps(Product.class);
        Index partialIndex = new Index()
            .on("price", IndexDirection.ASCENDING)
            .named("active_products_price_idx")
            .partial(PartialIndexFilter.of(Criteria.where("active").is(true)));
        indexOps.ensureIndex(partialIndex)
            .doOnSuccess(name -> log.info("인덱스 생성 완료: {}", name))
            .subscribe();
    }
}
```

### 8.6.5 explain()으로 쿼리 실행 계획 분석

인덱스를 만들었다고 해서 항상 인덱스가 사용되는 건 아니다. 쿼리가 정말로 인덱스를 활용하고 있는지 확인하려면 `explain()`으로 실행 계획을 분석해야 한다. `ReactiveMongoTemplate`에서 네이티브 컬렉션을 가져와 `explain()`을 호출하면 실행 계획을 얻을 수 있다. 결과에서 `queryPlanner.winningPlan.stage`가 `IXSCAN`(인덱스 스캔)이면 좋은 것이고, `COLLSCAN`(컬렉션 풀 스캔)이라면 인덱스를 다시 설계해야 한다는 뜻이다. 또한 `totalDocsExamined`와 `nReturned`가 비슷할수록 인덱스가 잘 설계된 것이다.

### 8.6.6 인덱스 설계 실무 가이드라인

마지막으로 실제 프로덕션에서 적용할 수 있는 가이드라인을 정리하면:

1. **가장 자주 실행되는 쿼리부터 우선으로 인덱스를 설계한다.** 모든 필드에 인덱스를 걸 필요는 없다.
2. **복합 인덱스는 ESR 규칙을 따른다.** Equality, Sort, Range 순서로 필드를 배치해야 효율적이다.
3. **인덱스는 쓰기 성능에 영향을 미친다.** 매번 INSERT/UPDATE할 때마다 인덱스도 갱신해야 하므로 불필요한 인덱스는 제거하자.
4. **Covered Query를 활용한다.** 필요한 모든 필드가 인덱스에 포함되면 실제 도큐먼트를 읽지 않고 결과를 반환할 수 있다.
5. **Partial Index로 인덱스 크기를 줄인다.** 활성 데이터만 인덱싱하면 저장 공간과 성능을 모두 개선할 수 있다.

---

## 요약

| 주제 | 핵심 내용 |
|------|----------|
| **ReactiveMongoTemplate** | `Query`/`Update` 객체로 세밀한 CRUD, 부분 업데이트, Upsert 수행 |
| **Criteria API** | 동적 쿼리 조합, and/or/in/regex 조건, 정렬/페이징/Projection |
| **Aggregation Pipeline** | match/group/sort/project/unwind/lookup으로 복잡한 집계와 통계 API 구현 |
| **Change Streams** | 컬렉션 변경을 실시간 감시, resume token으로 재연결 시 이벤트 유실 방지 |
| **트랜잭션** | Replica Set 필수, `@Transactional` 또는 `TransactionalOperator`로 원자적 연산 보장 |
| **인덱스 최적화** | `@Indexed`, `@CompoundIndex`, TTL 인덱스, ESR 규칙, explain 분석으로 쿼리 성능 개선 |

다음 장에서는 데이터 검증과 예외 처리로 넘어간다. Bean Validation을 활용한 입력값 검증, 커스텀 Validator 작성, 글로벌 예외 처리 구조, 클라이언트 친화적인 에러 응답 표준화 등을 살펴볼 예정이다.
# Chapter 9. 데이터 검증과 예외 처리

MongoDB 데이터 접근을 심화한 Chapter 8을 마쳤다면, 이제 실무에서 가장 중요한 부분을 다룬다: 클라이언트로부터 들어오는 데이터가 제대로 된 형식인지 검증하고, 문제가 발생했을 때 일관성 있게 처리하는 방법이다.

실제 프로젝트에서는 "쓰레기 데이터는 빨리 걸러낼수록 좋다"가 기본 원칙이다. 부정확한 입력을 초반에 차단하면 나중에 뒤에서 처리하는 복잡한 로직을 피할 수 있고, 예외가 발생했을 때는 클라이언트가 이해하기 쉬운 일관된 형식으로 알려줘야 한다. 필자의 경험상, 이 부분을 제대로 구성하면 버그 신고와 지원 비용이 크게 줄어든다.

이 장에서는 Bean Validation으로 입력을 선언적으로 검증하는 방법부터 시작해서, 복잡한 비즈니스 규칙을 처리하는 커스텀 Validator, 그리고 `@ControllerAdvice`, `ErrorWebExceptionHandler` 같은 글로벌 예외 처리기까지 실용적인 패턴을 차례로 살펴본다. 마지막으로 RFC 7807 Problem Details 표준도 알아본다.

---

## 9.1 Bean Validation을 활용한 입력 검증

### 9.1.1 의존성 추가

Spring Boot에서 Bean Validation을 쓰려면 먼저 의존성을 선언해야 한다. 다행히 `spring-boot-starter-validation`이 모든 것을 담고 있어서 추가만 하면 바로 사용할 수 있다.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

이 스타터 안에는 Hibernate Validator가 포함되어 있고, Jakarta Bean Validation 3.0 API(`jakarta.validation` 패키지)도 함께 제공된다.

### 9.1.2 주요 검증 어노테이션

실무에서 가장 자주 쓰이는 검증 어노테이션들을 정리해봤다.

| 어노테이션 | 설명 | 적용 대상 |
|-----------|------|----------|
| `@NotNull` | null이 아니어야 한다 | 모든 타입 |
| `@NotBlank` | null이 아니고, 공백을 제외한 길이가 1 이상 | `String` |
| `@NotEmpty` | null이 아니고, 비어 있지 않아야 한다 | `String`, `Collection`, `Map`, 배열 |
| `@Size(min, max)` | 길이 또는 크기가 범위 내 | `String`, `Collection`, `Map`, 배열 |
| `@Email` | 이메일 형식이어야 한다 | `String` |
| `@Pattern(regexp)` | 정규표현식에 매칭되어야 한다 | `String` |
| `@Min` / `@Max` | 지정 값 이상 / 이하 | 숫자 타입 |
| `@Positive` | 양수여야 한다 | 숫자 타입 |
| `@Past` / `@Future` | 과거 / 미래 날짜여야 한다 | 날짜, 시간 타입 |

### 9.1.3 DTO에 검증 어노테이션 적용

이제 Chapter 6에서 만들었던 사용자 등록 DTO에 검증 규칙을 붙여보자. 이렇게 하면 클라이언트의 요청이 들어올 때 자동으로 검증된다.

```java
package com.example.webfluxdemo.dto;

import jakarta.validation.constraints.*;
import lombok.*;

@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserCreateRequest {

    @NotBlank(message = "이름은 필수 입력 항목입니다")
    @Size(min = 2, max = 50, message = "이름은 2~50자 사이여야 합니다")
    private String name;

    @NotBlank(message = "이메일은 필수 입력 항목입니다")
    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String email;

    @NotBlank(message = "비밀번호는 필수 입력 항목입니다")
    @Pattern(
        regexp = "^(?=.*[A-Za-z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!%*#?&]{8,20}$",
        message = "비밀번호는 8~20자이며, 영문, 숫자, 특수문자를 포함해야 합니다"
    )
    private String password;
}
```

상품 생성 DTO에도 비슷한 방식으로 검증을 추가할 수 있다.

```java
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProductCreateRequest {

    @NotBlank(message = "상품명은 필수 입력 항목입니다")
    @Size(max = 200, message = "상품명은 200자를 초과할 수 없습니다")
    private String name;

    @NotNull(message = "가격은 필수 입력 항목입니다")
    @Positive(message = "가격은 양수여야 합니다")
    private Integer price;

    @Size(max = 1000, message = "설명은 1000자를 초과할 수 없습니다")
    private String description;

    @NotBlank(message = "카테고리는 필수 입력 항목입니다")
    private String category;
}
```

### 9.1.4 컨트롤러에서 @Valid 적용

WebFlux를 쓸 때 어노테이션 기반 컨트롤러라면, `@Valid`를 `@RequestBody`와 함께 붙이기만 하면 자동으로 검증이 시작된다.

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<UserResponse> createUser(
            @Valid @RequestBody UserCreateRequest request) {
        return userService.createUser(request);
    }

    @PutMapping("/{id}")
    public Mono<UserResponse> updateUser(
            @PathVariable String id,
            @Valid @RequestBody UserUpdateRequest request) {
        return userService.updateUser(id, request);
    }
}
```

만약 `@Valid`가 붙은 파라미터의 검증이 실패하면 어떻게 될까? Spring WebFlux가 `WebExchangeBindException`을 던지는데, 이건 9.3절에서 만들 글로벌 예외 처리기가 받아서 깔끔한 형식으로 클라이언트에 전달해준다.

### 9.1.5 함수형 엔드포인트에서의 검증

함수형 엔드포인트는 어노테이션 없이 라우팅을 정의하는 방식이라, 검증도 직접 손으로 해줘야 한다. `Validator`를 주입받아서 명시적으로 검증하는 방식이다.

```java
@Component
@RequiredArgsConstructor
public class ProductHandler {

    private final ProductService productService;
    private final Validator validator;

    public Mono<ServerResponse> createProduct(ServerRequest request) {
        return request.bodyToMono(ProductCreateRequest.class)
            .doOnNext(this::validate)
            .flatMap(productService::createProduct)
            .flatMap(product -> ServerResponse
                .created(URI.create("/api/products/" + product.getId()))
                .bodyValue(product));
    }

    private <T> void validate(T body) {
        Set<ConstraintViolation<T>> violations = validator.validate(body);
        if (!violations.isEmpty()) {
            throw new ConstraintViolationException(violations);
        }
    }
}
```

검증에서 문제가 발견되면 `ConstraintViolationException`을 던져버리면 되는데, 이것도 나중에 만들 글로벌 예외 처리기가 받아서 깔끔하게 정리해준다.

---

## 9.2 커스텀 Validator 구현

### 9.2.1 커스텀 어노테이션 정의

Bean Validation의 표준 어노테이션만으로는 표현하기 어려운 비즈니스 규칙들이 있다. 예를 들어, 특정한 카테고리 값들만 허용하는 경우 같은 경우 말이다. 이럴 때는 자신만의 검증 어노테이션을 만드는 게 깔끔하다.

```java
@Documented
@Constraint(validatedBy = AllowedCategoryValidator.class)
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
public @interface AllowedCategory {
    String message() default "허용되지 않은 카테고리입니다";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
    String[] values() default {};
}
```

### 9.2.2 ConstraintValidator 구현

이제 실제로 검증 로직을 구현할 차례다. `ConstraintValidator<A, T>` 인터페이스를 구현하면 되는데, `A`는 어노테이션 타입이고 `T`는 검증할 필드의 타입이다.

```java
public class AllowedCategoryValidator
        implements ConstraintValidator<AllowedCategory, String> {

    private Set<String> allowedValues;

    @Override
    public void initialize(AllowedCategory annotation) {
        this.allowedValues = Set.of(annotation.values());
    }

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null) {
            return true; // null 검사는 @NotBlank에 위임
        }
        return allowedValues.contains(value);
    }
}
```

이제 DTO의 필드에 이 커스텀 어노테이션을 붙이면 된다.

```java
@AllowedCategory(
    values = {"ELECTRONICS", "BOOKS", "CLOTHING", "FOOD"},
    message = "카테고리는 ELECTRONICS, BOOKS, CLOTHING, FOOD 중 하나여야 합니다"
)
@NotBlank(message = "카테고리는 필수 입력 항목입니다")
private String category;
```

### 9.2.3 크로스 필드 검증 (클래스 레벨 Validator)

이번엔 좀 더 복잡한 경우를 생각해보자. 비밀번호와 비밀번호 확인 필드가 일치해야 한다거나, 여러 필드를 함께 검증해야 하는 상황 말이다. 이럴 때는 **클래스 레벨 어노테이션**으로 처리한다.

```java
@Documented
@Constraint(validatedBy = PasswordMatchValidator.class)
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface PasswordMatch {
    String message() default "비밀번호와 비밀번호 확인이 일치하지 않습니다";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

그 다음 검증 대상이 될 DTO가 따를 인터페이스를 정의한다.

```java
public interface PasswordConfirmable {
    String getPassword();
    String getPasswordConfirm();
}
```

```java
public class PasswordMatchValidator
        implements ConstraintValidator<PasswordMatch, PasswordConfirmable> {

    @Override
    public boolean isValid(PasswordConfirmable dto,
                           ConstraintValidatorContext context) {
        if (dto.getPassword() == null || dto.getPasswordConfirm() == null) {
            return true;
        }
        boolean matches = dto.getPassword().equals(dto.getPasswordConfirm());
        if (!matches) {
            context.disableDefaultConstraintViolation();
            context.buildConstraintViolationWithTemplate(
                    "비밀번호와 비밀번호 확인이 일치하지 않습니다")
                .addPropertyNode("passwordConfirm")
                .addConstraintViolation();
        }
        return matches;
    }
}
```

필자의 경험상, 이런 식으로 `@PasswordMatch`를 DTO 클래스에 붙이면 필드별 검증과 크로스 필드 검증이 깔끔하게 함께 실행된다.

```java
@PasswordMatch
@Getter @NoArgsConstructor @AllArgsConstructor @Builder
public class SignUpRequest implements PasswordConfirmable {

    @NotBlank(message = "이름은 필수 입력 항목입니다")
    private String name;

    @NotBlank @Email
    private String email;

    @NotBlank
    private String password;

    @NotBlank
    private String passwordConfirm;
}
```

---

## 9.3 글로벌 예외 처리 (@ControllerAdvice)

### 9.3.1 커스텀 예외 클래스 정의

지금부터 예외 처리 전략을 짠다. 비즈니스 로직에서 터지는 예외들을 타입별로 구분해서 관리하면, 나중에 처리하기도 편하고 에러 메시지도 일관되게 만들 수 있다.

```java
package com.example.webfluxdemo.exception;

import lombok.Getter;

@Getter
public class BusinessException extends RuntimeException {

    private final ErrorCode errorCode;

    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }

    public BusinessException(ErrorCode errorCode, String detail) {
        super(detail);
        this.errorCode = errorCode;
    }
}
```

```java
public class ResourceNotFoundException extends BusinessException {
    public ResourceNotFoundException(String resourceName, String id) {
        super(ErrorCode.RESOURCE_NOT_FOUND,
              resourceName + "을(를) 찾을 수 없습니다. ID: " + id);
    }
}

public class DuplicateResourceException extends BusinessException {
    public DuplicateResourceException(String resourceName, String field) {
        super(ErrorCode.DUPLICATE_RESOURCE,
              resourceName + "이(가) 이미 존재합니다. 필드: " + field);
    }
}
```

### 9.3.2 ErrorCode 열거형

에러 코드를 열거형으로 관리하는 건 간단하면서도 강력한 패턴이다. 에러의 종류를 한곳에서 정의해두면 코드 전체에서 일관성을 유지할 수 있다.

```java
package com.example.webfluxdemo.exception;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

@Getter
@RequiredArgsConstructor
public enum ErrorCode {

    // 공통
    INVALID_INPUT(HttpStatus.BAD_REQUEST, "C001", "잘못된 입력값입니다"),
    RESOURCE_NOT_FOUND(HttpStatus.NOT_FOUND, "C002", "리소스를 찾을 수 없습니다"),
    INTERNAL_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "C003", "서버 내부 오류"),
    DUPLICATE_RESOURCE(HttpStatus.CONFLICT, "C004", "중복된 리소스입니다"),

    // 사용자
    USER_NOT_FOUND(HttpStatus.NOT_FOUND, "U001", "사용자를 찾을 수 없습니다"),
    EMAIL_ALREADY_EXISTS(HttpStatus.CONFLICT, "U002", "이미 등록된 이메일입니다"),

    // 상품
    PRODUCT_NOT_FOUND(HttpStatus.NOT_FOUND, "P001", "상품을 찾을 수 없습니다"),
    INSUFFICIENT_STOCK(HttpStatus.BAD_REQUEST, "P002", "재고가 부족합니다");

    private final HttpStatus status;
    private final String code;
    private final String message;
}
```

### 9.3.3 ErrorResponse DTO

이제 클라이언트에 어떤 형식으로 에러를 알려줄지 정의해보자.

```java
package com.example.webfluxdemo.exception;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;
import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {

    private final String code;
    private final String message;
    private final int status;
    private final LocalDateTime timestamp;
    private final List<FieldError> errors;

    @Getter @Builder
    public static class FieldError {
        private final String field;
        private final String value;
        private final String reason;
    }

    public static ErrorResponse of(ErrorCode ec) {
        return of(ec, ec.getMessage(), null);
    }

    public static ErrorResponse of(ErrorCode ec, String message) {
        return of(ec, message, null);
    }

    public static ErrorResponse of(ErrorCode ec, List<FieldError> errors) {
        return of(ec, ec.getMessage(), errors);
    }

    private static ErrorResponse of(ErrorCode ec, String msg,
                                    List<FieldError> errors) {
        return ErrorResponse.builder()
            .code(ec.getCode()).message(msg)
            .status(ec.getStatus().value())
            .timestamp(LocalDateTime.now()).errors(errors)
            .build();
    }
}
```

### 9.3.4 @RestControllerAdvice 구현

드디어 예외를 처리하는 핵심 부분이다. `@RestControllerAdvice`는 `@ControllerAdvice`와 `@ResponseBody`를 합친 거고, 모든 컨트롤러에서 터지는 예외를 한곳에서 받아서 처리하는 역할을 한다.

```java
package com.example.webfluxdemo.exception;

import jakarta.validation.ConstraintViolationException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.support.WebExchangeBindException;
import java.util.List;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(WebExchangeBindException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
            WebExchangeBindException ex) {

        List<ErrorResponse.FieldError> fieldErrors = ex.getFieldErrors()
            .stream()
            .map(e -> ErrorResponse.FieldError.builder()
                .field(e.getField())
                .value(e.getRejectedValue() != null
                    ? e.getRejectedValue().toString() : "")
                .reason(e.getDefaultMessage())
                .build())
            .toList();

        log.warn("Validation failed: {}", fieldErrors);
        return ResponseEntity.badRequest()
            .body(ErrorResponse.of(ErrorCode.INVALID_INPUT, fieldErrors));
    }

    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleConstraintViolation(
            ConstraintViolationException ex) {
        List<ErrorResponse.FieldError> fieldErrors = ex.getConstraintViolations()
            .stream()
            .map(v -> ErrorResponse.FieldError.builder()
                .field(v.getPropertyPath().toString())
                .reason(v.getMessage()).build())
            .toList();
        return ResponseEntity.badRequest()
            .body(ErrorResponse.of(ErrorCode.INVALID_INPUT, fieldErrors));
    }

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusiness(
            BusinessException ex) {

        ErrorCode ec = ex.getErrorCode();
        log.warn("Business exception: [{}] {}", ec.getCode(), ex.getMessage());
        return ResponseEntity.status(ec.getStatus())
            .body(ErrorResponse.of(ec, ex.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception ex) {

        log.error("Unhandled exception", ex);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(ErrorResponse.of(ErrorCode.INTERNAL_ERROR));
    }
}
```

### 9.3.5 서비스 계층에서 예외 발생

이제 서비스 계층에서는 어떻게 예외를 던질까? 리액티브 파이프라인 안에서는 `switchIfEmpty`와 `Mono.error`를 조합해서 처리한다.

```java
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public Mono<UserResponse> findById(String id) {
        return userRepository.findById(id)
            .map(UserResponse::from)
            .switchIfEmpty(Mono.error(
                new ResourceNotFoundException("사용자", id)));
    }

    public Mono<UserResponse> createUser(UserCreateRequest request) {
        return userRepository.findByEmail(request.getEmail())
            .flatMap(existing -> Mono.<User>error(
                new DuplicateResourceException("이메일", request.getEmail())))
            .switchIfEmpty(Mono.defer(() -> {
                User user = User.builder()
                    .name(request.getName())
                    .email(request.getEmail())
                    .password(request.getPassword())
                    .build();
                return userRepository.save(user);
            }))
            .map(UserResponse::from);
    }
}
```

서비스에서 던진 예외는 `GlobalExceptionHandler`가 받아서 깔끔한 HTTP 응답으로 변환해준다.

### 9.3.6 에러 응답 예시

실제로 클라이언트가 받는 응답이 어떻게 생겼는지 몇 가지 예를 보자.

```json
{
  "code": "C001",
  "message": "잘못된 입력값입니다",
  "status": 400,
  "timestamp": "2026-02-14T10:30:00",
  "errors": [
    { "field": "name", "value": "", "reason": "이름은 필수 입력 항목입니다" },
    { "field": "email", "value": "invalid", "reason": "올바른 이메일 형식이 아닙니다" }
  ]
}
```

리소스를 찾을 수 없는 경우는 어떨까?

```json
{
  "code": "C002",
  "message": "사용자을(를) 찾을 수 없습니다. ID: 64a1b2c3d4e5f6",
  "status": 404,
  "timestamp": "2026-02-14T10:31:00"
}
```

---

## 9.4 ErrorWebExceptionHandler를 활용한 함수형 예외 처리

### 9.4.1 @ControllerAdvice의 한계

지금까지 `@RestControllerAdvice`를 다뤘는데, 이건 어노테이션 기반 컨트롤러에서만 완벽하게 작동한다는 걸 알아야 한다. 함수형 엔드포인트(`RouterFunction`)에서 발생하는 예외 중에는 `@ExceptionHandler`가 잡지 못하는 게 있다. 특히 라우팅 전이나 필터 단계에서 터지는 예외 말이다. 이런 경우를 대비하려면 `ErrorWebExceptionHandler`를 사용해야 한다.

### 9.4.2 AbstractErrorWebExceptionHandler 확장

Spring Boot에서 제공하는 `AbstractErrorWebExceptionHandler`를 상속받으면 에러 처리를 맘대로 커스터마이징할 수 있다. 핵심은 `getRoutingFunction()`을 오버라이드해서 모든 에러 요청이 우리가 정의한 렌더 메서드로 가도록 하는 것이다.

```java
@Component
@Order(-2) // 기본 에러 핸들러(-1)보다 높은 우선순위
public class CustomErrorWebExceptionHandler
        extends AbstractErrorWebExceptionHandler {

    public CustomErrorWebExceptionHandler(
            ErrorAttributes errorAttributes, WebProperties webProperties,
            ApplicationContext ctx, ServerCodecConfigurer configurer) {
        super(errorAttributes, webProperties.getResources(), ctx);
        this.setMessageWriters(configurer.getWriters());
    }

    @Override
    protected RouterFunction<ServerResponse> getRoutingFunction(
            ErrorAttributes errorAttributes) {
        return RouterFunctions.route(
            RequestPredicates.all(), this::renderErrorResponse);
    }

    private Mono<ServerResponse> renderErrorResponse(ServerRequest request) {
        Throwable error = getError(request);
        HttpStatus status;
        String code, message;

        if (error instanceof BusinessException bex) {
            status = bex.getErrorCode().getStatus();
            code = bex.getErrorCode().getCode();
            message = bex.getMessage();
        } else if (error instanceof WebExchangeBindException) {
            status = HttpStatus.BAD_REQUEST;
            code = "C001"; message = "잘못된 입력값입니다";
        } else {
            status = HttpStatus.INTERNAL_SERVER_ERROR;
            code = "C003"; message = "서버 내부 오류가 발생했습니다";
        }

        Map<String, Object> body = Map.of(
            "code", code, "message", message,
            "status", status.value(),
            "timestamp", LocalDateTime.now().toString(),
            "path", request.path());

        return ServerResponse.status(status)
            .contentType(MediaType.APPLICATION_JSON)
            .body(BodyInserters.fromValue(body));
    }
}
```

### 9.4.3 @ControllerAdvice와의 공존

`@Order(-2)`를 붙인 이유가 뭘까? Spring이 기본으로 제공하는 `DefaultErrorWebExceptionHandler`가 `-1`의 우선순위를 가지고 있어서, 우리의 커스텀 핸들러가 먼저 실행되도록 한 것이다. 둘을 동시에 사용할 수 있는데, 처리 순서는 이렇다.

| 단계 | 처리 주체 | 대상 |
|------|----------|------|
| 1 | `@ExceptionHandler` | 어노테이션 컨트롤러에서 발생한 예외 |
| 2 | `ErrorWebExceptionHandler` | 1단계에서 처리되지 않은 모든 예외 |

실무에서 권장하는 패턴은 이렇다: 어노테이션 기반 API에서는 `@RestControllerAdvice`가 예외를 받고, 함수형 엔드포인트나 필터에서 발생한 예외는 `ErrorWebExceptionHandler`가 처리하는 구조다. 단, 중요한 건 두 방식이 같은 형식의 에러 응답을 돌려줘야 한다는 점이다.

---

## 9.5 에러 응답 표준화 (Problem Details)

### 9.5.1 RFC 7807이란?

지금까지는 우리만의 에러 응답 형식을 만들었는데, 사실 업계에 표준이 있다. RFC 7807(Problem Details for HTTP APIs)이라고 불리는데, HTTP API에서 에러를 어떻게 표현할지를 정한 규격이다.

| 필드 | 설명 |
|------|------|
| `type` | 에러 유형을 식별하는 URI |
| `title` | 에러의 짧은 요약 |
| `status` | HTTP 상태 코드 |
| `detail` | 에러의 상세 설명 |
| `instance` | 에러가 발생한 구체적 URI |

Content-Type은 `application/problem+json`을 사용한다.

### 9.5.2 Spring Framework 6의 ProblemDetail

좋은 소식은 Spring Framework 6부터는 이 표준을 구현한 `ProblemDetail` 클래스를 기본으로 제공한다는 거다. `setProperty()`로 맞춤 필드도 추가할 수 있다.

```java
// ProblemDetail의 주요 구조
public class ProblemDetail {
    private URI type;
    private String title;
    private int status;
    private String detail;
    private URI instance;
    private Map<String, Object> properties; // 확장 필드
}
```

### 9.5.3 ProblemDetail 기반 글로벌 예외 처리

이제 9.3절의 `GlobalExceptionHandler`를 `ProblemDetail`을 사용하도록 개선해보자. 반환 타입을 `ResponseEntity<ErrorResponse>` 대신 `ProblemDetail`로 바꾸기만 하면 된다.

```java
package com.example.webfluxdemo.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.support.WebExchangeBindException;
import java.net.URI;
import java.time.Instant;
import java.util.*;

@Slf4j
@RestControllerAdvice
public class ProblemDetailExceptionHandler {

    private static final String BASE_TYPE = "https://api.example.com/errors/";

    @ExceptionHandler(WebExchangeBindException.class)
    public ProblemDetail handleValidation(WebExchangeBindException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST, "입력값 검증에 실패했습니다");
        problem.setType(URI.create(BASE_TYPE + "validation-failed"));
        problem.setTitle("Validation Failed");
        problem.setProperty("errors", ex.getFieldErrors().stream()
            .map(fe -> Map.of("field", fe.getField(),
                "message", Objects.toString(fe.getDefaultMessage(), "")))
            .toList());
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }

    @ExceptionHandler(BusinessException.class)
    public ProblemDetail handleBusiness(BusinessException ex) {
        ErrorCode ec = ex.getErrorCode();
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            ec.getStatus(), ex.getMessage());
        problem.setType(URI.create(BASE_TYPE + ec.getCode()));
        problem.setTitle(ec.getMessage());
        problem.setProperty("errorCode", ec.getCode());
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }

    @ExceptionHandler(Exception.class)
    public ProblemDetail handleUnhandled(Exception ex) {
        log.error("Unhandled exception", ex);
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.INTERNAL_SERVER_ERROR, "서버 내부 오류가 발생했습니다");
        problem.setType(URI.create(BASE_TYPE + "internal-error"));
        problem.setTitle("Internal Server Error");
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }
}
```

### 9.5.4 ProblemDetail 응답 예시

이제 실제로 어떻게 응답이 달라지는지 보자. 검증 실패 때는 `application/problem+json` 타입으로 반환된다.

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 400,
  "detail": "입력값 검증에 실패했습니다",
  "errors": [
    { "field": "name", "message": "이름은 필수 입력 항목입니다" },
    { "field": "price", "message": "가격은 양수여야 합니다" }
  ],
  "timestamp": "2026-02-14T01:30:00Z"
}
```

비즈니스 로직에서 터진 예외는 어떨까?

```json
{
  "type": "https://api.example.com/errors/U002",
  "title": "이미 등록된 이메일입니다",
  "status": 409,
  "detail": "이메일이(가) 이미 존재합니다. 필드: user@example.com",
  "errorCode": "U002",
  "timestamp": "2026-02-14T01:31:00Z"
}
```

### 9.5.5 ProblemDetail 활성화 설정

Spring Boot 3에서 이 기능을 전면적으로 활성화하려면 설정 파일에 한두 줄을 추가하면 된다.

```yaml
spring:
  webflux:
    problemdetails:
      enabled: true
```

필자의 경험상, 이 설정을 켜두면 Spring이 자체적으로 처리하는 예외들(404 Not Found, 405 Method Not Allowed 등)도 모두 `ProblemDetail` 형식으로 통일되어서 관리가 훨씬 깔끔해진다.

### 9.5.6 ErrorWebExceptionHandler에서 ProblemDetail 사용

9.4절에서 만들었던 함수형 엔드포인트용 `ErrorWebExceptionHandler`도 당연히 `ProblemDetail` 형식을 써야 한다. `renderErrorResponse` 메서드에서 `Map` 대신 `ProblemDetail`을 만들고, Content-Type을 `MediaType.APPLICATION_PROBLEM_JSON`으로 설정하기만 하면 된다.

```java
private Mono<ServerResponse> renderErrorResponse(ServerRequest request) {
    Throwable error = getError(request);
    HttpStatus status = (error instanceof BusinessException bex)
        ? bex.getErrorCode().getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    ProblemDetail problem = ProblemDetail.forStatusAndDetail(
        status, error.getMessage());
    problem.setInstance(URI.create(request.path()));
    problem.setProperty("timestamp", Instant.now());

    return ServerResponse.status(status)
        .contentType(MediaType.APPLICATION_PROBLEM_JSON)
        .body(BodyInserters.fromValue(problem));
}
```

`APPLICATION_PROBLEM_JSON`을 설정하면 Content-Type이 정확히 `application/problem+json`으로 들어가서 RFC 7807 표준을 완벽히 따르게 된다.

---

## 요약

이 장에서 배운 내용들을 간단히 정리해보자.

| 주제 | 핵심 내용 |
|------|----------|
| **Bean Validation** | `@NotBlank`, `@Email`, `@Pattern` 등으로 DTO 필드를 선언적으로 검증, 컨트롤러에서 `@Valid`로 활성화 |
| **커스텀 Validator** | `ConstraintValidator` 구현으로 비즈니스 규칙 검증, 클래스 레벨 어노테이션으로 크로스 필드 검증 |
| **@RestControllerAdvice** | `@ExceptionHandler`로 예외 유형별 처리, `ErrorResponse` DTO로 일관된 응답 반환 |
| **ErrorWebExceptionHandler** | `AbstractErrorWebExceptionHandler` 확장으로 함수형 엔드포인트 포함 모든 예외 통합 처리 |
| **Problem Details** | RFC 7807 기반 `ProblemDetail` 클래스로 에러 응답 표준화, `application/problem+json` 타입 사용 |

다음 장에서는 WebFlux의 필터와 인터셉터로 넘어간다. `WebFilter`와 `HandlerFilterFunction`을 가지고 요청과 응답을 로깅하고, CORS를 설정하고, API 속도 제한을 구현하는 방법들을 차례로 배워본다.
# Chapter 10. WebFlux 필터와 인터셉터

지난 장에서 데이터 검증과 예외 처리를 다루었으니, 이제 요청과 응답 양쪽에 걸친 **횡단 관심사(cross-cutting concerns)**를 효율적으로 처리할 차례다. Spring MVC 개발자라면 `Filter`와 `HandlerInterceptor`에 익숙할 텐데, WebFlux에서는 `WebFilter`와 `HandlerFilterFunction`이라는 리액티브 방식의 도구를 제공한다. 이 장에서는 이 두 가지를 구현하는 방법부터 시작해서, 로깅, CORS, 속도 제한 같은 실무에서 정말 자주 마주치는 패턴들까지 차근차근 살펴보겠다.

---

## 10.1 WebFilter 구현

### 10.1.1 WebFilter 인터페이스 이해

`WebFilter`는 Spring WebFlux의 핵심 확장점으로, 모든 HTTP 요청을 가로챌 수 있는 게이트웨이 역할을 한다. 어노테이션 기반 컨트롤러든 함수형 엔드포인트든 동일하게 적용되기 때문에 매우 강력하다.

```java
public interface WebFilter {
    Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain);
}
```

| 파라미터 | 설명 |
|---------|------|
| `ServerWebExchange` | HTTP 요청(`ServerHttpRequest`)과 응답(`ServerHttpResponse`)을 모두 담고 있는 컨텍스트 객체 |
| `WebFilterChain` | 다음 필터 또는 핸들러로 요청을 전달하는 체인 |

동작 방식은 **필터 체인** 패턴을 따른다. 각 필터가 `chain.filter(exchange)`를 호출하면 다음 필터로 요청이 전달되고, 그 반환값인 `Mono<Void>`에 리액티브 연산자를 붙여서 응답 처리를 할 수 있다.

```
[클라이언트] → [WebFilter 1] → [WebFilter 2] → ... → [핸들러]
                                                         ↓
[클라이언트] ← [WebFilter 1] ← [WebFilter 2] ← ... ← [응답]
```

### 10.1.2 요청 전후 처리 필터

가장 기본적인 패턴부터 보자. `@Component`로 등록하면 스프링이 알아서 필터 체인에 추가해주는데, `chain.filter()` 호출 전후에 코드를 끼워 넣으면 요청과 응답을 동시에 처리할 수 있다.

```java
@Slf4j
@Component
public class RequestTimingFilter implements WebFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        // === 전처리 ===
        long startTime = System.currentTimeMillis();
        String method = exchange.getRequest().getMethod().name();
        String path = exchange.getRequest().getURI().getPath();

        log.info(">>> 요청 시작: {} {}", method, path);

        return chain.filter(exchange)
            // === 후처리 ===
            .doFinally(signalType -> {
                long duration = System.currentTimeMillis() - startTime;
                log.info("<<< 요청 완료: {} {} - {}ms [{}]",
                    method, path, duration, signalType);
            });
    }
}
```

> **주의**: `then(Mono.fromRunnable(...))`은 정상 완료 시에만 실행된다. 에러를 포함한 모든 경우를 처리하려면 위 예시처럼 `doFinally`를 사용해야 한다.

### 10.1.3 @Order로 필터 실행 순서 지정

웹 애플리케이션이 복잡해지면 보안 검사, 로깅, 메트릭 수집 등 여러 필터를 체인 형태로 등록하게 되는데, 이때 실행 순서가 중요하다. `@Order` 어노테이션으로 간단히 제어할 수 있으며, 숫자가 작을수록 먼저 실행된다.

```java
@Component
@Order(1)
public class SecurityCheckFilter implements WebFilter { /* 보안 검사 */ }

@Component
@Order(2)
public class LoggingFilter implements WebFilter { /* 로깅 */ }

@Component
@Order(3)
public class MetricsFilter implements WebFilter { /* 메트릭 수집 */ }
```

`Ordered` 인터페이스를 구현하는 방법도 있다.

```java
@Component
public class HighPriorityFilter implements WebFilter, Ordered {
    @Override
    public int getOrder() { return Ordered.HIGHEST_PRECEDENCE; }

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        return chain.filter(exchange);
    }
}
```

### 10.1.4 조건부 필터 적용과 요청 차단

실무에서는 모든 요청에 필터를 적용할 필요는 없다. 특정 경로(예: `/api/**`)에만 필터를 작동시키려면 내부에서 경로를 확인하고 조건부로 동작하면 된다. 필자의 경험상, API 인증 같은 필터는 공개 엔드포인트를 거르는 것이 성능에 도움이 된다.

```java
@Slf4j
@Component
@Order(1)
public class ApiKeyFilter implements WebFilter {

    private static final String API_KEY_HEADER = "X-API-Key";
    private static final String VALID_API_KEY = "my-secret-api-key";

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String path = exchange.getRequest().getURI().getPath();

        // /api/** 경로에만 필터 적용
        if (!path.startsWith("/api/")) {
            return chain.filter(exchange);
        }

        String apiKey = exchange.getRequest().getHeaders().getFirst(API_KEY_HEADER);
        if (VALID_API_KEY.equals(apiKey)) {
            return chain.filter(exchange);
        }

        // 요청 차단: chain.filter()를 호출하지 않고 응답 완료
        log.warn("유효하지 않은 API Key 요청: {}", path);
        exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
        return exchange.getResponse().setComplete();
    }
}
```

### 10.1.5 요청 속성(Attribute) 전달

필터 단계에서 수집한 정보(예: 요청 ID, 사용자 정보)를 컨트롤러까지 전달해야 할 때가 있다. `ServerWebExchange`의 속성 맵을 활용하면 간단하게 해결된다.

```java
@Component
@Order(0)
public class RequestContextFilter implements WebFilter {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String requestId = UUID.randomUUID().toString().substring(0, 8);
        exchange.getAttributes().put("requestId", requestId);
        exchange.getResponse().getHeaders().add("X-Request-Id", requestId);
        return chain.filter(exchange);
    }
}

// 컨트롤러에서 속성 사용
@GetMapping("/api/products")
public Mono<ResponseEntity<List<Product>>> getProducts(ServerWebExchange exchange) {
    String requestId = exchange.getAttribute("requestId");
    log.info("[{}] 상품 목록 조회 요청", requestId);
    // ...
}
```

---

## 10.2 HandlerFilterFunction 활용

### 10.2.1 WebFilter와 HandlerFilterFunction 비교

WebFilter는 글로벌하게 모든 요청을 잡지만, `HandlerFilterFunction`은 다르다. 함수형 엔드포인트(RouterFunction) 기반 API에 특화된 필터로, 더 세밀한 제어가 가능하다.

```java
@FunctionalInterface
public interface HandlerFilterFunction<T extends ServerResponse, R extends ServerResponse> {
    Mono<R> filter(ServerRequest request, HandlerFunction<T> next);
}
```

| 항목 | WebFilter | HandlerFilterFunction |
|------|-----------|----------------------|
| 적용 대상 | 모든 요청 (어노테이션 + 함수형) | 함수형 엔드포인트만 |
| 적용 범위 | 글로벌 | 특정 RouterFunction |
| 접근 객체 | `ServerWebExchange` | `ServerRequest` / `ServerResponse` |
| 등록 방법 | `@Component` 자동 등록 | `RouterFunction.filter()` |

### 10.2.2 기본 사용법

가장 간단한 형태부터 보자. `RouterFunction`의 `filter()` 메서드에 람다식으로 필터 로직을 끼워 넣으면 된다.

```java
@Configuration
public class ProductRouter {
    @Bean
    public RouterFunction<ServerResponse> productRoutes(ProductHandler handler) {
        return nest(path("/api/products"),
            route(GET(""), handler::getAll)
            .andRoute(POST(""), handler::create)
            .andRoute(PUT("/{id}"), handler::update)
            .andRoute(DELETE("/{id}"), handler::delete)
        )
        .filter((request, next) -> {
            log.info("Product API 요청: {} {}", request.method(), request.path());
            return next.handle(request);
        });
    }
}
```

### 10.2.3 인증 필터 구현

이제 실제로 쓸 만한 예제를 봐보자. JWT 토큰 검증 같은 인증 필터를 `HandlerFilterFunction`으로 구현하는 패턴이다.

```java
public class AuthFilterFunction
        implements HandlerFilterFunction<ServerResponse, ServerResponse> {

    private final TokenValidator tokenValidator;

    public AuthFilterFunction(TokenValidator tokenValidator) {
        this.tokenValidator = tokenValidator;
    }

    @Override
    public Mono<ServerResponse> filter(ServerRequest request,
                                       HandlerFunction<ServerResponse> next) {
        String authHeader = request.headers().firstHeader("Authorization");

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return ServerResponse.status(HttpStatus.UNAUTHORIZED)
                .bodyValue(Map.of("error", "Authorization 헤더가 필요합니다."));
        }

        String token = authHeader.substring(7);

        return tokenValidator.validate(token)
            .flatMap(userId -> {
                ServerRequest modifiedRequest = ServerRequest.from(request)
                    .attribute("userId", userId)
                    .build();
                return next.handle(modifiedRequest);
            })
            .onErrorResume(InvalidTokenException.class, e ->
                ServerResponse.status(HttpStatus.UNAUTHORIZED)
                    .bodyValue(Map.of("error", e.getMessage()))
            );
    }
}
```

핵심은 라우터 정의 단계에서 공개 API와 보호 API를 명확히 분리하는 것이다. 그러면 필터를 선택적으로 적용할 수 있어서 불필요한 오버헤드를 피할 수 있다.

```java
@Configuration
public class AppRouter {

    private final TokenValidator tokenValidator;

    public AppRouter(TokenValidator tokenValidator) {
        this.tokenValidator = tokenValidator;
    }

    @Bean
    public RouterFunction<ServerResponse> routes(
            ProductHandler productHandler, AuthHandler authHandler) {

        // 인증 불필요: 공개 API
        RouterFunction<ServerResponse> publicRoutes = route(
            POST("/api/auth/login"), authHandler::login
        ).andRoute(
            POST("/api/auth/register"), authHandler::register
        );

        // 인증 필요: 보호된 API
        RouterFunction<ServerResponse> protectedRoutes = nest(path("/api/products"),
            route(GET(""), productHandler::getAll)
            .andRoute(POST(""), productHandler::create)
            .andRoute(DELETE("/{id}"), productHandler::delete)
        ).filter(new AuthFilterFunction(tokenValidator));

        return publicRoutes.and(protectedRoutes);
    }
}
```

### 10.2.4 역할 기반 접근 제어 필터

인증 필터만으로 부족하면 역할(Role) 기반 인가를 추가하면 된다. 필터를 여러 개 체이닝하면 인증(Authentication) 이후 인가(Authorization)가 순차적으로 실행되므로, 보안을 이중으로 확보할 수 있다.

```java
public class RoleFilterFunction
        implements HandlerFilterFunction<ServerResponse, ServerResponse> {

    private final Set<String> allowedRoles;

    public RoleFilterFunction(String... roles) {
        this.allowedRoles = Set.of(roles);
    }

    @Override
    public Mono<ServerResponse> filter(ServerRequest request,
                                       HandlerFunction<ServerResponse> next) {
        String userRole = request.attribute("userRole")
            .map(Object::toString).orElse("");

        if (allowedRoles.contains(userRole)) {
            return next.handle(request);
        }
        return ServerResponse.status(HttpStatus.FORBIDDEN)
            .bodyValue(Map.of("error", "접근 권한이 없습니다."));
    }
}

// 관리자 전용 API에 인증 + 역할 필터 체이닝
RouterFunction<ServerResponse> adminRoutes = nest(path("/api/admin"),
    route(GET("/users"), adminHandler::getAllUsers)
    .andRoute(DELETE("/users/{id}"), adminHandler::deleteUser)
)
.filter(new AuthFilterFunction(tokenValidator))
.filter(new RoleFilterFunction("ADMIN"));
```

---

## 10.3 요청/응답 로깅

### 10.3.1 요청 로깅 필터

프로덕션 환경에서는 요청의 생명주기를 추적해야 한다. 요청이 들어오는 순간부터 응답을 내보낼 때까지의 모든 정보를 체계적으로 기록해 놓으면, 나중에 문제 분석이 훨씬 수월하다.

```java
@Slf4j
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class RequestLoggingFilter implements WebFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        String requestId = UUID.randomUUID().toString().substring(0, 8);
        String method = request.getMethod().name();
        String path = request.getURI().getPath();
        String clientIp = extractClientIp(request);

        log.info("[{}] >>> {} {} ip={}", requestId, method, path, clientIp);

        long startTime = System.nanoTime();
        exchange.getResponse().getHeaders().add("X-Request-Id", requestId);
        exchange.getAttributes().put("requestId", requestId);

        return chain.filter(exchange)
            .doFinally(signalType -> {
                long durationMs = (System.nanoTime() - startTime) / 1_000_000;
                HttpStatusCode status = exchange.getResponse().getStatusCode();
                log.info("[{}] <<< {} {} -> {} ({}ms)",
                    requestId, method, path, status, durationMs);
            });
    }

    private String extractClientIp(ServerHttpRequest request) {
        String xff = request.getHeaders().getFirst("X-Forwarded-For");
        if (xff != null && !xff.isEmpty()) {
            return xff.split(",")[0].trim();
        }
        return Optional.ofNullable(request.getRemoteAddress())
            .map(addr -> addr.getAddress().getHostAddress())
            .orElse("unknown");
    }
}
```

### 10.3.2 응답 바디 로깅 (ServerHttpResponseDecorator)

요청만 기록해서는 부족할 때가 많다. 응답 내용도 알고 싶다면? 문제는 응답 바디가 스트림 형태라서 직접 읽을 수 없다는 점이다. `ServerHttpResponseDecorator`로 감싸면 쓰기 시점에 바이트를 가로챌 수 있다. 필자의 경험상, 디버깅할 때 이 기법이 정말 유용하다.

```java
@Slf4j
@Component
@Order(Ordered.HIGHEST_PRECEDENCE + 1)
public class ResponseBodyLoggingFilter implements WebFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        if (!log.isDebugEnabled()) return chain.filter(exchange);

        String requestId = exchange.getAttribute("requestId");
        ServerHttpResponse original = exchange.getResponse();

        ServerHttpResponseDecorator decorated = new ServerHttpResponseDecorator(original) {
            @Override
            public Mono<Void> writeWith(Publisher<? extends DataBuffer> body) {
                if (body instanceof Flux<? extends DataBuffer> fluxBody) {
                    return super.writeWith(fluxBody.buffer().map(dataBuffers -> {
                        DataBuffer joined = original.bufferFactory().join(dataBuffers);
                        byte[] content = new byte[joined.readableByteCount()];
                        joined.read(content);
                        DataBufferUtils.release(joined);
                        log.debug("[{}] 응답 바디: {}", requestId,
                            new String(content, StandardCharsets.UTF_8));
                        return original.bufferFactory().wrap(content);
                    }));
                }
                return super.writeWith(body);
            }
        };
        return chain.filter(exchange.mutate().response(decorated).build());
    }
}
```

> **주의**: 응답 바디 로깅은 메모리와 성능에 영향을 미친다. 반드시 디버그 레벨에서만 활성화하고, 대용량 응답에서는 크기 제한 로직을 추가해야 한다.

### 10.3.3 요청 추적 ID와 Reactor Context

여기서 한 가지 까다로운 문제가 발생한다. 리액티브 애플리케이션에서는 스레드가 계속 바뀌기 때문에, 기존의 ThreadLocal 기반 `MDC(Mapped Diagnostic Context)`가 제대로 작동하지 않는다는 것이다. 대신 Reactor의 **Context**를 활용하면 요청 추적 ID를 전체 리액티브 체인에 걸쳐 전파할 수 있다.

```java
@Slf4j
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class TraceIdFilter implements WebFilter {

    private static final String TRACE_ID_KEY = "traceId";

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String traceId = Optional.ofNullable(
                exchange.getRequest().getHeaders().getFirst("X-Trace-Id")
            ).orElse(UUID.randomUUID().toString());

        exchange.getResponse().getHeaders().add("X-Trace-Id", traceId);

        return chain.filter(exchange)
            .contextWrite(Context.of(TRACE_ID_KEY, traceId));
    }
}
```

서비스 계층에서 Context의 추적 ID를 활용한다.

```java
@Service
@Slf4j
public class ProductService {
    public Mono<Product> findById(String id) {
        return Mono.deferContextual(ctx -> {
            String traceId = ctx.getOrDefault("traceId", "N/A");
            log.info("[{}] 상품 조회: id={}", traceId, id);
            return productRepository.findById(id);
        });
    }
}
```

Spring Boot 3.x에서는 Micrometer **Context Propagation**을 사용하면 MDC 자동 전파를 구성할 수 있다.

```yaml
spring:
  reactor:
    context-propagation: auto
```

---

## 10.4 CORS 설정

### 10.4.1 CORS 개요

모던 웹 개발에서는 프론트엔드와 백엔드가 분리되어 있는 경우가 대부분이다. 브라우저의 보안 정책인 **동일 출처 정책(Same-Origin Policy)** 때문에, 다른 도메인(또는 포트)의 서버를 호출할 때 특별한 허가가 필요하다. 흔한 예로, 프런트엔드가 `http://localhost:3000`에서 백엔드 `http://localhost:8080`을 호출하면 CORS 에러가 발생한다. 서버가 이를 허용한다는 신호를 보내려면 응답에 적절한 헤더를 포함해야 한다.

| CORS 헤더 | 설명 |
|-----------|------|
| `Access-Control-Allow-Origin` | 허용할 출처 |
| `Access-Control-Allow-Methods` | 허용할 HTTP 메서드 |
| `Access-Control-Allow-Headers` | 허용할 요청 헤더 |
| `Access-Control-Allow-Credentials` | 쿠키/인증 정보 포함 허용 여부 |
| `Access-Control-Max-Age` | Preflight 요청 캐시 시간(초) |

### 10.4.2 WebFluxConfigurer를 이용한 글로벌 설정

CORS를 설정하는 방법은 여러 가지인데, 가장 깔끔한 것은 `WebFluxConfigurer` 인터페이스를 구현하는 방식이다. 모든 엔드포인트에 일괄 적용되므로 관리가 편하다.

```java
@Configuration
public class CorsConfig implements WebFluxConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("http://localhost:3000", "https://myapp.example.com")
            .allowedMethods("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS")
            .allowedHeaders("*")
            .exposedHeaders("X-Request-Id", "X-Trace-Id")
            .allowCredentials(true)
            .maxAge(3600);
    }
}
```

### 10.4.3 @CrossOrigin 어노테이션

전체 설정 대신 특정 컨트롤러나 메서드에만 CORS를 적용하고 싶으면 `@CrossOrigin`을 사용하면 된다. 클래스 레벨과 메서드 레벨에서 동시에 설정하면 둘이 **병합**되니 주의하자.

```java
@RestController
@RequestMapping("/api/products")
@CrossOrigin(origins = "http://localhost:3000", maxAge = 3600)
public class ProductController {

    @CrossOrigin(origins = "https://partner.example.com")
    @GetMapping("/{id}")
    public Mono<Product> getById(@PathVariable String id) {
        return productService.findById(id);
    }
}
```

### 10.4.4 CorsWebFilter (프로그래밍 방식)

함수형 엔드포인트를 사용하면 `@CrossOrigin` 어노테이션을 붙일 수 없다는 게 단점이다. 이 경우 `CorsWebFilter`를 빈으로 등록해서 프로그래매틱하게 설정하면, 어노테이션 기반과 함수형 모두 커버할 수 있다.

```java
@Configuration
public class CorsFilterConfig {

    @Bean
    public CorsWebFilter corsWebFilter() {
        CorsConfiguration config = new CorsConfiguration();
        config.addAllowedOrigin("http://localhost:3000");
        config.addAllowedOrigin("https://myapp.example.com");
        config.addAllowedMethod("*");
        config.addAllowedHeader("*");
        config.addExposedHeader("X-Request-Id");
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", config);
        return new CorsWebFilter(source);
    }
}
```

### 10.4.5 환경별 CORS 설정

실제로는 개발 환경에서는 어떤 출처든 허용하고, 프로덕션에서는 특정 도메인만 허용하는 식으로 환경별로 다르게 설정해야 한다. `application.yml` 프로파일을 활용하면 간단히 해결된다.

```yaml
# application.yml             → app.cors.allowed-origins: "http://localhost:3000"
# application-prod.yml        → app.cors.allowed-origins: "https://myapp.example.com"
```

```java
@Configuration
public class CorsConfig implements WebFluxConfigurer {

    @Value("${app.cors.allowed-origins}")
    private String[] allowedOrigins;

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins(allowedOrigins)
            .allowedMethods("GET", "POST", "PUT", "DELETE", "PATCH")
            .allowedHeaders("*")
            .allowCredentials(true)
            .maxAge(3600);
    }
}
```

---

## 10.5 요청 속도 제한(Rate Limiting)

### 10.5.1 토큰 버킷 알고리즘

만약 API를 공개한다면, 악의적인 사용자나 실수로 인한 과다 요청에 대비해야 한다. 이때 속도 제한(Rate Limiting)은 필수 기능이다. 여러 알고리즘이 있지만, 가장 널리 사용되는 건 토큰 버킷 알고리즘이다.

1. **버킷**에 토큰이 일정 속도로 채워진다.
2. 요청이 들어오면 버킷에서 토큰 1개를 소비한다.
3. 토큰이 없으면 요청을 거부한다(429 Too Many Requests).
4. 버킷 크기가 고정되어 순간적인 버스트(burst)를 일정 수준까지 허용한다.

```
[토큰 생성기] ---(초당 10개)---> [버킷 (최대 20개)]
                                       ↓
                                 요청 -> 토큰 1개 소비
                                 토큰 부족 -> 429 응답
```

### 10.5.2 Bucket4j 의존성

알고리즘을 직접 구현할 수도 있지만, **Bucket4j** 라이브러리를 사용하면 편하다. 토큰 버킷 알고리즘을 스레드 안전하게 구현했고, 성능도 검증되었다. `build.gradle.kts`에 의존성을 추가하자: `implementation("com.bucket4j:bucket4j-core:8.10.1")`

### 10.5.3 IP 기반 속도 제한 필터

가장 기본적인 구현은 클라이언트 IP를 기준으로 각각 독립적인 버킷을 유지하는 것이다. 필자의 경험상, 공개 API에는 이 정도면 충분하다.

```java
@Slf4j
@Component
public class RateLimitFilter implements WebFilter {

    private final Map<String, Bucket> bucketCache = new ConcurrentHashMap<>();

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String path = exchange.getRequest().getURI().getPath();
        if (!path.startsWith("/api/")) {
            return chain.filter(exchange);
        }

        String clientIp = extractClientIp(exchange);
        Bucket bucket = bucketCache.computeIfAbsent(clientIp, this::createBucket);
        ConsumptionProbe probe = bucket.tryConsumeAndReturnRemaining(1);

        if (probe.isConsumed()) {
            exchange.getResponse().getHeaders()
                .add("X-RateLimit-Remaining",
                    String.valueOf(probe.getRemainingTokens()));
            return chain.filter(exchange);
        }

        // 속도 제한 초과 -> 429 응답
        long waitSeconds = probe.getNanosToWaitForRefill() / 1_000_000_000;
        log.warn("속도 제한 초과: IP={}, 재시도까지 {}초", clientIp, waitSeconds);

        exchange.getResponse().setStatusCode(HttpStatus.TOO_MANY_REQUESTS);
        exchange.getResponse().getHeaders().setContentType(MediaType.APPLICATION_JSON);
        exchange.getResponse().getHeaders().add("Retry-After", String.valueOf(waitSeconds));

        String errorBody = """
            {
              "error": "TOO_MANY_REQUESTS",
              "message": "요청 속도 제한을 초과했습니다.",
              "retryAfterSeconds": %d
            }
            """.formatted(waitSeconds);

        return exchange.getResponse().writeWith(
            Mono.just(exchange.getResponse().bufferFactory()
                .wrap(errorBody.getBytes()))
        );
    }

    private Bucket createBucket(String key) {
        Bandwidth limit = Bandwidth.classic(
            10,                                      // 버킷 용량 (버스트)
            Refill.greedy(60, Duration.ofMinutes(1)) // 분당 60개 보충
        );
        return Bucket.builder().addLimit(limit).build();
    }

    private String extractClientIp(ServerWebExchange exchange) {
        String xff = exchange.getRequest().getHeaders().getFirst("X-Forwarded-For");
        if (xff != null && !xff.isEmpty()) return xff.split(",")[0].trim();
        return Optional.ofNullable(exchange.getRequest().getRemoteAddress())
            .map(addr -> addr.getAddress().getHostAddress()).orElse("unknown");
    }
}
```

### 10.5.4 사용자 등급별 차등 속도 제한

IP 기반만으로는 부족하면, 인증된 사용자별로 다른 할당량을 줄 수 있다. 무료 사용자는 분당 20건, 프리미엄은 1000건 같은 식으로 계층화할 수 있다. `Plan` enum으로 정책을 정의하고, 사용자 ID와 등급을 조합한 키로 버킷을 관리하는 게 핵심이다.

```java
@Slf4j
@Component
@Order(10)  // 인증 필터 이후에 실행
public class UserRateLimitFilter implements WebFilter {

    private final Map<String, Bucket> bucketCache = new ConcurrentHashMap<>();

    enum Plan {
        FREE(20, Duration.ofMinutes(1)),       // 무료: 분당 20건
        BASIC(100, Duration.ofMinutes(1)),      // 기본: 분당 100건
        PREMIUM(1000, Duration.ofMinutes(1));   // 프리미엄: 분당 1000건

        final int capacity;
        final Duration period;
        Plan(int capacity, Duration period) {
            this.capacity = capacity;
            this.period = period;
        }
    }

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String userId = exchange.getAttribute("userId");
        if (userId == null || !exchange.getRequest().getURI()
                .getPath().startsWith("/api/")) {
            return chain.filter(exchange);
        }

        String userPlan = exchange.getAttribute("userPlan");
        Plan plan = resolvePlan(userPlan);
        Bucket bucket = bucketCache.computeIfAbsent(
            userId + ":" + plan.name(), k -> createBucket(plan));

        ConsumptionProbe probe = bucket.tryConsumeAndReturnRemaining(1);

        // 남은 호출 횟수를 헤더로 전달
        exchange.getResponse().getHeaders()
            .add("X-RateLimit-Limit", String.valueOf(plan.capacity));
        exchange.getResponse().getHeaders()
            .add("X-RateLimit-Remaining", String.valueOf(probe.getRemainingTokens()));

        if (probe.isConsumed()) return chain.filter(exchange);

        // 429 응답 (IP 기반 필터와 동일한 패턴)
        exchange.getResponse().setStatusCode(HttpStatus.TOO_MANY_REQUESTS);
        String body = """
            {"error":"TOO_MANY_REQUESTS","plan":"%s","limit":%d}
            """.formatted(plan.name(), plan.capacity);
        return exchange.getResponse().writeWith(
            Mono.just(exchange.getResponse().bufferFactory().wrap(body.getBytes())));
    }

    private Plan resolvePlan(String planStr) {
        try { return Plan.valueOf(planStr.toUpperCase()); }
        catch (Exception e) { return Plan.FREE; }
    }

    private Bucket createBucket(Plan plan) {
        return Bucket.builder().addLimit(Bandwidth.classic(
            plan.capacity, Refill.greedy(plan.capacity, plan.period))).build();
    }
}
```

### 10.5.5 엔드포인트별 차등 속도 제한

로그인 API나 비밀번호 재설정 같은 민감한 엔드포인트는 각별한 주의가 필요하다. 이런 곳에는 `HandlerFilterFunction`으로 훨씬 더 엄격한 제한을 개별 적용할 수 있다.

```java
@Configuration
public class RateLimitConfig {

    @Bean
    public RouterFunction<ServerResponse> rateLimitedAuthRoutes(AuthHandler handler) {
        return route(POST("/api/auth/login"), handler::login)
            .filter(createRateLimitFilter(5, Duration.ofMinutes(1)))   // 분당 5회
            .andRoute(POST("/api/auth/register"), handler::register)
            .filter(createRateLimitFilter(3, Duration.ofHours(1)));    // 시간당 3회
    }

    private HandlerFilterFunction<ServerResponse, ServerResponse>
            createRateLimitFilter(int capacity, Duration period) {
        Map<String, Bucket> buckets = new ConcurrentHashMap<>();
        return (request, next) -> {
            String ip = request.remoteAddress()
                .map(a -> a.getAddress().getHostAddress()).orElse("unknown");
            Bucket bucket = buckets.computeIfAbsent(ip, k ->
                Bucket.builder().addLimit(
                    Bandwidth.classic(capacity, Refill.greedy(capacity, period))
                ).build());

            if (bucket.tryConsume(1)) return next.handle(request);

            return ServerResponse.status(HttpStatus.TOO_MANY_REQUESTS)
                .bodyValue(Map.of("error", "요청이 너무 많습니다."));
        };
    }
}
```

### 10.5.6 버킷 캐시 메모리 관리

여기서 놓치기 쉬운 점이 있다. `ConcurrentHashMap`에 IP별 버킷이 계속 쌓이면 언젠가는 메모리를 다 써버린다. 실제 운영 환경에서 이 문제를 겪었던 개발자는 Caffeine 캐시로 자동 만료를 구현하는 방법을 안다.

```kotlin
dependencies {
    implementation("com.github.ben-manes.caffeine:caffeine:3.1.8")
}
```

```java
private final Cache<String, Bucket> bucketCache = Caffeine.newBuilder()
    .maximumSize(100_000)
    .expireAfterAccess(Duration.ofMinutes(10))
    .build();

// 사용: bucketCache.get(clientIp, this::createBucket)
```

---

## 10.6 정리

| 주제 | 핵심 기술 | 적용 범위 |
|------|----------|----------|
| WebFilter | `WebFilter` 인터페이스, `@Order` | 모든 요청 (글로벌) |
| HandlerFilterFunction | `RouterFunction.filter()` | 함수형 엔드포인트 (선택적) |
| 요청/응답 로깅 | `ServerHttpResponseDecorator`, Reactor Context | 전역 로깅, 추적 ID |
| CORS | `WebFluxConfigurer`, `@CrossOrigin`, `CorsWebFilter` | API 전체 또는 개별 엔드포인트 |
| 속도 제한 | Bucket4j, 토큰 버킷 알고리즘 | IP별, 사용자별, 엔드포인트별 |

**실무에서 자주 적용되는 설계 원칙**은 다음과 같다:
- **글로벌 관심사**(로깅, 추적 ID, CORS)는 `WebFilter`로 모든 곳에 적용한다.
- **특정 API 그룹에만 필요한 로직**(인증, 인가, 특정 엔드포인트의 속도 제한)은 `HandlerFilterFunction`으로 선택적으로 적용한다.
- 필터 실행 순서(`@Order`)는 반드시 명시적으로 설정해서 예기치 않은 동작을 미리 차단한다.
- 응답 바디 로깅처럼 오버헤드가 큰 필터는 디버그 모드에서만 켜거나, 트래픽이 많은 시간대에는 비활성화하는 식으로 조건부 활성화를 고려한다.

이제 필터를 통한 기초적인 횡단 관심사 처리를 익혔으니, 다음 Chapter 11에서는 **Spring Security WebFlux**로 한 단계 업그레이드된 인증과 인가 시스템을 만들어보자. 이번 장에서 직접 구현한 인증 필터가 Spring Security의 강력한 `SecurityWebFilterChain`으로 어떻게 진화하는지 보게 될 것이다.
# Chapter 11. 리액티브 보안 (Spring Security WebFlux)

Spring WebFlux로 API 서버를 구축할 때 보안 구현 방식은 기존 서블릿 기반 Spring Security와 상당히 다르다. ThreadLocal이 작동하지 않고, 비동기 논블로킹 특성을 고려해야 하기 때문이다. 이 장에서는 WebFlux 환경에 맞춘 Spring Security 설정부터 시작해서 인증/인가, JWT 토큰 기반 인증, SecurityContext 다루기, 그리고 OAuth2 통합까지 단계적으로 살펴볼 것이다.

---

## 11.1 Spring Security Reactive 설정

### 11.1.1 의존성 추가

먼저 `build.gradle`에 필요한 Spring Security 의존성들을 넣어야 한다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    implementation 'org.springframework.boot:spring-boot-starter-security'
    implementation 'org.springframework.boot:spring-boot-starter-data-mongodb-reactive'

    // JWT (11.4절), OAuth2 (11.6절)
    implementation 'io.jsonwebtoken:jjwt-api:0.12.6'
    runtimeOnly 'io.jsonwebtoken:jjwt-impl:0.12.6'
    runtimeOnly 'io.jsonwebtoken:jjwt-jackson:0.12.6'
    implementation 'org.springframework.boot:spring-boot-starter-oauth2-client'
    implementation 'org.springframework.boot:spring-boot-starter-oauth2-resource-server'

    testImplementation 'org.springframework.security:spring-security-test'
}
```

재미있는 점은 이 의존성들을 추가하는 것만으로 자동으로 Spring Security가 활성화된다는 것이다. 모든 엔드포인트가 기본 인증으로 보호되기 시작한다.

### 11.1.2 서블릿 기반과의 차이

| 구분 | Servlet (Spring MVC) | Reactive (Spring WebFlux) |
|------|---------------------|--------------------------|
| **필터 체인** | `SecurityFilterChain` | `SecurityWebFilterChain` (`WebFilter`) |
| **설정 빌더** | `HttpSecurity` | `ServerHttpSecurity` |
| **인증 저장소** | `SecurityContextHolder` (ThreadLocal) | `ReactiveSecurityContextHolder` (Reactor Context) |
| **UserDetailsService** | `UserDetailsService` | `ReactiveUserDetailsService` |
| **인증 매니저** | `AuthenticationManager` | `ReactiveAuthenticationManager` |
| **메서드 보안** | `@EnableMethodSecurity` | `@EnableReactiveMethodSecurity` |

가장 크리티컬한 차이는 **인증 정보를 어디에 저장하는가** 하는 문제다. 전통적인 서블릿 환경에서는 `ThreadLocal`을 이용하는데, 리액티브는 한 요청이 여러 스레드를 타고 처리되므로 이 방식이 작동하지 않는다. 대신 **Reactor의 Context** 메커니즘을 활용해야 한다.

### 11.1.3 기본 보안 설정 클래스

이제 실제로 보안을 구성해 보자. `@EnableWebFluxSecurity` 어노테이션으로 리액티브 보안을 켜고 `SecurityWebFilterChain` 빈을 정의하면 된다.

```java
@Configuration
@EnableWebFluxSecurity
public class SecurityConfig {

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        return http
            .authorizeExchange(exchanges -> exchanges
                .anyExchange().authenticated()
            )
            .httpBasic(Customizer.withDefaults())
            .formLogin(Customizer.withDefaults())
            .build();
    }
}
```

`Customizer.withDefaults()`는 Spring Security 6.1 이상에서 권장되는 설정 패턴이다.

---

## 11.2 SecurityWebFilterChain 구성

### 11.2.1 ServerHttpSecurity 주요 설정

`ServerHttpSecurity`라는 빌더를 통해 리액티브 보안을 상세하게 설정한다. 어떤 경로를 누구에게 열어줄지, CORS는 어떻게 할지 등을 여기서 결정한다.

```java
@Bean
public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
    return http
        .authorizeExchange(exchanges -> exchanges
            .pathMatchers(HttpMethod.GET, "/api/products/**").permitAll()
            .pathMatchers(HttpMethod.POST, "/api/products/**").hasRole("ADMIN")
            .pathMatchers("/api/admin/**").hasRole("ADMIN")
            .pathMatchers("/api/users/signup", "/api/users/login").permitAll()
            .anyExchange().authenticated()
        )
        .httpBasic(Customizer.withDefaults())
        .csrf(csrf -> csrf.disable())
        .cors(cors -> cors.configurationSource(corsConfigurationSource()))
        .formLogin(formLogin -> formLogin.disable())
        .build();
}
```

### 11.2.2 authorizeExchange 상세 설정

`authorizeExchange` 내에서 쓸 수 있는 여러 매처와 권한 검증 규칙들을 정리해 보면 다음과 같다.

```java
.authorizeExchange(exchanges -> exchanges
    // HTTP 메서드 + 경로 조합
    .pathMatchers(HttpMethod.GET, "/api/products/**").permitAll()
    .pathMatchers(HttpMethod.DELETE, "/api/**").hasRole("ADMIN")

    // 역할/권한 기반 인가
    .pathMatchers("/api/manager/**").hasAnyRole("ADMIN", "MANAGER")
    .pathMatchers("/api/reports/**").hasAuthority("REPORT_READ")

    // 커스텀 인가 로직
    .pathMatchers("/api/users/{userId}/**")
        .access((authentication, context) -> {
            String userId = context.getVariables().get("userId");
            return authentication
                .map(auth -> auth.getName().equals(userId))
                .map(AuthorizationDecision::new);
        })

    .anyExchange().authenticated()
)
```

### 11.2.3 CSRF와 CORS 설정

API 서버를 만들 때는 보통 CSRF를 꺼둔다. 쿠키 기반 토큰이 필요하지 않기 때문이다. 다만 SPA 같은 브라우저 기반 애플리케이션이라면 쿠키에 저장된 CSRF 토큰을 검증해야 한다.

```java
// REST API: CSRF 비활성화
.csrf(csrf -> csrf.disable())

// 브라우저 기반: 쿠키 CSRF 토큰
.csrf(csrf -> csrf
    .csrfTokenRepository(CookieServerCsrfTokenRepository.withHttpOnlyFalse()))
```

CORS 정책은 `CorsConfigurationSource` 빈을 통해 설정하는 것이 일반적이다.

```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("http://localhost:3000"));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    config.setAllowedHeaders(List.of("*"));
    config.setAllowCredentials(true);

    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}
```

---

## 11.3 인증과 인가 구현

### 11.3.1 ReactiveUserDetailsService

리액티브 환경에서는 당연히 `ReactiveUserDetailsService`를 사용해야 한다. 비동기로 사용자 정보를 조회해서 `Mono<UserDetails>`로 반환하는 방식이다. 먼저 사용자 도메인과 MongoDB 리포지토리를 먼저 만들어 보자.

```java
@Document(collection = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {
    @Id
    private String id;
    private String username;
    private String password;
    private String email;
    private List<String> roles;
    private boolean enabled;
    private LocalDateTime createdAt;
}
```

```java
public interface UserRepository extends ReactiveMongoRepository<User, String> {
    Mono<User> findByUsername(String username);
    Mono<Boolean> existsByUsername(String username);
}
```

이제 MongoDB에서 사용자를 조회하는 `ReactiveUserDetailsService`를 구현해 보자.

```java
@Service
@RequiredArgsConstructor
public class MongoUserDetailsService implements ReactiveUserDetailsService {

    private final UserRepository userRepository;

    @Override
    public Mono<UserDetails> findByUsername(String username) {
        return userRepository.findByUsername(username)
            .map(user -> org.springframework.security.core.userdetails.User.builder()
                .username(user.getUsername())
                .password(user.getPassword())
                .roles(user.getRoles().toArray(new String[0]))
                .disabled(!user.isEnabled())
                .build()
            )
            .switchIfEmpty(Mono.error(
                new UsernameNotFoundException("사용자를 찾을 수 없습니다: " + username)
            ));
    }
}
```

### 11.3.2 PasswordEncoder와 회원가입

비밀번호는 절대 평문으로 저장하면 안 되고, BCrypt 같은 해시 알고리즘으로 암호화해서 저장해야 한다.

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
```

```java
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public Mono<User> signup(SignupRequest request) {
        return userRepository.existsByUsername(request.getUsername())
            .flatMap(exists -> {
                if (exists) {
                    return Mono.error(new DuplicateException("이미 사용 중인 사용자명입니다."));
                }
                User user = User.builder()
                    .username(request.getUsername())
                    .password(passwordEncoder.encode(request.getPassword()))
                    .email(request.getEmail())
                    .roles(List.of("USER"))
                    .enabled(true)
                    .createdAt(LocalDateTime.now())
                    .build();
                return userRepository.save(user);
            });
    }
}
```

### 11.3.3 @PreAuthorize 메서드 보안

`@EnableReactiveMethodSecurity`를 켜면 서비스 메서드 단위에서 세분화된 권한 검증을 할 수 있다. 이건 정말 유용한 기능이다.

```java
@Configuration
@EnableWebFluxSecurity
@EnableReactiveMethodSecurity
public class SecurityConfig {
    // SecurityWebFilterChain 빈 정의
}
```

```java
@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;

    @PreAuthorize("hasRole('ADMIN')")
    public Mono<Product> create(Product product) {
        product.setCreatedAt(LocalDateTime.now());
        return productRepository.save(product);
    }

    @PreAuthorize("hasRole('ADMIN') or hasRole('MANAGER')")
    public Mono<Product> update(String id, Product product) {
        return productRepository.findById(id)
            .map(existing -> {
                existing.setName(product.getName());
                existing.setPrice(product.getPrice());
                existing.setUpdatedAt(LocalDateTime.now());
                return existing;
            })
            .flatMap(productRepository::save);
    }

    // 현재 사용자 본인의 데이터만 조회 허용
    @PreAuthorize("#username == authentication.name or hasRole('ADMIN')")
    public Mono<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }
}
```

필자의 경험상 리액티브 환경에서도 `@PreAuthorize`는 `Mono`/`Flux` 반환 타입을 문제없이 처리한다. 권한이 없으면 `AccessDeniedException`이 던져지는데, 이를 적절히 핸들링해야 한다.

---

## 11.4 JWT 기반 인증 구현

요즘 REST API 서버에서는 세션을 쓰지 않고 JWT(JSON Web Token)로 무상태 인증을 한다. JWT는 Header(헤더-알고리즘/타입), Payload(페이로드-클레임), Signature(서명) 이렇게 세 부분으로 나뉜다. 이 방식은 확장성이 좋고, 마이크로서비스 환경에 잘 맞는다.

### 11.4.1 JWT 유틸리티 클래스

jjwt 라이브러리는 JWT를 쉽게 다루기 위한 라이브러리인데, 이걸 활용해서 토큰을 생성하고 검증하고 파싱하는 유틸리티를 만들어 보자.

```java
@Component
public class JwtTokenProvider {

    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.access-token-expiration}")
    private long accessTokenExpiration;

    @Value("${jwt.refresh-token-expiration}")
    private long refreshTokenExpiration;

    private SecretKey key;

    @PostConstruct
    public void init() {
        this.key = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secretKey));
    }

    public String generateAccessToken(UserDetails userDetails) {
        Map<String, Object> claims = Map.of("roles",
            userDetails.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority).toList());
        return createToken(claims, userDetails.getUsername(), accessTokenExpiration);
    }

    public String generateRefreshToken(UserDetails userDetails) {
        return createToken(Map.of(), userDetails.getUsername(), refreshTokenExpiration);
    }

    private String createToken(Map<String, Object> claims, String subject,
                               long expiration) {
        Date now = new Date();
        return Jwts.builder()
            .claims(claims).subject(subject).issuedAt(now)
            .expiration(new Date(now.getTime() + expiration))
            .signWith(key).compact();
    }

    public String getUsernameFromToken(String token) {
        return getClaims(token).getSubject();
    }

    @SuppressWarnings("unchecked")
    public List<String> getRolesFromToken(String token) {
        return getClaims(token).get("roles", List.class);
    }

    public boolean validateToken(String token) {
        try { getClaims(token); return true; }
        catch (JwtException | IllegalArgumentException e) { return false; }
    }

    private Claims getClaims(String token) {
        return Jwts.parser().verifyWith(key).build()
            .parseSignedClaims(token).getPayload();
    }
}
```

`application.yml` 설정을 추가한다.

```yaml
jwt:
  secret: "dGhpcyBpcyBhIHZlcnkgbG9uZyBzZWNyZXQga2V5IGZvciBIUzI1NiBhbGdvcml0aG0="
  access-token-expiration: 3600000     # 1시간
  refresh-token-expiration: 604800000  # 7일
```

### 11.4.2 JWT 인증 필터

Authorization 헤더에서 JWT를 추출해서 검증하고 `Authentication` 객체로 변환하는 컨버터와 매니저를 만들어야 한다.

```java
@Component
@RequiredArgsConstructor
public class JwtAuthenticationConverter implements ServerAuthenticationConverter {

    private final JwtTokenProvider jwtTokenProvider;

    @Override
    public Mono<Authentication> convert(ServerWebExchange exchange) {
        return Mono.justOrEmpty(
                exchange.getRequest().getHeaders().getFirst(HttpHeaders.AUTHORIZATION))
            .filter(header -> header.startsWith("Bearer "))
            .map(header -> header.substring(7))
            .filter(jwtTokenProvider::validateToken)
            .map(token -> {
                String username = jwtTokenProvider.getUsernameFromToken(token);
                List<GrantedAuthority> authorities = jwtTokenProvider
                    .getRolesFromToken(token).stream()
                    .map(SimpleGrantedAuthority::new)
                    .collect(Collectors.toList());
                return new UsernamePasswordAuthenticationToken(
                    username, null, authorities);
            });
    }
}
```

```java
@Component
@RequiredArgsConstructor
public class JwtReactiveAuthenticationManager implements ReactiveAuthenticationManager {

    private final ReactiveUserDetailsService userDetailsService;

    @Override
    public Mono<Authentication> authenticate(Authentication authentication) {
        return userDetailsService.findByUsername(authentication.getName())
            .map(userDetails -> new UsernamePasswordAuthenticationToken(
                userDetails, null, authentication.getAuthorities()));
    }
}
```

### 11.4.3 JWT SecurityWebFilterChain 구성

위에서 만든 컨버터와 매니저를 사용해서 JWT 기반의 완전한 보안 설정을 구성해 보자.

```java
@Configuration
@EnableWebFluxSecurity
@EnableReactiveMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtReactiveAuthenticationManager authenticationManager;
    private final JwtAuthenticationConverter authenticationConverter;

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        AuthenticationWebFilter jwtFilter =
            new AuthenticationWebFilter(authenticationManager);
        jwtFilter.setServerAuthenticationConverter(authenticationConverter);

        return http
            .authorizeExchange(exchanges -> exchanges
                .pathMatchers("/api/auth/**").permitAll()
                .pathMatchers(HttpMethod.GET, "/api/products/**").permitAll()
                .pathMatchers("/api/admin/**").hasRole("ADMIN")
                .anyExchange().authenticated()
            )
            .addFilterAt(jwtFilter, SecurityWebFiltersOrder.AUTHENTICATION)
            .httpBasic(httpBasic -> httpBasic.disable())
            .formLogin(formLogin -> formLogin.disable())
            .csrf(csrf -> csrf.disable())
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint((exchange, e) -> Mono.fromRunnable(
                    () -> exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED)))
                .accessDeniedHandler((exchange, denied) -> Mono.fromRunnable(
                    () -> exchange.getResponse().setStatusCode(HttpStatus.FORBIDDEN)))
            )
            .securityContextRepository(NoOpServerSecurityContextRepository.getInstance())
            .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

`NoOpServerSecurityContextRepository`를 설정하면 서버에서 세션을 전혀 생성하지 않는 완전한 stateless 구조가 완성된다.

### 11.4.4 인증 컨트롤러

이제 클라이언트가 회원가입하고 로그인하고 토큰을 갱신할 수 있도록 엔드포인트들을 만들어 보자.

```java
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserService userService;
    private final ReactiveUserDetailsService userDetailsService;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    @PostMapping("/signup")
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<UserResponse> signup(@Valid @RequestBody SignupRequest request) {
        return userService.signup(request).map(UserResponse::from);
    }

    @PostMapping("/login")
    public Mono<TokenResponse> login(@Valid @RequestBody LoginRequest request) {
        return userDetailsService.findByUsername(request.getUsername())
            .filter(ud -> passwordEncoder.matches(
                request.getPassword(), ud.getPassword()))
            .map(ud -> new TokenResponse(
                jwtTokenProvider.generateAccessToken(ud),
                jwtTokenProvider.generateRefreshToken(ud)))
            .switchIfEmpty(Mono.error(
                new BadCredentialsException("잘못된 사용자명 또는 비밀번호입니다.")));
    }

    @PostMapping("/refresh")
    public Mono<TokenResponse> refresh(@RequestBody RefreshTokenRequest request) {
        String refreshToken = request.getRefreshToken();
        if (!jwtTokenProvider.validateToken(refreshToken)) {
            return Mono.error(
                new BadCredentialsException("유효하지 않은 리프레시 토큰입니다."));
        }
        String username = jwtTokenProvider.getUsernameFromToken(refreshToken);
        return userDetailsService.findByUsername(username)
            .map(ud -> new TokenResponse(
                jwtTokenProvider.generateAccessToken(ud), refreshToken));
    }
}
```

컨트롤러에서 사용할 요청/응답 DTO도 정의해야 한다.

```java
@Data
public class LoginRequest {
    @NotBlank private String username;
    @NotBlank private String password;
}

@Data
public class RefreshTokenRequest {
    @NotBlank private String refreshToken;
}

@Data
@AllArgsConstructor
public class TokenResponse {
    private String accessToken;
    private String refreshToken;
}
```

### 11.4.5 전체 인증 흐름

JWT 기반 인증이 어떻게 흘러가는지 정리하면 다음과 같다.

1. **회원가입**: `POST /api/auth/signup` — 입력받은 비밀번호를 BCrypt로 인코딩해서 MongoDB에 저장
2. **로그인**: `POST /api/auth/login` — 사용자명과 비밀번호를 검증하면 Access Token과 Refresh Token을 발급
3. **인증된 API 호출**: `Authorization: Bearer <accessToken>` 헤더를 붙여서 요청 — `JwtAuthenticationConverter`가 토큰을 추출하고 검증한 뒤 `Authentication` 객체 생성
4. **토큰 갱신**: `POST /api/auth/refresh` — Refresh Token이 유효하면 새로운 Access Token을 발급

---

## 11.5 리액티브 환경에서의 SecurityContext 관리

### 11.5.1 ReactiveSecurityContextHolder

서블릿 환경의 `SecurityContextHolder.getContext()`는 ThreadLocal 기반인데, 리액티브 환경에서는 이걸 쓰면 안 된다.

```java
// 리액티브 환경에서의 올바른 방식
Mono<String> username = ReactiveSecurityContextHolder.getContext()
    .map(SecurityContext::getAuthentication)
    .map(Authentication::getName);
```

### 11.5.2 현재 사용자 정보 가져오기

서비스 계층에서 현재 로그인한 사용자 정보를 어떻게 가져오는지 살펴보자.

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;

    public Flux<Order> getMyOrders() {
        return ReactiveSecurityContextHolder.getContext()
            .map(ctx -> ctx.getAuthentication().getName())
            .flatMapMany(orderRepository::findByUsername);
    }

    public Mono<Order> createOrder(OrderRequest request) {
        return ReactiveSecurityContextHolder.getContext()
            .map(ctx -> ctx.getAuthentication().getName())
            .flatMap(username -> {
                Order order = Order.builder()
                    .username(username)
                    .items(request.getItems())
                    .totalAmount(request.getTotalAmount())
                    .createdAt(LocalDateTime.now())
                    .build();
                return orderRepository.save(order);
            });
    }
}
```

### 11.5.3 컨트롤러에서 인증 정보 접근

컨트롤러의 핸들러 메서드에서는 `@AuthenticationPrincipal`이나 `Mono<Principal>`을 주입받는 방식이 더 편하다.

```java
@GetMapping("/me")
public Mono<UserResponse> getMyProfile(
        @AuthenticationPrincipal Mono<UserDetails> principal) {
    return principal
        .flatMap(user -> userService.findByUsername(user.getUsername()))
        .map(UserResponse::from);
}

@GetMapping("/me/orders")
public Flux<Order> getMyOrders(Mono<Principal> principal) {
    return principal.map(Principal::getName)
        .flatMapMany(orderService::findByUsername);
}
```

### 11.5.4 SecurityContext 주의사항

`ReactiveSecurityContextHolder.getContext()`의 반환값은 반드시 리액티브 체인 내부에서 `map`/`flatMap`으로 계속 연결해야 한다. Reactor의 Context는 구독할 때 전파되는데, 체인이 끊기면 SecurityContext를 더 이상 읽을 수 없기 때문이다. 필자의 경험상 이것 때문에 생기는 버그가 많다.

```java
// 잘못된 사용: context를 구독하지 않으므로 SecurityContext 접근 불가
Mono<SecurityContext> context = ReactiveSecurityContextHolder.getContext();
return orderRepository.save(order);

// 올바른 사용: 체인 내부에서 연결
return ReactiveSecurityContextHolder.getContext()
    .map(ctx -> ctx.getAuthentication().getName())
    .flatMap(username -> orderRepository.save(buildOrder(request, username)));
```

---

## 11.6 OAuth2 / OpenID Connect 연동

### 11.6.1 OAuth2 Login 설정

구글이나 깃허브 같은 소셜 로그인을 지원하려면 `application.yml`에 OAuth2 클라이언트 정보를 등록해야 한다.

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: ${GOOGLE_CLIENT_ID}
            client-secret: ${GOOGLE_CLIENT_SECRET}
            scope: openid, profile, email
          github:
            client-id: ${GITHUB_CLIENT_ID}
            client-secret: ${GITHUB_CLIENT_SECRET}
            scope: read:user, user:email
        provider:
          github:
            user-name-attribute: login
```

구글은 OpenID Connect를 지원해서 provider 설정이 자동으로 적용되지만, 깃허브는 `user-name-attribute`를 직접 지정해 줘야 한다.

### 11.6.2 OAuth2 SecurityWebFilterChain 설정

OAuth2 로그인을 활성화하는 보안 설정은 매우 간단하다.

```java
@Configuration
@EnableWebFluxSecurity
public class OAuth2SecurityConfig {

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        return http
            .authorizeExchange(exchanges -> exchanges
                .pathMatchers("/", "/login/**", "/oauth2/**").permitAll()
                .anyExchange().authenticated()
            )
            .oauth2Login(Customizer.withDefaults())
            .csrf(csrf -> csrf.disable())
            .build();
    }
}
```

`oauth2Login(Customizer.withDefaults())`라는 한 줄의 설정만으로 `/oauth2/authorization/{registrationId}` 엔드포인트와 리다이렉트 콜백이 자동으로 준비된다. 정말 편하다.

### 11.6.3 OAuth2 사용자 정보 커스터마이징

소셜 로그인이 성공한 후에 사용자 정보를 우리 MongoDB에 저장하고 싶다면 `ReactiveOAuth2UserService`를 커스터마이징해야 한다.

```java
@Service
@RequiredArgsConstructor
public class CustomOAuth2UserService
        implements ReactiveOAuth2UserService<OidcUserRequest, OidcUser> {

    private final UserRepository userRepository;
    private final ReactiveOidcUserService delegate = new ReactiveOidcUserService();

    @Override
    public Mono<OidcUser> loadUser(OidcUserRequest userRequest) {
        return delegate.loadUser(userRequest)
            .flatMap(oidcUser -> {
                String email = oidcUser.getEmail();
                String provider = userRequest.getClientRegistration()
                    .getRegistrationId();
                return userRepository.findByEmail(email)
                    .switchIfEmpty(createOAuth2User(email, oidcUser.getFullName(),
                                                     provider))
                    .thenReturn(oidcUser);
            });
    }

    private Mono<User> createOAuth2User(String email, String name, String provider) {
        User user = User.builder()
            .username(email).email(email).password("")
            .roles(List.of("USER")).enabled(true)
            .createdAt(LocalDateTime.now()).build();
        return userRepository.save(user);
    }
}
```

### 11.6.4 Resource Server 설정

Keycloak이나 Auth0 같은 외부 인증 서버에서 발급받은 JWT를 검증해야 하는 경우가 있다. 이 경우 우리 애플리케이션은 Resource Server가 되는데, 그 설정 방법을 살펴보자.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/my-realm
```

```java
@Configuration
@EnableWebFluxSecurity
public class ResourceServerConfig {

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        return http
            .authorizeExchange(exchanges -> exchanges
                .pathMatchers(HttpMethod.GET, "/api/products/**").permitAll()
                .pathMatchers("/api/admin/**").hasAuthority("SCOPE_admin")
                .anyExchange().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .csrf(csrf -> csrf.disable())
            .build();
    }

    @Bean
    public ReactiveJwtAuthenticationConverter jwtAuthenticationConverter() {
        JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter =
            new JwtGrantedAuthoritiesConverter();
        grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");
        grantedAuthoritiesConverter.setAuthoritiesClaimName("roles");

        ReactiveJwtAuthenticationConverter converter =
            new ReactiveJwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(
            new ReactiveJwtGrantedAuthoritiesConverterAdapter(
                grantedAuthoritiesConverter));
        return converter;
    }
}
```

### 11.6.5 JWT와 OAuth2의 선택 기준

| 시나리오 | 권장 방식 |
|----------|----------|
| 단순한 단일 애플리케이션, 자체 인증 처리 | JWT 자체 발급 (11.4절) |
| 마이크로서비스 아키텍처, 중앙 인증 서버 | OAuth2 Resource Server |
| 구글/깃허브 같은 소셜 로그인 필요 | OAuth2 Login |
| SPA와 API 서버 분리 | JWT 자체 발급 또는 OAuth2 + PKCE |

---

## 요약

이 장에서 배운 내용의 핵심을 정리하면 다음과 같다.

| 주제 | 핵심 내용 |
|------|----------|
| **리액티브 보안 설정** | `@EnableWebFluxSecurity`와 `SecurityWebFilterChain`으로 WebFlux 보안 활성화, ThreadLocal 대신 Reactor Context 사용 |
| **경로별 인가 설정** | `ServerHttpSecurity`의 `authorizeExchange`로 세분화된 접근 제어, CSRF/CORS 설정 |
| **인증과 인가** | `ReactiveUserDetailsService` 구현, BCrypt 해싱, `@PreAuthorize` 메서드 보안 |
| **JWT 기반 인증** | `JwtTokenProvider`로 토큰 생성/검증, `AuthenticationWebFilter` 통합, 완전한 stateless 구조 |
| **현재 사용자 정보** | `ReactiveSecurityContextHolder`로 인증 정보 조회, 리액티브 체인 내부에서 map/flatMap 연결 필수 |
| **OAuth2 지원** | OAuth2 Login으로 소셜 로그인, Resource Server로 외부 JWT 검증, 사용자 정보 자동 저장 |

다음 장에서는 Server-Sent Events(SSE)를 활용해서 클라이언트에게 실시간으로 데이터를 스트리밍하는 방법을 다룬다.
