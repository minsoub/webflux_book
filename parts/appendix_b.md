# 부록 B. MongoDB 쿼리 연산자 정리

이 부록에서는 MongoDB의 주요 쿼리 연산자를 카테고리별로 정리하고, 각 연산자에 대해 MongoDB 네이티브 쿼리와 Spring Data MongoDB(Criteria API)로 변환한 Java 코드를 함께 제공한다.

---

## B.1 비교 연산자

| 연산자 | 설명 | MongoDB 쿼리 예제 | Spring Data Criteria |
|--------|------|-------------------|---------------------|
| `$eq` | 값이 같음 | `{ status: { $eq: "active" } }` | `Criteria.where("status").is("active")` |
| `$ne` | 값이 같지 않음 | `{ status: { $ne: "inactive" } }` | `Criteria.where("status").ne("inactive")` |
| `$gt` | 초과 | `{ age: { $gt: 25 } }` | `Criteria.where("age").gt(25)` |
| `$gte` | 이상 | `{ age: { $gte: 18 } }` | `Criteria.where("age").gte(18)` |
| `$lt` | 미만 | `{ age: { $lt: 65 } }` | `Criteria.where("age").lt(65)` |
| `$lte` | 이하 | `{ age: { $lte: 65 } }` | `Criteria.where("age").lte(65)` |
| `$in` | 배열 내 값과 일치 | `{ status: { $in: ["active", "pending"] } }` | `Criteria.where("status").in("active", "pending")` |
| `$nin` | 배열 내 어떤 값과도 불일치 | `{ role: { $nin: ["admin"] } }` | `Criteria.where("role").nin("admin")` |

**범위 조건 결합 예제:**

```javascript
// MongoDB: 나이가 18 이상 65 이하
db.users.find({ age: { $gte: 18, $lte: 65 } })
```

```java
// Spring Data MongoDB
Criteria criteria = Criteria.where("age").gte(18).lte(65);
reactiveMongoTemplate.find(Query.query(criteria), User.class);
```

---

## B.2 논리 연산자

| 연산자 | 설명 |
|--------|------|
| `$and` | 모든 조건을 만족하는 도큐먼트를 선택 |
| `$or` | 하나 이상의 조건을 만족하는 도큐먼트를 선택 |
| `$not` | 조건을 만족하지 않는 도큐먼트를 선택 |
| `$nor` | 모든 조건을 만족하지 않는 도큐먼트를 선택 |

```javascript
// $and: status가 "active"이고 age가 18 이상
db.users.find({ $and: [{ status: "active" }, { age: { $gte: 18 } }] })
// $or: role이 "admin"이거나 age가 30 이상
db.users.find({ $or: [{ role: "admin" }, { age: { $gte: 30 } }] })
// $nor: status가 "active"도 아니고 role이 "admin"도 아닌 도큐먼트
db.users.find({ $nor: [{ status: "active" }, { role: "admin" }] })
```

```java
// $and — Criteria 체이닝으로 AND 조건이 된다
Criteria and = Criteria.where("status").is("active").and("age").gte(18);
// $or
Criteria or = new Criteria().orOperator(
    Criteria.where("role").is("admin"),
    Criteria.where("age").gte(30));
// $not
Criteria not = Criteria.where("age").not().gt(25);
// $nor
Criteria nor = new Criteria().norOperator(
    Criteria.where("status").is("active"),
    Criteria.where("role").is("admin"));
```

---

## B.3 요소 연산자

| 연산자 | 설명 | MongoDB 쿼리 예제 | Spring Data Criteria |
|--------|------|-------------------|---------------------|
| `$exists` | 필드 존재 여부 확인 | `{ email: { $exists: true } }` | `Criteria.where("email").exists(true)` |
| `$type` | 필드의 BSON 타입 확인 | `{ age: { $type: "int" } }` | `Criteria.where("age").type(Type.INT32)` |

---

## B.4 배열 연산자

| 연산자 | 설명 |
|--------|------|
| `$all` | 배열이 지정된 모든 요소를 포함 |
| `$elemMatch` | 배열 내 요소가 모든 조건을 만족 |
| `$size` | 배열 크기가 일치 |

```javascript
// $all: tags에 "mongodb"와 "reactive" 모두 포함
db.articles.find({ tags: { $all: ["mongodb", "reactive"] } })
// $elemMatch: scores 중 80~90 사이 요소가 존재
db.students.find({ scores: { $elemMatch: { $gte: 80, $lte: 90 } } })
// $size: tags 길이가 정확히 3
db.articles.find({ tags: { $size: 3 } })
```

```java
Criteria all = Criteria.where("tags").all("mongodb", "reactive");
Criteria elem = Criteria.where("scores").elemMatch(new Criteria().gte(80).lte(90));
Criteria size = Criteria.where("tags").size(3);
```

---

