# Chapter 18. 모니터링과 관측 가능성

배포 후 운영 환경에서 리액티브 애플리케이션을 안정적으로 관리하는 일은 생각보다 복잡하다. 그래서 우리에게는 세 가지 핵심 관측 가능성(Observability) 축이 필요한 것인데, 바로 **메트릭(Metrics)**, **트레이스(Traces)**, **로그(Logs)**다.

특히 WebFlux의 경우 전통적인 서블릿 기반 애플리케이션과는 다르다. 하나의 요청이 여러 스레드를 넘나들며 처리되기 때문에, 단순한 `ThreadLocal` 기반의 기존 모니터링 방식으로는 충분하지 않다.

이 장에서는 실제 운영 환경에 필요한 관측 가능성을 어떻게 구축할지 배워볼 것이다. Spring Boot Actuator로 메트릭을 노출하는 것부터 시작해서, Micrometer와 Prometheus로 수집하고, Grafana로 시각화하는 전체 파이프라인을 함께 구성해보자. 그리고 Reactor 스트림 내부에서 메트릭을 수집하는 방법, 분산 추적(Zipkin/Jaeger) 구성, 그리고 리액티브 환경에 맞춘 구조화된 로깅까지 실전에서 필요한 전략들을 차근차근 살펴보겠다.

---

## 18.1 Spring Boot Actuator 설정

### 18.1.1 Actuator 소개와 의존성

Spring Boot Actuator는 애플리케이션의 상태, 메트릭, 환경 정보 같은 것들을 HTTP 엔드포인트로 손쉽게 노출할 수 있게 해주는 운영 도구 모듈이다. WebFlux 환경에서도 동일하게 동작하며, 무엇보다 리액티브 기반의 Health Indicator를 제공한다는 점이 중요하다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    implementation 'org.springframework.boot:spring-boot-starter-data-mongodb-reactive'
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
}
```

### 18.1.2 엔드포인트 활성화와 노출 설정

Actuator를 처음 설정할 때 주의할 점이 하나 있는데, 기본적으로 대부분의 엔드포인트는 활성화되지만 HTTP로 노출되는 것은 `health`뿐이라는 것이다. 따라서 운영에 필요한 엔드포인트를 선택적으로 노출해야 한다.

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health, info, metrics, prometheus, env, loggers
      base-path: /actuator
  endpoint:
    health:
      show-details: when_authorized
      show-components: when_authorized
    info:
      enabled: true
  info:
    env:
      enabled: true
    java:
      enabled: true
    os:
      enabled: true
```

주요 엔드포인트는 다음과 같다.

| 엔드포인트 | 경로 | 설명 |
|-----------|------|------|
| **health** | `/actuator/health` | 애플리케이션 및 의존 서비스 상태 |
| **info** | `/actuator/info` | 애플리케이션 정보 (버전, Git 커밋 등) |
| **metrics** | `/actuator/metrics` | Micrometer 기반 메트릭 목록 |
| **prometheus** | `/actuator/prometheus` | Prometheus 형식의 메트릭 |
| **loggers** | `/actuator/loggers` | 런타임 로그 레벨 변경 |

### 18.1.3 커스텀 Health Indicator

MongoDB Reactive 스타터를 사용하면 `ReactiveMongoHealthIndicator`가 자동으로 등록되어 매우 편하다. 그런데 외부 결제 서비스라던가, 자동 감지되지 않는 외부 서비스의 상태를 확인하려면? 이럴 때는 `ReactiveHealthIndicator`를 직접 구현해서 처리해야 한다.

```java
@Component
public class ExternalPaymentServiceHealthIndicator
        implements ReactiveHealthIndicator {

    private final WebClient paymentClient;

    public ExternalPaymentServiceHealthIndicator(
            @Qualifier("paymentServiceClient") WebClient paymentClient) {
        this.paymentClient = paymentClient;
    }

    @Override
    public Mono<Health> health() {
        return paymentClient.get()
            .uri("/health")
            .retrieve()
            .bodyToMono(String.class)
            .map(response -> Health.up()
                .withDetail("service", "payment-api").build())
            .onErrorResume(ex -> Mono.just(Health.down()
                .withDetail("service", "payment-api")
                .withDetail("error", ex.getMessage()).build()))
            .timeout(Duration.ofSeconds(3),
                Mono.just(Health.down()
                    .withDetail("error", "Health check timed out").build()));
    }
}
```

### 18.1.4 Actuator 보안 설정

Actuator 엔드포인트를 운영 환경에 배포할 때 반드시 신경 써야 할 부분이 보안이다. 엔드포인트에는 민감한 정보들이 포함될 수 있으니까, Spring Security WebFlux와 연동하여 접근을 제한하는 것이 필수다.

```java
@Configuration
@EnableWebFluxSecurity
public class ActuatorSecurityConfig {

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(
            ServerHttpSecurity http) {
        return http
            .authorizeExchange(exchanges -> exchanges
                .pathMatchers("/actuator/health", "/actuator/info").permitAll()
                .pathMatchers("/actuator/prometheus").hasRole("MONITORING")
                .pathMatchers("/actuator/**").hasRole("ADMIN")
                .pathMatchers("/api/**").authenticated()
                .anyExchange().permitAll()
            )
            .httpBasic(Customizer.withDefaults())
            .csrf(csrf -> csrf.disable())
            .build();
    }
}
```

더 나아가, 운영 환경에서는 Actuator 포트를 애플리케이션 포트와 완전히 분리하는 방식을 강력히 권장한다.

```yaml
# application-prod.yml
management:
  server:
    port: 9090
  endpoints:
    web:
      exposure:
        include: health, prometheus
```

이 방식을 사용하면 애플리케이션은 8080 포트에서, Actuator는 9090 포트에서 서비스되므로, 방화벽 규칙으로 내부 네트워크만 접근 가능하도록 제한할 수 있다는 이점이 있다.

---

## 18.2 Micrometer와 Prometheus 연동

### 18.2.1 Micrometer 소개

Micrometer를 처음 들을 때, 사람들은 보통 "또 다른 라이브러리?"라고 생각한다. 그런데 이것은 정말 훌륭한 설계다. 흔히 말하는 **벤더 중립적 메트릭 파사드**로서, SLF4J가 로깅 구현체를 추상화하는 것처럼, Micrometer는 Prometheus, Datadog, CloudWatch 등 메트릭 수집 구현체를 모두 추상화한다. Spring Boot Actuator는 내부적으로 이 Micrometer를 활용하고 있으니, 우리가 제대로 이해하고 사용해야 할 필요가 있다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
    implementation 'io.micrometer:micrometer-registry-prometheus'
}
```

위 의존성을 추가하면 `/actuator/prometheus` 엔드포인트가 자동으로 활성화된다.

### 18.2.2 자동 수집 메트릭

설정을 하면, Spring Boot와 Micrometer가 자동으로 많은 메트릭을 수집해준다는 점이 정말 편하다. 별도의 코드 없이도 다양한 메트릭이 자동으로 수집되기 때문이다.

| 카테고리 | 메트릭 예시 | 설명 |
|---------|-----------|------|
| **JVM** | `jvm_memory_used_bytes` | 힙/논힙 메모리 사용량 |
| **JVM** | `jvm_gc_pause_seconds` | GC 일시 정지 시간 |
| **HTTP** | `http_server_requests_seconds` | HTTP 요청 처리 시간 (uri, method, status별) |
| **MongoDB** | `mongodb_driver_pool_size` | MongoDB 커넥션 풀 크기 |
| **MongoDB** | `mongodb_driver_commands_seconds` | MongoDB 명령 실행 시간 |
| **System** | `system_cpu_usage` | 시스템 CPU 사용률 |

### 18.2.3 커스텀 메트릭 -- Counter

이제 본격적으로 메트릭을 직접 정의해서 사용해보자. 가장 간단한 형태인 `Counter`부터 시작하면, 이것은 단조 증가하는 값을 추적한다. 주문 건수, 에러 발생 횟수 같은 것들을 기록할 때 매우 유용하다.

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final MeterRegistry meterRegistry;

    public Mono<Order> createOrder(OrderRequest request) {
        return orderRepository.save(Order.from(request))
            .doOnSuccess(order ->
                Counter.builder("orders.created")
                    .description("총 생성된 주문 수")
                    .tag("category", order.getCategory())
                    .tag("payment_method", order.getPaymentMethod())
                    .register(meterRegistry)
                    .increment())
            .doOnError(ex ->
                Counter.builder("orders.failed")
                    .description("주문 실패 수")
                    .tag("error_type", ex.getClass().getSimpleName())
                    .register(meterRegistry)
                    .increment());
    }
}
```

### 18.2.4 커스텀 메트릭 -- Gauge

`Gauge`는 Counter와 달리, 현재 시점의 값을 나타낸다. 대기열 크기, 활성 연결 수처럼 증가했다 감소했다를 반복하는 값에 사용하면 좋다.

```java
@Component
public class QueueMetrics {

    private final AtomicInteger pendingTaskCount = new AtomicInteger(0);

    public QueueMetrics(MeterRegistry meterRegistry) {
        Gauge.builder("tasks.pending", pendingTaskCount, AtomicInteger::get)
            .description("처리 대기 중인 작업 수")
            .register(meterRegistry);
    }

    public void taskAdded() { pendingTaskCount.incrementAndGet(); }
    public void taskCompleted() { pendingTaskCount.decrementAndGet(); }
}
```

### 18.2.5 커스텀 메트릭 -- Timer

마지막으로 소개할 `Timer`는 실무에서 정말 자주 쓰이는 메트릭인데, 작업의 소요 시간과 호출 횟수를 동시에 기록한다. 성능 분석에 필수적이고, 필자의 경험상 성능 문제를 추적할 때 가장 먼저 확인하는 메트릭이다.

```java
@Service
@RequiredArgsConstructor
public class ProductSearchService {

    private final ReactiveMongoTemplate mongoTemplate;
    private final MeterRegistry meterRegistry;

    public Flux<Product> search(String keyword) {
        Timer.Sample sample = Timer.start(meterRegistry);

        return mongoTemplate.find(
                new Query(Criteria.where("name").regex(keyword, "i")),
                Product.class)
            .doFinally(signalType ->
                sample.stop(Timer.builder("product.search.duration")
                    .description("상품 검색 소요 시간")
                    .tag("signal", signalType.name())
                    .publishPercentiles(0.5, 0.95, 0.99)
                    .publishPercentileHistogram()
                    .register(meterRegistry)));
    }
}
```

`publishPercentiles`로 p50, p95, p99 레이턴시를 Grafana에서 바로 확인할 수 있다.

### 18.2.6 공통 태그와 메트릭 사전 등록

모든 메트릭에 공통적으로 적용할 태그가 있다면, 중복 코드 대신 한 곳에서 관리하자.

```java
@Configuration
public class MetricsConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> commonTags() {
        return registry -> registry.config()
            .commonTags(
                "application", "webflux-shop",
                "environment", System.getenv().getOrDefault("ENV", "local")
            );
    }

    @Bean
    public Timer externalApiTimer(MeterRegistry registry) {
        return Timer.builder("external.api.duration")
            .description("외부 API 호출 소요 시간")
            .publishPercentiles(0.5, 0.95, 0.99)
            .register(registry);
    }
}
```

### 18.2.7 Prometheus 설정 (prometheus.yml)

이제 Prometheus가 우리 애플리케이션의 메트릭을 주기적으로 수집하도록 설정해야 한다.

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'webflux-app'
    metrics_path: '/actuator/prometheus'
    scrape_interval: 10s
    static_configs:
      - targets: ['host.docker.internal:8080']
        labels:
          app: 'webflux-shop'
          env: 'development'

  - job_name: 'webflux-cluster'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets:
          - 'webflux-app-1:9090'
          - 'webflux-app-2:9090'
          - 'webflux-app-3:9090'
