# Chapter 12. Server-Sent Events (SSE)

웹 애플리케이션을 개발하다 보면 서버에서 클라이언트에게 실시간으로 데이터를 보내야 하는 상황이 자주 나온다. 주식 시세 업데이트, 사용자 알림, 라이브 피드, 대시보드 변경 감지 같은 기능들이 좋은 예시다. 이 장에서는 이런 요구사항을 해결하는 Server-Sent Events(SSE) 기술을 깊이 있게 살펴본다. SSE 프로토콜의 동작 원리부터 시작해서, Spring WebFlux의 `Flux`를 이용한 SSE 엔드포인트 구현, 실시간 알림 시스템을 Sinks로 만드는 방법, 그리고 MongoDB Change Streams와 SSE를 조합하여 데이터 변경을 실시간으로 감지하고 전달하는 기법까지 실무에서 바로 활용할 수 있는 패턴들을 다룬다.

---

## 12.1 SSE란 무엇인가?

### 12.1.1 SSE 프로토콜 개요

Server-Sent Events(SSE)는 HTTP 위에서 서버가 클라이언트로 단방향 실시간 데이터를 보내는 표준 프로토콜이다. W3C에서 HTML5 표준으로 정의했고, 모던 브라우저들이 `EventSource` API를 통해 기본 지원하고 있다.

SSE를 이해하기 위해 몇 가지 특징을 짚고 넘어가자.

- **단방향 통신**: 서버에서 클라이언트로만 데이터를 전송한다. 클라이언트가 서버로 데이터를 보내려면 별도의 HTTP 요청을 사용한다.
- **HTTP 기반**: 일반 HTTP/1.1 또는 HTTP/2 위에서 동작하므로 별도의 프로토콜이 필요 없다.
- **자동 재연결**: 연결이 끊어지면 브라우저가 자동으로 재연결을 시도한다.
- **이벤트 ID 지원**: 마지막으로 수신한 이벤트 ID를 기억하여, 재연결 시 놓친 이벤트를 복구할 수 있다.
- **텍스트 기반**: `text/event-stream` MIME 타입을 사용하며, UTF-8 인코딩 텍스트로 데이터를 전송한다.

### 12.1.2 SSE 메시지 형식

SSE 메시지 형식은 매우 간단하다. 텍스트 줄들로 이루어져 있고, 각 필드는 콜론으로 분리된다.

```
id: 1
event: notification
data: {"message": "새 댓글이 등록되었습니다.", "postId": "abc123"}
retry: 5000

```

각 필드가 무엇을 하는지 살펴보면 이렇다.

| 필드 | 설명 | 기본값 |
|------|------|--------|
| `id` | 이벤트 고유 식별자. 재연결 시 `Last-Event-ID` 헤더로 전송됨 | 없음 |
| `event` | 이벤트 타입. 클라이언트에서 `addEventListener`로 특정 타입만 수신 가능 | `message` |
| `data` | 실제 전송 데이터. 여러 줄 가능 (각 줄마다 `data:` 접두사 필요) | 없음 |
| `retry` | 재연결 대기 시간(밀리초). 서버가 클라이언트의 재연결 간격을 제어 | 브라우저 기본값 |
| `:` (주석) | 콜론으로 시작하는 줄은 주석으로 처리됨. 연결 유지(keep-alive)에 활용 | - |

메시지는 빈 줄(`\n\n`)로 구분되는데, 이것이 SSE에서 하나의 메시지 경계를 나타낸다.

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

SSE는 알림, 뉴스 피드, 주식 시세, 진행률 표시 같은 **서버에서 클라이언트로의 단방향 스트리밍** 시나리오에서 빛난다. 기존 HTTP 인프라(로드밸런서, 프록시, 인증)를 그대로 활용할 수 있다는 점이 큰 장점이고, 브라우저가 자동으로 재연결을 처리해주니 구현 복잡도도 낮다. 필자의 경험상 단순한 알림 시스템에서는 WebSocket보다 SSE를 선택하는 것이 훨씬 운영하기 편하다. 다만 채팅이나 게임처럼 양방향 실시간 통신이 필요하거나 바이너리 데이터를 자주 주고받아야 한다면 WebSocket이 더 나은 선택이다.

### 12.1.4 클라이언트 측 EventSource API

클라이언트 쪽에서 SSE를 수신하는 JavaScript 코드를 보자. 정말 간단하다.

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

`EventSource`는 한 가지 놀라운 기능이 있는데, 연결이 떨어지면 자동으로 재연결을 시도한다는 것이다. 개발자가 따로 구현할 필요가 없다. `readyState` 속성으로 연결 상태를 확인할 수 있으며, 세 가지 상태(`CONNECTING(0)`, `OPEN(1)`, `CLOSED(2)`)를 가진다.

---

## 12.2 Flux를 활용한 SSE 엔드포인트 구현

### 12.2.1 TEXT_EVENT_STREAM 미디어 타입

다행히 Spring WebFlux에는 SSE 지원이 이미 내장되어 있어서 추가 라이브러리를 설치할 필요가 없다. SSE 엔드포인트를 구현하는 가장 직관적인 방법은 컨트롤러 메서드에서 `Flux`를 반환하고 `produces` 속성에 `text/event-stream` 미디어 타입을 지정하는 것이다. 보기보다 간단하다.

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

보면 알겠지만, `MediaType.TEXT_EVENT_STREAM_VALUE`는 단순히 `"text/event-stream"` 문자열을 상수로 정의한 것이다. 이것만 설정하면 Spring WebFlux가 나머지를 다 처리해준다. `Flux`의 각 요소가 자동으로 SSE 메시지 형식(`data:` 필드)으로 변환되어 클라이언트에 흘러간다.

### 12.2.2 ServerSentEvent 클래스 활용

하지만 `data` 필드만으로는 부족한 경우가 많다. `id`, `event`, `retry` 같은 필드들도 제어하고 싶으면 `ServerSentEvent<T>` 제네릭 클래스를 사용하면 된다.

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

흥미로운 점은 `ServerSentEvent`를 반환 타입으로 사용할 때는 `produces` 속성을 생략해도 된다는 것이다. Spring WebFlux가 반환 타입을 분석해서 자동으로 `text/event-stream`을 적용해버린다.

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

실제 SSE 구현에서는 타이머 같은 구조가 자주 나온다. `Flux.interval()`이 바로 그 도구다. 지정된 간격으로 0부터 시작하는 `Long` 값을 계속 내보내는 Hot Publisher다. 주기적으로 데이터를 보내야 하는 SSE 엔드포인트에 딱 맞다.