## B.5 정규식 연산자

```javascript
// name이 "Kim"으로 시작 (대소문자 무시)
db.users.find({ name: { $regex: "^Kim", $options: "i" } })
// email이 "@example.com"으로 끝남
db.users.find({ email: { $regex: "@example\\.com$" } })
```

```java
Criteria regex1 = Criteria.where("name").regex("^Kim", "i");
Criteria regex2 = Criteria.where("email").regex("@example\\.com$");
reactiveMongoTemplate.find(Query.query(regex1), User.class);
```

---

## B.6 업데이트 연산자

| 연산자 | 설명 | Update API |
|--------|------|-----------|
| `$set` | 필드 값 설정 | `new Update().set("field", value)` |
| `$unset` | 필드 제거 | `new Update().unset("field")` |
| `$inc` | 값 증감 | `new Update().inc("field", 1)` |
| `$push` | 배열에 요소 추가 | `new Update().push("field", value)` |
| `$pull` | 배열에서 요소 제거 | `new Update().pull("field", value)` |
| `$addToSet` | 중복 없이 배열에 추가 | `new Update().addToSet("field", value)` |

### $set / $unset / $inc

```javascript
db.users.updateOne({ _id: ObjectId("...") },
  { $set: { status: "inactive" }, $inc: { loginCount: 1 }, $unset: { temp: "" } })
```

```java
Query query = Query.query(Criteria.where("id").is(userId));
Update update = new Update()
    .set("status", "inactive")
    .inc("loginCount", 1)
    .unset("temp");
reactiveMongoTemplate.updateFirst(query, update, User.class);
```

### $push / $pull / $addToSet

```javascript
db.articles.updateOne({ _id: ObjectId("...") }, { $push: { tags: "webflux" } })
db.articles.updateOne({ _id: ObjectId("...") }, { $pull: { tags: "deprecated" } })
db.articles.updateOne({ _id: ObjectId("...") }, { $addToSet: { tags: "reactive" } })
```

```java
Query query = Query.query(Criteria.where("id").is(articleId));
reactiveMongoTemplate.updateFirst(query, new Update().push("tags", "webflux"), Article.class);
reactiveMongoTemplate.updateFirst(query, new Update().pull("tags", "deprecated"), Article.class);
reactiveMongoTemplate.updateFirst(query, new Update().addToSet("tags", "reactive"), Article.class);
```

---

## B.7 Aggregation Pipeline 스테이지

| 스테이지 | 설명 |
|----------|------|
| `$match` | 조건 필터링 |
| `$group` | 그룹화 및 집계 |
| `$project` | 출력 필드 지정 |
| `$sort` | 정렬 |
| `$limit` | 결과 수 제한 |
| `$skip` | 도큐먼트 건너뛰기 |
| `$unwind` | 배열을 개별 도큐먼트로 분해 |
| `$lookup` | 다른 컬렉션과 조인 |

### $match / $group

```javascript
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: { _id: "$category", count: { $sum: 1 }, total: { $sum: "$amount" } } }
])
```

```java
Aggregation agg = Aggregation.newAggregation(
    Aggregation.match(Criteria.where("status").is("completed")),
    Aggregation.group("category").count().as("count").sum("amount").as("total")
);
reactiveMongoTemplate.aggregate(agg, "orders", Document.class);
```

### $project / $sort / $limit / $skip

```javascript
db.articles.aggregate([
  { $project: { title: 1, author: 1, _id: 0 } },
  { $sort: { createdAt: -1 } },
  { $skip: 20 },
  { $limit: 10 }
])
```

```java
Aggregation agg = Aggregation.newAggregation(
    Aggregation.project("title", "author").andExclude("_id"),
    Aggregation.sort(Sort.Direction.DESC, "createdAt"),
    Aggregation.skip(20),
    Aggregation.limit(10)
);
reactiveMongoTemplate.aggregate(agg, "articles", Article.class);
```

### $unwind