```

그리고 Docker Compose로 Prometheus를 실행하면 되는데, 제대로 설정되었는지 확인하려면 Prometheus UI(`http://localhost:9090`)에서 `up{job="webflux-app"}` 쿼리를 실행해서 타겟 연결 상태를 확인하면 된다.

```yaml
# docker-compose-monitoring.yml
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

---

## 18.3 Grafana 대시보드 구성

### 18.3.1 Grafana Docker 설치와 데이터소스 연결

Prometheus에서 수집한 메트릭을 이제 시각화해야 한다. 기존 `docker-compose-monitoring.yml`에 Grafana를 추가하자.

```yaml
services:
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin123
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    depends_on:
      - prometheus
```

`docker compose -f docker-compose-monitoring.yml up -d`로 실행하고, `http://localhost:3000`에 접속해서 로그인하면 된다. Grafana의 프로비저닝 기능을 사용하면 Prometheus 데이터소스를 자동으로 등록할 수 있다.

```yaml
# grafana/provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

### 18.3.3 대시보드 임포트

Grafana 커뮤니티에서 이미 만들어놓은 훌륭한 대시보드들이 있다. 이걸 임포트하면 처음부터 모두 직접 만들 필요 없이 빠르게 모니터링 환경을 구축할 수 있으니, 실무에서 자주 활용하면 좋다.

| 대시보드 ID | 이름 | 용도 |
|------------|------|------|
| **4701** | JVM (Micrometer) | JVM 메모리, GC, 스레드 모니터링 |
| **11378** | Spring Boot Statistics | HTTP 요청, 에러율, 응답 시간 |
| **12900** | Spring Boot Observability | 종합 관측 가능성 |

Grafana UI에서 **Dashboards > Import** 메뉴로 이동하여 대시보드 ID를 입력하면 된다.

### 18.3.4 커스텀 대시보드 PromQL 쿼리

프로젝트에 맞게 커스텀 패널을 만들어야 할 때가 분명히 온다. 그럴 때를 위해 자주 사용하는 PromQL 쿼리들을 정리해놨으니, 필요할 때 참고하자.

**초당 요청 수 (RPS)**:
```promql
rate(http_server_requests_seconds_count{application="webflux-shop"}[5m])
```

**95번째 백분위 응답 시간**:
```promql
histogram_quantile(0.95,
  rate(http_server_requests_seconds_bucket{application="webflux-shop"}[5m]))
```

**에러율 (%)**:
```promql
sum(rate(http_server_requests_seconds_count{status=~"5.."}[5m]))
/
sum(rate(http_server_requests_seconds_count[5m]))
* 100
```

### 18.3.5 알림 규칙 설정

대시보드를 만들었으면 이제 문제 상황을 자동으로 감지하고 알려주는 알림 기능을 설정해야 한다. Grafana의 알림 기능을 사용하면 Slack, Email, PagerDuty 등으로 문제를 바로 알릴 수 있다. Grafana UI의 **Alerting > Alert Rules > New alert rule**에서 생성하면 되며, 주요 설정 항목은 다음과 같다.

| 설정 항목 | 값 | 설명 |
|----------|---|------|
| **Rule name** | 높은 에러율 경고 | 알림 규칙 이름 |
| **Query** | 위 에러율 PromQL | 감시 대상 쿼리 |
| **Threshold** | `> 5` | 에러율 5% 초과 시 |
| **Pending period** | `5m` | 5분간 지속 시 알림 발생 |

알림 채널은 **Alerting > Contact points**에서 설정한다.

---

## 18.4 리액티브 스트림 메트릭 수집

### 18.4.1 Reactor 메트릭 활성화

Reactor는 Micrometer와 깊게 통합되어 있는데, 내장 메트릭 기능을 제공한다. 이 기능을 활성화하면 Reactor 파이프라인 내부의 구독 상태, 요청 수, 에러 등을 추적할 수 있으니 매우 유용하다.

```java
@SpringBootApplication
public class WebFluxApplication {

    public static void main(String[] args) {
        Hooks.enableAutomaticContextPropagation();
        Schedulers.enableMetrics();
        SpringApplication.run(WebFluxApplication.class, args);
    }
}
```

### 18.4.2 개별 연산자 메트릭 수집

특정 Reactor 체인에 대해 더 세밀한 메트릭을 수집하려면 `.name()`과 `.tag()` 연산자를 활용하면 된다. 그리고 체인 끝에 `.metrics()`를 추가하면 해당 시점까지의 모든 메트릭이 Micrometer로 자동 기록된다.

```java
@Service
@RequiredArgsConstructor
public class NotificationService {

    private final ReactiveMongoTemplate mongoTemplate;

    public Flux<Notification> getUnreadNotifications(String userId) {
        return mongoTemplate.find(
                Query.query(Criteria.where("userId").is(userId)
                    .and("read").is(false)),
                Notification.class)
            .name("notification.unread.fetch")
            .tag("type", "unread")
            .metrics();
    }
}
```

이렇게 구성하면 다음과 같은 메트릭이 자동으로 생성되는데, 한번 생기면 Grafana에서 바로 확인할 수 있다.

| 메트릭 이름 | 설명 |
|------------|------|
| `reactor.notification.unread.fetch.subscribed` | 구독 횟수 |
| `reactor.notification.unread.fetch.requested` | 요청된 요소 수 |
| `reactor.notification.unread.fetch.onNext.delay` | onNext 신호 간의 지연 시간 |
| `reactor.notification.unread.fetch.flow.duration` | 전체 실행 시간 |

### 18.4.3 Schedulers 메트릭

스레드 풀 성능을 모니터링할 필요가 있을 때는 `Schedulers.enableMetrics()` 호출 후 다음 메트릭들이 수집된다.

| 메트릭 | 설명 |
|--------|------|
| `executor_pool_size_threads` | 현재 스레드 풀 크기 |
| `executor_active_threads` | 활성 스레드 수 |
| `executor_queued_tasks` | 대기열 태스크 수 |
| `executor_completed_tasks_total` | 완료된 태스크 수 |

만약 여러 개의 스케줄러를 사용하고 있다면, 각 스케줄러에 이름을 부여해서 생성하면 스케줄러별로 메트릭을 구분하여 모니터링할 수 있다는 점이 도움이 된다.

```java
@Configuration
public class SchedulerMetricsConfig {

    @Bean
    public Scheduler metricsEnabledBoundedElastic() {
        return Schedulers.newBoundedElastic(
            Schedulers.DEFAULT_BOUNDED_ELASTIC_SIZE,
            Schedulers.DEFAULT_BOUNDED_ELASTIC_QUEUESIZE,
            "custom-bounded-elastic"
        );
    }
}
```

---

## 18.5 분산 추적 (Zipkin / Jaeger)

### 18.5.1 분산 추적의 필요성

우리의 애플리케이션이 점점 커지고 마이크로서비스 구조로 변하면, 하나의 사용자 요청이 수십 개의 서비스를 거쳐 처리되는 일이 생긴다. 이런 상황에서 "어디서 느려졌어?"라는 질문에 답하기 위해서는 분산 추적이 필수다. 분산 추적은 **Trace ID**와 **Span ID**로 요청 전체의 호출 흐름을 연결해서 보여준다.

```
[사용자 요청]
  └─ Trace ID: abc123
      ├─ Span 1: API Gateway (10ms)
      ├─ Span 2: Product Service (25ms)
      │   └─ Span 3: MongoDB 쿼리 (8ms)
      └─ Span 4: Order Service (30ms)
          └─ Span 5: Payment API 호출 (20ms)
```

### 18.5.2 Micrometer Tracing 설정

Spring Boot 3.x부터는 분산 추적의 표준으로 Micrometer Tracing을 사용한다. 이것이 좋은 이유는 Brave(Zipkin) 또는 OpenTelemetry 브릿지 중 원하는 것을 선택해서 사용할 수 있다는 유연성이다.

**Zipkin을 사용하는 경우**:

```groovy
dependencies {
    implementation 'io.micrometer:micrometer-tracing-bridge-brave'
    implementation 'io.zipkin.reporter2:zipkin-reporter-brave'
}
```

**Jaeger를 사용하는 경우 (OpenTelemetry)**:

```groovy
dependencies {
    implementation 'io.micrometer:micrometer-tracing-bridge-otel'
    implementation 'io.opentelemetry:opentelemetry-exporter-zipkin'
}
```

> **참고**: Jaeger는 Zipkin 호환 프로토콜을 지원하므로, Zipkin 리포터로도 Jaeger에 데이터를 전송할 수 있다. 최신 Jaeger는 OTLP(OpenTelemetry Protocol)를 기본 수집 프로토콜로 권장한다.

### 18.5.3 application.yml 설정

설정은 상당히 간단한데, 주의할 점은 `sampling.probability`다. 개발 환경에서는 100%로 설정하고, 운영에서는 필자의 경험상 10% 정도로 줄이는 것이 좋다. 그래야 Zipkin 스토리지에 부담을 주지 않으면서도 충분한 샘플을 수집할 수 있기 때문이다.

```yaml
management:
  tracing:
    sampling:
      probability: 1.0        # 개발: 100%, 운영: 0.1 (10%) 권장
    propagation:
      type: b3                 # W3C 또는 B3 전파 형식
  zipkin:
    tracing:
      endpoint: http://localhost:9411/api/v2/spans

logging:
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] [%X{traceId}/%X{spanId}] %-5level %logger{36} - %msg%n"
```

### 18.5.4 Zipkin / Jaeger Docker 설치

Zipkin은 정말 간단하게 `docker run -d -p 9411:9411 openzipkin/zipkin`으로 실행할 수 있다. Jaeger를 사용하려면 다음과 같이 설정하면 된다.

```yaml
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"    # Jaeger UI
      - "9411:9411"      # Zipkin 호환 포트
      - "4317:4317"      # OTLP gRPC
    environment:
      COLLECTOR_ZIPKIN_HOST_PORT: ":9411"
```

Zipkin UI는 `http://localhost:9411`, Jaeger UI는 `http://localhost:16686`에서 접근한다.

### 18.5.5 WebClient에서의 Trace 전파

외부 서비스를 호출할 때 trace 정보가 자동으로 전파되게 하려면, `WebClient`를 `WebClient.Builder` 빈으로 생성해야 한다. 그러면 Micrometer Tracing이 자동으로 Trace 전파 필터를 추가한다. 여기서 중요한 팁은 `WebClient.create()`를 사용하면 안 되고, 반드시 스프링이 관리하는 `WebClient.Builder`를 주입받아 사용해야 한다는 것이다.

```java
@Configuration
public class WebClientConfig {

    @Bean
    public WebClient externalServiceClient(WebClient.Builder builder) {
        // Builder 빈을 주입받으면 Tracing 필터가 자동 추가됨
        return builder
            .baseUrl("https://external-service.example.com")
            .build();
    }
}
```

이렇게 생성한 `WebClient`로 외부 API를 호출하면, Trace ID가 자동으로 요청 헤더에 포함된다. 나중에 Zipkin UI에서 트레이스를 조회해보면 MongoDB 조회, 외부 API 호출 같은 여러 작업이 각각 별도의 Span으로 기록되면서도, 동일한 Trace ID로 하나로 연결되어 있는 것을 확인할 수 있다. 이것이 분산 추적의 진정한 가치다.

### 18.5.6 커스텀 Span 생성

자동 계측만으로는 충분하지 않을 때도 있다. 특정 메서드나 로직 블록의 성능을 더 상세하게 추적해야 한다면, `@Observed` 어노테이션으로 메서드 단위 Span을 직접 생성하거나, `Observation` API를 사용해서 더 세밀하게 제어할 수 있다.

```java
@Service
public class InventoryService {

    @Observed(name = "inventory.check",
              contextualName = "check-inventory",
              lowCardinalityKeyValues = {"inventory.type", "product"})
    public Mono<Boolean> checkAvailability(String productId, int quantity) {
        return Mono.just(true);
    }
}
```

