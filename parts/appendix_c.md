# 부록 C. 자주 발생하는 문제와 해결 방법 (FAQ)

Spring WebFlux와 MongoDB 리액티브 스택으로 개발하다 보면 명령형 프로그래밍에서는 만나지 못했던 새로운 유형의 문제들을 마주하게 된다. 이 부록에서는 실무에서 빈번하게 발생하는 15가지 문제를 선별하여, 증상 파악부터 원인 분석, 해결 방법까지 체계적으로 정리한다.

---

## FAQ 1. "block()/blockFirst()/blockLast() are blocking" 에러

**증상**: 리액티브 파이프라인 내부에서 `block()`을 호출하면 `IllegalStateException`이 발생한다.

**원인 분석**: Netty의 이벤트 루프 스레드에서 `block()`을 호출하면 해당 스레드가 차단된다. 이벤트 루프가 멈추면 모든 요청 처리가 중단되므로, Reactor는 이를 감지하고 예외를 던진다.

**해결 방법**: `block()` 대신 `flatMap`, `zip`, `then` 등 리액티브 연산자로 체이닝한다.

```java
// 잘못된 코드
User user = userRepository.findById(userId).block(); // 예외 발생!

// 올바른 코드
return userRepository.findById(userId)
    .flatMap(user -> profileRepository.findByUser(user));
```

부득이하게 블로킹 코드를 호출해야 한다면 `Schedulers.boundedElastic()`으로 전환한다.

```java
Mono.fromCallable(() -> legacyBlockingService.call())
    .subscribeOn(Schedulers.boundedElastic());
```

---

## FAQ 2. "Scheduler was blocked" 에러와 BlockHound

**증상**: BlockHound 활성화 후 `BlockingOperationError: Blocking call!` 에러가 발생한다.

**원인 분석**: BlockHound는 논블로킹 스레드에서 발생하는 블로킹 호출(파일 I/O, `Thread.sleep` 등)을 런타임에 감지한다. 서드파티 라이브러리에 숨어 있는 블로킹 지점이 원인인 경우가 많다.

**해결 방법**: BlockHound를 테스트 의존성으로 추가하고, 허용 가능한 블로킹 호출은 화이트리스트에 등록한다.

```java
BlockHound.install(builder -> builder
    .allowBlockingCallsInside(
        "com.mongodb.internal.connection.DefaultServerMonitor", "run")
    .allowBlockingCallsInside(
        "io.netty.resolver.dns.DnsServerAddressStreamProviders",
        "unixResolverEnabled")
);
```

---

## FAQ 3. MongoDB 연결 실패 및 타임아웃 문제

**증상**: `MongoTimeoutException: Timed out after 30000 ms while waiting for a server`가 발생한다.

**원인 분석**: 커넥션 풀 크기 부족, 네트워크 지연, 레플리카 셋 구성 변경, DNS 해석 지연 등이 원인이다.

**해결 방법**: `MongoClientSettings`를 직접 구성하여 커넥션 풀과 타임아웃을 조정한다.

```java
@Override
protected void configureClientSettings(MongoClientSettings.Builder builder) {
    builder.applyToConnectionPoolSettings(pool -> pool
            .maxSize(50)
            .minSize(10)
            .maxWaitTime(5, TimeUnit.SECONDS)
            .maxConnectionIdleTime(30, TimeUnit.SECONDS))
        .applyToSocketSettings(socket -> socket
            .connectTimeout(5, TimeUnit.SECONDS)
            .readTimeout(10, TimeUnit.SECONDS))
        .applyToServerSettings(server -> server
            .heartbeatFrequency(10, TimeUnit.SECONDS));
}
```

---

## FAQ 4. ReactiveSecurityContext에서 인증 정보가 null인 경우

**증상**: `ReactiveSecurityContextHolder.getContext()`가 빈 `Mono`를 반환한다.

**원인 분석**: Spring Security 리액티브 구현은 `ThreadLocal`이 아닌 Reactor Context를 통해 `SecurityContext`를 전파한다. 파이프라인이 끊기면 Context가 전파되지 않아 인증 정보가 사라진다.

**해결 방법**: 리액티브 체인을 끊지 않고 유지하거나, 컨트롤러에서 파라미터로 전달한다.

```java
// 올바른 코드: 체인 유지
return ReactiveSecurityContextHolder.getContext()
    .map(ctx -> ctx.getAuthentication().getName())
    .map(name -> "prefix_" + name);

// 더 나은 방법: 컨트롤러 파라미터로 전달
@GetMapping("/me")
public Mono<UserDto> getMyInfo(@AuthenticationPrincipal Mono<UserDetails> principal) {
    return principal.flatMap(user -> userService.findByUsername(user.getUsername()));
}
```