```java
@Slf4j
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

실무에서는 한 가지 이벤트만 보내는 경우보다 여러 종류의 이벤트를 섞어서 보내야 할 때가 많다. 시스템 상태, 통계, 하트비트 같은 것들이 동시에 흘러가야 하는 상황 말이다. `Flux.merge`를 사용하면 여러 스트림을 하나로 합칠 수 있고, 클라이언트는 `addEventListener`로 필요한 이벤트만 골라서 받을 수 있다.

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

컨트롤러 방식 대신 Router Functions를 선호한다면 그쪽으로도 SSE를 구현할 수 있다.

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

`Flux.interval()`로 주기적으로 데이터를 보내는 것만으로는 실무 서비스를 만들 수 없다. 댓글이 달리거나 특정 이벤트가 발생할 때 연결된 모든 클라이언트에게 즉각적으로 알려줘야 하니까. 바로 이런 상황에서 Reactor의 `Sinks`가 활용된다. 프로그래밍 방식으로 이벤트를 발행할 수 있는 Hot Publisher이기 때문에 이 목적에 완벽하다.

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

Sinks의 종류를 이해하려면 각 팩토리 메서드의 차이를 알아야 한다.

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

모든 알림을 모든 사용자에게 보낼 수는 없다. 각 사용자마다 독립적인 구독을 관리해야 하고, 해당 사용자에게만 알림을 전달해야 한다. 이것이 실무에서 많이 쓰이는 패턴인데, 살펴보자.

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

SSE 연결이 끊어지는 상황은 여러 가지가 있다. 정리해보면 이렇다.

1. **클라이언트가 연결을 닫는 경우**: `EventSource.close()` 호출 또는 브라우저 탭 닫기
2. **서버에서 스트림을 완료하는 경우**: `Flux`가 `onComplete` 또는 `onError` 신호를 발생
3. **네트워크 문제**: 예기치 않게 연결이 끊어지는 경우
4. **프록시/로드밸런서 타임아웃**: 일정 시간 동안 데이터가 흐르지 않으면 자동으로 연결 종료

모든 상황을 통일되게 처리하려면 `doFinally`를 사용하면 된다. 이 메서드는 `onComplete`, `onError`, `cancel` 모든 종료 신호를 감지하기 때문에, 리소스를 안전하게 정리하는 데 이상적이다.

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

여기까지 배운 것들을 실제로 조합해보자. 게시글에 댓글이 달릴 때 게시글 작성자에게 알림을 보내는 상황을 구현해보면 이렇게 된다.

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

참고로, 11장에서 배운 JWT 인증을 이 시스템과 함께 사용하면 `ReactiveSecurityContextHolder`에서 현재 사용자를 가져와서 인증된 사용자 전용 SSE 구독을 만들 수 있다. 필자의 경험상 이렇게 조합하면 보안이 훨씬 단단해진다.

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

MongoDB의 Change Streams 기능은 컬렉션, 데이터베이스, 또는 클러스터 전체의 데이터 변경을 실시간으로 감시한다. 8장에서 기초를 다루었지만, 이번에는 이 기능을 SSE와 결합해서 클라이언트에게 데이터 변경을 즉시 알리는 방법을 중점적으로 살펴본다.

- **이벤트 타입**: `insert`, `update`, `replace`, `delete`, `invalidate`
- **Resume Token**: 연결이 끊어진 지점부터 이벤트를 다시 수신할 수 있다
- **필터링**: Aggregation Pipeline을 사용하여 관심 있는 변경만 수신 가능
- **요구사항**: Replica Set 또는 Sharded Cluster 환경에서만 작동한다. 단일 노드 MongoDB에서는 쓸 수 없다는 점을 기억해두자

### 12.4.2 ReactiveMongoTemplate의 changeStream()

Spring Data MongoDB에서 제공하는 `ReactiveMongoTemplate`은 `changeStream()` 메서드로 MongoDB의 Change Streams를 `Flux`로 변환해준다. 간단하지만 강력한 도구다.

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

MongoDB의 Change Streams 이벤트를 받아서 SSE로 클라이언트에게 보내는 컨트롤러를 만들어보자.

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
                        .operationType(event.getOperationType().name())
                        .product(event.getBody())
                        .timestamp(Instant.now())
                        .build();

                    return ServerSentEvent.<ProductChangeEvent>builder()
                        .id(event.getRaw() != null && event.getRaw().getResumeToken() != null
                            ? event.getRaw().getResumeToken().toJson() : null)
                        .event("product-" + event.getOperationType().name())
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

네트워크가 끊어지거나 클라이언트가 재연결할 때 이전에 받던 이벤트들을 빠뜨리지 않으려면 Resume Token을 활용해야 한다. SSE의 `id` 필드에 Resume Token을 넣어두면, 브라우저가 자동으로 재연결 시 `Last-Event-ID` 헤더에 담아서 보낸다. 매우 우아한 설계다.

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
            String tokenJson = event.getRaw() != null && event.getRaw().getResumeToken() != null
                ? event.getRaw().getResumeToken().toJson() : null;

            ProductChangeEvent payload = ProductChangeEvent.builder()
                .operationType(event.getOperationType().name())
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

클라이언트 쪽에서는 특별히 할 일이 없다. `EventSource`가 알아서 재연결할 때 `Last-Event-ID`를 보내니까.

```javascript
const es = new EventSource('/api/products/stream/resumable');
es.addEventListener('product-change', (e) => {
    console.log('이벤트 ID:', e.lastEventId);
    const change = JSON.parse(e.data);
    applyChange(change);
});
```

### 12.4.5 실시간 데이터 동기화 패턴

Change Streams와 SSE를 조합하면 여러 브라우저 탭이나 사용자 간에 데이터를 실시간으로 동기화할 수 있다. 한 사용자가 상품 정보를 수정하면, 같은 상품을 보고 있는 다른 사용자의 화면에 즉시 반영되는 그런 경험을 만들 수 있다는 뜻이다. 필자의 경험상 이 패턴을 구현할 때 핵심은 이렇다.

1. **`@PostConstruct`에서 Change Stream 시작**: 애플리케이션 기동 시 감시할 컬렉션에 대해 Change Stream을 구독한다.
2. **세션별 Sink 관리**: `ConcurrentHashMap<String, Sinks.Many<ChangeEvent>>`로 세션마다 독립적인 Sink를 생성한다.
3. **이벤트 분배**: Change Stream에서 수신한 이벤트를 해당 컬렉션을 구독 중인 모든 세션의 Sink에 `tryEmitNext`로 전달한다.
4. **SSE 엔드포인트**: `GET /api/sync/stream/{collection}?sessionId=xxx` 형태로 클라이언트가 특정 컬렉션의 변경 사항을 구독한다.

이 패턴은 12.3절의 사용자별 알림 구독과 동일한 `ConcurrentHashMap` + `Sinks` 구조를 컬렉션 단위로 확장한 것이다.

### 12.4.6 프로덕션 환경 고려사항

개발 환경에서는 잘 작동하는 SSE도 프로덕션에 올리면 문제가 생기는 경우가 많다. 미리 알아둬야 할 사항들을 정리했다.

**1. 연결 수 관리**

SSE는 HTTP 연결을 계속 열어놓기 때문에, 동시 연결 수가 늘어나면 서버 메모리와 파일 디스크립터가 빠르게 소진된다. `AtomicInteger`로 활성 연결 수를 세어두고 최대 한계를 설정해둔다. 너무 많은 연결을 받지 않도록 선제적으로 차단하는 것이 좋다.

**2. 프록시/로드밸런서 설정**

Nginx 같은 리버스 프록시가 앞단에 있으면, SSE 연결이 조기에 끊어지는 문제가 자주 생긴다. 이를 방지하려면 프록시에서 버퍼링을 끄고 타임아웃을 충분히 길게 설정해야 한다.

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

프록시 타임아웃으로 연결이 끊어지는 것을 방지하려면 주기적으로 하트비트를 보내면 된다. SSE의 주석 문법(`:` 접두사)을 활용하면 클라이언트 쪽 이벤트 핸들러를 건드리지 않으면서도 연결을 살려둘 수 있다.

**4. 에러 복구 전략**

Change Stream이 갑자기 끊어질 수 있다. 데이터베이스가 재시작되거나 네트워크 문제가 생길 때 말이다. 이럴 때 자동으로 재시도하는 로직이 있으면 훨씬 안정적이다. `retryWhen`에 지수 백오프를 걸어두면 일시적 장애에서 우아하게 복구할 수 있다.

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

이번 장에서 배운 내용의 핵심을 다시 한 번 정리해보자.

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

다음 장은 WebSocket으로 나아간다. 양방향 실시간 통신이 필요한 채팅 애플리케이션을 어떻게 만드는지 알아볼 것이다.
# Chapter 13. WebSocket

채팅, 게임, 실시간 대시보드 같은 애플리케이션들을 만들다 보면 HTTP의 요청-응답 모델만으로는 부족함을 느끼게 된다. 사용자가 메시지를 보낼 때까지 기다렸다가 응답하는 방식으로는, 서버가 즉시 클라이언트에게 데이터를 보낼 수 없기 때문이다. 이런 상황에서 WebSocket이 빛을 발한다. 한 번 연결을 수립하면 양쪽이 자유롭게 메시지를 주고받을 수 있고, Spring WebFlux는 리액티브 스트림 기반의 WebSocket 지원을 기본으로 제공한다.

이 장에서는 WebSocket이 어떻게 동작하는지 먼저 살펴보고, WebFlux에서 핸들러를 구현한 후 실제 채팅 애플리케이션을 만들어볼 것이다. 마지막으로 프로덕션 환경에 필요한 세션 관리 전략까지 다룰 예정이다.

---

## 13.1 WebSocket 프로토콜 이해

### 13.1.1 WebSocket이란?

WebSocket은 RFC 6455로 표준화된 프로토콜인데, 단순하게 말하면 TCP 연결 위에서 클라이언트와 서버가 **전이중(Full-Duplex) 양방향 통신**을 할 수 있게 해준다. HTTP는 클라이언트의 요청을 기다렸다가 응답하는 방식이지만, WebSocket은 연결이 한 번 수립되면 양쪽 모두 언제든 메시지를 보낼 수 있다. 이 차이가 실시간 애플리케이션 개발에서 정말 중요하다.

| 특징 | 설명 |
|------|------|
| **양방향 통신** | 클라이언트와 서버 모두 독립적으로 메시지를 전송할 수 있다 |
| **지속 연결** | 한 번 연결이 수립되면 명시적으로 종료할 때까지 유지된다 |
| **낮은 오버헤드** | HTTP 헤더 없이 최소 2바이트의 프레임 헤더로 메시지를 교환한다 |
| **실시간성** | 폴링 없이 서버에서 즉시 클라이언트로 데이터를 전송할 수 있다 |

### 13.1.2 HTTP 핸드셰이크

흥미롭게도, WebSocket 연결은 일반 HTTP 요청으로 시작된다. 프로토콜을 업그레이드하는 과정을 거치는 것이다.

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

구체적으로는 이렇게 진행된다:

1. 클라이언트가 `Upgrade: websocket` 헤더를 포함한 HTTP GET 요청을 보낸다
2. 서버는 `Sec-WebSocket-Key`에 매직 GUID(`258EAFA5-E914-47DA-95CA-C5AB0DC85B11`)를 붙여서 SHA-1 해시를 만들고, 그 결과를 `Sec-WebSocket-Accept`에 담아 응답한다
3. 서버가 `101 Switching Protocols`를 반환하면, TCP 연결은 살아있되 프로토콜만 WebSocket으로 바뀐다
4. 이제부터 양쪽은 WebSocket 프레임 형식으로 메시지를 교환한다

### 13.1.3 프레임 구조

연결이 수립되면 이제 프레임(Frame) 단위로 데이터를 주고받는다. 각 프레임은 그 의도를 나타내는 Opcode를 가지고 있다.

| Opcode | 의미 |
|--------|------|
| `0x1` | 텍스트 프레임 (UTF-8) |
| `0x2` | 바이너리 프레임 |
| `0x8` | 연결 종료 (Close) |
| `0x9` | Ping |
| `0xA` | Pong |

실제로 개발할 때는 이런 저수준의 세부사항까지 신경 쓸 일은 거의 없다. 다만 알아두면 좋은 것은, 텍스트 프레임은 채팅 메시지 같은 문자열을 보낼 때, 바이너리 프레임은 이미지나 파일 같은 데이터를 보낼 때 사용된다는 점이다. 각 프레임은 내부적으로 마지막 프레임 여부, 페이로드 길이, 실제 데이터 등으로 구성된다.

### 13.1.4 WebSocket vs SSE vs Long Polling 비교

| 특성 | WebSocket | SSE | Long Polling |
|------|-----------|-----|--------------|
| **통신 방향** | 양방향 (Full-Duplex) | 단방향 (서버->클라이언트) | 단방향 |
| **프로토콜** | ws:// / wss:// | HTTP | HTTP |
| **오버헤드** | 매우 낮음 (2-14바이트) | 낮음 | 높음 (매번 HTTP 헤더) |
| **자동 재연결** | 직접 구현 필요 | EventSource 자동 지원 | 직접 구현 필요 |
| **바이너리 전송** | 지원 | 미지원 | 미지원 |

Chapter 12에서 다룬 SSE는 서버에서 클라이언트로 일방적으로 보내는 스트리밍에는 제격이다. 하지만 채팅처럼 양쪽 모두 메시지를 보내야 한다면 WebSocket이 필요하다. 필자의 경험상, 실시간 알림처럼 서버의 푸시만 필요한 경우 SSE를 쓰면 구현이 훨씬 간단하지만, 사용자 상호작용이 있는 경우 WebSocket을 선택하게 된다.

---

## 13.2 WebFlux에서 WebSocket 핸들러 구현

### 13.2.1 의존성 설정

좋은 소식은 Spring WebFlux에 WebSocket 지원이 이미 포함되어 있다는 것이다. 별도로 추가할 게 없다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    implementation 'org.springframework.boot:spring-boot-starter-data-mongodb-reactive'
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
}
```