`@Observed`를 사용하려면 `ObservedAspect` 빈을 등록해야 한다.

```java
@Configuration
public class ObservationConfig {

    @Bean
    public ObservedAspect observedAspect(ObservationRegistry registry) {
        return new ObservedAspect(registry);
    }
}
```

`Observation` API를 사용하면 리액티브 체인 내에서 더 세밀한 Span 제어가 가능하다.

```java
@Service
@RequiredArgsConstructor
public class PaymentProcessService {

    private final ObservationRegistry observationRegistry;

    public Mono<PaymentResult> processPayment(PaymentRequest request) {
        Observation observation = Observation.createNotStarted(
                "payment.process", observationRegistry)
            .lowCardinalityKeyValue("payment.method", request.getPaymentMethod());

        return Mono.just(request)
            .flatMap(this::validatePayment)
            .flatMap(this::executePayment)
            .doOnSubscribe(s -> observation.start())
            .doOnTerminate(observation::stop)
            .doOnError(observation::error);
    }
}
```

---

## 18.6 구조화된 로깅 (Logback + MDC in Reactive)

### 18.6.1 구조화된 로깅의 필요성

로그를 파일에 저장해뒀다가 나중에 문제를 분석하려면, 텍스트 기반 로그로는 원하는 정보를 찾기가 정말 어렵다. 검색도 어렵고 집계도 안 된다. 그래서 운영 환경에서는 ELK(Elasticsearch + Logstash + Kibana)나 Loki 같은 로그 수집 시스템과 연동하는데, 이 경우 **JSON 형식** 로그가 효과적이다.

```
# 기존 텍스트 로그
2026-02-14 10:30:15.123 [reactor-http-nio-3] INFO c.e.s.OrderService - 주문 생성 완료: orderId=abc123
```

```json
// 구조화된 JSON 로그
{
  "timestamp": "2026-02-14T10:30:15.123Z",
  "level": "INFO",
  "logger": "com.example.shop.OrderService",
  "message": "주문 생성 완료",
  "traceId": "6a3f7b2c1d4e5f",
  "spanId": "a1b2c3d4",
  "orderId": "abc123",
  "userId": "user-456",
  "service": "webflux-shop"
}
```

### 18.6.2 Logback JSON 설정

로그를 JSON 형식으로 만들려면 `logstash-logback-encoder` 라이브러리를 사용하면 된다. 매우 편하다.

```groovy
dependencies {
    implementation 'net.logstash.logback:logstash-logback-encoder:7.4'
}
```

```xml
<!-- src/main/resources/logback-spring.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <springProperty scope="context" name="APP_NAME"
                    source="spring.application.name" defaultValue="webflux-app"/>

    <!-- 개발 환경: 텍스트 로그 -->
    <springProfile name="local,dev">
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder>
                <pattern>%d{HH:mm:ss.SSS} [%thread] [%X{traceId:-}/%X{spanId:-}] %-5level %logger{36} - %msg%n</pattern>
            </encoder>
        </appender>
        <root level="INFO"><appender-ref ref="CONSOLE"/></root>
    </springProfile>

    <!-- 운영 환경: JSON 로그 -->
    <springProfile name="prod,staging">
        <appender name="JSON_CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder class="net.logstash.logback.encoder.LogstashEncoder">
                <includeMdcKeyName>traceId</includeMdcKeyName>
                <includeMdcKeyName>spanId</includeMdcKeyName>
                <includeMdcKeyName>userId</includeMdcKeyName>
                <includeMdcKeyName>requestId</includeMdcKeyName>
                <customFields>{"service":"${APP_NAME}"}</customFields>
                <timeZone>UTC</timeZone>
            </encoder>
        </appender>
        <root level="INFO"><appender-ref ref="JSON_CONSOLE"/></root>
    </springProfile>
</configuration>
```

### 18.6.3 리액티브 환경에서의 MDC 문제와 해결

전통적인 서블릿 애플리케이션에서는 MDC(Mapped Diagnostic Context)가 `ThreadLocal` 기반으로 동작하기 때문에 각 요청별로 로그를 추적하는 것이 쉽다. 그런데 리액티브 환경은 다르다. 하나의 요청이 여러 스레드를 넘나들며 처리되기 때문에, `publishOn()`이나 `subscribeOn()`으로 스레드가 전환되면 기존 MDC 값이 유실되는 문제가 생긴다.

Spring Boot 3.x부터는 `context-propagation` 라이브러리와 `Hooks.enableAutomaticContextPropagation()`을 사용해서 이 문제를 깔끔하게 해결할 수 있다. 18.4.1에서 설정한 것처럼 이것을 활성화하면 `traceId`와 `spanId`가 자동으로 MDC에 전파된다. 만약 `userId`나 `requestId` 같은 비즈니스 컨텍스트를 추가로 전파하려면, `WebFilter`와 `ThreadLocalAccessor`를 구현해서 처리하면 된다.

### 18.6.4 커스텀 컨텍스트 전파

이제 실제로 구현해보자. `WebFilter`에서 Reactor Context에 값을 저장하고, `ThreadLocalAccessor`를 통해 MDC와 자동으로 연결하면 된다.

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class ContextPropagationFilter implements WebFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange,
                             WebFilterChain chain) {
        String requestId = Optional.ofNullable(
                exchange.getRequest().getHeaders().getFirst("X-Request-Id"))
            .orElse(UUID.randomUUID().toString().substring(0, 12));

        return exchange.getPrincipal()
            .map(Principal::getName)
            .defaultIfEmpty("anonymous")
            .flatMap(userId -> chain.filter(exchange)
                .contextWrite(ctx -> ctx
                    .put("requestId", requestId)
                    .put("userId", userId)));
    }
}
```

그 다음, `ThreadLocalAccessor`를 구현해서 Reactor Context와 MDC 간의 자동 전파를 설정한다.

```java
public class UserIdThreadLocalAccessor implements ThreadLocalAccessor<String> {

    public static final String KEY = "userId";

    @Override
    public Object key() { return KEY; }

    @Override
    public String getValue() { return MDC.get(KEY); }

    @Override
    public void setValue(String value) { MDC.put(KEY, value); }

    @Override
    public void reset() { MDC.remove(KEY); }
}
```

`ThreadLocalAccessor` 구현체는 `ContextRegistry`에 등록하면 자동으로 작동한다. `requestId`도 `userId`와 동일한 패턴으로 구현해서 등록하면 되니까 복잡하지 않다.

```java
@Configuration
public class ContextPropagationConfig {

    @PostConstruct
    public void init() {
        ContextRegistry.getInstance()
            .registerThreadLocalAccessor(new UserIdThreadLocalAccessor());
        ContextRegistry.getInstance()
            .registerThreadLocalAccessor(new RequestIdThreadLocalAccessor());
    }
}
```

이 설정을 마치면, 스레드가 몇 번 전환되더라도 `userId`와 `requestId`가 MDC에 자동으로 전파되고, 결국 JSON 로그에 모두 포함되게 된다.

### 18.6.5 구조화된 로그 작성 패턴

마지막으로, 실제로 로그를 작성할 때는 `logstash-logback-encoder`의 `StructuredArguments`를 사용하면 로그 메시지와 JSON 필드를 동시에 기록할 수 있다. 이렇게 하면 나중에 Kibana에서 필드 기반으로 검색하고 집계하기가 훨씬 쉬워진다.

```java
import static net.logstash.logback.argument.StructuredArguments.*;

@Service
@Slf4j
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;

    public Mono<Order> createOrder(OrderRequest request) {
        return orderRepository.save(Order.from(request))
            .doOnSuccess(order ->
                log.info("주문 생성 완료: {} {} {}",
                    keyValue("orderId", order.getId()),
                    keyValue("amount", order.getTotalAmount()),
                    keyValue("items", order.getItems().size())))
            .doOnError(ex ->
                log.error("주문 생성 실패: {} {}",
                    keyValue("userId", request.getUserId()),
                    keyValue("error", ex.getMessage()), ex));
        // JSON: {"message":"주문 생성 완료: orderId=abc amount=15000 items=3",
        //        "orderId":"abc", "amount":15000, "items":3, ...}
    }
}
```

---

## 요약

이 장에서 다룬 내용을 정리하면 다음과 같다.

| 주제 | 핵심 내용 |
|------|----------|
| **Actuator** | `health`, `info`, `metrics`, `prometheus` 엔드포인트 노출, `ReactiveHealthIndicator`로 논블로킹 상태 확인, 포트 분리와 Security 연동으로 보안 강화 |
| **Micrometer + Prometheus** | `Counter`(단조 증가), `Gauge`(현재 값), `Timer`(소요 시간 + 호출 수) 커스텀 메트릭, `prometheus.yml`로 스크래핑 설정 |
| **Grafana** | Docker 설치, Prometheus 데이터소스 프로비저닝, 커뮤니티 대시보드 임포트, PromQL로 커스텀 패널, 알림 규칙 설정 |
| **리액티브 메트릭** | `.name().tag().metrics()`로 Reactor 체인 메트릭 수집, `Schedulers.enableMetrics()`로 스케줄러 모니터링 |
| **분산 추적** | Micrometer Tracing + Brave(Zipkin) 또는 OpenTelemetry(Jaeger), `WebClient.Builder` 빈으로 자동 Trace 전파, `@Observed`로 커스텀 Span |
| **구조화된 로깅** | `logstash-logback-encoder`로 JSON 로그, `Hooks.enableAutomaticContextPropagation()`으로 Reactor Context-MDC 자동 전파, `ThreadLocalAccessor`로 커스텀 컨텍스트 전파 |

다음 장에서는 완성된 애플리케이션의 성능을 어떻게 측정하고 최적화할지 배워보겠다. MongoDB 커넥션 풀 튜닝부터 시작해서, Netty 이벤트 루프 최적화, 캐싱, BlockHound를 활용한 블로킹 코드 탐지, 그리고 Gatling과 k6를 이용한 실전 부하 테스트까지 다룰 것이다.
# Chapter 19. 성능 최적화

리액티브 아키텍처를 채택했다고 자동으로 높은 성능이 따라오는 건 아니다. 실제로 논블로킹 모델의 이점을 제대로 누리려면, 병목 지점을 정확히 측정하고, 커넥션 풀과 이벤트 루프를 우리 애플리케이션 특성에 맞게 조정해야 한다. 여기에 캐싱으로 불필요한 I/O를 줄이고, 블로킹 코드를 철저히 제거해야 진정한 고성능을 얻을 수 있다. 이번 장에서는 리액티브 애플리케이션의 **성능 측정 방법**부터 **MongoDB 커넥션 풀 튜닝**, **Netty 이벤트 루프 최적화**, **캐싱 전략**, **BlockHound를 활용한 블로킹 탐지**, 그리고 **Gatling/k6를 활용한 부하 테스트**까지 실전 성능 최적화의 전 과정을 살펴본다.

---

## 19.1 리액티브 애플리케이션 성능 측정

성능 최적화의 첫 번째 원칙은 간단하다: **측정 없이 최적화하지 말 것**. 감에 의존한 최적화는 코드 복잡도만 높일 뿐, 실질적인 개선을 가져오지 않는다.

### 19.1.1 핵심 성능 지표

성능을 이야기할 때 보통 세 가지 축으로 나눠서 본다.

| 지표 | 설명 | 측정 단위 |
|------|------|----------|
| **처리량(Throughput)** | 단위 시간당 처리한 요청 수 | req/sec |
| **지연시간(Latency)** | 요청 시작부터 응답 완료까지 소요 시간 | ms (p50, p95, p99) |
| **리소스 사용률** | CPU, 메모리, 스레드, 커넥션 점유율 | %, 개수 |

리액티브 애플리케이션의 핵심은 적은 스레드로 높은 처리량을 달성하는 것이다. 그래서 스레드 수 대비 처리량의 비율이 정말 중요한 평가 기준이 된다. 지연시간을 볼 때도 단순 평균은 거의 무의미하다. p95, p99 같은 백분위를 봐야 실제 사용자가 경험하는 성능을 알 수 있다.

```
[전통적 MVC 모델]
스레드 200개 → 동시 처리 200 요청 → 처리량 ~2,000 req/sec