---

## FAQ 5. WebFlux에서 @Transactional이 작동하지 않는 경우

**증상**: `@Transactional`을 선언했는데 MongoDB 작업이 트랜잭션으로 묶이지 않는다.

**원인 분석**: MongoDB 트랜잭션은 레플리카 셋(Replica Set) 구성이 필수다. 또한 `ReactiveMongoTransactionManager` 빈이 등록되어 있어야 한다.

**해결 방법**: 레플리카 셋을 구성하고 트랜잭션 매니저를 등록한다.

```bash
mongosh --eval "rs.initiate({_id:'rs0', members:[{_id:0, host:'localhost:27017'}]})"
```

```java
@Bean
ReactiveMongoTransactionManager transactionManager(ReactiveMongoDatabaseFactory factory) {
    return new ReactiveMongoTransactionManager(factory);
}
```

---

## FAQ 6. Flux 데이터가 중복으로 발행되는 경우 (Cold vs Hot)

**증상**: 하나의 `Flux`를 여러 곳에서 구독하면 DB 쿼리가 구독 횟수만큼 반복 실행된다.

**원인 분석**: Reactor의 `Flux`/`Mono`는 기본적으로 Cold Publisher다. 각 구독자에 대해 독립적으로 데이터 생성을 시작하므로 소스 작업이 중복 실행된다.

**해결 방법**: `cache()` 또는 `share()`로 Hot Publisher로 변환한다.

```java
Flux<Product> products = productRepository.findAll().cache(); // 결과 캐싱
```

| 연산자 | 동작 | 용도 |
|--------|------|------|
| `cache()` | 모든 데이터를 버퍼링, 새 구독자에게 재전송 | 변하지 않는 결과 조회 |
| `cache(Duration)` | TTL이 지나면 소스를 재구독 | 일정 시간 캐싱 |
| `share()` | 진행 중인 스트림을 공유, 이전 데이터 유실 | 실시간 이벤트 스트림 |

---

## FAQ 7. WebClient에서 DataBufferLimitException 발생

**증상**: 대용량 응답 수신 시 `Exceeded limit on max bytes to buffer : 262144` 에러가 발생한다.

**원인 분석**: WebClient는 기본적으로 응답 본문을 최대 256KB까지만 버퍼링한다.

**해결 방법**: 버퍼 크기를 조정하거나, 스트리밍으로 처리한다.

```java
// 방법 1: 버퍼 크기 확장
WebClient.builder()
    .codecs(c -> c.defaultCodecs().maxInMemorySize(10 * 1024 * 1024))
    .build();

// 방법 2: 스트리밍 처리 (권장)
webClient.get().uri("/api/products/export")
    .accept(MediaType.APPLICATION_NDJSON)
    .retrieve()
    .bodyToFlux(Product.class);
```

---

## FAQ 8. 리액티브 환경에서 ThreadLocal/MDC 사용 문제

**증상**: MDC에 설정한 `traceId`가 리액티브 파이프라인을 타면서 `null`로 나타난다.

**원인 분석**: MDC는 `ThreadLocal` 기반이므로, 하나의 요청이 여러 스레드를 오가는 리액티브 환경에서는 스레드 전환 시 MDC 값이 사라진다.

**해결 방법**: Micrometer Context Propagation을 활용하여 자동 동기화한다.

```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>context-propagation</artifactId>
</dependency>
```

```java
// 애플리케이션 시작 시 Hook 등록
Hooks.enableAutomaticContextPropagation();

// WebFilter에서 Reactor Context에 값 저장
@Override
public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
    String traceId = Optional.ofNullable(
            exchange.getRequest().getHeaders().getFirst("X-Trace-Id"))
        .orElse(UUID.randomUUID().toString().substring(0, 8));
    return chain.filter(exchange)
        .contextWrite(ctx -> ctx.put("traceId", traceId));
}
```

---

## FAQ 9. MongoDB Change Streams 연결 끊김 처리

**증상**: Change Streams 수신 중 MongoDB 장애나 네트워크 단절 시 스트림이 영구적으로 끊어진다.

**원인 분석**: 네트워크 단절이나 프라이머리 전환 시 롱 커넥션이 끊기며, 자동 재연결 로직이 없으면 이벤트 수신이 중단된다.