### 13.2.2 WebSocketHandler 인터페이스

Spring WebFlux에서 WebSocket을 다루는 핵심은 `WebSocketHandler` 인터페이스다.

```java
public interface WebSocketHandler {
    Mono<Void> handle(WebSocketSession session);
}
```

`handle()` 메서드가 연결이 수립되면 호출되고, 이 메서드가 반환하는 `Mono<Void>`가 완료되면 연결이 끝난다. `WebSocketSession` 객체는 `receive()`로 들어오는 메시지 스트림을 얻고, `send()`로 메시지를 보낸다.

이해를 돕기 위해 간단한 에코 핸들러를 만들어보자.

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

이제 이 핸들러를 특정 URL 경로에 연결해야 한다. `HandlerMapping`과 `WebSocketHandlerAdapter`를 설정하면 된다.

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

실제 구현할 때는 상황에 따라 다른 패턴을 쓴다. 기본적으로 세 가지를 생각해볼 수 있다.

**패턴 1: 수신 전용** — 클라이언트에서 오는 메시지를 받아서 처리하기만 한다

```java
public Mono<Void> handle(WebSocketSession session) {
    return session.receive()
        .doOnNext(msg -> log.info("수신: {}", msg.getPayloadAsText()))
        .then();
}
```

**패턴 2: 송신 전용** — 서버에서 클라이언트로 계속 데이터를 보낸다

