# Chapter 12. Server-Sent Events (SSE)

웹 애플리케이션에서 서버가 클라이언트에게 실시간으로 데이터를 전달해야 하는 상황은 매우 흔하다. 주식 시세, 알림, 라이브 피드, 대시보드 업데이트 등이 대표적인 사례다. 이번 장에서는 Server-Sent Events(SSE) 프로토콜의 개념과 Spring WebFlux에서 `Flux`를 활용한 SSE 엔드포인트 구현, Sinks 기반의 실시간 알림 시스템 구축, 그리고 MongoDB Change Streams와 SSE를 연동하여 데이터 변경 사항을 실시간으로 전달하는 방법까지 단계별로 다룬다.

---

## 12.1 SSE란 무엇인가?

### 12.1.1 SSE 프로토콜 개요

Server-Sent Events(SSE)는 서버에서 클라이언트로 단방향 실시간 데이터를 전송하기 위한 HTTP 기반 표준 프로토콜이다. W3C에 의해 HTML5 사양의 일부로 표준화되었으며, `EventSource` API를 통해 브라우저에서 기본적으로 지원한다.

SSE의 핵심 특징은 다음과 같다.

- **단방향 통신**: 서버에서 클라이언트로만 데이터를 전송한다. 클라이언트가 서버로 데이터를 보내려면 별도의 HTTP 요청을 사용한다.
- **HTTP 기반**: 일반 HTTP/1.1 또는 HTTP/2 위에서 동작하므로 별도의 프로토콜이 필요 없다.
- **자동 재연결**: 연결이 끊어지면 브라우저가 자동으로 재연결을 시도한다.
- **이벤트 ID 지원**: 마지막으로 수신한 이벤트 ID를 기억하여, 재연결 시 놓친 이벤트를 복구할 수 있다.
- **텍스트 기반**: `text/event-stream` MIME 타입을 사용하며, UTF-8 인코딩 텍스트로 데이터를 전송한다.

### 12.1.2 SSE 메시지 형식

SSE 메시지는 텍스트 줄로 구성되며, 각 필드는 콜론으로 구분된다.

```
id: 1
event: notification
data: {"message": "새 댓글이 등록되었습니다.", "postId": "abc123"}
retry: 5000

```

각 필드의 의미는 다음과 같다.

| 필드 | 설명 | 기본값 |
|------|------|--------|
| `id` | 이벤트 고유 식별자. 재연결 시 `Last-Event-ID` 헤더로 전송됨 | 없음 |
| `event` | 이벤트 타입. 클라이언트에서 `addEventListener`로 특정 타입만 수신 가능 | `message` |
| `data` | 실제 전송 데이터. 여러 줄 가능 (각 줄마다 `data:` 접두사 필요) | 없음 |
| `retry` | 재연결 대기 시간(밀리초). 서버가 클라이언트의 재연결 간격을 제어 | 브라우저 기본값 |
| `:` (주석) | 콜론으로 시작하는 줄은 주석으로 처리됨. 연결 유지(keep-alive)에 활용 | - |

메시지와 메시지 사이는 빈 줄(`\n\n`)로 구분한다.

### 12.1.3 SSE vs WebSocket vs 폴링 비교

| 구분 | SSE | WebSocket | 폴링 (Polling) |
|------|-----|-----------|----------------|
| **통신 방향** | 단방향 (서버 -> 클라이언트) | 양방향 | 단방향 (클라이언트 요청 기반) |
| **프로토콜** | HTTP | WS (WebSocket 프로토콜) | HTTP |
| **연결 유지** | 지속 연결 | 지속 연결 | 매 요청마다 연결/해제 |
| **자동 재연결** | 브라우저 기본 지원 | 직접 구현 필요 | 해당 없음 |
| **데이터 형식** | 텍스트 (UTF-8) | 텍스트 + 바이너리 | 제한 없음 |
| **방화벽/프록시** | HTTP이므로 통과 용이 | 차단될 수 있음 | 문제 없음 |
| **HTTP/2 호환** | 멀티플렉싱 활용 가능 | 별도 연결 필요 | 해당 없음 |
| **서버 부하** | 낮음 | 낮음 | 높음 (반복 요청) |

SSE가 적합한 시나리오는 알림, 뉴스 피드, 주식 시세, 진행률 업데이트 등 **서버에서 클라이언트로의 단방향 스트리밍**이다. 기존 HTTP 인프라(로드밸런서, 프록시, 인증)를 그대로 활용할 수 있고, 브라우저가 자동으로 재연결을 처리하므로 구현이 간단하다. 반면, 양방향 실시간 통신(채팅, 게임)이나 바이너리 데이터 전송이 필요한 경우에는 WebSocket이 더 적합하다.

### 12.1.4 클라이언트 측 EventSource API

브라우저에서 SSE를 수신하는 JavaScript 코드는 매우 간결하다.

```javascript
const eventSource = new EventSource('/api/notifications/stream');

// 기본 message 이벤트 수신
eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('수신:', data);
};

// 특정 이벤트 타입 수신
eventSource.addEventListener('notification', (event) => {
    const notification = JSON.parse(event.data);
    showNotification(notification);
});

// 에러 처리 및 연결 종료
eventSource.onerror = (error) => {
    console.error('SSE 연결 오류:', error);
    if (eventSource.readyState === EventSource.CLOSED) {
        console.log('연결이 종료되었습니다.');
    }
};
```

`EventSource`는 연결이 끊어지면 자동으로 재연결을 시도한다. `readyState`는 `CONNECTING(0)`, `OPEN(1)`, `CLOSED(2)` 세 가지 상태를 가진다.

---

## 12.2 Flux를 활용한 SSE 엔드포인트 구현

### 12.2.1 TEXT_EVENT_STREAM 미디어 타입

SSE는 Spring WebFlux에 기본 내장되어 있으므로 추가 의존성이 필요 없다. SSE 엔드포인트를 만드는 가장 간단한 방법은 컨트롤러 메서드에서 `Flux`를 반환하면서 `produces`에 `text/event-stream` 미디어 타입을 지정하는 것이다.

```java
@RestController
@RequestMapping("/api/sse")
public class SseController {

    @GetMapping(value = "/time", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> streamTime() {
        return Flux.interval(Duration.ofSeconds(1))
            .map(sequence -> "현재 시각: " + LocalDateTime.now()
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
    }
}
```

`MediaType.TEXT_EVENT_STREAM_VALUE`는 `"text/event-stream"` 문자열 상수다. 이 설정만으로 Spring WebFlux는 `Flux`의 각 요소를 SSE 메시지 형식(`data:` 필드)으로 변환하여 클라이언트에 전송한다.

### 12.2.2 ServerSentEvent 클래스 활용

단순 `data` 필드만이 아니라 `id`, `event`, `retry` 등 SSE 메시지의 모든 필드를 제어하려면 `ServerSentEvent<T>` 제네릭 클래스를 사용한다.

```java
@GetMapping(value = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<String>> streamEvents() {
    return Flux.interval(Duration.ofSeconds(2))
        .map(sequence -> ServerSentEvent.<String>builder()
            .id(String.valueOf(sequence))
            .event("heartbeat")
            .data("서버 상태: 정상 (seq=" + sequence + ")")
            .retry(Duration.ofSeconds(10))
            .comment("keep-alive")
            .build());
}
```

`ServerSentEvent`를 반환 타입으로 사용하면 `produces` 속성을 생략해도 된다. Spring WebFlux가 반환 타입을 보고 자동으로 `text/event-stream`으로 설정한다.

```java
// produces 생략 가능 - ServerSentEvent 반환 시 자동 적용
@GetMapping("/events-auto")
public Flux<ServerSentEvent<Map<String, Object>>> streamEventsAuto() {
    return Flux.interval(Duration.ofSeconds(3))
        .map(seq -> ServerSentEvent.<Map<String, Object>>builder()
            .id(String.valueOf(seq))
            .event("status-update")
            .data(Map.of("sequence", seq, "timestamp", Instant.now().toString()))
            .build());
}
```

### 12.2.3 Flux.interval을 활용한 주기적 데이터 전송

`Flux.interval()`은 지정된 간격으로 0부터 시작하는 `Long` 값을 방출하는 Hot Publisher다. 주기적으로 데이터를 전송하는 SSE 엔드포인트에 적합하다.

```java
@RestController
@RequestMapping("/api/sse")
@RequiredArgsConstructor
public class DashboardSseController {

    private final SystemMetricsService metricsService;

    @GetMapping(value = "/dashboard", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<DashboardData>> streamDashboard() {
        return Flux.interval(Duration.ofSeconds(5))
            .flatMap(tick -> metricsService.collectMetrics())
            .map(metrics -> ServerSentEvent.<DashboardData>builder()
                .event("dashboard-update")
                .data(metrics)
                .build())
            .doOnCancel(() -> log.info("대시보드 SSE 연결 해제"));
    }
}
```

```java
@Data
@Builder
public class DashboardData {
    private double cpuUsage;
    private long memoryUsed;
    private long memoryTotal;
    private int activeThreads;
    private Instant timestamp;
}
```

### 12.2.4 이벤트 타입 혼합과 Flux.merge

서로 다른 이벤트 타입을 하나의 SSE 스트림에 혼합하여 전송할 수 있다. `Flux.merge`로 여러 스트림을 결합하고, 클라이언트는 `addEventListener`로 관심 있는 이벤트만 선택적으로 수신한다.

```java
@GetMapping(value = "/mixed", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<?>> streamMixedEvents() {
    Flux<ServerSentEvent<?>> statusStream = Flux.interval(Duration.ofSeconds(5))
        .map(tick -> ServerSentEvent.builder()
            .event("system-status")
            .data(Map.of("status", "healthy", "uptime", tick * 5))
            .build());

    Flux<ServerSentEvent<?>> statsStream = Flux.interval(Duration.ofSeconds(10))
        .map(tick -> ServerSentEvent.builder()
            .event("statistics")
            .data(Map.of("activeUsers", 42 + tick, "requestsPerSec", 150))
            .build());

    // 30초마다 주석 기반 하트비트 전송 (연결 유지용)
    Flux<ServerSentEvent<?>> heartbeat = Flux.interval(Duration.ofSeconds(30))
        .map(tick -> ServerSentEvent.builder().comment("heartbeat").build());

    return Flux.merge(statusStream, statsStream, heartbeat);
}
```

### 12.2.5 함수형 라우터에서 SSE 구현

Router Functions 스타일로도 SSE 엔드포인트를 구현할 수 있다.

```java
@Configuration
public class SseRouterConfig {

    @Bean
    public RouterFunction<ServerResponse> sseRoutes(SseHandler handler) {
        return RouterFunctions.route()
            .GET("/api/sse/stream", handler::stream)
            .build();
    }
}

@Component
public class SseHandler {

    public Mono<ServerResponse> stream(ServerRequest request) {
        Flux<ServerSentEvent<String>> events = Flux.interval(Duration.ofSeconds(1))
            .map(seq -> ServerSentEvent.<String>builder()
                .id(String.valueOf(seq))
                .data("tick " + seq)
                .build());

        return ServerResponse.ok()
            .contentType(MediaType.TEXT_EVENT_STREAM)
            .body(events, ServerSentEvent.class);
    }
}
```

---

## 12.3 실시간 알림 시스템 구축

### 12.3.1 Sinks를 활용한 이벤트 브로드캐스팅

실제 서비스에서 SSE는 단순 타이머가 아니라 특정 이벤트 발생 시 연결된 클라이언트들에게 즉시 데이터를 전달해야 한다. Reactor의 `Sinks`는 프로그래밍 방식으로 이벤트를 발행할 수 있는 Hot Publisher로, 이 용도에 적합하다.

```java
@Service
@Slf4j
public class NotificationBroadcaster {

    private final Sinks.Many<Notification> sink =
        Sinks.many().multicast().onBackpressureBuffer(256);

    public void publish(Notification notification) {
        Sinks.EmitResult result = sink.tryEmitNext(notification);
        if (result.isFailure()) {
            log.warn("알림 발행 실패: {}, result={}", notification.getId(), result);
        }
    }

    public Flux<Notification> subscribe() {
        return sink.asFlux();
    }
}
```

Sinks의 주요 팩토리 메서드를 비교하면 다음과 같다.

| 메서드 | 설명 | 사용 시나리오 |
|--------|------|--------------|
| `Sinks.many().multicast()` | 여러 구독자에게 동일 이벤트를 전달. 구독 전 발행된 이벤트는 수신 불가 | 실시간 알림, 라이브 피드 |
| `Sinks.many().replay()` | 과거 이벤트를 새 구독자에게 재전송 가능 | 최근 N건의 이벤트 보여주기 |
| `Sinks.many().unicast()` | 단일 구독자만 허용 | 1:1 전용 스트림 |

### 12.3.2 알림 도메인 모델

```java
@Document(collection = "notifications")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Notification {
    @Id
    private String id;
    private String userId;       // 수신 대상 사용자
    private String type;         // COMMENT, LIKE, FOLLOW, SYSTEM 등
    private String title;
    private String message;
    private Map<String, Object> metadata;  // 추가 정보 (postId, commentId 등)
    private boolean read;
    private LocalDateTime createdAt;
}
```

```java
public interface NotificationRepository
        extends ReactiveMongoRepository<Notification, String> {
    Flux<Notification> findByUserIdOrderByCreatedAtDesc(String userId);
    Flux<Notification> findByUserIdAndReadFalse(String userId);
    Mono<Long> countByUserIdAndReadFalse(String userId);
}
```

### 12.3.3 사용자별 알림 구독 관리

실제 서비스에서는 모든 알림을 모든 사용자에게 브로드캐스팅하지 않는다. 사용자별로 구독을 관리하고, 해당 사용자에게만 알림을 전달해야 한다.

```java
@Service
@Slf4j
public class NotificationService {

    private final NotificationRepository notificationRepository;
    private final ConcurrentHashMap<String, Sinks.Many<Notification>> userSinks =
        new ConcurrentHashMap<>();

    public NotificationService(NotificationRepository notificationRepository) {
        this.notificationRepository = notificationRepository;
    }

    /**
     * 사용자별 알림 스트림을 구독한다.
     */
    public Flux<ServerSentEvent<Notification>> subscribe(String userId) {
        Sinks.Many<Notification> userSink = userSinks.computeIfAbsent(userId,
            key -> {
                log.info("사용자 {} 알림 구독 생성", key);
                return Sinks.many().multicast().onBackpressureBuffer(128);
            });

        return userSink.asFlux()
            .map(notification -> ServerSentEvent.<Notification>builder()
                .id(notification.getId())
                .event(notification.getType())
                .data(notification)
                .build());
    }

    /**
     * 특정 사용자에게 알림을 전송한다.
     * MongoDB에 저장하고, 접속 중이면 SSE로 실시간 전달한다.
     */
    public Mono<Notification> sendNotification(Notification notification) {
        notification.setCreatedAt(LocalDateTime.now());
        notification.setRead(false);

        return notificationRepository.save(notification)
            .doOnSuccess(saved -> {
                Sinks.Many<Notification> userSink =
                    userSinks.get(saved.getUserId());
                if (userSink != null) {
                    Sinks.EmitResult result = userSink.tryEmitNext(saved);
                    if (result.isFailure()) {
                        log.warn("사용자 {} 알림 전송 실패: {}",
                            saved.getUserId(), result);
                    }
                } else {
                    log.debug("사용자 {} 미접속 상태, 알림은 DB에만 저장됨",
                        saved.getUserId());
                }
            });
    }

    public Mono<Long> getUnreadCount(String userId) {
        return notificationRepository.countByUserIdAndReadFalse(userId);
    }

    public Mono<Notification> markAsRead(String notificationId) {
        return notificationRepository.findById(notificationId)
            .map(notification -> {
                notification.setRead(true);
                return notification;
            })
            .flatMap(notificationRepository::save);
    }

    /**
     * 사용자의 SSE 연결이 해제될 때 호출된다.
     */
    public void removeSubscription(String userId) {
        Sinks.Many<Notification> removed = userSinks.remove(userId);
        if (removed != null) {
            removed.tryEmitComplete();
            log.info("사용자 {} 알림 구독 해제", userId);
        }
    }
}
```