**해결 방법**: `retryWhen`과 Resume Token을 활용하여 끊긴 지점부터 재수신한다.

```java
private volatile BsonValue lastResumeToken;

public Flux<Order> watchOrders() {
    return createChangeStream()
        .doOnNext(event -> lastResumeToken =
            event.getRaw().getResumeToken().get("_data"))
        .map(ChangeStreamEvent::getBody)
        .retryWhen(Retry.backoff(Long.MAX_VALUE, Duration.ofSeconds(1))
            .maxBackoff(Duration.ofMinutes(1)));
}

private Flux<ChangeStreamEvent<Order>> createChangeStream() {
    var builder = ChangeStreamOptions.builder()
        .filter(Aggregation.newAggregation(
            Aggregation.match(Criteria.where("operationType")
                .in("insert", "update"))));
    if (lastResumeToken != null) {
        builder.resumeAfter(new BsonDocument("_data", lastResumeToken));
    }
    return mongoTemplate.changeStream("orders", builder.build(), Order.class);
}
```

---

## FAQ 10. 테스트에서 StepVerifier가 타임아웃되는 경우

**증상**: `StepVerifier` 테스트가 기본 타임아웃(10초) 이후 `AssertionError`로 실패한다.

**원인 분석**: 테스트 대상이 완료 신호(`onComplete`)를 발행하지 않으면 `StepVerifier`가 무한 대기한다. 빈 결과, 누락된 구독, 무한 스트림이 원인이다.

**해결 방법**: 상황에 맞는 검증 전략을 선택한다.

```java
// 빈 Mono: verifyComplete()
StepVerifier.create(userRepository.findById("nonexistent"))
    .verifyComplete();

// 무한 스트림: thenCancel()
StepVerifier.create(eventService.streamEvents())
    .expectNextCount(3)
    .thenCancel()
    .verify();

// 시간 지연: withVirtualTime()
StepVerifier.withVirtualTime(() ->
        Mono.error(new RuntimeException("fail"))
            .retryWhen(Retry.fixedDelay(3, Duration.ofSeconds(10))))
    .expectSubscription()
    .thenAwait(Duration.ofSeconds(30))
    .expectError()
    .verify();
```

---

## FAQ 11. Native Image 빌드 시 리플렉션 관련 에러

**증상**: GraalVM Native Image 빌드 후 런타임에 `ClassNotFoundException`이 발생한다.

**원인 분석**: Native Image는 빌드 시점에 정적 분석으로 클래스를 판별하므로, 리플렉션으로 접근하는 클래스가 바이너리에 포함되지 않을 수 있다.

**해결 방법**: Spring Boot 3.x의 AOT 기능을 활용하고, 커스텀 리플렉션은 힌트를 등록한다.

```java
@Configuration
@ImportRuntimeHints(MongoModelHints.class)
public class NativeConfig { }

public class MongoModelHints implements RuntimeHintsRegistrar {
    @Override
    public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
        hints.reflection()
            .registerType(User.class, MemberCategory.values())
            .registerType(Order.class, MemberCategory.values());
    }
}
```

---

## FAQ 12. CORS 관련 문제 해결

**증상**: 프론트엔드에서 API 호출 시 브라우저 콘솔에 CORS 에러가 표시된다.

**원인 분석**: 브라우저의 동일 출처 정책에 의해 다른 도메인/포트의 요청이 차단된다. Spring Security를 함께 쓸 경우 보안 필터에서도 CORS를 설정해야 한다.

**해결 방법**: WebFlux 설정과 Security 설정 양쪽에서 CORS를 구성한다.

```java
// WebFlux CORS 설정
@Override
public void addCorsMappings(CorsRegistry registry) {
    registry.addMapping("/api/**")
        .allowedOrigins("http://localhost:3000")
        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
        .allowCredentials(true).maxAge(3600);
}

// Security CORS 설정 (Security 사용 시 필수)
@Bean
SecurityWebFilterChain securityFilterChain(ServerHttpSecurity http) {
    return http
        .cors(cors -> cors.configurationSource(corsConfigurationSource()))
        .csrf(ServerHttpSecurity.CsrfSpec::disable)
        .build();
}
```

---

## FAQ 13. WebSocket 연결이 끊어지는 경우

**증상**: WebSocket 연결이 일정 시간 후 끊어지며 `onClose` 이벤트가 발생한다.

**원인 분석**: 프록시/로드밸런서의 유휴 타임아웃(Nginx 기본 60초)이 주요 원인이다.