```java
public Mono<Void> handle(WebSocketSession session) {
    Flux<WebSocketMessage> output = Flux.interval(Duration.ofSeconds(1))
        .map(tick -> session.textMessage("서버 시간: " + LocalDateTime.now()));
    return session.send(output);
}
```

**패턴 3: 양방향** — 수신과 송신을 동시에 처리한다

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

실무에서는 평문보다는 JSON 형식의 메시지를 주고받는다. 구조가 명확해서 다루기 훨씬 편하기 때문이다.

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

브라우저의 JavaScript로 동작을 테스트하면 다음과 같이 한다.

```javascript
const ws = new WebSocket('ws://localhost:8080/ws/echo');
ws.onopen = () => ws.send('Hello WebSocket!');
ws.onmessage = (event) => console.log('수신:', event.data);
ws.onclose = (event) => console.log('종료:', event.code);
```

---

## 13.3 실시간 채팅 애플리케이션 구축

이제 WebSocket의 진정한 가치가 나오는 부분이다. WebSocket과 MongoDB를 결합해서 여러 채팅방을 지원하는 실시간 채팅 애플리케이션을 만들어보자.

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

이제 핵심 부분이다. 한 사용자가 메시지를 보내면 같은 채팅방의 모든 다른 사용자들에게 전달해야 한다. Reactor의 `Sinks`라는 기능을 사용하면 이를 깔끔하게 구현할 수 있다. 한쪽에서 메시지를 발행하면 여러 세션이 이를 구독하는 구조인데, 필자의 경험상 채팅처럼 다대다 통신이 필요한 경우 `Sinks`가 정말 유용하다.

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

`Sinks.many().multicast().onBackpressureBuffer(256)`는 여러 구독자에게 동시에 메시지를 전달하는 Hot Publisher를 만든다. 만약 어떤 클라이언트가 느려서 메시지를 처리하지 못하면, 최대 256개까지 버퍼에 보관했다가 추후에 보낸다. 이렇게 하면 느린 클라이언트 때문에 빠른 클라이언트까지 영향을 받지 않는다.

### 13.3.4 채팅 메시지 서비스

메시지를 저장하고 브로드캐스팅하는 로직을 한 곳에 모으자.

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

지금까지 만든 서비스들을 모두 조합해서 실제 채팅을 처리할 WebSocket 핸들러를 만든다.

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

WebSocket 연결이 시작되기 전에 채팅방을 만들고 관리해야 한다. 이를 위한 REST API를 준비하자.

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

채팅에서 중요한 부분 중 하나는 사용자가 입장했을 때 기존 메시지를 보여주는 것이다. 이를 하는 방법은 크게 두 가지가 있다.

**전략 1: REST API를 통한 초기 로드** — WebSocket 연결을 맺기 전에 REST API로 최근 메시지를 미리 가져온다

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

**전략 2: WebSocket 내 히스토리 전송** — 연결 직후 과거 메시지를 먼저 보낸 다음, 실시간 메시지로 전환한다

```java
Flux<WebSocketMessage> history = chatMessageService.getRecentMessages(roomId, 50)
    .mapNotNull(msg -> toWebSocketMessage(session, msg));
Flux<WebSocketMessage> live = messageBroker.subscribe(roomId)
    .mapNotNull(msg -> toWebSocketMessage(session, msg));

Flux<WebSocketMessage> output = history.concatWith(live);
```

일반적으로는 전략 1이 더 간단하고, 과거 메시지와 실시간 메시지 사이에 누락될 위험도 적다. 필자의 경험상 프로덕션 환경에서는 전략 1을 쓰는 것이 더 안정적이다.

### 13.3.8 MongoDB 인덱스 설정

채팅방별로 시간 순서대로 메시지를 자주 조회하므로, 성능을 위해 복합 인덱스를 만들어두자.

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