```javascript
// tags 배열을 분해하여 태그별 빈도 집계
db.articles.aggregate([
  { $unwind: "$tags" },
  { $group: { _id: "$tags", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

```java
Aggregation agg = Aggregation.newAggregation(
    Aggregation.unwind("tags"),
    Aggregation.group("tags").count().as("count"),
    Aggregation.sort(Sort.Direction.DESC, "count")
);
reactiveMongoTemplate.aggregate(agg, "articles", Document.class);
```

### $lookup

```javascript
db.orders.aggregate([
  { $lookup: { from: "products", localField: "productId",
               foreignField: "_id", as: "productDetails" } }
])
```

```java
Aggregation agg = Aggregation.newAggregation(
    Aggregation.lookup("products", "productId", "_id", "productDetails")
);
reactiveMongoTemplate.aggregate(agg, "orders", Document.class);
```

### 파이프라인 조합 예제

카테고리별 매출 상위 5개를 조회하는 실전 파이프라인이다.

```java
Aggregation agg = Aggregation.newAggregation(
    Aggregation.match(Criteria.where("status").is("completed")),
    Aggregation.group("category")
        .sum("amount").as("totalRevenue")
        .count().as("orderCount"),
    Aggregation.sort(Sort.Direction.DESC, "totalRevenue"),
    Aggregation.limit(5),
    Aggregation.project()
        .and("_id").as("category")
        .andInclude("totalRevenue", "orderCount")
        .andExclude("_id")
);
Flux<Document> results = reactiveMongoTemplate.aggregate(agg, "orders", Document.class);
```

---

## B.8 인덱스

| 인덱스 유형 | 설명 | 생성 예제 |
|-------------|------|----------|
| 단일 필드 | 하나의 필드에 대한 기본 인덱스 | `db.users.createIndex({ email: 1 })` |
| 복합 | 두 개 이상의 필드를 결합 | `db.orders.createIndex({ userId: 1, createdAt: -1 })` |
| 유니크 | 중복 값을 허용하지 않음 | `db.users.createIndex({ email: 1 }, { unique: true })` |
| 텍스트 | 전문 검색 지원 (컬렉션당 1개) | `db.articles.createIndex({ content: "text" })` |
| TTL | 일정 시간 후 도큐먼트 자동 삭제 | `db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 })` |

### 단일 필드 / 유니크 인덱스

```java
@Document(collection = "users")
public class User {
    @Indexed(unique = true)
    private String email;

    @Indexed(direction = IndexDirection.DESCENDING)
    private LocalDateTime createdAt;
}
// 프로그래밍 방식
reactiveMongoTemplate.indexOps("users")
    .ensureIndex(new Index().on("email", Sort.Direction.ASC).unique())
    .subscribe();
```

### 복합 인덱스

```java
@Document(collection = "orders")
@CompoundIndex(name = "user_date_idx", def = "{'userId': 1, 'createdAt': -1}")
public class Order {
    private String userId;
    private LocalDateTime createdAt;
}
```

### 텍스트 인덱스

```java
@Document(collection = "articles")
public class Article {
    @TextIndexed(weight = 10)
    private String title;
    @TextIndexed(weight = 5)
    private String content;
}
// 텍스트 검색 쿼리
TextCriteria textCriteria = TextCriteria.forDefaultLanguage().matching("reactive webflux");
Query query = TextQuery.queryText(textCriteria).sortByScore();
reactiveMongoTemplate.find(query, Article.class);
```

### TTL 인덱스

```java
@Document(collection = "sessions")
public class Session {
    @Indexed(expireAfterSeconds = 3600)
    private LocalDateTime createdAt;
}
// 프로그래밍 방식
reactiveMongoTemplate.indexOps("sessions")
    .ensureIndex(new Index().on("createdAt", Sort.Direction.ASC)
        .expire(3600, TimeUnit.SECONDS))
    .subscribe();
```

---

## B.9 자주 사용하는 패턴

### 페이징 처리

```java
Query query = Query.query(Criteria.where("status").is("active"))
    .with(Sort.by(Sort.Direction.DESC, "createdAt"))
    .skip(page * size).limit(size);
reactiveMongoTemplate.find(query, Article.class);
```

### Upsert (존재하면 수정, 없으면 삽입)

```java
Query query = Query.query(Criteria.where("userId").is(userId).and("date").is(today));
Update update = new Update()
    .set("lastAccess", LocalDateTime.now())
    .inc("visitCount", 1)
    .setOnInsert("createdAt", LocalDateTime.now());
reactiveMongoTemplate.upsert(query, update, UserActivity.class);
```

### 동적 쿼리 생성

```java
public Flux<Product> search(String keyword, Double minPrice,
                            Double maxPrice, List<String> categories) {
    List<Criteria> conditions = new ArrayList<>();
    if (keyword != null) conditions.add(Criteria.where("name").regex(keyword, "i"));
    if (minPrice != null) conditions.add(Criteria.where("price").gte(minPrice));
    if (maxPrice != null) conditions.add(Criteria.where("price").lte(maxPrice));
    if (categories != null && !categories.isEmpty())
        conditions.add(Criteria.where("category").in(categories));

    Criteria criteria = new Criteria();
    if (!conditions.isEmpty())
        criteria.andOperator(conditions.toArray(new Criteria[0]));

    return reactiveMongoTemplate.find(Query.query(criteria), Product.class);
}
```

---

> **참고**: MongoDB 연산자의 전체 목록은 [MongoDB 공식 문서](https://www.mongodb.com/docs/manual/reference/operator/)에서, Spring Data MongoDB의 Criteria API 상세 내용은 [Spring Data MongoDB 레퍼런스](https://docs.spring.io/spring-data/mongodb/reference/)에서 확인할 수 있다.