### 12.3.4 알림 SSE 컨트롤러

```java
@RestController
@RequestMapping("/api/notifications")
@RequiredArgsConstructor
@Slf4j
public class NotificationController {

    private final NotificationService notificationService;

    @GetMapping(value = "/stream/{userId}",
                produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<Notification>> streamNotifications(
            @PathVariable String userId) {

        log.info("SSE 연결: userId={}", userId);

        // 실시간 알림 스트림
        Flux<ServerSentEvent<Notification>> notificationStream =
            notificationService.subscribe(userId);

        // 30초마다 하트비트 전송 (프록시/로드밸런서 타임아웃 방지)
        Flux<ServerSentEvent<Notification>> heartbeat =
            Flux.interval(Duration.ofSeconds(30))
                .map(tick -> ServerSentEvent.<Notification>builder()
                    .comment("heartbeat")
                    .build());

        return Flux.merge(notificationStream, heartbeat)
            .doOnCancel(() -> {
                log.info("SSE 연결 해제: userId={}", userId);
                notificationService.removeSubscription(userId);
            });
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<Notification> sendNotification(
            @RequestBody Notification notification) {
        return notificationService.sendNotification(notification);
    }

    @PatchMapping("/{notificationId}/read")
    public Mono<Notification> markAsRead(
            @PathVariable String notificationId) {
        return notificationService.markAsRead(notificationId);
    }
}
```

### 12.3.5 연결 해제 처리와 리소스 정리

SSE 연결이 종료되는 경우는 다음과 같다.

1. **클라이언트가 연결을 닫는 경우**: `EventSource.close()` 호출 또는 브라우저 탭 닫기
2. **서버에서 스트림을 완료하는 경우**: `Flux`가 `onComplete` 또는 `onError` 신호를 발생
3. **네트워크 문제**: 연결이 예기치 않게 끊어지는 경우
4. **프록시/로드밸런서 타임아웃**: 일정 시간 동안 데이터가 전송되지 않으면 연결이 종료

각 상황에 대한 처리는 `doFinally`를 활용한다. `doFinally`는 `onComplete`, `onError`, `cancel` 모든 종료 신호에 대해 실행되므로, 리소스 정리에 가장 적합하다.

```java
@GetMapping(value = "/stream/{userId}",
            produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<Notification>> streamWithCleanup(
        @PathVariable String userId) {

    return notificationService.subscribe(userId)
        .timeout(Duration.ofHours(1))
        .onErrorResume(TimeoutException.class, e -> {
            log.info("SSE 타임아웃: userId={}", userId);
            return Flux.empty();
        })
        .doFinally(signalType -> {
            log.info("SSE 스트림 종료: userId={}, signal={}", userId, signalType);
            notificationService.removeSubscription(userId);
        });
}
```

### 12.3.6 알림 발행 연동 예제

게시글에 댓글이 달릴 때 알림을 전송하는 시나리오를 구현한다.

```java
@Service
@RequiredArgsConstructor
public class CommentService {

    private final CommentRepository commentRepository;
    private final PostRepository postRepository;
    private final NotificationService notificationService;

    public Mono<Comment> addComment(String postId, CommentRequest request) {
        Comment comment = Comment.builder()
            .postId(postId)
            .authorId(request.getAuthorId())
            .authorName(request.getAuthorName())
            .content(request.getContent())
            .createdAt(LocalDateTime.now())
            .build();

        return commentRepository.save(comment)
            .flatMap(saved -> postRepository.findById(postId)
                .flatMap(post -> {
                    if (!post.getAuthorId().equals(request.getAuthorId())) {
                        Notification notification = Notification.builder()
                            .userId(post.getAuthorId())
                            .type("COMMENT")
                            .title("새 댓글")
                            .message(request.getAuthorName() + "님이 '"
                                + post.getTitle() + "'에 댓글을 남겼습니다.")
                            .metadata(Map.of(
                                "postId", postId,
                                "commentId", saved.getId()))
                            .build();
                        return notificationService.sendNotification(notification)
                            .thenReturn(saved);
                    }
                    return Mono.just(saved);
                }));
    }
}
```

11장에서 다룬 JWT 인증과 연동하면, `ReactiveSecurityContextHolder`에서 현재 사용자를 꺼내어 인증된 사용자 전용 SSE 구독을 구현할 수도 있다.

```java
@GetMapping(value = "/stream/me",
            produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<Notification>> streamMyNotifications() {
    return ReactiveSecurityContextHolder.getContext()
        .map(ctx -> ctx.getAuthentication().getName())
        .flatMapMany(username -> notificationService.subscribe(username)
            .doFinally(signal ->
                notificationService.removeSubscription(username)));
}
```

---

## 12.4 MongoDB Change Streams + SSE 연동

### 12.4.1 Change Streams 개요

MongoDB Change Streams는 컬렉션, 데이터베이스, 또는 전체 클러스터의 데이터 변경 사항을 실시간으로 감시하는 기능이다. 8장에서 기본 개념을 다루었으며, 이번 절에서는 이를 SSE와 연동하여 데이터 변경 사항을 클라이언트에 실시간으로 전달하는 방법에 초점을 맞춘다.

- **이벤트 타입**: `insert`, `update`, `replace`, `delete`, `invalidate`
- **Resume Token**: 연결이 끊어진 지점부터 이벤트를 다시 수신할 수 있다
- **필터링**: Aggregation Pipeline을 사용하여 관심 있는 변경만 수신 가능
- **요구사항**: Replica Set 또는 Sharded Cluster 환경에서만 동작한다

### 12.4.2 ReactiveMongoTemplate의 changeStream()

Spring Data MongoDB의 `ReactiveMongoTemplate`은 `changeStream()` 메서드를 통해 Change Streams를 `Flux`로 변환한다.

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class ProductChangeStreamService {

    private final ReactiveMongoTemplate mongoTemplate;

    public Flux<ChangeStreamEvent<Product>> watchProducts() {
        return mongoTemplate.changeStream("products",
                ChangeStreamOptions.builder()
                    .filter(Aggregation.newAggregation(
                        Aggregation.match(Criteria.where("operationType")
                            .in("insert", "update", "replace"))))
                    .build(),
                Product.class)
            .doOnNext(event -> log.info("변경 감지: type={}, id={}",
                event.getOperationType(), event.getBody()));
    }

    public Flux<ChangeStreamEvent<Product>> watchProductsByCategory(
            String category) {
        return mongoTemplate.changeStream("products",
                ChangeStreamOptions.builder()
                    .filter(Aggregation.newAggregation(
                        Aggregation.match(Criteria.where("operationType")
                            .in("insert", "update", "replace")
                            .and("fullDocument.category").is(category))))
                    .build(),
                Product.class);
    }
}
```

### 12.4.3 Change Streams를 SSE로 전달

Change Streams에서 수신한 이벤트를 SSE를 통해 클라이언트에 전달하는 컨트롤러를 구현한다.

```java
@Data
@Builder
public class ProductChangeEvent {
    private String operationType;
    private Product product;
    private Instant timestamp;
}
```

```java
@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
@Slf4j
public class ProductSseController {

    private final ProductChangeStreamService changeStreamService;

    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<ProductChangeEvent>> streamProductChanges() {

        Flux<ServerSentEvent<ProductChangeEvent>> changeStream =
            changeStreamService.watchProducts()
                .map(event -> {
                    ProductChangeEvent payload = ProductChangeEvent.builder()
                        .operationType(event.getOperationType().getValue())
                        .product(event.getBody())
                        .timestamp(Instant.now())
                        .build();

                    return ServerSentEvent.<ProductChangeEvent>builder()
                        .id(event.getResumeToken() != null
                            ? event.getResumeToken().toJson() : null)
                        .event("product-" + event.getOperationType().getValue())
                        .data(payload)
                        .build();
                });

        Flux<ServerSentEvent<ProductChangeEvent>> heartbeat =
            Flux.interval(Duration.ofSeconds(30))
                .map(tick -> ServerSentEvent.<ProductChangeEvent>builder()
                    .comment("heartbeat")
                    .build());

        return Flux.merge(changeStream, heartbeat)
            .doOnCancel(() -> log.info("상품 변경 SSE 연결 해제"));
    }
}
```

### 12.4.4 Resume Token을 활용한 이벤트 복구

클라이언트가 재연결할 때 놓친 이벤트를 복구하려면 Resume Token을 활용한다. SSE의 `id` 필드에 Resume Token을 설정하면, 브라우저가 재연결 시 `Last-Event-ID` 헤더로 자동 전송한다.

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class ResumableChangeStreamService {

    private final ReactiveMongoTemplate mongoTemplate;

    public Flux<ChangeStreamEvent<Product>> watchProducts(String resumeToken) {
        ChangeStreamOptions.ChangeStreamOptionsBuilder optionsBuilder =
            ChangeStreamOptions.builder()
                .filter(Aggregation.newAggregation(
                    Aggregation.match(Criteria.where("operationType")
                        .in("insert", "update", "replace"))));

        if (resumeToken != null && !resumeToken.isEmpty()) {
            try {
                BsonDocument token = BsonDocument.parse(resumeToken);
                optionsBuilder.resumeAfter(token);
                log.info("Resume Token으로 변경 스트림 재개");
            } catch (Exception e) {
                log.warn("유효하지 않은 Resume Token, 처음부터 시작");
            }
        }

        return mongoTemplate.changeStream("products",
            optionsBuilder.build(), Product.class);
    }
}
```

```java
@GetMapping(value = "/stream/resumable",
            produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<ProductChangeEvent>> streamResumable(
        @RequestHeader(value = "Last-Event-ID", required = false)
        String lastEventId) {

    return resumableChangeStreamService.watchProducts(lastEventId)
        .map(event -> {
            String tokenJson = event.getResumeToken() != null
                ? event.getResumeToken().toJson() : null;

            ProductChangeEvent payload = ProductChangeEvent.builder()
                .operationType(event.getOperationType().getValue())
                .product(event.getBody())
                .timestamp(Instant.now())
                .build();

            return ServerSentEvent.<ProductChangeEvent>builder()
                .id(tokenJson)
                .event("product-change")
                .data(payload)
                .build();
        });
}
```

클라이언트에서는 별도 처리 없이 `EventSource`가 재연결 시 `Last-Event-ID`를 자동 전송한다.

```javascript
const es = new EventSource('/api/products/stream/resumable');
es.addEventListener('product-change', (e) => {
    console.log('이벤트 ID:', e.lastEventId);
    const change = JSON.parse(e.data);
    applyChange(change);
});
```

### 12.4.5 실시간 데이터 동기화 패턴

Change Streams + SSE를 조합하면 여러 클라이언트 간의 실시간 데이터 동기화를 구현할 수 있다. 한 사용자가 데이터를 수정하면, 같은 화면을 보고 있는 다른 사용자에게 즉시 변경 사항이 반영되는 구조다. 구현의 핵심은 다음과 같다.

1. **`@PostConstruct`에서 Change Stream 시작**: 애플리케이션 기동 시 감시할 컬렉션에 대해 Change Stream을 구독한다.
2. **세션별 Sink 관리**: `ConcurrentHashMap<String, Sinks.Many<ChangeEvent>>`로 세션마다 독립적인 Sink를 생성한다.
3. **이벤트 분배**: Change Stream에서 수신한 이벤트를 해당 컬렉션을 구독 중인 모든 세션의 Sink에 `tryEmitNext`로 전달한다.
4. **SSE 엔드포인트**: `GET /api/sync/stream/{collection}?sessionId=xxx` 형태로 클라이언트가 특정 컬렉션의 변경 사항을 구독한다.

이 패턴은 12.3절의 사용자별 알림 구독과 동일한 `ConcurrentHashMap` + `Sinks` 구조를 컬렉션 단위로 확장한 것이다.

### 12.4.6 프로덕션 환경 고려사항

SSE를 프로덕션 환경에서 운영할 때 반드시 고려해야 할 사항들을 정리한다.

**1. 연결 수 관리**

SSE는 HTTP 연결을 지속적으로 유지하므로, 동시 연결 수가 많아지면 서버 리소스가 소진될 수 있다. `AtomicInteger`로 활성 연결 수를 추적하고 최대치를 제한하는 것이 좋다.

**2. 프록시/로드밸런서 설정**

Nginx 등의 리버스 프록시를 사용할 경우, SSE 연결이 조기에 종료되지 않도록 버퍼링을 비활성화하고 타임아웃을 늘려야 한다.

```nginx
location /api/sse/ {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Connection '';
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 86400s;
    chunked_transfer_encoding off;
}
```

**3. 하트비트**

프록시의 유휴 타임아웃을 방지하기 위해 주기적으로 하트비트를 전송한다. SSE의 주석(`:` 접두사)을 사용하면 클라이언트 측 이벤트 핸들러가 트리거되지 않는다.

**4. 에러 복구 전략**

Change Stream이 중단되었을 때 자동으로 재시작하는 전략이 필요하다. `retryWhen`에 지수 백오프를 적용하면 일시적 장애에서 안정적으로 복구할 수 있다.

```java
private void watchCollectionWithRetry(String collectionName) {
    mongoTemplate.changeStream(collectionName,
            ChangeStreamOptions.empty(), Document.class)
        .doOnError(e -> log.error("{} Change Stream 오류", collectionName, e))
        .retryWhen(Retry.backoff(Long.MAX_VALUE, Duration.ofSeconds(1))
            .maxBackoff(Duration.ofMinutes(1))
            .doBeforeRetry(signal -> log.warn("{} Change Stream 재시도 #{}",
                collectionName, signal.totalRetries())))
        .subscribe(this::processChangeEvent);
}
```

---

## 요약

이번 장에서 다룬 핵심 내용을 정리한다.

| 주제 | 핵심 내용 |
|------|----------|
| **SSE 프로토콜** | 서버에서 클라이언트로의 단방향 HTTP 기반 실시간 스트리밍, 자동 재연결, 이벤트 ID 지원 |
| **SSE vs WebSocket** | SSE는 단방향/HTTP 기반으로 인프라 호환성이 높고, WebSocket은 양방향/바이너리 지원 |
| **Flux + SSE** | `TEXT_EVENT_STREAM` 미디어 타입과 `ServerSentEvent<T>` 클래스로 SSE 엔드포인트 구현 |
| **Sinks 브로드캐스팅** | `Sinks.many().multicast()`로 이벤트를 발행하고 여러 SSE 구독자에게 실시간 전달 |
| **사용자별 알림** | `ConcurrentHashMap`으로 사용자별 Sink를 관리하여 개인화된 알림 스트림 구현 |
| **연결 해제 처리** | `doOnCancel`, `doFinally`로 SSE 연결 종료 시 리소스 정리 |
| **Change Streams + SSE** | MongoDB 데이터 변경을 감지하여 SSE로 실시간 전달, Resume Token으로 이벤트 복구 |
| **실시간 데이터 동기화** | Change Streams + Sinks + SSE를 조합하여 여러 클라이언트 간 데이터 동기화 |