WebSocket 세션도 생명주기가 있다: `CONNECTING -> OPEN -> CLOSING -> CLOSED`. 여러 세션을 추적하고 필요할 때 제어하려면 세션을 중앙에서 관리해야 한다.

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

    public Map<String, WebSocketSession> getSessions(String roomId) {
        return roomSessions.getOrDefault(roomId, new ConcurrentHashMap<>());
    }

    public String getUsername(String sessionId) {
        return sessionUserMap.getOrDefault(sessionId, "unknown");
    }

    public Map<String, WebSocketSession> getAllSessions() {
        Map<String, WebSocketSession> all = new ConcurrentHashMap<>();
        roomSessions.values().forEach(all::putAll);
        return all;
    }
}
```

ChatWebSocketHandler에 이를 통합하면, 연결 시점에 `register()`를 호출하고, 연결이 끝나는 시점인 `doFinally()`에서 `unregister()`를 호출하는 식으로 세션 생명주기를 관리한다.

### 13.4.2 Ping/Pong 하트비트

네트워크가 불안정하거나 오랫동안 아무 메시지도 없으면, 프록시나 방화벽이 유휴 연결을 끊어버릴 수 있다. 이를 방지하려면 주기적으로 Ping/Pong을 주고받으면서 연결이 살아있음을 알린다.

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

그런데 프록시나 방화벽이 WebSocket 프레임을 제대로 지원하지 않는 경우도 있다. 이런 상황에서는 애플리케이션 레벨에서 직접 하트비트를 처리해야 한다.

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

결국 네트워크는 끊긴다. 이를 대비한 자동 재연결 메커니즘은 필수다. 클라이언트와 서버 양쪽에서 대비해야 한다.

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

클라이언트가 재연결할 때 타임스탬프를 전달하면, 그 이후의 메시지들을 모두 전송해줄 수 있다.

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

WebSocket 연결을 닫을 때는 `CloseStatus` 코드로 종료 사유를 알린다. 주요 코드들이다.

| 코드 | 의미 |
|------|------|
| 1000 | 정상 종료 |
| 1001 | 서버 종료 또는 페이지 이동 |
| 1008 | 정책 위반 |
| 1011 | 서버 내부 오류 |
| 4000+ | 애플리케이션 정의 코드 |

예를 들어, 부정행위를 하는 사용자를 강제로 퇴장시키려면 이렇게 할 수 있다.

```java
public Mono<Void> disconnectUser(String roomId, String targetUsername) {
    return Flux.fromIterable(sessionRegistry.getSessions(roomId).entrySet())
        .filter(e -> targetUsername.equals(sessionRegistry.getUsername(e.getKey())))
        .flatMap(e -> e.getValue()
            .close(new CloseStatus(4001, "관리자에 의해 종료")))
        .then();
}
```

WebSocket 엔드포인트도 당연히 인증이 필요하다. WebSocket 핸드셰이크가 사실 HTTP 요청이므로, Spring Security를 그냥 적용할 수 있다. 다만 JWT 토큰 같은 걸 어떻게 전달할지는 생각해야 한다. 일반적으로는 쿼리 파라미터나 첫 번째 메시지에 담아서 보낸다.

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

> **주의**: URL 쿼리 파라미터로 토큰을 전달하면 로그에 그대로 남을 수 있다. 서버 로그, 브라우저 히스토리, 프록시 로그 등 여러 곳에 보인다는 뜻이다. 필자의 경험상 프로덕션에서는 쿠키를 쓰거나, WebSocket 연결 직후 첫 번째 메시지로 토큰을 보내는 것이 더 안전하다.

---

## 요약

이 장에서 배운 내용을 정리해보면:

| 주제 | 핵심 내용 |
|------|----------|
| **WebSocket 프로토콜** | HTTP 핸드셰이크로 시작해서 프레임으로 양방향 통신, SSE나 Long Polling과는 다른 특성 |
| **WebSocket 핸들러** | `WebSocketHandler` 인터페이스로 연결 관리, URL 매핑, 수신/송신/양방향 처리 |
| **실시간 채팅** | `Sinks.Many`로 메시지 브로드캐스팅, MongoDB에 저장, 과거 메시지 로드 |
| **세션 관리** | 세션 추적, 하트비트로 연결 유지, 재연결 시 메시지 복구, 보안 |

WebSocket은 정말로 강력한 도구다. 실시간 양방향 통신이 필요한 거의 모든 상황에서 유용하다. Spring WebFlux의 리액티브 지원과 Reactor의 `Sinks`를 잘 조합하면, 수많은 동시 연결을 안정적으로 처리하는 애플리케이션을 만들 수 있다. 다음 장에서는 다시 클라이언트 입장으로 돌아가서, WebClient로 외부 API를 리액티브하게 호출하는 방법을 다룬다.
# Chapter 14. WebClient: 리액티브 HTTP 클라이언트

Spring WebFlux를 사용하면서 외부 서비스와 통신해야 한다면, `RestTemplate` 같은 구식 도구보다 `WebClient`를 써야 한다. Spring 5에서 도입된 `WebClient`는 **논블로킹 리액티브 HTTP 클라이언트**로, 필자의 경험상 대규모 시스템에서 효율성 면에서 압도적으로 우수하다. 이 장에서는 실전에서 꼭 필요한 설정부터 기본 사용법, 에러 핸들링, 재시도 전략, 타임아웃 관리, 여러 API 동시 호출, 필터 구현까지 모두 살펴보겠다.

---

## 14.1 WebClient 설정과 기본 사용법

### 14.1.1 WebClient란?

`WebClient`는 Spring WebFlux에 포함된 논블로킹 HTTP 클라이언트이고, 내부에서 Reactor Netty의 `HttpClient`를 사용하고 있다. 리액티브 스트림 방식으로 요청과 응답을 다루는 것이 특징이다. 다음 표를 보면 기존 `RestTemplate`과 어떤 점이 다른지 한눈에 파악할 수 있다.

| 특성 | RestTemplate | WebClient |
|------|-------------|-----------|
| **블로킹 여부** | 블로킹 | 논블로킹 |
| **반환 타입** | 직접 객체 반환 | `Mono<T>`, `Flux<T>` |
| **스트리밍** | 미지원 | SSE, 스트리밍 응답 지원 |
| **유지 상태** | Spring 6에서 deprecated | 현재 권장 방식 |

### 14.1.2 WebClient 생성과 빈 설정

`WebClient`를 생성하는 방법은 몇 가지가 있다. `create()`, `create(baseUrl)`, `builder()`인데, 필자의 경험상 실전에서는 `builder()`로 설정하고 빈으로 등록하는 것이 가장 깔끔하다. 여러 외부 서비스를 호출해야 한다면, 각 서비스마다 별도 빈을 만드는 게 나중에 유지보수하기 좋다.

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

운영 환경이라면 Reactor Netty 커넥션 풀을 꼭 설정해줘야 한다. 기본값으로 두면 의외로 성능이 떨어질 수 있다.

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

대용량 응답을 다루거나 커스텀 직렬화가 필요하면 코덱을 설정해야 한다. `maxInMemorySize`는 응답 본문을 메모리에 버퍼링할 때 최대 크기인데, 기본값이 256KB이다. 실무에서 큰 JSON 파일을 받다 보면 `DataBufferLimitException`이 터질 수 있으니, 그럴 땐 이 값을 올려야 한다.

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

GET, POST, PUT, DELETE 각각을 어떻게 처리하는지 하나씩 살펴보자.

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
// JSON 본문 전송 (bodyValue: 준비된 객체)
public Mono<Product> createProduct(ProductRequest request) {
    return webClient.post().uri("/api/products")
        .bodyValue(request).retrieve().bodyToMono(Product.class);
}

// Mono 본문 전송 (body: Publisher 타입)
public Mono<Product> createProductReactive(Mono<ProductRequest> request) {
    return webClient.post().uri("/api/products")
        .body(request, ProductRequest.class).retrieve().bodyToMono(Product.class);
}

// 폼 데이터 전송
public Mono<String> submitForm(String username, String password) {
    return webClient.post().uri("/api/auth/login")
        .contentType(MediaType.APPLICATION_FORM_URLENCODED)
        .body(BodyInserters.fromFormData("username", username)
            .with("password", password))
        .retrieve().bodyToMono(String.class);
}
```

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