[리액티브 모델]
스레드 8개(이벤트 루프) → 동시 처리 수천 요청 → 처리량 ~10,000+ req/sec
```

### 19.1.2 Micrometer 메트릭 활용

이전 장에서 설정한 Micrometer를 이제 성능 분석에 적극 활용해야 한다. WebFlux가 자동으로 수집하는 핵심 메트릭들을 보자.

| 메트릭 이름 | 설명 |
|------------|------|
| `http.server.requests` | HTTP 요청 처리 시간 (타이머) |
| `reactor.netty.http.server.data.received` | 서버가 수신한 데이터 바이트 |
| `mongodb.driver.pool.size` | MongoDB 커넥션 풀 크기 |
| `mongodb.driver.pool.waitqueuesize` | MongoDB 커넥션 대기 큐 크기 |
| `jvm.threads.live` | 활성 JVM 스레드 수 |

이런 기본 메트릭 외에 커스텀 메트릭을 추가하면 비즈니스 로직의 성능도 측정할 수 있다.

```java
@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;
    private final MeterRegistry meterRegistry;

    public Mono<Product> findById(String id) {
        return Mono.defer(() -> {
            Timer.Sample sample = Timer.start(meterRegistry);

            return productRepository.findById(id)
                .doOnSuccess(p -> sample.stop(
                    Timer.builder("product.findById")
                        .tag("result", p != null ? "found" : "not_found")
                        .register(meterRegistry)
                ))
                .doOnError(e -> sample.stop(
                    Timer.builder("product.findById")
                        .tag("result", "error")
                        .register(meterRegistry)
                ));
        });
    }
}
```

### 19.1.3 JMH 마이크로벤치마크

JMH(Java Microbenchmark Harness)라는 도구를 알고 있나? JVM 수준의 정밀한 벤치마크를 할 때 필자도 자주 쓰는 도구인데, `build.gradle`에 플러그인을 추가하면 쉽게 시작할 수 있다.

```groovy
plugins {
    id 'me.champeau.jmh' version '0.7.2'
}

dependencies {
    jmh 'org.openjdk.jmh:jmh-core:1.37'
    jmh 'org.openjdk.jmh:jmh-generator-annprocess:1.37'
}
```

Reactor 연산자들의 성능 차이를 실제로 비교해보는 벤치마크를 작성해보자.

```java
@State(Scope.Thread)
@BenchmarkMode({Mode.Throughput, Mode.AverageTime})
@OutputTimeUnit(TimeUnit.MILLISECONDS)
public class ReactorBenchmark {

    private List<String> items;

    @Setup
    public void setup() {
        items = IntStream.range(0, 10_000)
            .mapToObj(i -> "item-" + i)
            .collect(Collectors.toList());
    }

    @Benchmark
    public void flatMap_동시성_기본값(Blackhole bh) {
        bh.consume(Flux.fromIterable(items)
            .flatMap(item -> Mono.fromCallable(() -> item.toUpperCase()))
            .collectList()
            .block());
    }

    @Benchmark
    public void map_단순변환(Blackhole bh) {
        bh.consume(Flux.fromIterable(items)
            .map(String::toUpperCase)
            .collectList()
            .block());
    }
}
```

> **참고**: `map`은 동기 변환이므로 `flatMap`보다 훨씬 빠르다. 비동기 I/O가 불필요한 단순 변환에는 항상 `map`을 사용해야 한다.

### 19.1.4 프로파일링 도구

프로파일링 도구도 여러 가지가 있으니 상황에 맞춰 고르면 된다.

| 도구 | 용도 | 특징 |
|------|------|------|
| **VisualVM** | CPU/메모리 프로파일링 | 무료, JDK 번들 |
| **async-profiler** | 저오버헤드 CPU/메모리 프로파일링 | 프로덕션 환경 사용 가능 |
| **JDK Flight Recorder (JFR)** | 포괄적 런타임 분석 | JDK 11+, 프로덕션 안전 |
| **IntelliJ Profiler** | IDE 통합 프로파일링 | 개발 시 편리 |

```bash
# async-profiler 실행 (애플리케이션 PID: 12345)
./asprof -d 30 -f profile.html -e cpu 12345

# JFR 기록 시작
java -XX:+FlightRecorder \
     -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     -jar application.jar
```

리액티브 애플리케이션의 프로파일링에서 꼭 봐야 할 부분이 하나 있다. 이벤트 루프 스레드(`reactor-http-nio-*`)의 CPU 사용률이 80%를 넘으면 병목 가능성이 매우 높다는 신호다. 필자의 경험상 이 지표가 80%를 넘으면 대부분 무거운 연산이 이벤트 루프에서 직접 실행되고 있었다. 이런 경우 별도 스케줄러로 그 작업을 오프로드하면 눈에 띄게 개선된다.

---

## 19.2 MongoDB 커넥션 풀 튜닝

MongoDB 드라이버가 내부적으로 커넥션 풀을 관리하는데, 이 풀의 설정이 전체 처리량에 미치는 영향은 정말 크다. 풀 크기, 타임아웃, 유휴 커넥션 관리 방식을 어떻게 설정하는지에 따라 성능이 크게 달라진다.

### 19.2.1 기본 커넥션 풀 동작

MongoDB Reactive Streams 드라이버의 커넥션 풀 기본값은 다음과 같다.

| 설정 | 기본값 | 설명 |
|------|--------|------|
| `minPoolSize` | 0 | 최소 유지 커넥션 수 |
| `maxPoolSize` | 100 | 최대 커넥션 수 |
| `maxWaitTime` | 120초 | 커넥션 획득 대기 시간 |
| `maxConnectionIdleTime` | 0 (무제한) | 유휴 커넥션 유지 시간 |
| `maxConnectionLifeTime` | 0 (무제한) | 커넥션 최대 수명 |

### 19.2.2 MongoClientSettings를 활용한 커넥션 풀 설정

`application.yml`에 URI 파라미터로 설정하는 방법도 있지만, `MongoClientSettings` 빈을 직접 구성하면 훨씬 세밀한 제어가 가능하다. 이게 실무에서는 훨씬 흔한 방식이다.

```java
@Configuration
public class MongoConfig extends AbstractReactiveMongoConfiguration {

    @Value("${spring.data.mongodb.uri}")
    private String mongoUri;

    @Override
    protected String getDatabaseName() {
        return "myapp";
    }

    @Override
    @Bean
    public MongoClient reactiveMongoClient() {
        ConnectionString connString = new ConnectionString(mongoUri);

        MongoClientSettings settings = MongoClientSettings.builder()
            .applyConnectionString(connString)
            .applyToConnectionPoolSettings(pool -> pool
                .minSize(10)                                     // 최소 커넥션
                .maxSize(50)                                     // 최대 커넥션
                .maxWaitTime(5, TimeUnit.SECONDS)                // 커넥션 대기 타임아웃
                .maxConnectionIdleTime(30, TimeUnit.SECONDS)     // 유휴 커넥션 정리
                .maxConnectionLifeTime(5, TimeUnit.MINUTES)      // 커넥션 최대 수명
                .maintenanceFrequency(30, TimeUnit.SECONDS)      // 정리 주기
            )
            .applyToSocketSettings(socket -> socket
                .connectTimeout(3, TimeUnit.SECONDS)
                .readTimeout(10, TimeUnit.SECONDS)
            )
            .applyToServerSettings(server -> server
                .heartbeatFrequency(10, TimeUnit.SECONDS)
                .minHeartbeatFrequency(500, TimeUnit.MILLISECONDS)
            )
            .build();

        return MongoClients.create(settings);
    }
}
```

### 19.2.3 풀 크기 산정 가이드라인

풀 크기를 정할 때는 다음 공식을 기준으로 생각하면 된다.

```
최적 풀 크기 = (동시 요청 수) x (평균 쿼리 시간) / (목표 응답 시간)
```

예시를 들어보자. 동시 요청이 500건이고, 평균 쿼리 시간이 10ms, 목표 응답 시간이 100ms라면? 계산하면 `500 x 10 / 100 = 50`이 나온다. 이게 적정 풀 크기다.

| 시나리오 | minSize | maxSize | 근거 |
|----------|---------|---------|------|
| **개발 환경** | 2 | 10 | 리소스 절약 |
| **소규모 서비스** | 5 | 30 | 동시 사용자 ~100명 |
| **중규모 서비스** | 10 | 50 | 동시 사용자 ~1,000명 |
| **대규모 서비스** | 20 | 100 | 동시 사용자 ~10,000명 |

> **주의**: `maxSize`를 무조건 크게 잡으면 MongoDB 서버 측 리소스가 고갈될 수 있다. 모든 애플리케이션 인스턴스의 `maxSize` 합이 MongoDB의 `net.maxIncomingConnections`(기본 65,536)의 80%를 넘지 않도록 한다.

### 19.2.4 커넥션 풀 모니터링과 타임아웃

이제 실제로 커넥션 풀이 잘 동작하는지 모니터링해야 한다. 메트릭을 활성화하고, 타임아웃은 계층별로 정리해서 설정해보자.

```yaml
# application.yml
management:
  metrics:
    mongo:
      connectionpool:
        enabled: true
      command:
        enabled: true
```

```
# Prometheus 메트릭 예시
mongodb_driver_pool_size{server_address="localhost:27017"} 25
mongodb_driver_pool_checkedout{server_address="localhost:27017"} 12
mongodb_driver_pool_waitqueuesize{server_address="localhost:27017"} 0
```

`waitqueuesize`가 계속 0보다 크다는 건 위험한 신호다. `maxSize`를 늘리거나, 아니면 쿼리 자체를 더 빠르게 만들어야 한다는 뜻이다. 타임아웃은 다음처럼 계층별로 구성하는 게 좋다.

```
소켓 타임아웃 (connectTimeout, readTimeout)
  └─ 쿼리 타임아웃 (maxTime)
       └─ Reactor 타임아웃 (timeout 연산자)
            └─ HTTP 응답 타임아웃 (WebFlux 타임아웃)
```

```java
public Flux<Product> findByCategory(String category) {
    Query query = new Query(Criteria.where("category").is(category))
        .maxTime(Duration.ofSeconds(5));  // 쿼리 레벨 타임아웃 (5초)

    return mongoTemplate.find(query, Product.class)
        .timeout(Duration.ofSeconds(10));  // Reactor 레벨 타임아웃
}
```

---

## 19.3 Netty 이벤트 루프 최적화

Spring WebFlux는 내부적으로 Reactor Netty를 기본 서버로 쓰고 있다. Netty의 이벤트 루프를 어떻게 설정하는지가 전체 처리량을 좌우한다고 해도 과언이 아니다.

### 19.3.1 이벤트 루프 기본 구조

```
[Boss EventLoopGroup]       <- 새 커넥션 수락 (accept)
  └─ 스레드 1개 (보통)

[Worker EventLoopGroup]     <- I/O 이벤트 처리 (read/write)
  └─ 스레드 N개 (기본: CPU 코어 수)
    ├─ reactor-http-nio-1
    ├─ reactor-http-nio-2
    └─ reactor-http-nio-N
```

### 19.3.2 LoopResources를 활용한 이벤트 루프 커스터마이징

```java
@Configuration
public class NettyConfig {