다음 장에서는 WebSocket을 활용한 양방향 실시간 통신과 채팅 애플리케이션 구현을 다룬다.


---

# Chapter 13. WebSocket

실시간 양방향 통신이 필요한 채팅, 게임, 실시간 대시보드 등의 애플리케이션에서는 HTTP의 요청-응답 모델만으로는 한계가 있다. WebSocket은 클라이언트와 서버 간에 지속적인 양방향 통신 채널을 제공하며, Spring WebFlux는 리액티브 스트림 기반의 WebSocket 지원을 내장하고 있다. 이번 장에서는 WebSocket 프로토콜의 동작 원리를 이해하고, WebFlux에서 WebSocket 핸들러를 구현하며, 실시간 채팅 애플리케이션을 구축하고, 세션 관리 전략까지 단계별로 다룬다.

---

## 13.1 WebSocket 프로토콜 이해

### 13.1.1 WebSocket이란?

WebSocket은 RFC 6455로 표준화된 통신 프로토콜로, 단일 TCP 연결 위에서 클라이언트와 서버 간 **전이중(Full-Duplex) 양방향 통신**을 가능하게 한다. 기존 HTTP는 클라이언트가 요청을 보내야만 서버가 응답하는 반이중 구조인 반면, WebSocket은 연결 수립 후 양쪽 모두 자유롭게 메시지를 주고받을 수 있다.

| 특징 | 설명 |
|------|------|
| **양방향 통신** | 클라이언트와 서버 모두 독립적으로 메시지를 전송할 수 있다 |
| **지속 연결** | 한 번 연결이 수립되면 명시적으로 종료할 때까지 유지된다 |
| **낮은 오버헤드** | HTTP 헤더 없이 최소 2바이트의 프레임 헤더로 메시지를 교환한다 |
| **실시간성** | 폴링 없이 서버에서 즉시 클라이언트로 데이터를 전송할 수 있다 |

### 13.1.2 HTTP 핸드셰이크

WebSocket 연결은 HTTP Upgrade 핸드셰이크로 시작된다.

**클라이언트 요청:**

```
GET /ws/chat HTTP/1.1
Host: localhost:8080
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

**서버 응답:**

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

핸드셰이크 과정은 다음과 같다.

1. 클라이언트가 `Upgrade: websocket` 헤더를 포함한 HTTP GET 요청을 전송한다.
2. 서버는 `Sec-WebSocket-Key`에 매직 GUID(`258EAFA5-E914-47DA-95CA-C5AB0DC85B11`)를 연결하여 SHA-1 해시를 생성하고 `Sec-WebSocket-Accept`에 포함한다.
3. 서버가 `101 Switching Protocols`를 반환하면 TCP 연결은 유지된 채 프로토콜이 WebSocket으로 전환된다.
4. 이후부터 양쪽 모두 WebSocket 프레임으로 메시지를 교환한다.

### 13.1.3 프레임 구조

핸드셰이크 완료 후 데이터는 프레임(Frame) 단위로 교환된다. 주요 Opcode는 다음과 같다.

| Opcode | 의미 |
|--------|------|
| `0x1` | 텍스트 프레임 (UTF-8) |
| `0x2` | 바이너리 프레임 |
| `0x8` | 연결 종료 (Close) |
| `0x9` | Ping |
| `0xA` | Pong |

각 프레임은 FIN 비트(마지막 프레임 여부), Opcode(프레임 유형), MASK 비트(클라이언트->서버는 반드시 마스킹), Payload 길이, 실제 데이터로 구성된다. 텍스트 프레임은 채팅 메시지 같은 문자열 데이터에, 바이너리 프레임은 이미지나 파일 전송에 사용한다.

### 13.1.4 WebSocket vs SSE vs Long Polling 비교

| 특성 | WebSocket | SSE | Long Polling |
|------|-----------|-----|--------------|
| **통신 방향** | 양방향 (Full-Duplex) | 단방향 (서버->클라이언트) | 단방향 |
| **프로토콜** | ws:// / wss:// | HTTP | HTTP |
| **오버헤드** | 매우 낮음 (2-14바이트) | 낮음 | 높음 (매번 HTTP 헤더) |
| **자동 재연결** | 직접 구현 필요 | EventSource 자동 지원 | 직접 구현 필요 |
| **바이너리 전송** | 지원 | 미지원 | 미지원 |

Chapter 12에서 다룬 SSE는 단방향 스트리밍에 적합하지만, 채팅처럼 양방향 통신이 필요한 시나리오에서는 WebSocket이 필수적이다. 실시간 알림처럼 서버 푸시만 필요하면 SSE가 더 간단하다.

---

## 13.2 WebFlux에서 WebSocket 핸들러 구현

### 13.2.1 의존성 설정

Spring WebFlux에는 WebSocket 지원이 기본 포함되어 있으므로 별도의 의존성이 필요 없다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    implementation 'org.springframework.boot:spring-boot-starter-data-mongodb-reactive'
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
}
```

### 13.2.2 WebSocketHandler 인터페이스

Spring WebFlux의 WebSocket 지원은 `WebSocketHandler` 인터페이스를 중심으로 설계되어 있다.

```java
public interface WebSocketHandler {
    Mono<Void> handle(WebSocketSession session);
}
```

`handle()` 메서드는 WebSocket 연결 수립 시 호출되며, 반환하는 `Mono<Void>`가 완료되면 연결이 종료된다. `WebSocketSession`은 `receive()`로 수신 메시지 스트림(`Flux<WebSocketMessage>`)을, `send()`로 송신 스트림을 제공한다.

가장 기본적인 에코 핸들러를 구현한다.

```java
@Component
@Slf4j
public class EchoWebSocketHandler implements WebSocketHandler {

    @Override
    public Mono<Void> handle(WebSocketSession session) {
        log.info("WebSocket 연결 수립: sessionId={}", session.getId());

        Flux<WebSocketMessage> output = session.receive()
            .map(message -> {
                String payload = message.getPayloadAsText();
                log.info("수신 메시지: {}", payload);
                return session.textMessage("Echo: " + payload);
            });

        return session.send(output)
            .doFinally(signal ->
                log.info("WebSocket 연결 종료: sessionId={}", session.getId()));
    }
}
```

### 13.2.3 HandlerMapping 설정

WebSocket 핸들러를 URL 경로에 매핑하려면 `HandlerMapping`과 `WebSocketHandlerAdapter`를 설정한다.

```java
@Configuration
public class WebSocketConfig {

    @Bean
    public HandlerMapping webSocketHandlerMapping(EchoWebSocketHandler echoHandler) {
        Map<String, WebSocketHandler> handlerMap = Map.of("/ws/echo", echoHandler);

        SimpleUrlHandlerMapping mapping = new SimpleUrlHandlerMapping();
        mapping.setUrlMap(handlerMap);
        mapping.setOrder(Ordered.HIGHEST_PRECEDENCE);
        return mapping;
    }

    @Bean
    public WebSocketHandlerAdapter webSocketHandlerAdapter() {
        return new WebSocketHandlerAdapter();
    }
}
```

`order`를 `Ordered.HIGHEST_PRECEDENCE`로 설정하여 다른 핸들러 매핑보다 먼저 WebSocket 요청을 처리한다.

### 13.2.4 메시지 송수신 패턴

WebSocket 메시지 송수신은 세 가지 패턴으로 나눌 수 있다.

**패턴 1: 수신 전용** -- 클라이언트 메시지를 받아 처리만 한다.

```java
public Mono<Void> handle(WebSocketSession session) {
    return session.receive()
        .doOnNext(msg -> log.info("수신: {}", msg.getPayloadAsText()))
        .then();
}
```

**패턴 2: 송신 전용** -- 서버에서 클라이언트로 일방적으로 푸시한다.

```java
public Mono<Void> handle(WebSocketSession session) {
    Flux<WebSocketMessage> output = Flux.interval(Duration.ofSeconds(1))
        .map(tick -> session.textMessage("서버 시간: " + LocalDateTime.now()));
    return session.send(output);
}
```

**패턴 3: 양방향** -- `Mono.zip()`으로 수신과 송신을 동시에 구독한다.

```java
public Mono<Void> handle(WebSocketSession session) {
    Mono<Void> input = session.receive()
        .doOnNext(msg -> processMessage(msg.getPayloadAsText()))
        .then();

    Mono<Void> output = session.send(
        externalEventSource().map(event -> session.textMessage(event)));

    return Mono.zip(input, output).then();
}
```

### 13.2.5 JSON 메시지 처리

실제 애플리케이션에서는 JSON 형식의 구조화된 메시지를 교환한다.

```java
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class ChatMessage {
    private String type;       // MESSAGE, JOIN, LEAVE
    private String roomId;
    private String sender;
    private String content;
    private LocalDateTime timestamp;
}
```

```java
@Component
@RequiredArgsConstructor @Slf4j
public class JsonWebSocketHandler implements WebSocketHandler {

    private final ObjectMapper objectMapper;

    @Override
    public Mono<Void> handle(WebSocketSession session) {
        Flux<WebSocketMessage> output = session.receive()
            .map(WebSocketMessage::getPayloadAsText)
            .flatMap(payload -> {
                try {
                    ChatMessage msg = objectMapper.readValue(payload, ChatMessage.class);
                    msg.setTimestamp(LocalDateTime.now());
                    return Mono.just(session.textMessage(
                        objectMapper.writeValueAsString(msg)));
                } catch (JsonProcessingException e) {
                    log.error("JSON 파싱 오류: {}", e.getMessage());
                    return Mono.empty();
                }
            });
        return session.send(output);
    }
}
```

JavaScript 클라이언트로 동작을 확인한다.

```javascript
const ws = new WebSocket('ws://localhost:8080/ws/echo');
ws.onopen = () => ws.send('Hello WebSocket!');
ws.onmessage = (event) => console.log('수신:', event.data);
ws.onclose = (event) => console.log('종료:', event.code);
```

---

## 13.3 실시간 채팅 애플리케이션 구축

WebSocket과 MongoDB를 결합하여 다중 채팅방을 지원하는 실시간 채팅 애플리케이션을 구축한다.

### 13.3.1 도메인 모델과 리포지토리

```java
@Document(collection = "chat_rooms")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class ChatRoom {
    @Id private String id;
    private String name;
    private String description;
    private String createdBy;
    private Set<String> participants;
    private LocalDateTime createdAt;
}
```

```java
@Document(collection = "chat_messages")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class ChatMessageDocument {
    @Id private String id;
    @Indexed private String roomId;
    private String sender;
    private String content;
    private MessageType type;
    private LocalDateTime timestamp;

    public enum MessageType { MESSAGE, JOIN, LEAVE, SYSTEM }
}
```

```java
public interface ChatRoomRepository extends ReactiveMongoRepository<ChatRoom, String> {
    Flux<ChatRoom> findByParticipantsContaining(String username);
}

public interface ChatMessageRepository
        extends ReactiveMongoRepository<ChatMessageDocument, String> {
    Flux<ChatMessageDocument> findByRoomIdOrderByTimestampDesc(
        String roomId, Pageable pageable);
    Flux<ChatMessageDocument> findByRoomIdAndTimestampAfterOrderByTimestampAsc(
        String roomId, LocalDateTime after);
}
```

### 13.3.2 채팅방 관리 서비스

```java
@Service
@RequiredArgsConstructor
public class ChatRoomService {

    private final ChatRoomRepository chatRoomRepository;

    public Mono<ChatRoom> createRoom(String name, String description,
                                      String createdBy) {
        ChatRoom room = ChatRoom.builder()
            .name(name).description(description).createdBy(createdBy)
            .participants(new HashSet<>(Set.of(createdBy)))
            .createdAt(LocalDateTime.now()).build();
        return chatRoomRepository.save(room);
    }

    public Flux<ChatRoom> getAllRooms() {
        return chatRoomRepository.findAll();
    }

    public Mono<ChatRoom> joinRoom(String roomId, String username) {
        return chatRoomRepository.findById(roomId)
            .flatMap(room -> {
                room.getParticipants().add(username);
                return chatRoomRepository.save(room);
            });
    }

    public Mono<ChatRoom> leaveRoom(String roomId, String username) {
        return chatRoomRepository.findById(roomId)
            .flatMap(room -> {
                room.getParticipants().remove(username);
                return chatRoomRepository.save(room);
            });
    }
}
```

### 13.3.3 메시지 브로드캐스팅

채팅 메시지를 같은 채팅방의 모든 세션에 브로드캐스팅하는 핵심 서비스를 구현한다. Reactor의 `Sinks`를 사용하여 메시지를 발행하고, 각 세션이 이를 구독하는 구조로 설계한다.

```java
@Service
@Slf4j
public class ChatMessageBroker {

    private final Map<String, Sinks.Many<ChatMessageDocument>> roomSinks =
        new ConcurrentHashMap<>();

    public Sinks.Many<ChatMessageDocument> getRoomSink(String roomId) {
        return roomSinks.computeIfAbsent(roomId,
            id -> Sinks.many().multicast().onBackpressureBuffer(256));
    }

    public void publish(String roomId, ChatMessageDocument message) {
        Sinks.EmitResult result = getRoomSink(roomId).tryEmitNext(message);
        if (result.isFailure()) {
            log.warn("메시지 발행 실패: roomId={}, result={}", roomId, result);
        }
    }

    public Flux<ChatMessageDocument> subscribe(String roomId) {
        return getRoomSink(roomId).asFlux();
    }

    public void removeRoom(String roomId) {
        Sinks.Many<ChatMessageDocument> removed = roomSinks.remove(roomId);
        if (removed != null) removed.tryEmitComplete();
    }
}
```

`Sinks.many().multicast().onBackpressureBuffer(256)`는 여러 구독자에게 동시에 메시지를 전달하는 Hot Publisher를 생성한다. 구독자가 처리하지 못한 메시지는 최대 256개까지 버퍼에 저장된다.

### 13.3.4 채팅 메시지 서비스

```java
@Service
@RequiredArgsConstructor @Slf4j
public class ChatMessageService {

    private final ChatMessageRepository chatMessageRepository;
    private final ChatMessageBroker messageBroker;

    public Mono<ChatMessageDocument> saveAndBroadcast(ChatMessageDocument message) {
        message.setTimestamp(LocalDateTime.now());
        return chatMessageRepository.save(message)
            .doOnSuccess(saved -> messageBroker.publish(saved.getRoomId(), saved));
    }

    public Flux<ChatMessageDocument> getRecentMessages(String roomId, int limit) {
        return chatMessageRepository.findByRoomIdOrderByTimestampDesc(
            roomId, PageRequest.of(0, limit));
    }

    public Flux<ChatMessageDocument> getMessagesSince(
            String roomId, LocalDateTime since) {
        return chatMessageRepository
            .findByRoomIdAndTimestampAfterOrderByTimestampAsc(roomId, since);
    }
}
```

### 13.3.5 채팅 WebSocket 핸들러

서비스를 조합하여 채팅 전용 WebSocket 핸들러를 완성한다.