두 가지 방식이 있고 상황에 따라 쓰임이 다르다. `retrieve()`는 응답 본문만 간단하게 뽑아내주고 4xx/5xx 에러는 자동으로 예외를 던진다. 반면 `exchangeToMono()`를 쓰면 상태 코드나 헤더 같은 전체 응답 정보에 접근할 수 있어서 더 세밀한 제어가 가능하다.

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

음, SSE나 NDJSON 같은 스트리밍 응답도 당연히 처리할 수 있다.

```java
// SSE 스트림
public Flux<ServerSentEvent<String>> subscribeToEvents() {
    return webClient.get().uri("/api/events/stream")
        .accept(MediaType.TEXT_EVENT_STREAM).retrieve()
        .bodyToFlux(new ParameterizedTypeReference<ServerSentEvent<String>>() {});
}

// NDJSON 스트림
public Flux<Product> streamProducts() {
    return webClient.get().uri("/api/products/stream")
        .accept(MediaType.APPLICATION_NDJSON).retrieve()
        .bodyToFlux(Product.class);
}
```

---

## 14.3 에러 핸들링과 재시도 전략

외부 API를 호출하면 당연히 에러가 날 수 있다. 네트워크 문제, 서버 다운, 타임아웃... 이런 것들을 어떻게 처리할지가 중요하다.

### 14.3.1 onStatus()를 활용한 상태 코드별 처리

`retrieve()`는 기본적으로 4xx/5xx 응답에 `WebClientResponseException`을 자동으로 던진다. 하지만 `onStatus()`를 사용하면 각 상태 코드별로 맞춤 처리를 정의할 수 있다.

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

단순 `retry(n)`은 실패하면 바로 재시도하는데, 이건 외부 서비스에 부하를 받게 만들 수 있다. 운영 환경에서는 반드시 `Retry.backoff()`로 지수 백오프(exponential backoff)를 적용해야 한다. 처음엔 짧게 기다렸다가 점점 더 길게 기다리는 방식이다.

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

외부 서비스가 계속 장애 상태라면 재시도만 해서는 소용없다. 이럴 땐 요청 자체를 차단하고 빨리 실패하는 게 낫다. Resilience4j라는 라이브러리로 서킷 브레이커 패턴을 구현하면 된다.

```groovy
dependencies {
    implementation 'io.github.resilience4j:resilience4j-spring-boot3:2.3.0'
    implementation 'io.github.resilience4j:resilience4j-reactor:2.3.0'
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

타임아웃은 정말 중요하다. 만약 타임아웃이 없다면 외부 서비스의 장애가 자신의 서버까지 파급되어 버린다. 클라이언트가 계속 응답을 기다리다 보니 스레드 또는 리소스가 고갈되는 거다.

### 14.4.1 계층별 타임아웃

네트워크 요청은 여러 단계로 이루어져 있는데, 각 단계마다 타임아웃을 설정할 수 있다.

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

Reactor 레벨에서 제공하는 `timeout()` 연산자로 전체 리액티브 체인, 재시도를 포함한 최종 시간을 제한할 수 있다.

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

지금까지 배운 기법들을 실제 프로젝트에서 어떻게 조합해서 쓰는지 보자.

### 14.5.1 REST API 호출 서비스

외부 날씨 API를 호출하는 예제를 만들어 보자. 에러 처리, 재시도, 타임아웃까지 모두 함께 적용해야 한다.

```java
@Slf4j
@Service
public class WeatherClientService {

    private final WebClient webClient;

    public WeatherClientService(WebClient.Builder builder,
                                @Value("${weather.api.key}") String apiKey) {
        this.webClient = builder
            .baseUrl("https://api.openweathermap.org/data/2.5")
            .build();
    }

    public Mono<WeatherResponse> getCurrentWeather(String city) {
        return webClient.get()
            .uri(uriBuilder -> uriBuilder.path("/weather")
                .queryParam("q", city).queryParam("appid", apiKey)
                .queryParam("units", "metric").build())
            .retrieve()
            .onStatus(HttpStatusCode::is4xxClientError, response ->
                response.statusCode() == HttpStatus.NOT_FOUND
                    ? Mono.error(new CityNotFoundException("도시를 찾을 수 없습니다: " + city))
                    : response.createException())
            .bodyToMono(WeatherResponse.class)
            .retryWhen(Retry.backoff(2, Duration.ofSeconds(1))
                .filter(ex -> ex instanceof WebClientResponseException.ServiceUnavailable))
            .timeout(Duration.ofSeconds(10));
    }
}
```

### 14.5.2 여러 API 동시 호출 (zip)

대시보드처럼 여러 소스의 데이터가 필요한 경우, `Mono.zip()`으로 독립적인 API 호출들을 병렬로 실행하고 결과를 한데 모을 수 있다.

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

포인트는 세 API 호출이 **동시에** 실행된다는 것이다. 따라서 가장 느린 호출 기준으로만 대기하면 된다. 각각을 순차로 호출하는 것보다 훨씬 빠르다.

### 14.5.3 여러 API 결과 병합 (merge)

반면 `Flux.merge()`는 여러 소스의 결과를 도착 순서대로 그냥 합친다. 상대적으로 단순한 조합이지만, 스트리밍 데이터를 다룰 때는 이게 더 편할 수 있다.

```java
public Flux<PriceQuote> getPriceQuotes(String productId) {
    Flux<PriceQuote> a = webClient.get()
        .uri("https://supplier-a.com/api/price/{id}", productId)
        .retrieve().bodyToMono(PriceQuote.class).flux();
    Flux<PriceQuote> b = webClient.get()
        .uri("https://supplier-b.com/api/price/{id}", productId)
        .retrieve().bodyToMono(PriceQuote.class).flux();

    return Flux.merge(a, b)
        .timeout(Duration.ofSeconds(5))
        .onErrorResume(ex -> Flux.empty());
}
```

### 14.5.4 순차 API 호출 (flatMap 체이닝)

반대로 첫 번째 API의 결과가 두 번째 API 호출에 필요한 경우도 있다. 이럴 땐 `flatMap`으로 체이닝해서 순차적으로 실행한다.

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

외부 API가 실패해도 서비스는 계속 돌아야 할 수 있다. 이럴 때는 캐시나 기본값 같은 대체 데이터로 폴백하는 방식이 있다.

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

API가 페이지네이션으로 데이터를 제공하면, `expand()` 연산자로 다음 페이지를 자동으로 호출할 수 있다. 더 이상 다음 페이지가 없으면 `Mono.empty()`를 반환해서 재귀를 멈춘다.

```java
public Flux<Product> getAllProductsPaginated() {
    return fetchPage(0)
        .expand(page -> page.hasNext() ? fetchPage(page.getPage() + 1) : Mono.empty())
        .flatMapIterable(PageResponse::getContent);
}