    @Bean
    public NettyReactiveWebServerFactory nettyFactory() {
        NettyReactiveWebServerFactory factory = new NettyReactiveWebServerFactory();

        factory.addServerCustomizers(httpServer -> {
            LoopResources loopResources = LoopResources.create(
                "custom-http",      // 스레드 이름 접두사
                1,                  // selector 스레드 수 (accept)
                Runtime.getRuntime().availableProcessors() * 2,  // worker 스레드 수
                true                // 데몬 스레드 여부
            );

            return httpServer
                .runOn(loopResources)
                .option(ChannelOption.SO_BACKLOG, 2048)          // 연결 대기 큐
                .childOption(ChannelOption.SO_KEEPALIVE, true)   // TCP Keep-Alive
                .childOption(ChannelOption.TCP_NODELAY, true);   // Nagle 알고리즘 비활성화
        });

        return factory;
    }
}
```

### 19.3.3 Native Transport (Epoll, KQueue)

JVM의 표준 NIO를 쓸 수도 있지만, 운영체제 수준의 네이티브 I/O를 사용하면 성능이 훨씬 좋아진다. 필자의 경험상 프로덕션 환경에서는 이 차이가 꽤 크게 느껴진다.

| Transport | 운영체제 | 장점 |
|-----------|---------|------|
| **NIO** (기본) | 모든 OS | 호환성 |
| **Epoll** | Linux | 낮은 지연시간, edge-triggered I/O |
| **KQueue** | macOS, BSD | macOS에서 최적 성능 |

```groovy
dependencies {
    // Linux Epoll
    runtimeOnly 'io.netty:netty-transport-native-epoll::linux-x86_64'

    // macOS KQueue (Intel / Apple Silicon)
    runtimeOnly 'io.netty:netty-transport-native-kqueue::osx-x86_64'
    runtimeOnly 'io.netty:netty-transport-native-kqueue::osx-aarch_64'
}
```

```java
@Configuration
public class NativeTransportConfig {

    @Bean
    public NettyReactiveWebServerFactory nettyFactory() {
        NettyReactiveWebServerFactory factory = new NettyReactiveWebServerFactory();

        factory.addServerCustomizers(httpServer -> {
            LoopResources loopResources = LoopResources.create(
                "native-http", 1,
                Runtime.getRuntime().availableProcessors(), true
            );
            return httpServer.runOn(loopResources, true);  // preferNative = true
        });

        return factory;
    }
}
```

`preferNative`를 `true`로 설정하면 Reactor Netty가 플랫폼에 맞는 네이티브 Transport를 자동으로 선택한다. 네이티브 라이브러리가 없으면 NIO로 자동 폴백한다.

### 19.3.4 이벤트 루프 블로킹 방지

이벤트 루프 스레드에서 블로킹 작업을 하면 안 된다. 이건 리액티브 프로그래밍의 대원칙이다. 무거운 연산은 별도 스케줄러로 넘기자.

```java
@Service
public class ReportService {

    // CPU 집약적 작업 전용 스케줄러
    private final Scheduler cpuScheduler = Schedulers.newParallel(
        "cpu-worker", Runtime.getRuntime().availableProcessors());

    // 레거시 블로킹 코드 전용 스케줄러
    private final Scheduler blockingScheduler = Schedulers.newBoundedElastic(
        100, 10_000, "blocking-worker", 60);

    public Mono<Report> generateReport(String reportId) {
        return loadData(reportId)
            .publishOn(cpuScheduler)         // CPU 작업은 별도 스레드에서
            .map(this::heavyComputation)
            .flatMap(this::saveReport);
    }

    public Mono<LegacyData> callLegacyApi(String id) {
        return Mono.fromCallable(() -> legacyService.getById(id))
            .subscribeOn(blockingScheduler);  // 블로킹 전용 스레드에서 실행
    }
}
```

---

## 19.4 캐싱 전략 (Caffeine, Redis)

I/O 연산을 줄이는 가장 확실한 방법은 뭘까? 그건 캐싱이다. 다만 리액티브 애플리케이션에서는 캐시 조회 자체도 논블로킹으로 이루어져야 한다는 점을 잊으면 안 된다.

### 19.4.1 Caffeine 로컬 캐시

Caffeine은 JVM 에서 쓸 수 있는 고성능 로컬 캐시 라이브러리다. 리액티브 환경에 맞게 래퍼 클래스를 한 번 만들어놓으면, 여러 곳에서 쉽게 재사용할 수 있다.

```groovy
dependencies {
    implementation 'com.github.ben-manes.caffeine:caffeine:3.1.8'
}
```

```java
@Component
public class ReactiveCaffeineCache<K, V> {

    private final Cache<K, V> cache;

    public ReactiveCaffeineCache(int maxSize, Duration ttl) {
        this.cache = Caffeine.newBuilder()
            .maximumSize(maxSize)
            .expireAfterWrite(ttl)
            .recordStats()
            .build();
    }

    public Mono<V> get(K key) {
        return Mono.justOrEmpty(cache.getIfPresent(key));
    }

    public Mono<V> get(K key, Function<K, Mono<V>> loader) {
        V cached = cache.getIfPresent(key);
        if (cached != null) {
            return Mono.just(cached);
        }
        return loader.apply(key)
            .doOnNext(value -> cache.put(key, value));
    }

    public Mono<Void> put(K key, V value) {
        cache.put(key, value);
        return Mono.empty();
    }

    public Mono<Void> evict(K key) {
        cache.invalidate(key);
        return Mono.empty();
    }
}
```

이제 이 캐시를 서비스에서 실제로 어떻게 써야 하는지 보자.

```java
@Service
public class ProductService {

    private final ProductRepository productRepository;
    private final ReactiveCaffeineCache<String, Product> productCache;

    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
        this.productCache = new ReactiveCaffeineCache<>(10_000, Duration.ofMinutes(5));
    }

    public Mono<Product> findById(String id) {
        return productCache.get(id, key -> productRepository.findById(key));
    }

    public Mono<Product> update(String id, ProductUpdateRequest request) {
        return productRepository.findById(id)
            .flatMap(product -> {
                product.setName(request.getName());
                product.setPrice(request.getPrice());
                return productRepository.save(product);
            })
            .doOnNext(product -> productCache.put(id, product));
    }

    public Mono<Void> delete(String id) {
        return productRepository.deleteById(id)
            .then(productCache.evict(id));
    }
}
```

### 19.4.2 Reactive Redis 분산 캐시

애플리케이션이 여러 인스턴스로 운영되는 환경이면? 이때는 Reactive Redis를 분산 캐시로 써야 한다. 로컬 캐시만으로는 인스턴스 간에 데이터가 동기화되지 않기 때문이다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-data-redis-reactive'
}
```

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379
      timeout: 3s
      lettuce:
        pool:
          max-active: 50
          max-idle: 10
          min-idle: 5
```

```java
@Service
@RequiredArgsConstructor
public class RedisCacheService {

    private final ReactiveStringRedisTemplate redisTemplate;
    private final ObjectMapper objectMapper;

    public <T> Mono<T> getOrLoad(String key, Class<T> type,
                                  Duration ttl, Mono<T> loader) {
        return redisTemplate.opsForValue()
            .get(key)
            .flatMap(json -> deserialize(json, type))
            .switchIfEmpty(
                loader.flatMap(value ->
                    serialize(value)
                        .flatMap(json ->
                            redisTemplate.opsForValue()
                                .set(key, json, ttl)
                                .thenReturn(value)
                        )
                )
            );
    }

    public Mono<Boolean> evict(String key) {
        return redisTemplate.delete(key).map(count -> count > 0);
    }

    private <T> Mono<T> deserialize(String json, Class<T> type) {
        return Mono.fromCallable(() -> objectMapper.readValue(json, type))
            .onErrorResume(e -> Mono.empty());  // 역직렬화 실패 시 캐시 미스 처리
    }

    private <T> Mono<String> serialize(T value) {
        return Mono.fromCallable(() -> objectMapper.writeValueAsString(value));
    }
}
```

### 19.4.3 멀티 레벨 캐시 전략

로컬 캐시(Caffeine)와 분산 캐시(Redis)를 함께 쓰면 어떻게 될까? **L1/L2 캐시** 구조로 만들면 성능도 좋고 데이터 일관성도 유지할 수 있다.

```java
@Service
public class MultiLevelCacheService<T> {

    private final ReactiveCaffeineCache<String, T> l1Cache;   // 로컬
    private final RedisCacheService redisCacheService;         // 분산

    public MultiLevelCacheService(RedisCacheService redisCacheService) {
        this.l1Cache = new ReactiveCaffeineCache<>(5_000, Duration.ofMinutes(1));
        this.redisCacheService = redisCacheService;
    }

    public Mono<T> get(String key, Class<T> type,
                       Duration redisTtl, Mono<T> loader) {
        // L1 (Caffeine) -> L2 (Redis) -> 원본 데이터 소스
        return l1Cache.get(key)
            .switchIfEmpty(
                redisCacheService.getOrLoad(key, type, redisTtl, loader)
                    .doOnNext(value -> l1Cache.put(key, value))
            );
    }

    public Mono<Void> evict(String key) {
        return l1Cache.evict(key)
            .then(redisCacheService.evict(key))
            .then();
    }
}
```

```
요청 -> [L1 Caffeine 캐시] --히트--> 즉시 반환 (< 1ms)
              | 미스
              v
       [L2 Redis 캐시]    --히트--> L1에 저장 후 반환 (~1-3ms)
              | 미스
              v
       [MongoDB 조회]     -------> L1+L2에 저장 후 반환 (~5-50ms)
```

---

## 19.5 블로킹 코드 탐지 및 제거 (BlockHound)

리액티브 애플리케이션에서 가장 위험한 함정이 하나 있다. 바로 **이벤트 루프 스레드에서 몰래 일어나는 블로킹 호출**이다. 단 한 줄의 블로킹 코드도 전체 처리량을 극적으로 떨어뜨릴 수 있다. BlockHound는 이런 위험한 호출들을 런타임에 자동으로 발견해주는 도구다. Java Agent 방식으로 동작해서 코드 수정 없이도 탐지가 가능하다.

### 19.5.1 BlockHound 설정

```groovy
dependencies {
    testImplementation 'io.projectreactor.tools:blockhound:1.0.9.RELEASE'
}
```

```java
@SpringBootTest
class ApplicationBlockingTest {

    @BeforeAll
    static void setup() {
        BlockHound.install();
    }

    @Test
    void 블로킹_호출_없음_검증() {
        Mono.delay(Duration.ofMillis(1))
            .doOnNext(it -> {
                // 이벤트 루프 스레드에서 실행됨
                // 여기서 블로킹 호출이 있으면 예외 발생
            })
            .block();
    }
}
```

### 19.5.2 흔한 블로킹 코드 패턴과 수정

실무에서 자주 만나는 블로킹 코드들을 몇 가지 패턴으로 정리해봤다. 이 예시들을 알아두면 코드 리뷰할 때도 도움이 될 것 같다.

**패턴 1: 파일 I/O**

```java
// 블로킹 (위험)
public Mono<String> readFile(String path) {
    return Mono.just(Files.readString(Path.of(path)));  // 블로킹!
}

// 논블로킹 (수정)
public Mono<String> readFile(String path) {
    return Mono.fromCallable(() -> Files.readString(Path.of(path)))
        .subscribeOn(Schedulers.boundedElastic());
}
```

**패턴 2: Thread.sleep()**

```java
// 블로킹 (위험)
return Mono.fromCallable(() -> { Thread.sleep(1000); return "delayed"; });

// 논블로킹 (수정)
return Mono.delay(Duration.ofSeconds(1)).thenReturn("delayed");
```

**패턴 3: 동기 HTTP 호출**

```java
// 블로킹 (위험) - RestTemplate 사용
ExternalData data = restTemplate.getForObject(url, ExternalData.class);
return Mono.justOrEmpty(data);

// 논블로킹 (수정) - WebClient 사용
return webClient.get().uri(url).retrieve().bodyToMono(ExternalData.class);
```

**패턴 4: JDBC 호출**

```java
// 블로킹 (위험)
return Mono.justOrEmpty(jdbcTemplate.queryForObject(sql, mapper, id));