```java
@Component
@RequiredArgsConstructor @Slf4j
public class ChatWebSocketHandler implements WebSocketHandler {

    private final ChatMessageService chatMessageService;
    private final ChatMessageBroker messageBroker;
    private final ObjectMapper objectMapper;

    @Override
    public Mono<Void> handle(WebSocketSession session) {
        URI uri = session.getHandshakeInfo().getUri();
        Map<String, String> params = parseQueryParams(uri);
        String roomId = params.get("roomId");
        String username = params.get("username");

        if (roomId == null || username == null) {
            return session.close(CloseStatus.POLICY_VIOLATION);
        }

        log.info("채팅 연결: roomId={}, username={}", roomId, username);

        // 입장 알림
        Mono<Void> joinNotification = createSystemMessage(
            roomId, username + "님이 입장했습니다.",
            ChatMessageDocument.MessageType.JOIN);

        // 수신: 클라이언트 메시지를 저장 및 브로드캐스트
        Mono<Void> input = session.receive()
            .flatMap(msg -> handleIncoming(msg.getPayloadAsText(), roomId, username))
            .doFinally(signal -> createSystemMessage(roomId,
                username + "님이 퇴장했습니다.",
                ChatMessageDocument.MessageType.LEAVE).subscribe())
            .then();

        // 송신: 채팅방 브로드캐스트 스트림 구독
        Flux<WebSocketMessage> output = messageBroker.subscribe(roomId)
            .mapNotNull(chatMsg -> toWebSocketMessage(session, chatMsg));

        return joinNotification
            .then(Mono.zip(input, session.send(output)).then());
    }

    private Mono<ChatMessageDocument> handleIncoming(
            String payload, String roomId, String sender) {
        try {
            ChatMessage incoming = objectMapper.readValue(payload, ChatMessage.class);
            ChatMessageDocument doc = ChatMessageDocument.builder()
                .roomId(roomId).sender(sender).content(incoming.getContent())
                .type(ChatMessageDocument.MessageType.MESSAGE).build();
            return chatMessageService.saveAndBroadcast(doc);
        } catch (JsonProcessingException e) {
            log.error("메시지 파싱 오류: {}", e.getMessage());
            return Mono.empty();
        }
    }

    private Mono<Void> createSystemMessage(String roomId, String content,
                                            ChatMessageDocument.MessageType type) {
        ChatMessageDocument msg = ChatMessageDocument.builder()
            .roomId(roomId).sender("SYSTEM").content(content).type(type).build();
        return chatMessageService.saveAndBroadcast(msg).then();
    }

    private WebSocketMessage toWebSocketMessage(
            WebSocketSession session, ChatMessageDocument msg) {
        try {
            return session.textMessage(objectMapper.writeValueAsString(msg));
        } catch (JsonProcessingException e) {
            return null;
        }
    }

    private Map<String, String> parseQueryParams(URI uri) {
        Map<String, String> params = new HashMap<>();
        String query = uri.getQuery();
        if (query == null) return params;
        for (String param : query.split("&")) {
            String[] pair = param.split("=", 2);
            if (pair.length == 2) params.put(pair[0], pair[1]);
        }
        return params;
    }
}
```

WebSocket 라우팅에 등록한다.

```java
@Configuration
public class WebSocketConfig {
    @Bean
    public HandlerMapping webSocketHandlerMapping(ChatWebSocketHandler chatHandler) {
        SimpleUrlHandlerMapping mapping = new SimpleUrlHandlerMapping();
        mapping.setUrlMap(Map.of("/ws/chat", chatHandler));
        mapping.setOrder(Ordered.HIGHEST_PRECEDENCE);
        return mapping;
    }

    @Bean
    public WebSocketHandlerAdapter webSocketHandlerAdapter() {
        return new WebSocketHandlerAdapter();
    }
}
```

### 13.3.6 채팅방 REST API

WebSocket 연결 전 채팅방을 관리하기 위한 REST API를 제공한다.

```java
@RestController
@RequestMapping("/api/chat/rooms")
@RequiredArgsConstructor
public class ChatRoomController {

    private final ChatRoomService chatRoomService;
    private final ChatMessageService chatMessageService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<ChatRoom> createRoom(@RequestBody CreateRoomRequest request) {
        return chatRoomService.createRoom(
            request.getName(), request.getDescription(), request.getCreatedBy());
    }

    @GetMapping
    public Flux<ChatRoom> getAllRooms() {
        return chatRoomService.getAllRooms();
    }

    @GetMapping("/{roomId}/messages")
    public Flux<ChatMessageDocument> getRecentMessages(
            @PathVariable String roomId,
            @RequestParam(defaultValue = "50") int limit) {
        return chatMessageService.getRecentMessages(roomId, limit);
    }

    @PostMapping("/{roomId}/join")
    public Mono<ChatRoom> joinRoom(@PathVariable String roomId,
                                    @RequestParam String username) {
        return chatRoomService.joinRoom(roomId, username);
    }
}
```

### 13.3.7 이전 메시지 로드

클라이언트가 채팅방에 접속할 때 이전 메시지를 로드하는 두 가지 전략이 있다.

**전략 1: REST API를 통한 초기 로드** -- WebSocket 연결 전에 REST API로 최근 메시지를 가져온다.

```javascript
async function joinChatRoom(roomId, username) {
    const res = await fetch(`/api/chat/rooms/${roomId}/messages?limit=50`);
    const history = await res.json();
    history.reverse().forEach(msg => displayMessage(msg));

    const ws = new WebSocket(
        `ws://localhost:8080/ws/chat?roomId=${roomId}&username=${username}`);
    ws.onmessage = (e) => displayMessage(JSON.parse(e.data));
}
```

**전략 2: WebSocket 내 히스토리 전송** -- `concatWith()`로 히스토리 후 실시간 스트림을 연결한다.

```java
Flux<WebSocketMessage> history = chatMessageService.getRecentMessages(roomId, 50)
    .mapNotNull(msg -> toWebSocketMessage(session, msg));
Flux<WebSocketMessage> live = messageBroker.subscribe(roomId)
    .mapNotNull(msg -> toWebSocketMessage(session, msg));

Flux<WebSocketMessage> output = history.concatWith(live);
```

전략 1이 관리가 용이하고, 히스토리-실시간 사이 메시지 누락 위험이 적어 프로덕션에서 권장된다.

### 13.3.8 MongoDB 인덱스 설정

채팅 메시지 조회 성능을 위해 복합 인덱스를 설정한다.

```java
@Configuration
@RequiredArgsConstructor
public class MongoIndexConfig {
    private final ReactiveMongoTemplate mongoTemplate;

    @PostConstruct
    public void initIndexes() {
        mongoTemplate.indexOps(ChatMessageDocument.class)
            .ensureIndex(new Index()
                .on("roomId", Sort.Direction.ASC)
                .on("timestamp", Sort.Direction.DESC))
            .subscribe();
    }
}
```

---

## 13.4 WebSocket 세션 관리

### 13.4.1 세션 라이프사이클

WebSocket 세션은 `CONNECTING -> OPEN -> CLOSING -> CLOSED` 순서의 라이프사이클을 따른다. 세션을 체계적으로 관리하기 위해 세션 레지스트리를 구현한다.

```java
@Component @Slf4j
public class WebSocketSessionRegistry {

    private final Map<String, Map<String, WebSocketSession>> roomSessions =
        new ConcurrentHashMap<>();
    private final Map<String, String> sessionUserMap = new ConcurrentHashMap<>();

    public void register(String roomId, String username, WebSocketSession session) {
        roomSessions.computeIfAbsent(roomId, k -> new ConcurrentHashMap<>())
            .put(session.getId(), session);
        sessionUserMap.put(session.getId(), username);
        log.info("세션 등록: roomId={}, username={}, 현재 인원={}",
            roomId, username, getSessionCount(roomId));
    }

    public void unregister(String roomId, WebSocketSession session) {
        Map<String, WebSocketSession> sessions = roomSessions.get(roomId);
        if (sessions != null) {
            sessions.remove(session.getId());
            if (sessions.isEmpty()) roomSessions.remove(roomId);
        }
        sessionUserMap.remove(session.getId());
    }

    public int getSessionCount(String roomId) {
        Map<String, WebSocketSession> s = roomSessions.get(roomId);
        return s != null ? s.size() : 0;
    }

    public Set<String> getOnlineUsers(String roomId) {
        Map<String, WebSocketSession> sessions = roomSessions.get(roomId);
        if (sessions == null) return Collections.emptySet();
        return sessions.keySet().stream()
            .map(sessionUserMap::get).filter(Objects::nonNull)
            .collect(Collectors.toSet());
    }

    public Map<String, WebSocketSession> getAllSessions() {
        Map<String, WebSocketSession> all = new ConcurrentHashMap<>();
        roomSessions.values().forEach(all::putAll);
        return all;
    }
}
```

세션 레지스트리를 ChatWebSocketHandler에 통합하면 `register()`를 연결 시에, `unregister()`를 `doFinally()`에서 호출하여 세션 생명주기를 관리한다.

### 13.4.2 Ping/Pong 하트비트

WebSocket 연결이 네트워크 문제나 유휴 상태로 끊어질 수 있다. Ping/Pong 메커니즘으로 연결 상태를 주기적으로 확인한다.

**서버 측 Ping 스케줄러:**

```java
@Component
@RequiredArgsConstructor @Slf4j
public class WebSocketPingScheduler {

    private final WebSocketSessionRegistry sessionRegistry;

    @Scheduled(fixedRate = 30000)
    public void sendPing() {
        sessionRegistry.getAllSessions().forEach((sessionId, session) -> {
            if (session.isOpen()) {
                session.send(Mono.just(session.pingMessage(factory ->
                    factory.wrap("ping".getBytes(StandardCharsets.UTF_8)))))
                    .subscribe(null, error ->
                        log.warn("Ping 실패: sessionId={}", sessionId));
            }
        });
    }
}
```

`@EnableScheduling`을 메인 애플리케이션에 추가해야 한다.

**애플리케이션 레벨 하트비트:**

프록시가 WebSocket 프레임을 지원하지 않는 환경에서는 애플리케이션 레벨 하트비트를 사용한다.

```java
// 수신 시 하트비트 필터링
Mono<Void> input = session.receive()
    .filter(msg -> !"HEARTBEAT".equals(msg.getPayloadAsText()))
    .flatMap(msg -> handleIncoming(msg.getPayloadAsText(), roomId, username))
    .then();

// 송신 시 하트비트와 실시간 메시지 병합
Flux<WebSocketMessage> heartbeat = Flux.interval(Duration.ofSeconds(25))
    .map(tick -> session.textMessage("HEARTBEAT"));
Flux<WebSocketMessage> output = Flux.merge(
    messageBroker.subscribe(roomId).mapNotNull(m -> toWebSocketMessage(session, m)),
    heartbeat);
```

### 13.4.3 재연결 처리

네트워크 불안정으로 연결이 끊어질 때를 대비하여 클라이언트 측 자동 재연결과 서버 측 메시지 복구를 구현한다.

**클라이언트 재연결 (지수 백오프):**

```javascript
class ReconnectingWebSocket {
    constructor(url, options = {}) {
        this.url = url;
        this.maxRetries = options.maxRetries || 10;
        this.retryDelay = options.retryDelay || 1000;
        this.maxRetryDelay = options.maxRetryDelay || 30000;
        this.retryCount = 0;
        this.lastMessageTimestamp = null;
        this.connect();
    }

    connect() {
        let connectUrl = this.url;
        if (this.lastMessageTimestamp) {
            const sep = connectUrl.includes('?') ? '&' : '?';
            connectUrl += `${sep}since=${this.lastMessageTimestamp}`;
        }
        this.ws = new WebSocket(connectUrl);

        this.ws.onopen = () => { this.retryCount = 0; };
        this.ws.onmessage = (e) => {
            if (e.data === 'HEARTBEAT') return;
            const msg = JSON.parse(e.data);
            this.lastMessageTimestamp = msg.timestamp;
            this.onMessage?.(msg);
        };
        this.ws.onclose = (e) => {
            if (e.code !== 1000 && this.retryCount < this.maxRetries) {
                const delay = Math.min(
                    this.retryDelay * Math.pow(2, this.retryCount),
                    this.maxRetryDelay);
                setTimeout(() => { this.retryCount++; this.connect(); }, delay);
            }
        };
    }

    send(data) {
        if (this.ws?.readyState === WebSocket.OPEN)
            this.ws.send(typeof data === 'string' ? data : JSON.stringify(data));
    }

    close() { this.maxRetries = 0; this.ws?.close(1000); }
}
```

**서버 측 메시지 복구:**

```java
@Override
public Mono<Void> handle(WebSocketSession session) {
    // ... 파라미터 추출 ...
    String sinceParam = params.get("since");

    // 재연결 시 놓친 메시지 복구
    Flux<WebSocketMessage> missedMessages = Flux.empty();
    if (sinceParam != null) {
        LocalDateTime since = LocalDateTime.parse(sinceParam);
        missedMessages = chatMessageService.getMessagesSince(roomId, since)
            .mapNotNull(msg -> toWebSocketMessage(session, msg));
    }

    Flux<WebSocketMessage> liveMessages = messageBroker.subscribe(roomId)
        .mapNotNull(msg -> toWebSocketMessage(session, msg));

    // 놓친 메시지 먼저 전송 후 실시간 스트림 전환
    Flux<WebSocketMessage> output = missedMessages.concatWith(liveMessages);

    Mono<Void> input = session.receive()
        .filter(msg -> !"HEARTBEAT".equals(msg.getPayloadAsText()))
        .flatMap(msg -> handleIncoming(msg.getPayloadAsText(), roomId, username))
        .doFinally(signal -> sessionRegistry.unregister(roomId, session))
        .then();

    return Mono.zip(input, session.send(output)).then();
}
```

### 13.4.4 연결 종료와 보안

주요 `CloseStatus` 코드를 정리한다.

| 코드 | 의미 |
|------|------|
| 1000 | 정상 종료 |
| 1001 | 서버 종료 또는 페이지 이동 |
| 1008 | 정책 위반 |
| 1011 | 서버 내부 오류 |
| 4000+ | 애플리케이션 정의 코드 |

서버에서 특정 사용자를 강제 퇴장시키는 예시이다.

```java
public Mono<Void> disconnectUser(String roomId, String targetUsername) {
    return Flux.fromIterable(sessionRegistry.getSessions(roomId).entrySet())
        .filter(e -> targetUsername.equals(sessionRegistry.getUsername(e.getKey())))
        .flatMap(e -> e.getValue()
            .close(new CloseStatus(4001, "관리자에 의해 종료")))
        .then();
}
```

WebSocket 엔드포인트에도 Spring Security를 적용할 수 있다. WebSocket 핸드셰이크는 HTTP 요청이므로, JWT 토큰을 쿼리 파라미터로 전달하고 핸들러에서 검증한다.

```java
@Bean
public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
    return http
        .authorizeExchange(ex -> ex
            .pathMatchers("/ws/**").authenticated()
            .pathMatchers("/api/auth/**").permitAll()
            .anyExchange().authenticated())
        .csrf(csrf -> csrf.disable())
        .build();
}
```

```java
// 핸들러 내부에서 JWT 검증
String token = params.get("token");
if (token == null || !jwtTokenProvider.validateToken(token)) {
    return session.close(new CloseStatus(4401, "인증 실패"));
}
String username = jwtTokenProvider.getUsernameFromToken(token);
```

```javascript
// 클라이언트에서 토큰 전달
const token = localStorage.getItem('accessToken');
const ws = new WebSocket(
    `ws://localhost:8080/ws/chat?roomId=${roomId}&username=${user}&token=${token}`);