private Mono<PageResponse<Product>> fetchPage(int page) {
    return webClient.get()
        .uri(uriBuilder -> uriBuilder.path("/api/products")
            .queryParam("page", page).queryParam("size", 100).build())
        .retrieve()
        .bodyToMono(new ParameterizedTypeReference<PageResponse<Product>>() {});
}
```

---

## 14.6 WebClient 필터와 인터셉터

대규모 애플리케이션에서는 로깅, 인증, 에러 처리 같은 공통 로직을 모든 API 호출에 적용해야 하는데, 매번 반복하는 건 비효율적이다. `ExchangeFilterFunction`으로 이런 횡단 관심사(cross-cutting concern)를 깔끔하게 처리할 수 있다.

### 14.6.1 ExchangeFilterFunction과 로깅 필터

`ExchangeFilterFunction`은 `WebClient`의 요청/응답 파이프라인에 끼워넣는 필터다. `WebClient.builder().filter()`로 등록하고, 여러 개를 등록하면 등록한 순서 그대로 체이닝된다.

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

외부 API 호출할 때는 당연히 인증이 필요하다. 간단한 API 키부터 복잡한 OAuth 토큰까지 여러 방식이 있다. 필터로 이걸 깔끔하게 처리해 보자.

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

기타 유용한 필터들도 몇 가지 있다.

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

이제 여러 필터를 조합해서 실제로 WebClient 빈을 만드는 방법을 보자.

```java
@Configuration
@RequiredArgsConstructor
public class WebClientConfig {

    private final DynamicAuthFilter dynamicAuthFilter;
    @Value("${external.api.base-url}") private String baseUrl;

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
            .filter(WebClientFilters.traceIdFilter())       // 1. 추적
            .filter(dynamicAuthFilter.authFilter())          // 2. 인증
            .filter(WebClientFilters.logRequestResponse())   // 3. 로깅
            .filter(WebClientFilters.errorHandlingFilter())  // 4. 에러 처리
            .build();
    }
}
```

필터는 등록 순서대로 체이닝되므로 순서가 중요하다. 필자의 경험상 추적 -> 인증 -> 로깅 -> 에러 처리 이 순서가 가장 깔끔하다.

### 14.6.5 테스트에서의 WebClient 모킹

`WebClient`를 사용하는 코드를 테스트할 때는 실제 외부 API를 호출할 수 없다. `MockWebServer`라는 도구로 가짜 API를 만들어서 테스트한다.

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

다음 장에서는 R2DBC를 활용하여 관계형 데이터베이스를 리액티브 방식으로 접근하는 방법과, MongoDB를 함께 사용하는 멀티 데이터소스 구성을 다룬다.
# Chapter 15. R2DBC와의 통합 (보너스)

지금까지 MongoDB를 중심으로 리액티브 데이터 접근을 살펴봤지만, 현실 프로젝트를 보면 관계형 데이터베이스(RDBMS)와 함께 사용해야 할 때가 매우 많습니다. 예를 들어 사용자 인증과 결제 정보는 강한 일관성이 필요하니 PostgreSQL에 저장하고, 상품 카탈로그와 리뷰는 높은 쓰기 처리량이 필요하니 MongoDB에 저장하는 식으로 말이죠. 이런 **하이브리드 아키텍처**를 설계할 때 핵심 도구가 **R2DBC(Reactive Relational Database Connectivity)**입니다. 이번 장에서는 R2DBC가 무엇인지, 그리고 MongoDB와 함께 사용할 때 어떤 패턴과 주의사항이 있는지 실전 예제로 함께 살펴보겠습니다.

---

## 15.1 R2DBC란?

### 15.1.1 R2DBC 소개

R2DBC는 **Reactive Relational Database Connectivity**의 약자로, 관계형 데이터베이스에 접근하는 비동기/논블로킹 방식의 SPI(Service Provider Interface) 명세입니다. 기존 JDBC는 블로킹 I/O 기반으로 설계되었지만, R2DBC는 처음부터 Reactive Streams 표준을 염두에 두고 논블로킹으로 만들어졌다는 점이 가장 큰 차이입니다.

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

필자의 경험상, JDBC 기반의 `JdbcTemplate`이나 JPA를 WebFlux와 함께 사용하면 곧바로 성능 문제가 나타납니다. 이벤트 루프 스레드가 데이터베이스 I/O를 기다리면서 블로킹되기 때문인데, 그러면 한 번에 처리할 수 있는 요청의 개수가 급격히 떨어지게 됩니다. R2DBC는 이 문제의 근본적인 해결책입니다.

```
[JDBC + WebFlux]
이벤트 루프 스레드 → DB 쿼리 실행(블로킹) → 스레드 대기 → 처리량 저하