**해결 방법**: 핑/퐁 메커니즘으로 연결을 유지한다.

```java
@Override
public Mono<Void> handle(WebSocketSession session) {
    Flux<WebSocketMessage> pingFlux = Flux.interval(Duration.ofSeconds(30))
        .map(tick -> session.pingMessage(factory ->
            factory.wrap(ByteBuffer.wrap("ping".getBytes()))));
    Flux<WebSocketMessage> messageFlux = session.receive()
        .filter(msg -> msg.getType() == WebSocketMessage.Type.TEXT)
        .flatMap(msg -> processMessage(msg, session));
    return session.send(pingFlux.mergeWith(messageFlux));
}
```

Nginx에서는 `proxy_read_timeout`을 충분히 늘려야 한다(예: `3600s`).

---

## FAQ 14. 메모리 누수 (구독 해제 미처리)

**증상**: 가동 시간이 길어질수록 힙 메모리가 지속 증가하며 `OutOfMemoryError`가 발생한다.

**원인 분석**: 무한 `Flux`(`interval`, SSE, WebSocket 등)를 구독한 후 해제하지 않으면, 구독 객체와 내부 버퍼가 GC 대상이 되지 않아 메모리가 누적된다.

**해결 방법**: `Disposable`을 관리하고 라이프사이클에 맞춰 해제한다.

```java
@Service
public class EventMonitorService implements DisposableBean {
    private final Disposable subscription;

    public EventMonitorService(EventPublisher publisher) {
        this.subscription = publisher.events()
            .subscribe(this::process, e -> log.error("처리 실패", e));
    }

    @Override
    public void destroy() {
        if (subscription != null && !subscription.isDisposed()) {
            subscription.dispose();
        }
    }
}
```

SSE 엔드포인트에서는 `doOnCancel()`로 클라이언트 연결 종료를 감지하여 리소스를 정리한다.

---

## FAQ 15. Reactor Context 전파 문제

**증상**: `contextWrite()`로 저장한 값을 `deferContextual()`로 읽으면 값이 존재하지 않는다.

**원인 분석**: Reactor Context는 구독자에서 발행자 방향(아래에서 위)으로 전파된다. `contextWrite()`가 체인의 상류에 위치하면 하류의 연산자가 해당 Context를 참조할 수 없다.

**해결 방법**: `contextWrite()`를 체인의 하류(구독자 쪽)에 배치한다.

```java
// 잘못된 코드: contextWrite가 상류에 위치
Mono.just("data")
    .contextWrite(ctx -> ctx.put("key", "value"))
    .flatMap(data -> Mono.deferContextual(ctx ->
        Mono.just(ctx.getOrDefault("key", "없음")))); // "없음" 반환

// 올바른 코드: contextWrite를 하류에 배치
Mono.just("data")
    .flatMap(data -> Mono.deferContextual(ctx ->
        Mono.just(ctx.get("key"))))  // "value" 정상 반환
    .contextWrite(ctx -> ctx.put("key", "value"));
```

여러 레이어에 걸쳐 Context를 전파하려면 `WebFilter`에서 설정하면 전체 파이프라인에서 접근 가능하다.

```java
@Override
public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
    String tenantId = exchange.getRequest().getHeaders().getFirst("X-Tenant-Id");
    return chain.filter(exchange)
        .contextWrite(ctx -> ctx.put("tenantId",
            tenantId != null ? tenantId : "default"));
}
```

---

## 정리

리액티브 프로그래밍에서 발생하는 대부분의 문제는 다음 세 가지 원칙을 이해하면 예방할 수 있다.

1. **체인을 끊지 마라**: 리액티브 파이프라인은 하나의 연속된 체인이어야 한다. `block()`, 새로운 구독, 중간 변수 할당 등으로 체인이 끊기면 Context 전파, 에러 처리, 백프레셔 등이 제대로 작동하지 않는다.

2. **스레드를 가정하지 마라**: 리액티브 코드는 어떤 스레드에서든 실행될 수 있다. `ThreadLocal`, `synchronized`, 가변 상태 등 특정 스레드에 의존하는 패턴은 피해야 한다.

3. **구독 생명주기를 관리하라**: 모든 구독은 반드시 완료되거나 명시적으로 해제되어야 한다. 무한 스트림을 구독할 때는 반드시 해제 로직을 함께 작성한다.

이 세 가지 원칙을 기억하며 개발한다면, 이 부록에서 다룬 문제 대부분을 사전에 방지할 수 있을 것이다.