```

> **주의**: URL 쿼리 파라미터로 토큰을 전달하면 로그에 노출될 수 있다. 프로덕션에서는 쿠키나 첫 번째 메시지를 통한 인증, 또는 핸드셰이크 전 별도 토큰 발급 엔드포인트를 활용하는 것이 더 안전하다.

---

## 요약

이번 장에서 다룬 핵심 내용을 정리한다.

| 주제 | 핵심 내용 |
|------|----------|
| **WebSocket 프로토콜** | HTTP 핸드셰이크로 연결 수립, 프레임 기반 양방향 통신, SSE/Long Polling과의 차이 |
| **WebSocket 핸들러** | `WebSocketHandler` 인터페이스, `SimpleUrlHandlerMapping`으로 경로 매핑, 수신/송신/양방향 패턴 |
| **실시간 채팅** | `Sinks.Many`를 활용한 메시지 브로드캐스팅, MongoDB 저장, 이전 메시지 로드, REST API 연동 |
| **세션 관리** | 세션 레지스트리, Ping/Pong 하트비트, 지수 백오프 재연결, 보안 설정 |

WebSocket은 실시간 양방향 통신이 필요한 다양한 시나리오에서 핵심적인 역할을 한다. Spring WebFlux의 리액티브 WebSocket 지원과 Reactor의 `Sinks`를 활용하면, 높은 동시 연결 수를 효율적으로 처리하는 확장성 있는 실시간 애플리케이션을 구축할 수 있다. 다음 장에서는 WebClient를 활용하여 외부 API를 리액티브하게 호출하는 방법을 다룬다.


---

# Chapter 14. WebClient: 리액티브 HTTP 클라이언트

Spring WebFlux 애플리케이션에서 외부 서비스와 통신해야 할 때, 전통적인 `RestTemplate` 대신 `WebClient`를 사용한다. `WebClient`는 Spring 5에서 도입된 **논블로킹 리액티브 HTTP 클라이언트**로, 이번 장에서는 설정과 기본 사용법부터 에러 핸들링, 재시도, 타임아웃, 외부 API 동시 호출, 필터까지 실전에서 필요한 모든 내용을 다룬다.

---

## 14.1 WebClient 설정과 기본 사용법

### 14.1.1 WebClient란?

`WebClient`는 Spring WebFlux 모듈에 포함된 논블로킹 HTTP 클라이언트다. 내부적으로 Reactor Netty의 `HttpClient`를 사용하며, 리액티브 스트림 기반으로 요청과 응답을 처리한다.

| 특성 | RestTemplate | WebClient |
|------|-------------|-----------|
| **블로킹 여부** | 블로킹 | 논블로킹 |
| **반환 타입** | 직접 객체 반환 | `Mono<T>`, `Flux<T>` |
| **스트리밍** | 미지원 | SSE, 스트리밍 응답 지원 |
| **유지 상태** | Spring 6에서 deprecated | 현재 권장 방식 |

### 14.1.2 WebClient 생성과 빈 설정

`WebClient`는 `create()`, `create(baseUrl)`, `builder()` 세 가지 방식으로 생성한다. 실전에서는 `builder()`를 사용하여 빈으로 등록하는 것이 일반적이다. 여러 외부 서비스를 호출하는 경우, 서비스별로 별도의 빈을 정의한다.

```java
@Configuration
public class WebClientConfig {

    @Bean("userServiceClient")
    public WebClient userServiceClient() {
        return WebClient.builder()
            .baseUrl("https://user-service.example.com")
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .build();
    }

    @Bean("orderServiceClient")
    public WebClient orderServiceClient() {
        return WebClient.builder()
            .baseUrl("https://order-service.example.com")
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .build();
    }
}
```

### 14.1.3 커넥션 풀 설정

운영 환경에서는 Reactor Netty의 커넥션 풀을 명시적으로 설정하는 것이 바람직하다.

```java
@Bean
public WebClient webClient() {
    ConnectionProvider provider = ConnectionProvider.builder("custom-pool")
        .maxConnections(500)                           // 최대 커넥션 수
        .maxIdleTime(Duration.ofSeconds(20))            // 유휴 커넥션 유지 시간
        .maxLifeTime(Duration.ofSeconds(60))            // 커넥션 최대 수명
        .pendingAcquireTimeout(Duration.ofSeconds(60))  // 커넥션 대기 타임아웃
        .evictInBackground(Duration.ofSeconds(120))     // 백그라운드 정리 주기
        .build();

    HttpClient httpClient = HttpClient.create(provider)
        .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000)
        .compress(true);

    return WebClient.builder()
        .baseUrl("https://api.example.com")
        .clientConnector(new ReactorClientHttpConnector(httpClient))
        .build();
}
```

### 14.1.4 코덱(Codec) 설정

대용량 응답 처리나 커스텀 직렬화가 필요한 경우 코덱을 설정한다. `maxInMemorySize`는 응답 본문의 메모리 버퍼 최대 크기(기본 256KB)이며, 대용량 JSON 응답 시 `DataBufferLimitException`이 발생하면 이 값을 늘린다.

```java
@Bean
public WebClient webClient() {
    return WebClient.builder()
        .codecs(configurer -> {
            configurer.defaultCodecs().maxInMemorySize(10 * 1024 * 1024); // 10MB

            ObjectMapper mapper = new ObjectMapper();
            mapper.registerModule(new JavaTimeModule());
            mapper.setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);
            configurer.defaultCodecs().jackson2JsonEncoder(
                new Jackson2JsonEncoder(mapper, MediaType.APPLICATION_JSON));
            configurer.defaultCodecs().jackson2JsonDecoder(
                new Jackson2JsonDecoder(mapper, MediaType.APPLICATION_JSON));
        })
        .build();
}
```

---

## 14.2 요청/응답 처리 (GET, POST, PUT, DELETE)

### 14.2.1 GET 요청

```java
@Service
@RequiredArgsConstructor
public class ProductClientService {

    private final WebClient webClient;

    // 단일 객체 조회
    public Mono<Product> getProduct(String id) {
        return webClient.get()
            .uri("/api/products/{id}", id)
            .retrieve()
            .bodyToMono(Product.class);
    }

    // 목록 조회
    public Flux<Product> getAllProducts() {
        return webClient.get()
            .uri("/api/products")
            .retrieve()
            .bodyToFlux(Product.class);
    }

    // 쿼리 파라미터 사용
    public Flux<Product> searchProducts(String keyword, int page, int size) {
        return webClient.get()
            .uri(uriBuilder -> uriBuilder
                .path("/api/products/search")
                .queryParam("keyword", keyword)
                .queryParam("page", page)
                .queryParam("size", size)
                .build())
            .retrieve()
            .bodyToFlux(Product.class);
    }
}
```

### 14.2.2 POST 요청

```java
// JSON 본문 전송
public Mono<Product> createProduct(ProductRequest request) {
    return webClient.post()
        .uri("/api/products")
        .bodyValue(request)
        .retrieve()
        .bodyToMono(Product.class);
}

// Mono를 본문으로 전송
public Mono<Product> createProductReactive(Mono<ProductRequest> request) {
    return webClient.post()
        .uri("/api/products")
        .body(request, ProductRequest.class)
        .retrieve()
        .bodyToMono(Product.class);
}

// 폼 데이터 전송
public Mono<String> submitForm(String username, String password) {
    return webClient.post()
        .uri("/api/auth/login")
        .contentType(MediaType.APPLICATION_FORM_URLENCODED)
        .body(BodyInserters.fromFormData("username", username)
            .with("password", password))
        .retrieve()
        .bodyToMono(String.class);
}
```

`bodyValue()`는 이미 준비된 객체를 전송할 때, `body()`는 `Publisher` 타입(Mono, Flux)을 전송할 때 사용한다.

### 14.2.3 PUT과 DELETE 요청

```java
public Mono<Product> updateProduct(String id, ProductRequest request) {
    return webClient.put()
        .uri("/api/products/{id}", id)
        .bodyValue(request)
        .retrieve()
        .bodyToMono(Product.class);
}

public Mono<Void> deleteProduct(String id) {
    return webClient.delete()
        .uri("/api/products/{id}", id)
        .retrieve()
        .bodyToMono(Void.class);
}
```

### 14.2.4 retrieve() vs exchangeToMono()

**retrieve()**: 간결한 방식. 4xx/5xx 상태 코드에 대해 자동으로 예외를 발생시킨다.

```java
Mono<Product> product = webClient.get()
    .uri("/api/products/{id}", id)
    .retrieve()
    .bodyToMono(Product.class);
```

**exchangeToMono()**: 상태 코드, 헤더 등 전체 응답 정보에 접근할 수 있다.

```java
public Mono<Product> getProductWithStatus(String id) {
    return webClient.get()
        .uri("/api/products/{id}", id)
        .exchangeToMono(response -> {
            if (response.statusCode().is2xxSuccessful()) {
                return response.bodyToMono(Product.class);
            } else if (response.statusCode() == HttpStatus.NOT_FOUND) {
                return Mono.empty();
            } else {
                return response.createError();
            }
        });
}
```

> **주의**: 이전 버전의 `exchange()` 메서드는 deprecated되었다. 리소스 누수 위험이 있으므로, 반드시 `exchangeToMono()` 또는 `exchangeToFlux()`를 사용한다.

응답 헤더와 상태 코드가 모두 필요하면 `toEntity()`를 사용한다.

```java
public Mono<ResponseEntity<Product>> getProductWithHeaders(String id) {
    return webClient.get()
        .uri("/api/products/{id}", id)
        .retrieve()
        .toEntity(Product.class);
}
```

### 14.2.5 스트리밍 응답 처리

SSE 스트림이나 NDJSON 스트림을 구독할 수 있다.

```java
public Flux<ServerSentEvent<String>> subscribeToEvents() {
    return webClient.get()
        .uri("/api/events/stream")
        .accept(MediaType.TEXT_EVENT_STREAM)
        .retrieve()
        .bodyToFlux(new ParameterizedTypeReference<ServerSentEvent<String>>() {});
}

public Flux<Product> streamProducts() {
    return webClient.get()
        .uri("/api/products/stream")
        .accept(MediaType.APPLICATION_NDJSON)
        .retrieve()
        .bodyToFlux(Product.class);
}
```

---

## 14.3 에러 핸들링과 재시도 전략

### 14.3.1 onStatus()를 활용한 상태 코드별 처리

`retrieve()`는 4xx/5xx 상태 코드에 대해 자동으로 `WebClientResponseException`을 발생시킨다. `onStatus()`로 상태 코드별 커스텀 에러 처리를 정의할 수 있다.

```java
public Mono<Product> getProduct(String id) {
    return webClient.get()
        .uri("/api/products/{id}", id)
        .retrieve()
        .onStatus(HttpStatusCode::is4xxClientError, response -> {
            if (response.statusCode() == HttpStatus.NOT_FOUND) {
                return Mono.error(
                    new ProductNotFoundException("상품을 찾을 수 없습니다: " + id));
            }
            return response.bodyToMono(ErrorResponse.class)
                .flatMap(error -> Mono.error(
                    new InvalidRequestException(error.getMessage())));
        })
        .onStatus(HttpStatusCode::is5xxServerError, response ->
            response.bodyToMono(String.class)
                .flatMap(body -> Mono.error(
                    new ExternalServiceException("서버 에러: " + body)))
        )
        .bodyToMono(Product.class);
}
```

### 14.3.2 retryWhen()과 Retry.backoff()

`retry(n)`은 즉시 재시도하므로 서버에 과부하를 유발할 수 있다. 운영 환경에서는 `Retry.backoff()`로 지수 백오프(exponential backoff) 전략을 사용한다.

```java
public Mono<Product> getProductWithBackoff(String id) {
    return webClient.get()
        .uri("/api/products/{id}", id)
        .retrieve()
        .bodyToMono(Product.class)
        .retryWhen(Retry.backoff(3, Duration.ofSeconds(1))
            .maxBackoff(Duration.ofSeconds(10))
            .jitter(0.5)
            .filter(ex -> ex instanceof WebClientResponseException.ServiceUnavailable
                       || ex instanceof ConnectException)
            .doBeforeRetry(signal -> log.warn(
                "재시도 #{} - 원인: {}",
                signal.totalRetries() + 1,
                signal.failure().getMessage()))
            .onRetryExhaustedThrow((spec, signal) ->
                new ExternalServiceException(
                    "재시도 횟수 초과: " + signal.failure().getMessage(),
                    signal.failure()))
        );
}
```

| 재시도 횟수 | 최소 대기 시간 | jitter=0.5 적용 시 범위 |
|-----------|-------------|---------------------|
| 1회차 | 1초 | 0.5초 ~ 1.5초 |
| 2회차 | 2초 | 1초 ~ 3초 |
| 3회차 | 4초 | 2초 ~ 6초 |

`jitter`는 여러 클라이언트가 동시에 재시도하여 부하가 집중되는 "thundering herd" 문제를 방지한다.

### 14.3.3 서킷 브레이커 패턴

외부 서비스가 장시간 장애 상태일 때, Resilience4j로 서킷 브레이커를 적용한다.

```groovy
dependencies {
    implementation 'io.github.resilience4j:resilience4j-spring-boot3:2.2.0'
    implementation 'io.github.resilience4j:resilience4j-reactor:2.2.0'
}
```

```yaml
resilience4j:
  circuitbreaker:
    instances:
      productService:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 30s
        permitted-number-of-calls-in-half-open-state: 3
```

```java
@Service
@RequiredArgsConstructor
public class ProductClientService {

    private final WebClient webClient;
    private final CircuitBreakerRegistry circuitBreakerRegistry;

    public Mono<Product> getProduct(String id) {
        CircuitBreaker cb = circuitBreakerRegistry.circuitBreaker("productService");

        return webClient.get()
            .uri("/api/products/{id}", id)
            .retrieve()
            .bodyToMono(Product.class)
            .transformDeferred(CircuitBreakerOperator.of(cb))
            .onErrorResume(CallNotPermittedException.class, ex -> {
                log.warn("서킷 브레이커 OPEN - 폴백 실행");
                return Mono.just(Product.fallback(id));
            })
            .retryWhen(Retry.backoff(2, Duration.ofMillis(500))
                .filter(ex -> !(ex instanceof CallNotPermittedException)));
    }
}
```

| 상태 | 동작 |
|------|------|
| **CLOSED** | 정상 상태. 모든 요청 전달, 실패율 모니터링 |
| **OPEN** | 차단 상태. 즉시 폴백 실행. 대기 시간 후 HALF_OPEN 전환 |
| **HALF_OPEN** | 일부 요청만 허용하여 복구 확인. 성공하면 CLOSED, 실패하면 OPEN |

---

## 14.4 타임아웃 설정

외부 서비스 호출 시 타임아웃은 필수다. 타임아웃 없이 호출하면 외부 장애가 자신의 애플리케이션까지 전파될 수 있다.

### 14.4.1 계층별 타임아웃

```java
HttpClient httpClient = HttpClient.create()
    // 1. 커넥션 타임아웃: TCP 연결 수립
    .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 3000)
    // 2. 응답 타임아웃: 첫 응답 바이트 수신까지
    .responseTimeout(Duration.ofSeconds(5))
    // 3. 읽기/쓰기 타임아웃: 데이터 전송 중 무응답
    .doOnConnected(conn -> conn
        .addHandlerLast(new ReadTimeoutHandler(10, TimeUnit.SECONDS))
        .addHandlerLast(new WriteTimeoutHandler(10, TimeUnit.SECONDS)));

WebClient webClient = WebClient.builder()
    .clientConnector(new ReactorClientHttpConnector(httpClient))
    .build();