// 논블로킹 (수정 방법 1: boundedElastic으로 격리)
return Mono.fromCallable(() -> jdbcTemplate.queryForObject(sql, mapper, id))
    .subscribeOn(Schedulers.boundedElastic());

// 논블로킹 (수정 방법 2: R2DBC 사용 - Chapter 15 참조)
return r2dbcUserRepository.findById(id);
```

### 19.5.3 BlockHound 커스텀 설정과 테스트 활용

BlockHound도 완벽하진 않다. 특정 라이브러리가 의도적으로 블로킹 호출을 해야 한다면? 그땐 그걸 명시적으로 허용해야 한다. 커스텀 설정으로 탐지 규칙을 조정할 수 있다.

```java
@BeforeAll
static void setup() {
    BlockHound.install(builder -> builder
        // 특정 클래스/메서드의 블로킹 허용 (레거시 라이브러리 등)
        .allowBlockingCallsInside(
            "com.example.legacy.LegacyService", "initialize")
        // 특정 스레드 이름 패턴 제외
        .nonBlockingThreadPredicate(current ->
            current.or(t -> t.getName().startsWith("blocking-worker")))
    );
}
```

StepVerifier와 BlockHound를 함께 쓰면 블로킹 호출을 자동으로 잡아내는 테스트를 만들 수 있다.

```java
@SpringBootTest
class ProductServiceBlockingTest {

    @BeforeAll
    static void setup() {
        BlockHound.install();
    }

    @Autowired
    private ProductService productService;

    @Test
    void findById_논블로킹_검증() {
        StepVerifier.create(
            Mono.defer(() -> productService.findById("test-id"))
                .subscribeOn(Schedulers.parallel())  // 논블로킹 스레드에서 실행
        )
        .expectNextCount(1)
        .verifyComplete();
        // 블로킹 호출이 있으면 ReactorBlockHoundIntegration 예외 발생
    }
}
```

> **참고**: BlockHound는 프로덕션에서는 절대 켜면 안 된다. JVM Agent 방식이라 오버헤드가 크고, 초기화 같은 정당한 블로킹 호출에서도 예외를 던진다. 개발이나 테스트, 스테이징 환경에만 켜두자.

---

## 19.6 부하 테스트 (Gatling, k6)

지금까지 최적화 기법들을 봤는데, 이게 실제로 효과가 있는지 어떻게 알까? 실제 부하 조건에서 테스트해야 한다.

### 19.6.1 Gatling 부하 테스트

Gatling은 부하 테스트를 위한 강력한 도구다. Scala로 만들어졌지만, Java DSL을 써서 테스트 시나리오를 작성할 수도 있다.

```groovy
plugins {
    id 'io.gatling.gradle' version '3.11.5.2'
}

dependencies {
    gatlingImplementation 'io.gatling.highcharts:gatling-charts-highcharts:3.11.5'
}
```

```java
// src/gatling/java/simulations/ProductApiSimulation.java
public class ProductApiSimulation extends Simulation {

    HttpProtocolBuilder httpProtocol = http
        .baseUrl("http://localhost:8080")
        .acceptHeader("application/json")
        .contentTypeHeader("application/json");

    ScenarioBuilder listProducts = scenario("제품 목록 조회")
        .exec(
            http("GET /api/products")
                .get("/api/products")
                .queryParam("page", "0")
                .queryParam("size", "20")
                .check(status().is(200))
        )
        .pause(Duration.ofMillis(100), Duration.ofMillis(500));

    ScenarioBuilder createProduct = scenario("제품 등록")
        .exec(
            http("POST /api/products")
                .post("/api/products")
                .body(StringBody("""
                    {"name":"테스트 상품","price":10000,"category":"electronics"}
                    """))
                .check(status().is(201))
        )
        .pause(Duration.ofMillis(200), Duration.ofMillis(1000));

    {
        setUp(
            listProducts.injectOpen(
                rampUsersPerSec(10).to(200).during(Duration.ofMinutes(2)),
                constantUsersPerSec(200).during(Duration.ofMinutes(3)),
                rampUsersPerSec(200).to(500).during(Duration.ofMinutes(2)),
                constantUsersPerSec(500).during(Duration.ofMinutes(3))
            ),
            createProduct.injectOpen(
                constantUsersPerSec(20).during(Duration.ofMinutes(10))
            )
        ).protocols(httpProtocol)
         .assertions(
             global().responseTime().percentile3().lt(500),
             global().successfulRequests().percent().gt(99.0)
         );
    }
}
```

### 19.6.2 k6 부하 테스트

k6는 좀 더 현대적이고 간단한 부하 테스트 도구다. Go로 만들어졌고, JavaScript로 테스트를 작성하면 된다. CLI로 실행하는 것도 정말 간단하다.

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const productListDuration = new Trend('product_list_duration');

export const options = {
    stages: [
        { duration: '1m', target: 50 },
        { duration: '3m', target: 200 },
        { duration: '2m', target: 500 },
        { duration: '3m', target: 500 },
        { duration: '1m', target: 0 },
    ],
    thresholds: {
        http_req_duration: ['p(95)<500', 'p(99)<1000'],
        errors: ['rate<0.01'],
    },
};

const BASE_URL = 'http://localhost:8080';

export default function () {
    const listRes = http.get(`${BASE_URL}/api/products?page=0&size=20`);
    productListDuration.add(listRes.timings.duration);

    check(listRes, {
        'status is 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
    });
    errorRate.add(listRes.status !== 200);
    sleep(Math.random() * 0.5);

    const createRes = http.post(
        `${BASE_URL}/api/products`,
        JSON.stringify({ name: `상품 ${Date.now()}`, price: 10000, category: 'test' }),
        { headers: { 'Content-Type': 'application/json' } }
    );
    check(createRes, { 'created': (r) => r.status === 201 });
    sleep(Math.random() * 1);
}
```

```bash
# 실행
k6 run load-test.js

# Grafana 연동 (InfluxDB로 메트릭 전송)
k6 run --out influxdb=http://localhost:8086/k6 load-test.js
```

### 19.6.3 MVC vs WebFlux 성능 비교

그럼 이제 흔한 질문을 답해보자: Spring MVC와 Spring WebFlux는 성능이 얼마나 다를까? 동일한 비즈니스 로직으로 비교한 결과를 정리해봤다. 물론 실제 수치는 하드웨어와 로직의 특성에 따라 달라진다.

| 지표 | Spring MVC | Spring WebFlux | 비고 |
|------|-----------|---------------|------|
| **동시 사용자 100명** | | | |
| 처리량 | ~5,000 req/sec | ~6,000 req/sec | 유사 |
| p95 지연시간 | ~20ms | ~18ms | 유사 |
| 스레드 수 | ~200 | ~8 | WebFlux 압도적 |
| 메모리 사용량 | ~512MB | ~256MB | WebFlux 절반 |
| **동시 사용자 1,000명** | | | |
| 처리량 | ~4,500 req/sec | ~9,000 req/sec | WebFlux 2배 |
| p95 지연시간 | ~250ms | ~50ms | WebFlux 5배 |
| 스레드 수 | ~1,000+ | ~8 | WebFlux 압도적 |
| **동시 사용자 5,000명** | | | |
| 처리량 | ~3,000 req/sec | ~8,500 req/sec | WebFlux 3배 |
| p95 지연시간 | ~2,000ms+ | ~120ms | WebFlux 16배 |
| 에러율 | ~5% | ~0.1% | MVC 커넥션 거부 |

> **핵심 포인트**: 동시 사용자가 적을 때는 둘 다 엇비슷하다. WebFlux의 진정한 가치는 **높은 동시성**이 필요한 상황에서 드러난다. 외부 API 호출이 많거나 느린 DB 쿼리가 있는 애플리케이션일수록 WebFlux가 훨씬 유리하다.

### 19.6.4 부하 테스트 결과 분석 체크리스트

부하 테스트 결과를 볼 때 뭘 봐야 할까? 이런 체크리스트를 참고하면 된다.

| 점검 항목 | 정상 기준 | 이상 시 대응 |
|----------|----------|-------------|
| **p95 응답 시간** | SLA 목표 이내 | 병목 구간 프로파일링 |
| **에러율** | < 0.1% | 에러 로그 분석, 타임아웃 조정 |
| **CPU 사용률** | < 80% | 스케줄러 오프로드, 알고리즘 최적화 |
| **메모리 사용률** | GC 오버헤드 < 5% | 힙 크기 조정, 객체 풀링 |
| **커넥션 풀 대기** | waitQueue = 0 | 풀 크기 증가, 쿼리 최적화 |
| **이벤트 루프 CPU** | 각 스레드 < 70% | 블로킹 코드 제거, 연산 오프로드 |

### 19.6.5 성능 최적화 사이클

성능 최적화는 한 번 끝나는 게 아니다. 계속 반복되는 과정이다.

```
1. 측정 (Baseline)       <- Gatling/k6로 현재 성능 측정
2. 분석 (Bottleneck)     <- 프로파일링, 메트릭, 로그 분석
3. 최적화 (Fix)          <- 커넥션 풀, 캐시, 블로킹 제거, 쿼리 최적화
4. 검증 (Verify)         <- 동일 조건에서 재측정, 비교
5. 반복 (Iterate)        <- 다음 병목 지점으로 이동
```

한 번에 여러 개를 손보면 뭐가 효과가 있었는지 알 수 없다. **한 번에 하나씩만 바꾸고 측정하자**. 이게 원칙이다.

---

## 요약

이 장에서 다룬 내용을 정리해보면 다음과 같다.

| 주제 | 핵심 내용 |
|------|----------|
| **성능 측정** | 처리량/지연시간/리소스 3축 측정, Micrometer 메트릭, JMH 마이크로벤치마크, async-profiler/JFR 프로파일링 |
| **MongoDB 커넥션 풀** | `MongoClientSettings`로 풀 크기/타임아웃 설정, 커넥션 풀 메트릭 모니터링, 계층별 타임아웃 전략 |
| **Netty 이벤트 루프** | `LoopResources`로 스레드 수 조정, Epoll/KQueue 네이티브 Transport, 블로킹 작업 스케줄러 오프로드 |
| **캐싱 전략** | Caffeine 로컬 캐시, Reactive Redis 분산 캐시, L1/L2 멀티 레벨 캐시 구조 |
| **BlockHound** | 블로킹 호출 런타임 탐지, 흔한 블로킹 패턴과 수정법, StepVerifier 테스트 통합 |
| **부하 테스트** | Gatling/k6 스크립트 작성, MVC vs WebFlux 성능 비교, 결과 분석 체크리스트, 최적화 사이클 |

성능 최적화에서 가장 중요한 건 뭘까? 결국 **측정 -> 분석 -> 최적화 -> 검증**을 계속 반복하는 것이다. 감에 의존하지 말고, 항상 데이터를 기반으로 판단해야 한다. 그게 성공하는 최적화의 비결이다.

다음 장에서는 애플리케이션을 Docker 컨테이너로 만들고, Kubernetes에 배포하고, CI/CD 파이프라인을 구성하는 방법을 다룬다.
# Chapter 20. 컨테이너화와 배포

개발을 마치고 실전 운영 환경으로 나가려면 어떻게 해야 할까? 그 답이 **컨테이너(Container)**다. Docker와 Kubernetes는 이제 거의 표준이 되었다. Docker를 쓰면 애플리케이션과 실행 환경을 하나의 이미지로 묶어 어디서든 동일하게 실행할 수 있고, Kubernetes로는 수십 개의 컨테이너를 마치 한 대의 머신인 것처럼 관리할 수 있다.