[R2DBC + WebFlux]
이벤트 루프 스레드 → DB 쿼리 요청(논블로킹) → 다른 요청 처리 → 결과 도착 시 콜백
```

### 15.1.3 지원 데이터베이스와 의존성 설정

R2DBC는 SPI 명세이기 때문에 각 데이터베이스 벤더나 커뮤니티에서 드라이버를 구현합니다. 주요 데이터베이스의 상황은 다음과 같습니다.

| 데이터베이스 | Maven/Gradle Artifact |
|-------------|----------------------|
| **PostgreSQL** | `org.postgresql:r2dbc-postgresql` |
| **MySQL** | `io.asyncer:r2dbc-mysql` |
| **MariaDB** | `org.mariadb:r2dbc-mariadb` |
| **H2** | `io.r2dbc:r2dbc-h2` |
| **Oracle** | `com.oracle.database.r2dbc:oracle-r2dbc` |

이 장에서는 가장 널리 사용되는 **PostgreSQL**을 기준으로 진행하겠습니다. 먼저 `build.gradle`에 R2DBC 관련 의존성을 추가해야 합니다.

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

Spring Data R2DBC의 API는 MongoDB와 상당히 유사합니다. 다음 표를 보면 어떤 요소들이 있는지 이해할 수 있습니다.

| 구성 요소 | 설명 |
|----------|------|
| `ReactiveCrudRepository` | 기본 CRUD 연산을 제공하는 리포지토리 인터페이스 |
| `R2dbcEntityTemplate` | `ReactiveMongoTemplate`에 대응하는 저수준 템플릿 |
| `@Table`, `@Id`, `@Column` | 엔티티 매핑 어노테이션 (`@Entity`는 사용하지 않음) |
| `DatabaseClient` | SQL을 직접 작성하여 실행하는 저수준 클라이언트 |
| `R2dbcTransactionManager` | 리액티브 트랜잭션 관리자 |

MongoDB에서 `ReactiveMongoRepository`를 써본 개발자라면 R2DBC의 리포지토리도 거의 같은 방식으로 사용할 수 있습니다.

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

멀티 데이터소스 환경에서 성공의 핵심은 각 데이터베이스의 역할을 처음부터 명확히 정의하는 것입니다. 아래는 전형적인 전자상거래 플랫폼의 아키텍처입니다.

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

### 15.2.2 application.yml에 두 데이터소스 설정

설정 파일에서 MongoDB와 PostgreSQL의 접속 정보를 분리하여 정의합니다.

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

관계형 데이터베이스를 사용하려면 테이블 스키마를 미리 정의해야 합니다. Flyway를 이용해 `src/main/resources/db/migration/V1__init.sql` 파일을 작성하겠습니다.

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

두 데이터소스를 독립적으로 관리하려면 각각의 설정 클래스가 필요합니다. 리포지토리 스캔 경로를 분리하는 것이 핵심입니다.

> **참고**: Spring Boot의 R2DBC 자동 설정을 비활성화(`@SpringBootApplication(exclude = R2dbcAutoConfiguration.class)`)하거나, 자동 설정을 사용하는 경우 이 설정 클래스를 제거하세요.

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

멀티 데이터소스 환경에서 패키지를 분리하면 나중에 코드를 유지보수할 때 훨씬 수월합니다.

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

R2DBC 엔티티는 MongoDB와 다르게 `@Table`, `@Id`, `@Column` 어노테이션을 사용합니다. 다음은 주문 테이블을 매핑한 예제입니다.

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

한편 MongoDB 도큐먼트는 유연한 스키마의 장점을 충분히 활용합니다. 상품 정보처럼 다양한 속성이 필요한 경우가 좋은 예입니다.

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

두 데이터소스의 리포지토리를 패키지별로 명확히 분리하여 정의합니다.

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

멀티 데이터소스 환경에서 실제 가치를 발휘하려면 두 데이터베이스의 결과를 효과적으로 조합해야 합니다. Reactor의 연산자들이 이 부분에서 핵심 역할을 합니다.

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

멀티 데이터소스 환경에서 트랜잭션은 가장 까다로운 부분입니다. 필자의 경험상 여기서 실수하면 데이터 불일치 문제가 프로덕션까지 고스란히 들어갑니다.

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

분산 환경에서 일관성을 보장하는 가장 실용적인 방법은 Saga 패턴입니다. 한쪽이 실패하면 이미 성공한 다른 쪽의 변경을 의도적으로 되돌리는 방식인데, 이를 보상(compensation)이라고 부릅니다.

### 15.3.3 실전 예제: 주문 시스템 (Saga 패턴)

이제 실제 온라인 쇼핑 플랫폼에서 사용할 수 있는 주문 서비스를 구현해봅시다. 재고 차감(MongoDB) -> 주문 생성(PostgreSQL) -> 결제 처리(PostgreSQL) 순서로 진행하는데, 각 단계가 실패하면 이전 단계들을 순차적으로 보상합니다.

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
        Payment payment = Payment.builder()
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

이제 클라이언트 요청을 받아서 주문 서비스와 조회 서비스를 호출하는 컨트롤러를 만듭니다.

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

Spring Data R2DBC의 자동 쿼리 생성만으로는 부족한 경우도 있습니다. 그럴 때는 `DatabaseClient`를 사용해 SQL을 직접 작성할 수 있습니다. 예를 들어 판매 통계 같은 복잡한 집계 쿼리를 실행할 때 유용합니다.

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

이제 실무에서 자주 만나는 시나리오를 다루겠습니다. PostgreSQL의 주문 집계 데이터와 MongoDB의 상품 상세 정보, 리뷰 정보를 조합해 대시보드를 구성하는 예제입니다.

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

멀티 데이터소스를 성공적으로 운영하려면 몇 가지 중요한 원칙들이 있습니다. 필자가 실제 프로젝트에서 배운 내용을 정리해봤습니다.

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
                .doFinally(signal -> Mono.from(conn.close()).subscribe()))
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

마지막으로 멀티 데이터소스 환경에서 흔히 빠지는 함정들과 대응 방법을 정리했습니다. 이 부분을 꼼꼼히 읽어두면 나중에 많은 디버깅 시간을 절약할 수 있습니다.

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

이번 장에서는 리액티브 환경에서 관계형 데이터베이스를 다루는 R2DBC를 살펴봤고, MongoDB와 함께 사용하는 멀티 데이터소스 아키텍처를 실전 예제로 학습했습니다.

| 주제 | 핵심 내용 |
|------|----------|
| **R2DBC 소개** | JDBC의 리액티브 대안, Reactive Streams 기반 논블로킹 DB 접근 |
| **JDBC vs R2DBC** | 블로킹 vs 논블로킹, ThreadLocal vs Reactor Context 기반 트랜잭션 |
| **멀티 데이터소스 구성** | 패키지 분리, 설정 클래스 분리, 리포지토리 스캔 경로 분리 |
| **데이터 조합** | `flatMap`(순차), `zip`(병렬)을 활용한 조합 패턴 |
| **트랜잭션 관리** | 분산 트랜잭션 불가, Saga 패턴과 보상 트랜잭션으로 대응 |
| **실전 예제** | 주문 시스템 -- 재고 차감(MongoDB) + 주문 생성(PostgreSQL) + 결제 처리 |

요약하면, R2DBC는 WebFlux 기반 애플리케이션에서 관계형 데이터베이스를 사용할 때 현재 유일한 리액티브 선택지입니다. MongoDB와 함께 사용하면 각 데이터베이스의 강점을 충분히 활용할 수 있지만, 분산 환경의 트랜잭션과 데이터 정합성 문제에 대한 신중한 설계가 필수적입니다. 이 장에서 다룬 Saga 패턴과 보상 트랜잭션 개념을 잘 이해하고 있다면, 복잡한 멀티 데이터소스 시스템도 자신감 있게 설계할 수 있을 겁니다.

다음 장에서는 리액티브 애플리케이션을 체계적으로 테스트하는 전략을 다룹니다. StepVerifier와 WebTestClient를 활용해 리액티브 코드를 효과적으로 검증하는 방법을 살펴보겠습니다.