```

### 14.4.2 Reactor timeout() 연산자

리액티브 체인 수준에서 재시도 포함 전체 시간을 제한한다.

```java
public Mono<Product> getProduct(String id) {
    return webClient.get()
        .uri("/api/products/{id}", id)
        .retrieve()
        .bodyToMono(Product.class)
        .retryWhen(Retry.backoff(3, Duration.ofSeconds(1)))
        .timeout(Duration.ofSeconds(15))
        .onErrorResume(TimeoutException.class, ex ->
            Mono.error(new ExternalServiceException("응답 시간 초과")));
}
```

### 14.4.3 타임아웃 종합 정리

| 타임아웃 | 적용 계층 | 대상 |
|---------|----------|------|
| **커넥션 타임아웃** | TCP | 서버와 TCP 연결 수립 |
| **응답 타임아웃** | HTTP | 첫 응답 바이트 수신까지 |
| **읽기 타임아웃** | TCP | 데이터 읽기 중 무응답 |
| **쓰기 타임아웃** | TCP | 데이터 쓰기 중 무응답 |
| **Reactor timeout()** | 리액티브 | 전체 리액티브 체인 완료 |

---

## 14.5 외부 API 연동 실전 예제

### 14.5.1 REST API 호출 서비스

외부 날씨 API를 호출하는 실전 예제다.

```java
@Slf4j
@Service
public class WeatherClientService {

    private final WebClient webClient;

    public WeatherClientService(WebClient.Builder builder,
                                @Value("${weather.api.key}") String apiKey) {
        this.webClient = builder
            .baseUrl("https://api.openweathermap.org/data/2.5")
            .defaultUriVariables(Map.of("appid", apiKey))
            .build();
    }

    public Mono<WeatherResponse> getCurrentWeather(String city) {
        return webClient.get()
            .uri(uriBuilder -> uriBuilder
                .path("/weather")
                .queryParam("q", city)
                .queryParam("appid", "{appid}")
                .queryParam("units", "metric")
                .build())
            .retrieve()
            .onStatus(HttpStatusCode::is4xxClientError, response -> {
                if (response.statusCode() == HttpStatus.NOT_FOUND) {
                    return Mono.error(new CityNotFoundException("도시를 찾을 수 없습니다: " + city));
                }
                return response.createException();
            })
            .bodyToMono(WeatherResponse.class)
            .retryWhen(Retry.backoff(2, Duration.ofSeconds(1))
                .filter(ex -> ex instanceof WebClientResponseException.ServiceUnavailable))
            .timeout(Duration.ofSeconds(10));
    }
}
```

### 14.5.2 여러 API 동시 호출 (zip)

`Mono.zip()`으로 독립적인 여러 API를 병렬 실행하고 결과를 조합한다.

```java
@Service
@RequiredArgsConstructor
public class DashboardService {

    private final UserClientService userClient;
    private final OrderClientService orderClient;
    private final WeatherClientService weatherClient;

    public Mono<DashboardResponse> getDashboard(String userId) {
        Mono<UserProfile> userMono = userClient.getProfile(userId);
        Mono<List<Order>> ordersMono = orderClient.getRecentOrders(userId).collectList();
        Mono<WeatherResponse> weatherMono = weatherClient.getCurrentWeather("Seoul");

        return Mono.zip(userMono, ordersMono, weatherMono)
            .map(tuple -> DashboardResponse.builder()
                .user(tuple.getT1())
                .recentOrders(tuple.getT2())
                .weather(tuple.getT3())
                .build());
    }
}
```

세 개의 API 호출은 **동시에** 실행된다. 순차 호출 시 각 응답 시간의 합만큼 걸리지만, `Mono.zip()`은 가장 느린 호출 기준으로만 대기한다.

### 14.5.3 여러 API 결과 병합 (merge)

`Flux.merge()`는 여러 소스의 결과를 도착 순서대로 합친다. 동일한 타입의 데이터를 여러 소스에서 수집할 때 유용하다.

```java
public Flux<PriceQuote> getPriceQuotes(String productId) {
    Flux<PriceQuote> a = webClient.get()
        .uri("https://supplier-a.com/api/price/{id}", productId)
        .retrieve().bodyToMono(PriceQuote.class).flux();
    Flux<PriceQuote> b = webClient.get()
        .uri("https://supplier-b.com/api/price/{id}", productId)
        .retrieve().bodyToMono(PriceQuote.class).flux();
    Flux<PriceQuote> c = webClient.get()
        .uri("https://supplier-c.com/api/price/{id}", productId)
        .retrieve().bodyToMono(PriceQuote.class).flux();

    return Flux.merge(a, b, c)
        .timeout(Duration.ofSeconds(5))
        .onErrorResume(ex -> Flux.empty());
}
```

### 14.5.4 순차 API 호출 (flatMap 체이닝)

하나의 API 결과를 다음 API의 입력으로 사용하는 경우 `flatMap`으로 체이닝한다.

```java
// 1. 사용자 조회 → 2. 주문 생성 → 3. 결제 처리
public Mono<PaymentResult> processOrder(String userId, OrderRequest orderRequest) {
    return webClient.get()
        .uri("/api/users/{id}", userId)
        .retrieve()
        .bodyToMono(UserProfile.class)
        .flatMap(user -> {
            orderRequest.setShippingAddress(user.getAddress());
            return webClient.post()
                .uri("/api/orders")
                .bodyValue(orderRequest)
                .retrieve()
                .bodyToMono(OrderResponse.class);
        })
        .flatMap(order -> webClient.post()
            .uri("/api/payments")
            .bodyValue(new PaymentRequest(order.getId(), order.getTotalAmount()))
            .retrieve()
            .bodyToMono(PaymentResult.class));
}
```

### 14.5.5 폴백(Fallback) 패턴

외부 API 실패 시 대체 데이터를 반환한다.

```java
@Slf4j
@Service
@RequiredArgsConstructor
public class ProductService {

    private final WebClient webClient;
    private final ProductRepository productRepository;

    public Mono<Product> getProduct(String id) {
        return webClient.get()
            .uri("/api/products/{id}", id)
            .retrieve().bodyToMono(Product.class)
            .timeout(Duration.ofSeconds(3))
            .onErrorResume(ex -> {
                log.warn("외부 API 실패, 로컬 DB 폴백: {}", ex.getMessage());
                return productRepository.findById(id);
            });
    }

    // 다단계 폴백: 캐시 → 외부 API → 기본값
    public Mono<ExchangeRate> getExchangeRate(String currency) {
        return getFromCache(currency)
            .switchIfEmpty(getFromExternalApi(currency)
                .doOnNext(rate -> saveToCache(currency, rate)))
            .switchIfEmpty(Mono.just(ExchangeRate.defaultRate(currency)))
            .onErrorReturn(ExchangeRate.defaultRate(currency));
    }
}
```

### 14.5.6 페이지네이션 API 전체 조회

`expand()` 연산자로 재귀적으로 다음 페이지를 호출한다.

```java
public Flux<Product> getAllProductsPaginated() {
    return fetchPage(0)
        .expand(page -> page.hasNext()
            ? fetchPage(page.getPage() + 1)
            : Mono.empty())
        .flatMapIterable(PageResponse::getContent);
}

private Mono<PageResponse<Product>> fetchPage(int page) {
    return webClient.get()
        .uri(uriBuilder -> uriBuilder
            .path("/api/products")
            .queryParam("page", page)
            .queryParam("size", 100)
            .build())
        .retrieve()
        .bodyToMono(new ParameterizedTypeReference<PageResponse<Product>>() {});
}
```

---

## 14.6 WebClient 필터와 인터셉터

### 14.6.1 ExchangeFilterFunction과 로깅 필터

`ExchangeFilterFunction`은 `WebClient`의 요청/응답 파이프라인에 횡단 관심사를 추가하는 메커니즘이다. `WebClient.builder().filter()`로 등록하며, 여러 필터를 등록하면 등록 순서대로 체이닝된다.

```java
@Slf4j
public class WebClientFilters {

    public static ExchangeFilterFunction logRequestResponse() {
        return (request, next) -> {
            long startTime = System.currentTimeMillis();
            log.info(">>> {} {}", request.method(), request.url());

            return next.exchange(request)
                .doOnNext(response -> {
                    long duration = System.currentTimeMillis() - startTime;
                    log.info("<<< {} {} - {}ms",
                        response.statusCode(), request.url(), duration);
                });
        };
    }
}
```

### 14.6.2 인증 필터

정적 API 키 필터와 동적 토큰 갱신 필터를 구현한다.

```java
public static ExchangeFilterFunction apiKeyAuth(String apiKey) {
    return (request, next) -> {
        ClientRequest filtered = ClientRequest.from(request)
            .header("X-API-Key", apiKey).build();
        return next.exchange(filtered);
    };
}
```

```java
@Component
@RequiredArgsConstructor
public class DynamicAuthFilter {

    private final TokenService tokenService;

    public ExchangeFilterFunction authFilter() {
        return (request, next) ->
            tokenService.getValidToken()
                .flatMap(token -> {
                    ClientRequest filtered = ClientRequest.from(request)
                        .header(HttpHeaders.AUTHORIZATION, "Bearer " + token)
                        .build();
                    return next.exchange(filtered);
                });
    }
}
```

```java
@Service
public class TokenService {

    private final WebClient authClient;
    private final AtomicReference<TokenInfo> cachedToken = new AtomicReference<>();

    public TokenService(WebClient.Builder builder) {
        this.authClient = builder.baseUrl("https://auth.example.com").build();
    }

    public Mono<String> getValidToken() {
        TokenInfo current = cachedToken.get();
        if (current != null && !current.isExpired()) {
            return Mono.just(current.getAccessToken());
        }
        return authClient.post().uri("/oauth/token")
            .contentType(MediaType.APPLICATION_FORM_URLENCODED)
            .body(BodyInserters.fromFormData("grant_type", "client_credentials")
                .with("client_id", "my-client").with("client_secret", "my-secret"))
            .retrieve().bodyToMono(TokenInfo.class)
            .doOnNext(cachedToken::set).map(TokenInfo::getAccessToken);
    }
}
```

### 14.6.3 에러 처리 필터와 요청 ID 전파 필터

```java
public static ExchangeFilterFunction errorHandlingFilter() {
    return (request, next) -> next.exchange(request)
        .flatMap(response -> {
            if (response.statusCode().is5xxServerError()) {
                return response.bodyToMono(String.class)
                    .flatMap(body -> Mono.error(new ExternalServiceException(
                        "서버 에러 [" + request.method() + " " + request.url() + "]: " + body)));
            }
            return Mono.just(response);
        });
}

public static ExchangeFilterFunction traceIdFilter() {
    return (request, next) -> {
        String traceId = Optional.ofNullable(MDC.get("traceId"))
            .orElse(UUID.randomUUID().toString().substring(0, 8));
        ClientRequest filtered = ClientRequest.from(request)
            .header("X-Trace-Id", traceId).build();
        return next.exchange(filtered);
    };
}
```

### 14.6.4 필터 조합과 적용

여러 필터를 조합하여 적용하는 전체 예제다.

```java
@Configuration
@RequiredArgsConstructor
public class WebClientConfig {

    private final DynamicAuthFilter dynamicAuthFilter;

    @Value("${external.api.base-url}")
    private String baseUrl;

    @Bean
    public WebClient webClient() {
        HttpClient httpClient = HttpClient.create()
            .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000)
            .responseTimeout(Duration.ofSeconds(10))
            .doOnConnected(conn -> conn
                .addHandlerLast(new ReadTimeoutHandler(10, TimeUnit.SECONDS))
                .addHandlerLast(new WriteTimeoutHandler(10, TimeUnit.SECONDS)));

        return WebClient.builder()
            .baseUrl(baseUrl)
            .clientConnector(new ReactorClientHttpConnector(httpClient))
            .codecs(c -> c.defaultCodecs().maxInMemorySize(5 * 1024 * 1024))
            // 필터 순서: 추적 → 인증 → 로깅 → 에러 처리
            .filter(WebClientFilters.traceIdFilter())
            .filter(dynamicAuthFilter.authFilter())
            .filter(WebClientFilters.logRequestResponse())
            .filter(WebClientFilters.errorHandlingFilter())
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .build();
    }
}
```

필터 등록 순서가 곧 실행 순서다. 권장 순서는 추적 -> 인증 -> 로깅 -> 에러 처리 순이다.

### 14.6.5 테스트에서의 WebClient 모킹

`MockWebServer`로 외부 API를 모킹하여 테스트한다.

```groovy
testImplementation 'com.squareup.okhttp3:mockwebserver:4.12.0'
```

```java
class ProductClientServiceTest {

    private MockWebServer mockWebServer;
    private ProductClientService service;

    @BeforeEach
    void setUp() throws IOException {
        mockWebServer = new MockWebServer();
        mockWebServer.start();
        service = new ProductClientService(
            WebClient.builder().baseUrl(mockWebServer.url("/").toString()).build());
    }

    @AfterEach
    void tearDown() throws IOException { mockWebServer.shutdown(); }

    @Test
    void getProduct_성공() {
        mockWebServer.enqueue(new MockResponse()
            .setBody("{\"id\":\"123\",\"name\":\"테스트 상품\",\"price\":10000}")
            .addHeader("Content-Type", "application/json"));

        StepVerifier.create(service.getProduct("123"))
            .assertNext(p -> assertThat(p.getName()).isEqualTo("테스트 상품"))
            .verifyComplete();
    }