이번 장에서는 실제 프로젝트에서 어떻게 Spring Boot WebFlux + MongoDB 애플리케이션을 컨테이너화하고 운영 환경으로 보내는지 살펴본다. Docker 이미지 빌드부터 Docker Compose를 이용한 로컬 환경 구성, Kubernetes 배포, MongoDB Atlas 연동, GitHub Actions로 자동화된 CI/CD 파이프라인 구축, 그리고 GraalVM Native Image까지 단계별로 진행해보자.

---

## 20.1 Docker 이미지 빌드 (Jib, Buildpacks)

Docker 이미지를 만드는 방법은 여러 가지가 있다. 전통적인 Dockerfile부터 시작해서 요즘 핫한 도구들까지 선택지가 많다. Google Jib과 Spring Boot의 Cloud Native Buildpacks가 가장 인기 있는 방식이고, 각각 장단점이 있다.

### 20.1.1 Jib을 활용한 Docker 이미지 빌드

Jib은 Google이 만든 도구인데, 사실 꽤 편리하다. Docker 데몬을 설치하고 실행할 필요가 없다는 게 큰 장점이다. **Docker 데몬 없이도** 빌드하고 바로 레지스트리에 올릴 수 있다. `build.gradle`에 플러그인을 추가하기만 하면 된다.

```groovy
plugins {
    id 'org.springframework.boot' version '3.4.1'
    id 'io.spring.dependency-management' version '1.1.7'
    id 'com.google.cloud.tools.jib' version '3.4.4'
    id 'java'
}

jib {
    from {
        image = 'eclipse-temurin:21-jre'
        platforms {
            platform {
                architecture = 'amd64'
                os = 'linux'
            }
            platform {
                architecture = 'arm64'
                os = 'linux'
            }
        }
    }
    to {
        image = 'ghcr.io/myorg/webflux-app'
        tags = [project.version, 'latest']
        auth {
            username = System.getenv('REGISTRY_USERNAME')
            password = System.getenv('REGISTRY_PASSWORD')
        }
    }
    container {
        jvmFlags = [
            '-XX:+UseZGC',
            '-XX:MaxRAMPercentage=75.0',
            '-Djava.security.egd=file:/dev/./urandom',
            '-Dspring.profiles.active=prod'
        ]
        ports = ['8080']
        creationTime = 'USE_CURRENT_TIMESTAMP'
        user = '1000:1000'
    }
}
```

상황에 따라 사용할 수 있는 명령어가 세 가지다.

```bash
# Docker 데몬 없이 레지스트리에 직접 푸시
./gradlew jib

# 로컬 Docker 데몬에 이미지 빌드
./gradlew jibDockerBuild

# tar 파일로 이미지 내보내기
./gradlew jibBuildTar
```

> **Tip**: Jib은 애플리케이션을 `classes`, `resources`, `dependencies`, `snapshot-dependencies`의 네 레이어로 자동 분리한다. 소스 코드만 변경하면 `classes` 레이어만 다시 빌드되므로 CI/CD에서 빌드 시간을 크게 단축할 수 있다.

### 20.1.2 Cloud Native Buildpacks

Spring Boot 3.x부터는 Cloud Native Buildpacks를 바로 사용할 수 있다. 추가 플러그인 설치 없이 기본 Gradle 명령어로 OCI 이미지를 빌드하면 되니까 편하다.

```groovy
bootBuildImage {
    imageName = "ghcr.io/myorg/webflux-app:${project.version}"
    environment = [
        'BP_JVM_VERSION': '21',
        'BP_JVM_TYPE': 'JRE',
        'BPE_JAVA_TOOL_OPTIONS': '-XX:+UseZGC -XX:MaxRAMPercentage=75.0'
    ]
    docker {
        publishRegistry {
            username = System.getenv('REGISTRY_USERNAME')
            password = System.getenv('REGISTRY_PASSWORD')
            url = 'https://ghcr.io'
        }
    }
}
```

```bash
./gradlew bootBuildImage
```

### 20.1.3 빌드 방식 비교

세 가지 방식의 특징을 정리하면 아래와 같다.

| 항목 | Dockerfile | Jib | Buildpacks |
|------|-----------|-----|------------|
| Docker 데몬 필요 | O | X | O |
| Dockerfile 필요 | O | X | X |
| 빌드 속도 | 보통 | 빠름 | 느림 |
| 레이어 최적화 | 수동 | 자동 | 자동 |
| 멀티 아키텍처 | 수동 설정 | 선언적 | 제한적 |
| CI/CD 친화성 | 보통 | 높음 | 높음 |

필자의 경험상, Buildpacks는 초기 빌드가 상당히 오래 걸린다. 하지만 캐시가 쌓인 후에는 빌드가 빨라진다. CI/CD 환경에서 Docker 데몬을 설정하기 어렵다면 Jib을 쓰는 게 가장 무난하다.

---

## 20.2 Docker Compose로 전체 스택 구성

이제 로컬에서 전체 환경을 한 번에 띄워보자. Docker Compose를 쓰면 Spring Boot 앱, MongoDB, Prometheus, Grafana를 한 번의 명령어로 구성할 수 있다.

### 20.2.1 Docker Compose 구성 파일

```yaml
# docker/docker-compose.yml
version: '3.8'
services:
  app:
    build:
      context: ..
      dockerfile: Dockerfile
    container_name: webflux-app
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: docker
      SPRING_DATA_MONGODB_URI: mongodb://appuser:apppass@mongodb:27017/webfluxdb?authSource=admin
      JAVA_TOOL_OPTIONS: >-
        -XX:+UseZGC
        -XX:MaxRAMPercentage=75.0
    depends_on:
      mongodb:
        condition: service_healthy
    networks:
      - app-network
    deploy:
      resources:
        limits:
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
      interval: 15s
      timeout: 5s
      retries: 5
      start_period: 30s
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: appuser
      MONGO_INITDB_ROOT_PASSWORD: apppass
      MONGO_INITDB_DATABASE: webfluxdb
    volumes:
      - mongodb-data:/data/db
      - ./mongo/init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
  prometheus:
    image: prom/prometheus:v2.51.0
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=7d'
    networks:
      - app-network
  grafana:
    image: grafana/grafana:10.4.0
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
    networks:
      - app-network
    depends_on:
      - prometheus
volumes:
  mongodb-data:
  prometheus-data:
  grafana-data:
networks:
  app-network:
    driver: bridge
```

### 20.2.2 Prometheus 설정과 MongoDB 초기화

```yaml
# docker/prometheus/prometheus.yml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'webflux-app'
    metrics_path: '/actuator/prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['app:8080']
```

```javascript
// docker/mongo/init-mongo.js
db = db.getSiblingDB('webfluxdb');
db.createCollection('products');
db.products.createIndex({ "name": 1 }, { unique: true });
db.products.createIndex({ "category": 1, "price": 1 });
```

### 20.2.3 Docker 프로파일용 애플리케이션 설정

```yaml
# src/main/resources/application-docker.yml
spring:
  data:
    mongodb:
      uri: ${SPRING_DATA_MONGODB_URI:mongodb://localhost:27017/webfluxdb}

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  endpoint:
    health:
      show-details: always
      probes:
        enabled: true
server:
  port: 8080
  netty:
    connection-timeout: 5s
```

```bash
# 전체 스택 시작
docker compose -f docker/docker-compose.yml up -d

# 로그 확인
docker compose -f docker/docker-compose.yml logs -f app

# 전체 스택 종료 및 볼륨 삭제
docker compose -f docker/docker-compose.yml down -v
```

실제로는 이 정도면 로컬에서 프로덕션과 거의 같은 환경을 구성할 수 있다.

---

## 20.3 Kubernetes 배포 기초

프로덕션으로 나가려면 보통 Kubernetes(K8s)를 쓴다. 수십, 수백 개의 컨테이너를 관리해야 할 때 정말 강력하다.

### 20.3.1 ConfigMap과 Secret

```yaml
# k8s/base/configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: webflux-app-config
  namespace: webflux-app
data:
  SPRING_PROFILES_ACTIVE: "k8s"
  JAVA_TOOL_OPTIONS: >-
    -XX:+UseZGC
    -XX:MaxRAMPercentage=75.0
    -XX:+ExitOnOutOfMemoryError
  MANAGEMENT_SERVER_PORT: "8081"
```

```yaml
# k8s/base/secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: webflux-app-secret
  namespace: webflux-app
type: Opaque
stringData:
  SPRING_DATA_MONGODB_URI: "mongodb+srv://appuser:securepass@cluster0.example.mongodb.net/webfluxdb?retryWrites=true&w=majority"
```

> **주의**: Secret을 Git에 평문으로 커밋하면 안 된다. 프로덕션에서는 **Sealed Secrets**, **External Secrets Operator**, 또는 **HashiCorp Vault**를 사용하여 시크릿을 관리한다.

### 20.3.2 Deployment

```yaml
# k8s/base/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webflux-app
  namespace: webflux-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: webflux-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    metadata:
      labels:
        app.kubernetes.io/name: webflux-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8081"
        prometheus.io/path: "/actuator/prometheus"
    spec:
      terminationGracePeriodSeconds: 30
      containers:
        - name: webflux-app
          image: ghcr.io/myorg/webflux-app:1.0.0
          ports:
            - name: http
              containerPort: 8080
            - name: management
              containerPort: 8081
          envFrom:
            - configMapRef:
                name: webflux-app-config
            - secretRef:
                name: webflux-app-secret
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "1000m"
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: management
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: management
            initialDelaySeconds: 30
            periodSeconds: 10
          startupProbe:
            httpGet:
              path: /actuator/health/liveness
              port: management
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 20
          lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 5"]
```

여기서 중요한 게 K8s 프로브와 Spring Boot Actuator의 관계다. 각 프로브가 어떤 엔드포인트를 호출하는지 잘 이해해야 한다.

| K8s 프로브 | Actuator 엔드포인트 | 역할 |
|-----------|-------------------|------|
| `startupProbe` | `/actuator/health/liveness` | 애플리케이션 시작 완료 확인 |
| `readinessProbe` | `/actuator/health/readiness` | 트래픽 수신 준비 확인 |
| `livenessProbe` | `/actuator/health/liveness` | 프로세스 정상 동작 확인 |

그리고 `preStop` 훅의 `sleep 5`가 중요한데, 이건 K8s가 Service 엔드포인트 목록에서 파드를 제거하는 동안 추가 시간을 주는 거다. 이렇게 해야 **정상 종료(Graceful Shutdown)** 중에 요청을 잃지 않는다.

### 20.3.3 Service와 HPA

```yaml
# k8s/base/service.yml
apiVersion: v1
kind: Service
metadata:
  name: webflux-app
  namespace: webflux-app
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: http
  selector:
    app.kubernetes.io/name: webflux-app
```

```yaml
# k8s/base/hpa.yml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webflux-app
  namespace: webflux-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webflux-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```

여기서 한 가지 주의할 점이 있다. 필자의 경험상 리액티브 애플리케이션은 CPU 사용률이 낮아 보이는데도 높은 처리량을 낸다. 따라서 CPU 기반 HPA만으로는 정확한 스케일링 시점을 판단하기 어렵다. 커스텀 메트릭(요청 큐 크기, p99 지연시간 등)을 함께 활용하는 게 좋다.

---

## 20.4 MongoDB Atlas 클라우드 연동

프로덕션에서 MongoDB를 직접 관리하는 건 번거롭다. **MongoDB Atlas**라는 관리형 서비스를 쓰면 훨씬 편하다. 필자의 경험상 자동 백업, 패치 관리, 고가용성 설정 등이 모두 자동으로 되니까 개발팀이 코드에 집중할 수 있다.

### 20.4.1 Atlas 연결 설정

```yaml
# src/main/resources/application-prod.yml
spring:
  data:
    mongodb:
      uri: mongodb+srv://${MONGO_USERNAME}:${MONGO_PASSWORD}@cluster0.abc123.mongodb.net/${MONGO_DATABASE}?retryWrites=true&w=majority&maxPoolSize=50&minPoolSize=5&connectTimeoutMS=10000&serverSelectionTimeoutMS=10000
```