    @Test
    void getProduct_재시도_후_성공() {
        // 처음 두 번은 503, 세 번째는 성공
        mockWebServer.enqueue(new MockResponse().setResponseCode(503));
        mockWebServer.enqueue(new MockResponse().setResponseCode(503));
        mockWebServer.enqueue(new MockResponse()
            .setBody("{\"id\":\"123\",\"name\":\"상품\",\"price\":5000}")
            .addHeader("Content-Type", "application/json"));

        StepVerifier.create(service.getProductWithBackoff("123"))
            .assertNext(p -> assertThat(p.getId()).isEqualTo("123"))
            .verifyComplete();
        assertThat(mockWebServer.getRequestCount()).isEqualTo(3);
    }
}
```

---

## 요약

| 주제 | 핵심 내용 |
|------|----------|
| **WebClient 설정** | `WebClient.builder()`로 빈 생성, 커넥션 풀(`ConnectionProvider`), 코덱(`maxInMemorySize`, Jackson) 설정 |
| **요청/응답 처리** | GET/POST/PUT/DELETE, `retrieve()` vs `exchangeToMono()`, `bodyToMono`/`bodyToFlux`, 스트리밍 |
| **에러 핸들링** | `onStatus()`로 상태 코드별 처리, `onErrorResume()`으로 폴백, 서킷 브레이커로 장애 전파 차단 |
| **재시도 전략** | `Retry.backoff()`로 지수 백오프, `jitter`로 부하 분산, `filter()`로 재시도 대상 예외 선별 |
| **타임아웃** | 커넥션/읽기/쓰기/응답 타임아웃 계층별 설정, Reactor `timeout()`으로 전체 체인 시간 제한 |
| **외부 API 연동** | `Mono.zip()`으로 병렬 호출, `Flux.merge()`로 결과 병합, 폴백 패턴, 페이지네이션 순회 |
| **필터** | `ExchangeFilterFunction`으로 로깅/인증/에러 처리/추적 필터 구현, 필터 체이닝 순서 |

다음 장에서는 R2DBC를 활용하여 관계형 데이터베이스를 리액티브 방식으로 접근하고, MongoDB와 함께 멀티 데이터소스를 구성하는 방법을 다룬다.


---

# Chapter 15. R2DBC와의 통합 (보너스)

지금까지 이 책에서는 MongoDB를 중심으로 리액티브 데이터 접근을 다루었다. 하지만 실무에서는 관계형 데이터베이스(RDBMS)와 함께 사용해야 하는 상황이 빈번하다. 예를 들어 사용자 인증과 결제 정보는 PostgreSQL에, 상품 카탈로그와 리뷰는 MongoDB에 저장하는 아키텍처가 대표적이다. 이번 장에서는 리액티브 환경에서 관계형 DB에 접근하기 위한 **R2DBC(Reactive Relational Database Connectivity)**를 소개하고, MongoDB와 R2DBC를 동시에 사용하는 **멀티 데이터소스** 구성 방법을 실전 예제와 함께 다룬다.

---

## 15.1 R2DBC란?

### 15.1.1 R2DBC 소개

R2DBC는 **Reactive Relational Database Connectivity**의 약자로, 관계형 데이터베이스에 대한 비동기/논블로킹 접근을 제공하는 SPI(Service Provider Interface) 명세다. 전통적인 JDBC가 블로킹 I/O 기반으로 설계된 반면, R2DBC는 Reactive Streams 표준을 기반으로 처음부터 논블로킹으로 설계되었다.

| 원칙 | 설명 |
|------|------|
| **완전한 논블로킹** | 데이터베이스 연결, 쿼리 실행, 결과 처리 모든 과정이 논블로킹 |
| **Reactive Streams 기반** | `Publisher`, `Subscriber` 패턴을 사용하여 배압(Backpressure) 지원 |
| **SPI 명세** | 드라이버 제공자가 구현하는 인터페이스 규격 |
| **SQL 중심** | ORM이 아닌 SQL 기반 접근 (Spring Data R2DBC가 리포지토리 추상화 제공) |

### 15.1.2 JDBC vs R2DBC

| 구분 | JDBC | R2DBC |
|------|------|-------|
| **I/O 모델** | 블로킹 | 논블로킹 |
| **스레드 모델** | 요청당 스레드 점유 | 이벤트 루프 기반 |
| **반환 타입** | `ResultSet`, `List<T>` | `Mono<T>`, `Flux<T>` |
| **배압 지원** | 없음 | Reactive Streams 기반 지원 |
| **트랜잭션** | `ThreadLocal` 기반 | Reactor Context 기반 |
| **커넥션 풀** | HikariCP 등 | `r2dbc-pool` |
| **Spring 통합** | Spring Data JPA | Spring Data R2DBC |

JDBC 기반의 `JdbcTemplate`이나 JPA를 WebFlux 환경에서 사용하면 이벤트 루프 스레드가 블로킹되어 전체 애플리케이션의 처리량이 급격히 저하된다. R2DBC는 이 문제를 근본적으로 해결한다.

```
[JDBC + WebFlux]
이벤트 루프 스레드 → DB 쿼리 실행(블로킹) → 스레드 대기 → 처리량 저하

[R2DBC + WebFlux]
이벤트 루프 스레드 → DB 쿼리 요청(논블로킹) → 다른 요청 처리 → 결과 도착 시 콜백
```

### 15.1.3 지원 데이터베이스와 의존성 설정

R2DBC는 SPI 명세이므로, 각 데이터베이스 벤더 또는 커뮤니티가 드라이버를 제공한다.

| 데이터베이스 | Maven/Gradle Artifact |
|-------------|----------------------|
| **PostgreSQL** | `org.postgresql:r2dbc-postgresql` |
| **MySQL** | `io.asyncer:r2dbc-mysql` |
| **MariaDB** | `org.mariadb:r2dbc-mariadb` |
| **H2** | `io.r2dbc:r2dbc-h2` |
| **Oracle** | `com.oracle.database.r2dbc:oracle-r2dbc` |

이 장에서는 가장 널리 사용되는 **PostgreSQL**을 기준으로 설명한다. `build.gradle`에 R2DBC 관련 의존성을 추가한다.

```groovy
dependencies {
    // 기존 의존성
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    implementation 'org.springframework.boot:spring-boot-starter-data-mongodb-reactive'

    // R2DBC 의존성 추가
    implementation 'org.springframework.boot:spring-boot-starter-data-r2dbc'
    implementation 'org.postgresql:r2dbc-postgresql'

    // Flyway (스키마 마이그레이션) - R2DBC에서는 JDBC 드라이버도 필요
    implementation 'org.flywaydb:flyway-core'
    implementation 'org.flywaydb:flyway-database-postgresql'
    runtimeOnly 'org.postgresql:postgresql'

    testImplementation 'io.r2dbc:r2dbc-h2'
}
```

> **참고**: Flyway 같은 스키마 마이그레이션 도구는 아직 R2DBC를 직접 지원하지 않으므로, 마이그레이션 실행 시에만 JDBC 드라이버가 필요하다. Spring Boot는 시작 시 JDBC 드라이버로 마이그레이션을 수행한 후, 런타임에는 R2DBC 드라이버를 사용한다.

### 15.1.4 Spring Data R2DBC의 핵심 구성 요소

| 구성 요소 | 설명 |
|----------|------|
| `ReactiveCrudRepository` | 기본 CRUD 연산을 제공하는 리포지토리 인터페이스 |
| `R2dbcEntityTemplate` | `ReactiveMongoTemplate`에 대응하는 저수준 템플릿 |
| `@Table`, `@Id`, `@Column` | 엔티티 매핑 어노테이션 (`@Entity`는 사용하지 않음) |
| `DatabaseClient` | SQL을 직접 작성하여 실행하는 저수준 클라이언트 |
| `R2dbcTransactionManager` | 리액티브 트랜잭션 관리자 |

MongoDB의 `ReactiveMongoRepository`를 사용해본 개발자라면 R2DBC 리포지토리도 거의 동일한 방식으로 사용할 수 있다.

```java
// MongoDB 리포지토리 (이미 익숙한 패턴)
public interface ProductRepository
        extends ReactiveMongoRepository<Product, String> {
    Flux<Product> findByCategory(String category);
}

// R2DBC 리포지토리 (거의 동일한 패턴)
public interface PaymentRepository
        extends ReactiveCrudRepository<Payment, Long> {
    Flux<Payment> findByUserId(Long userId);
}
```

---

## 15.2 MongoDB + R2DBC(관계형 DB) 멀티 데이터소스 구성

### 15.2.1 아키텍처 설계

멀티 데이터소스 아키텍처에서 각 데이터베이스의 역할을 명확히 나누는 것이 중요하다.

```
┌─────────────────────────────────────────────────┐
│                   Spring WebFlux                 │
│                                                  │
│  ┌──────────────┐         ┌──────────────────┐  │
│  │  R2DBC Layer │         │  MongoDB Layer   │  │
│  │ - 사용자     │         │ - 상품 카탈로그  │  │
│  │ - 주문/결제  │         │ - 상품 리뷰      │  │
│  │ - 재고       │         │ - 활동 로그      │  │
│  └──────┬───────┘         └────────┬─────────┘  │
└─────────┼──────────────────────────┼─────────────┘
          │                          │
    ┌─────▼─────┐             ┌──────▼──────┐
    │ PostgreSQL │             │   MongoDB   │
    └───────────┘             └─────────────┘
```

| PostgreSQL (R2DBC) | MongoDB |
|---------------------|---------|
| 강한 일관성, ACID 트랜잭션 필수 | 유연한 스키마, 비정형 데이터 |
| 복잡한 조인이 필요한 데이터 | 높은 쓰기 처리량이 필요한 데이터 |
| 예: 사용자, 주문, 결제, 재고 | 예: 상품 카탈로그, 리뷰, 로그 |

### 15.2.2 application.yml 두 데이터소스 설정

```yaml
spring:
  # MongoDB 설정
  data:
    mongodb:
      uri: mongodb://localhost:27017/shopdb
      auto-index-creation: true

  # R2DBC (PostgreSQL) 설정
  r2dbc:
    url: r2dbc:postgresql://localhost:5432/shopdb
    username: shopuser
    password: ${DB_PASSWORD:shoppass}
    pool:
      initial-size: 5
      max-size: 20
      max-idle-time: 30m

  # Flyway (JDBC 기반 마이그레이션)
  flyway:
    enabled: true
    url: jdbc:postgresql://localhost:5432/shopdb
    user: shopuser
    password: ${DB_PASSWORD:shoppass}
    locations: classpath:db/migration
```

### 15.2.3 Flyway 스키마 마이그레이션

R2DBC는 관계형 DB를 사용하므로 테이블 스키마를 사전에 정의해야 한다. `src/main/resources/db/migration/V1__init.sql` 파일을 작성한다.

```sql
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        VARCHAR(20)  NOT NULL DEFAULT 'USER',
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT       NOT NULL REFERENCES users(id),
    order_number    VARCHAR(30)  NOT NULL UNIQUE,
    status          VARCHAR(20)  NOT NULL DEFAULT 'PENDING',
    total_amount    DECIMAL(12,2) NOT NULL,
    shipping_address TEXT,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
    id          BIGSERIAL PRIMARY KEY,
    order_id    BIGINT       NOT NULL REFERENCES orders(id),
    product_id  VARCHAR(50)  NOT NULL,  -- MongoDB ObjectId 참조
    product_name VARCHAR(200) NOT NULL,
    quantity    INT          NOT NULL,
    unit_price  DECIMAL(10,2) NOT NULL,
    subtotal    DECIMAL(12,2) NOT NULL
);