| 옵션 | 권장값 | 설명 |
|------|-------|------|
| `retryWrites` | true | 일시적 네트워크 오류 시 쓰기 자동 재시도 |
| `w` | majority | 과반수 노드 쓰기 확인 |
| `maxPoolSize` | 50 | 최대 커넥션 풀 크기 |
| `minPoolSize` | 5 | 최소 유지 커넥션 수 |
| `connectTimeoutMS` | 10000 | 연결 타임아웃 |

### 20.4.2 Java 설정과 헬스 체크

```java
@Configuration
public class MongoAtlasConfig {

    @Bean
    public MongoClientSettings mongoClientSettings() {
        return MongoClientSettings.builder()
            .applyConnectionString(
                new ConnectionString(System.getenv("SPRING_DATA_MONGODB_URI"))
            )
            .applyToSslSettings(ssl -> ssl.enabled(true))
            .applyToConnectionPoolSettings(pool -> pool
                .maxSize(50)
                .minSize(5)
                .maxConnectionIdleTime(60, TimeUnit.SECONDS)
                .maxWaitTime(10, TimeUnit.SECONDS)
            )
            .retryWrites(true)
            .retryReads(true)
            .build();
    }
}
```

```java
@Component
@RequiredArgsConstructor
public class MongoAtlasHealthIndicator implements ReactiveHealthIndicator {

    private final ReactiveMongoTemplate mongoTemplate;

    @Override
    public Mono<Health> health() {
        return mongoTemplate.executeCommand(new org.bson.Document("ping", 1))
            .map(result -> Health.up()
                .withDetail("database", "MongoDB Atlas")
                .build())
            .onErrorResume(ex -> Mono.just(
                Health.down()
                    .withDetail("error", ex.getMessage())
                    .build()))
            .timeout(Duration.ofSeconds(5))
            .onErrorReturn(Health.down()
                .withDetail("error", "Health check timeout")
                .build());
    }
}
```

### 20.4.3 K8s에서 Atlas 연결 시 고려사항

K8s에서 Atlas로 연결할 때 생각해야 할 부분들이 있다.

1. **고정 Egress IP**: K8s 클러스터의 모든 아웃바운드 트래픽이 고정 IP를 사용하도록 NAT Gateway를 설정하고, 그 IP를 Atlas IP Access List에 등록한다.
2. **VPC Peering / Private Link**: 보안이 중요한 프로덕션 환경이라면 Atlas의 VPC Peering이나 AWS PrivateLink를 설정하자.
3. **DNS 해석**: `mongodb+srv://` URI는 DNS SRV 레코드를 사용한다. K8s 클러스터의 DNS가 외부 DNS를 제대로 해석할 수 있어야 한다.

한 가지 더, Atlas의 무료 등급(M0)은 VPC Peering과 Private Link를 지원하지 않는다. 프로덕션에서는 최소 M10 이상을 써야 한다.

---

## 20.5 CI/CD 파이프라인 구성 (GitHub Actions)

이제 자동화 차례다. GitHub Actions를 쓰면 코드 푸시부터 테스트, 빌드, K8s 배포까지 자동으로 진행된다. 직접 배포할 필요 없이 git push 하나면 된다.

### 20.5.1 CI/CD 워크플로우

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  contents: read
  packages: write

env:
  JAVA_VERSION: '21'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    name: Build & Test
    runs-on: ubuntu-latest
    services:
      mongodb:
        image: mongo:7.0
        ports:
          - 27017:27017
        env:
          MONGO_INITDB_ROOT_USERNAME: testuser
          MONGO_INITDB_ROOT_PASSWORD: testpass
        options: >-
          --health-cmd "mongosh --eval 'db.adminCommand({ping:1})'"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
      - uses: gradle/actions/setup-gradle@v4
      - name: Run Tests
        env:
          SPRING_DATA_MONGODB_URI: mongodb://testuser:testpass@localhost:27017/testdb?authSource=admin
        run: ./gradlew test

  build-image:
    name: Build & Push Image
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    outputs:
      image-tag: ${{ steps.meta.outputs.version }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
      - uses: gradle/actions/setup-gradle@v4
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
      - name: Build and Push with Jib
        run: |
          ./gradlew jib \
            -Djib.to.image=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }} \
            -Djib.to.tags=${{ steps.meta.outputs.version }}
        env:
          REGISTRY_USERNAME: ${{ github.actor }}
          REGISTRY_PASSWORD: ${{ secrets.GITHUB_TOKEN }}

  deploy:
    name: Deploy to Kubernetes
    needs: build-image
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v4
      - name: Set Kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
      - name: Deploy
        run: |
          kubectl apply -k k8s/overlays/prod/
          kubectl -n webflux-app rollout status deployment/webflux-app --timeout=300s
```

### 20.5.2 브랜치 전략과 시크릿 관리

브랜치별로 다른 동작을 하도록 설정할 수 있다.

| 브랜치 | 트리거 | 수행 작업 |
|--------|-------|----------|
| `feature/*` | PR 생성 | 빌드, 테스트 |
| `develop` | Push | 빌드, 테스트, 스테이징 배포 |
| `main` | Push | 빌드, 테스트, 이미지 빌드, 프로덕션 배포 |

필요한 GitHub Secrets:

| 시크릿 이름 | 설명 |
|------------|------|
| `GITHUB_TOKEN` | 자동 제공 (GHCR 인증용) |
| `KUBE_CONFIG` | K8s kubeconfig (Base64 인코딩) |
| `MONGO_URI` | MongoDB Atlas 연결 문자열 |

팁으로, `environment: production` 설정을 쓰면 프로덕션 배포 전에 수동 승인(Manual Approval) 단계를 추가할 수 있다. 이렇게 하면 실수로 잘못된 코드가 배포되는 실수를 줄일 수 있다.

---

## 20.6 GraalVM Native Image 빌드

마지막으로 GraalVM Native Image를 살펴보자. 이건 Java를 컴파일 시점에 네이티브 코드로 변환해버린다. 덕분에 시작 시간이 몇 초에서 수백 밀리초로 줄어들고, 메모리도 훨씬 적게 쓴다. 서버리스 환경이나 마이크로서비스 아키텍처에 정말 좋다.

### 20.6.1 JVM vs Native Image 비교

| 항목 | JVM | Native Image |
|------|-----|-------------|
| 시작 시간 | 2~5초 | 50~200ms |
| 메모리 사용 | 256~512MB | 64~128MB |
| 최대 처리량 | 높음 (JIT 최적화) | 보통 (AOT 제한) |
| 빌드 시간 | 짧음 | 김 (수 분) |
| 리플렉션 지원 | 완전 | 설정 필요 |

### 20.6.2 Gradle 빌드 설정

```groovy
plugins {
    id 'org.springframework.boot' version '3.4.1'
    id 'io.spring.dependency-management' version '1.1.7'
    id 'org.graalvm.buildtools.native' version '0.10.4'
    id 'java'
}

graalvmNative {
    binaries {
        main {
            buildArgs.addAll([
                '--initialize-at-build-time',
                '-H:+ReportExceptionStackTraces'
            ])
            javaLauncher = javaToolchains.launcherFor {
                languageVersion = JavaLanguageVersion.of(21)
                vendor = JvmVendorSpec.GRAAL_VM
            }
        }
    }
    metadataRepository {
        enabled = true
    }
}
```

### 20.6.3 리플렉션 힌트 설정

Spring Boot 3.x는 대부분의 리플렉션 힌트를 자동으로 생성해준다. 다행히 개발자가 직접 설정할 필요가 거의 없다. 다만 동적으로 로드되는 특수한 클래스는 수동으로 등록해야 한다.

```java
@Configuration
@ImportRuntimeHints(NativeHintsRegistrar.class)
public class NativeImageConfig {
}

public class NativeHintsRegistrar implements RuntimeHintsRegistrar {

    @Override
    public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
        hints.reflection()
            .registerType(Product.class, MemberCategory.values())
            .registerType(Order.class, MemberCategory.values());

        hints.resources()
            .registerPattern("application*.yml");
    }
}
```

### 20.6.4 Native Image Docker 빌드

GraalVM을 로컬에 설치할 필요는 없다. Buildpacks를 쓰면 Docker 컨테이너 안에서 자동으로 빌드된다.

```groovy
bootBuildImage {
    imageName = "ghcr.io/myorg/webflux-app-native:${project.version}"
    environment = [
        'BP_NATIVE_IMAGE': 'true',
        'BP_JVM_VERSION': '21'
    ]
}
```

혹은 멀티 스테이지 Dockerfile로 직접 빌드할 수도 있다.

```dockerfile
FROM ghcr.io/graalvm/native-image-community:21 AS builder
WORKDIR /app
COPY gradle/ gradle/
COPY gradlew build.gradle settings.gradle ./
COPY src/ src/
RUN ./gradlew nativeCompile --no-daemon

FROM debian:bookworm-slim
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --from=builder /app/build/native/nativeCompile/webflux-app ./
USER appuser
EXPOSE 8080
ENTRYPOINT ["./webflux-app"]
```

### 20.6.5 주의사항

실제로 네이티브 이미지를 빌드할 때 주의할 점들이 있다.

1. **빌드 리소스**: 네이티브 이미지 컴파일은 상당히 무겁다. 최소 8GB 메모리가 필요하고 5~10분 이상 걸린다. CI/CD에서 대규모 프로젝트는 GitHub Actions의 Larger Runner를 사용하는 게 좋다.
2. **프로파일 결정 시점**: 네이티브 이미지는 빌드할 때 프로파일이 확정된다. 런타임에 바꿀 수 없다는 뜻이다. 나중에 런타임 변경이 필요하면 AOT 처리 시 명시적으로 설정해야 한다.

```bash
./gradlew nativeCompile -Pspring.profiles.active=prod
```

3. **서드파티 호환성**: 모든 라이브러리가 네이티브 이미지를 지원하진 않는다. 사용하는 라이브러리가 지원되는지 [GraalVM Reachability Metadata Repository](https://github.com/oracle/graalvm-reachability-metadata)에서 확인하자.
4. **GitHub Actions 빌드**: 보통 Git 태그를 푸시할 때 네이티브 이미지 빌드를 트리거하는 방식으로 구성한다.

```yaml
# .github/workflows/native-build.yml
name: Native Image Build
on:
  push:
    tags: ['v*']
jobs:
  native-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: graalvm/setup-graalvm@v1
        with:
          java-version: '21'
          distribution: 'graalvm-community'
      - uses: gradle/actions/setup-gradle@v4
      - run: ./gradlew nativeCompile
      - run: |
          docker build -f Dockerfile.native \
            -t ghcr.io/${{ github.repository }}-native:${{ github.ref_name }} .
          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker push ghcr.io/${{ github.repository }}-native:${{ github.ref_name }}
```

---

## 요약

지금까지 배포의 전체 과정을 다뤘다.

| 주제 | 핵심 도구 | 권장 사항 |
|------|----------|----------|
| Docker 빌드 | Jib, Buildpacks | CI/CD에서는 Jib 권장 |
| 로컬 스택 | Docker Compose | 헬스 체크와 의존성 순서 필수 |
| K8s 배포 | Deployment, HPA | 3종 프로브와 preStop 훅 설정 |
| Atlas 연동 | SRV 연결 | VPC Peering으로 보안 강화 |
| CI/CD | GitHub Actions | 브랜치 전략과 시크릿 관리 |
| Native Image | GraalVM, AOT | 서버리스 환경에 적합 |

컨테이너화와 CI/CD를 제대로 구축해놓으면, 이후 배포는 거의 자동화된다. 개발팀은 코드만 푸시하면 되고, 나머지는 파이프라인이 알아서 처리한다. 다음 장에서는 이런 환경에서 문제가 생겼을 때 **장애 대응과 트러블슈팅**을 어떻게 하는지 다룬다.