CREATE TABLE payments (
    id              BIGSERIAL PRIMARY KEY,
    order_id        BIGINT       NOT NULL REFERENCES orders(id),
    payment_method  VARCHAR(30)  NOT NULL,
    amount          DECIMAL(12,2) NOT NULL,
    status          VARCHAR(20)  NOT NULL DEFAULT 'PENDING',
    transaction_id  VARCHAR(100),
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

### 15.2.4 MongoDB/R2DBC 설정 클래스

두 데이터소스의 리포지토리 스캔 경로를 분리한다.

```java
@Configuration
@EnableR2dbcRepositories(basePackages = "com.example.shop.repository.r2dbc")
public class R2dbcConfig extends AbstractR2dbcConfiguration {

    @Value("${spring.r2dbc.url}")
    private String url;

    @Value("${spring.r2dbc.username}")
    private String username;

    @Value("${spring.r2dbc.password}")
    private String password;

    @Override
    @Bean
    public ConnectionFactory connectionFactory() {
        return ConnectionFactories.get(ConnectionFactoryOptions.builder()
            .from(ConnectionFactoryOptions.parse(url))
            .option(ConnectionFactoryOptions.USER, username)
            .option(ConnectionFactoryOptions.PASSWORD, password)
            .build());
    }

    @Bean
    public ReactiveTransactionManager transactionManager(
            ConnectionFactory connectionFactory) {
        return new R2dbcTransactionManager(connectionFactory);
    }
}
```

```java
@Configuration
@EnableReactiveMongoRepositories(
    basePackages = "com.example.shop.repository.mongo"
)
public class MongoConfig extends AbstractReactiveMongoConfiguration {

    @Value("${spring.data.mongodb.uri}")
    private String mongoUri;

    @Override
    protected String getDatabaseName() {
        return "shopdb";
    }

    @Override
    @Bean
    public MongoClient reactiveMongoClient() {
        return MongoClients.create(mongoUri);
    }

    @Bean
    public ReactiveMongoTransactionManager mongoTransactionManager(
            ReactiveMongoDatabaseFactory dbFactory) {
        return new ReactiveMongoTransactionManager(dbFactory);
    }
}
```

### 15.2.5 패키지 구조

멀티 데이터소스를 사용할 때 패키지 구조를 명확히 분리하는 것이 유지보수에 유리하다.

```
com.example.shop
├── config
│   ├── R2dbcConfig.java
│   └── MongoConfig.java
├── domain
│   ├── rdb                         # R2DBC 엔티티
│   │   ├── UserEntity.java
│   │   ├── OrderEntity.java
│   │   └── OrderItemEntity.java
│   └── mongo                       # MongoDB 도큐먼트
│       ├── Product.java
│       └── Review.java
├── repository
│   ├── r2dbc                       # R2DBC 리포지토리
│   │   ├── UserRepository.java
│   │   └── OrderRepository.java
│   └── mongo                       # MongoDB 리포지토리
│       ├── ProductRepository.java
│       └── ReviewRepository.java
├── service
└── controller
```

### 15.2.6 엔티티와 도큐먼트 정의

R2DBC 엔티티는 `@Table`, `@Id`, `@Column` 어노테이션을 사용한다.

```java
@Table("orders")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class OrderEntity {

    @Id
    private Long id;

    @Column("user_id")
    private Long userId;

    @Column("order_number")
    private String orderNumber;

    private String status;

    @Column("total_amount")
    private BigDecimal totalAmount;

    @Column("shipping_address")
    private String shippingAddress;

    @Column("created_at")
    private LocalDateTime createdAt;
}
```

MongoDB 도큐먼트는 유연한 스키마의 장점을 활용한다.

```java
@Document(collection = "products")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Product {

    @Id
    private String id;
    private String name;
    private String description;
    private String category;
    private BigDecimal price;
    private int stockQuantity;
    private List<String> tags;
    private Map<String, String> attributes;  // 유연한 속성
    private LocalDateTime createdAt;
}
```

### 15.2.7 각 리포지토리

두 데이터소스의 리포지토리를 패키지별로 분리하여 정의한다.

```java
// R2DBC 리포지토리 (com.example.shop.repository.r2dbc)
public interface OrderRepository extends ReactiveCrudRepository<OrderEntity, Long> {
    Flux<OrderEntity> findByUserIdOrderByCreatedAtDesc(Long userId);
    Mono<OrderEntity> findByOrderNumber(String orderNumber);
}

public interface OrderItemRepository
        extends ReactiveCrudRepository<OrderItemEntity, Long> {
    Flux<OrderItemEntity> findByOrderId(Long orderId);
}
```

```java
// MongoDB 리포지토리 (com.example.shop.repository.mongo)
public interface ProductRepository
        extends ReactiveMongoRepository<Product, String> {
    Flux<Product> findByCategory(String category);

    @Query("{ 'price': { '$gte': ?0, '$lte': ?1 } }")
    Flux<Product> findByPriceRange(BigDecimal minPrice, BigDecimal maxPrice);
}

public interface ReviewRepository
        extends ReactiveMongoRepository<Review, String> {
    Flux<Review> findByProductIdOrderByCreatedAtDesc(String productId);
    Mono<Long> countByProductId(String productId);
}
```

---

## 15.3 리액티브 환경에서 여러 데이터소스 조합하기

### 15.3.1 데이터 조합 패턴

두 데이터소스의 데이터를 조합할 때 Reactor의 연산자를 활용한다.

**패턴 1: 순차 조합 (flatMap)** -- 한쪽 결과를 기반으로 다른 데이터소스를 조회한다.

```java
@Service
@RequiredArgsConstructor
public class OrderQueryService {

    private final OrderRepository orderRepository;         // R2DBC
    private final OrderItemRepository orderItemRepository; // R2DBC
    private final ProductRepository productRepository;     // MongoDB

    public Mono<OrderDetailResponse> getOrderDetail(Long orderId) {
        return orderRepository.findById(orderId)
            .switchIfEmpty(Mono.error(
                new NotFoundException("주문을 찾을 수 없습니다: " + orderId)))
            .flatMap(order -> orderItemRepository.findByOrderId(orderId)
                .flatMap(item -> productRepository.findById(item.getProductId())
                    .map(product -> OrderItemDetail.builder()
                        .productName(product.getName())
                        .category(product.getCategory())
                        .quantity(item.getQuantity())
                        .unitPrice(item.getUnitPrice())
                        .build()))
                .collectList()
                .map(items -> OrderDetailResponse.builder()
                    .orderId(order.getId())
                    .orderNumber(order.getOrderNumber())
                    .status(order.getStatus())
                    .totalAmount(order.getTotalAmount())
                    .items(items)
                    .createdAt(order.getCreatedAt())
                    .build()));
    }
}
```

**패턴 2: 병렬 조합 (zip)** -- 서로 독립적인 데이터를 병렬로 조회하여 조합한다.

```java
public Mono<ProductPageResponse> getProductPage(String productId) {
    Mono<Product> productMono = productRepository.findById(productId)
        .switchIfEmpty(Mono.error(
            new NotFoundException("상품을 찾을 수 없습니다: " + productId)));

    Mono<List<Review>> reviewsMono = reviewRepository
        .findByProductIdOrderByCreatedAtDesc(productId)
        .collectList();

    Mono<Long> reviewCountMono = reviewRepository.countByProductId(productId);

    return Mono.zip(productMono, reviewsMono, reviewCountMono)
        .map(tuple -> ProductPageResponse.builder()
            .product(tuple.getT1())
            .reviews(tuple.getT2())
            .totalReviews(tuple.getT3())
            .build());
}
```

### 15.3.2 트랜잭션 주의사항

멀티 데이터소스 환경에서 트랜잭션은 가장 까다로운 부분이다.

**원칙 1: 각 데이터소스의 트랜잭션은 독립적이다**

```java
// 이 코드는 PostgreSQL 트랜잭션만 보장한다.
// MongoDB 저장이 실패해도 PostgreSQL 변경은 롤백되지 않는다!
@Transactional  // R2dbcTransactionManager가 기본으로 동작
public Mono<Order> createOrder(OrderRequest request) {
    return orderRepository.save(orderEntity)           // PostgreSQL - 트랜잭션 O
        .flatMap(order ->
            productRepository.save(updatedProduct)     // MongoDB - 트랜잭션 X
                .thenReturn(order));
}
```

**원칙 2: 트랜잭션 매니저를 명시적으로 지정한다**

```java
// PostgreSQL 트랜잭션 사용
@Transactional("transactionManager")
public Mono<OrderEntity> saveOrder(OrderEntity order) {
    return orderRepository.save(order);
}

// MongoDB 트랜잭션 사용
@Transactional("mongoTransactionManager")
public Mono<Product> updateProduct(Product product) {
    return productRepository.save(product);
}
```

**원칙 3: 보상 트랜잭션(Saga) 패턴을 활용한다**

두 데이터소스에 걸친 작업에서 일관성을 보장하려면 Saga 패턴을 적용한다. 한쪽이 실패하면 이미 성공한 다른 쪽의 변경을 보상(되돌리기)하는 방식이다.

### 15.3.3 실전 예제: 주문 시스템 (Saga 패턴)

재고 차감(MongoDB) -> 주문 생성(PostgreSQL) -> 결제 처리(PostgreSQL) 순서로 진행하며, 각 단계 실패 시 이전 단계를 보상하는 서비스를 구현한다.

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderSagaService {

    private final OrderRepository orderRepository;
    private final OrderItemRepository orderItemRepository;
    private final ProductRepository productRepository;
    private final PaymentRepository paymentRepository;

    /**
     * 보상 트랜잭션 패턴:
     * 1. 재고 차감 (MongoDB) -> 실패 시 즉시 에러
     * 2. 주문 생성 (PostgreSQL) -> 실패 시 재고 복원
     * 3. 결제 처리 (PostgreSQL) -> 실패 시 주문 취소 + 재고 복원
     */
    public Mono<OrderResult> placeOrder(Long userId, OrderRequest request) {
        return decreaseStock(request.getItems())
            .then(createOrderInDb(userId, request))
            .flatMap(order -> processPayment(order, request)
                .thenReturn(order)
                .onErrorResume(paymentError -> {
                    log.error("결제 실패, 보상 시작", paymentError);
                    return cancelOrder(order)
                        .then(restoreStock(request.getItems()))
                        .then(Mono.error(new PaymentException(
                            "결제 처리에 실패했습니다.", paymentError)));
                }))
            .onErrorResume(orderError -> {
                if (!(orderError instanceof PaymentException)) {
                    log.error("주문 생성 실패, 재고 복원", orderError);
                    return restoreStock(request.getItems())
                        .then(Mono.error(new OrderException(
                            "주문 생성에 실패했습니다.", orderError)));
                }
                return Mono.error(orderError);
            })
            .map(order -> OrderResult.builder()
                .orderId(order.getId())
                .orderNumber(order.getOrderNumber())
                .status("COMPLETED")
                .build());
    }

    private Mono<Void> decreaseStock(List<OrderItemRequest> items) {
        return Flux.fromIterable(items)
            .flatMap(item -> productRepository.findById(item.getProductId())
                .switchIfEmpty(Mono.error(new NotFoundException(
                    "상품을 찾을 수 없습니다: " + item.getProductId())))
                .flatMap(product -> {
                    if (product.getStockQuantity() < item.getQuantity()) {
                        return Mono.error(new InsufficientStockException(
                            product.getName() + " 재고가 부족합니다."));
                    }
                    product.setStockQuantity(
                        product.getStockQuantity() - item.getQuantity());
                    return productRepository.save(product);
                }))
            .then();
    }

    private Mono<Void> restoreStock(List<OrderItemRequest> items) {
        return Flux.fromIterable(items)
            .flatMap(item -> productRepository.findById(item.getProductId())
                .flatMap(product -> {
                    product.setStockQuantity(
                        product.getStockQuantity() + item.getQuantity());
                    return productRepository.save(product);
                }))
            .then();
    }

    private Mono<OrderEntity> createOrderInDb(Long userId, OrderRequest request) {
        OrderEntity order = OrderEntity.builder()
            .userId(userId)
            .orderNumber("ORD-" + System.currentTimeMillis())
            .status("PENDING")
            .totalAmount(request.calculateTotalAmount())
            .shippingAddress(request.getShippingAddress())
            .createdAt(LocalDateTime.now())
            .build();

        return orderRepository.save(order)
            .flatMap(savedOrder -> {
                List<OrderItemEntity> orderItems = request.getItems().stream()
                    .map(item -> OrderItemEntity.builder()
                        .orderId(savedOrder.getId())
                        .productId(item.getProductId())
                        .productName(item.getProductName())
                        .quantity(item.getQuantity())
                        .unitPrice(item.getUnitPrice())
                        .subtotal(item.getUnitPrice()
                            .multiply(BigDecimal.valueOf(item.getQuantity())))
                        .build())
                    .toList();
                return orderItemRepository.saveAll(orderItems)
                    .then(Mono.just(savedOrder));
            });
    }

    private Mono<Void> processPayment(OrderEntity order, OrderRequest request) {
        PaymentEntity payment = PaymentEntity.builder()
            .orderId(order.getId())
            .paymentMethod(request.getPaymentMethod())
            .amount(order.getTotalAmount())
            .status("COMPLETED")
            .transactionId("TXN-" + UUID.randomUUID())
            .createdAt(LocalDateTime.now())
            .build();
        return paymentRepository.save(payment).then();
    }

    private Mono<Void> cancelOrder(OrderEntity order) {
        order.setStatus("CANCELLED");
        return orderRepository.save(order).then();
    }
}
```

### 15.3.4 컨트롤러 구현

```java
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderSagaService orderSagaService;
    private final OrderQueryService orderQueryService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<OrderResult> placeOrder(
            @AuthenticationPrincipal Mono<UserDetails> principal,
            @Valid @RequestBody OrderRequest request) {
        return principal.flatMap(user -> {
            Long userId = Long.parseLong(user.getUsername());
            return orderSagaService.placeOrder(userId, request);
        });
    }

    @GetMapping("/{orderId}")
    public Mono<OrderDetailResponse> getOrderDetail(@PathVariable Long orderId) {
        return orderQueryService.getOrderDetail(orderId);
    }

    @GetMapping("/my")
    public Flux<OrderSummaryResponse> getMyOrders(
            @AuthenticationPrincipal Mono<UserDetails> principal) {
        return principal.flatMapMany(user -> {
            Long userId = Long.parseLong(user.getUsername());
            return orderQueryService.getUserOrders(userId);
        });
    }
}
```

### 15.3.5 DatabaseClient를 활용한 복잡한 쿼리

Spring Data R2DBC의 메서드 이름 기반 쿼리로 부족할 때, `DatabaseClient`로 SQL을 직접 작성한다.

```java
@Repository
@RequiredArgsConstructor
public class OrderCustomRepository {

    private final DatabaseClient databaseClient;

    public Flux<SalesStatistics> getSalesStatistics(
            LocalDateTime from, LocalDateTime to) {
        String sql = """
            SELECT DATE(o.created_at) AS sale_date,
                   COUNT(o.id) AS order_count,
                   SUM(o.total_amount) AS total_sales
            FROM orders o
            WHERE o.status = 'COMPLETED'
              AND o.created_at BETWEEN :from AND :to
            GROUP BY DATE(o.created_at)
            ORDER BY sale_date DESC
            """;

        return databaseClient.sql(sql)
            .bind("from", from)
            .bind("to", to)
            .map((row, metadata) -> SalesStatistics.builder()
                .saleDate(row.get("sale_date", LocalDate.class))
                .orderCount(row.get("order_count", Long.class))
                .totalSales(row.get("total_sales", BigDecimal.class))
                .build())
            .all();
    }
}
```

### 15.3.6 두 데이터소스 통계 조합

PostgreSQL의 주문 통계와 MongoDB의 상품 상세 정보를 조합하는 대시보드 서비스다.

```java
@Service
@RequiredArgsConstructor
public class DashboardService {

    private final OrderCustomRepository orderCustomRepository;
    private final ProductRepository productRepository;
    private final ReviewRepository reviewRepository;

    public Flux<PopularProductDashboard> getPopularProductDashboard(int limit) {
        return orderCustomRepository.getPopularProducts(limit)
            .flatMap(stats -> {
                Mono<Product> productMono = productRepository
                    .findById(stats.getProductId())
                    .defaultIfEmpty(Product.builder()
                        .id(stats.getProductId())
                        .name(stats.getProductName())
                        .category("UNKNOWN").build());

                Mono<Double> avgRatingMono = reviewRepository
                    .findByProductIdOrderByCreatedAtDesc(stats.getProductId())
                    .map(Review::getRating)
                    .collectList()
                    .map(ratings -> ratings.stream()
                        .mapToInt(Integer::intValue).average().orElse(0.0));

                return Mono.zip(productMono, avgRatingMono)
                    .map(tuple -> PopularProductDashboard.builder()
                        .productId(stats.getProductId())
                        .productName(stats.getProductName())
                        .category(tuple.getT1().getCategory())
                        .totalQuantitySold(stats.getTotalQuantity())
                        .averageRating(tuple.getT2())
                        .build());
            });
    }
}
```

### 15.3.7 멀티 데이터소스 환경의 베스트 프랙티스

**1. 데이터 비정규화로 정합성 관리**

```java
// 올바른 패턴: 주문 시점의 상품 정보를 비정규화하여 저장
@Table("order_items")
public class OrderItemEntity {
    private String productId;     // MongoDB ObjectId 참조
    private String productName;   // 비정규화 (주문 시점 상품명)
    private BigDecimal unitPrice; // 비정규화 (주문 시점 가격)
}
```

**2. 에러 처리 통합**

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public Mono<ErrorResponse> handleDataIntegrity(
            DataIntegrityViolationException ex) {
        return Mono.just(ErrorResponse.of("DATA_CONFLICT",
            "데이터 무결성 위반이 발생했습니다."));
    }

    @ExceptionHandler(DuplicateKeyException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public Mono<ErrorResponse> handleDuplicateKey(DuplicateKeyException ex) {
        return Mono.just(ErrorResponse.of("DUPLICATE_KEY",
            "중복된 데이터가 존재합니다."));
    }
}
```

**3. 헬스 체크 통합**

```java
@Component
@RequiredArgsConstructor
public class MultiDataSourceHealthIndicator
        implements ReactiveHealthIndicator {

    private final ConnectionFactory connectionFactory;
    private final ReactiveMongoTemplate mongoTemplate;

    @Override
    public Mono<Health> health() {
        Mono<String> r2dbcHealth = Mono.from(connectionFactory.create())
            .flatMap(conn -> Mono.from(conn.createStatement("SELECT 1")
                .execute())
                .flatMap(result -> Mono.from(result.map((row, meta) -> "UP")))
                .doFinally(signal -> conn.close()))
            .onErrorReturn("DOWN");

        Mono<String> mongoHealth = mongoTemplate.executeCommand("{ ping: 1 }")
            .map(doc -> "UP")
            .onErrorReturn("DOWN");

        return Mono.zip(r2dbcHealth, mongoHealth)
            .map(tuple -> {
                boolean allUp = "UP".equals(tuple.getT1())
                             && "UP".equals(tuple.getT2());
                return (allUp ? Health.up() : Health.down())
                    .withDetail("postgresql", tuple.getT1())
                    .withDetail("mongodb", tuple.getT2())
                    .build();
            });
    }
}
```

### 15.3.8 주의사항 정리

| 함정 | 대응 방법 |
|------|----------|
| **분산 트랜잭션 불가**: `@Transactional` 하나로 두 DB를 묶을 수 없음 | Saga 패턴, 보상 트랜잭션 |
| **참조 무결성 부재**: 두 DB 간 외래 키 제약 없음 | 비정규화, 방어적 코딩, 정기 정합성 검증 배치 |
| **트랜잭션 매니저 충돌**: 기본 `@Transactional`이 어느 매니저를 쓸지 모호 | `@Transactional("매니저명")` 명시 |
| **N+1 쿼리**: 두 데이터소스 조합 시 반복 조회 발생 | `collectList()` 후 일괄 조회, 캐싱 |
| **에러 타입 혼재**: R2DBC와 MongoDB가 다른 예외 체계 사용 | 통합 예외 핸들러, 비즈니스 예외로 래핑 |
| **스키마 관리**: R2DBC는 DDL 자동 생성 미지원 | Flyway 또는 Liquibase 사용 |

---

## 요약

이번 장에서는 리액티브 환경에서 관계형 데이터베이스에 접근하기 위한 R2DBC를 소개하고, MongoDB와 함께 사용하는 멀티 데이터소스 아키텍처를 다루었다.

| 주제 | 핵심 내용 |
|------|----------|
| **R2DBC 소개** | JDBC의 리액티브 대안, Reactive Streams 기반 논블로킹 DB 접근 |
| **JDBC vs R2DBC** | 블로킹 vs 논블로킹, ThreadLocal vs Reactor Context 기반 트랜잭션 |
| **멀티 데이터소스 구성** | 패키지 분리, 설정 클래스 분리, 리포지토리 스캔 경로 분리 |
| **데이터 조합** | `flatMap`(순차), `zip`(병렬)을 활용한 조합 패턴 |
| **트랜잭션 관리** | 분산 트랜잭션 불가, Saga 패턴과 보상 트랜잭션으로 대응 |
| **실전 예제** | 주문 시스템 -- 재고 차감(MongoDB) + 주문 생성(PostgreSQL) + 결제 처리 |

R2DBC는 WebFlux 기반 애플리케이션에서 관계형 데이터베이스를 사용할 때 유일한 리액티브 선택지다. MongoDB와 함께 사용하면 각 데이터베이스의 장점을 최대한 활용할 수 있지만, 분산 트랜잭션과 데이터 정합성에 대한 신중한 설계가 필요하다.

다음 장에서는 리액티브 테스트 전략을 다루며, StepVerifier와 WebTestClient를 활용한 테스트 작성법을 살펴본다.
