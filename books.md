# Spring Boot + WebFlux + JPA (MongoDB) 목차

---

## Part 1. 기초 다지기

### Chapter 1. 리액티브 프로그래밍 소개
- 1.1 리액티브 프로그래밍이란?
- 1.2 명령형 프로그래밍 vs 리액티브 프로그래밍
- 1.3 리액티브 스트림(Reactive Streams) 표준
- 1.4 배압(Backpressure)의 개념
- 1.5 왜 리액티브가 필요한가?

### Chapter 2. Spring WebFlux 개요
- 2.1 Spring MVC와 Spring WebFlux 비교
- 2.2 WebFlux의 내부 구조와 Netty
- 2.3 논블로킹 I/O의 원리
- 2.4 WebFlux를 선택해야 하는 경우와 그렇지 않은 경우
- 2.5 WebFlux의 두 가지 프로그래밍 모델: 어노테이션 기반 vs 함수형

### Chapter 3. Project Reactor 핵심
- 3.1 Mono와 Flux 이해하기
- 3.2 Reactor의 주요 연산자 (map, flatMap, filter, zip 등)
- 3.3 에러 처리 전략 (onErrorResume, onErrorReturn, retry)
- 3.4 스케줄러(Scheduler)와 스레드 모델
- 3.5 Cold vs Hot Publisher
- 3.6 Reactor 디버깅 기법

### Chapter 4. MongoDB 소개
- 4.1 NoSQL과 MongoDB의 특징
- 4.2 도큐먼트 모델과 컬렉션
- 4.3 MongoDB 설치 및 기본 CRUD
- 4.4 인덱싱과 쿼리 최적화 기초
- 4.5 MongoDB와 리액티브 드라이버

---

## Part 2. 프로젝트 시작하기

### Chapter 5. 개발 환경 구성
- 5.1 JDK, IDE, Docker 설치
- 5.2 Spring Initializr로 프로젝트 생성
- 5.3 주요 의존성 설정 (WebFlux, Reactive MongoDB, Lombok 등)
- 5.4 application.yml 설정
- 5.5 MongoDB Docker 컨테이너 구성
- 5.6 프로젝트 구조 설계

### Chapter 6. 어노테이션 기반 REST API 구현
- 6.1 도메인 모델(Document) 정의
- 6.2 ReactiveMongoRepository 활용
- 6.3 서비스 계층 구현
- 6.4 @RestController로 CRUD API 만들기
- 6.5 요청/응답 DTO 설계
- 6.6 API 테스트 (cURL, Postman)

### Chapter 7. 함수형 엔드포인트 (Router Functions)
- 7.1 HandlerFunction과 RouterFunction 이해
- 7.2 RouterFunction으로 라우팅 정의하기
- 7.3 HandlerFunction 구현
- 7.4 요청 파라미터 및 바디 처리
- 7.5 어노테이션 방식과 함수형 방식 비교

---

## Part 3. 심화 개발

### Chapter 8. MongoDB 리액티브 데이터 접근 심화
- 8.1 ReactiveMongoTemplate 활용
- 8.2 커스텀 쿼리와 Criteria API
- 8.3 Aggregation Pipeline 사용
- 8.4 변경 스트림(Change Streams) 활용
- 8.5 트랜잭션 처리 (ReactiveMongoTransactionManager)
- 8.6 인덱스 관리와 쿼리 성능 최적화

### Chapter 9. 데이터 검증과 예외 처리
- 9.1 Bean Validation을 활용한 입력 검증
- 9.2 커스텀 Validator 구현
- 9.3 글로벌 예외 처리 (@ControllerAdvice)
- 9.4 ErrorWebExceptionHandler를 활용한 함수형 예외 처리
- 9.5 에러 응답 표준화 (Problem Details)

### Chapter 10. WebFlux 필터와 인터셉터
- 10.1 WebFilter 구현
- 10.2 HandlerFilterFunction 활용
- 10.3 요청/응답 로깅
- 10.4 CORS 설정
- 10.5 요청 속도 제한(Rate Limiting)

### Chapter 11. 리액티브 보안 (Spring Security WebFlux)
- 11.1 Spring Security Reactive 설정
- 11.2 SecurityWebFilterChain 구성
- 11.3 인증과 인가 구현
- 11.4 JWT 기반 인증 구현
- 11.5 리액티브 환경에서의 SecurityContext 관리
- 11.6 OAuth2 / OpenID Connect 연동

---

## Part 4. 실시간 통신과 고급 기능

### Chapter 12. Server-Sent Events (SSE)
- 12.1 SSE란 무엇인가?
- 12.2 Flux를 활용한 SSE 엔드포인트 구현
- 12.3 실시간 알림 시스템 구축
- 12.4 MongoDB Change Streams + SSE 연동

### Chapter 13. WebSocket
- 13.1 WebSocket 프로토콜 이해
- 13.2 WebFlux에서 WebSocket 핸들러 구현
- 13.3 실시간 채팅 애플리케이션 구축
- 13.4 WebSocket 세션 관리

### Chapter 14. WebClient: 리액티브 HTTP 클라이언트
- 14.1 WebClient 설정과 기본 사용법
- 14.2 요청/응답 처리 (GET, POST, PUT, DELETE)
- 14.3 에러 핸들링과 재시도 전략
- 14.4 타임아웃 설정
- 14.5 외부 API 연동 실전 예제
- 14.6 WebClient 필터와 인터셉터

### Chapter 15. R2DBC와의 통합 (보너스)
- 15.1 R2DBC란?
- 15.2 MongoDB + R2DBC(관계형 DB) 멀티 데이터소스 구성
- 15.3 리액티브 환경에서 여러 데이터소스 조합하기

---

## Part 5. 테스트와 품질

### Chapter 16. 리액티브 테스트 전략
- 16.1 StepVerifier를 활용한 단위 테스트
- 16.2 WebTestClient를 활용한 통합 테스트
- 16.3 Embedded MongoDB를 활용한 리포지토리 테스트
- 16.4 Testcontainers로 MongoDB 테스트 환경 구성
- 16.5 MockWebServer를 활용한 외부 API 모킹
- 16.6 테스트 슬라이스(@WebFluxTest, @DataMongoTest)

### Chapter 17. 문서화와 API 관리
- 17.1 SpringDoc OpenAPI(Swagger) 연동
- 17.2 리액티브 API 문서 자동 생성
- 17.3 API 버전 관리 전략

---

## Part 6. 운영과 배포

### Chapter 18. 모니터링과 관측 가능성
- 18.1 Spring Boot Actuator 설정
- 18.2 Micrometer와 Prometheus 연동
- 18.3 Grafana 대시보드 구성
- 18.4 리액티브 스트림 메트릭 수집
- 18.5 분산 추적 (Zipkin / Jaeger)
- 18.6 구조화된 로깅 (Logback + MDC in Reactive)

### Chapter 19. 성능 최적화
- 19.1 리액티브 애플리케이션 성능 측정
- 19.2 MongoDB 커넥션 풀 튜닝
- 19.3 Netty 이벤트 루프 최적화
- 19.4 캐싱 전략 (Caffeine, Redis)
- 19.5 블로킹 코드 탐지 및 제거 (BlockHound)
- 19.6 부하 테스트 (Gatling, k6)

### Chapter 20. 컨테이너화와 배포
- 20.1 Docker 이미지 빌드 (Jib, Buildpacks)
- 20.2 Docker Compose로 전체 스택 구성
- 20.3 Kubernetes 배포 기초
- 20.4 MongoDB Atlas 클라우드 연동
- 20.5 CI/CD 파이프라인 구성 (GitHub Actions)
- 20.6 GraalVM Native Image 빌드

---

## Part 7. 실전 프로젝트

### Chapter 21. 실전 프로젝트: 실시간 게시판 서비스
- 21.1 요구사항 분석 및 설계
- 21.2 사용자 관리 (회원가입, 로그인, JWT)
- 21.3 게시글 CRUD API 구현
- 21.4 댓글 시스템 (내장 도큐먼트 vs 참조)
- 21.5 실시간 알림 (SSE)
- 21.6 페이징과 검색 기능
- 21.7 파일 업로드 (GridFS)
- 21.8 전체 테스트 작성
- 21.9 Docker Compose로 배포

---

## 부록

### 부록 A. Reactor 주요 연산자 레퍼런스
### 부록 B. MongoDB 쿼리 연산자 정리
### 부록 C. 자주 발생하는 문제와 해결 방법 (FAQ)
### 부록 D. 참고 자료 및 추천 학습 경로
# Chapter 1. 리액티브 프로그래밍 소개

현대 소프트웨어 시스템은 수백만 사용자의 동시 요청, 밀리초 단위의 응답 시간, 무중단 운영을 요구한다. 전통적인 명령형 프로그래밍 모델로는 이러한 요구사항을 충족하기 어렵다. 이 장에서는 리액티브 프로그래밍의 핵심 개념을 살펴보고, 왜 Spring WebFlux가 이 패러다임을 채택했는지 이해한다.

---

## 1.1 리액티브 프로그래밍이란?

### 1.1.1 정의와 핵심 원칙

리액티브 프로그래밍(Reactive Programming)은 **데이터 스트림과 변화의 전파**에 초점을 맞춘 프로그래밍 패러다임이다. 기존의 명령형 프로그래밍이 "이 값을 가져와서 이렇게 처리하라"라고 지시하는 방식이라면, 리액티브 프로그래밍은 "데이터가 흘러오면 이렇게 반응하라"라고 선언하는 방식이다.

스프레드시트를 떠올려 보자. 셀 A1에 10, B1에 20이 있고, C1에 `=A1+B1`이라는 수식을 넣으면 C1은 30이 된다. 이후 A1의 값을 50으로 바꾸면 C1은 자동으로 70으로 갱신된다. 이것이 리액티브 프로그래밍의 본질이다. C1은 A1과 B1의 **변화에 반응**한다.

리액티브 프로그래밍의 핵심 원칙은 다음과 같다.

- **비동기 데이터 스트림**: 모든 데이터를 시간에 따라 흐르는 스트림으로 모델링한다.
- **변화의 전파**: 상류(upstream)의 변화가 하류(downstream)로 자동 전파된다.
- **선언적 구성**: 데이터를 어떻게(how) 처리할지가 아니라, 무엇을(what) 할지 선언한다.
- **논블로킹 실행**: 스레드를 차단하지 않고 비동기적으로 작업을 수행한다.

### 1.1.2 리액티브 선언문 (Reactive Manifesto)

2014년에 발표된 리액티브 선언문은 리액티브 시스템이 갖추어야 할 네 가지 속성을 정의한다.

| 속성 | 설명 |
|------|------|
| **응답성(Responsive)** | 시스템이 가능한 한 즉각적으로 응답한다. 응답성은 사용자 경험의 핵심이다. |
| **탄력성(Resilient)** | 장애가 발생해도 시스템이 응답성을 유지한다. 장애는 각 컴포넌트 내부에 격리된다. |
| **유연성(Elastic)** | 작업 부하가 변화해도 시스템이 응답성을 유지한다. 리소스를 동적으로 확장/축소한다. |
| **메시지 기반(Message Driven)** | 비동기 메시지 전달을 통해 컴포넌트 간 느슨한 결합을 달성한다. |

이 네 가지 속성은 독립적이지 않다. 메시지 기반 아키텍처가 토대가 되고, 그 위에 유연성과 탄력성이 구현되며, 최종적으로 응답성이 확보된다.

### 1.1.3 데이터 스트림과 변화의 전파

리액티브 프로그래밍에서 모든 것은 스트림이다. 사용자 클릭 이벤트, HTTP 요청, 데이터베이스 쿼리 결과, 센서 데이터 등 모든 데이터가 시간축 위에 놓인 스트림으로 표현된다.

스트림은 세 가지 신호를 발행할 수 있다.

1. **onNext(item)**: 다음 데이터 항목을 전달한다.
2. **onError(error)**: 오류가 발생했음을 알린다. 스트림이 종료된다.
3. **onComplete()**: 더 이상 전달할 데이터가 없음을 알린다. 스트림이 종료된다.

```
시간 →
──[item1]──[item2]──[item3]──|──>   (정상 완료: | = onComplete)
──[item1]──[item2]──X──>            (오류 발생: X = onError)
```

### 1.1.4 옵저버 패턴과의 관계

리액티브 프로그래밍은 GoF 디자인 패턴의 옵저버 패턴(Observer Pattern)을 확장한 것이다. 옵저버 패턴에서는 Subject가 상태 변화를 Observer에게 통지한다.

```java
// 전통적인 옵저버 패턴
public interface Observer {
    void update(String event);
}

public class EventSource {
    private final List<Observer> observers = new ArrayList<>();

    public void addObserver(Observer observer) {
        observers.add(observer);
    }

    public void notifyAll(String event) {
        observers.forEach(o -> o.update(event));
    }
}
```

리액티브 프로그래밍은 이 옵저버 패턴에 다음 세 가지를 추가한다.

- **완료 신호**: 데이터 발행이 끝났음을 구독자에게 알릴 수 있다.
- **오류 처리**: 오류를 스트림의 일부로 다루어 체계적으로 처리한다.
- **배압(Backpressure)**: 구독자가 처리할 수 있는 속도에 맞춰 데이터 발행 속도를 조절한다.

---

## 1.2 명령형 프로그래밍 vs 리액티브 프로그래밍

### 1.2.1 명령형 방식의 코드 예시

사용자 목록에서 활성 사용자를 필터링하고, 이름을 대문자로 변환하여 정렬하는 로직을 명령형으로 작성하면 다음과 같다.

```java
// 명령형 방식: 단계별로 "어떻게" 처리할지 기술
public List<String> getActiveUserNames(List<User> users) {
    List<String> activeUserNames = new ArrayList<>();

    for (User user : users) {
        if (user.isActive()) {
            String upperName = user.getName().toUpperCase();
            activeUserNames.add(upperName);
        }
    }

    Collections.sort(activeUserNames);
    return activeUserNames;
}
```

이 코드는 직관적이지만, 모든 데이터가 메모리에 준비되어 있어야 하고, 처리가 끝날 때까지 호출 스레드가 차단된다.

### 1.2.2 같은 로직의 리액티브 코드 예시

같은 로직을 Project Reactor를 사용한 리액티브 방식으로 작성하면 다음과 같다.

```java
// 리액티브 방식: "무엇을" 할지 선언적으로 기술
public Flux<String> getActiveUserNames(Flux<User> users) {
    return users
            .filter(User::isActive)
            .map(user -> user.getName().toUpperCase())
            .sort();
}
```

리액티브 코드는 데이터가 도착할 때마다 파이프라인을 통해 처리된다. 전체 데이터가 메모리에 있을 필요가 없으며, 호출 스레드를 차단하지 않는다.

### 1.2.3 동기 vs 비동기, 블로킹 vs 논블로킹

이 두 쌍의 개념은 자주 혼동되지만 서로 다른 차원의 개념이다.

**동기(Synchronous) vs 비동기(Asynchronous)**는 호출자가 결과를 기다리는 방식에 관한 것이다.

- 동기: 호출자가 결과가 반환될 때까지 기다린다.
- 비동기: 호출자가 결과를 기다리지 않고, 결과가 준비되면 콜백이나 이벤트로 통지받는다.

**블로킹(Blocking) vs 논블로킹(Non-blocking)**은 호출된 함수가 스레드를 점유하는 방식에 관한 것이다.

- 블로킹: 호출된 함수가 작업을 완료할 때까지 스레드를 점유한다.
- 논블로킹: 호출된 함수가 즉시 반환하고, 스레드를 다른 작업에 활용할 수 있다.

```java
// 동기 + 블로킹: 스레드가 응답을 받을 때까지 멈춘다
User user = userRepository.findById(1L);  // 블로킹 호출

// 비동기 + 논블로킹: 스레드가 즉시 반환되고, 데이터가 준비되면 처리된다
Mono<User> user = userRepository.findById(1L);  // 논블로킹 호출
user.subscribe(u -> System.out.println(u.getName()));
```

### 1.2.4 장단점 비교

| 구분 | 명령형 | 리액티브 |
|------|--------|----------|
| **코드 가독성** | 직관적이고 이해하기 쉬움 | 학습 곡선이 존재함 |
| **디버깅** | 스택 트레이스가 명확함 | 비동기 스택 트레이스 추적이 어려움 |
| **리소스 활용** | 스레드 차단으로 비효율적 | 적은 스레드로 높은 처리량 달성 |
| **확장성** | 스레드 수에 비례하여 제한적 | 이벤트 루프 기반으로 높은 확장성 |
| **에러 처리** | try-catch로 직관적 | 연산자 체인에서 처리 |
| **적합한 상황** | CPU 집약적, 단순한 CRUD | I/O 집약적, 대규모 동시 연결 |

---

## 1.3 리액티브 스트림(Reactive Streams) 표준

### 1.3.1 개요

리액티브 스트림은 비동기 스트림 처리를 위한 표준 인터페이스 명세이다. Netflix, Lightbend, Pivotal 등이 공동으로 개발했으며, Java 9부터 `java.util.concurrent.Flow` 클래스로 JDK에 포함되었다.

이 표준은 단 4개의 인터페이스로 구성된다.

### 1.3.2 Publisher

데이터를 생산하는 주체이다. 구독자의 요청에 따라 데이터를 발행한다.

```java
public interface Publisher<T> {
    void subscribe(Subscriber<? super T> subscriber);
}
```

`subscribe()` 메서드는 구독자를 등록한다. 호출되면 Publisher는 `Subscriber.onSubscribe()`를 호출하여 Subscription 객체를 전달한다.

### 1.3.3 Subscriber

데이터를 소비하는 주체이다. Publisher로부터 데이터를 수신하고 처리한다.

```java
public interface Subscriber<T> {
    void onSubscribe(Subscription subscription);
    void onNext(T item);
    void onError(Throwable throwable);
    void onComplete();
}
```

| 메서드 | 호출 시점 | 역할 |
|--------|----------|------|
| `onSubscribe` | 구독 시작 시 | Subscription을 수신하여 데이터 요청 시작 |
| `onNext` | 데이터 발행 시 | 각 데이터 항목을 처리 |
| `onError` | 오류 발생 시 | 오류를 처리하고 스트림 종료 |
| `onComplete` | 발행 완료 시 | 정상 종료 처리 |

### 1.3.4 Subscription

Publisher와 Subscriber 사이의 연결을 나타낸다. 배압 제어의 핵심이다.

```java
public interface Subscription {
    void request(long n);
    void cancel();
}
```

- `request(n)`: Publisher에게 n개의 데이터를 요청한다. 이것이 배압의 핵심 메커니즘이다.
- `cancel()`: 구독을 취소한다. 더 이상 데이터를 수신하지 않는다.

### 1.3.5 Processor

Publisher와 Subscriber를 동시에 구현한다. 데이터를 수신하여 변환한 뒤 다시 발행하는 중간 처리 단계이다.

```java
public interface Processor<T, R> extends Subscriber<T>, Publisher<R> {
}
```

### 1.3.6 상호작용 흐름

네 인터페이스의 상호작용을 순서대로 정리하면 다음과 같다.

```
Subscriber                    Publisher
    |                             |
    |--- subscribe(subscriber) -->|
    |                             |
    |<-- onSubscribe(subscription)|
    |                             |
    |--- request(3) ------------->|   (3개 요청)
    |                             |
    |<-- onNext(item1) -----------|
    |<-- onNext(item2) -----------|
    |<-- onNext(item3) -----------|
    |                             |
    |--- request(2) ------------->|   (2개 추가 요청)
    |                             |
    |<-- onNext(item4) -----------|
    |<-- onComplete() ------------|   (발행 완료)
```

### 1.3.7 Java 코드로 보는 전체 흐름

```java
import java.util.concurrent.Flow.*;

public class SimpleReactiveExample {

    public static void main(String[] args) {
        // Publisher: 1~5를 발행
        SubmissionPublisher<Integer> publisher = new SubmissionPublisher<>();

        // Subscriber: 데이터를 수신하여 출력
        Subscriber<Integer> subscriber = new Subscriber<>() {
            private Subscription subscription;

            @Override
            public void onSubscribe(Subscription subscription) {
                this.subscription = subscription;
                subscription.request(1); // 첫 번째 항목 요청
            }

            @Override
            public void onNext(Integer item) {
                System.out.println("수신: " + item);
                subscription.request(1); // 다음 항목 요청
            }

            @Override
            public void onError(Throwable throwable) {
                System.err.println("오류: " + throwable.getMessage());
            }

            @Override
            public void onComplete() {
                System.out.println("완료");
            }
        };

        publisher.subscribe(subscriber);

        // 데이터 발행
        for (int i = 1; i <= 5; i++) {
            publisher.submit(i);
        }
        publisher.close();
    }
}
```

### 1.3.8 주요 구현체

| 구현체 | 개발 주체 | 특징 |
|--------|----------|------|
| **Project Reactor** | Pivotal (VMware) | Spring WebFlux의 기본 구현체. Mono/Flux 제공 |
| **RxJava** | Netflix | 가장 오래된 리액티브 라이브러리. Observable/Flowable 제공 |
| **Akka Streams** | Lightbend | Akka 액터 모델 기반. Source/Flow/Sink 제공 |
| **Mutiny** | Red Hat | Quarkus 프레임워크의 기본 구현체. Uni/Multi 제공 |

이 책에서는 Spring WebFlux의 기본 구현체인 **Project Reactor**를 사용한다.

---

## 1.4 배압(Backpressure)의 개념

### 1.4.1 배압이 필요한 이유

배압은 데이터 소비자가 생산자에게 "속도를 늦춰 달라"고 요청하는 메커니즘이다.

일상적인 비유로 설명하면, 컨베이어 벨트 위의 물건을 포장하는 작업자를 생각해 보자. 벨트가 너무 빨리 움직이면 물건이 쌓이고 바닥에 떨어진다. 작업자가 "속도를 줄여 주세요"라고 요청할 수 있어야 한다. 이것이 배압이다.

소프트웨어 시스템에서 배압이 없으면 다음 문제가 발생한다.

- **메모리 초과(OOM)**: 처리하지 못한 데이터가 버퍼에 무한히 쌓인다.
- **응답 지연**: 과부하된 컴포넌트의 처리 속도가 급격히 저하된다.
- **시스템 장애**: 한 컴포넌트의 과부하가 전체 시스템으로 전파된다.

### 1.4.2 배압 전략

Project Reactor는 다양한 배압 전략을 제공한다.

| 전략 | 설명 | 사용 시나리오 |
|------|------|-------------|
| **BUFFER** | 소비되지 못한 항목을 버퍼에 저장 | 데이터 손실이 허용되지 않을 때 |
| **DROP** | 소비자가 준비되지 않으면 새 항목을 버림 | 최신 데이터만 중요할 때 |
| **LATEST** | 가장 최근 항목만 유지하고 나머지 버림 | 센서 데이터 등 최신 값만 필요할 때 |
| **ERROR** | 소비자가 감당할 수 없으면 오류 발생 | 엄격한 흐름 제어가 필요할 때 |

### 1.4.3 코드로 보는 배압 처리

```java
import reactor.core.publisher.Flux;
import reactor.core.scheduler.Schedulers;
import java.time.Duration;

public class BackpressureExample {

    public static void main(String[] args) throws InterruptedException {

        // 빠른 생산자: 1ms 간격으로 데이터 발행
        Flux<Long> fastProducer = Flux.interval(Duration.ofMillis(1));

        // onBackpressureDrop: 소비자가 처리 못하면 버림
        fastProducer
            .onBackpressureDrop(dropped ->
                System.out.println("버려진 항목: " + dropped))
            .publishOn(Schedulers.boundedElastic())
            .subscribe(item -> {
                // 느린 소비자: 100ms 걸림
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                System.out.println("처리: " + item);
            });

        Thread.sleep(5000);
    }
}
```

request를 사용하여 명시적으로 배압을 제어하는 예시도 살펴보자.

```java
import reactor.core.publisher.Flux;
import org.reactivestreams.Subscription;
import reactor.core.publisher.BaseSubscriber;

public class ExplicitBackpressure {

    public static void main(String[] args) {

        Flux<Integer> numbers = Flux.range(1, 100);

        numbers.subscribe(new BaseSubscriber<>() {
            private int count = 0;
            private final int BATCH_SIZE = 10;

            @Override
            protected void hookOnSubscribe(Subscription subscription) {
                // 처음에 10개만 요청
                request(BATCH_SIZE);
            }

            @Override
            protected void hookOnNext(Integer value) {
                System.out.println("처리: " + value);
                count++;
                if (count % BATCH_SIZE == 0) {
                    System.out.println("--- 배치 완료, 다음 " + BATCH_SIZE + "개 요청 ---");
                    request(BATCH_SIZE);
                }
            }

            @Override
            protected void hookOnComplete() {
                System.out.println("모든 데이터 처리 완료");
            }
        });
    }
}
```

위 코드에서 구독자는 한 번에 10개씩만 요청하여 처리 속도를 제어한다. `request(BATCH_SIZE)` 호출이 배압의 핵심이다.

### 1.4.4 Reactor의 배압 연산자 요약

```java
// 1. onBackpressureBuffer: 버퍼에 저장 (크기 제한 가능)
flux.onBackpressureBuffer(100)              // 최대 100개 버퍼
    .subscribe(...);

// 2. onBackpressureDrop: 초과분 버림
flux.onBackpressureDrop()
    .subscribe(...);

// 3. onBackpressureLatest: 최신 항목만 유지
flux.onBackpressureLatest()
    .subscribe(...);

// 4. onBackpressureError: 오류 발생
flux.onBackpressureError()
    .subscribe(...);

// 5. limitRate: 프리페치 크기 제한
flux.limitRate(50)                          // 한 번에 50개씩만 요청
    .subscribe(...);
```

---

## 1.5 왜 리액티브가 필요한가?

### 1.5.1 Thread-per-request 모델의 한계

전통적인 서블릿 기반 웹 애플리케이션은 하나의 HTTP 요청마다 하나의 스레드를 할당하는 thread-per-request 모델을 사용한다.

```
[요청 1] → [스레드 1] → DB 호출 (200ms 대기) → 응답
[요청 2] → [스레드 2] → API 호출 (300ms 대기) → 응답
[요청 3] → [스레드 3] → DB 호출 (200ms 대기) → 응답
  ...
[요청 201] → 스레드 풀 고갈 → 대기열에서 대기
```

이 모델의 문제점은 명확하다.

- **스레드 풀 크기 제한**: Tomcat 기본 스레드 풀은 200개다. 201번째 요청은 대기해야 한다.
- **I/O 대기 중 자원 낭비**: 스레드가 DB 응답을 기다리는 동안 아무 일도 하지 않지만 메모리(약 1MB/스레드)를 점유한다.
- **컨텍스트 스위칭 비용**: 스레드 수가 늘어나면 OS의 컨텍스트 스위칭 비용이 증가한다.

### 1.5.2 리소스 효율성 비교

같은 하드웨어에서 10,000개의 동시 연결을 처리하는 시나리오를 비교해 보자.

**thread-per-request 모델 (Spring MVC + Tomcat)**

```
필요 스레드: 10,000개
스레드당 메모리: ~1MB
총 메모리: ~10GB (스레드 스택만)
실제 CPU 작업: 약 5% (나머지 95%는 I/O 대기)
```

**이벤트 루프 모델 (Spring WebFlux + Netty)**

```
필요 스레드: CPU 코어 수 (예: 8개)
스레드당 메모리: ~1MB
총 메모리: ~8MB (스레드 스택)
실제 CPU 작업: 동일하지만 I/O 대기 없이 다른 요청 처리
```

```java
// Spring MVC: 블로킹 방식
@RestController
public class UserController {

    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        // 스레드가 DB 응답을 기다리며 차단됨
        User user = userRepository.findById(id);

        // 스레드가 외부 API 응답을 기다리며 차단됨
        UserProfile profile = profileClient.getProfile(user.getProfileId());

        user.setProfile(profile);
        return user;
    }
}

// Spring WebFlux: 논블로킹 방식
@RestController
public class UserController {

    @GetMapping("/users/{id}")
    public Mono<User> getUser(@PathVariable Long id) {
        // 스레드가 차단되지 않음 - 콜백으로 연결
        return userRepository.findById(id)
            .flatMap(user ->
                profileClient.getProfile(user.getProfileId())
                    .map(profile -> {
                        user.setProfile(profile);
                        return user;
                    })
            );
    }
}
```

### 1.5.3 리액티브가 적합한 유즈케이스

리액티브가 모든 상황에서 최선의 선택은 아니다. 다음은 리액티브가 적합한 경우와 그렇지 않은 경우이다.

**리액티브가 적합한 경우**

- **높은 동시 연결 수**: 채팅, 알림, 실시간 대시보드 등 수천~수만 개의 동시 연결이 필요한 경우
- **I/O 집약적 워크로드**: 다수의 외부 API 호출, 데이터베이스 쿼리가 주를 이루는 경우
- **스트리밍 데이터**: IoT 센서 데이터, 실시간 로그 처리, 주식 시세 등 연속적인 데이터 흐름
- **마이크로서비스 간 통신**: 서비스 간 비동기 메시지 교환이 빈번한 경우
- **Server-Sent Events / WebSocket**: 서버에서 클라이언트로 실시간 데이터를 푸시하는 경우

**리액티브가 적합하지 않은 경우**

- **CPU 집약적 작업**: 이미지 처리, 복잡한 수학 연산 등 CPU를 오래 사용하는 작업
- **단순한 CRUD 애플리케이션**: 동시 사용자가 적고 복잡한 비동기 흐름이 불필요한 경우
- **팀의 경험 부족**: 리액티브 프로그래밍의 학습 곡선과 디버깅 난이도를 감당하기 어려운 경우

### 1.5.4 성능 벤치마크 참고

아래는 동시 연결 수에 따른 처리량 변화를 개념적으로 나타낸 것이다.

```
처리량(req/s)
  ^
  |
  |         ╱ WebFlux (논블로킹)
  |       ╱
  |     ╱───────────────────
  |   ╱
  | ╱   ╱── MVC (블로킹)
  |╱  ╱
  | ╱
  |╱──────────
  +────────────────────────> 동시 연결 수
     100  500 1000  5000 10000
```

동시 연결 수가 적을 때는 Spring MVC와 WebFlux의 성능 차이가 거의 없다. 오히려 MVC가 약간 빠를 수도 있다. 하지만 동시 연결 수가 증가하면 MVC의 처리량은 스레드 풀 크기에 의해 제한되는 반면, WebFlux는 적은 스레드로도 높은 처리량을 유지한다.

---

## 정리

이 장에서 다룬 핵심 내용을 정리하면 다음과 같다.

| 주제 | 핵심 내용 |
|------|----------|
| 리액티브 프로그래밍 | 데이터 스트림과 변화의 전파에 초점을 맞춘 비동기 프로그래밍 패러다임 |
| 리액티브 선언문 | 응답성, 탄력성, 유연성, 메시지 기반의 네 가지 속성 |
| 명령형 vs 리액티브 | 명령형은 "어떻게", 리액티브는 "무엇을" 선언. 각각의 장단점이 존재 |
| 리액티브 스트림 | Publisher, Subscriber, Subscription, Processor 4개 인터페이스로 구성된 표준 |
| 배압 | 소비자가 생산자에게 속도 조절을 요청하는 메커니즘 |
| 리액티브의 필요성 | I/O 집약적이고 높은 동시성이 요구되는 시스템에 적합 |

다음 장에서는 이 개념들의 구체적인 구현체인 **Project Reactor**를 깊이 살펴본다. Mono와 Flux의 사용법, 주요 연산자, 그리고 실전 패턴을 다룬다.


---

# Chapter 2. Spring WebFlux 개요

Spring WebFlux는 Spring Framework 5에서 도입된 리액티브 웹 프레임워크다. 기존 Spring MVC가 서블릿 기반의 동기/블로킹 모델 위에 구축되었다면, WebFlux는 논블로킹 I/O와 리액티브 스트림을 기반으로 설계되었다. 이 장에서는 WebFlux의 전체적인 아키텍처, 내부 동작 원리, 그리고 언제 WebFlux를 선택해야 하는지에 대해 살펴본다.

---

## 2.1 Spring MVC와 Spring WebFlux 비교

### 2.1.1 아키텍처 차이: 서블릿 스택 vs 리액티브 스택

Spring MVC는 Java Servlet API 위에 구축된다. 클라이언트 요청이 들어오면 서블릿 컨테이너(Tomcat, Jetty 등)가 스레드 풀에서 하나의 스레드를 할당하고, 해당 스레드가 요청의 시작부터 끝까지 전체 처리를 담당한다. 이를 **thread-per-request** 모델이라 한다.

```
[Spring MVC 스택]
┌─────────────────────┐
│   Servlet Container  │  (Tomcat, Jetty)
│   ┌───────────────┐  │
│   │ DispatcherServlet │
│   │   ┌─────────┐ │  │
│   │   │ Handler  │ │  │
│   │   │ Mapping  │ │  │
│   │   └─────────┘ │  │
│   │   ┌─────────┐ │  │
│   │   │Controller│ │  │
│   │   └─────────┘ │  │
│   └───────────────┘  │
│   Servlet API        │
│   (Blocking I/O)     │
└─────────────────────┘
```

반면 Spring WebFlux는 리액티브 스택 위에 구축된다. 서블릿 API에 의존하지 않으며, 기본적으로 Netty를 런타임으로 사용한다. 소수의 이벤트 루프 스레드가 다수의 요청을 논블로킹 방식으로 처리한다.

```
[Spring WebFlux 스택]
┌─────────────────────┐
│   Reactive Runtime   │  (Netty, Undertow)
│   ┌───────────────┐  │
│   │DispatcherHandler│
│   │   ┌─────────┐ │  │
│   │   │ Handler  │ │  │
│   │   │ Mapping  │ │  │
│   │   └─────────┘ │  │
│   │   ┌─────────┐ │  │
│   │   │Controller│ │  │
│   │   │   or     │ │  │
│   │   │RouterFunc│ │  │
│   │   └─────────┘ │  │
│   └───────────────┘  │
│   Reactive Streams   │
│   (Non-Blocking I/O) │
└─────────────────────┘
```

### 2.1.2 스레드 모델 차이

**Spring MVC**의 스레드 모델은 직관적이다. 동시에 200개의 요청을 처리하려면 최소 200개의 스레드가 필요하다. 각 스레드는 데이터베이스 응답을 기다리는 동안에도 점유된 상태로 남는다.

```
[Spring MVC - Thread-per-Request]

요청 A ──▶ Thread-1: [수신]──[처리]──[DB 대기...]──[응답]──▶ 완료
요청 B ──▶ Thread-2: [수신]──[처리]──[DB 대기...]──[응답]──▶ 완료
요청 C ──▶ Thread-3: [수신]──[처리]──[DB 대기...]──[응답]──▶ 완료
  ...
요청 N ──▶ Thread-N: (스레드 풀 고갈 → 대기 큐에서 대기)
```

**Spring WebFlux**는 이벤트 루프 기반이다. CPU 코어 수만큼의 소수 스레드(기본적으로 코어 수 x 1)가 모든 요청을 논블로킹으로 처리한다. I/O 대기 시간 동안 스레드가 다른 요청을 처리할 수 있다.

```
[Spring WebFlux - Event Loop]

EventLoop-1: [요청A 수신]─[요청B 수신]─[요청A DB콜백]─[요청C 수신]─[요청B DB콜백]─...
EventLoop-2: [요청D 수신]─[요청E 수신]─[요청D DB콜백]─[요청F 수신]─[요청E DB콜백]─...
```

**처리량과 지연 시간 비교**

| 항목 | Spring MVC | Spring WebFlux |
|------|-----------|---------------|
| 동시 연결 수 | 스레드 풀 크기에 제한 (보통 200~500) | 수만 개 이상 동시 연결 가능 |
| 스레드 수 | 요청 수에 비례 | CPU 코어 수에 비례 (고정) |
| 메모리 사용 | 스레드당 약 512KB~1MB 스택 | 적은 스레드로 메모리 효율적 |
| I/O 바운드 작업 | 대기 중 스레드 낭비 | 대기 중 다른 작업 처리 |
| CPU 바운드 작업 | 효율적 | 이점 없음 (오히려 복잡성 증가) |
| 지연 시간 | 부하 낮을 때 약간 유리 | 부하 높을 때 안정적 |
| 최대 처리량 | 스레드 풀 포화 시 급감 | 일정하게 유지 |

### 2.1.3 코드 스타일 비교

동일한 사용자 조회 API를 두 방식으로 구현하여 비교해보자.

**Spring MVC 방식:**

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable String id) {
        User user = userService.findById(id);  // 블로킹 호출
        if (user == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(user);
    }

    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        List<User> users = userService.findAll();  // 블로킹 호출
        return ResponseEntity.ok(users);
    }

    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User saved = userService.save(user);  // 블로킹 호출
        return ResponseEntity
                .created(URI.create("/api/users/" + saved.getId()))
                .body(saved);
    }
}
```

**Spring WebFlux 방식:**

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<User>> getUser(@PathVariable String id) {
        return userService.findById(id)                    // 논블로킹 호출
                .map(user -> ResponseEntity.ok(user))
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @GetMapping
    public Flux<User> getAllUsers() {
        return userService.findAll();  // 논블로킹, 스트리밍 가능
    }

    @PostMapping
    public Mono<ResponseEntity<User>> createUser(@RequestBody User user) {
        return userService.save(user)                      // 논블로킹 호출
                .map(saved -> ResponseEntity
                        .created(URI.create("/api/users/" + saved.getId()))
                        .body(saved));
    }
}
```

핵심적인 차이점을 정리하면 다음과 같다.

| 구분 | Spring MVC | Spring WebFlux |
|------|-----------|---------------|
| 반환 타입 | `User`, `List<User>` | `Mono<User>`, `Flux<User>` |
| 실행 방식 | 메서드 호출 시 즉시 실행 | 구독(subscribe) 시 실행 |
| 데이터 흐름 | 동기적, 순차적 | 비동기적, 이벤트 기반 |
| 에러 처리 | try-catch | `onErrorResume`, `onErrorReturn` |
| 기본 서버 | Tomcat | Netty |

---

## 2.2 WebFlux의 내부 구조와 Netty

### 2.2.1 Netty란 무엇인가

Netty는 JVM 위에서 동작하는 비동기 이벤트 기반 네트워크 프레임워크다. 고성능 프로토콜 서버와 클라이언트를 빠르게 개발할 수 있도록 설계되었으며, HTTP, WebSocket, TCP, UDP 등 다양한 프로토콜을 지원한다.

Spring WebFlux가 Netty를 기본 런타임으로 선택한 이유는 다음과 같다.

- **논블로킹 I/O**: Java NIO 기반으로 소수 스레드로 대량의 동시 연결 처리
- **이벤트 루프 모델**: 효율적인 리소스 활용과 높은 동시성
- **검증된 안정성**: Discord, Apple, Netflix 등 대규모 서비스에서 검증
- **풍부한 프로토콜 지원**: HTTP/1.1, HTTP/2, WebSocket 기본 지원

### 2.2.2 이벤트 루프(Event Loop) 모델

Netty의 이벤트 루프는 하나의 스레드가 **셀렉터(Selector)**를 통해 여러 채널(연결)의 I/O 이벤트를 감시하고 처리하는 구조다.

```
[Netty 이벤트 루프 구조]

                  ┌──────────────────────────────┐
                  │       EventLoopGroup          │
                  │  (Boss Group - 연결 수락)      │
                  │  ┌────────────────────────┐   │
                  │  │ EventLoop (Thread-1)   │   │
                  │  │  → 새 연결 수락(accept)  │   │
                  │  └────────────────────────┘   │
                  └──────────┬───────────────────┘
                             │ 연결을 Worker에 등록
                  ┌──────────▼───────────────────┐
                  │       EventLoopGroup          │
                  │  (Worker Group - I/O 처리)     │
                  │  ┌────────────────────────┐   │
                  │  │ EventLoop-1 (Thread)   │   │
                  │  │  채널 A, D, G 담당      │   │
                  │  └────────────────────────┘   │
                  │  ┌────────────────────────┐   │
                  │  │ EventLoop-2 (Thread)   │   │
                  │  │  채널 B, E, H 담당      │   │
                  │  └────────────────────────┘   │
                  │  ┌────────────────────────┐   │
                  │  │ EventLoop-N (Thread)   │   │
                  │  │  채널 C, F, I 담당      │   │
                  │  └────────────────────────┘   │
                  └──────────────────────────────┘
```

각 이벤트 루프 스레드는 다음 과정을 무한 반복한다.

1. **Selector로 I/O 이벤트 대기**: 등록된 채널 중 읽기/쓰기 가능한 채널이 있는지 확인
2. **이벤트 처리**: 준비된 채널의 데이터를 읽거나 쓰기
3. **태스크 큐 처리**: 예약된 작업(스케줄된 태스크) 실행

이 모델의 핵심 규칙은 **하나의 채널은 항상 같은 이벤트 루프에 바인딩**된다는 것이다. 이로 인해 동기화 없이도 스레드 안전성이 보장된다.

### 2.2.3 HttpHandler, WebHandler, DispatcherHandler 파이프라인

Spring WebFlux는 내부적으로 계층화된 핸들러 파이프라인을 구성한다.

```
[요청 처리 파이프라인]

HTTP 요청
   │
   ▼
┌──────────────┐
│  HttpHandler │  ← 서버 API와 리액티브 스트림의 연결점
│  (최하위 계층) │     Netty, Undertow 등 서버별 어댑터 제공
└──────┬───────┘
       ▼
┌──────────────────┐
│  WebHttpHandler  │  ← HttpHandler를 감싸는 데코레이터
│  Build           │     세션, 코덱, 로케일 등 웹 기능 통합
└──────┬───────────┘
       ▼
┌──────────────────┐
│   WebFilter 체인  │  ← 요청/응답을 가로채는 필터 (인증, 로깅 등)
└──────┬───────────┘
       ▼
┌──────────────────┐
│ WebExceptionHandler │  ← 예외 처리
└──────┬───────────┘
       ▼
┌──────────────────┐
│ DispatcherHandler │  ← 핵심 디스패처 (MVC의 DispatcherServlet 역할)
│  ┌─────────────┐ │
│  │HandlerMapping│ │  → 요청 URL을 핸들러에 매핑
│  └──────┬──────┘ │
│  ┌──────▼──────┐ │
│  │HandlerAdapter│ │  → 핸들러 실행
│  └──────┬──────┘ │
│  ┌──────▼──────┐ │
│  │ResultHandler │ │  → 결과를 HTTP 응답으로 변환
│  └─────────────┘ │
└──────────────────┘
```

**HttpHandler**는 가장 낮은 수준의 계약이다. 단일 메서드 `handle(ServerHttpRequest, ServerHttpResponse)`를 정의하며, Netty, Undertow, Tomcat(서블릿 3.1+) 등의 서버별 어댑터가 이를 구현한다.

```java
public interface HttpHandler {
    Mono<Void> handle(ServerHttpRequest request, ServerHttpResponse response);
}
```

**DispatcherHandler**는 Spring MVC의 `DispatcherServlet`에 해당하는 중앙 디스패처다. 세 단계로 요청을 처리한다.

```java
// DispatcherHandler의 핵심 로직 (간략화)
public Mono<Void> handle(ServerWebExchange exchange) {
    return Flux.fromIterable(this.handlerMappings)       // 1. 핸들러 매핑 탐색
            .concatMap(mapping -> mapping.getHandler(exchange))
            .next()
            .flatMap(handler -> invokeHandler(exchange, handler))  // 2. 핸들러 실행
            .flatMap(result -> handleResult(exchange, result));    // 3. 결과 처리
}
```

### 2.2.4 요청 처리 흐름

클라이언트의 HTTP 요청이 WebFlux 애플리케이션에 도달하여 응답이 반환되기까지의 전체 흐름을 정리하면 다음과 같다.

1. **Netty가 TCP 연결을 수락**하고 HTTP 요청을 파싱한다.
2. **HttpHandler 어댑터**가 Netty의 요청/응답 객체를 `ServerHttpRequest`, `ServerHttpResponse`로 변환한다.
3. **WebHttpHandlerBuilder**가 구성한 필터 체인(`WebFilter`)이 순서대로 실행된다.
4. **DispatcherHandler**가 `HandlerMapping`을 통해 적절한 핸들러를 찾는다.
   - `RequestMappingHandlerMapping`: 어노테이션 기반 핸들러
   - `RouterFunctionMapping`: 함수형 라우터
5. **HandlerAdapter**가 핸들러를 실행하고 `Mono<HandlerResult>`를 반환한다.
6. **HandlerResultHandler**가 결과를 HTTP 응답으로 변환하여 클라이언트에 전송한다.

모든 단계가 `Mono`와 `Flux`로 연결되어 있어 전체 파이프라인이 논블로킹으로 동작한다. 어느 한 단계에서도 스레드를 블로킹하지 않는다는 것이 핵심이다.

---

## 2.3 논블로킹 I/O의 원리

### 2.3.1 블로킹 I/O vs 논블로킹 I/O

**블로킹 I/O**에서는 `read()` 또는 `write()` 호출 시 데이터가 준비될 때까지 호출한 스레드가 대기 상태에 들어간다. 스레드는 아무 일도 하지 못하면서 시스템 리소스를 점유한다.

```java
// 블로킹 I/O 예시 (java.io)
try (Socket socket = new Socket("example.com", 80);
     InputStream in = socket.getInputStream()) {

    byte[] buffer = new byte[1024];
    int bytesRead = in.read(buffer);  // ← 데이터가 올 때까지 스레드 블로킹
    // 이 줄은 데이터를 읽을 때까지 실행되지 않는다
    processData(buffer, bytesRead);
}
```

```
[블로킹 I/O 타임라인]

Thread-1: ──[read() 호출]──────[대기중...]──────[데이터 수신]──[처리]──▶
                               ↑
                         스레드가 아무 일도 못함
```

**논블로킹 I/O**에서는 `read()` 호출이 즉시 반환된다. 데이터가 아직 없으면 "아직 없다"는 결과를 반환하고, 스레드는 다른 작업을 수행할 수 있다.

```java
// 논블로킹 I/O 예시 (java.nio)
SocketChannel channel = SocketChannel.open();
channel.configureBlocking(false);  // 논블로킹 모드 설정
channel.connect(new InetSocketAddress("example.com", 80));

ByteBuffer buffer = ByteBuffer.allocate(1024);
int bytesRead = channel.read(buffer);  // ← 즉시 반환 (데이터 없으면 0 또는 -1)
// 스레드가 블로킹되지 않으므로 바로 다음 줄 실행
```

```
[논블로킹 I/O 타임라인]

Thread-1: ──[read()→0]──[다른작업]──[read()→0]──[다른작업]──[read()→데이터]──[처리]──▶
              ↑             ↑           ↑           ↑
         즉시 반환      유용한 작업   즉시 반환    유용한 작업
```

### 2.3.2 Java NIO와 Selector

Java NIO(New I/O)의 핵심 컴포넌트인 **Selector**는 하나의 스레드가 여러 채널의 I/O 이벤트를 효율적으로 감시할 수 있게 한다. 운영체제의 `epoll`(Linux), `kqueue`(macOS) 시스템 콜을 활용한다.

```java
// Java NIO Selector 사용 예시
Selector selector = Selector.open();

// 여러 채널을 셀렉터에 등록
ServerSocketChannel serverChannel = ServerSocketChannel.open();
serverChannel.configureBlocking(false);
serverChannel.bind(new InetSocketAddress(8080));
serverChannel.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    // I/O 이벤트가 있을 때까지 대기 (효율적인 대기)
    selector.select();

    Set<SelectionKey> selectedKeys = selector.selectedKeys();
    Iterator<SelectionKey> iter = selectedKeys.iterator();

    while (iter.hasNext()) {
        SelectionKey key = iter.next();

        if (key.isAcceptable()) {
            // 새 연결 수락
            SocketChannel client = serverChannel.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        } else if (key.isReadable()) {
            // 데이터 읽기 가능
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            client.read(buffer);
            // 데이터 처리...
        }

        iter.remove();
    }
}
```

```
[Selector 동작 원리]

                    ┌───────────────┐
                    │   Selector    │
                    │   (Thread-1)  │
                    └───┬───┬───┬───┘
                        │   │   │
            ┌───────────┘   │   └───────────┐
            ▼               ▼               ▼
       ┌─────────┐   ┌─────────┐   ┌─────────┐
       │Channel A│   │Channel B│   │Channel C│
       │ (READ)  │   │ (WRITE) │   │ (READ)  │
       └─────────┘   └─────────┘   └─────────┘

  하나의 스레드가 select()를 호출하면:
  → 운영체제가 준비된 채널만 알려줌 (예: A와 C)
  → 스레드가 A와 C만 처리 (불필요한 폴링 없음)
```

### 2.3.3 이벤트 루프의 동작 방식

Netty의 이벤트 루프는 Java NIO의 Selector를 기반으로 하되, 더 정교한 태스크 스케줄링과 파이프라인 처리를 추가한 것이다.

이벤트 루프의 한 사이클(iteration)은 다음과 같다.

```
[이벤트 루프 사이클]

┌─────────────────────────────────────────────┐
│                Event Loop                    │
│                                              │
│  1. select()  ─── I/O 이벤트 감지            │
│       │                                      │
│       ▼                                      │
│  2. processSelectedKeys() ─── I/O 처리       │
│       │    (데이터 읽기/쓰기, 연결 수락)       │
│       ▼                                      │
│  3. runAllTasks() ─── 태스크 큐 처리          │
│       │    (사용자가 제출한 작업, 타이머 등)    │
│       │                                      │
│       └──────── 반복 ────────────────────────│
└─────────────────────────────────────────────┘
```

중요한 원칙: **이벤트 루프 스레드에서 블로킹 작업을 절대 수행하면 안 된다.** 하나의 이벤트 루프가 수천 개의 연결을 담당하므로, 해당 스레드가 블로킹되면 수천 개의 연결이 동시에 지연된다.

```java
// 절대 하면 안 되는 코드 (이벤트 루프에서 블로킹)
@GetMapping("/bad-example")
public Mono<String> badExample() {
    Thread.sleep(1000);  // 이벤트 루프 스레드를 1초간 블로킹!
    return Mono.just("이렇게 하면 안 됩니다");
}

// 올바른 코드 (논블로킹)
@GetMapping("/good-example")
public Mono<String> goodExample() {
    return Mono.delay(Duration.ofSeconds(1))  // 논블로킹 대기
            .then(Mono.just("논블로킹으로 1초 후 응답"));
}
```

블로킹이 불가피한 경우에는 별도의 스케줄러로 작업을 위임해야 한다.

```java
// 블로킹이 불가피한 경우 - 별도 스케줄러 사용
@GetMapping("/blocking-needed")
public Mono<String> blockingNeeded() {
    return Mono.fromCallable(() -> {
                // 블로킹 API 호출 (예: 레거시 JDBC)
                return legacyService.queryDatabase();
            })
            .subscribeOn(Schedulers.boundedElastic());  // 블로킹 전용 스레드 풀
}
```

---

## 2.4 WebFlux를 선택해야 하는 경우와 그렇지 않은 경우

### 2.4.1 WebFlux가 적합한 시나리오

**1. 높은 동시성이 요구되는 I/O 바운드 애플리케이션**

마이크로서비스 게이트웨이, API 중개 서비스처럼 다수의 외부 서비스를 호출하고 결과를 조합하는 경우에 WebFlux가 빛을 발한다.

```java
// 여러 외부 서비스를 동시에 호출하여 결과 조합
public Mono<DashboardData> getDashboard(String userId) {
    Mono<UserProfile> profile = userService.getProfile(userId);
    Mono<List<Order>> orders = orderService.getOrders(userId);
    Mono<List<Notification>> notifications = notificationService.get(userId);

    return Mono.zip(profile, orders, notifications)
            .map(tuple -> new DashboardData(
                    tuple.getT1(),
                    tuple.getT2(),
                    tuple.getT3()
            ));
    // 세 호출이 동시에 실행되어 전체 응답 시간 단축
}
```

**2. 실시간 스트리밍 애플리케이션**

SSE(Server-Sent Events), WebSocket을 활용한 실시간 데이터 스트리밍에 WebFlux의 `Flux`가 자연스럽게 대응한다.

```java
// 실시간 주가 스트리밍
@GetMapping(value = "/stocks/{symbol}/stream",
            produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<StockPrice> streamStockPrice(@PathVariable String symbol) {
    return stockService.getPriceStream(symbol);  // 무한 스트림
}
```

**3. 대량의 동시 연결을 유지해야 하는 경우**

채팅 서비스, 알림 시스템처럼 수천~수만 개의 커넥션을 장시간 유지해야 하는 경우, 스레드-퍼-리퀘스트 모델은 메모리 한계에 금방 도달한다.

**4. 전체 파이프라인이 리액티브인 경우**

데이터베이스(MongoDB Reactive, R2DBC), 메시지 브로커(Reactor Kafka, Reactor RabbitMQ), HTTP 클라이언트(WebClient) 모두 리액티브 드라이버를 사용할 수 있을 때 WebFlux의 이점이 극대화된다.

### 2.4.2 WebFlux가 부적합한 시나리오

**1. JDBC/JPA(관계형 DB) 블로킹 드라이버를 사용하는 경우**

전통적인 JDBC나 Spring Data JPA는 블로킹 API다. WebFlux 위에서 사용하면 이벤트 루프를 블로킹하게 되어 오히려 성능이 저하된다. R2DBC가 대안이지만, JPA의 풍부한 기능(지연 로딩, 캐시 등)을 포기해야 한다.

**2. CPU 집약적인 작업이 대부분인 경우**

이미지 처리, 복잡한 계산, 암호화 등 CPU를 장시간 사용하는 작업에서는 논블로킹 I/O의 이점이 없다. 오히려 리액티브 프로그래밍의 복잡성만 추가된다.

**3. 팀의 리액티브 프로그래밍 경험이 부족한 경우**

리액티브 프로그래밍은 학습 곡선이 가파르다. 디버깅이 어렵고, 기존의 명령형 사고방식과 근본적으로 다른 접근이 필요하다. 팀 전체가 충분히 준비되지 않은 상태에서 도입하면 생산성이 크게 떨어질 수 있다.

**4. 동시 요청 수가 적은 내부 관리 도구**

동시 사용자가 수십 명 수준인 백오피스 시스템에서는 Spring MVC가 충분하며, WebFlux를 도입할 이유가 없다.

### 2.4.3 의사결정 기준

다음 체크리스트를 통해 WebFlux 도입 여부를 판단할 수 있다.

```
[WebFlux 도입 의사결정 흐름]

높은 동시성(수천 이상)이 필요한가?
  ├── 아니오 → Spring MVC 사용
  └── 예
       │
       전체 I/O 파이프라인이 논블로킹 가능한가?
       (DB, 메시지 큐, 외부 API 등)
         ├── 아니오 → Spring MVC 사용 (또는 부분적 리액티브)
         └── 예
              │
              팀이 리액티브 프로그래밍에 익숙한가?
                ├── 아니오 → 학습 기간 확보 후 도입 검토
                └── 예 → Spring WebFlux 사용
```

---

## 2.5 WebFlux의 두 가지 프로그래밍 모델

Spring WebFlux는 두 가지 프로그래밍 모델을 제공한다. 어노테이션 기반 모델과 함수형 엔드포인트 모델이다. 두 모델은 동일한 리액티브 런타임 위에서 동작하며, 하나의 애플리케이션 내에서 혼용할 수도 있다.

### 2.5.1 어노테이션 기반 모델

Spring MVC를 사용해본 개발자에게 가장 친숙한 방식이다. `@Controller`, `@RestController`, `@RequestMapping` 등의 어노테이션을 그대로 사용하되, 반환 타입이 `Mono`와 `Flux`로 바뀐다.

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    /**
     * 단일 상품 조회
     */
    @GetMapping("/{id}")
    public Mono<ResponseEntity<Product>> getProduct(@PathVariable String id) {
        return productService.findById(id)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    /**
     * 전체 상품 목록 조회
     */
    @GetMapping
    public Flux<Product> getAllProducts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return productService.findAll(page, size);
    }

    /**
     * 상품 생성
     */
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<Product> createProduct(@Valid @RequestBody Product product) {
        return productService.save(product);
    }

    /**
     * 상품 수정
     */
    @PutMapping("/{id}")
    public Mono<ResponseEntity<Product>> updateProduct(
            @PathVariable String id,
            @Valid @RequestBody Product product) {
        return productService.update(id, product)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    /**
     * 상품 삭제
     */
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteProduct(@PathVariable String id) {
        return productService.deleteById(id);
    }

    /**
     * 카테고리별 상품 스트리밍 (SSE)
     */
    @GetMapping(value = "/stream/category/{category}",
                produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<Product> streamByCategory(@PathVariable String category) {
        return productService.findByCategoryStream(category);
    }
}
```

서비스 계층도 함께 살펴보자.

```java
@Service
public class ProductService {

    private final ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    public Mono<Product> findById(String id) {
        return productRepository.findById(id);
    }

    public Flux<Product> findAll(int page, int size) {
        return productRepository.findAll()
                .skip((long) page * size)
                .take(size);
    }

    public Mono<Product> save(Product product) {
        product.setCreatedAt(LocalDateTime.now());
        return productRepository.save(product);
    }

    public Mono<Product> update(String id, Product product) {
        return productRepository.findById(id)
                .flatMap(existing -> {
                    existing.setName(product.getName());
                    existing.setPrice(product.getPrice());
                    existing.setUpdatedAt(LocalDateTime.now());
                    return productRepository.save(existing);
                });
    }

    public Mono<Void> deleteById(String id) {
        return productRepository.deleteById(id);
    }

    public Flux<Product> findByCategoryStream(String category) {
        return productRepository.findByCategory(category);
    }
}
```

### 2.5.2 함수형 엔드포인트 모델

함수형 모델은 라우팅과 핸들러를 프로그래밍 방식으로 정의한다. `RouterFunction`이 라우팅 규칙을 정의하고, `HandlerFunction`이 요청을 처리한다.

**핸들러(Handler):**

```java
@Component
public class ProductHandler {

    private final ProductService productService;

    public ProductHandler(ProductService productService) {
        this.productService = productService;
    }

    /**
     * 단일 상품 조회
     */
    public Mono<ServerResponse> getProduct(ServerRequest request) {
        String id = request.pathVariable("id");
        return productService.findById(id)
                .flatMap(product -> ServerResponse.ok()
                        .contentType(MediaType.APPLICATION_JSON)
                        .bodyValue(product))
                .switchIfEmpty(ServerResponse.notFound().build());
    }

    /**
     * 전체 상품 목록 조회
     */
    public Mono<ServerResponse> getAllProducts(ServerRequest request) {
        int page = request.queryParam("page")
                .map(Integer::parseInt).orElse(0);
        int size = request.queryParam("size")
                .map(Integer::parseInt).orElse(20);

        Flux<Product> products = productService.findAll(page, size);
        return ServerResponse.ok()
                .contentType(MediaType.APPLICATION_JSON)
                .body(products, Product.class);
    }

    /**
     * 상품 생성
     */
    public Mono<ServerResponse> createProduct(ServerRequest request) {
        return request.bodyToMono(Product.class)
                .flatMap(productService::save)
                .flatMap(saved -> ServerResponse
                        .created(URI.create("/api/products/" + saved.getId()))
                        .contentType(MediaType.APPLICATION_JSON)
                        .bodyValue(saved));
    }

    /**
     * 상품 수정
     */
    public Mono<ServerResponse> updateProduct(ServerRequest request) {
        String id = request.pathVariable("id");
        return request.bodyToMono(Product.class)
                .flatMap(product -> productService.update(id, product))
                .flatMap(updated -> ServerResponse.ok()
                        .contentType(MediaType.APPLICATION_JSON)
                        .bodyValue(updated))
                .switchIfEmpty(ServerResponse.notFound().build());
    }

    /**
     * 상품 삭제
     */
    public Mono<ServerResponse> deleteProduct(ServerRequest request) {
        String id = request.pathVariable("id");
        return productService.deleteById(id)
                .then(ServerResponse.noContent().build());
    }
}
```

**라우터(Router):**

```java
@Configuration
public class ProductRouter {

    @Bean
    public RouterFunction<ServerResponse> productRoutes(ProductHandler handler) {
        return RouterFunctions.route()
                .path("/api/products", builder -> builder
                        .GET("/{id}", handler::getProduct)
                        .GET("", handler::getAllProducts)
                        .POST("", handler::createProduct)
                        .PUT("/{id}", handler::updateProduct)
                        .DELETE("/{id}", handler::deleteProduct)
                )
                .build();
    }
}
```

여러 도메인의 라우터를 조합할 수도 있다.

```java
@Configuration
public class AppRouter {

    @Bean
    public RouterFunction<ServerResponse> allRoutes(
            ProductHandler productHandler,
            OrderHandler orderHandler,
            UserHandler userHandler) {

        return RouterFunctions.route()
                .path("/api/products", builder -> builder
                        .GET("/{id}", productHandler::getProduct)
                        .GET("", productHandler::getAllProducts)
                        .POST("", productHandler::createProduct)
                )
                .path("/api/orders", builder -> builder
                        .GET("/{id}", orderHandler::getOrder)
                        .GET("", orderHandler::getAllOrders)
                        .POST("", orderHandler::createOrder)
                )
                .path("/api/users", builder -> builder
                        .GET("/{id}", userHandler::getUser)
                        .POST("", userHandler::createUser)
                )
                .filter((request, next) -> {
                    // 공통 필터: 요청 로깅
                    System.out.println("Request: " + request.method()
                            + " " + request.path());
                    return next.handle(request);
                })
                .build();
    }
}
```

### 2.5.3 두 모델의 비교와 선택 기준

| 기준 | 어노테이션 기반 | 함수형 엔드포인트 |
|------|--------------|----------------|
| 학습 비용 | 낮음 (MVC 경험 활용) | 중간 (새로운 API 학습 필요) |
| 코드 스타일 | 선언적 (어노테이션) | 프로그래밍 방식 (코드로 라우팅) |
| 라우팅 유연성 | 제한적 | 매우 유연 (조건부 라우팅 등) |
| 테스트 | `@WebFluxTest` | 순수 단위 테스트 용이 |
| 검증 | `@Valid` 자동 적용 | 수동으로 검증 로직 작성 |
| IDE 지원 | 우수 (자동완성, 네비게이션) | 보통 |
| 한 파일 응집도 | 낮음 (라우팅이 분산) | 높음 (한 곳에서 라우팅 파악) |

**어노테이션 기반을 선택하는 경우:**

- 기존 Spring MVC 경험이 있는 팀
- 빠른 개발 속도가 중요한 프로젝트
- 표준적인 CRUD API를 구현하는 경우
- Bean Validation을 적극 활용하는 경우

**함수형 엔드포인트를 선택하는 경우:**

- 라우팅 규칙이 복잡하거나 동적인 경우
- 경량 마이크로서비스에서 최소한의 프레임워크 의존이 필요한 경우
- 함수형 프로그래밍 스타일을 선호하는 팀
- 테스트에서 스프링 컨텍스트 없이 핸들러를 단위 테스트하고 싶은 경우

실무에서는 어노테이션 기반 모델이 더 널리 사용된다. Spring MVC에서의 전환 비용이 낮고, 대부분의 팀이 이미 익숙하기 때문이다. 함수형 모델은 특수한 라우팅 요구사항이 있거나, 팀이 함수형 스타일에 익숙한 경우에 선택하면 좋다.

---

## 정리

이 장에서 다룬 핵심 내용을 요약하면 다음과 같다.

- **Spring MVC vs WebFlux**: MVC는 서블릿 기반 thread-per-request 모델이고, WebFlux는 이벤트 루프 기반 논블로킹 모델이다. WebFlux는 높은 동시성에서 적은 리소스로 안정적인 처리량을 유지한다.
- **Netty와 이벤트 루프**: WebFlux의 기본 런타임인 Netty는 이벤트 루프 모델을 통해 소수의 스레드로 수만 개의 동시 연결을 처리한다. 이벤트 루프 스레드를 블로킹하면 안 된다.
- **논블로킹 I/O**: Java NIO의 Selector를 활용하여 하나의 스레드가 여러 채널의 I/O를 효율적으로 관리한다. 데이터가 준비될 때만 처리하므로 스레드 낭비가 없다.
- **도입 판단 기준**: 높은 동시성, 리액티브 파이프라인, 팀 역량의 세 조건이 모두 충족될 때 WebFlux를 선택한다.
- **두 가지 프로그래밍 모델**: 어노테이션 기반은 MVC 경험을 활용할 수 있어 접근성이 높고, 함수형 모델은 라우팅의 유연성과 테스트 용이성에서 장점이 있다.

다음 장에서는 WebFlux의 핵심 기반인 **Project Reactor**를 깊이 있게 다룬다. `Mono`와 `Flux`의 동작 원리, 주요 연산자, 에러 처리 전략 등을 살펴볼 것이다.


---

# Chapter 3. Project Reactor 핵심

Project Reactor는 Spring WebFlux의 리액티브 프로그래밍 기반이다. 이 장에서는 Reactor의 두 가지 핵심 타입인 `Mono`와 `Flux`를 깊이 있게 다루고, 실전에서 빈번하게 사용하는 연산자, 에러 처리, 스케줄러, 그리고 디버깅 기법까지 체계적으로 살펴본다.

---

## 3.1 Mono와 Flux 이해하기

### 3.1.1 Mono: 0..1개의 요소

`Mono<T>`는 **최대 1개의 요소**를 발행하는 Publisher이다. 데이터베이스에서 단일 레코드를 조회하거나, HTTP 요청의 응답 하나를 반환할 때 주로 사용한다.

```java
// 값이 있는 Mono
Mono<String> mono = Mono.just("Hello Reactor");

// 빈 Mono (값 없이 완료)
Mono<String> empty = Mono.empty();

// 에러를 발행하는 Mono
Mono<String> error = Mono.error(new RuntimeException("오류 발생"));
```

### 3.1.2 Flux: 0..N개의 요소

`Flux<T>`는 **0개에서 N개까지의 요소**를 발행하는 Publisher이다. 컬렉션 데이터를 스트리밍하거나, 실시간 이벤트를 연속적으로 전달할 때 사용한다.

```java
// 여러 값을 가진 Flux
Flux<String> flux = Flux.just("Spring", "WebFlux", "Reactor");

// 리스트에서 Flux 생성
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
Flux<Integer> fromList = Flux.fromIterable(numbers);

// 범위로 생성
Flux<Integer> range = Flux.range(1, 10); // 1부터 10까지
```

### 3.1.3 다양한 생성 방법

```java
// defer: 구독 시점에 Mono/Flux를 생성 (Lazy 평가)
Mono<Long> deferred = Mono.defer(() -> Mono.just(System.currentTimeMillis()));

// fromCallable: Callable로부터 Mono 생성
Mono<String> fromCallable = Mono.fromCallable(() -> {
    // 블로킹 작업도 래핑 가능
    return someBlockingMethod();
});

// create: 프로그래밍 방식으로 Flux 생성 (비동기 브릿지)
Flux<String> created = Flux.create(sink -> {
    sink.next("첫 번째");
    sink.next("두 번째");
    sink.next("세 번째");
    sink.complete();
});

// generate: 동기적으로 하나씩 값을 생성
Flux<Integer> generated = Flux.generate(
    () -> 0,                        // 초기 상태
    (state, sink) -> {
        sink.next(state);
        if (state == 9) sink.complete();
        return state + 1;           // 다음 상태
    }
);

// interval: 일정 간격으로 값 발행 (0부터 증가하는 Long)
Flux<Long> interval = Flux.interval(Duration.ofSeconds(1));
```

### 3.1.4 구독(subscribe)의 의미와 동작

Reactor에서 가장 핵심적인 개념은 **"아무것도 구독하지 않으면 아무 일도 일어나지 않는다"** 는 것이다. `Mono`와 `Flux`는 선언적 파이프라인일 뿐, `subscribe()`를 호출해야 실제 데이터 흐름이 시작된다.

```java
Flux<Integer> pipeline = Flux.range(1, 5)
    .map(i -> i * 2)
    .filter(i -> i > 4);

// subscribe()를 호출하지 않으면 위 코드는 아무 것도 실행하지 않는다.

// 기본 구독
pipeline.subscribe();

// 값 소비자 지정
pipeline.subscribe(
    value -> System.out.println("값: " + value)
);

// 값, 에러, 완료 핸들러 지정
pipeline.subscribe(
    value -> System.out.println("값: " + value),
    error -> System.err.println("에러: " + error.getMessage()),
    () -> System.out.println("완료!")
);

```

> **주의**: Spring WebFlux에서는 프레임워크가 자동으로 구독을 처리한다. 컨트롤러에서 `Mono`나 `Flux`를 반환하면 WebFlux가 내부적으로 `subscribe()`를 호출하므로, 직접 `subscribe()`를 호출할 필요가 없다. 오히려 직접 호출하면 예기치 않은 동작이 발생할 수 있다.

---

## 3.2 Reactor의 주요 연산자

### 3.2.1 변환 연산자

#### map: 동기 변환

각 요소를 동기적으로 1:1 변환한다.

```java
Flux<String> upperCase = Flux.just("spring", "webflux", "reactor")
    .map(String::toUpperCase);
// 결과: "SPRING", "WEBFLUX", "REACTOR"
```

#### flatMap: 비동기 변환 (순서 보장 X)

각 요소를 `Publisher`로 변환하고 결과를 병합한다. **순서가 보장되지 않으며**, 동시에 여러 내부 Publisher를 구독한다.

```java
Flux<User> users = Flux.just(1L, 2L, 3L)
    .flatMap(id -> userRepository.findById(id));
// 결과 순서: id=2 응답이 먼저 올 수 있음
```

#### flatMapSequential: 비동기 변환 (순서 보장)

`flatMap`과 동일하게 동시 실행하되, **원래 순서를 보장**한다.

```java
Flux<User> users = Flux.just(1L, 2L, 3L)
    .flatMapSequential(id -> userRepository.findById(id));
// 결과 순서: id=1, id=2, id=3 순서 보장
```

#### concatMap: 순차 비동기 변환

각 요소를 순차적으로 처리한다. 이전 요소의 처리가 완료된 후 다음 요소를 처리하므로 **순서가 보장**되지만, `flatMapSequential`보다 느리다.

```java
Flux<User> users = Flux.just(1L, 2L, 3L)
    .concatMap(id -> userRepository.findById(id));
// id=1 조회 완료 -> id=2 조회 시작 -> id=2 완료 -> id=3 조회 시작
```

#### flatMap vs flatMapSequential vs concatMap 비교

| 연산자 | 동시 실행 | 순서 보장 | 사용 시기 |
|--------|----------|----------|----------|
| `flatMap` | O | X | 순서 무관, 최대 처리량 필요 |
| `flatMapSequential` | O | O | 동시 실행 + 순서 보장 |
| `concatMap` | X | O | 순차 처리 필수 |

### 3.2.2 필터링 연산자

```java
Flux<Integer> numbers = Flux.range(1, 20);

// filter: 조건에 맞는 요소만 통과
Flux<Integer> evenNumbers = numbers.filter(n -> n % 2 == 0);
// 결과: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20

// take: 처음 N개만 가져오기
Flux<Integer> firstThree = numbers.take(3);
// 결과: 1, 2, 3

// skip: 처음 N개 건너뛰기
Flux<Integer> skipped = numbers.skip(17);
// 결과: 18, 19, 20

// distinct: 중복 제거
Flux<String> unique = Flux.just("A", "B", "A", "C", "B")
    .distinct();
// 결과: "A", "B", "C"

// distinctUntilChanged: 연속 중복 제거
Flux<String> changed = Flux.just("A", "A", "B", "B", "A")
    .distinctUntilChanged();
// 결과: "A", "B", "A"
```

### 3.2.3 결합 연산자

#### zip: 각 Publisher의 요소를 쌍으로 결합

```java
Mono<String> name = Mono.just("홍길동");
Mono<Integer> age = Mono.just(30);

Mono<String> combined = Mono.zip(name, age)
    .map(tuple -> tuple.getT1() + "님은 " + tuple.getT2() + "세입니다.");
// 결과: "홍길동님은 30세입니다."

// Flux에서의 zip
Flux<String> names = Flux.just("Alice", "Bob", "Charlie");
Flux<Integer> scores = Flux.just(95, 87, 92);

Flux<String> results = Flux.zip(names, scores)
    .map(tuple -> tuple.getT1() + ": " + tuple.getT2() + "점");
// 결과: "Alice: 95점", "Bob: 87점", "Charlie: 92점"
```

#### merge: 여러 Publisher를 인터리빙 방식으로 병합

요소가 발행되는 즉시 하류로 전달한다. 순서는 도착 순이다.

```java
Flux<String> fast = Flux.interval(Duration.ofMillis(100))
    .map(i -> "FAST-" + i).take(3);
Flux<String> slow = Flux.interval(Duration.ofMillis(200))
    .map(i -> "SLOW-" + i).take(3);

Flux<String> merged = Flux.merge(fast, slow);
// 도착 순서대로 병합: FAST-0, FAST-1, SLOW-0, FAST-2, SLOW-1, SLOW-2
```

#### concat: 순서를 유지하며 병합

첫 번째 Publisher가 완료된 후 두 번째 Publisher를 구독한다.

```java
Flux<String> first = Flux.just("1", "2", "3");
Flux<String> second = Flux.just("A", "B", "C");

Flux<String> concatenated = Flux.concat(first, second);
// 결과: "1", "2", "3", "A", "B", "C" (항상 이 순서)
```

#### combineLatest: 각 Publisher의 최신 값 결합

어느 한 Publisher에서 새 값이 발행되면, 다른 Publisher의 최신 값과 결합한다.

```java
Flux<String> letters = Flux.just("A", "B", "C")
    .delayElements(Duration.ofMillis(100));
Flux<Integer> numbers = Flux.just(1, 2, 3)
    .delayElements(Duration.ofMillis(150));

Flux<String> combined = Flux.combineLatest(
    letters, numbers,
    (letter, number) -> letter + number
);
// 최신 값끼리 결합: A1, B1, B2, C2, C3 (타이밍에 따라 다를 수 있음)
```

### 3.2.4 집계 연산자

```java
Flux<Integer> numbers = Flux.just(3, 1, 4, 1, 5, 9, 2, 6);

// reduce: 모든 요소를 하나로 축약
Mono<Integer> sum = numbers.reduce(0, Integer::sum);
// 결과: 31

// count: 요소 개수
Mono<Long> count = numbers.count();
// 결과: 8

// collectList: 모든 요소를 List로 수집
Mono<List<Integer>> list = numbers.collectList();
// 결과: [3, 1, 4, 1, 5, 9, 2, 6]

// collectMap: 요소를 Map으로 수집
Flux<User> users = userRepository.findAll();
Mono<Map<String, User>> userMap = users
    .collectMap(User::getId, user -> user);

```

### 3.2.5 유용한 유틸리티 연산자

```java
// switchIfEmpty: 빈 결과일 때 대체 Publisher 사용
Mono<User> user = userRepository.findById(id)
    .switchIfEmpty(Mono.error(
        new NotFoundException("사용자를 찾을 수 없습니다: " + id)
    ));

// defaultIfEmpty: 빈 결과일 때 기본값 사용
Mono<String> config = configRepository.findByKey("timeout")
    .defaultIfEmpty("30");

// doOnNext, doOnError, doOnComplete: 부수 효과 (사이드 이펙트)
Flux<User> usersWithLog = userRepository.findAll()
    .doOnNext(u -> log.info("조회된 사용자: {}", u.getName()))
    .doOnError(e -> log.error("조회 실패", e))
    .doOnComplete(() -> log.info("전체 사용자 조회 완료"));

// timeout: 지정 시간 내에 값이 없으면 에러
Mono<User> userWithTimeout = userRepository.findById(id)
    .timeout(Duration.ofSeconds(5));
```

---

## 3.3 에러 처리 전략

리액티브 스트림에서 에러가 발생하면 스트림이 종료된다. Reactor는 다양한 에러 처리 연산자를 제공하여 우아한 에러 복구를 가능하게 한다.

### 3.3.1 onErrorReturn: 기본값으로 대체

에러 발생 시 지정한 기본값을 반환하고 스트림을 정상 완료한다.

```java
Mono<String> result = externalApi.getData()
    .onErrorReturn("기본값");

// 특정 예외 타입에만 적용
Mono<String> result2 = externalApi.getData()
    .onErrorReturn(TimeoutException.class, "시간 초과 - 기본값 사용");
```

### 3.3.2 onErrorResume: 대체 Publisher로 전환

에러 발생 시 다른 Publisher로 전환한다. 폴백(fallback) 로직을 구현할 때 유용하다.

```java
Mono<User> user = primaryDb.findById(id)
    .onErrorResume(e -> {
        log.warn("Primary DB 실패, Secondary DB로 전환", e);
        return secondaryDb.findById(id);
    });

// 에러 타입별 분기 처리
Mono<String> data = externalService.call()
    .onErrorResume(TimeoutException.class, e -> cachedService.getCached())
    .onErrorResume(ServiceUnavailableException.class, e -> Mono.just("서비스 점검 중"));
```

### 3.3.3 onErrorMap: 에러를 다른 에러로 변환

예외를 도메인에 맞는 다른 예외로 변환한다.

```java
Mono<User> user = userRepository.findById(id)
    .switchIfEmpty(Mono.error(new UserNotFoundException(id)))
    .onErrorMap(DataAccessException.class, e ->
        new ServiceException("데이터 접근 오류", e)
    );
```

### 3.3.4 doOnError: 에러 발생 시 부수 효과

스트림 자체를 변경하지 않고 로깅 등의 부수 효과를 실행한다.

```java
Mono<User> user = userRepository.findById(id)
    .doOnError(e -> {
        log.error("사용자 조회 중 에러 발생. id={}", id, e);
        metrics.incrementErrorCount("user.findById");
    })
    .onErrorResume(e -> Mono.empty());
```

### 3.3.5 retry: 단순 재시도

에러 발생 시 지정한 횟수만큼 재구독한다.

```java
Mono<String> result = externalApi.call()
    .retry(3); // 최대 3회 재시도
```

### 3.3.6 retryWhen: 고급 재시도 전략

`Retry` 스펙을 사용하여 세밀한 재시도 정책을 구현한다.

```java
import reactor.util.retry.Retry;

Mono<String> result = externalApi.call()
    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1))
        .maxBackoff(Duration.ofSeconds(10))
        .jitter(0.5)
        .filter(throwable -> throwable instanceof ServiceUnavailableException)
        .onRetryExhaustedThrow((retryBackoffSpec, retrySignal) ->
            new ServiceException(
                "재시도 횟수 초과. 마지막 에러: " + retrySignal.failure().getMessage(),
                retrySignal.failure()
            )
        )
    );
```

### 3.3.7 실전 에러 처리 패턴

다음은 실제 서비스 계층에서 사용하는 종합 에러 처리 패턴이다.

```java
@Service
@RequiredArgsConstructor
public class UserService {

    private final ReactiveMongoTemplate mongoTemplate;
    private final UserCacheService cacheService;
    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    public Mono<User> findUserById(String id) {
        return cacheService.getCachedUser(id)            // 1. 캐시 조회
            .switchIfEmpty(
                mongoTemplate.findById(id, User.class)   // 2. DB 조회
                    .doOnNext(user ->
                        cacheService.cacheUser(user)      // 3. 캐시 저장
                            .subscribe()
                    )
            )
            .switchIfEmpty(
                Mono.error(new UserNotFoundException(id)) // 4. 없으면 예외
            )
            .timeout(Duration.ofSeconds(5))               // 5. 타임아웃
            .doOnError(TimeoutException.class, e ->
                log.warn("사용자 조회 타임아웃. id={}", id)
            )
            .onErrorMap(TimeoutException.class, e ->
                new ServiceException("사용자 조회 시간 초과", e)
            )
            .retryWhen(Retry.backoff(2, Duration.ofMillis(500))
                .filter(e -> e instanceof DataAccessException)
            );
    }

    public Flux<User> searchUsers(String keyword) {
        Query query = new Query(
            Criteria.where("name").regex(keyword, "i")
        );

        return mongoTemplate.find(query, User.class)
            .onErrorResume(e -> {
                log.error("사용자 검색 실패. keyword={}", keyword, e);
                return Flux.empty();
            });
    }
}
```

---

## 3.4 스케줄러(Scheduler)와 스레드 모델

Reactor는 기본적으로 **호출자 스레드**에서 동작한다. 스케줄러를 사용하면 작업을 실행할 스레드를 제어할 수 있다.

### 3.4.1 주요 스케줄러 종류

| 스케줄러 | 설명 | 스레드 수 | 사용 시기 |
|---------|------|----------|----------|
| `Schedulers.parallel()` | CPU 집약적 작업 | CPU 코어 수 | 계산, 변환 작업 |
| `Schedulers.boundedElastic()` | 블로킹 I/O 래핑 | 최대 10 * CPU 코어 | 블로킹 코드 감싸기 |
| `Schedulers.single()` | 단일 재사용 스레드 | 1 | 순차 실행 보장 |
| `Schedulers.immediate()` | 현재 스레드 | - | 테스트, 디폴트 |
| `Schedulers.fromExecutorService()` | 커스텀 스레드 풀 | 사용자 지정 | 특수한 요구사항 |

### 3.4.2 publishOn vs subscribeOn

두 연산자는 이름이 비슷하지만 동작 방식이 완전히 다르다.

#### publishOn: 하류 연산자의 실행 스레드를 변경

`publishOn` 이후의 연산자들이 지정한 스케줄러에서 실행된다. 파이프라인 중간에 스레드를 전환할 때 사용한다.

```java
Flux.range(1, 5)
    .map(i -> {
        log.info("[map1] {} - {}", i, Thread.currentThread().getName());
        return i * 10;
    })
    .publishOn(Schedulers.parallel())   // 여기서부터 parallel 스레드
    .map(i -> {
        log.info("[map2] {} - {}", i, Thread.currentThread().getName());
        return i + 1;
    })
    .subscribe(i ->
        log.info("[subscribe] {} - {}", i, Thread.currentThread().getName())
    );

// map1은 main 스레드, publishOn 이후 map2와 subscribe는 parallel-1 스레드에서 실행
```

#### subscribeOn: 전체 구독 체인의 실행 스레드를 변경

소스의 구독(데이터 발행) 시점부터의 스레드를 변경한다. **위치에 관계없이** 소스 발행 스레드에 영향을 미친다.

```java
Mono.fromCallable(() -> {
        log.info("[callable] {}", Thread.currentThread().getName());
        return blockingIoOperation();
    })
    .subscribeOn(Schedulers.boundedElastic())  // 소스가 boundedElastic에서 실행
    .map(result -> processResult(result))
    .subscribe();
// callable, map, subscribe 모두 boundedElastic-1 스레드에서 실행
```

#### publishOn과 subscribeOn 함께 사용

```java
Flux.range(1, 3)
    .subscribeOn(Schedulers.single())          // 소스: single 스레드
    .map(i -> {
        log.info("[map1] {}", Thread.currentThread().getName()); // single-1
        return "값-" + i;
    })
    .publishOn(Schedulers.parallel())          // 이후: parallel 스레드
    .map(s -> {
        log.info("[map2] {}", Thread.currentThread().getName()); // parallel-1
        return s.toUpperCase();
    })
    .subscribe();
```

### 3.4.3 블로킹 코드를 감싸는 방법

리액티브 파이프라인 안에서 블로킹 코드를 직접 호출하면 이벤트 루프 스레드를 점유하여 전체 시스템 처리량이 급격히 떨어진다. 불가피하게 블로킹 코드를 사용해야 할 때는 반드시 `boundedElastic` 스케줄러로 격리해야 한다.

```java
@Service
public class LegacyIntegrationService {

    private final LegacyBlockingClient legacyClient;

    // 잘못된 방법 - 이벤트 루프 스레드를 블로킹
    public Mono<String> wrongWay() {
        return Mono.just(legacyClient.blockingCall()); // 절대 이렇게 하지 말 것!
    }

    // 올바른 방법 - boundedElastic에서 블로킹 실행
    public Mono<String> correctWay() {
        return Mono.fromCallable(() -> legacyClient.blockingCall())
            .subscribeOn(Schedulers.boundedElastic());
    }

    // 여러 블로킹 호출을 병렬로 실행
    public Mono<AggregatedResult> parallelBlockingCalls() {
        Mono<String> call1 = Mono.fromCallable(() -> legacyClient.callServiceA())
            .subscribeOn(Schedulers.boundedElastic());

        Mono<String> call2 = Mono.fromCallable(() -> legacyClient.callServiceB())
            .subscribeOn(Schedulers.boundedElastic());

        return Mono.zip(call1, call2)
            .map(tuple -> new AggregatedResult(tuple.getT1(), tuple.getT2()));
    }
}
```

> **Tip**: 프로젝트에 `BlockHound` 라이브러리를 추가하면 이벤트 루프 스레드에서 블로킹 호출이 발생할 때 즉시 탐지할 수 있다. 19장에서 자세히 다룬다.

---

## 3.5 Cold vs Hot Publisher

### 3.5.1 Cold Publisher

Cold Publisher는 **구독할 때마다 데이터를 처음부터 새로 발행**한다. 대부분의 Reactor 연산자는 Cold Publisher를 생성한다.

```java
Flux<Long> coldFlux = Flux.defer(() -> {
    log.info("새로운 데이터 소스 생성");
    return Flux.just(System.currentTimeMillis());
});

// 구독자 1: 자신만의 데이터를 받음
coldFlux.subscribe(v -> log.info("구독자1: {}", v));

Thread.sleep(100);

// 구독자 2: 별도의 새로운 데이터를 받음 (다른 타임스탬프)
coldFlux.subscribe(v -> log.info("구독자2: {}", v));

// 각 구독자가 서로 다른 타임스탬프를 받음 (매번 새로 생성)
```

### 3.5.2 Hot Publisher

Hot Publisher는 **구독 여부와 관계없이 데이터를 발행**하며, 구독자들은 구독 이후의 데이터만 받는다.

```java
// ConnectableFlux로 Hot Publisher 만들기
Flux<Long> hotFlux = Flux.interval(Duration.ofSeconds(1))
    .publish()
    .autoConnect(2); // 2명이 구독하면 자동 시작

// 구독자 1
hotFlux.subscribe(v -> log.info("구독자1: {}", v));

Thread.sleep(1500);

// 구독자 2가 연결되면 발행 시작, 구독자2는 중간부터 수신
hotFlux.subscribe(v -> log.info("구독자2: {}", v));
```

### 3.5.3 Sinks를 활용한 Hot Publisher 생성

`Sinks`는 Reactor 3.4부터 도입된 프로그래밍 방식의 신호 발행 도구이다. 기존의 `Processor` 를 대체하며 스레드 안전성을 보장한다.

```java
// Sinks.Many: 여러 값을 여러 구독자에게 발행
Sinks.Many<String> sink = Sinks.many().multicast().onBackpressureBuffer();

Flux<String> hotFlux = sink.asFlux();

// 구독자 등록
hotFlux.subscribe(v -> log.info("구독자1: {}", v));
hotFlux.subscribe(v -> log.info("구독자2: {}", v));

// 값 발행
sink.tryEmitNext("메시지 1");
sink.tryEmitNext("메시지 2");
sink.tryEmitComplete();

// 두 구독자 모두 "메시지 1", "메시지 2"를 수신
```

```java
// Sinks.Many의 다양한 스펙
Sinks.Many<String> unicast   = Sinks.many().unicast().onBackpressureBuffer();   // 구독자 1명
Sinks.Many<String> multicast = Sinks.many().multicast().onBackpressureBuffer(); // 여러 구독자
Sinks.Many<String> replay    = Sinks.many().replay().limit(5); // 최근 5개 재생
```

**실전 예제 - 이벤트 버스 구현**:

```java
@Component
public class EventBus {

    private final Sinks.Many<DomainEvent> sink =
        Sinks.many().multicast().onBackpressureBuffer();

    public void publish(DomainEvent event) {
        sink.tryEmitNext(event);
    }

    public Flux<DomainEvent> subscribe() {
        return sink.asFlux();
    }

    public <T extends DomainEvent> Flux<T> subscribe(Class<T> eventType) {
        return sink.asFlux()
            .filter(eventType::isInstance)
            .cast(eventType);
    }
}
```

### 3.5.4 share()와 cache()

#### share(): Cold Publisher를 Hot Publisher로 변환

```java
Flux<Long> shared = Flux.interval(Duration.ofSeconds(1))
    .doOnSubscribe(s -> log.info("구독 시작"))
    .share(); // 첫 구독자가 구독할 때 시작, 모든 구독자가 해제되면 중지

shared.subscribe(v -> log.info("구독자1: {}", v));

Thread.sleep(2500);

// 구독자2는 중간부터 받음
shared.subscribe(v -> log.info("구독자2: {}", v));
```

#### cache(): 결과를 캐싱

```java
// 한 번 실행된 결과를 캐싱하여 이후 구독자에게 재사용
Mono<Config> config = loadConfigFromDb()
    .cache(Duration.ofMinutes(10)); // 10분간 캐시

// 첫 번째 호출: DB 조회 실행
config.subscribe(c -> log.info("설정1: {}", c));

// 두 번째 호출: 캐시된 값 반환 (DB 조회 없음)
config.subscribe(c -> log.info("설정2: {}", c));

// Flux에서도 사용 가능
Flux<Product> products = productRepository.findAll()
    .cache(Duration.ofMinutes(5)); // 전체 시퀀스를 캐시
```

---

## 3.6 Reactor 디버깅 기법

리액티브 코드의 디버깅은 명령형 코드보다 까다롭다. 비동기 스택 트레이스가 연산자 체인의 원래 위치를 보여주지 않기 때문이다. Reactor는 이를 돕는 도구를 제공한다.

### 3.6.1 log(): 리액티브 신호 로깅

`log()` 연산자는 구독, 요청, 발행, 완료, 에러 등 모든 리액티브 신호를 로깅한다.

```java
Flux.range(1, 5)
    .log("NumberFlux")    // 카테고리 이름 지정 가능
    .map(i -> i * 2)
    .log("DoubledFlux")
    .subscribe();

// 출력: onSubscribe, request, onNext, onComplete 등 모든 신호 로깅

// 특정 신호만 로깅
Flux.range(1, 5)
    .log("MyFlux", Level.INFO, SignalType.ON_NEXT, SignalType.ON_ERROR)
    .subscribe();
```

### 3.6.2 checkpoint(): 에러 추적 지점 설정

`checkpoint()`는 에러 발생 시 연산자 체인의 어느 지점에서 문제가 발생했는지 추적할 수 있게 한다.

```java
Flux<Integer> flux = Flux.just(1, 2, 0, 4)
    .map(i -> 100 / i)
    .checkpoint("나눗셈 연산 후")        // 이 지점에 체크포인트 설정
    .map(i -> i + 10)
    .checkpoint("덧셈 연산 후");

flux.subscribe(
    v -> log.info("값: {}", v),
    e -> log.error("에러 발생", e)
);

// 에러 메시지에 체크포인트 정보 포함:
// Assembly trace from producer [reactor.core.publisher.FluxMap],
// described as [나눗셈 연산 후]
```

```java
// 상세 스택 트레이스 포함 (비용이 더 들지만 디버깅에 유용)
.checkpoint("상세 체크포인트", true)
```

### 3.6.3 Hooks.onOperatorDebug(): 글로벌 디버그 모드

모든 연산자에 대해 어셈블리(조립) 시점의 스택 트레이스를 자동 캡처한다. **성능 오버헤드가 크므로 개발 환경에서만 사용**해야 한다.

```java
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        // 개발 환경에서만 활성화
        if (isDevProfile()) {
            Hooks.onOperatorDebug();
        }
        SpringApplication.run(Application.class, args);
    }
}
```

활성화하면 에러 발생 시 연산자가 조립된 소스 코드 위치(클래스명, 줄 번호)를 스택 트레이스에 포함시켜 준다.

### 3.6.4 ReactorDebugAgent: 프로덕션 친화적 디버깅

`Hooks.onOperatorDebug()`의 성능 문제를 해결한 대안이다. Java Agent 방식으로 바이트코드를 변환하여, 런타임 오버헤드 없이 디버그 정보를 제공한다.

**의존성 추가**:

```xml
<dependency>
    <groupId>io.projectreactor</groupId>
    <artifactId>reactor-tools</artifactId>
</dependency>
```

**활성화**:

```java
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        ReactorDebugAgent.init();               // JVM 시작 시 한 번 호출
        ReactorDebugAgent.processExistingClasses(); // 이미 로드된 클래스 처리
        SpringApplication.run(Application.class, args);
    }
}
```

### 3.6.5 디버깅 실전 전략 정리

| 방법 | 성능 영향 | 사용 환경 | 설명 |
|------|----------|----------|------|
| `log()` | 낮음 | 모든 환경 | 특정 지점의 신호 확인 |
| `checkpoint()` | 낮음 | 모든 환경 | 특정 지점에 디버그 마커 설정 |
| `Hooks.onOperatorDebug()` | **높음** | 개발 환경만 | 모든 연산자의 스택 트레이스 캡처 |
| `ReactorDebugAgent` | 낮음 | 모든 환경 | 바이트코드 변환 기반 디버깅 |

**권장 디버깅 워크플로우**:

```java
// 1단계: log()로 신호 흐름 확인
userRepository.findById(id)
    .log("findById")
    .flatMap(user -> orderRepository.findByUserId(user.getId()))
    .log("findOrders")
    .subscribe();

// 2단계: 문제 지점에 checkpoint() 추가
userRepository.findById(id)
    .checkpoint("사용자 조회")
    .flatMap(user -> orderRepository.findByUserId(user.getId()))
    .checkpoint("주문 목록 조회")
    .subscribe();

// 3단계: 그래도 찾기 어려우면 ReactorDebugAgent 활성화
```

---

## 요약

이 장에서 다룬 Project Reactor의 핵심 개념을 정리하면 다음과 같다.

- **Mono와 Flux**는 리액티브 스트림의 기본 구성 요소다. Mono는 0..1개, Flux는 0..N개의 요소를 비동기적으로 발행한다.
- **연산자**를 조합하여 선언적으로 데이터 처리 파이프라인을 구성한다. `flatMap`과 `concatMap`의 차이처럼, 각 연산자의 동작 특성을 이해하는 것이 중요하다.
- **에러 처리**는 `onErrorReturn`, `onErrorResume`, `retry` 등을 활용하여 우아하게 복구할 수 있다. 특히 `retryWhen`과 `Retry.backoff()`를 조합하면 실전에서 필요한 재시도 전략을 구현할 수 있다.
- **스케줄러**를 통해 작업의 실행 스레드를 제어한다. `publishOn`은 하류의 스레드를 전환하고, `subscribeOn`은 소스의 스레드를 전환한다. 블로킹 코드는 반드시 `boundedElastic`으로 격리해야 한다.
- **Cold vs Hot Publisher** 개념을 이해하면 데이터 공유와 멀티캐스트 시나리오를 올바르게 구현할 수 있다. `Sinks`는 프로그래밍 방식으로 Hot Publisher를 생성하는 현대적 도구이다.
- **디버깅**은 `log()`, `checkpoint()`로 시작하고, 필요 시 `ReactorDebugAgent`를 활용한다.

다음 장에서는 MongoDB의 기본 개념과 리액티브 드라이버에 대해 알아본다.


---

# Chapter 4. MongoDB 소개

앞선 장에서 리액티브 프로그래밍의 개념과 Project Reactor의 핵심을 다뤘다. 이번 장에서는 리액티브 스택과 궁합이 뛰어난 데이터베이스인 MongoDB를 살펴본다. MongoDB가 왜 리액티브 애플리케이션에 적합한지, 도큐먼트 모델의 특성은 무엇인지, 그리고 실제 설치부터 CRUD 조작까지 실습한다.

---

## 4.1 NoSQL과 MongoDB의 특징

### 4.1.1 RDBMS vs NoSQL 비교

전통적인 관계형 데이터베이스(RDBMS)는 정규화된 테이블, SQL 쿼리, ACID 트랜잭션을 기반으로 한다. 반면 NoSQL은 특정 사용 사례에 최적화된 다양한 데이터 모델을 제공한다.

| 구분 | RDBMS | NoSQL (MongoDB) |
|------|-------|-----------------|
| 데이터 모델 | 테이블, 행, 열 | 도큐먼트 (JSON/BSON) |
| 스키마 | 고정 스키마 (DDL 필수) | 유연한 스키마 (스키마리스) |
| 확장 방식 | 주로 수직 확장 (Scale-up) | 수평 확장 (Scale-out, 샤딩) |
| 트랜잭션 | 강력한 ACID 지원 | 단일 도큐먼트 ACID, 멀티 도큐먼트 트랜잭션 지원 |
| 조인 | JOIN 연산 기본 지원 | 일반적으로 비정규화, `$lookup`으로 제한적 지원 |
| 쿼리 언어 | SQL | MQL (MongoDB Query Language) |
| 적합한 사용 사례 | 복잡한 관계, 정합성 중시 | 빠른 반복 개발, 대규모 읽기/쓰기, 유연한 구조 |

### 4.1.2 MongoDB 핵심 특징

**스키마 유연성**

MongoDB는 같은 컬렉션 안에 서로 다른 구조의 도큐먼트를 저장할 수 있다. 애플리케이션 요구사항이 빠르게 변화하는 환경에서 스키마 마이그레이션 부담을 크게 줄여준다.

```javascript
// 같은 컬렉션에 서로 다른 구조의 도큐먼트가 공존 가능
{ name: "Alice", email: "alice@example.com" }
{ name: "Bob", email: "bob@example.com", phone: "010-1234-5678", address: { city: "Seoul" } }
```

**수평 확장 (Sharding)**

데이터가 증가하면 샤드를 추가하여 여러 서버에 데이터를 분산 저장한다. 애플리케이션 코드 변경 없이 처리 용량을 늘릴 수 있다.

**높은 가용성 (Replica Set)**

복제 세트(Replica Set)를 통해 데이터의 복제본을 여러 노드에 유지한다. 프라이머리 노드가 장애를 겪으면 자동으로 세컨더리 노드가 프라이머리로 승격된다.

### 4.1.3 CAP 정리에서의 MongoDB 위치

분산 시스템에서는 일관성(Consistency), 가용성(Availability), 분단 내성(Partition Tolerance) 세 가지를 동시에 모두 만족할 수 없다는 것이 CAP 정리다.

- **C (Consistency)**: 모든 노드가 같은 시점에 같은 데이터를 반환한다.
- **A (Availability)**: 모든 요청에 대해 응답을 반환한다.
- **P (Partition Tolerance)**: 네트워크 분단이 발생해도 시스템이 동작한다.

MongoDB는 기본적으로 **CP 시스템**으로 분류된다. 프라이머리 노드에 쓰기를 집중하여 일관성을 보장하고, 네트워크 분단 시 가용성보다 일관성을 우선한다. 단, `readPreference`와 `writeConcern` 설정을 조정하면 가용성과 일관성 사이의 균형을 유연하게 조절할 수 있다.

```javascript
// writeConcern 설정 예시
db.orders.insertOne(
  { item: "laptop", qty: 1 },
  { writeConcern: { w: "majority", wtimeout: 5000 } }
)
```

- `w: "majority"` — 과반수 노드에 쓰기가 확인되어야 성공으로 간주
- `w: 1` — 프라이머리에만 쓰기 확인 (기본값, 더 빠르지만 덜 안전)

---

## 4.2 도큐먼트 모델과 컬렉션

### 4.2.1 BSON 형식과 도큐먼트 구조

MongoDB는 내부적으로 **BSON**(Binary JSON) 형식으로 데이터를 저장한다. BSON은 JSON의 확장으로, JSON이 지원하지 않는 추가 데이터 타입을 포함한다.

| BSON 타입 | 설명 | 예시 |
|-----------|------|------|
| String | UTF-8 문자열 | `"Hello"` |
| Int32 / Int64 | 정수형 | `42`, `NumberLong(123456789)` |
| Double | 부동소수점 | `3.14` |
| Boolean | 논리값 | `true`, `false` |
| Date | 날짜/시간 | `ISODate("2025-01-01T00:00:00Z")` |
| ObjectId | 12바이트 고유 식별자 | `ObjectId("507f1f77bcf86cd799439011")` |
| Array | 배열 | `[1, 2, 3]` |
| Object | 내장 도큐먼트 | `{ city: "Seoul" }` |
| Decimal128 | 고정밀 소수점 | `NumberDecimal("19.99")` |
| Binary | 바이너리 데이터 | — |

도큐먼트의 기본 구조는 다음과 같다.

```javascript
{
  _id: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),  // 자동 생성되는 고유 식별자
  title: "Spring WebFlux 입문",
  author: {                                     // 내장 도큐먼트
    name: "홍길동",
    email: "hong@example.com"
  },
  tags: ["spring", "webflux", "reactive"],      // 배열
  price: NumberDecimal("35000"),
  publishedAt: ISODate("2025-03-15T09:00:00Z"),
  inStock: true
}
```

`_id` 필드는 컬렉션 내에서 도큐먼트를 고유하게 식별하는 기본 키다. 명시적으로 지정하지 않으면 MongoDB가 `ObjectId`를 자동으로 생성한다.

### 4.2.2 컬렉션 개념

컬렉션(Collection)은 RDBMS의 테이블에 대응하는 개념이다. 그러나 테이블과 달리 컬렉션에 저장되는 도큐먼트들이 반드시 같은 스키마를 가질 필요는 없다.

```javascript
// 컬렉션 생성 (명시적)
db.createCollection("books")

// 또는 첫 번째 도큐먼트 삽입 시 자동 생성
db.books.insertOne({ title: "MongoDB in Action" })
```

필요한 경우 **Schema Validation**을 적용하여 도큐먼트 구조를 강제할 수 있다.

```javascript
db.createCollection("books", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "author", "price"],
      properties: {
        title:  { bsonType: "string", description: "제목은 필수 문자열" },
        author: { bsonType: "string", description: "저자는 필수 문자열" },
        price:  { bsonType: "number", minimum: 0, description: "가격은 0 이상" }
      }
    }
  }
})
```

### 4.2.3 내장 도큐먼트(Embedded) vs 참조(Reference)

MongoDB 스키마 설계에서 가장 중요한 결정 중 하나는 **데이터를 내장할 것인가, 참조할 것인가**이다.

**내장 도큐먼트 방식**

관련 데이터를 하나의 도큐먼트 안에 중첩하여 저장한다.

```javascript
// 주문 도큐먼트에 배송 주소를 내장
{
  _id: ObjectId("..."),
  orderNumber: "ORD-2025-001",
  customer: "김철수",
  items: [
    { productName: "키보드", quantity: 1, price: 89000 },
    { productName: "마우스", quantity: 2, price: 45000 }
  ],
  shippingAddress: {
    zipCode: "06234",
    city: "서울",
    detail: "강남구 테헤란로 123"
  }
}
```

**참조 방식**

별도의 컬렉션에 데이터를 저장하고 `_id`로 연결한다.

```javascript
// users 컬렉션
{ _id: ObjectId("user001"), name: "김철수", email: "kim@example.com" }

// orders 컬렉션 - userId로 참조
{
  _id: ObjectId("order001"),
  userId: ObjectId("user001"),   // 참조
  orderNumber: "ORD-2025-001",
  items: [...]
}
```

**선택 기준**

| 기준 | 내장 (Embedded) | 참조 (Reference) |
|------|----------------|-----------------|
| 관계 유형 | 1:1, 1:N (소량) | 1:N (대량), N:M |
| 읽기 패턴 | 함께 조회하는 경우 | 독립적으로 조회하는 경우 |
| 데이터 크기 | 내장 데이터가 작을 때 | 내장 시 도큐먼트가 16MB 제한에 근접할 때 |
| 갱신 빈도 | 드물게 변경 | 자주 독립적으로 변경 |

### 4.2.4 스키마 설계 패턴

MongoDB에서 자주 사용되는 설계 패턴 몇 가지를 소개한다.

**버킷 패턴 (Bucket Pattern)**: 시계열 데이터처럼 연속적인 데이터를 일정 단위(시간, 개수)로 묶어 하나의 도큐먼트에 저장한다.

```javascript
{
  sensorId: "sensor-001",
  date: ISODate("2025-01-15"),
  readings: [
    { time: ISODate("2025-01-15T00:00:00Z"), value: 23.5 },
    { time: ISODate("2025-01-15T00:05:00Z"), value: 23.7 },
    // ... 하루치 데이터를 하나의 도큐먼트에 저장
  ],
  count: 288,
  avg: 24.1
}
```

**다형성 패턴 (Polymorphic Pattern)**: 유사하지만 구조가 약간 다른 데이터를 같은 컬렉션에 저장한다. `type` 필드로 구분한다.

```javascript
// products 컬렉션
{ type: "book", title: "MongoDB 가이드", author: "홍길동", pages: 500 }
{ type: "electronics", title: "무선 마우스", brand: "Logitech", weight: 85 }
```

---

## 4.3 MongoDB 설치 및 기본 CRUD

### 4.3.1 Docker를 통한 설치

개발 환경에서는 Docker를 사용하면 가장 간편하게 MongoDB를 실행할 수 있다.

```bash
# MongoDB 최신 버전 실행
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret1234 \
  -v mongodb_data:/data/db \
  mongo:7

# 컨테이너 상태 확인
docker ps

# 로그 확인
docker logs mongodb
```

`docker-compose.yml`로 관리하면 더 편리하다.

```yaml
version: "3.8"

services:
  mongodb:
    image: mongo:7
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: secret1234
      MONGO_INITDB_DATABASE: webflux_demo
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

```bash
# 실행
docker compose up -d

# 종료
docker compose down
```

### 4.3.2 mongosh 사용법

`mongosh`는 MongoDB의 공식 셸 클라이언트다. Docker 컨테이너 안에서 바로 실행할 수 있다.

```bash
# mongosh 접속
docker exec -it mongodb mongosh -u admin -p secret1234

# 데이터베이스 목록 조회
show dbs

# 데이터베이스 선택 (없으면 첫 도큐먼트 삽입 시 자동 생성)
use webflux_demo

# 컬렉션 목록 조회
show collections

# 현재 데이터베이스 확인
db.getName()
```

### 4.3.3 insertOne / insertMany

```javascript
// 단일 도큐먼트 삽입
db.books.insertOne({
  title: "Spring WebFlux 완벽 가이드",
  author: "홍길동",
  price: 35000,
  tags: ["spring", "webflux", "reactive"],
  publishedAt: new Date("2025-03-15")
})

// 다수 도큐먼트 삽입
db.books.insertMany([
  {
    title: "MongoDB 실전 활용",
    author: "김영희",
    price: 32000,
    tags: ["mongodb", "nosql"],
    publishedAt: new Date("2025-01-10")
  },
  {
    title: "리액티브 프로그래밍 입문",
    author: "이철수",
    price: 28000,
    tags: ["reactive", "java"],
    publishedAt: new Date("2024-11-20")
  },
  {
    title: "Kotlin과 WebFlux",
    author: "박민수",
    price: 38000,
    tags: ["kotlin", "webflux", "spring"],
    publishedAt: new Date("2025-06-01")
  }
])
```

### 4.3.4 find / findOne

```javascript
// 전체 조회
db.books.find()

// 보기 좋게 출력
db.books.find().pretty()

// 조건 조회: 가격이 30000 이상인 책
db.books.find({ price: { $gte: 30000 } })

// 특정 필드만 조회 (프로젝션)
db.books.find(
  { price: { $gte: 30000 } },
  { title: 1, price: 1, _id: 0 }
)
// 결과:
// { title: "Spring WebFlux 완벽 가이드", price: 35000 }
// { title: "MongoDB 실전 활용", price: 32000 }
// { title: "Kotlin과 WebFlux", price: 38000 }

// 단일 도큐먼트 조회
db.books.findOne({ author: "홍길동" })

// 배열 필드 조건: tags에 "webflux"가 포함된 책
db.books.find({ tags: "webflux" })

// 논리 연산자 조합
db.books.find({
  $or: [
    { price: { $lt: 30000 } },
    { author: "홍길동" }
  ]
})

// 정렬, 스킵, 제한
db.books.find().sort({ price: -1 }).skip(0).limit(2)
```

### 4.3.5 update

```javascript
// 단일 도큐먼트 수정
db.books.updateOne(
  { title: "MongoDB 실전 활용" },
  { $set: { price: 34000, updatedAt: new Date() } }
)

// 다수 도큐먼트 수정: 모든 책의 가격을 10% 인상
db.books.updateMany(
  {},
  { $mul: { price: 1.1 } }
)

// 배열에 요소 추가
db.books.updateOne(
  { title: "Spring WebFlux 완벽 가이드" },
  { $push: { tags: "java" } }
)

// 필드 제거
db.books.updateOne(
  { title: "Spring WebFlux 완벽 가이드" },
  { $unset: { updatedAt: "" } }
)

// upsert: 있으면 수정, 없으면 삽입
db.books.updateOne(
  { title: "새로운 책" },
  { $set: { author: "신규 저자", price: 25000 } },
  { upsert: true }
)
```

주요 업데이트 연산자 정리:

| 연산자 | 설명 | 예시 |
|--------|------|------|
| `$set` | 필드 값 설정 | `{ $set: { price: 30000 } }` |
| `$unset` | 필드 제거 | `{ $unset: { field: "" } }` |
| `$inc` | 숫자 증감 | `{ $inc: { stock: -1 } }` |
| `$mul` | 숫자 곱셈 | `{ $mul: { price: 1.1 } }` |
| `$push` | 배열에 요소 추가 | `{ $push: { tags: "new" } }` |
| `$pull` | 배열에서 요소 제거 | `{ $pull: { tags: "old" } }` |
| `$addToSet` | 배열에 중복 없이 추가 | `{ $addToSet: { tags: "new" } }` |

### 4.3.6 delete

```javascript
// 단일 도큐먼트 삭제
db.books.deleteOne({ title: "새로운 책" })

// 조건에 맞는 다수 도큐먼트 삭제
db.books.deleteMany({ price: { $lt: 30000 } })

// 컬렉션의 모든 도큐먼트 삭제
db.books.deleteMany({})

// 컬렉션 자체 삭제
db.books.drop()
```

### 4.3.7 MongoDB Compass

MongoDB Compass는 공식 GUI 클라이언트로, 다음과 같은 기능을 제공한다.

- **연결**: `mongodb://admin:secret1234@localhost:27017` 형식의 URI로 접속
- **도큐먼트 탐색**: 시각적으로 데이터를 조회, 편집, 삭제
- **쿼리 작성**: 필터, 프로젝션, 정렬을 GUI에서 구성
- **Aggregation Pipeline 빌더**: 파이프라인 스테이지를 시각적으로 조합
- **인덱스 관리**: 인덱스 생성, 삭제, 성능 분석
- **스키마 분석**: 컬렉션 내 도큐먼트 구조를 시각적으로 파악

> **Tip**: 개발 단계에서 복잡한 쿼리를 작성할 때 Compass의 Aggregation Pipeline 빌더로 먼저 검증한 뒤, 코드로 옮기는 방법을 추천한다.

---

## 4.4 인덱싱과 쿼리 최적화 기초

### 4.4.1 인덱스 종류

인덱스가 없으면 MongoDB는 컬렉션 전체를 스캔(COLLSCAN)해야 한다. 적절한 인덱스를 생성하면 쿼리 성능을 크게 향상시킬 수 있다.

**단일 필드 인덱스**

```javascript
// author 필드에 오름차순 인덱스 생성
db.books.createIndex({ author: 1 })

// price 필드에 내림차순 인덱스 생성
db.books.createIndex({ price: -1 })
```

**복합 인덱스 (Compound Index)**

여러 필드를 조합한 인덱스다. 필드 순서가 중요하다. **ESR 규칙**(Equality, Sort, Range)에 따라 동등 조건 필드를 앞에, 정렬 필드를 중간에, 범위 조건 필드를 뒤에 배치하면 효율적이다.

```javascript
// author(동등) + publishedAt(정렬/범위)에 복합 인덱스
db.books.createIndex({ author: 1, publishedAt: -1 })

// 활용 쿼리: 특정 저자의 책을 최신순으로 조회
db.books.find({ author: "홍길동" }).sort({ publishedAt: -1 })
```

**멀티키 인덱스 (Multikey Index)**

배열 필드에 인덱스를 생성하면 자동으로 멀티키 인덱스가 된다. 배열의 각 요소에 대해 인덱스 항목이 생성된다.

```javascript
// tags 배열 필드에 인덱스
db.books.createIndex({ tags: 1 })

// 활용: tags에 "webflux"가 포함된 도큐먼트 조회
db.books.find({ tags: "webflux" })
```

**텍스트 인덱스 (Text Index)**

전문 검색(Full-Text Search)을 위한 인덱스다.

```javascript
// title과 author에 텍스트 인덱스 생성
db.books.createIndex({ title: "text", author: "text" })

// 텍스트 검색
db.books.find({ $text: { $search: "WebFlux 가이드" } })

// 관련도 점수와 함께 조회
db.books.find(
  { $text: { $search: "WebFlux 가이드" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } })
```

**고유 인덱스 (Unique Index)**

```javascript
// email 필드에 고유 인덱스 생성
db.users.createIndex({ email: 1 }, { unique: true })
```

**TTL 인덱스**

일정 시간이 지난 도큐먼트를 자동으로 삭제한다. 세션, 로그 등 만료가 필요한 데이터에 유용하다.

```javascript
// createdAt 기준으로 24시간(86400초) 후 자동 삭제
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 })
```

### 4.4.2 인덱스 생성과 관리

```javascript
// 현재 컬렉션의 모든 인덱스 조회
db.books.getIndexes()

// 인덱스 삭제
db.books.dropIndex("author_1")

// 모든 인덱스 삭제 (_id 인덱스 제외)
db.books.dropIndexes()

// 인덱스 크기 확인
db.books.stats().indexSizes
```

> **주의**: 인덱스는 읽기 성능을 향상시키지만 쓰기 시 인덱스 갱신 비용이 발생한다. 불필요한 인덱스는 오히려 성능을 저하시킨다. 실제 쿼리 패턴을 분석하여 필요한 인덱스만 생성하자.

### 4.4.3 explain()으로 쿼리 실행 계획 분석

`explain()` 메서드를 사용하면 쿼리가 어떻게 실행되는지 확인할 수 있다.

```javascript
// 실행 계획 확인
db.books.find({ author: "홍길동" }).explain("executionStats")
```

주요 확인 항목:

```javascript
{
  "executionStats": {
    "executionSuccess": true,
    "nReturned": 1,              // 반환된 도큐먼트 수
    "executionTimeMillis": 0,     // 실행 시간 (ms)
    "totalKeysExamined": 1,       // 검사한 인덱스 키 수
    "totalDocsExamined": 1,       // 검사한 도큐먼트 수
    "executionStages": {
      "stage": "FETCH",           // 실행 스테이지
      "inputStage": {
        "stage": "IXSCAN",        // 인덱스 스캔 사용
        "indexName": "author_1"
      }
    }
  }
}
```

핵심 지표 해석:

| 지표 | 좋은 상태 | 나쁜 상태 |
|------|-----------|-----------|
| `stage` | `IXSCAN` (인덱스 스캔) | `COLLSCAN` (컬렉션 풀 스캔) |
| `totalDocsExamined` / `nReturned` | 비율이 1에 가까움 | 비율이 매우 큼 (불필요한 스캔) |
| `executionTimeMillis` | 짧음 | 길면 최적화 필요 |

**COLLSCAN이 나타나면** 해당 쿼리 조건에 맞는 인덱스 생성을 검토해야 한다.

```javascript
// 인덱스 없이 조회 (COLLSCAN)
db.books.find({ price: { $gte: 30000 } }).explain("executionStats")
// => stage: "COLLSCAN", totalDocsExamined: 전체 도큐먼트 수

// 인덱스 생성 후 조회 (IXSCAN)
db.books.createIndex({ price: 1 })
db.books.find({ price: { $gte: 30000 } }).explain("executionStats")
// => stage: "IXSCAN", totalDocsExamined ≈ nReturned
```

---

## 4.5 MongoDB와 리액티브 드라이버

### 4.5.1 MongoDB Reactive Streams Driver

MongoDB는 공식적으로 **Reactive Streams** 사양을 구현한 Java 드라이버를 제공한다. 이 드라이버는 논블로킹 I/O를 기반으로 동작하며, Netty를 내부 네트워크 레이어로 사용한다.

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.mongodb</groupId>
    <artifactId>mongodb-driver-reactivestreams</artifactId>
    <version>5.3.0</version>
</dependency>
```

Reactive Streams Driver를 직접 사용하는 예시:

```java
import com.mongodb.reactivestreams.client.MongoClients;
import com.mongodb.reactivestreams.client.MongoClient;
import com.mongodb.reactivestreams.client.MongoDatabase;
import com.mongodb.reactivestreams.client.MongoCollection;
import org.bson.Document;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

// 클라이언트 생성
MongoClient mongoClient = MongoClients.create("mongodb://admin:secret1234@localhost:27017");
MongoDatabase database = mongoClient.getDatabase("webflux_demo");
MongoCollection<Document> collection = database.getCollection("books");

// 도큐먼트 삽입 (Publisher를 Reactor의 Mono로 래핑)
Document book = new Document("title", "Reactive MongoDB")
    .append("author", "Jane Doe")
    .append("price", 42000);

Mono.from(collection.insertOne(book))
    .subscribe(result ->
        System.out.println("Inserted ID: " + result.getInsertedId()));

// 도큐먼트 조회 (Publisher를 Reactor의 Flux로 래핑)
Flux.from(collection.find())
    .doOnNext(doc -> System.out.println(doc.toJson()))
    .subscribe();
```

### 4.5.2 동기 vs 리액티브 드라이버 비교

| 구분 | 동기 드라이버 | 리액티브 드라이버 |
|------|-------------|-----------------|
| 아티팩트 | `mongodb-driver-sync` | `mongodb-driver-reactivestreams` |
| I/O 모델 | 블로킹 | 논블로킹 |
| 반환 타입 | `List<T>`, `T` | `Publisher<T>` |
| 스레드 모델 | 요청당 스레드 점유 | 이벤트 루프 기반, 스레드 공유 |
| 배압 지원 | 없음 | Reactive Streams 배압 지원 |
| 적합한 프레임워크 | Spring MVC | Spring WebFlux |

동기 드라이버에서 `find()`를 호출하면 결과가 모두 반환될 때까지 호출 스레드가 블로킹된다. 리액티브 드라이버에서는 `Publisher`를 반환하고 구독 시점에 비동기로 데이터를 스트리밍한다.

```java
// 동기 드라이버 — 스레드가 결과 반환까지 대기
List<Document> books = syncCollection.find().into(new ArrayList<>());

// 리액티브 드라이버 — 논블로킹, 데이터가 준비되면 콜백
Flux.from(reactiveCollection.find())
    .collectList()
    .subscribe(books -> { /* 결과 처리 */ });
```

### 4.5.3 Spring Data MongoDB Reactive 모듈 소개

실무에서 Reactive Streams Driver를 직접 사용하는 일은 드물다. **Spring Data MongoDB Reactive** 모듈이 드라이버를 추상화하여 훨씬 편리한 프로그래밍 모델을 제공한다.

**의존성 추가**

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-mongodb-reactive</artifactId>
</dependency>
```

```groovy
// build.gradle (Kotlin DSL)
implementation("org.springframework.boot:spring-boot-starter-data-mongodb-reactive")
```

**도메인 모델 정의**

```java
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Document(collection = "books")   // MongoDB 컬렉션 매핑
public class Book {

    @Id
    private String id;            // MongoDB의 _id에 매핑
    private String title;
    private String author;
    private BigDecimal price;
    private List<String> tags;
    private LocalDateTime publishedAt;

    // 생성자, getter, setter 생략
}
```

**ReactiveMongoRepository 정의**

```java
import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface BookRepository extends ReactiveMongoRepository<Book, String> {

    // 메서드 이름 기반 쿼리 자동 생성
    Flux<Book> findByAuthor(String author);

    Flux<Book> findByPriceGreaterThanEqual(BigDecimal price);

    Flux<Book> findByTagsContaining(String tag);

    Mono<Book> findByTitle(String title);
}
```

**서비스 및 컨트롤러 예시**

```java
@Service
@RequiredArgsConstructor
public class BookService {

    private final BookRepository bookRepository;

    public Flux<Book> findAll() {
        return bookRepository.findAll();
    }

    public Mono<Book> findById(String id) {
        return bookRepository.findById(id)
            .switchIfEmpty(Mono.error(
                new RuntimeException("Book not found: " + id)));
    }

    public Mono<Book> create(Book book) {
        return bookRepository.save(book);
    }

    public Mono<Void> delete(String id) {
        return bookRepository.deleteById(id);
    }
}

@RestController
@RequestMapping("/api/books")
@RequiredArgsConstructor
public class BookController {

    private final BookService bookService;

    @GetMapping
    public Flux<Book> getAll() {
        return bookService.findAll();
    }

    @GetMapping("/{id}")
    public Mono<Book> getById(@PathVariable String id) {
        return bookService.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<Book> create(@RequestBody Book book) {
        return bookService.create(book);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(@PathVariable String id) {
        return bookService.delete(id);
    }
}
```

위 코드에서 중요한 점은 **반환 타입이 모두 `Mono` 또는 `Flux`라는 것**이다. 컨트롤러에서 `Mono`나 `Flux`를 반환하면 WebFlux가 구독을 관리하고, 데이터가 준비되는 대로 논블로킹 방식으로 HTTP 응답을 스트리밍한다. 데이터베이스 쿼리부터 HTTP 응답까지 전체 흐름에서 스레드가 블로킹되지 않는다.

**application.yml 설정**

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://admin:secret1234@localhost:27017/webflux_demo?authSource=admin
```

> **Spring Data MongoDB Reactive의 핵심 구성 요소**는 Chapter 5에서 프로젝트를 직접 구성하면서 상세하게 다루고, Chapter 6에서 실제 REST API를 구현하며 실습한다. Chapter 8에서는 `ReactiveMongoTemplate`, Aggregation, Change Streams 등 심화 기능을 다룬다.

---

## 4장 정리

이번 장에서 다룬 핵심 내용을 정리한다.

| 주제 | 핵심 요약 |
|------|----------|
| NoSQL vs RDBMS | MongoDB는 유연한 스키마, 수평 확장, 높은 가용성을 제공하는 도큐먼트 DB |
| CAP 정리 | MongoDB는 CP 시스템. `writeConcern`, `readPreference`로 균형 조절 가능 |
| 도큐먼트 모델 | BSON 형식, 내장 vs 참조 설계 결정이 핵심 |
| 기본 CRUD | `insertOne/Many`, `find`, `updateOne/Many`, `deleteOne/Many` |
| 인덱스 | 단일, 복합, 멀티키, 텍스트, TTL. `explain()`으로 실행 계획 분석 |
| 리액티브 드라이버 | 논블로킹 I/O, `Publisher<T>` 반환, Spring Data MongoDB Reactive로 추상화 |

다음 Chapter 5에서는 실제 개발 환경을 구성하고, Spring Boot + WebFlux + MongoDB Reactive 프로젝트를 처음부터 세팅한다.
# Chapter 5. 개발 환경 구성

Part 1에서 리액티브 프로그래밍, WebFlux, Reactor, MongoDB의 이론적 토대를 다졌다. 이제 Part 2의 첫 장으로서 실제 코드를 작성할 수 있는 개발 환경을 구성한다. JDK 설치부터 IDE 설정, Docker 기반 MongoDB 실행, 프로젝트 생성, 의존성 구성, 그리고 팀 단위에서도 활용 가능한 프로젝트 구조 설계까지 한 번에 정리한다.

---

## 5.1 JDK, IDE, Docker 설치

### 5.1.1 JDK 17+ 설치 — SDKMAN 활용

Spring Boot 3.x는 Java 17 이상을 요구한다. 여러 JDK 버전을 프로젝트별로 전환해야 하는 경우가 많으므로 **SDKMAN**을 활용하면 편리하다.

**SDKMAN 설치 (macOS / Linux)**

```bash
# SDKMAN 설치
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# 설치 확인
sdk version
```

**JDK 설치 및 버전 관리**

```bash
sdk list java                          # 설치 가능한 JDK 목록
sdk install java 21.0.5-amzn           # Amazon Corretto 21 설치 (LTS)
sdk default java 21.0.5-amzn           # 기본 JDK 설정
java -version                          # 확인
```

> **Windows 사용자**: SDKMAN 대신 [scoop](https://scoop.sh)(`scoop install corretto21-jdk`)이나 직접 다운로드를 권장한다.

**프로젝트별 JDK 자동 전환** -- 프로젝트 루트에 `.sdkmanrc`를 생성하면 디렉터리 진입 시 자동 전환된다.

```properties
# .sdkmanrc
java=21.0.5-amzn
```

### 5.1.2 IntelliJ IDEA 설정

**권장 에디션**: IntelliJ IDEA Ultimate (Spring Boot 지원 내장). Community Edition도 사용 가능하지만 Spring 전용 도구 지원이 제한적이다.

**필수 플러그인**

| 플러그인 | 용도 |
|---------|------|
| Lombok | `@Data`, `@Builder` 등 Lombok 어노테이션 지원 |
| Docker | IDE 내에서 Docker 컨테이너 관리 |
| MongoDB Plugin | MongoDB 쿼리 실행 및 데이터 브라우징 |
| Reactive Streams | Reactor 체인 디버깅 보조 |

**IDE 핵심 설정**

- `Annotation Processors` → Enable annotation processing 체크 (Lombok 필수)
- `Build Tools → Gradle` → Build and run using: **IntelliJ IDEA** (빌드 속도 향상)
- `File Encodings` → Project/Properties Encoding: **UTF-8**

### 5.1.3 Docker Desktop 설치

MongoDB를 로컬에서 실행할 때 Docker를 사용하면 설치·제거가 간편하고 팀원 간 동일한 환경을 보장할 수 있다.

```bash
# macOS — Homebrew를 통한 설치
brew install --cask docker

# 설치 확인
docker --version
docker compose version
```

Docker Desktop 실행 후 **Resources** 설정에서 메모리를 최소 4GB 이상 할당하는 것을 권장한다. MongoDB와 애플리케이션을 동시에 실행하려면 충분한 리소스가 필요하다.

---

## 5.2 Spring Initializr로 프로젝트 생성

### 5.2.1 start.spring.io 사용법

[https://start.spring.io](https://start.spring.io)에 접속하여 다음과 같이 설정한다.

| 항목 | 설정값 |
|------|--------|
| Project | Gradle - Kotlin DSL |
| Language | Java |
| Spring Boot | 3.4.x (최신 안정 버전) |
| Group | `com.example` |
| Artifact | `webflux-mongo-demo` |
| Name | `webflux-mongo-demo` |
| Package name | `com.example.webfluxmongodemo` |
| Packaging | Jar |
| Java | 21 |

### 5.2.2 의존성 선택

Spring Initializr에서 다음 의존성을 추가한다.

| 의존성 | 설명 |
|--------|------|
| **Spring Reactive Web** | WebFlux 핵심 (Netty 내장) |
| **Spring Data Reactive MongoDB** | 리액티브 MongoDB 드라이버 + Repository |
| **Lombok** | 보일러플레이트 코드 제거 |
| **Spring Boot DevTools** | 핫 리로드, 자동 재시작 |
| **Validation** | Bean Validation (jakarta.validation) |
| **Spring Boot Actuator** | 헬스 체크, 메트릭 |

**GENERATE** 버튼을 클릭하면 ZIP 파일이 다운로드된다. 압축을 풀고 IntelliJ IDEA에서 `Open`으로 프로젝트를 연다.

> **IntelliJ에서 직접 생성**: `File → New → Project → Spring Boot`를 선택하면 IDE 안에서 동일한 작업을 수행할 수 있다.

### 5.2.3 초기 프로젝트 구조

Spring Initializr가 생성하는 기본 구조는 `build.gradle.kts`, `src/main/java/` 하위의 메인 클래스, `src/main/resources/application.properties`, `src/test/` 하위의 테스트 클래스로 구성된다. 이후 `application.properties`는 `application.yml`로 변환하여 사용한다.

---

## 5.3 주요 의존성 설정

### 5.3.1 build.gradle.kts 전체 예시

```kotlin
plugins {
    java
    id("org.springframework.boot") version "3.4.1"
    id("io.spring.dependency-management") version "1.1.7"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

configurations {
    compileOnly {
        extendsFrom(configurations.annotationProcessor.get())
    }
}

repositories {
    mavenCentral()
}

dependencies {
    // Spring WebFlux (Netty 기반 논블로킹 웹 서버)
    implementation("org.springframework.boot:spring-boot-starter-webflux")
    // Spring Data Reactive MongoDB
    implementation("org.springframework.boot:spring-boot-starter-data-mongodb-reactive")
    // Validation (jakarta.validation)
    implementation("org.springframework.boot:spring-boot-starter-validation")
    // Actuator (헬스 체크, 메트릭)
    implementation("org.springframework.boot:spring-boot-starter-actuator")

    // Lombok
    compileOnly("org.projectlombok:lombok")
    annotationProcessor("org.projectlombok:lombok")
    // DevTools (개발 시 자동 재시작)
    developmentOnly("org.springframework.boot:spring-boot-devtools")

    // 테스트
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("io.projectreactor:reactor-test")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

### 5.3.2 의존성 상세 설명

| 스타터 | 포함 항목 |
|--------|-----------|
| `starter-webflux` | `spring-webflux` + `reactor-netty`(내장 서버) + Jackson JSON |
| `starter-data-mongodb-reactive` | `mongodb-driver-reactivestreams` + `spring-data-mongodb` + Reactor 어댑터 |
| `reactor-test` | `StepVerifier` 등 리액티브 스트림 테스트 유틸 (Ch.16에서 상세 설명) |

> **주의**: `spring-boot-starter-web`(Spring MVC)을 함께 추가하면 MVC가 우선 적용되어 Netty 대신 Tomcat이 구동된다. 반드시 둘 중 하나만 선택한다.

### 5.3.3 Gradle Wrapper 버전 관리

```bash
./gradlew --version                        # 현재 버전 확인
./gradlew wrapper --gradle-version=8.12    # 업그레이드
```

---

## 5.4 application.yml 설정

`application.properties`를 삭제하고 `application.yml`을 생성한다. YAML 형식이 계층 구조를 표현하기에 더 적합하다.

### 5.4.1 기본 설정 (application.yml)

```yaml
spring:
  application:
    name: webflux-mongo-demo
  data:
    mongodb:
      uri: mongodb://appuser:apppass@localhost:27017/webflux_demo?authSource=admin
  jackson:
    default-property-inclusion: non_null
    serialization:
      write-dates-as-timestamps: false
    deserialization:
      fail-on-unknown-properties: false

server:
  port: 8080
  netty:
    connection-timeout: 5000
    idle-timeout: 15000

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,env
  endpoint:
    health:
      show-details: when-authorized

logging:
  level:
    root: INFO
    com.example.webfluxmongodemo: DEBUG
    org.springframework.data.mongodb: DEBUG
    reactor.netty: INFO
  pattern:
    console: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"
```

### 5.4.2 프로파일별 설정

Spring Boot는 `application-{profile}.yml` 파일을 통해 환경별 설정을 분리할 수 있다.

**application-local.yml (로컬 개발)**

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://appuser:apppass@localhost:27017/webflux_demo?authSource=admin
  devtools:
    restart:
      enabled: true
      poll-interval: 2s
      quiet-period: 1s

logging:
  level:
    com.example.webfluxmongodemo: DEBUG
    org.springframework.data.mongodb.core.ReactiveMongoTemplate: DEBUG
```

**application-prod.yml (운영)**

```yaml
spring:
  data:
    mongodb:
      uri: ${MONGODB_URI}    # 환경 변수에서 주입

server:
  port: ${SERVER_PORT:8080}   # 환경 변수 없으면 8080 기본값

logging:
  level:
    root: WARN
    com.example.webfluxmongodemo: INFO
    org.springframework.data.mongodb: WARN
```

**프로파일 활성화 방법**

```bash
java -jar app.jar --spring.profiles.active=local      # JVM 옵션
export SPRING_PROFILES_ACTIVE=local                    # 환경 변수
```

### 5.4.3 MongoDB 연결 URI 상세

MongoDB URI 포맷을 정확히 이해하면 다양한 환경에 대응할 수 있다.

```
mongodb://[username:password@]host[:port]/database[?options]
```

| 옵션 | 설명 | 예시 |
|------|------|------|
| `authSource` | 인증 DB | `authSource=admin` |
| `replicaSet` | 복제 세트 이름 | `replicaSet=rs0` |
| `maxPoolSize` | 커넥션 풀 최대 크기 | `maxPoolSize=50` |
| `connectTimeoutMS` | 연결 타임아웃 | `connectTimeoutMS=5000` |
| `ssl` | SSL/TLS 사용 여부 | `ssl=true` |

**복제 세트 연결 예시**

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://user:pass@host1:27017,host2:27017,host3:27017/mydb?replicaSet=rs0&readPreference=secondaryPreferred
```

---

## 5.5 MongoDB Docker 컨테이너 구성

### 5.5.1 docker-compose.yml 작성

프로젝트 루트에 `docker-compose.yml`을 생성한다.

```yaml
version: "3.9"

services:
  # ──────────────────────────────────────────────
  # MongoDB
  # ──────────────────────────────────────────────
  mongodb:
    image: mongo:7.0
    container_name: webflux-mongo
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin1234
      MONGO_INITDB_DATABASE: webflux_demo
    volumes:
      - mongo-data:/data/db                  # 데이터 영속화
      - ./docker/mongo-init.js:/docker-entrypoint-initdb.d/init.js:ro  # 초기화 스크립트
    command: ["mongod", "--bind_ip_all"]
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # ──────────────────────────────────────────────
  # Mongo Express (선택 — 웹 기반 관리 도구)
  # ──────────────────────────────────────────────
  mongo-express:
    image: mongo-express:1.0
    container_name: webflux-mongo-express
    restart: unless-stopped
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: admin1234
      ME_CONFIG_MONGODB_URL: mongodb://admin:admin1234@mongodb:27017/
      ME_CONFIG_BASICAUTH: "false"
    depends_on:
      mongodb:
        condition: service_healthy

volumes:
  mongo-data:
    driver: local
```

### 5.5.2 초기화 스크립트

`docker/mongo-init.js` 파일을 작성하여 컨테이너 최초 실행 시 애플리케이션 전용 사용자와 데이터베이스를 자동 생성한다.

```javascript
// docker/mongo-init.js
// MongoDB 컨테이너 최초 실행 시 1회 실행된다.

// 애플리케이션 전용 사용자 생성
db = db.getSiblingDB("webflux_demo");

db.createUser({
    user: "appuser",
    pwd: "apppass",
    roles: [
        { role: "readWrite", db: "webflux_demo" }
    ]
});

// 초기 컬렉션 생성 (선택)
db.createCollection("users");
db.createCollection("posts");

print("===== MongoDB 초기화 완료 =====");
```

### 5.5.3 Docker Compose 실행

```bash
docker compose up -d                    # 컨테이너 시작 (백그라운드)
docker compose logs -f mongodb          # 로그 확인
docker compose ps                       # 상태 확인
docker compose down                     # 중지
docker compose down -v                  # 중지 + 볼륨 삭제 (데이터 초기화)
```

**정상 동작 확인**

```bash
docker exec -it webflux-mongo mongosh -u appuser -p apppass \
  --authenticationDatabase admin webflux_demo

# 셸 내부에서
db.users.insertOne({ name: "테스트", email: "test@example.com" })
db.users.find()
```

### 5.5.4 .env 파일로 민감 정보 분리

docker-compose.yml에 비밀번호를 직접 넣는 대신 `.env` 파일을 활용하고, `.gitignore`에 `.env`를 추가한다.

```properties
# .env (git에 포함시키지 않는다)
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=admin1234
```

```yaml
# docker-compose.yml에서 환경 변수 참조
environment:
  MONGO_INITDB_ROOT_USERNAME: ${MONGO_ROOT_USERNAME}
  MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
```

---

## 5.6 프로젝트 구조 설계

프로젝트가 커지면 패키지 구조가 코드의 탐색성과 유지보수성을 좌우한다. 두 가지 대표적인 구조를 비교한 뒤 본서의 권장 구조를 제시한다.

### 5.6.1 계층형 vs 도메인형 비교

| 구분 | 계층형 (Layer-based) | 도메인형 (Domain-based) |
|------|---------------------|------------------------|
| 패키지 분류 기준 | 기술적 역할 (`controller/`, `service/`, `repository/`) | 비즈니스 도메인 (`user/`, `post/`, `comment/`) |
| 장점 | 구조 단순, Spring 입문자에게 친숙 | 관련 코드가 한 곳에 모여 파악·수정 용이, MSA 분리에 유리 |
| 단점 | 프로젝트가 커지면 도메인 간 경계 불명확, 수정 시 패키지 넘나듦 | 초반에 과도한 분리처럼 느껴질 수 있음 |

### 5.6.2 본서의 권장 구조 — 도메인형 하이브리드

본서에서는 도메인형을 기본으로 하되, 공통 관심사(설정, 예외 처리, 유틸리티)를 `global/` 패키지로 분리하는 하이브리드 구조를 사용한다.

```
webflux-mongo-demo/
├── build.gradle.kts
├── settings.gradle.kts
├── docker-compose.yml
├── docker/
│   └── mongo-init.js
├── .env
├── .gitignore
└── src/
    ├── main/
    │   ├── java/com/example/webfluxmongodemo/
    │   │   │
    │   │   ├── WebfluxMongoDemoApplication.java   ← 메인 클래스
    │   │   │
    │   │   ├── global/                            ← 전역 공통 모듈
    │   │   │   ├── config/
    │   │   │   │   ├── MongoConfig.java
    │   │   │   │   ├── WebFluxConfig.java
    │   │   │   │   └── SecurityConfig.java
    │   │   │   ├── exception/
    │   │   │   │   ├── GlobalExceptionHandler.java
    │   │   │   │   ├── ErrorResponse.java
    │   │   │   │   └── BusinessException.java
    │   │   │   └── util/
    │   │   │       └── DateUtils.java
    │   │   │
    │   │   ├── user/                              ← 사용자 도메인
    │   │   │   ├── domain/
    │   │   │   │   └── User.java
    │   │   │   ├── dto/
    │   │   │   │   ├── UserCreateRequest.java
    │   │   │   │   ├── UserUpdateRequest.java
    │   │   │   │   └── UserResponse.java
    │   │   │   ├── repository/
    │   │   │   │   └── UserRepository.java
    │   │   │   ├── service/
    │   │   │   │   └── UserService.java
    │   │   │   └── controller/
    │   │   │       └── UserController.java
    │   │   │
    │   │   └── post/                              ← 게시글 도메인
    │   │       ├── domain/
    │   │       │   └── Post.java
    │   │       ├── dto/
    │   │       │   ├── PostCreateRequest.java
    │   │       │   └── PostResponse.java
    │   │       ├── repository/
    │   │       │   └── PostRepository.java
    │   │       ├── service/
    │   │       │   └── PostService.java
    │   │       └── controller/
    │   │           └── PostController.java
    │   │
    │   └── resources/
    │       ├── application.yml
    │       ├── application-local.yml
    │       └── application-prod.yml
    │
    └── test/
        └── java/com/example/webfluxmongodemo/
            ├── user/
            │   ├── UserServiceTest.java
            │   └── UserControllerTest.java
            └── post/
                ├── PostServiceTest.java
                └── PostControllerTest.java
```

### 5.6.3 핵심 클래스 골격 코드

프로젝트 구조를 잡았으니 각 계층의 골격 코드를 미리 작성한다. 본격적인 구현은 Chapter 6에서 진행한다.

**메인 클래스**

```java
package com.example.webfluxmongodemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class WebfluxMongoDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(WebfluxMongoDemoApplication.class, args);
    }
}
```

**도메인 (Document)**

```java
package com.example.webfluxmongodemo.user.domain;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.index.Indexed;

import java.time.LocalDateTime;

@Document(collection = "users")     // MongoDB 컬렉션 매핑
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
public class User {

    @Id
    private String id;              // MongoDB의 _id에 매핑

    @Indexed(unique = true)         // 고유 인덱스 자동 생성
    private String email;

    private String name;
    private String password;

    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    public void updateName(String name) {
        this.name = name;
    }
}
```

**리포지토리**

```java
package com.example.webfluxmongodemo.user.repository;

import com.example.webfluxmongodemo.user.domain.User;
import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import reactor.core.publisher.Mono;

public interface UserRepository extends ReactiveMongoRepository<User, String> {

    Mono<User> findByEmail(String email);

    Mono<Boolean> existsByEmail(String email);
}
```

> `ReactiveMongoRepository`는 `ReactiveCrudRepository`를 확장하며, 반환 타입이 `Mono`와 `Flux`다. 블로킹 호출이 전혀 없다.

**서비스**

```java
package com.example.webfluxmongodemo.user.service;

import com.example.webfluxmongodemo.user.domain.User;
import com.example.webfluxmongodemo.user.dto.UserCreateRequest;
import com.example.webfluxmongodemo.user.dto.UserResponse;
import com.example.webfluxmongodemo.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public Mono<UserResponse> createUser(UserCreateRequest request) {
        User user = User.builder()
                .email(request.email())
                .name(request.name())
                .password(request.password())   // 실제로는 암호화 필수
                .build();

        return userRepository.save(user)
                .map(UserResponse::from);
    }

    public Mono<UserResponse> getUserById(String id) {
        return userRepository.findById(id)
                .map(UserResponse::from)
                .switchIfEmpty(Mono.error(
                    new IllegalArgumentException("사용자를 찾을 수 없습니다: " + id)
                ));
    }

    public Flux<UserResponse> getAllUsers() {
        return userRepository.findAll()
                .map(UserResponse::from);
    }

    public Mono<Void> deleteUser(String id) {
        return userRepository.deleteById(id);
    }
}
```

**DTO (Java Record 활용)**

```java
package com.example.webfluxmongodemo.user.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record UserCreateRequest(
    @NotBlank(message = "이름은 필수입니다")
    String name,

    @NotBlank(message = "이메일은 필수입니다")
    @Email(message = "올바른 이메일 형식이 아닙니다")
    String email,

    @NotBlank(message = "비밀번호는 필수입니다")
    @Size(min = 8, message = "비밀번호는 8자 이상이어야 합니다")
    String password
) {}
```

```java
package com.example.webfluxmongodemo.user.dto;

import com.example.webfluxmongodemo.user.domain.User;
import java.time.LocalDateTime;

public record UserResponse(
    String id,
    String name,
    String email,
    LocalDateTime createdAt
) {
    public static UserResponse from(User user) {
        return new UserResponse(
            user.getId(),
            user.getName(),
            user.getEmail(),
            user.getCreatedAt()
        );
    }
}
```

**컨트롤러**

```java
package com.example.webfluxmongodemo.user.controller;

import com.example.webfluxmongodemo.user.dto.UserCreateRequest;
import com.example.webfluxmongodemo.user.dto.UserResponse;
import com.example.webfluxmongodemo.user.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<UserResponse> createUser(@Valid @RequestBody UserCreateRequest request) {
        return userService.createUser(request);
    }

    @GetMapping("/{id}")
    public Mono<UserResponse> getUser(@PathVariable String id) {
        return userService.getUserById(id);
    }

    @GetMapping
    public Flux<UserResponse> getAllUsers() {
        return userService.getAllUsers();
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteUser(@PathVariable String id) {
        return userService.deleteUser(id);
    }
}
```

**MongoDB 설정 클래스**

```java
package com.example.webfluxmongodemo.global.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.EnableReactiveMongoAuditing;
import org.springframework.data.mongodb.repository.config.EnableReactiveMongoRepositories;

@Configuration
@EnableReactiveMongoRepositories(
    basePackages = "com.example.webfluxmongodemo"
)
@EnableReactiveMongoAuditing   // @CreatedDate, @LastModifiedDate 활성화
public class MongoConfig {
    // ReactiveMongoClient는 Spring Boot가 자동 구성한다.
    // 커스텀 설정이 필요한 경우에만 Bean을 등록한다.
}
```

### 5.6.4 프로젝트 실행 및 검증

```bash
docker compose up -d                                          # MongoDB 시작
./gradlew bootRun --args='--spring.profiles.active=local'     # 애플리케이션 시작
```

정상 기동 시 `Netty started on port 8080` 로그가 출력된다. 헬스 체크와 API로 검증한다.

```bash
# 헬스 체크 — mongo 컴포넌트가 UP이면 성공
curl http://localhost:8080/actuator/health

# 사용자 생성
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"홍길동","email":"hong@example.com","password":"password1234"}'

# 사용자 조회
curl http://localhost:8080/api/users
```

---

## 정리

이번 장에서 구성한 개발 환경을 요약하면 다음과 같다.

| 항목 | 도구/설정 |
|------|-----------|
| JDK | 21 (SDKMAN으로 관리) |
| IDE | IntelliJ IDEA + Lombok, Docker 플러그인 |
| 빌드 도구 | Gradle 8.12 + Kotlin DSL |
| 웹 프레임워크 | Spring WebFlux (Netty) |
| 데이터베이스 | MongoDB 7.0 (Docker) |
| 데이터 접근 | Spring Data Reactive MongoDB |
| 설정 관리 | application.yml + 프로파일 분리 |
| 프로젝트 구조 | 도메인형 하이브리드 |

다음 장에서는 이 환경 위에서 어노테이션 기반 REST API를 본격적으로 구현한다. 도메인 모델 정의부터 Repository, Service, Controller 각 계층의 상세 구현과 API 테스트까지 다룬다.


---

# Chapter 6. 어노테이션 기반 REST API 구현

Chapter 5에서 프로젝트 구조와 개발 환경을 갖추었다. 이번 장에서는 본격적으로 도메인 모델을 정의하고, 리포지토리, 서비스, 컨트롤러 계층을 순서대로 구축하여 완전한 CRUD REST API를 완성한다. 모든 계층에서 `Mono`와 `Flux`를 반환하며, 요청부터 응답, 데이터베이스 접근까지 논블로킹으로 동작하는 리액티브 파이프라인을 구성한다.

---

## 6.1 도메인 모델(Document) 정의

### 6.1.1 주요 어노테이션 정리

Spring Data MongoDB는 Java 객체를 MongoDB 도큐먼트에 매핑하기 위한 다양한 어노테이션을 제공한다.

| 어노테이션 | 설명 |
|-----------|------|
| `@Document` | 클래스를 MongoDB 컬렉션에 매핑한다. `collection` 속성으로 컬렉션 이름을 지정한다. |
| `@Id` | 필드를 MongoDB의 `_id`에 매핑한다. `String` 타입이면 자동으로 `ObjectId`가 생성된다. |
| `@Field` | 필드명을 MongoDB 도큐먼트의 키 이름과 다르게 매핑할 때 사용한다. |
| `@Indexed` | 해당 필드에 인덱스를 생성한다. `unique`, `direction` 등의 속성을 지원한다. |
| `@CreatedDate` | 도큐먼트 최초 저장 시 자동으로 현재 시각을 기록한다. |
| `@LastModifiedDate` | 도큐먼트 수정 시 자동으로 현재 시각을 갱신한다. |
| `@Version` | 낙관적 잠금(Optimistic Locking)을 위한 버전 필드를 지정한다. |
| `@Transient` | 해당 필드를 MongoDB에 저장하지 않는다. |

### 6.1.2 User 도메인 모델

```java
package com.example.webfluxdemo.domain;

import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.annotation.Version;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;

@Document(collection = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
@ToString
public class User {

    @Id
    private String id;

    @Field("name")
    private String name;

    @Indexed(unique = true)
    private String email;

    private String password;

    @Builder.Default
    private String role = "USER";

    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    @Version
    private Long version;

    public void updateProfile(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public void changePassword(String password) {
        this.password = password;
    }
}
```

`@Version` 필드를 추가하면 동시 수정 시 `OptimisticLockingFailureException`이 발생하여 데이터 정합성을 보호한다.

### 6.1.3 Post 도메인 모델

```java
package com.example.webfluxdemo.domain;

import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Document(collection = "posts")
@CompoundIndex(name = "author_created", def = "{'authorId': 1, 'createdAt': -1}")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
@ToString
public class Post {

    @Id
    private String id;

    private String title;

    private String content;

    @Indexed
    private String authorId;

    @Builder.Default
    private List<String> tags = new ArrayList<>();

    @Builder.Default
    private int viewCount = 0;

    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    public void update(String title, String content, List<String> tags) {
        this.title = title;
        this.content = content;
        this.tags = tags != null ? tags : this.tags;
    }

    public void incrementViewCount() {
        this.viewCount++;
    }
}
```

`@CompoundIndex`로 `authorId` 오름차순 + `createdAt` 내림차순 복합 인덱스를 생성하여, 특정 작성자의 최신 게시글 조회 쿼리를 최적화한다.

### 6.1.4 Auditing 설정

`@CreatedDate`, `@LastModifiedDate`가 동작하려면 Auditing 기능을 활성화해야 한다.

```java
package com.example.webfluxdemo.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.EnableReactiveMongoAuditing;

@Configuration
@EnableReactiveMongoAuditing
public class MongoConfig {
}
```

리액티브 환경에서는 반드시 `EnableReactiveMongoAuditing`을 사용해야 하며, 일반 `@EnableMongoAuditing`은 동작하지 않는다. 자동 인덱스 생성을 활성화하려면 `application.yml`에 다음 설정을 추가한다.

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://admin:secret1234@localhost:27017/webflux_demo?authSource=admin
      auto-index-creation: true
```

> **주의**: `auto-index-creation`은 개발 환경에서는 편리하지만, 운영 환경에서는 수동 인덱스 관리를 권장한다. 대규모 컬렉션에서 인덱스 자동 생성은 서비스 시작 시간을 지연시킬 수 있다.

---

## 6.2 ReactiveMongoRepository 활용

### 6.2.1 UserRepository 정의

```java
public interface UserRepository extends ReactiveMongoRepository<User, String> {

    // 메서드 이름 기반 쿼리 자동 생성
    Mono<User> findByEmail(String email);

    Flux<User> findByName(String name);

    Flux<User> findByRole(String role);

    Mono<Boolean> existsByEmail(String email);

    // @Query: MongoDB JSON 쿼리 직접 작성
    @Query("{ 'name': { $regex: ?0, $options: 'i' } }")
    Flux<User> searchByName(String keyword);

    // 특정 필드만 조회 (fields 속성)
    @Query(value = "{ 'role': ?0 }", fields = "{ 'name': 1, 'email': 1 }")
    Flux<User> findNameAndEmailByRole(String role);
}
```

`ReactiveMongoRepository<T, ID>`는 `ReactiveCrudRepository`를 확장하며, 다음 메서드를 기본으로 제공한다.

| 메서드 | 반환 타입 | 설명 |
|--------|----------|------|
| `save(T entity)` | `Mono<T>` | 삽입 또는 수정 |
| `findById(ID id)` | `Mono<T>` | ID로 조회 |
| `findAll()` | `Flux<T>` | 전체 조회 |
| `deleteById(ID id)` | `Mono<Void>` | ID로 삭제 |
| `count()` | `Mono<Long>` | 전체 개수 |
| `existsById(ID id)` | `Mono<Boolean>` | 존재 여부 확인 |

### 6.2.2 PostRepository 정의

```java
public interface PostRepository extends ReactiveMongoRepository<Post, String> {

    Flux<Post> findByAuthorId(String authorId);

    Flux<Post> findByTagsContaining(String tag);

    Flux<Post> findByTitleContainingIgnoreCase(String keyword);

    // 페이징: Pageable 파라미터를 전달
    Flux<Post> findByAuthorId(String authorId, Pageable pageable);

    Mono<Long> countByAuthorId(String authorId);

    // 복잡한 쿼리: 제목 또는 내용에 키워드가 포함된 게시글 검색
    @Query("{ $or: [ " +
           "  { 'title': { $regex: ?0, $options: 'i' } }, " +
           "  { 'content': { $regex: ?0, $options: 'i' } } " +
           "] }")
    Flux<Post> searchByKeyword(String keyword);

    // 정렬: 메서드 이름에 OrderBy 포함
    Flux<Post> findByAuthorIdOrderByCreatedAtDesc(String authorId);
}
```

### 6.2.3 쿼리 메서드 이름 규칙

Spring Data는 메서드 이름을 파싱하여 쿼리를 자동 생성한다. 주요 키워드:

| 키워드 | 예시 | 생성 쿼리 |
|--------|-----|-----------|
| `Is` / `Equals` | `findByName(String)` | `{ 'name': ?0 }` |
| `Between` | `findByAgeBetween(int, int)` | `{ 'age': { $gte: ?0, $lte: ?1 } }` |
| `Containing` | `findByTitleContaining(String)` | `{ 'title': { $regex: ?0 } }` |
| `In` | `findByRoleIn(List)` | `{ 'role': { $in: ?0 } }` |
| `OrderBy` | `findByAuthorIdOrderByCreatedAtDesc` | 정렬 추가 |
| `IgnoreCase` | `findByNameIgnoreCase(String)` | 대소문자 무시 |

### 6.2.4 페이징 처리

리액티브 환경에서의 페이징은 `Pageable`을 파라미터로 전달하고, 별도로 총 개수를 조회한다.

```java
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;

// 0번째 페이지, 10개씩, 생성일 내림차순
Pageable pageable = PageRequest.of(0, 10, Sort.by(Sort.Direction.DESC, "createdAt"));

Flux<Post> posts = postRepository.findByAuthorId("user123", pageable);
Mono<Long> totalCount = postRepository.countByAuthorId("user123");
```

> **참고**: Spring Data Reactive에는 `Page<T>` 반환 타입이 없다. `Page`는 전체 개수를 동기적으로 계산해야 하므로 리액티브 모델과 맞지 않기 때문이다. 대신 `Flux<T>`와 `Mono<Long>`을 조합하여 페이징 정보를 구성한다.

---

## 6.3 서비스 계층 구현

### 6.3.1 커스텀 예외 정의

먼저 서비스 계층에서 사용할 커스텀 예외를 정의한다.

```java
@Getter
public class ResourceNotFoundException extends RuntimeException {
    private final String resourceName;
    private final String fieldName;
    private final String fieldValue;

    public ResourceNotFoundException(String resourceName, String fieldName,
                                     String fieldValue) {
        super(String.format("%s not found with %s: '%s'",
                resourceName, fieldName, fieldValue));
        this.resourceName = resourceName;
        this.fieldName = fieldName;
        this.fieldValue = fieldValue;
    }
}

public class DuplicateResourceException extends RuntimeException {
    public DuplicateResourceException(String message) { super(message); }
}
```

### 6.3.2 UserService 구현체

인터페이스에서 `Mono<User> createUser(User)`, `Mono<User> getUserById(String)`, `Flux<User> getAllUsers()` 등의 CRUD 메서드를 정의하고, 구현체를 작성한다.

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    @Override
    public Mono<User> createUser(User user) {
        return userRepository.existsByEmail(user.getEmail())
                .flatMap(exists -> {
                    if (exists) {
                        return Mono.error(new DuplicateResourceException(
                                "Email already exists: " + user.getEmail()));
                    }
                    return userRepository.save(user);
                })
                .doOnSuccess(saved -> log.info("User created: {}", saved.getId()));
    }

    @Override
    public Mono<User> getUserById(String id) {
        return userRepository.findById(id)
                .switchIfEmpty(Mono.error(
                        new ResourceNotFoundException("User", "id", id)));
    }

    @Override
    public Flux<User> getAllUsers() { return userRepository.findAll(); }

    @Override
    public Flux<User> searchUsers(String keyword) {
        return userRepository.searchByName(keyword);
    }

    @Override
    public Mono<User> updateUser(String id, User user) {
        return userRepository.findById(id)
                .switchIfEmpty(Mono.error(
                        new ResourceNotFoundException("User", "id", id)))
                .flatMap(existingUser -> {
                    existingUser.updateProfile(user.getName(), user.getEmail());
                    return userRepository.save(existingUser);
                })
                .doOnSuccess(updated -> log.info("User updated: {}", updated.getId()));
    }

    @Override
    public Mono<Void> deleteUser(String id) {
        return userRepository.findById(id)
                .switchIfEmpty(Mono.error(
                        new ResourceNotFoundException("User", "id", id)))
                .flatMap(userRepository::delete)
                .doOnSuccess(v -> log.info("User deleted: {}", id));
    }
}
```

핵심 패턴: `switchIfEmpty`는 리액티브에서 `null` 검사를 대체하고, `flatMap`은 비동기 연산을 체이닝하며, `doOnSuccess`는 로깅 등 사이드 이펙트를 수행한다.

### 6.3.3 PostService 구현체

`PostService`도 동일한 패턴을 따른다. 핵심 메서드만 발췌한다.

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class PostService {

    private final PostRepository postRepository;

    public Mono<Post> createPost(Post post) {
        return postRepository.save(post)
                .doOnSuccess(saved -> log.info("Post created: {}", saved.getId()));
    }

    public Mono<Post> getPostById(String id) {
        return postRepository.findById(id)
                .switchIfEmpty(Mono.error(
                        new ResourceNotFoundException("Post", "id", id)));
    }

    public Flux<Post> getPostsByAuthor(String authorId, int page, int size) {
        PageRequest pageable = PageRequest.of(page, size,
                Sort.by(Sort.Direction.DESC, "createdAt"));
        return postRepository.findByAuthorId(authorId, pageable);
    }

    public Mono<Long> countPostsByAuthor(String authorId) { return postRepository.countByAuthorId(authorId); }

    public Mono<Post> updatePost(String id, Post post) {
        return postRepository.findById(id)
                .switchIfEmpty(Mono.error(
                        new ResourceNotFoundException("Post", "id", id)))
                .flatMap(existing -> {
                    existing.update(post.getTitle(), post.getContent(), post.getTags());
                    return postRepository.save(existing);
                });
    }

    public Mono<Void> deletePost(String id) {
        return postRepository.findById(id)
                .switchIfEmpty(Mono.error(
                        new ResourceNotFoundException("Post", "id", id)))
                .flatMap(postRepository::delete);
    }
}
```

---

## 6.4 @RestController로 CRUD API 만들기

### 6.4.1 UserController

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<UserResponse> createUser(@RequestBody CreateUserRequest request) {
        User user = User.builder()
                .name(request.name())
                .email(request.email())
                .password(request.password())
                .build();
        return userService.createUser(user)
                .map(UserResponse::from);
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<UserResponse>> getUserById(@PathVariable String id) {
        return userService.getUserById(id)
                .map(UserResponse::from)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @GetMapping
    public Flux<UserResponse> getAllUsers() {
        return userService.getAllUsers()
                .map(UserResponse::from);
    }

    @GetMapping("/search")
    public Flux<UserResponse> searchUsers(@RequestParam String keyword) {
        return userService.searchUsers(keyword)
                .map(UserResponse::from);
    }

    @PutMapping("/{id}")
    public Mono<ResponseEntity<UserResponse>> updateUser(
            @PathVariable String id,
            @RequestBody UpdateUserRequest request) {
        User user = User.builder()
                .name(request.name())
                .email(request.email())
                .build();
        return userService.updateUser(id, user)
                .map(UserResponse::from)
                .map(ResponseEntity::ok);
    }

    @DeleteMapping("/{id}")
    public Mono<ResponseEntity<Void>> deleteUser(@PathVariable String id) {
        return userService.deleteUser(id)
                .then(Mono.just(ResponseEntity.noContent().<Void>build()));
    }
}
```

컨트롤러의 핵심 패턴은 다음과 같다.

- **`@ResponseStatus`**: `ResponseEntity` 없이 상태 코드를 간편하게 지정한다.
- **`ResponseEntity`를 `Mono`로 감싸기**: `map(ResponseEntity::ok)`로 200 응답, `defaultIfEmpty(ResponseEntity.notFound().build())`로 404를 반환한다.
- **`then()`**: `Mono<Void>` 완료 후 새로운 값을 발행한다. 삭제 후 204 응답에 활용한다.

### 6.4.2 PostController

`PostController`는 `UserController`와 동일한 패턴을 따른다. 페이징 조회 부분만 발췌한다.

```java
@RestController
@RequestMapping("/api/posts")
@RequiredArgsConstructor
public class PostController {

    private final PostService postService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<PostResponse> createPost(@RequestBody CreatePostRequest request) {
        Post post = Post.builder()
                .title(request.title())
                .content(request.content())
                .authorId(request.authorId())
                .tags(request.tags())
                .build();
        return postService.createPost(post).map(PostResponse::from);
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<PostResponse>> getPostById(@PathVariable String id) {
        return postService.getPostById(id)
                .map(PostResponse::from)
                .map(ResponseEntity::ok);
    }

    @GetMapping("/author/{authorId}")
    public Flux<PostResponse> getPostsByAuthor(
            @PathVariable String authorId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        return postService.getPostsByAuthor(authorId, page, size)
                .map(PostResponse::from);
    }

    @PutMapping("/{id}")
    public Mono<ResponseEntity<PostResponse>> updatePost(
            @PathVariable String id, @RequestBody UpdatePostRequest request) {
        Post post = Post.builder()
                .title(request.title()).content(request.content())
                .tags(request.tags()).build();
        return postService.updatePost(id, post)
                .map(PostResponse::from).map(ResponseEntity::ok);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deletePost(@PathVariable String id) {
        return postService.deletePost(id);
    }
}
```

### 6.4.3 완성된 API 엔드포인트 정리

| 메서드 | URI | 상태 코드 |
|--------|-----|----------|
| `POST` | `/api/users` | 201 |
| `GET` | `/api/users`, `/api/users/{id}`, `/api/users/search?keyword=` | 200 |
| `PUT` | `/api/users/{id}` | 200 |
| `DELETE` | `/api/users/{id}` | 204 |
| `POST` | `/api/posts` | 201 |
| `GET` | `/api/posts`, `/api/posts/{id}`, `/api/posts/author/{authorId}?page=&size=` | 200 |
| `PUT` | `/api/posts/{id}` | 200 |
| `DELETE` | `/api/posts/{id}` | 204 |

---

## 6.5 요청/응답 DTO 설계

### 6.5.1 Java record를 활용한 DTO

Java 16부터 도입된 `record` 클래스는 불변 데이터 캐리어에 적합하다. 생성자, `equals()`, `hashCode()`, `toString()`을 자동으로 생성하므로 DTO로 사용하기에 이상적이다.

**User 관련 DTO**

```java
public record CreateUserRequest(String name, String email, String password) {}

public record UpdateUserRequest(String name, String email) {}

public record UserResponse(
        String id, String name, String email, String role,
        LocalDateTime createdAt, LocalDateTime updatedAt
) {
    // 도메인 -> DTO 변환 정적 팩토리 메서드
    public static UserResponse from(User user) {
        return new UserResponse(user.getId(), user.getName(), user.getEmail(),
                user.getRole(), user.getCreatedAt(), user.getUpdatedAt());
    }
}
```

**Post 관련 DTO**

Post DTO도 동일한 패턴이다. `PostResponse`의 `from()` 정적 팩토리 메서드만 발췌한다.

```java
public record CreatePostRequest(String title, String content,
                                 String authorId, List<String> tags) {}

public record UpdatePostRequest(String title, String content, List<String> tags) {}

public record PostResponse(
        String id, String title, String content, String authorId,
        List<String> tags, int viewCount,
        LocalDateTime createdAt, LocalDateTime updatedAt
) {
    public static PostResponse from(Post post) {
        return new PostResponse(
                post.getId(), post.getTitle(), post.getContent(),
                post.getAuthorId(), post.getTags(), post.getViewCount(),
                post.getCreatedAt(), post.getUpdatedAt());
    }
}
```

### 6.5.2 DTO 사용의 이점

도메인 모델을 직접 API 응답으로 노출하지 않고 DTO를 사용하는 이유: (1) `password`, `version` 등 내부 필드 노출 방지(**보안**), (2) 도메인 변경이 API 계약에 영향을 주지 않음(**안정성**), (3) 용도별 다른 DTO 제공 가능(**유연성**), (4) Bean Validation 적용 가능(**검증**, Chapter 9에서 상세히 다룬다).

### 6.5.3 페이징 응답 DTO

페이징 결과를 감싸는 범용 DTO를 만들면 클라이언트에 페이징 메타 정보를 함께 전달할 수 있다.

```java
package com.example.webfluxdemo.dto;

import java.util.List;

public record PageResponse<T>(
        List<T> content,
        int page,
        int size,
        long totalElements,
        int totalPages
) {
    public static <T> PageResponse<T> of(List<T> content, int page,
                                          int size, long totalElements) {
        int totalPages = (int) Math.ceil((double) totalElements / size);
        return new PageResponse<>(content, page, size, totalElements, totalPages);
    }
}
```

컨트롤러에서 페이징 응답을 구성하는 예시:

```java
@GetMapping("/author/{authorId}")
public Mono<PageResponse<PostResponse>> getPostsByAuthorPaged(
        @PathVariable String authorId,
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size) {

    Mono<List<PostResponse>> contentMono = postService
            .getPostsByAuthor(authorId, page, size)
            .map(PostResponse::from)
            .collectList();

    Mono<Long> countMono = postService.countPostsByAuthor(authorId);

    return Mono.zip(contentMono, countMono)
            .map(tuple -> PageResponse.of(tuple.getT1(), page, size, tuple.getT2()));
}
```

`Mono.zip`으로 콘텐츠 조회와 총 개수 조회를 **동시에** 실행하고, 두 결과를 `PageResponse`로 조합한다. 리액티브 병렬 처리의 관용적 패턴이다.

---

## 6.6 API 테스트

애플리케이션을 실행한 후, 다양한 도구로 API를 호출하여 동작을 검증한다.

```bash
# 애플리케이션 실행
./gradlew bootRun
```

### 6.6.1 cURL 테스트

**사용자 생성 (POST)**

```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "홍길동",
    "email": "hong@example.com",
    "password": "securePass123"
  }'
```

응답 예시:

```json
{
  "id": "65f1a2b3c4d5e6f7a8b9c0d1",
  "name": "홍길동",
  "email": "hong@example.com",
  "role": "USER",
  "createdAt": "2025-06-15T10:30:00",
  "updatedAt": "2025-06-15T10:30:00"
}
```

**사용자 조회 (GET)**

```bash
# 전체 조회
curl http://localhost:8080/api/users

# 단건 조회
curl http://localhost:8080/api/users/65f1a2b3c4d5e6f7a8b9c0d1
```

**수정 / 삭제 / 게시글**

```bash
# 사용자 수정
curl -X PUT http://localhost:8080/api/users/65f1a2b3c4d5e6f7a8b9c0d1 \
  -H "Content-Type: application/json" \
  -d '{ "name": "홍길동(수정)", "email": "hong-updated@example.com" }'

# 사용자 삭제
curl -X DELETE http://localhost:8080/api/users/65f1a2b3c4d5e6f7a8b9c0d1 -v

# 게시글 생성
curl -X POST http://localhost:8080/api/posts \
  -H "Content-Type: application/json" \
  -d '{ "title": "WebFlux 첫 글", "content": "리액티브 API 구현",
        "authorId": "65f1a2b3c4d5e6f7a8b9c0d1", "tags": ["spring","webflux"] }'

# 게시글 검색
curl "http://localhost:8080/api/posts/search?keyword=WebFlux"

# 작성자별 페이징 조회
curl "http://localhost:8080/api/posts/author/65f1a2b3c4d5e6f7a8b9c0d1?page=0&size=5"
```

### 6.6.2 HTTPie 테스트

HTTPie는 cURL보다 직관적인 문법을 제공하는 HTTP 클라이언트다.

```bash
# 사용자 생성 — JSON 필드를 key=value 형식으로 전달
http POST localhost:8080/api/users \
  name="김철수" email="kim@example.com" password="pass1234"

# 조회
http localhost:8080/api/users

# 게시글 생성 — JSON 배열은 := 연산자로 전달
http POST localhost:8080/api/posts \
  title="HTTPie 테스트" content="HTTPie로 API를 테스트합니다." \
  authorId="65f1a2b3c4d5e6f7a8b9c0d1" tags:='["test", "httpie"]'
```

> **팁**: HTTPie에서 `=`는 문자열, `:=`는 JSON 리터럴(숫자, 배열, 객체, boolean)을 전달한다.

### 6.6.3 IntelliJ HTTP Client

IntelliJ IDEA에 내장된 HTTP Client를 사용하면 `.http` 파일로 요청을 관리할 수 있다. 프로젝트 루트에 `.http` 파일을 작성한다.

```http
### 사용자 생성
POST http://localhost:8080/api/users
Content-Type: application/json

{
  "name": "이영희",
  "email": "lee@example.com",
  "password": "myPassword456"
}

### 전체 사용자 조회
GET http://localhost:8080/api/users

### 사용자 수정
PUT http://localhost:8080/api/users/{{userId}}
Content-Type: application/json

{
  "name": "이영희(수정)",
  "email": "lee-updated@example.com"
}

### 사용자 삭제
DELETE http://localhost:8080/api/users/{{userId}}
```

`{{userId}}`와 같은 변수는 `http-client.env.json` 파일에서 환경별로 관리한다. `.http` 파일을 Git으로 관리하면 팀원과 API 테스트를 공유할 수 있다는 것이 큰 장점이다.

---

## 6장 정리

이번 장에서 다룬 핵심 내용을 정리한다.

| 주제 | 핵심 요약 |
|------|----------|
| 도메인 모델 | `@Document`, `@Id`, `@Indexed`, `@CompoundIndex`로 도큐먼트 매핑. Auditing으로 생성/수정 시각 자동 관리 |
| 리포지토리 | `ReactiveMongoRepository`로 기본 CRUD 자동 제공. 쿼리 메서드 이름 규칙, `@Query`, 페이징 지원 |
| 서비스 계층 | `switchIfEmpty`로 존재 여부 검증, `flatMap`으로 비동기 체이닝, 커스텀 예외로 의미 있는 에러 전달 |
| 컨트롤러 | `@RestController`로 CRUD 엔드포인트 구성. `ResponseEntity`로 상태 코드 제어, `Mono`/`Flux` 반환 |
| DTO 설계 | Java `record`로 불변 DTO 정의. 도메인과 API 계약을 분리하여 보안과 유지보수성 확보 |
| API 테스트 | cURL, HTTPie, IntelliJ HTTP Client로 엔드포인트 검증 |

다음 Chapter 7에서는 어노테이션 방식 대신 **함수형 엔드포인트(Router Functions)** 를 사용하여 동일한 API를 구현하고, 두 방식의 차이점과 장단점을 비교한다.


---

# Chapter 7. 함수형 엔드포인트 (Router Functions)

앞선 Chapter 6에서는 `@RestController`와 어노테이션 기반으로 REST API를 구현했다. Spring WebFlux는 또 다른 프로그래밍 모델인 **함수형 엔드포인트**를 제공한다. 이번 장에서는 `RouterFunction`과 `HandlerFunction`을 사용하여 동일한 API를 함수형 방식으로 구현하고, 두 방식의 차이를 비교한다.

---

## 7.1 HandlerFunction과 RouterFunction 이해

### 7.1.1 함수형 엔드포인트의 핵심 구성 요소

함수형 엔드포인트는 두 가지 핵심 인터페이스로 구성된다.

| 구성 요소 | 역할 | 대응하는 어노테이션 방식 |
|-----------|------|------------------------|
| `HandlerFunction` | 요청을 받아 응답을 생성하는 함수 | `@RequestMapping` 메서드 본문 |
| `RouterFunction` | 요청을 적절한 HandlerFunction으로 라우팅 | `@RequestMapping`, `@GetMapping` 등 |
| `ServerRequest` | 불변(immutable) HTTP 요청 객체 | 메서드 파라미터 (`@RequestBody`, `@PathVariable` 등) |
| `ServerResponse` | HTTP 응답을 빌더 패턴으로 생성 | 컨트롤러 반환값 |

### 7.1.2 HandlerFunction 인터페이스

`HandlerFunction<T extends ServerResponse>`는 `ServerRequest`를 받아 `Mono<T>`를 반환하는 함수형 인터페이스다.

```java
@FunctionalInterface
public interface HandlerFunction<T extends ServerResponse> {
    Mono<T> handle(ServerRequest request);
}
```

개념적으로 보면 `Function<ServerRequest, Mono<ServerResponse>>`와 동일하다. 이 단순한 시그니처 덕분에 람다로 간결하게 핸들러를 작성할 수 있다.

```java
// 람다로 작성한 간단한 핸들러
HandlerFunction<ServerResponse> helloHandler = request ->
    ServerResponse.ok()
        .contentType(MediaType.TEXT_PLAIN)
        .bodyValue("Hello, WebFlux!");
```

### 7.1.3 RouterFunction 인터페이스

`RouterFunction<T extends ServerResponse>`는 요청을 분석하여 적절한 `HandlerFunction`으로 연결하는 역할을 한다.

```java
@FunctionalInterface
public interface RouterFunction<T extends ServerResponse> {
    Mono<HandlerFunction<T>> route(ServerRequest request);
}
```

직접 구현하기보다는 `RouterFunctions.route()` 헬퍼 메서드를 사용하여 선언적으로 라우팅을 정의한다.

### 7.1.4 ServerRequest와 ServerResponse

**ServerRequest**는 불변 객체로, HTTP 메서드, URI, 헤더, 쿼리 파라미터, 요청 바디에 접근하는 메서드를 제공한다.

```java
// ServerRequest 주요 메서드
request.method();                          // HTTP 메서드
request.uri();                             // 전체 URI
request.path();                            // 경로
request.pathVariable("id");               // 경로 변수
request.queryParam("name");               // 쿼리 파라미터 (Optional)
request.headers();                         // 헤더 접근
request.bodyToMono(Product.class);        // 바디를 Mono로 변환
request.bodyToFlux(Product.class);        // 바디를 Flux로 변환
```

**ServerResponse**는 빌더 패턴으로 HTTP 응답을 구성한다.

```java
// 200 OK + JSON 바디
ServerResponse.ok()
    .contentType(MediaType.APPLICATION_JSON)
    .bodyValue(product);

// 201 Created + Location 헤더
ServerResponse.created(URI.create("/api/products/" + id))
    .bodyValue(savedProduct);

// 204 No Content
ServerResponse.noContent().build();

// 404 Not Found
ServerResponse.notFound().build();

// Mono/Flux를 바디로 설정
ServerResponse.ok().body(productMono, Product.class);
ServerResponse.ok().body(productFlux, Product.class);
```

---

## 7.2 RouterFunction으로 라우팅 정의하기

### 7.2.1 기본 라우팅 정의

`RouterFunctions.route()`와 `RequestPredicates`를 조합하여 라우팅 규칙을 정의한다.

```java
import static org.springframework.web.reactive.function.server.RouterFunctions.route;
import static org.springframework.web.reactive.function.server.RequestPredicates.*;

@Configuration
public class ProductRouter {

    @Bean
    public RouterFunction<ServerResponse> productRoutes(ProductHandler handler) {
        return route(GET("/api/products"), handler::getAll)
            .andRoute(GET("/api/products/{id}"), handler::getById)
            .andRoute(POST("/api/products"), handler::create)
            .andRoute(PUT("/api/products/{id}"), handler::update)
            .andRoute(DELETE("/api/products/{id}"), handler::delete);
    }
}
```

`RequestPredicates`는 요청 조건을 표현하는 유틸리티 클래스다. HTTP 메서드, 경로, 콘텐츠 타입 등 다양한 조건을 조합할 수 있다.

```java
// 메서드 + 경로
GET("/api/products")
POST("/api/products")

// 경로만
path("/api/products")

// 콘텐츠 타입 조건 추가
POST("/api/products").and(contentType(MediaType.APPLICATION_JSON))

// Accept 헤더 조건
GET("/api/products").and(accept(MediaType.APPLICATION_JSON))

// 조건 결합
method(HttpMethod.GET).and(path("/api/products")).and(accept(MediaType.APPLICATION_JSON))
```

### 7.2.2 nest()로 라우팅 그룹화

공통 경로 접두사나 조건을 공유하는 라우트를 `nest()`로 그룹화하면 중복을 제거하고 가독성을 높일 수 있다.

```java
@Configuration
public class ProductRouter {

    @Bean
    public RouterFunction<ServerResponse> productRoutes(ProductHandler handler) {
        return nest(path("/api/products"),
            route(GET(""), handler::getAll)
            .andRoute(GET("/{id}"), handler::getById)
            .andRoute(POST("").and(contentType(MediaType.APPLICATION_JSON)), handler::create)
            .andRoute(PUT("/{id}").and(contentType(MediaType.APPLICATION_JSON)), handler::update)
            .andRoute(DELETE("/{id}"), handler::delete)
        );
    }
}
```

여러 리소스를 하나의 설정 클래스에서 관리할 수도 있다.

```java
@Configuration
public class AppRouter {

    @Bean
    public RouterFunction<ServerResponse> routes(
            ProductHandler productHandler,
            CategoryHandler categoryHandler,
            OrderHandler orderHandler) {

        return nest(path("/api"),
            nest(path("/products"),
                route(GET(""), productHandler::getAll)
                .andRoute(GET("/{id}"), productHandler::getById)
                .andRoute(POST(""), productHandler::create)
                .andRoute(PUT("/{id}"), productHandler::update)
                .andRoute(DELETE("/{id}"), productHandler::delete)
            )
            .andNest(path("/categories"),
                route(GET(""), categoryHandler::getAll)
                .andRoute(GET("/{id}"), categoryHandler::getById)
                .andRoute(POST(""), categoryHandler::create)
            )
            .andNest(path("/orders"),
                route(GET(""), orderHandler::getAll)
                .andRoute(POST(""), orderHandler::create)
            )
        );
    }
}
```

### 7.2.3 필터 적용

`RouterFunction`에 `filter()`를 적용하여 요청/응답을 가로채는 공통 로직을 추가할 수 있다. 어노테이션 방식의 `WebFilter`나 `HandlerInterceptor`에 대응하는 개념이다.

```java
@Bean
public RouterFunction<ServerResponse> productRoutes(ProductHandler handler) {
    return nest(path("/api/products"),
        route(GET(""), handler::getAll)
        .andRoute(GET("/{id}"), handler::getById)
        .andRoute(POST(""), handler::create)
    )
    .filter((request, next) -> {
        long startTime = System.currentTimeMillis();
        log.info("Request: {} {}", request.method(), request.path());

        return next.handle(request)
            .doOnSuccess(response -> {
                long duration = System.currentTimeMillis() - startTime;
                log.info("Response: {} ({}ms)", response.statusCode(), duration);
            });
    });
}
```

### 7.2.4 before()와 after()

`filter()` 외에도 `before()`와 `after()`로 요청 전/후 처리를 분리할 수 있다.

```java
@Bean
public RouterFunction<ServerResponse> productRoutes(ProductHandler handler) {
    return route(GET("/api/products"), handler::getAll)
        .andRoute(POST("/api/products"), handler::create)
        .before(request -> {
            log.info("[Before] {} {}", request.method(), request.path());
            return request;
        })
        .after((request, response) -> {
            log.info("[After] {} -> {}", request.path(), response.statusCode());
            return response;
        });
}
```

---

## 7.3 HandlerFunction 구현

### 7.3.1 Handler 클래스 구조

실전에서는 핸들러를 별도의 클래스로 분리하여 관리한다. 어노테이션 방식의 컨트롤러에 대응하는 역할을 한다.

```java
@Component
@RequiredArgsConstructor
public class ProductHandler {

    private final ProductService productService;

    /**
     * 전체 상품 조회
     */
    public Mono<ServerResponse> getAll(ServerRequest request) {
        Flux<Product> products = productService.findAll();
        return ServerResponse.ok()
            .contentType(MediaType.APPLICATION_JSON)
            .body(products, Product.class);
    }

    /**
     * 단일 상품 조회
     */
    public Mono<ServerResponse> getById(ServerRequest request) {
        String id = request.pathVariable("id");
        return productService.findById(id)
            .flatMap(product -> ServerResponse.ok()
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(product))
            .switchIfEmpty(ServerResponse.notFound().build());
    }

    /**
     * 상품 생성
     */
    public Mono<ServerResponse> create(ServerRequest request) {
        return request.bodyToMono(Product.class)
            .flatMap(productService::save)
            .flatMap(saved -> ServerResponse
                .created(URI.create("/api/products/" + saved.getId()))
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(saved));
    }

    /**
     * 상품 수정
     */
    public Mono<ServerResponse> update(ServerRequest request) {
        String id = request.pathVariable("id");
        return request.bodyToMono(Product.class)
            .flatMap(product -> productService.update(id, product))
            .flatMap(updated -> ServerResponse.ok()
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(updated))
            .switchIfEmpty(ServerResponse.notFound().build());
    }

    /**
     * 상품 삭제
     */
    public Mono<ServerResponse> delete(ServerRequest request) {
        String id = request.pathVariable("id");
        return productService.deleteById(id)
            .then(ServerResponse.noContent().build());
    }
}
```

### 7.3.2 도메인 모델과 서비스 계층

핸들러가 사용하는 도메인 모델과 서비스 계층은 어노테이션 방식과 동일하게 재사용할 수 있다.

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
    private BigDecimal price;
    private String category;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
```

```java
@Service
@RequiredArgsConstructor
public class ProductService {

    private final ReactiveMongoRepository<Product, String> productRepository;

    public Flux<Product> findAll() { return productRepository.findAll(); }
    public Mono<Product> findById(String id) { return productRepository.findById(id); }

    public Mono<Product> save(Product product) {
        product.setCreatedAt(LocalDateTime.now());
        product.setUpdatedAt(LocalDateTime.now());
        return productRepository.save(product);
    }

    public Mono<Product> update(String id, Product product) {
        return productRepository.findById(id)
            .map(existing -> {
                existing.setName(product.getName());
                existing.setPrice(product.getPrice());
                existing.setCategory(product.getCategory());
                existing.setUpdatedAt(LocalDateTime.now());
                return existing;
            })
            .flatMap(productRepository::save);
    }

    public Mono<Void> deleteById(String id) { return productRepository.deleteById(id); }
```

### 7.3.3 에러 처리가 포함된 핸들러

실전에서는 검증 실패, 데이터 없음 등 다양한 에러 상황을 핸들러 내에서 처리해야 한다.

```java
@Component
@RequiredArgsConstructor
public class ProductHandler {

    private final ProductService productService;
    private final Validator validator;

    public Mono<ServerResponse> create(ServerRequest request) {
        return request.bodyToMono(Product.class)
            .doOnNext(this::validate)
            .flatMap(productService::save)
            .flatMap(saved -> ServerResponse
                .created(URI.create("/api/products/" + saved.getId()))
                .bodyValue(saved))
            .onErrorResume(ValidationException.class, e ->
                ServerResponse.badRequest()
                    .bodyValue(new ErrorResponse("VALIDATION_ERROR", e.getMessage())))
            .onErrorResume(e ->
                ServerResponse.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .bodyValue(new ErrorResponse("INTERNAL_ERROR", "서버 내부 오류가 발생했습니다.")));
    }

    private void validate(Product product) {
        Errors errors = new BeanPropertyBindingResult(product, "product");
        validator.validate(product, errors);
        if (errors.hasErrors()) {
            String message = errors.getFieldErrors().stream()
                .map(e -> e.getField() + ": " + e.getDefaultMessage())
                .collect(Collectors.joining(", "));
            throw new ValidationException(message);
        }
    }
}
```

```java
@Data
@AllArgsConstructor
public class ErrorResponse {
    private String code;
    private String message;
}
```

---

## 7.4 요청 파라미터 및 바디 처리

### 7.4.1 경로 변수 (Path Variable)

경로 패턴에 `{변수명}`으로 선언하고, `ServerRequest.pathVariable()`로 추출한다.

```java
// Router 정의
route(GET("/api/products/{id}"), handler::getById)

// Handler에서 추출
public Mono<ServerResponse> getById(ServerRequest request) {
    String id = request.pathVariable("id");
    return productService.findById(id)
        .flatMap(product -> ServerResponse.ok().bodyValue(product))
        .switchIfEmpty(ServerResponse.notFound().build());
}
```

여러 경로 변수를 사용하는 경우도 동일하다.

```java
// 중첩 리소스 라우팅
route(GET("/api/categories/{categoryId}/products/{productId}"), handler::getProductInCategory)

// Handler
public Mono<ServerResponse> getProductInCategory(ServerRequest request) {
    String categoryId = request.pathVariable("categoryId");
    String productId = request.pathVariable("productId");
    return productService.findByCategoryAndId(categoryId, productId)
        .flatMap(product -> ServerResponse.ok().bodyValue(product))
        .switchIfEmpty(ServerResponse.notFound().build());
}
```

### 7.4.2 쿼리 파라미터 (Query Parameter)

`ServerRequest.queryParam()`은 `Optional<String>`을 반환한다. `queryParams()`로 전체 파라미터 맵을 얻을 수도 있다.

```java
// GET /api/products?category=electronics&minPrice=10000&page=0&size=20
public Mono<ServerResponse> search(ServerRequest request) {
    Optional<String> category = request.queryParam("category");
    Optional<String> minPrice = request.queryParam("minPrice");
    int page = request.queryParam("page")
        .map(Integer::parseInt)
        .orElse(0);
    int size = request.queryParam("size")
        .map(Integer::parseInt)
        .orElse(20);

    Flux<Product> results = productService.search(
        category.orElse(null),
        minPrice.map(BigDecimal::new).orElse(null),
        PageRequest.of(page, size)
    );

    return ServerResponse.ok()
        .contentType(MediaType.APPLICATION_JSON)
        .body(results, Product.class);
}
```

### 7.4.3 요청 바디 처리: bodyToMono / bodyToFlux

단일 객체는 `bodyToMono()`, 컬렉션은 `bodyToFlux()`로 역직렬화한다.

```java
// 단일 객체 수신
public Mono<ServerResponse> create(ServerRequest request) {
    return request.bodyToMono(Product.class)
        .flatMap(productService::save)
        .flatMap(saved -> ServerResponse.created(
            URI.create("/api/products/" + saved.getId()))
            .bodyValue(saved));
}

// 여러 객체 일괄 수신
public Mono<ServerResponse> createBatch(ServerRequest request) {
    Flux<Product> products = request.bodyToFlux(Product.class);
    return productService.saveAll(products)
        .collectList()
        .flatMap(savedList -> ServerResponse.ok()
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(savedList));
}
```

### 7.4.4 ParameterizedTypeReference 활용

제네릭 타입을 역직렬화할 때는 `ParameterizedTypeReference`를 사용한다.

```java
// Map<String, Object> 형태의 바디 수신
public Mono<ServerResponse> handleDynamic(ServerRequest request) {
    return request.bodyToMono(new ParameterizedTypeReference<Map<String, Object>>() {})
        .flatMap(body -> {
            String name = (String) body.get("name");
            // 동적 처리
            return ServerResponse.ok().bodyValue(Map.of("received", name));
        });
}
```

### 7.4.5 헤더 및 쿠키 접근

```java
public Mono<ServerResponse> withHeaders(ServerRequest request) {
    // 헤더 접근
    ServerRequest.Headers headers = request.headers();
    List<MediaType> acceptTypes = headers.accept();
    Optional<String> authHeader = headers.firstHeader("Authorization");
    OptionalLong contentLength = headers.contentLength();

    // 쿠키 접근
    MultiValueMap<String, HttpCookie> cookies = request.cookies();
    HttpCookie sessionCookie = cookies.getFirst("SESSION_ID");

    return ServerResponse.ok()
        .bodyValue(Map.of(
            "accept", acceptTypes.toString(),
            "hasAuth", authHeader.isPresent()
        ));
}
```

### 7.4.6 멀티파트 파일 업로드

함수형 엔드포인트에서도 멀티파트 요청을 처리할 수 있다.

```java
// Router 정의
route(POST("/api/products/{id}/image")
    .and(contentType(MediaType.MULTIPART_FORM_DATA)), handler::uploadImage)
```

```java
// Handler 구현
public Mono<ServerResponse> uploadImage(ServerRequest request) {
    String productId = request.pathVariable("id");

    return request.multipartData()
        .flatMap(parts -> {
            Part filePart = parts.getFirst("file");
            if (filePart instanceof FilePart fp) {
                String filename = fp.filename();
                Path destination = Path.of("/uploads", productId + "_" + filename);
                return fp.transferTo(destination)
                    .then(productService.updateImagePath(productId, destination.toString()))
                    .flatMap(updated -> ServerResponse.ok().bodyValue(updated));
            }
            return ServerResponse.badRequest()
                .bodyValue(new ErrorResponse("INVALID_FILE", "파일이 전송되지 않았습니다."));
        });
}
```

여러 파트를 개별 처리할 때는 `BodyExtractors.toMultipartData()`를 사용하여 텍스트 필드(`FormFieldPart`)와 파일(`FilePart`)을 각각 추출할 수 있다.

---

## 7.5 어노테이션 방식과 함수형 방식 비교

### 7.5.1 같은 API를 두 방식으로 구현

동일한 상품 CRUD API를 어노테이션 방식과 함수형 방식으로 구현하여 비교한다.

**어노테이션 방식 (@RestController)**

```java
@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;

    @GetMapping
    public Flux<Product> getAll() {
        return productService.findAll();
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<Product>> getById(@PathVariable String id) {
        return productService.findById(id)
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<Product> create(@Valid @RequestBody Product product) {
        return productService.save(product);
    }

    @PutMapping("/{id}")
    public Mono<ResponseEntity<Product>> update(
            @PathVariable String id,
            @Valid @RequestBody Product product) {
        return productService.update(id, product)
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(@PathVariable String id) {
        return productService.deleteById(id);
    }
}
```

**함수형 방식 (RouterFunction + HandlerFunction)**

```java
// Router
@Configuration
public class ProductRouter {

    @Bean
    public RouterFunction<ServerResponse> productRoutes(ProductHandler handler) {
        return nest(path("/api/products"),
            route(GET(""), handler::getAll)
            .andRoute(GET("/{id}"), handler::getById)
            .andRoute(POST("").and(contentType(MediaType.APPLICATION_JSON)),
                      handler::create)
            .andRoute(PUT("/{id}").and(contentType(MediaType.APPLICATION_JSON)),
                      handler::update)
            .andRoute(DELETE("/{id}"), handler::delete)
        );
    }
}

// Handler
@Component
@RequiredArgsConstructor
public class ProductHandler {

    private final ProductService productService;

    public Mono<ServerResponse> getAll(ServerRequest request) {
        return ServerResponse.ok()
            .contentType(MediaType.APPLICATION_JSON)
            .body(productService.findAll(), Product.class);
    }

    public Mono<ServerResponse> getById(ServerRequest request) {
        String id = request.pathVariable("id");
        return productService.findById(id)
            .flatMap(product -> ServerResponse.ok()
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(product))
            .switchIfEmpty(ServerResponse.notFound().build());
    }

    public Mono<ServerResponse> create(ServerRequest request) {
        return request.bodyToMono(Product.class)
            .flatMap(productService::save)
            .flatMap(saved -> ServerResponse
                .created(URI.create("/api/products/" + saved.getId()))
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(saved));
    }

    public Mono<ServerResponse> update(ServerRequest request) {
        String id = request.pathVariable("id");
        return request.bodyToMono(Product.class)
            .flatMap(product -> productService.update(id, product))
            .flatMap(updated -> ServerResponse.ok()
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(updated))
            .switchIfEmpty(ServerResponse.notFound().build());
    }

    public Mono<ServerResponse> delete(ServerRequest request) {
        String id = request.pathVariable("id");
        return productService.deleteById(id)
            .then(ServerResponse.noContent().build());
    }
}
```

### 7.5.2 핵심 차이점 분석

두 방식의 주요 차이를 항목별로 비교한다.

**라우팅 정의**: 어노테이션 방식은 라우팅 정보(`@GetMapping`)와 비즈니스 로직이 한 곳에 위치한다. 함수형 방식은 Router(라우팅 정의)와 Handler(로직)가 물리적으로 분리된다.

**파라미터 바인딩**: 어노테이션 방식은 `@PathVariable`, `@RequestBody` 등으로 자동 바인딩된다. 함수형 방식은 `ServerRequest`의 `pathVariable()`, `bodyToMono()` 등을 직접 호출한다.

**검증 처리**: 어노테이션 방식은 `@Valid`로 자동 검증된다. 함수형 방식은 `Validator`를 수동 호출해야 한다.

### 7.5.3 장단점 비교표

| 비교 항목 | 어노테이션 방식 | 함수형 방식 |
|-----------|----------------|------------|
| **진입 장벽** | 낮음 (Spring MVC 경험 활용) | 중간 (함수형 개념 필요) |
| **코드 간결성** | 간결 (어노테이션이 많은 것을 대행) | 상대적으로 장황 |
| **라우팅-로직 분리** | 같은 클래스에 혼재 | 명확히 분리 |
| **파라미터 바인딩** | 자동 (`@PathVariable`, `@RequestBody`) | 수동 (`pathVariable()`, `bodyToMono()`) |
| **검증 통합** | `@Valid` 자동 적용 | `Validator` 수동 호출 |
| **테스트 용이성** | `@WebFluxTest` 슬라이스 테스트 | 순수 함수 단위 테스트 용이 |
| **타입 안전성** | 런타임 리플렉션 의존 | 컴파일 타임 검증 |
| **라우팅 유연성** | 고정된 어노테이션 규칙 | 프로그래밍 방식으로 동적 라우팅 가능 |
| **필터 적용** | `WebFilter` (전역) | `filter()` 메서드로 라우트별 적용 가능 |
| **OpenAPI 문서화** | SpringDoc 자동 감지 | 추가 설정 필요 |

### 7.5.4 실무 선택 기준

두 방식은 동일한 `DispatcherHandler`에서 처리되므로 **같은 애플리케이션에 공존할 수 있다**. 실무에서는 상황에 따라 적절한 방식을 선택하면 된다.

**어노테이션 방식이 적합한 경우**

- 팀에 Spring MVC 경험자가 많을 때
- CRUD 위주의 표준적인 REST API
- `@Valid`, `@ControllerAdvice` 등 Spring의 자동 지원이 필요할 때
- Swagger/OpenAPI 문서 자동 생성이 중요할 때

**함수형 방식이 적합한 경우**

- 라우팅 로직이 동적으로 변해야 할 때
- 라우팅 정의와 비즈니스 로직을 명확히 분리하고 싶을 때
- 특정 라우트 그룹에만 필터를 적용해야 할 때
- 경량 마이크로서비스에서 불필요한 어노테이션 처리를 줄이고 싶을 때
- 함수형 프로그래밍 스타일을 선호하는 팀

**혼합 사용 예시**

```java
// 어노테이션 방식 — 일반 CRUD API
@RestController
@RequestMapping("/api/users")
public class UserController {
    // 표준적인 CRUD 엔드포인트
}

// 함수형 방식 — 동적 라우팅이 필요한 특수 API
@Configuration
public class WebhookRouter {

    @Bean
    public RouterFunction<ServerResponse> webhookRoutes(WebhookHandler handler) {
        return nest(path("/api/webhooks"),
            route(POST("/{provider}"), handler::handle)
            .filter((request, next) -> {
                // 웹훅 제공자별 서명 검증
                String provider = request.pathVariable("provider");
                return verifySignature(request, provider)
                    .flatMap(valid -> valid
                        ? next.handle(request)
                        : ServerResponse.status(HttpStatus.UNAUTHORIZED).build());
            })
        );
    }
}
```

### 7.5.5 함수형 엔드포인트에서 OpenAPI 문서화

함수형 방식에서는 SpringDoc이 라우팅 정보를 자동 감지하지 못한다. `@RouterOperation`으로 API 명세를 수동 추가해야 한다.

```java
@Bean
@RouterOperations({
    @RouterOperation(path = "/api/products", method = RequestMethod.GET,
        beanClass = ProductHandler.class, beanMethod = "getAll",
        operation = @Operation(operationId = "getAllProducts",
            summary = "전체 상품 조회")),
    @RouterOperation(path = "/api/products/{id}", method = RequestMethod.GET,
        beanClass = ProductHandler.class, beanMethod = "getById",
        operation = @Operation(operationId = "getProductById",
            summary = "상품 단건 조회",
            parameters = @Parameter(name = "id", in = ParameterIn.PATH, required = true)))
})
public RouterFunction<ServerResponse> productRoutes(ProductHandler handler) {
    return nest(path("/api/products"),
        route(GET(""), handler::getAll)
        .andRoute(GET("/{id}"), handler::getById)
    );
}
```

---

## 요약

이번 장에서 다룬 핵심 내용을 정리한다.

| 주제 | 핵심 내용 |
|------|----------|
| **HandlerFunction** | `ServerRequest -> Mono<ServerResponse>` 시그니처의 함수형 인터페이스 |
| **RouterFunction** | `route()`, `nest()`로 선언적 라우팅 정의, `filter()`로 공통 로직 적용 |
| **ServerRequest** | 불변 요청 객체, `pathVariable()`, `queryParam()`, `bodyToMono()` 등으로 데이터 추출 |
| **ServerResponse** | 빌더 패턴으로 상태 코드, 헤더, 바디를 설정하여 응답 생성 |
| **멀티파트 처리** | `multipartData()`, `BodyExtractors.toMultipartData()`로 파일 업로드 처리 |
| **어노테이션 vs 함수형** | 같은 애플리케이션에 공존 가능, 상황에 따라 적합한 방식 선택 |

다음 장에서는 MongoDB 리액티브 데이터 접근을 심화하여, `ReactiveMongoTemplate`, 커스텀 쿼리, Aggregation Pipeline, 변경 스트림 등을 다룬다.
# Chapter 8. MongoDB 리액티브 데이터 접근 심화

Chapter 6에서 `ReactiveMongoRepository`를 활용한 기본 CRUD를 구현했다. 이번 장에서는 `ReactiveMongoTemplate`을 중심으로 MongoDB의 고급 기능을 리액티브 방식으로 활용하는 방법을 다룬다. Criteria API를 이용한 동적 쿼리, Aggregation Pipeline을 활용한 통계 API, Change Streams를 이용한 실시간 데이터 감시, 트랜잭션 처리, 그리고 인덱스 관리와 쿼리 성능 최적화까지 실전에서 필요한 심화 주제를 집중적으로 살펴본다.

---

## 8.1 ReactiveMongoTemplate 활용

### 8.1.1 ReactiveMongoTemplate vs ReactiveMongoRepository

Chapter 6에서 사용한 `ReactiveMongoRepository`는 메서드 이름 기반 쿼리 자동 생성, 기본 CRUD 메서드 제공 등 편리한 추상화를 제공한다. 그러나 복잡한 쿼리, 부분 업데이트, Aggregation, Change Streams 등 고급 기능을 사용하려면 `ReactiveMongoTemplate`이 필요하다.

| 비교 항목 | ReactiveMongoRepository | ReactiveMongoTemplate |
|-----------|------------------------|----------------------|
| **추상화 수준** | 높음 (인터페이스 선언만으로 사용) | 낮음 (직접 Query/Update 객체 구성) |
| **기본 CRUD** | 자동 제공 | 직접 구현 |
| **부분 업데이트** | 미지원 (전체 도큐먼트 교체) | `Update` 객체로 특정 필드만 수정 |
| **Upsert / Aggregation** | 미지원 | `upsert()`, `aggregate()` 제공 |
| **Change Streams** | 미지원 | `changeStream()` 메서드 제공 |
| **동적 쿼리** | 제한적 (`@Query` + SpEL) | `Criteria`로 자유롭게 조합 |

실무에서는 두 가지를 함께 사용하는 경우가 많다. 간단한 CRUD는 `ReactiveMongoRepository`로 처리하고, 복잡한 쿼리나 고급 기능이 필요한 부분에서 `ReactiveMongoTemplate`을 사용한다.

### 8.1.2 ReactiveMongoTemplate 기본 CRUD

`ReactiveMongoTemplate`은 Spring Boot의 자동 설정에 의해 빈으로 등록된다. 별도의 설정 없이 주입받아 사용할 수 있다.

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

`Query` 객체는 MongoDB 쿼리 조건을, `Update` 객체는 수정할 필드와 값을 지정한다.

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

`upsert`는 조건에 맞는 도큐먼트가 있으면 업데이트하고, 없으면 새로 삽입하는 원자적 연산이다. `findAndModify()`는 도큐먼트를 찾아 수정하고 결과를 반환하는 원자적 연산이다.

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

`Criteria`는 MongoDB 쿼리 조건을 빌더 패턴으로 구성하는 클래스다.

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

실무에서는 사용자의 검색 조건에 따라 쿼리를 동적으로 구성해야 하는 경우가 많다.

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

MongoDB Aggregation Pipeline은 도큐먼트를 여러 단계(stage)에 걸쳐 변환하고 집계하는 프레임워크다. Spring Data MongoDB는 `Aggregation` 클래스를 통해 파이프라인을 구성하고, `ReactiveMongoTemplate.aggregate()`로 실행한다.

| 단계 | MongoDB 연산자 | Spring Data 메서드 | 설명 |
|------|---------------|-------------------|------|
| Match | `$match` | `Aggregation.match()` | 도큐먼트 필터링 |
| Group | `$group` | `Aggregation.group()` | 그룹별 집계 |
| Sort | `$sort` | `Aggregation.sort()` | 결과 정렬 |
| Project | `$project` | `Aggregation.project()` | 필드 선택/변환 |
| Unwind | `$unwind` | `Aggregation.unwind()` | 배열 분해 |
| Lookup | `$lookup` | `Aggregation.lookup()` | 컬렉션 조인 |

### 8.3.2 기본 집계: 카테고리별 통계

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

`TypedAggregation`은 입력 타입을 명시하여 컬렉션 이름을 `@Document` 어노테이션에서 자동 추론한다. `Aggregation.newAggregation(Product.class, ...)`처럼 첫 번째 인자로 도메인 클래스를 전달하면, `aggregate()` 호출 시 컬렉션 이름을 생략할 수 있다.

### 8.3.4 Unwind와 Lookup

**Unwind**는 배열 필드를 개별 도큐먼트로 분해한다. **Lookup**은 다른 컬렉션과 조인한다.

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

MongoDB Change Streams는 컬렉션의 데이터 변경(삽입, 수정, 삭제)을 실시간으로 감시하는 기능이다. 내부적으로 oplog를 기반으로 동작하며, **Replica Set 또는 Sharded Cluster 환경에서만 사용할 수 있다**. 실시간 알림, 이벤트 발행, 데이터 동기화, 캐시 무효화 등에 활용된다.

### 8.4.2 ReactiveMongoTemplate으로 Change Streams 구독

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

`returnFullDocumentOnUpdate()`를 호출하면 UPDATE 이벤트 시 전체 도큐먼트를 수신한다. 이 옵션이 없으면 변경된 필드 정보만 포함된다.

### 8.4.3 Change Streams + SSE 연동

Change Streams를 Server-Sent Events와 결합하면 클라이언트에게 실시간 알림을 전달할 수 있다.

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

Change Streams는 `resume token`을 제공하여 연결이 끊어진 후 마지막 이벤트부터 다시 수신할 수 있다.

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

`ResumeTokenStore`는 resume token을 MongoDB에 저장/조회하는 컴포넌트로, `upsert`를 사용하여 구현한다. 이벤트를 처리할 때마다 토큰을 저장해두면 애플리케이션 재시작 후에도 유실 없이 이벤트를 이어서 수신할 수 있다.

---

## 8.5 트랜잭션 처리 (ReactiveMongoTransactionManager)

### 8.5.1 MongoDB 트랜잭션의 전제 조건

MongoDB 트랜잭션은 **Replica Set 환경에서만 사용할 수 있다**. Docker Compose로 단일 노드 Replica Set을 구성하면 개발 환경에서도 트랜잭션을 테스트할 수 있다.

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

서비스 메서드에 `@Transactional`을 붙이면 리액티브 환경에서도 트랜잭션이 동작한다. 예외 발생 시 모든 연산이 자동 롤백된다.

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

`TransactionalOperator`를 사용하면 트랜잭션 경계를 프로그래밍 방식으로 제어할 수 있다.

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

Spring Data MongoDB의 `@Indexed`로 단일 필드 인덱스를 선언한다.

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

여러 필드를 조합한 복합 인덱스는 `@CompoundIndex`로 선언한다.

```java
@Document(collection = "products")
@CompoundIndex(name = "category_price_idx", def = "{'category': 1, 'price': -1}")
@CompoundIndex(name = "category_active_created_idx",
               def = "{'category': 1, 'active': 1, 'createdAt': -1}")
public class Product { /* ... */ }
```

복합 인덱스 필드 순서는 **ESR (Equality, Sort, Range) 규칙**을 따르면 최적이다.

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

TTL 인덱스는 지정된 시간이 지나면 도큐먼트를 자동 삭제한다. 세션, 임시 토큰, 로그에 적합하다.

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

`ReactiveMongoTemplate`의 `indexOps()`를 사용하면 애플리케이션 시작 시 프로그래밍 방식으로 인덱스를 생성할 수 있다. Partial Index는 특정 조건을 만족하는 도큐먼트에만 인덱스를 적용하여 저장 공간과 쓰기 성능을 절약한다.

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

인덱스가 제대로 활용되는지 확인하려면 `explain()`으로 실행 계획을 분석한다. `ReactiveMongoTemplate`에서 네이티브 컬렉션을 가져와 `explain()`을 호출하고, 결과의 `queryPlanner.winningPlan.stage`가 `IXSCAN`(인덱스 스캔)인지 확인한다. `COLLSCAN`(컬렉션 풀 스캔)이라면 인덱스 추가가 필요하다. 또한 `totalDocsExamined`와 `nReturned`가 가까울수록 인덱스 효율이 좋다.

### 8.6.6 인덱스 설계 실무 가이드라인

1. **가장 자주 실행되는 쿼리부터 인덱스를 설계한다.** 모든 필드에 인덱스를 걸 필요는 없다.
2. **복합 인덱스는 ESR 규칙을 따른다.** Equality, Sort, Range 순서로 필드를 배치한다.
3. **인덱스는 쓰기 성능에 영향을 준다.** INSERT/UPDATE마다 인덱스 갱신이 필요하므로 불필요한 인덱스는 제거한다.
4. **Covered Query를 활용한다.** 필요한 모든 필드가 인덱스에 포함되면 도큐먼트를 읽지 않고 결과를 반환한다.
5. **Partial Index로 인덱스 크기를 줄인다.** 조건을 만족하는 도큐먼트에만 인덱스를 적용한다.

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

다음 장에서는 데이터 검증과 예외 처리를 다루며, Bean Validation, 커스텀 Validator, 글로벌 예외 처리, 에러 응답 표준화 등을 살펴본다.


---

# Chapter 9. 데이터 검증과 예외 처리

Chapter 8에서 MongoDB 데이터 접근을 심화했다면, 이번 장에서는 클라이언트로부터 유입되는 데이터의 **검증**과 애플리케이션 전반의 **예외 처리**를 다룬다. 올바르지 않은 입력은 가능한 한 빨리 걸러내야 하며, 예외가 발생했을 때는 일관된 형식으로 클라이언트에 전달해야 한다. Bean Validation, 커스텀 Validator, `@ControllerAdvice`, `ErrorWebExceptionHandler`, 그리고 RFC 7807 기반 Problem Details까지 단계별로 살펴본다.

---

## 9.1 Bean Validation을 활용한 입력 검증

### 9.1.1 의존성 추가

Spring Boot에서 Bean Validation을 사용하려면 `spring-boot-starter-validation` 의존성이 필요하다.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

이 스타터는 Hibernate Validator를 포함하며, Jakarta Bean Validation 3.0 API(`jakarta.validation` 패키지)를 제공한다.

### 9.1.2 주요 검증 어노테이션

자주 사용하는 Bean Validation 어노테이션을 정리한다.

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

Chapter 6에서 사용한 사용자 등록 DTO에 검증 로직을 추가한다.

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

상품 생성 DTO에도 동일하게 적용한다.

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

WebFlux 어노테이션 기반 컨트롤러에서는 `@Valid`를 `@RequestBody`와 함께 사용한다.

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

`@Valid`가 선언된 파라미터에서 검증이 실패하면, Spring WebFlux는 `WebExchangeBindException`을 발생시킨다. 이 예외는 9.3절에서 글로벌 예외 처리기로 가공하여 클라이언트에 반환한다.

### 9.1.5 함수형 엔드포인트에서의 검증

함수형 엔드포인트에서는 `@Valid`를 직접 사용할 수 없다. `Validator`를 주입받아 수동으로 검증을 수행한다.

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

`ConstraintViolation`이 발견되면 `ConstraintViolationException`을 던지며, 이 예외도 글로벌 예외 처리기에서 일괄 처리한다.

---

## 9.2 커스텀 Validator 구현

### 9.2.1 커스텀 어노테이션 정의

표준 어노테이션으로 표현하기 어려운 비즈니스 규칙은 커스텀 Validator로 구현한다. 허용된 카테고리 값만 받아들이는 검증기를 만들어 보자.

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

`ConstraintValidator<A, T>` 인터페이스를 구현한다. `A`는 어노테이션 타입, `T`는 검증 대상 필드 타입이다.

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

DTO에 적용하면 다음과 같다.

```java
@AllowedCategory(
    values = {"ELECTRONICS", "BOOKS", "CLOTHING", "FOOD"},
    message = "카테고리는 ELECTRONICS, BOOKS, CLOTHING, FOOD 중 하나여야 합니다"
)
@NotBlank(message = "카테고리는 필수 입력 항목입니다")
private String category;
```

### 9.2.3 크로스 필드 검증 (클래스 레벨 Validator)

비밀번호와 비밀번호 확인이 일치하는지처럼, 두 개 이상의 필드를 함께 검증해야 하는 경우에는 **클래스 레벨 어노테이션**을 사용한다.

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

검증 대상 DTO가 구현할 인터페이스를 먼저 정의한다.

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

DTO 클래스에 `@PasswordMatch`를 선언하면 필드 레벨 검증과 크로스 필드 검증이 모두 수행된다.

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

비즈니스 로직에서 발생하는 예외를 명확하게 구분하기 위해 커스텀 예외 계층을 정의한다.

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

에러 코드를 열거형으로 관리하면 에러 종류를 중앙에서 일관되게 유지할 수 있다.

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

클라이언트에 반환할 에러 응답 형식을 정의한다.

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

`@RestControllerAdvice`는 `@ControllerAdvice`와 `@ResponseBody`의 조합이다. 모든 컨트롤러에서 발생하는 예외를 한 곳에서 처리한다.

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

리액티브 파이프라인 안에서 `switchIfEmpty`와 `Mono.error`를 조합하여 예외를 전파한다.

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

전파된 예외는 `GlobalExceptionHandler`가 캐치하여 적절한 HTTP 응답으로 변환한다.

### 9.3.6 에러 응답 예시

검증 실패 시 클라이언트가 받는 응답은 다음과 같다.

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

리소스를 찾지 못한 경우는 다음과 같다.

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

`@RestControllerAdvice`는 어노테이션 기반 컨트롤러에서 잘 동작하지만, 함수형 엔드포인트(`RouterFunction`)에서 발생하는 예외는 처리하지 못하는 경우가 있다. 특히 라우팅 전에 발생하는 예외나 필터 단계의 예외는 `@ExceptionHandler`의 범위 밖이다. WebFlux에서 모든 예외를 통합 처리하려면 `ErrorWebExceptionHandler`를 사용한다.

### 9.4.2 AbstractErrorWebExceptionHandler 확장

Spring Boot의 `AbstractErrorWebExceptionHandler`를 확장하면 기본 에러 처리를 커스터마이징할 수 있다. 핵심은 `getRoutingFunction()`을 오버라이드하여 모든 에러 요청을 커스텀 렌더 메서드로 보내는 것이다.

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

`@Order(-2)`를 설정한 이유는 기본 `DefaultErrorWebExceptionHandler`가 `@Order(-1)`이기 때문이다. 두 방식을 함께 사용할 수 있으며, 처리 순서는 다음과 같다.

| 단계 | 처리 주체 | 대상 |
|------|----------|------|
| 1 | `@ExceptionHandler` | 어노테이션 컨트롤러에서 발생한 예외 |
| 2 | `ErrorWebExceptionHandler` | 1단계에서 처리되지 않은 모든 예외 |

어노테이션 기반 API에서는 `@RestControllerAdvice`가 예외를 잡고, 함수형 엔드포인트나 필터에서 발생한 예외는 `ErrorWebExceptionHandler`가 처리하는 구조를 권장한다. 두 방식의 에러 응답 형식을 반드시 통일해야 한다.

---

## 9.5 에러 응답 표준화 (Problem Details)

### 9.5.1 RFC 7807이란?

RFC 7807(Problem Details for HTTP APIs)은 HTTP API에서 에러 응답의 표준 형식을 정의한 규격이다.

| 필드 | 설명 |
|------|------|
| `type` | 에러 유형을 식별하는 URI |
| `title` | 에러의 짧은 요약 |
| `status` | HTTP 상태 코드 |
| `detail` | 에러의 상세 설명 |
| `instance` | 에러가 발생한 구체적 URI |

Content-Type은 `application/problem+json`을 사용한다.

### 9.5.2 Spring Framework 6의 ProblemDetail

Spring Framework 6부터는 `ProblemDetail` 클래스를 기본 제공한다. `setProperty()`로 확장 필드를 추가할 수 있다.

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

9.3절의 `GlobalExceptionHandler`를 `ProblemDetail`을 반환하도록 리팩터링한다. 반환 타입을 `ResponseEntity<ErrorResponse>` 대신 `ProblemDetail`로 변경하면 된다.

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

검증 실패 시 응답은 `application/problem+json` 타입으로 반환된다.

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

비즈니스 예외 응답은 다음과 같다.

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

Spring Boot 3에서 `ProblemDetail`을 완전히 활성화하려면 `application.yml`에 다음 설정을 추가한다.

```yaml
spring:
  webflux:
    problemdetails:
      enabled: true
```

이 설정을 활성화하면 Spring이 기본으로 처리하는 예외(404 Not Found, 405 Method Not Allowed 등)도 `ProblemDetail` 형식으로 반환된다.

### 9.5.6 ErrorWebExceptionHandler에서 ProblemDetail 사용

9.4절의 `ErrorWebExceptionHandler`에서도 `ProblemDetail` 형식을 적용할 수 있다. `renderErrorResponse` 메서드에서 `Map` 대신 `ProblemDetail`을 생성하고, Content-Type을 `MediaType.APPLICATION_PROBLEM_JSON`으로 설정하면 된다.

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

`APPLICATION_PROBLEM_JSON`을 사용하면 Content-Type이 `application/problem+json`으로 설정되어 RFC 7807 표준을 온전히 준수한다.

---

## 요약

이번 장에서 다룬 핵심 내용을 정리한다.

| 주제 | 핵심 내용 |
|------|----------|
| **Bean Validation** | `@NotBlank`, `@Email`, `@Pattern` 등으로 DTO 필드를 선언적으로 검증, 컨트롤러에서 `@Valid`로 활성화 |
| **커스텀 Validator** | `ConstraintValidator` 구현으로 비즈니스 규칙 검증, 클래스 레벨 어노테이션으로 크로스 필드 검증 |
| **@RestControllerAdvice** | `@ExceptionHandler`로 예외 유형별 처리, `ErrorResponse` DTO로 일관된 응답 반환 |
| **ErrorWebExceptionHandler** | `AbstractErrorWebExceptionHandler` 확장으로 함수형 엔드포인트 포함 모든 예외 통합 처리 |
| **Problem Details** | RFC 7807 기반 `ProblemDetail` 클래스로 에러 응답 표준화, `application/problem+json` 타입 사용 |

다음 장에서는 WebFlux 필터와 인터셉터를 다루며, `WebFilter`, `HandlerFilterFunction`을 활용한 요청/응답 로깅, CORS 설정, 요청 속도 제한 등을 살펴본다.


---

# Chapter 10. WebFlux 필터와 인터셉터

Chapter 9에서 데이터 검증과 예외 처리를 다루었다. 이번 장에서는 요청과 응답의 **횡단 관심사(cross-cutting concerns)**를 처리하는 필터와 인터셉터를 살펴본다. Spring MVC의 `Filter`와 `HandlerInterceptor`에 대응하는 WebFlux의 `WebFilter`와 `HandlerFilterFunction`을 구현하고, 로깅, CORS, 속도 제한까지 실전에서 자주 사용하는 패턴을 모두 다룬다.

---

## 10.1 WebFilter 구현

### 10.1.1 WebFilter 인터페이스 이해

`WebFilter`는 Spring WebFlux에서 모든 HTTP 요청에 대해 공통 로직을 실행할 수 있는 서블릿 필터 대응 인터페이스다. 어노테이션 기반 컨트롤러와 함수형 엔드포인트 모두에 적용된다.

```java
public interface WebFilter {
    Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain);
}
```

| 파라미터 | 설명 |
|---------|------|
| `ServerWebExchange` | HTTP 요청(`ServerHttpRequest`)과 응답(`ServerHttpResponse`)을 모두 담고 있는 컨텍스트 객체 |
| `WebFilterChain` | 다음 필터 또는 핸들러로 요청을 전달하는 체인 |

핵심 원리는 **필터 체인** 패턴이다. 각 필터는 `chain.filter(exchange)`를 호출하여 다음 단계로 요청을 넘기고, 반환값인 `Mono<Void>`에 연산자를 체이닝하여 응답 후처리를 수행한다.

```
[클라이언트] → [WebFilter 1] → [WebFilter 2] → ... → [핸들러]
                                                         ↓
[클라이언트] ← [WebFilter 1] ← [WebFilter 2] ← ... ← [응답]
```

### 10.1.2 요청 전후 처리 필터

`@Component`로 등록하면 스프링이 자동으로 필터 체인에 추가한다. `chain.filter()` 호출 전후로 코드를 배치하여 요청과 응답 양쪽을 처리할 수 있다.

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

여러 WebFilter가 등록된 경우 `@Order` 어노테이션으로 실행 순서를 제어한다. 값이 작을수록 먼저 실행된다.

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

WebFilter는 기본적으로 **모든 요청**에 적용된다. 특정 경로에만 필터를 적용하려면 내부에서 경로를 확인하고, 요청을 차단하려면 `chain.filter()`를 호출하지 않고 응답을 즉시 완료한다.

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

필터에서 설정한 데이터를 다운스트림 핸들러로 전달할 때 `ServerWebExchange`의 속성을 활용한다.

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

`HandlerFilterFunction`은 **함수형 엔드포인트(RouterFunction)** 전용 필터다.

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

`RouterFunction`의 `filter()` 메서드에 람다로 필터를 전달한다.

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

실제 프로젝트에서 자주 사용하는 인증 필터를 `HandlerFilterFunction`으로 구현한다.

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

라우터에서 공개 API와 보호된 API를 분리하여 인증 필터를 선택적으로 적용한다.

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

인증 필터를 확장하여 역할(Role) 기반 인가 필터도 구현할 수 있다. 여러 필터를 체이닝하면 인증 -> 인가 순서로 적용된다.

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

운영 환경에서 요청 정보를 체계적으로 기록하는 로깅 필터를 구현한다.

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

응답 바디는 스트림 형태이므로 직접 읽을 수 없다. `ServerHttpResponseDecorator`로 `writeWith`를 오버라이드하여 쓰기 시점에 바이트를 가로채 기록한다.

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

리액티브 환경에서는 스레드가 수시로 전환되므로 기존 `MDC`가 정상 작동하지 않는다. Reactor의 **Context**를 활용하여 추적 ID를 전파한다.

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

브라우저는 **동일 출처 정책(Same-Origin Policy)**을 적용한다. 프런트엔드(`http://localhost:3000`)에서 백엔드(`http://localhost:8080`)를 호출하면 출처가 다르므로 CORS 에러가 발생한다. 서버에서 적절한 CORS 헤더를 응답에 포함해야 한다.

| CORS 헤더 | 설명 |
|-----------|------|
| `Access-Control-Allow-Origin` | 허용할 출처 |
| `Access-Control-Allow-Methods` | 허용할 HTTP 메서드 |
| `Access-Control-Allow-Headers` | 허용할 요청 헤더 |
| `Access-Control-Allow-Credentials` | 쿠키/인증 정보 포함 허용 여부 |
| `Access-Control-Max-Age` | Preflight 요청 캐시 시간(초) |

### 10.4.2 WebFluxConfigurer를 이용한 글로벌 설정

가장 권장되는 방법으로, 모든 엔드포인트에 일괄 적용된다.

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

컨트롤러 또는 개별 메서드 레벨에서 세밀하게 CORS를 설정할 수 있다. 클래스 레벨과 메서드 레벨 설정이 동시에 존재하면 **병합**된다.

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

함수형 엔드포인트에는 `@CrossOrigin`을 사용할 수 없다. `CorsWebFilter`를 빈으로 등록하면 어노테이션 기반과 함수형 모두에 적용된다.

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

개발과 운영 환경마다 허용 출처가 다른 경우 `application.yml` 프로파일과 `@Value`를 조합한다.

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

가장 널리 사용되는 속도 제한 알고리즘이다.

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

**Bucket4j**는 토큰 버킷 알고리즘의 Java 구현체로, 스레드 안전하며 성능이 뛰어나다. `build.gradle.kts`에 의존성을 추가한다: `implementation("com.bucket4j:bucket4j-core:8.10.1")`

### 10.5.3 IP 기반 속도 제한 필터

클라이언트 IP별로 독립적인 버킷을 관리하는 필터를 구현한다.

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

인증된 사용자별로 등급(plan)에 따라 다른 제한을 적용한다. 핵심은 `Plan` enum으로 등급별 정책을 정의하고, 사용자 ID와 등급을 조합한 키로 버킷을 관리하는 것이다.

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

로그인 API처럼 브루트포스 공격에 취약한 엔드포인트에는 `HandlerFilterFunction`으로 더 엄격한 제한을 적용한다.

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

`ConcurrentHashMap`에 IP별 버킷이 무한히 쌓이면 메모리 누수가 발생한다. Caffeine 캐시를 사용하면 자동 만료를 쉽게 구현할 수 있다.

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

**설계 원칙**:
- **글로벌 관심사**(로깅, 추적 ID, CORS)에는 `WebFilter`를 사용한다.
- **특정 API 그룹에만 적용할 로직**(인증, 인가, 속도 제한)에는 `HandlerFilterFunction`을 사용한다.
- 필터 순서(`@Order`)는 명시적으로 관리하여 의도하지 않은 동작을 방지한다.
- 응답 바디 로깅처럼 성능에 영향을 주는 필터는 조건부로 활성화한다.

다음 Chapter 11에서는 **Spring Security WebFlux**를 활용하여 본격적인 인증과 인가를 구현한다. 이번 장에서 직접 구현한 인증 필터가 Spring Security의 `SecurityWebFilterChain`으로 어떻게 대체되고 확장되는지 비교해 볼 것이다.


---

# Chapter 11. 리액티브 보안 (Spring Security WebFlux)

Spring WebFlux 기반 애플리케이션에서 보안은 서블릿 기반의 Spring Security와 다른 아키텍처로 동작한다. 이번 장에서는 리액티브 환경에 맞는 Spring Security 설정, 인증/인가 구현, JWT 기반 인증, SecurityContext 관리, 그리고 OAuth2 연동까지 단계별로 다룬다.

---

## 11.1 Spring Security Reactive 설정

### 11.1.1 의존성 추가

`build.gradle`에 Spring Security 의존성을 추가한다.

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

의존성을 추가하는 것만으로 Spring Security가 활성화되며, 모든 엔드포인트에 기본 인증이 적용된다.

### 11.1.2 서블릿 기반과의 차이

| 구분 | Servlet (Spring MVC) | Reactive (Spring WebFlux) |
|------|---------------------|--------------------------|
| **필터 체인** | `SecurityFilterChain` | `SecurityWebFilterChain` (`WebFilter`) |
| **설정 빌더** | `HttpSecurity` | `ServerHttpSecurity` |
| **인증 저장소** | `SecurityContextHolder` (ThreadLocal) | `ReactiveSecurityContextHolder` (Reactor Context) |
| **UserDetailsService** | `UserDetailsService` | `ReactiveUserDetailsService` |
| **인증 매니저** | `AuthenticationManager` | `ReactiveAuthenticationManager` |
| **메서드 보안** | `@EnableMethodSecurity` | `@EnableReactiveMethodSecurity` |

가장 중요한 차이는 **SecurityContext 저장 방식**이다. 서블릿 환경에서는 `ThreadLocal`에 인증 정보를 저장하지만, 리액티브 환경에서는 하나의 요청이 여러 스레드에서 처리될 수 있으므로 **Reactor의 Context**를 사용한다.

### 11.1.3 기본 보안 설정 클래스

`@EnableWebFluxSecurity`로 리액티브 보안을 활성화하고, `SecurityWebFilterChain` 빈을 정의한다.

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

`Customizer.withDefaults()`는 Spring Security 6.1부터 권장되는 설정 방식이다.

---

## 11.2 SecurityWebFilterChain 구성

### 11.2.1 ServerHttpSecurity 주요 설정

`ServerHttpSecurity`는 리액티브 보안 설정의 빌더 역할을 한다.

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

`authorizeExchange`에서 사용할 수 있는 다양한 매처와 접근 규칙을 정리한다.

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

REST API 서버에서는 일반적으로 CSRF를 비활성화한다. 브라우저 기반 애플리케이션에서는 쿠키 기반 CSRF 토큰을 사용한다.

```java
// REST API: CSRF 비활성화
.csrf(csrf -> csrf.disable())

// 브라우저 기반: 쿠키 CSRF 토큰
.csrf(csrf -> csrf
    .csrfTokenRepository(CookieServerCsrfTokenRepository.withHttpOnlyFalse()))
```

CORS는 `CorsConfigurationSource` 빈으로 설정한다.

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

리액티브 환경에서는 `ReactiveUserDetailsService`를 구현한다. `findByUsername()`이 `Mono<UserDetails>`를 반환한다. 먼저 사용자 도메인 모델과 리포지토리를 정의한다.

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

MongoDB 기반 `ReactiveUserDetailsService` 구현체를 작성한다.

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

비밀번호는 BCrypt로 해시하여 저장한다.

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

`@EnableReactiveMethodSecurity`를 활성화하면 서비스 계층에서 메서드 단위 보안을 적용할 수 있다.

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

리액티브 환경에서 `@PreAuthorize`는 `Mono`/`Flux` 반환 타입과 함께 동작하며, 인가 실패 시 `AccessDeniedException`이 발생한다.

---

## 11.4 JWT 기반 인증 구현

REST API 환경에서는 세션 대신 JWT(JSON Web Token)를 사용하여 무상태(stateless) 인증을 구현하는 것이 일반적이다. JWT는 Header(알고리즘, 타입), Payload(클레임), Signature(서명) 세 부분으로 구성된다.

### 11.4.1 JWT 유틸리티 클래스

jjwt 라이브러리를 사용하여 토큰 생성, 검증, 파싱을 담당하는 클래스를 구현한다.

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

JWT 토큰에서 `Authentication` 객체를 생성하는 컨버터와 `ReactiveAuthenticationManager`를 구현한다.

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

JWT 기반 인증을 위한 전체 보안 설정을 구성한다.

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

`NoOpServerSecurityContextRepository`를 설정하여 서버 측 세션을 생성하지 않는 완전한 무상태 구조를 만든다.

### 11.4.4 인증 컨트롤러

로그인, 토큰 갱신, 회원가입 엔드포인트를 구현한다.

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

요청/응답 DTO를 정의한다.

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

JWT 기반 인증의 전체 흐름을 정리한다.

1. **회원가입**: `POST /api/auth/signup` -- 비밀번호 BCrypt 인코딩 후 MongoDB 저장
2. **로그인**: `POST /api/auth/login` -- 비밀번호 검증 후 Access Token + Refresh Token 발급
3. **인증된 API 호출**: `Authorization: Bearer <accessToken>` 헤더 전송 -- `JwtAuthenticationConverter`가 토큰 추출/검증 후 `Authentication` 객체 생성
4. **토큰 갱신**: `POST /api/auth/refresh` -- Refresh Token 검증 후 새 Access Token 발급

---

## 11.5 리액티브 환경에서의 SecurityContext 관리

### 11.5.1 ReactiveSecurityContextHolder

서블릿 환경의 `SecurityContextHolder.getContext()`는 `ThreadLocal` 기반이므로 리액티브 환경에서 사용할 수 없다.

```java
// 리액티브 환경에서의 올바른 방식
Mono<String> username = ReactiveSecurityContextHolder.getContext()
    .map(SecurityContext::getAuthentication)
    .map(Authentication::getName);
```

### 11.5.2 현재 사용자 정보 가져오기

서비스 계층에서 현재 인증된 사용자 정보를 활용하는 패턴을 살펴본다.

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

어노테이션 기반 컨트롤러에서는 `@AuthenticationPrincipal`이나 `Mono<Principal>`을 파라미터로 주입받을 수 있다.

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

`ReactiveSecurityContextHolder.getContext()`의 반환값은 반드시 리액티브 체인 안에서 `map`/`flatMap`으로 연결해야 한다. Reactor의 `Context`는 구독 시점에 전파되므로, 체인이 끊기면 `SecurityContext`를 읽을 수 없다.

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

`application.yml`에 OAuth2 클라이언트를 등록한다.

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

Google은 OpenID Connect를 지원하므로 `provider` 설정이 자동 적용된다. GitHub은 `user-name-attribute`를 수동 지정해야 한다.

### 11.6.2 OAuth2 SecurityWebFilterChain 설정

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

`oauth2Login(Customizer.withDefaults())`만으로 `/oauth2/authorization/{registrationId}` 엔드포인트와 콜백 URL이 자동 설정된다.

### 11.6.3 OAuth2 사용자 정보 커스터마이징

소셜 로그인 후 사용자 정보를 MongoDB에 저장하려면 `ReactiveOAuth2UserService`를 커스터마이징한다.

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

외부 인증 서버(Keycloak, Auth0 등)에서 발급한 JWT를 검증하는 Resource Server 설정이다.

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
| 단일 애플리케이션, 자체 인증 | JWT 자체 발급 (11.4) |
| 마이크로서비스, 중앙 인증 서버 존재 | OAuth2 Resource Server |
| 소셜 로그인이 필요한 웹 애플리케이션 | OAuth2 Login |
| SPA + API 서버 분리 구조 | JWT 자체 발급 또는 OAuth2 + PKCE |

---

## 요약

이번 장에서 다룬 핵심 내용을 정리한다.

| 주제 | 핵심 내용 |
|------|----------|
| **리액티브 보안 설정** | `@EnableWebFluxSecurity`, `SecurityWebFilterChain`, 서블릿 방식과의 차이 |
| **SecurityWebFilterChain** | `ServerHttpSecurity`로 경로별 인가, CSRF, CORS, 인증 방식 설정 |
| **인증과 인가** | `ReactiveUserDetailsService`, `PasswordEncoder`, `@PreAuthorize` 메서드 보안 |
| **JWT 인증** | `JwtTokenProvider`로 토큰 생성/검증, `AuthenticationWebFilter`로 필터 체인 통합 |
| **SecurityContext** | `ReactiveSecurityContextHolder`로 인증 정보 접근, 리액티브 체인 내부에서만 사용 |
| **OAuth2 연동** | OAuth2 Login(소셜 로그인), Resource Server(외부 JWT 검증), 사용자 정보 커스터마이징 |

다음 장에서는 Server-Sent Events(SSE)를 활용한 실시간 데이터 스트리밍을 다룬다.
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
# Chapter 18. 모니터링과 관측 가능성

운영 환경에서 리액티브 애플리케이션을 안정적으로 관리하려면 세 가지 관측 가능성(Observability) 축이 필요하다. **메트릭(Metrics)**, **트레이스(Traces)**, **로그(Logs)**다. 전통적인 서블릿 기반 애플리케이션과 달리, WebFlux 애플리케이션은 하나의 요청이 여러 스레드를 넘나들며 처리되므로 `ThreadLocal` 기반의 기존 모니터링 방식만으로는 한계가 있다. 이번 장에서는 Spring Boot Actuator를 기반으로 메트릭을 노출하고, Micrometer와 Prometheus로 수집하며, Grafana로 시각화하는 전체 파이프라인을 구성한다. 나아가 Reactor 스트림 내부의 메트릭 수집, 분산 추적(Zipkin/Jaeger), 그리고 리액티브 환경에서의 구조화된 로깅까지 실전에서 필요한 관측 가능성 전략을 종합적으로 다룬다.

---

## 18.1 Spring Boot Actuator 설정

### 18.1.1 Actuator 소개와 의존성

Spring Boot Actuator는 애플리케이션의 상태, 메트릭, 환경 정보 등을 HTTP 엔드포인트로 노출하는 운영 도구 모듈이다. WebFlux 환경에서도 동일하게 동작하며, 리액티브 기반의 Health Indicator를 제공한다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    implementation 'org.springframework.boot:spring-boot-starter-data-mongodb-reactive'
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
}
```

### 18.1.2 엔드포인트 활성화와 노출 설정

기본적으로 Actuator는 대부분의 엔드포인트를 활성화하지만, HTTP로 노출되는 것은 `health`뿐이다. 운영에 필요한 엔드포인트를 선택적으로 노출한다.

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

MongoDB Reactive 스타터를 사용하면 `ReactiveMongoHealthIndicator`가 자동 등록된다. 자동 감지되지 않는 외부 서비스의 상태를 확인하려면 `ReactiveHealthIndicator`를 직접 구현한다.

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

Actuator 엔드포인트에는 민감한 정보가 포함될 수 있으므로, Spring Security WebFlux와 연동하여 접근을 제한해야 한다.

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

운영 환경에서는 Actuator 포트를 별도로 분리하는 것도 권장된다.

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

이렇게 하면 애플리케이션은 8080 포트에서, Actuator는 9090 포트에서 서비스되므로 방화벽 규칙으로 외부 접근을 차단할 수 있다.

---

## 18.2 Micrometer와 Prometheus 연동

### 18.2.1 Micrometer 소개

Micrometer는 JVM 기반 애플리케이션을 위한 **벤더 중립적 메트릭 파사드**다. SLF4J가 로깅 구현체를 추상화하듯, Micrometer는 Prometheus, Datadog, CloudWatch 등 메트릭 수집 구현체를 추상화한다. Spring Boot Actuator는 내부적으로 Micrometer를 사용한다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
    implementation 'io.micrometer:micrometer-registry-prometheus'
}
```

위 의존성을 추가하면 `/actuator/prometheus` 엔드포인트가 자동으로 활성화된다.

### 18.2.2 자동 수집 메트릭

Spring Boot와 Micrometer는 별도 코드 없이도 다양한 메트릭을 자동 수집한다.

| 카테고리 | 메트릭 예시 | 설명 |
|---------|-----------|------|
| **JVM** | `jvm_memory_used_bytes` | 힙/논힙 메모리 사용량 |
| **JVM** | `jvm_gc_pause_seconds` | GC 일시 정지 시간 |
| **HTTP** | `http_server_requests_seconds` | HTTP 요청 처리 시간 (uri, method, status별) |
| **MongoDB** | `mongodb_driver_pool_size` | MongoDB 커넥션 풀 크기 |
| **MongoDB** | `mongodb_driver_commands_seconds` | MongoDB 명령 실행 시간 |
| **System** | `system_cpu_usage` | 시스템 CPU 사용률 |

### 18.2.3 커스텀 메트릭 -- Counter

`Counter`는 단조 증가하는 값을 추적한다. 주문 건수, 에러 발생 횟수 등을 기록하는 데 적합하다.

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

`Gauge`는 현재 값을 나타낸다. 대기열 크기, 활성 연결 수 등 증감이 모두 가능한 값에 사용한다.

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

`Timer`는 작업의 소요 시간과 호출 횟수를 함께 기록한다. 성능 분석에 필수적이다.

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

Prometheus가 애플리케이션의 메트릭을 주기적으로 스크래핑하도록 설정한다.

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

Docker Compose로 Prometheus를 실행한다. Prometheus UI(`http://localhost:9090`)에서 `up{job="webflux-app"}` 쿼리로 타겟 연결 상태를 확인할 수 있다.

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

기존 `docker-compose-monitoring.yml`에 Grafana를 추가한다.

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

`docker compose -f docker-compose-monitoring.yml up -d`로 실행한 후, `http://localhost:3000`에 접속하여 로그인한다. 프로비저닝 기능으로 Prometheus 데이터소스를 자동 등록한다.

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

Grafana 커뮤니티에서 제공하는 대시보드를 임포트하면 빠르게 모니터링 환경을 구축할 수 있다.

| 대시보드 ID | 이름 | 용도 |
|------------|------|------|
| **4701** | JVM (Micrometer) | JVM 메모리, GC, 스레드 모니터링 |
| **11378** | Spring Boot Statistics | HTTP 요청, 에러율, 응답 시간 |
| **12900** | Spring Boot Observability | 종합 관측 가능성 |

Grafana UI에서 **Dashboards > Import** 메뉴로 이동하여 대시보드 ID를 입력하면 된다.

### 18.3.4 커스텀 대시보드 PromQL 쿼리

프로젝트에 맞는 커스텀 패널을 구성할 때 자주 사용하는 PromQL 쿼리는 다음과 같다.

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

Grafana의 알림 기능으로 이상 상태를 감지하고 Slack, Email, PagerDuty 등으로 알림을 발송한다. Grafana UI의 **Alerting > Alert Rules > New alert rule**에서 생성하며, 주요 설정 항목은 다음과 같다.

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

Reactor는 Micrometer와 통합된 내장 메트릭 기능을 제공한다. 이를 활성화하면 Reactor 파이프라인 내부의 구독 상태, 요청 수, 에러 등을 추적할 수 있다.

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

특정 Reactor 체인에 `.name()`과 `.tag()` 연산자를 사용하여 세밀한 메트릭을 수집한다. `.metrics()`를 체인 끝에 추가하면 해당 시점까지의 메트릭이 Micrometer로 기록된다.

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

이렇게 하면 다음 메트릭이 자동으로 생성된다.

| 메트릭 이름 | 설명 |
|------------|------|
| `reactor.notification.unread.fetch.subscribed` | 구독 횟수 |
| `reactor.notification.unread.fetch.requested` | 요청된 요소 수 |
| `reactor.notification.unread.fetch.onNext.delay` | onNext 신호 간의 지연 시간 |
| `reactor.notification.unread.fetch.flow.duration` | 전체 실행 시간 |

### 18.4.3 Schedulers 메트릭

`Schedulers.enableMetrics()` 호출 후 수집되는 스케줄러 관련 메트릭은 다음과 같다.

| 메트릭 | 설명 |
|--------|------|
| `executor_pool_size_threads` | 현재 스레드 풀 크기 |
| `executor_active_threads` | 활성 스레드 수 |
| `executor_queued_tasks` | 대기열 태스크 수 |
| `executor_completed_tasks_total` | 완료된 태스크 수 |

이름을 부여한 커스텀 스케줄러를 생성하면 스케줄러별로 메트릭을 구분하여 모니터링할 수 있다.

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

마이크로서비스 환경에서 하나의 사용자 요청은 여러 서비스를 거쳐 처리된다. 분산 추적은 이 과정을 **Trace ID**와 **Span ID**로 연결하여 전체 호출 흐름을 시각화한다.

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

Spring Boot 3.x에서는 Micrometer Tracing이 분산 추적의 표준 추상화 계층이다. Brave(Zipkin) 또는 OpenTelemetry 브릿지를 선택할 수 있다.

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

Zipkin은 `docker run -d -p 9411:9411 openzipkin/zipkin`으로 간단히 실행할 수 있다. Jaeger를 사용하는 경우 다음과 같이 설정한다.

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

`WebClient`를 `WebClient.Builder` 빈으로 생성하면 Micrometer Tracing이 자동으로 Trace 전파 필터를 추가한다. 중요한 점은 `WebClient.create()` 대신 반드시 스프링이 관리하는 `WebClient.Builder`를 주입받아 사용해야 한다는 것이다.

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

이렇게 생성한 `WebClient`로 외부 API를 호출하면, Trace ID가 요청 헤더에 자동으로 포함되어 전파된다. Zipkin UI에서 트레이스를 조회하면 MongoDB 조회와 외부 API 호출이 별도의 Span으로 기록되고 동일한 Trace ID로 묶인 것을 확인할 수 있다.

### 18.5.6 커스텀 Span 생성

자동 계측으로 충분하지 않은 경우, `@Observed` 어노테이션으로 메서드 단위 Span을 생성하거나, `Observation` API로 수동 제어한다.

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

운영 환경에서 텍스트 기반 로그는 검색과 집계가 어렵다. ELK(Elasticsearch + Logstash + Kibana)나 Loki 같은 로그 수집 시스템과 연동하려면 **JSON 형식** 로그가 효과적이다.

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

`logstash-logback-encoder`를 사용하여 JSON 형식 로그를 출력한다.

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

전통적인 서블릿 환경에서 MDC는 `ThreadLocal` 기반으로 동작한다. 그러나 리액티브 환경에서는 하나의 요청이 여러 스레드를 넘나들며 처리되므로, `publishOn()`이나 `subscribeOn()`으로 스레드가 전환되면 MDC 값이 유실된다.

Spring Boot 3.x에서는 `context-propagation` 라이브러리와 `Hooks.enableAutomaticContextPropagation()`으로 이 문제를 해결한다. 18.4.1에서 설정한 것처럼 이를 활성화하면 `traceId`와 `spanId`가 자동으로 MDC에 전파된다. 비즈니스 컨텍스트(`userId`, `requestId`)를 추가로 전파하려면 `WebFilter`와 `ThreadLocalAccessor`를 구현한다.

### 18.6.4 커스텀 컨텍스트 전파

`WebFilter`에서 Reactor Context에 값을 저장하고, `ThreadLocalAccessor`를 통해 MDC와 연결한다.

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

`ThreadLocalAccessor`를 구현하여 Reactor Context와 MDC 간의 자동 전파를 설정한다.

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
    public void setValue() { MDC.remove(KEY); }
}
```

`ThreadLocalAccessor` 구현체는 `ContextRegistry`에 등록한다. `requestId`용도 동일한 패턴으로 구현한다.

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

이제 스레드가 전환되더라도 `userId`와 `requestId`가 MDC에 자동 전파되며, JSON 로그에 포함된다.

### 18.6.5 구조화된 로그 작성 패턴

`logstash-logback-encoder`의 `StructuredArguments`를 사용하면 로그 메시지와 JSON 필드를 동시에 기록할 수 있다.

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

| 주제 | 핵심 내용 |
|------|----------|
| **Actuator** | `health`, `info`, `metrics`, `prometheus` 엔드포인트 노출, `ReactiveHealthIndicator`로 논블로킹 상태 확인, 포트 분리와 Security 연동으로 보안 강화 |
| **Micrometer + Prometheus** | `Counter`(단조 증가), `Gauge`(현재 값), `Timer`(소요 시간 + 호출 수) 커스텀 메트릭, `prometheus.yml`로 스크래핑 설정 |
| **Grafana** | Docker 설치, Prometheus 데이터소스 프로비저닝, 커뮤니티 대시보드 임포트, PromQL로 커스텀 패널, 알림 규칙 설정 |
| **리액티브 메트릭** | `.name().tag().metrics()`로 Reactor 체인 메트릭 수집, `Schedulers.enableMetrics()`로 스케줄러 모니터링 |
| **분산 추적** | Micrometer Tracing + Brave(Zipkin) 또는 OpenTelemetry(Jaeger), `WebClient.Builder` 빈으로 자동 Trace 전파, `@Observed`로 커스텀 Span |
| **구조화된 로깅** | `logstash-logback-encoder`로 JSON 로그, `Hooks.enableAutomaticContextPropagation()`으로 Reactor Context-MDC 자동 전파, `ThreadLocalAccessor`로 커스텀 컨텍스트 전파 |

다음 장에서는 리액티브 애플리케이션의 성능을 측정하고 최적화하는 전략을 다룬다. MongoDB 커넥션 풀 튜닝, Netty 이벤트 루프 최적화, 캐싱, BlockHound를 활용한 블로킹 코드 탐지, 그리고 Gatling/k6를 이용한 부하 테스트까지 실전 성능 최적화 기법을 종합적으로 살펴본다.
# Chapter 19. 성능 최적화

리액티브 아키텍처를 도입했다고 해서 자동으로 높은 성능이 보장되는 것은 아니다. 논블로킹 모델의 이점을 실제로 누리려면, 병목 지점을 정확히 측정하고, 커넥션 풀과 이벤트 루프를 애플리케이션 특성에 맞게 조정하며, 캐싱으로 불필요한 I/O를 줄이고, 블로킹 코드를 철저히 제거해야 한다. 이번 장에서는 리액티브 애플리케이션의 **성능 측정 방법**부터 **MongoDB 커넥션 풀 튜닝**, **Netty 이벤트 루프 최적화**, **캐싱 전략**, **BlockHound를 활용한 블로킹 탐지**, 그리고 **Gatling/k6를 활용한 부하 테스트**까지 실전 성능 최적화의 전 과정을 다룬다.

---

## 19.1 리액티브 애플리케이션 성능 측정

성능 최적화의 첫 번째 원칙은 **측정 없이 최적화하지 않는 것**이다. 감에 의존한 최적화는 오히려 코드 복잡도만 높이고 실질적인 개선을 가져오지 못한다.

### 19.1.1 핵심 성능 지표

리액티브 애플리케이션의 성능은 세 가지 축으로 평가한다.

| 지표 | 설명 | 측정 단위 |
|------|------|----------|
| **처리량(Throughput)** | 단위 시간당 처리한 요청 수 | req/sec |
| **지연시간(Latency)** | 요청 시작부터 응답 완료까지 소요 시간 | ms (p50, p95, p99) |
| **리소스 사용률** | CPU, 메모리, 스레드, 커넥션 점유율 | %, 개수 |

리액티브 애플리케이션은 적은 스레드로 높은 처리량을 달성하는 것이 목표다. 따라서 스레드 수 대비 처리량 비율이 중요한 평가 기준이 된다. 지연시간은 단순 평균보다 백분위(p95, p99)를 기준으로 판단해야 실제 사용자 경험을 반영할 수 있다.

```
[전통적 MVC 모델]
스레드 200개 → 동시 처리 200 요청 → 처리량 ~2,000 req/sec

[리액티브 모델]
스레드 8개(이벤트 루프) → 동시 처리 수천 요청 → 처리량 ~10,000+ req/sec
```

### 19.1.2 Micrometer 메트릭 활용

Chapter 18에서 설정한 Micrometer 메트릭을 성능 분석에 활용한다. WebFlux 애플리케이션에서 자동 수집되는 핵심 메트릭은 다음과 같다.

| 메트릭 이름 | 설명 |
|------------|------|
| `http.server.requests` | HTTP 요청 처리 시간 (타이머) |
| `reactor.netty.http.server.data.received` | 서버가 수신한 데이터 바이트 |
| `mongodb.driver.pool.size` | MongoDB 커넥션 풀 크기 |
| `mongodb.driver.pool.waitqueuesize` | MongoDB 커넥션 대기 큐 크기 |
| `jvm.threads.live` | 활성 JVM 스레드 수 |

커스텀 메트릭을 추가하여 비즈니스 로직의 성능도 측정할 수 있다.

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

JMH(Java Microbenchmark Harness)는 JVM 수준의 정밀한 벤치마크 도구다. `build.gradle`에 JMH 플러그인을 추가한다.

```groovy
plugins {
    id 'me.champeau.jmh' version '0.7.2'
}

dependencies {
    jmh 'org.openjdk.jmh:jmh-core:1.37'
    jmh 'org.openjdk.jmh:jmh-generator-annprocess:1.37'
}
```

Reactor 연산자 체인의 성능을 비교하는 벤치마크 예시를 작성한다.

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
        Flux.fromIterable(items)
            .flatMap(item -> Mono.fromCallable(() -> item.toUpperCase()))
            .collectList()
            .block();
    }

    @Benchmark
    public void map_단순변환(Blackhole bh) {
        Flux.fromIterable(items)
            .map(String::toUpperCase)
            .collectList()
            .block();
    }
}
```

> **참고**: `map`은 동기 변환이므로 `flatMap`보다 훨씬 빠르다. 비동기 I/O가 불필요한 단순 변환에는 항상 `map`을 사용해야 한다.

### 19.1.4 프로파일링 도구

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

리액티브 애플리케이션에서 프로파일링 시 주의할 점은, 이벤트 루프 스레드(`reactor-http-nio-*`)의 CPU 사용률이 80%를 넘으면 병목 가능성이 높다는 것이다. 이 경우 무거운 연산을 별도 스케줄러로 오프로드해야 한다.

---

## 19.2 MongoDB 커넥션 풀 튜닝

MongoDB 드라이버는 내부적으로 커넥션 풀을 관리한다. 풀 크기, 타임아웃, 유휴 커넥션 관리 설정이 처리량에 직접적인 영향을 미친다.

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

`application.yml`의 URI 파라미터 방식보다 `MongoClientSettings` 빈을 직접 구성하면 세밀한 제어가 가능하다.

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

커넥션 풀 크기는 다음 공식을 기준으로 산정한다.

```
최적 풀 크기 = (동시 요청 수) x (평균 쿼리 시간) / (목표 응답 시간)
```

예를 들어, 동시 요청 500건, 평균 쿼리 시간 10ms, 목표 응답 시간 100ms라면 최적 풀 크기는 `500 x 10 / 100 = 50`이다.

| 시나리오 | minSize | maxSize | 근거 |
|----------|---------|---------|------|
| **개발 환경** | 2 | 10 | 리소스 절약 |
| **소규모 서비스** | 5 | 30 | 동시 사용자 ~100명 |
| **중규모 서비스** | 10 | 50 | 동시 사용자 ~1,000명 |
| **대규모 서비스** | 20 | 100 | 동시 사용자 ~10,000명 |

> **주의**: `maxSize`를 무조건 크게 잡으면 MongoDB 서버 측 리소스가 고갈될 수 있다. 모든 애플리케이션 인스턴스의 `maxSize` 합이 MongoDB의 `net.maxIncomingConnections`(기본 65,536)의 80%를 넘지 않도록 한다.

### 19.2.4 커넥션 풀 모니터링과 타임아웃

커넥션 풀 메트릭을 활성화하고, 타임아웃을 계층별로 설정한다.

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

`waitqueuesize`가 지속적으로 0보다 큰 경우, `maxSize`를 늘리거나 쿼리 성능을 개선해야 한다는 신호다. 타임아웃은 다음 계층으로 구성한다.

```
소켓 타임아웃 (connectTimeout, readTimeout)
  └─ 쿼리 타임아웃 (maxTimeMsec)
       └─ Reactor 타임아웃 (timeout 연산자)
            └─ HTTP 응답 타임아웃 (WebFlux 타임아웃)
```

```java
public Flux<Product> findByCategory(String category) {
    Query query = new Query(Criteria.where("category").is(category))
        .maxTimeMsec(5000);  // 쿼리 레벨 타임아웃 (5초)

    return mongoTemplate.find(query, Product.class)
        .timeout(Duration.ofSeconds(10));  // Reactor 레벨 타임아웃
}
```

---

## 19.3 Netty 이벤트 루프 최적화

Spring WebFlux는 Reactor Netty를 기본 서버로 사용하며, Netty의 이벤트 루프 설정이 전체 처리량에 직접적인 영향을 미친다.

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

JVM의 기본 NIO 대신 운영체제의 네이티브 I/O를 사용하면 성능이 개선된다.

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

이벤트 루프 스레드에서 절대로 블로킹 작업을 수행해서는 안 된다. 무거운 연산은 별도의 스케줄러로 오프로드한다.

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

I/O 연산을 줄이는 가장 효과적인 방법은 캐싱이다. 리액티브 애플리케이션에서는 캐시 조회도 논블로킹으로 이루어져야 한다.

### 19.4.1 Caffeine 로컬 캐시

Caffeine은 JVM 기반의 고성능 로컬 캐시 라이브러리다. 리액티브 환경에서 활용하는 래퍼 클래스를 작성한다.

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

서비스에서 캐시를 활용하는 패턴은 다음과 같다.

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

멀티 인스턴스 환경에서는 Reactive Redis를 분산 캐시로 활용한다.

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

로컬 캐시(Caffeine)와 분산 캐시(Redis)를 조합하여 **L1/L2 캐시** 구조를 구성하면 성능과 일관성을 모두 확보할 수 있다.

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

리액티브 애플리케이션에서 가장 위험한 성능 저하 원인은 **이벤트 루프 스레드에서의 블로킹 호출**이다. 단 한 줄의 블로킹 코드가 전체 처리량을 극적으로 떨어뜨릴 수 있다. BlockHound는 이러한 블로킹 호출을 런타임에 자동으로 탐지하는 Java Agent 도구다.

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

리액티브 애플리케이션에서 자주 발견되는 블로킹 코드 패턴과 수정 방법을 정리한다.

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

특정 라이브러리의 블로킹 호출을 허용하거나, 커스텀 탐지 규칙을 추가할 수 있다.

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

StepVerifier와 BlockHound를 결합하여 블로킹 호출을 자동으로 검출하는 테스트를 작성한다.

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

> **참고**: BlockHound는 JVM Agent 방식으로 동작하므로 프로덕션 환경에서는 사용하지 않는다. 오버헤드가 발생하며, 의도적인 블로킹(초기화 등)에서도 예외가 발생할 수 있다. 테스트와 스테이징 환경에서만 활성화한다.

---

## 19.6 부하 테스트 (Gatling, k6)

성능 최적화의 효과를 검증하려면 실제 부하 조건에서 테스트해야 한다.

### 19.6.1 Gatling 부하 테스트

Gatling은 Scala 기반의 고성능 부하 테스트 도구다. Java DSL로도 시나리오를 작성할 수 있다.

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

k6는 Go로 작성된 현대적인 부하 테스트 도구다. JavaScript로 테스트 스크립트를 작성하며, CLI 기반으로 간편하게 실행할 수 있다.

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

동일한 비즈니스 로직에 대해 Spring MVC와 Spring WebFlux의 성능을 비교한 일반적인 결과는 다음과 같다. 실제 수치는 하드웨어와 비즈니스 로직에 따라 달라진다.

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

> **핵심 포인트**: 동시 사용자가 적을 때는 MVC와 WebFlux의 성능 차이가 크지 않다. WebFlux의 진가는 **높은 동시성** 상황에서 발휘된다. I/O 대기 시간이 긴 애플리케이션(외부 API 호출, 느린 DB 쿼리)일수록 WebFlux의 이점이 두드러진다.

### 19.6.4 부하 테스트 결과 분석 체크리스트

| 점검 항목 | 정상 기준 | 이상 시 대응 |
|----------|----------|-------------|
| **p95 응답 시간** | SLA 목표 이내 | 병목 구간 프로파일링 |
| **에러율** | < 0.1% | 에러 로그 분석, 타임아웃 조정 |
| **CPU 사용률** | < 80% | 스케줄러 오프로드, 알고리즘 최적화 |
| **메모리 사용률** | GC 오버헤드 < 5% | 힙 크기 조정, 객체 풀링 |
| **커넥션 풀 대기** | waitQueue = 0 | 풀 크기 증가, 쿼리 최적화 |
| **이벤트 루프 CPU** | 각 스레드 < 70% | 블로킹 코드 제거, 연산 오프로드 |

### 19.6.5 성능 최적화 사이클

성능 최적화는 일회성이 아니라 반복적인 과정이다.

```
1. 측정 (Baseline)       <- Gatling/k6로 현재 성능 측정
2. 분석 (Bottleneck)     <- 프로파일링, 메트릭, 로그 분석
3. 최적화 (Fix)          <- 커넥션 풀, 캐시, 블로킹 제거, 쿼리 최적화
4. 검증 (Verify)         <- 동일 조건에서 재측정, 비교
5. 반복 (Iterate)        <- 다음 병목 지점으로 이동
```

한 번에 여러 최적화를 적용하면 어떤 변경이 효과가 있었는지 판단할 수 없다. **한 번에 하나의 변경만 적용하고 측정하는 것**이 원칙이다.

---

## 요약

| 주제 | 핵심 내용 |
|------|----------|
| **성능 측정** | 처리량/지연시간/리소스 3축 측정, Micrometer 메트릭, JMH 마이크로벤치마크, async-profiler/JFR 프로파일링 |
| **MongoDB 커넥션 풀** | `MongoClientSettings`로 풀 크기/타임아웃 설정, 커넥션 풀 메트릭 모니터링, 계층별 타임아웃 전략 |
| **Netty 이벤트 루프** | `LoopResources`로 스레드 수 조정, Epoll/KQueue 네이티브 Transport, 블로킹 작업 스케줄러 오프로드 |
| **캐싱 전략** | Caffeine 로컬 캐시, Reactive Redis 분산 캐시, L1/L2 멀티 레벨 캐시 구조 |
| **BlockHound** | 블로킹 호출 런타임 탐지, 흔한 블로킹 패턴과 수정법, StepVerifier 테스트 통합 |
| **부하 테스트** | Gatling/k6 스크립트 작성, MVC vs WebFlux 성능 비교, 결과 분석 체크리스트, 최적화 사이클 |

성능 최적화에서 가장 중요한 것은 **측정 -> 분석 -> 최적화 -> 검증**의 사이클을 반복하는 것이다. 감이 아닌 데이터에 기반한 의사결정이 효과적인 최적화의 핵심이다.

다음 장에서는 애플리케이션의 컨테이너화와 배포를 다루며, Docker 이미지 빌드, Kubernetes 배포, CI/CD 파이프라인 구성을 실습한다.
# Chapter 20. 컨테이너화와 배포

리액티브 애플리케이션을 개발하고 최적화했다면, 이제 이를 안정적으로 운영 환경에 배포해야 한다. 현대 소프트웨어 배포의 표준은 **컨테이너(Container)**다. Docker를 활용하면 애플리케이션과 실행 환경을 하나의 이미지로 패키징하여 어디서든 동일하게 실행할 수 있고, Kubernetes를 통해 이를 자동으로 확장하고 관리할 수 있다. 이번 장에서는 Spring Boot WebFlux + MongoDB 리액티브 애플리케이션을 **Docker 이미지로 빌드**하고, **Docker Compose로 전체 스택을 구성**하며, **Kubernetes에 배포**하고, **MongoDB Atlas와 연동**하고, **GitHub Actions CI/CD 파이프라인**을 구축하며, **GraalVM Native Image**로 빌드하는 전 과정을 다룬다.

---

## 20.1 Docker 이미지 빌드 (Jib, Buildpacks)

Spring Boot 애플리케이션을 Docker 이미지로 만드는 방법은 크게 세 가지다. 직접 Dockerfile을 작성하는 방법, Google의 Jib을 사용하는 방법, 그리고 Spring Boot가 내장 지원하는 Cloud Native Buildpacks를 사용하는 방법이다.

### 20.1.1 Jib을 활용한 Docker 이미지 빌드

Jib은 Google이 개발한 Java 컨테이너 이미지 빌드 도구다. **Docker 데몬 없이** 이미지를 빌드하고 레지스트리에 직접 푸시할 수 있다. `build.gradle`에 플러그인을 추가한다.

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

빌드 명령어는 세 가지로 구분된다.

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

Spring Boot 3.x는 Cloud Native Buildpacks를 기본 지원한다. 별도 플러그인 없이 Gradle 태스크로 OCI 이미지를 빌드할 수 있다.

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

| 항목 | Dockerfile | Jib | Buildpacks |
|------|-----------|-----|------------|
| Docker 데몬 필요 | O | X | O |
| Dockerfile 필요 | O | X | X |
| 빌드 속도 | 보통 | 빠름 | 느림 |
| 레이어 최적화 | 수동 | 자동 | 자동 |
| 멀티 아키텍처 | 수동 설정 | 선언적 | 제한적 |
| CI/CD 친화성 | 보통 | 높음 | 높음 |

> **주의**: Buildpacks는 초기 빌드가 느리지만 캐시가 쌓이면 이후 빌드는 빨라진다. CI/CD 환경에서 Docker 데몬 설정이 어렵다면 Jib을 권장한다.

---

## 20.2 Docker Compose로 전체 스택 구성

로컬 개발 및 스테이징 환경에서는 Docker Compose를 활용하여 Spring Boot 애플리케이션, MongoDB, Prometheus, Grafana를 한 번에 구성할 수 있다.

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

---

## 20.3 Kubernetes 배포 기초

프로덕션 환경에서는 Kubernetes(이하 K8s)를 활용하여 컨테이너화된 애플리케이션을 오케스트레이션한다.

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

K8s 프로브와 Spring Boot Actuator의 매핑 관계를 이해하는 것이 중요하다.

| K8s 프로브 | Actuator 엔드포인트 | 역할 |
|-----------|-------------------|------|
| `startupProbe` | `/actuator/health/liveness` | 애플리케이션 시작 완료 확인 |
| `readinessProbe` | `/actuator/health/readiness` | 트래픽 수신 준비 확인 |
| `livenessProbe` | `/actuator/health/liveness` | 프로세스 정상 동작 확인 |

`preStop` 훅에서 `sleep 5`를 실행하는 이유는 K8s가 Service 엔드포인트 목록에서 파드를 제거하는 시간을 확보하여 **정상 종료(Graceful Shutdown)** 중 요청 유실을 방지하기 위해서다.

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

> **Tip**: 리액티브 애플리케이션은 CPU 사용률이 낮은 상태에서도 높은 처리량을 달성한다. CPU 기반 HPA만으로는 스케일링 시점을 정확히 판단하기 어려우므로, 커스텀 메트릭(요청 큐 크기, p99 지연시간)을 함께 활용하는 것을 권장한다.

---

## 20.4 MongoDB Atlas 클라우드 연동

프로덕션 환경에서는 MongoDB를 직접 운영하는 대신 관리형 서비스인 **MongoDB Atlas**를 사용하는 것이 운영 부담을 줄이는 효과적인 방법이다.

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

1. **고정 Egress IP**: K8s 클러스터의 아웃바운드 트래픽이 고정 IP를 사용하도록 NAT Gateway를 설정하고, 해당 IP를 Atlas IP Access List에 등록한다.
2. **VPC Peering / Private Link**: 보안이 중요한 환경에서는 Atlas의 VPC Peering 또는 AWS PrivateLink를 활용한다.
3. **DNS 해석**: `mongodb+srv://` URI는 DNS SRV 레코드를 사용하므로 K8s 클러스터의 DNS가 외부 DNS를 정상 해석할 수 있어야 한다.

> **주의**: Atlas Free Tier(M0)는 VPC Peering과 Private Link를 지원하지 않는다. 프로덕션에서는 최소 M10 이상을 사용한다.

---

## 20.5 CI/CD 파이프라인 구성 (GitHub Actions)

GitHub Actions를 활용하여 소스 코드 푸시부터 테스트, Docker 이미지 빌드, K8s 배포까지의 전체 파이프라인을 구성한다.

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

> **Tip**: `environment: production` 설정을 활용하면 프로덕션 배포 전 수동 승인(Manual Approval) 단계를 추가할 수 있다.

---

## 20.6 GraalVM Native Image 빌드

GraalVM Native Image는 Java 애플리케이션을 AOT(Ahead-of-Time) 컴파일하여 네이티브 실행 파일로 변환한다. 시작 시간이 밀리초 단위로 단축되고 메모리 사용량이 대폭 감소하여, 서버리스(Serverless) 환경에 적합하다.

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

Spring Boot 3.x는 AOT 처리를 통해 대부분의 리플렉션 힌트를 자동 생성한다. 동적으로 로드되는 클래스는 수동으로 등록해야 한다.

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

Buildpacks를 활용하면 GraalVM 로컬 설치 없이 네이티브 이미지를 빌드할 수 있다.

```groovy
bootBuildImage {
    imageName = "ghcr.io/myorg/webflux-app-native:${project.version}"
    environment = [
        'BP_NATIVE_IMAGE': 'true',
        'BP_JVM_VERSION': '21'
    ]
}
```

멀티 스테이지 Dockerfile로 직접 빌드하는 방법도 있다.

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

네이티브 이미지 환경에서 주의해야 할 핵심 사항을 정리한다.

1. **빌드 리소스**: 네이티브 이미지 빌드는 최소 8GB RAM이 필요하며 5~10분 이상 소요된다. CI/CD에서 대규모 프로젝트는 Larger Runner 사용을 고려한다.
2. **프로파일 결정 시점**: 네이티브 이미지는 빌드 시점에 프로파일이 결정된다. 런타임 변경이 필요하면 AOT 처리 시 명시해야 한다.

```bash
./gradlew nativeCompile -Pspring.profiles.active=prod
```

3. **서드파티 호환성**: 모든 라이브러리가 네이티브 이미지를 지원하는 것은 아니다. [GraalVM Reachability Metadata Repository](https://github.com/oracle/graalvm-reachability-metadata)에서 호환성을 확인한다.
4. **GitHub Actions 빌드**: 태그 푸시 시 네이티브 이미지를 빌드하는 워크플로우를 구성한다.

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

| 주제 | 핵심 도구 | 권장 사항 |
|------|----------|----------|
| Docker 빌드 | Jib, Buildpacks | CI/CD에서는 Jib 권장 |
| 로컬 스택 | Docker Compose | 헬스 체크와 의존성 순서 필수 |
| K8s 배포 | Deployment, HPA | 3종 프로브와 preStop 훅 설정 |
| Atlas 연동 | SRV 연결 | VPC Peering으로 보안 강화 |
| CI/CD | GitHub Actions | 브랜치 전략과 시크릿 관리 |
| Native Image | GraalVM, AOT | 서버리스 환경에 적합 |

컨테이너화와 CI/CD는 한 번 구축하면 이후 배포가 자동화된다. 다음 장에서는 **장애 대응과 트러블슈팅**을 다룬다.# Chapter 21. 실전 프로젝트: 실시간 게시판 서비스

지금까지 배운 WebFlux, MongoDB 리액티브, JWT 인증, SSE, 테스트 등의 개념을 하나의 완전한 프로젝트로 통합할 차례다. 이번 장에서는 **실시간 게시판 서비스**를 처음부터 끝까지 구축한다. 회원가입과 JWT 기반 인증, 게시글 CRUD, 댓글 시스템, MongoDB Change Streams를 활용한 실시간 알림, 페이징과 검색, GridFS 파일 업로드, 테스트 작성, Docker Compose 배포까지 실전에서 필요한 전 과정을 다룬다.

---

## 21.1 요구사항 분석 및 설계

### 21.1.1 기능 요구사항과 기술 스택

| 기능 영역 | 세부 기능 | 기술 |
|-----------|----------|------|
| **사용자 관리** | 회원가입, 로그인, JWT 토큰 발급 | Spring Security + jjwt |
| **게시글** | 작성, 조회, 수정, 삭제, 페이징 | ReactiveMongoRepository |
| **댓글** | 작성, 조회, 삭제 | ReactiveMongoTemplate |
| **실시간 알림** | 새 댓글 알림 | Change Streams + SSE |
| **검색** | 제목/본문 키워드 검색 | ReactiveMongoTemplate |
| **파일 업로드** | 첨부파일 업로드/다운로드 | GridFS |

전체 스택은 Spring Boot 3.x + WebFlux + MongoDB 7.x(Reactive) + Testcontainers + Docker Compose로 구성한다.

### 21.1.2 프로젝트 구조

```
reactive-board/
├── src/main/java/com/example/board/
│   ├── config/          # MongoConfig, SecurityConfig
│   ├── security/        # JwtTokenProvider, JwtAuthenticationFilter
│   ├── domain/          # User, Post, Comment
│   ├── repository/      # UserRepository, PostRepository, CommentRepository
│   ├── service/         # UserService, PostService, CommentService,
│   │                    # NotificationService, FileService, PostSearchService
│   ├── controller/      # AuthController, PostController, CommentController,
│   │                    # NotificationController, FileController
│   └── dto/             # 요청/응답 DTO 클래스
├── src/main/resources/application.yml
├── Dockerfile
└── docker-compose.yml
```

### 21.1.3 시스템 아키텍처

```
[클라이언트] → [Netty] → Controller → Service → MongoDB
                                         └── Change Streams → SSE → 클라이언트
```

---

## 21.2 사용자 관리 (회원가입, 로그인, JWT)

### 21.2.1 의존성 설정

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    implementation 'org.springframework.boot:spring-boot-starter-data-mongodb-reactive'
    implementation 'org.springframework.boot:spring-boot-starter-security'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    implementation 'io.jsonwebtoken:jjwt-api:0.12.6'
    runtimeOnly 'io.jsonwebtoken:jjwt-impl:0.12.6'
    runtimeOnly 'io.jsonwebtoken:jjwt-jackson:0.12.6'
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'io.projectreactor:reactor-test'
    testImplementation 'org.testcontainers:mongodb:1.20.4'
}
```

### 21.2.2 User 도메인 모델

```java
@Document(collection = "users")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class User {
    @Id private String id;
    @Indexed(unique = true) private String email;
    @Indexed(unique = true) private String nickname;
    private String password;
    @Builder.Default private List<String> roles = List.of("ROLE_USER");
    @CreatedDate private LocalDateTime createdAt;
}
```

### 21.2.3 JWT 토큰 제공자

```java
@Component
public class JwtTokenProvider {

    private final SecretKey secretKey;
    private final long accessTokenValidity;

    public JwtTokenProvider(@Value("${jwt.secret}") String secret,
            @Value("${jwt.access-token-validity:3600000}") long validity) {
        this.secretKey = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
        this.accessTokenValidity = validity;
    }

    public String createToken(String userId, String email, List<String> roles) {
        return Jwts.builder().subject(userId)
            .claim("email", email).claim("roles", roles)
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + accessTokenValidity))
            .signWith(secretKey).compact();
    }

    public Claims parseToken(String token) {
        return Jwts.parser().verifyWith(secretKey).build()
            .parseSignedClaims(token).getPayload();
    }

    public boolean validateToken(String token) {
        try { parseToken(token); return true; }
        catch (JwtException | IllegalArgumentException e) { return false; }
    }
}
```

### 21.2.4 JWT 인증 필터와 Security 설정

WebFlux 환경에서는 서블릿 필터 대신 `WebFilter`를 사용한다. Bearer 토큰을 추출하고, 유효하면 `ReactiveSecurityContextHolder`에 인증 정보를 설정한다.

```java
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter implements WebFilter {

    private final JwtTokenProvider jwtTokenProvider;

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String token = extractToken(exchange.getRequest());
        if (token != null && jwtTokenProvider.validateToken(token)) {
            Claims claims = jwtTokenProvider.parseToken(token);
            List<SimpleGrantedAuthority> authorities =
                claims.get("roles", List.class).stream()
                    .map(r -> new SimpleGrantedAuthority((String) r)).toList();
            var auth = new UsernamePasswordAuthenticationToken(
                claims.getSubject(), null, authorities);
            return chain.filter(exchange)
                .contextWrite(ReactiveSecurityContextHolder.withAuthentication(auth));
        }
        return chain.filter(exchange);
    }

    private String extractToken(ServerHttpRequest request) {
        String bearer = request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
        return (bearer != null && bearer.startsWith("Bearer "))
            ? bearer.substring(7) : null;
    }
}
```

Security 설정에서는 인증/비인증 엔드포인트를 구분하고, JWT 필터를 등록한다.

```java
@Configuration @EnableWebFluxSecurity @RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthenticationFilter;

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        return http
            .csrf(ServerHttpSecurity.CsrfSpec::disable)
            .httpBasic(ServerHttpSecurity.HttpBasicSpec::disable)
            .formLogin(ServerHttpSecurity.FormLoginSpec::disable)
            .authorizeExchange(ex -> ex
                .pathMatchers("/api/auth/**").permitAll()
                .pathMatchers(HttpMethod.GET, "/api/posts/**").permitAll()
                .pathMatchers("/api/notifications/**").permitAll()
                .anyExchange().authenticated())
            .addFilterBefore(jwtAuthenticationFilter, SecurityWebFiltersOrder.AUTHENTICATION)
            .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(); }
}
```

### 21.2.5 회원가입/로그인 서비스

```java
@Service @RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    public Mono<UserResponse> signup(SignupRequest request) {
        return userRepository.findByEmail(request.getEmail())
            .flatMap(existing -> Mono.<User>error(
                new DuplicateException("이미 등록된 이메일입니다.")))
            .switchIfEmpty(Mono.defer(() -> userRepository.save(User.builder()
                .email(request.getEmail()).nickname(request.getNickname())
                .password(passwordEncoder.encode(request.getPassword())).build())))
            .map(u -> new UserResponse(u.getId(), u.getEmail(), u.getNickname()));
    }

    public Mono<LoginResponse> login(LoginRequest request) {
        return userRepository.findByEmail(request.getEmail())
            .filter(u -> passwordEncoder.matches(request.getPassword(), u.getPassword()))
            .map(u -> new LoginResponse(
                jwtTokenProvider.createToken(u.getId(), u.getEmail(), u.getRoles()),
                u.getNickname()))
            .switchIfEmpty(Mono.error(
                new AuthenticationException("이메일 또는 비밀번호가 올바르지 않습니다.")));
    }
}
```

---

## 21.3 게시글 CRUD API 구현

### 21.3.1 Post 도메인 모델

```java
@Document(collection = "posts")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class Post {
    @Id private String id;
    @Indexed private String authorId;
    private String authorNickname;
    private String title;
    private String content;
    private List<String> attachmentIds;
    @Builder.Default private int viewCount = 0;
    @Builder.Default private int commentCount = 0;
    @CreatedDate private LocalDateTime createdAt;
    @LastModifiedDate private LocalDateTime updatedAt;
}
```

### 21.3.2 PostService

조회수 증가는 `ReactiveMongoTemplate`의 원자적 업데이트를 사용하고, 수정/삭제 시 작성자 권한을 검증한다.

```java
@Service @RequiredArgsConstructor
public class PostService {

    private final PostRepository postRepository;
    private final ReactiveMongoTemplate mongoTemplate;

    public Mono<Post> createPost(PostRequest req, String authorId, String nickname) {
        return postRepository.save(Post.builder().authorId(authorId)
            .authorNickname(nickname).title(req.getTitle())
            .content(req.getContent()).build());
    }

    public Mono<Post> getPost(String postId) {
        return postRepository.findById(postId)
            .switchIfEmpty(Mono.error(new NotFoundException("게시글을 찾을 수 없습니다.")))
            .flatMap(post -> mongoTemplate.updateFirst(
                Query.query(Criteria.where("id").is(postId)),
                new Update().inc("viewCount", 1), Post.class)
                .thenReturn(post));
    }

    public Mono<Post> updatePost(String postId, PostRequest req, String authorId) {
        return postRepository.findById(postId)
            .switchIfEmpty(Mono.error(new NotFoundException("게시글을 찾을 수 없습니다.")))
            .filter(p -> p.getAuthorId().equals(authorId))
            .switchIfEmpty(Mono.error(new ForbiddenException("수정 권한이 없습니다.")))
            .flatMap(p -> { p.setTitle(req.getTitle()); p.setContent(req.getContent());
                return postRepository.save(p); });
    }

    public Mono<Void> deletePost(String postId, String authorId) {
        return postRepository.findById(postId)
            .switchIfEmpty(Mono.error(new NotFoundException("게시글을 찾을 수 없습니다.")))
            .filter(p -> p.getAuthorId().equals(authorId))
            .switchIfEmpty(Mono.error(new ForbiddenException("삭제 권한이 없습니다.")))
            .flatMap(postRepository::delete);
    }
}
```

### 21.3.3 PostController

```java
@RestController @RequestMapping("/api/posts") @RequiredArgsConstructor
public class PostController {

    private final PostService postService;
    private final PostSearchService postSearchService;
    private final UserRepository userRepository;

    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    public Mono<PostResponse> createPost(@Valid @RequestBody PostRequest request,
            @AuthenticationPrincipal Mono<String> principalId) {
        return principalId.flatMap(uid -> userRepository.findById(uid)
            .flatMap(u -> postService.createPost(request, uid, u.getNickname()))
            .map(PostResponse::from));
    }

    @GetMapping("/{postId}")
    public Mono<PostResponse> getPost(@PathVariable String postId) {
        return postService.getPost(postId).map(PostResponse::from);
    }

    @PutMapping("/{postId}")
    public Mono<PostResponse> updatePost(@PathVariable String postId,
            @Valid @RequestBody PostRequest request,
            @AuthenticationPrincipal Mono<String> principalId) {
        return principalId.flatMap(uid ->
            postService.updatePost(postId, request, uid).map(PostResponse::from));
    }

    @DeleteMapping("/{postId}") @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deletePost(@PathVariable String postId,
            @AuthenticationPrincipal Mono<String> principalId) {
        return principalId.flatMap(uid -> postService.deletePost(postId, uid));
    }

    @GetMapping
    public Mono<PageResponse<PostResponse>> listPosts(
            @RequestParam(defaultValue = "") String keyword,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        return postSearchService.searchPosts(keyword, page, size);
    }
}
```

---

## 21.4 댓글 시스템 (내장 도큐먼트 vs 참조)

### 21.4.1 설계 선택

| 기준 | 임베디드(Embedded) | 참조(Reference) |
|------|-------------------|----------------|
| **문서 크기** | 댓글 증가 시 16MB 제한 위험 | 안정적 |
| **독립 쿼리** | 댓글만 별도 조회 어려움 | 페이징/정렬 가능 |
| **Change Stream** | 활용 제한적 | 댓글 컬렉션 감시 가능 |

댓글이 무제한 증가할 수 있고, Change Streams 기반 실시간 알림이 필요하므로 **참조 방식**을 선택한다.

### 21.4.2 Comment 모델과 서비스

```java
@Document(collection = "comments")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class Comment {
    @Id private String id;
    @Indexed private String postId;
    private String authorId;
    private String authorNickname;
    private String content;
    @CreatedDate private LocalDateTime createdAt;
}
```

```java
@Service @RequiredArgsConstructor
public class CommentService {

    private final CommentRepository commentRepository;
    private final PostRepository postRepository;
    private final ReactiveMongoTemplate mongoTemplate;

    public Mono<Comment> addComment(String postId, String content,
                                     String authorId, String authorNickname) {
        return postRepository.findById(postId)
            .switchIfEmpty(Mono.error(new NotFoundException("게시글을 찾을 수 없습니다.")))
            .then(Mono.defer(() -> commentRepository.save(Comment.builder()
                .postId(postId).authorId(authorId)
                .authorNickname(authorNickname).content(content).build())))
            .flatMap(c -> mongoTemplate.updateFirst(
                Query.query(Criteria.where("id").is(postId)),
                new Update().inc("commentCount", 1), Post.class).thenReturn(c));
    }

    public Flux<Comment> getComments(String postId) {
        return commentRepository.findByPostIdOrderByCreatedAtDesc(postId);
    }

    public Mono<Void> deleteComment(String commentId, String userId) {
        return commentRepository.findById(commentId)
            .filter(c -> c.getAuthorId().equals(userId))
            .switchIfEmpty(Mono.error(new ForbiddenException("삭제 권한이 없습니다.")))
            .flatMap(c -> commentRepository.delete(c).then(mongoTemplate.updateFirst(
                Query.query(Criteria.where("id").is(c.getPostId())),
                new Update().inc("commentCount", -1), Post.class).then()));
    }
}
```

---

## 21.5 실시간 알림 (SSE)

MongoDB Change Streams로 `comments` 컬렉션의 insert 이벤트를 감지하고, `Sinks.Many`를 통해 SSE로 클라이언트에 전송한다.

```
[댓글 작성] → MongoDB insert → Change Stream 감지 → Sinks.Many → SSE → 클라이언트
```

### 21.5.1 NotificationService

```java
@Service @Slf4j
public class NotificationService {

    private final Sinks.Many<NotificationEvent> sink;
    private final Flux<NotificationEvent> notificationFlux;

    public NotificationService(ReactiveMongoTemplate mongoTemplate) {
        this.sink = Sinks.many().multicast().onBackpressureBuffer(256);
        this.notificationFlux = sink.asFlux().share();

        mongoTemplate.changeStream("comments",
                ChangeStreamOptions.builder()
                    .filter(Aggregation.newAggregation(Aggregation.match(
                        Criteria.where("operationType").is("insert"))))
                    .build(), Comment.class)
            .doOnNext(event -> {
                Comment c = event.getBody();
                if (c != null) {
                    sink.tryEmitNext(NotificationEvent.builder()
                        .type("NEW_COMMENT").postId(c.getPostId())
                        .message(c.getAuthorNickname() + "님이 댓글을 작성했습니다.")
                        .createdAt(LocalDateTime.now()).build());
                }
            })
            .doOnError(e -> log.error("Change Stream 오류", e))
            .subscribe();
    }

    public Flux<NotificationEvent> getNotifications(String postId) {
        return notificationFlux.filter(e -> e.getPostId().equals(postId));
    }

    public Flux<NotificationEvent> getAllNotifications() { return notificationFlux; }
}
```

### 21.5.2 NotificationController

```java
@RestController @RequestMapping("/api/notifications") @RequiredArgsConstructor
public class NotificationController {

    private final NotificationService notificationService;

    @GetMapping(value = "/stream/{postId}", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<NotificationEvent>> streamByPost(
            @PathVariable String postId) {
        return notificationService.getNotifications(postId)
            .map(e -> ServerSentEvent.<NotificationEvent>builder()
                .id(UUID.randomUUID().toString()).event(e.getType()).data(e).build());
    }

    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<NotificationEvent>> streamAll() {
        return notificationService.getAllNotifications()
            .map(e -> ServerSentEvent.<NotificationEvent>builder()
                .id(UUID.randomUUID().toString()).event(e.getType()).data(e).build());
    }
}
```

Change Streams는 MongoDB **레플리카 셋(Replica Set)** 모드에서만 동작한다. 21.9절에서 이를 설정한다.

---

## 21.6 페이징과 검색 기능

리액티브 환경에서는 Spring Data의 `Page` 객체를 직접 사용할 수 없으므로 커스텀 DTO를 구성한다.

```java
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class PageResponse<T> {
    private List<T> content;
    private int page, size;
    private long totalElements;
    private int totalPages;
    private boolean hasNext;

    public static <T> Mono<PageResponse<T>> of(
            Flux<T> contentFlux, Mono<Long> countMono, int page, int size) {
        return Mono.zip(contentFlux.collectList(), countMono).map(tuple -> {
            long total = tuple.getT2();
            int tp = (int) Math.ceil((double) total / size);
            return PageResponse.<T>builder().content(tuple.getT1())
                .page(page).size(size).totalElements(total)
                .totalPages(tp).hasNext(page < tp - 1).build();
        });
    }
}
```

`ReactiveMongoTemplate`으로 동적 쿼리, 정렬, 페이징을 처리한다.

```java
@Service @RequiredArgsConstructor
public class PostSearchService {

    private final ReactiveMongoTemplate mongoTemplate;

    public Mono<PageResponse<PostResponse>> searchPosts(
            String keyword, int page, int size) {
        Criteria criteria = new Criteria();
        if (keyword != null && !keyword.isBlank()) {
            criteria.orOperator(Criteria.where("title").regex(keyword, "i"),
                Criteria.where("content").regex(keyword, "i"));
        }
        Query query = Query.query(criteria)
            .with(Sort.by(Sort.Direction.DESC, "createdAt"));
        Flux<PostResponse> content = mongoTemplate
            .find(query.skip((long) page * size).limit(size), Post.class)
            .map(PostResponse::from);
        Mono<Long> count = mongoTemplate.count(Query.query(criteria), Post.class);
        return PageResponse.of(content, count, page, size);
    }
}
```

검색 성능을 위해 텍스트 인덱스(Text Index)를 추가할 수 있다.

```java
@Configuration
public class MongoConfig {
    @EventListener(ApplicationReadyEvent.class)
    public void initIndices(ApplicationReadyEvent event) {
        ReactiveMongoTemplate template = event.getApplicationContext()
            .getBean(ReactiveMongoTemplate.class);
        template.indexOps(Post.class).ensureIndex(
            new TextIndexDefinition.TextIndexDefinitionBuilder()
                .onField("title").onField("content").build()).subscribe();
    }
}
```

---

## 21.7 파일 업로드 (GridFS)

MongoDB GridFS는 파일을 청크(Chunk)로 분할하여 저장한다. 리액티브 환경에서는 `ReactiveGridFsTemplate`을 사용한다.

```java
@Service @RequiredArgsConstructor
public class FileService {

    private final ReactiveGridFsTemplate gridFsTemplate;

    public Mono<String> uploadFile(FilePart filePart) {
        DBObject metadata = new BasicDBObject();
        metadata.put("contentType", filePart.headers().getContentType() != null
            ? filePart.headers().getContentType().toString()
            : MediaType.APPLICATION_OCTET_STREAM_VALUE);
        return gridFsTemplate.store(filePart.content(), filePart.filename(), metadata)
            .map(ObjectId::toString);
    }

    public Mono<GridFsResource> downloadFile(String fileId) {
        return gridFsTemplate.findOne(Query.query(Criteria.where("_id").is(fileId)))
            .flatMap(gridFsTemplate::getResource);
    }

    public Mono<Void> deleteFile(String fileId) {
        return gridFsTemplate.delete(Query.query(Criteria.where("_id").is(fileId))).then();
    }
}
```

```java
@RestController @RequestMapping("/api/files") @RequiredArgsConstructor
public class FileController {

    private final FileService fileService;

    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<Map<String, String>> upload(@RequestPart("file") Mono<FilePart> file) {
        return file.flatMap(fileService::uploadFile).map(id -> Map.of("fileId", id));
    }

    @GetMapping("/{fileId}")
    public Mono<ResponseEntity<Flux<DataBuffer>>> download(@PathVariable String fileId) {
        return fileService.downloadFile(fileId).map(r -> ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_DISPOSITION,
                "attachment; filename=\"" + r.getFilename() + "\"")
            .contentType(MediaType.APPLICATION_OCTET_STREAM)
            .body(r.getDownloadStream()));
    }
}
```

반환된 `fileId`를 게시글의 `attachmentIds`에 저장하면 게시글과 첨부파일을 연결할 수 있다.

---

## 21.8 전체 테스트 작성

```java
@Testcontainers
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public abstract class IntegrationTestBase {

    @Container
    static MongoDBContainer mongo = new MongoDBContainer("mongo:7.0")
        .withCommand("--replSet", "rs0");

    @DynamicPropertySource
    static void mongoProps(DynamicPropertyRegistry registry) {
        registry.add("spring.data.mongodb.uri", mongo::getReplicaSetUrl);
    }

    @Autowired protected WebTestClient webTestClient;
}
```

### 21.8.2 PostService 단위 테스트

```java
@ExtendWith(MockitoExtension.class)
class PostServiceTest {

    @Mock private PostRepository postRepository;
    @Mock private ReactiveMongoTemplate mongoTemplate;
    @InjectMocks private PostService postService;

    @Test @DisplayName("게시글 생성 시 저자 정보가 정확히 설정된다")
    void createPost_setsAuthorInfo() {
        Post saved = Post.builder().id("p1").authorId("u1")
            .authorNickname("홍길동").title("제목").build();
        when(postRepository.save(any(Post.class))).thenReturn(Mono.just(saved));
        StepVerifier.create(postService.createPost(
                new PostRequest("제목", "본문"), "u1", "홍길동"))
            .assertNext(p -> assertThat(p.getAuthorId()).isEqualTo("u1"))
            .verifyComplete();
    }

    @Test @DisplayName("존재하지 않는 게시글 조회 시 NotFoundException")
    void getPost_notFound() {
        when(postRepository.findById("x")).thenReturn(Mono.empty());
        StepVerifier.create(postService.getPost("x"))
            .expectError(NotFoundException.class).verify();
    }

    @Test @DisplayName("작성자가 아닌 사용자의 수정 시 ForbiddenException")
    void updatePost_wrongAuthor() {
        when(postRepository.findById("p1")).thenReturn(
            Mono.just(Post.builder().id("p1").authorId("u1").build()));
        StepVerifier.create(postService.updatePost("p1",
                new PostRequest("수정", "수정"), "u999"))
            .expectError(ForbiddenException.class).verify();
    }
}
```

### 21.8.3 PostController 통합 테스트

```java
class PostControllerTest extends IntegrationTestBase {

    @Autowired private UserRepository userRepository;
    @Autowired private PostRepository postRepository;
    @Autowired private JwtTokenProvider jwtTokenProvider;
    private String authToken;

    @BeforeEach
    void setup() {
        User user = User.builder().id("test-user").email("test@example.com")
            .nickname("테스터").password("encoded").build();
        userRepository.save(user).block();
        authToken = jwtTokenProvider.createToken(
            user.getId(), user.getEmail(), user.getRoles());
    }

    @AfterEach
    void cleanup() {
        postRepository.deleteAll().then(userRepository.deleteAll()).block();
    }

    @Test @DisplayName("인증된 사용자가 게시글을 생성하면 201 응답")
    void createPost_returns201() {
        webTestClient.post().uri("/api/posts")
            .header(HttpHeaders.AUTHORIZATION, "Bearer " + authToken)
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(new PostRequest("테스트 제목", "테스트 본문"))
            .exchange()
            .expectStatus().isCreated()
            .expectBody()
            .jsonPath("$.title").isEqualTo("테스트 제목")
            .jsonPath("$.authorNickname").isEqualTo("테스터");
    }

    @Test @DisplayName("인증 없이 게시글 생성 시 401 응답")
    void createPost_unauthenticated() {
        webTestClient.post().uri("/api/posts")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(new PostRequest("제목", "본문"))
            .exchange().expectStatus().isUnauthorized();
    }

    @Test @DisplayName("게시글 목록 페이징 조회")
    void listPosts_paged() {
        Flux.range(1, 15).flatMap(i -> postRepository.save(Post.builder()
            .title("게시글 " + i).content("본문").authorId("test-user")
            .authorNickname("테스터").build())).blockLast();
        webTestClient.get().uri("/api/posts?page=0&size=10").exchange()
            .expectStatus().isOk().expectBody()
            .jsonPath("$.content.length()").isEqualTo(10)
            .jsonPath("$.totalElements").isEqualTo(15)
            .jsonPath("$.hasNext").isEqualTo(true);
    }
}
```

---

## 21.9 Docker Compose로 배포

### 21.9.1 설정 파일

```yaml
# application.yml
spring:
  data:
    mongodb:
      uri: ${MONGODB_URI:mongodb://localhost:27017/reactive-board?replicaSet=rs0}
jwt:
  secret: ${JWT_SECRET:Y2xhdWRlLXdlYmZsdXgtYm9vay1zZWNyZXQta2V5LWZvci1qd3QtdG9rZW4=}
  access-token-validity: 3600000
```

```dockerfile
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY build/libs/reactive-board-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

MongoDB를 레플리카 셋으로 구성해야 Change Streams가 동작한다.

```yaml
# docker-compose.yml
version: '3.8'
services:
  mongodb:
    image: mongo:7.0
    ports: ["27017:27017"]
    volumes: [mongo-data:/data/db]
    command: ["--replSet", "rs0", "--bind_ip_all"]
    healthcheck:
      test: >
        mongosh --eval "try { rs.status().ok }
        catch(e) { rs.initiate({_id:'rs0',members:[{_id:0,host:'mongodb:27017'}]}).ok }"
      interval: 10s
      start_period: 30s
  app:
    build: .
    ports: ["8080:8080"]
    environment:
      MONGODB_URI: mongodb://mongodb:27017/reactive-board?replicaSet=rs0&directConnection=true
      JWT_SECRET: Y2xhdWRlLXdlYmZsdXgtYm9vay1zZWNyZXQta2V5LWZvci1qd3QtdG9rZW4=
    depends_on:
      mongodb: { condition: service_healthy }
volumes:
  mongo-data:
```

### 21.9.2 빌드 및 API 동작 확인

```bash
./gradlew clean build && docker compose up --build -d

# 회원가입 → 로그인 → 토큰 획득
curl -X POST http://localhost:8080/api/auth/signup -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","nickname":"홍길동","password":"pass123"}'
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123"}' | jq -r '.token')

# 게시글 작성 / SSE 구독 / 파일 업로드
curl -X POST http://localhost:8080/api/posts -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -d '{"title":"첫 게시글","content":"WebFlux 게시판"}'
curl -N http://localhost:8080/api/notifications/stream   # 별도 터미널에서 SSE 구독
curl -X POST http://localhost:8080/api/files -H "Authorization: Bearer $TOKEN" -F "file=@./sample.png"
```

### 21.9.3 전체 요청 흐름

```
[사용자 A] POST /api/posts → JWT 검증 → MongoDB insert → 201 Created
[사용자 B] GET /api/notifications/stream (SSE 연결 유지)
[사용자 C] POST /api/posts/{id}/comments → MongoDB insert → Change Stream → SSE 알림 전송
```

---

이번 장에서 구축한 실시간 게시판 서비스는 Part 1부터 Part 6까지 다룬 핵심 개념을 모두 통합한 결과물이다. Reactor 기반의 논블로킹 처리, MongoDB 리액티브 드라이버, JWT 인증, SSE 실시간 통신, GridFS 파일 관리, StepVerifier와 WebTestClient를 활용한 테스트, Docker Compose 배포까지 전 과정을 실전 코드로 경험했다. 다음 장에서는 이 프로젝트를 확장하여 실시간 채팅 서비스를 구축하며 WebSocket과 고급 메시징 패턴을 다룬다.
# 부록 A. Reactor 주요 연산자 레퍼런스

이 부록은 Project Reactor에서 실무적으로 자주 사용하는 연산자를 카테고리별로 정리한 레퍼런스이다. 각 연산자에 대해 간결한 설명, 코드 예제, 마블 다이어그램의 텍스트 표현을 제공한다. 본문 3장~5장에서 다룬 내용을 빠르게 참조할 수 있도록 구성했다.

> **표기 규칙**: 마블 다이어그램에서 `──>` 는 시간 흐름, `|` 는 onComplete, `X` 는 onError를 나타낸다.

---

## A.1 생성 연산자 (Creation Operators)

스트림의 출발점을 만드는 연산자들이다. 데이터 소스를 리액티브 파이프라인으로 진입시킨다.

| 연산자 | 반환 타입 | 설명 |
|--------|-----------|------|
| `just` | Mono / Flux | 주어진 값으로 즉시 스트림을 생성한다 |
| `empty` | Mono / Flux | 요소 없이 완료 신호만 발행한다 |
| `error` | Mono / Flux | 즉시 에러 신호를 발행한다 |
| `fromIterable` | Flux | Iterable 컬렉션을 Flux로 변환한다 |
| `fromStream` | Flux | Java Stream을 Flux로 변환한다 (일회성) |
| `range` | Flux | 시작값부터 지정 개수만큼 정수를 발행한다 |
| `interval` | Flux | 지정된 주기마다 0부터 증가하는 Long 값을 발행한다 |
| `defer` | Mono / Flux | 구독 시점에 Publisher를 지연 생성한다 |
| `create` | Mono / Flux | FluxSink/MonoSink를 통해 프로그래밍 방식으로 요소를 발행한다 |

### just / empty / error

`just`는 지정한 값을 즉시 발행한다. `empty`는 요소 없이 완료하고, `error`는 즉시 에러를 발행한다.

```java
Mono<String> mono = Mono.just("Hello");
Flux<Integer> flux = Flux.just(1, 2, 3);
Mono<String> empty = Mono.empty();
Mono<String> error = Mono.error(new IllegalArgumentException("잘못된 인자"));
```

```
just:   ──(Hello)──|──>
empty:  ──|──>
error:  ──X──>
```

### fromIterable / fromStream / range

기존 컬렉션, Stream, 정수 범위를 리액티브 스트림으로 변환한다.

```java
Flux<String> fromList = Flux.fromIterable(List.of("A", "B", "C"));
Flux<String> fromStream = Flux.fromStream(List.of("A", "B").stream()); // 일회성
Flux<Integer> range = Flux.range(1, 5); // 1, 2, 3, 4, 5
```

```
range:  ──(1)──(2)──(3)──(4)──(5)──|──>
```

### interval

지정 주기마다 0부터 증가하는 Long 값을 무한히 발행한다. `Schedulers.parallel()`에서 실행된다.

```java
Flux<Long> tick = Flux.interval(Duration.ofSeconds(1));       // 0, 1, 2, ...
Flux<Long> delayed = Flux.interval(Duration.ofSeconds(5), Duration.ofSeconds(1));
```

```
시간:  0s     1s     2s     3s
소스: ──(0)──(1)──(2)──(3)──...──>
```

### defer

구독 시점마다 새로운 Publisher를 생성한다. 구독 시점의 상태에 의존하는 로직에 필수적이다.

```java
Mono<Long> deferred = Mono.defer(() -> Mono.just(System.currentTimeMillis()));
// 구독할 때마다 다른 타임스탬프가 발행된다
```

### create

`FluxSink`를 통해 프로그래밍 방식으로 요소를 발행한다. 콜백 기반 API를 리액티브로 브릿지할 때 사용한다.

```java
Flux<String> bridge = Flux.create(sink -> {
    myListener.register(
        data -> sink.next(data),
        err  -> sink.error(err),
        ()   -> sink.complete()
    );
}, FluxSink.OverflowStrategy.BUFFER);
```

---

## A.2 변환 연산자 (Transformation Operators)

스트림의 각 요소를 다른 형태로 변환하거나 스트림 구조를 재구성한다.

| 연산자 | 설명 | 비동기 |
|--------|------|--------|
| `map` | 각 요소를 동기적으로 1:1 변환 | 동기 |
| `flatMap` | Publisher로 변환 후 병합 (순서 비보장) | 비동기 |
| `flatMapSequential` | Publisher로 변환 후 원래 순서대로 병합 | 비동기 |
| `concatMap` | 순차적으로 Publisher 변환 후 연결 | 비동기 |
| `switchMap` | 새 요소 시 이전 Publisher를 취소하고 전환 | 비동기 |
| `collectList` | 모든 요소를 List로 수집 | - |
| `collectMap` | 모든 요소를 Map으로 수집 | - |
| `reduce` | 모든 요소를 하나의 값으로 축약 | - |
| `scan` | 누적 중간 결과를 매 요소마다 발행 | - |

### map

각 요소에 동기 함수를 적용하여 1:1로 변환한다.

```java
Flux<String> upper = Flux.just("a", "b", "c").map(String::toUpperCase);
// 결과: "A", "B", "C"
```

```
소스:   ──(a)──(b)──(c)──|──>        결과:   ──(A)──(B)──(C)──|──>
```

### flatMap

각 요소를 비동기 Publisher로 변환하고 결과를 병합한다. **결과 순서가 보장되지 않는다**.

```java
Flux<String> result = Flux.just(1, 2, 3)
    .flatMap(id -> webClient.get().uri("/users/{id}", id)
        .retrieve().bodyToMono(String.class));
```

```
소스:    ──(1)────(2)────(3)──|──>
내부1:   ──────(R1)──>          내부2:   ────(R2)──>
결과:    ──(R2)──(R1)──(R3)──|──>   (순서 비결정적)
```

### flatMapSequential / concatMap

`flatMapSequential`은 내부 Publisher를 **동시에** 구독하되 **원래 순서대로** 결과를 발행한다. `concatMap`은 이전 Publisher가 **완료된 후** 다음을 구독한다(직렬 실행).

```java
Flux.just(1, 2, 3).flatMapSequential(id -> fetchUser(id)); // 병렬 실행, 순서 보장
Flux.just(1, 2, 3).concatMap(id -> fetchUser(id));          // 직렬 실행, 순서 보장
```

```
concatMap:
내부1:   ──(R1)──|
내부2:           ──(R2)──|
내부3:                   ──(R3)──|
결과:    ──(R1)──(R2)──(R3)──|──>
```

### switchMap

새 요소가 발행되면 진행 중인 내부 Publisher를 **즉시 취소**한다. 자동 완성 검색에 적합하다.

```java
Flux<String> results = userInput.switchMap(query -> searchService.search(query));
```

```
소스:    ──(A)────(AB)────(ABC)──|──>
내부1:   ──...X (취소)   내부2: ──...X (취소)   내부3: ──(결과)──|
결과:    ────────────────(결과)──|──>
```

### collectList / collectMap / reduce / scan

```java
Mono<List<String>> list = Flux.just("A", "B", "C").collectList();       // ["A","B","C"]
Mono<Map<Long, User>> map = userFlux.collectMap(User::getId);            // {1:User1, ...}
Mono<Integer> sum = Flux.range(1, 5).reduce(0, Integer::sum);           // 15
Flux<Integer> running = Flux.range(1, 5).scan(0, Integer::sum);         // 0,1,3,6,10,15
```

```
scan:   소스 ──(1)──(2)──(3)──(4)──(5)──|──>
        결과 ──(0)──(1)──(3)──(6)──(10)──(15)──|──>
```

---

## A.3 필터링 연산자 (Filtering Operators)

스트림에서 조건에 맞는 요소만 선별하거나 특정 위치의 요소를 추출한다.

| 연산자 | 설명 |
|--------|------|
| `filter` | Predicate에 맞는 요소만 통과시킨다 |
| `filterWhen` | 비동기 조건(Publisher<Boolean>)으로 필터링한다 |
| `distinct` | 중복 요소를 제거한다 |
| `take(n)` | 처음 n개의 요소만 취한 후 상류를 취소한다 |
| `skip(n)` | 처음 n개의 요소를 건너뛴다 |
| `next` | 첫 번째 요소만 Mono로 반환한다 |
| `last` | 마지막 요소만 Mono로 반환한다 |
| `elementAt(i)` | 인덱스 i 위치의 요소를 Mono로 반환한다 |

### filter / filterWhen

`filter`는 동기적 Predicate를, `filterWhen`은 비동기 조건을 평가한다.

```java
Flux<Integer> even = Flux.range(1, 10).filter(n -> n % 2 == 0);   // 2,4,6,8,10
Flux<User> active = userFlux.filterWhen(u -> userRepo.isActive(u.getId()));
```

```
소스:   ──(1)──(2)──(3)──(4)──(5)──|──>
결과:   ──(2)──(4)──|──>
```

### distinct

중복 요소를 제거한다. 키 추출 함수를 지정할 수도 있다.

```java
Flux.just("A", "B", "A", "C", "B").distinct();            // "A", "B", "C"
userFlux.distinct(User::getName);                           // 이름 기준 중복 제거
```

### take / skip

`take(n)`은 처음 n개만, `skip(n)`은 처음 n개를 건너뛴다. Duration 기반 변형도 있다.

```java
Flux.range(1, 10).take(3);    // 1, 2, 3
Flux.range(1, 10).skip(3);    // 4, 5, 6, 7, 8, 9, 10
Flux.interval(Duration.ofSeconds(1)).take(Duration.ofSeconds(5));
```

```
take(3): ──(1)──(2)──(3)──|──>   (이후 상류 취소)
```

### next / last / elementAt

```java
Flux.just("A", "B", "C").next();         // Mono<"A">
Flux.just("A", "B", "C").last();         // Mono<"C">
Flux.just("A", "B", "C").elementAt(1);   // Mono<"B">
```

---

## A.4 결합 연산자 (Combining Operators)

여러 스트림을 하나로 합친다. 합치는 방식에 따라 결과가 크게 달라진다.

| 연산자 | 설명 | 순서 보장 | 동시 구독 |
|--------|------|-----------|-----------|
| `zip` / `zipWith` | 각 소스의 요소를 쌍으로 결합 | 예 | 예 |
| `merge` / `mergeWith` | 도착 순서대로 인터리빙 | 아니오 | 예 |
| `concat` / `concatWith` | 순차적으로 연결 | 예 | 아니오 |
| `combineLatest` | 각 소스의 최신 값을 결합 | - | 예 |

### zip / zipWith

여러 소스의 요소를 **위치(인덱스) 기준**으로 쌍을 만든다. 가장 짧은 소스가 완료되면 전체가 완료된다.

```java
Flux<String> names = Flux.just("Alice", "Bob");
Flux<Integer> ages = Flux.just(30, 25);
Flux<String> result = Flux.zip(names, ages, (n, a) -> n + " is " + a);
// "Alice is 30", "Bob is 25"
```

```
소스1:  ──(Alice)──(Bob)──|──>
소스2:  ──(30)──(25)──|──>
결과:   ──(Alice 30)──(Bob 25)──|──>
```

### merge / mergeWith

여러 소스를 **동시에** 구독하고, 도착 순서대로 발행한다.

```java
Flux<String> merged = Flux.merge(
    Flux.just("A", "B").delayElements(Duration.ofMillis(100)),
    Flux.just("1", "2").delayElements(Duration.ofMillis(150)));
// 가능한 결과: "A", "1", "B", "2"
```

```
소스1:  ──(A)────(B)──|──>
소스2:  ────(1)────(2)──|──>
결과:   ──(A)──(1)──(B)──(2)──|──>
```

### concat / concatWith

첫 번째 소스가 완료된 후 두 번째 소스를 구독한다. 순서가 완벽하게 보장된다.

```java
Flux<String> concat = Flux.concat(Flux.just("A", "B"), Flux.just("C", "D"));
// 결과: "A", "B", "C", "D" (항상 이 순서)
```

```
소스1:  ──(A)──(B)──|
소스2:              ──(C)──(D)──|──>
결과:   ──(A)──(B)──(C)──(D)──|──>
```

### combineLatest

각 소스가 요소를 발행할 때마다 **다른 소스의 최신 값**과 결합한다.

```java
Flux<String> combined = Flux.combineLatest(
    Flux.just("A", "B").delayElements(Duration.ofMillis(100)),
    Flux.just(1, 2).delayElements(Duration.ofMillis(150)),
    (l, n) -> l + n);
```

```
소스1:  ──(A)────(B)────(C)──|──>
소스2:  ────(1)──────(2)──|──>
결과:   ────(A1)──(B1)──(B2)──(C2)──|──>
```

---

## A.5 에러 처리 연산자 (Error Handling Operators)

리액티브 스트림에서 에러를 복구하거나, 재시도하거나, 대체 값을 제공한다.

| 연산자 | 설명 |
|--------|------|
| `onErrorReturn` | 에러 시 대체 값을 발행하고 완료한다 |
| `onErrorResume` | 에러 시 대체 Publisher로 전환한다 |
| `onErrorMap` | 에러를 다른 예외로 변환한다 |
| `retry` | 에러 시 지정 횟수만큼 재구독한다 |
| `retryWhen` | 커스텀 재시도 전략을 적용한다 |
| `timeout` | 지정 시간 초과 시 에러를 발생시킨다 |

### onErrorReturn / onErrorResume / onErrorMap

```java
// onErrorReturn: 정적 대체 값
Mono<String> safe = callApi().onErrorReturn("기본값");
Mono<String> safe2 = callApi().onErrorReturn(TimeoutException.class, "시간 초과");

// onErrorResume: 대체 Publisher (가장 유연)
Mono<User> user = primaryDb.findUser(id)
    .onErrorResume(e -> cacheService.findUser(id));

// onErrorMap: 예외 변환
Mono<User> mapped = repository.findById(id)
    .onErrorMap(DataAccessException.class,
        e -> new UserNotFoundException("사용자 없음: " + id, e));
```

```
onErrorReturn:  소스 ──(데이터)──X    결과 ──(데이터)──(기본값)──|──>
onErrorResume:  소스 ──(데이터)──X    결과 ──(데이터)──(복구1)──(복구2)──|──>
```

### retry / retryWhen

`retry(n)`은 최대 n회 재구독한다. `retryWhen`은 지수 백오프, 재시도 조건 등을 세밀하게 제어한다.

```java
Mono<String> result = callApi().retry(3);

Mono<String> robust = callApi()
    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1))
        .maxBackoff(Duration.ofSeconds(10))
        .filter(e -> e instanceof TransientException)
        .onRetryExhaustedThrow((spec, signal) ->
            new ServiceUnavailableException("재시도 한도 초과")));
```

```
시도1: ──X    시도2: ──X    시도3: ──(결과)──|──>
```

### timeout

지정 시간 내에 요소가 발행되지 않으면 `TimeoutException`을 발생시킨다.

```java
Mono<String> result = callSlowApi().timeout(Duration.ofSeconds(5));
Mono<String> withFallback = callSlowApi()
    .timeout(Duration.ofSeconds(5), Mono.just("타임아웃 대체 응답"));
```

---

## A.6 유틸리티 연산자 (Utility Operators)

스트림 데이터를 변경하지 않으면서 부수 효과를 수행하거나, 동작을 관찰/공유한다.

| 연산자 | 설명 |
|--------|------|
| `doOnNext` | 각 요소 발행 시 부수 효과 실행 |
| `doOnError` | 에러 발생 시 부수 효과 실행 |
| `doOnComplete` | 완료 시 부수 효과 실행 |
| `doOnSubscribe` | 구독 시 부수 효과 실행 |
| `doFinally` | 종료 시(완료/에러/취소) 항상 실행 |
| `log` | 리액티브 시그널을 로깅 |
| `delayElements` | 각 요소 발행을 지정 시간만큼 지연 |
| `cache` | 결과를 캐싱하여 재구독 시 재사용 |
| `share` | 여러 구독자 간 하나의 구독 공유 (Hot) |
| `replay` | 과거 요소를 새 구독자에게 재생 |

### doOn* 시리즈

스트림의 시그널을 관찰하되 스트림 자체를 변경하지 않는다. 로깅, 메트릭 수집에 사용한다.

```java
Flux<User> pipeline = userService.findAll()
    .doOnSubscribe(sub -> log.info("사용자 조회 시작"))
    .doOnNext(user -> log.debug("사용자 발행: {}", user.getName()))
    .doOnError(e -> log.error("사용자 조회 실패", e))
    .doOnComplete(() -> log.info("사용자 조회 완료"));
```

### doFinally

스트림이 어떤 이유로든 종료될 때 실행된다. 리소스 정리에 적합하다.

```java
Flux<Data> stream = dataSource.stream()
    .doFinally(signalType -> {
        log.info("종료 원인: {}", signalType); // ON_COMPLETE, ON_ERROR, CANCEL
        resourceCleanup();
    });
```

### log

리액티브 시그널을 SLF4J 로거로 출력한다. 디버깅 시 파이프라인 동작을 추적할 때 유용하다.

```java
Flux<Integer> traced = Flux.range(1, 3).log("my.category").map(i -> i * 10);
// [my.category] onNext(1) -> [after.map] onNext(10) -> ...
```

### delayElements / cache

```java
Flux.just("A", "B", "C").delayElements(Duration.ofMillis(500));  // 500ms 간격 발행
Mono<Config> config = configService.load().cache(Duration.ofMinutes(5)); // 5분 캐싱
```

### share / replay

`share`는 여러 구독자가 하나의 구독을 공유한다. `replay`는 과거 요소를 새 구독자에게 재생한다.

```java
Flux<Long> shared = Flux.interval(Duration.ofSeconds(1)).share();
// 이후 구독자는 진행 중인 스트림에 합류 (과거 요소 유실)

Flux<Long> replayed = Flux.interval(Duration.ofSeconds(1))
    .replay(3).autoConnect();
// 새 구독자에게 최근 3개 요소를 재생 후 실시간 합류
```

---

## A.7 배압 연산자 (Backpressure Operators)

생산자의 발행 속도가 소비자의 처리 속도를 초과할 때 초과분을 제어한다.

| 연산자 | 초과 요소 처리 방식 |
|--------|---------------------|
| `onBackpressureBuffer` | 내부 버퍼에 저장 (용량 초과 시 에러 또는 드롭) |
| `onBackpressureDrop` | 즉시 폐기 |
| `onBackpressureLatest` | 최신 1개만 유지, 나머지 폐기 |
| `limitRate` | 하류의 request 크기를 제한 |

### onBackpressureBuffer / onBackpressureDrop / onBackpressureLatest

```java
// 버퍼: 최대 1000개 저장
Flux<Integer> buffered = fastProducer.onBackpressureBuffer(1000);

// 드롭: 초과분 즉시 폐기
Flux<SensorData> dropped = sensorFlux
    .onBackpressureDrop(d -> metrics.increment("sensor.dropped"));

// 최신: 최신 1개만 유지 (센서/주가 데이터에 적합)
Flux<StockPrice> latest = priceStream.onBackpressureLatest();
```

```
onBackpressureLatest:
생산자: ──(1)(2)(3)(4)(5)────(6)──>
소비자:    request(1)      request(1)
결과:   ──(1)────────────(5)──(6)──>   (2,3,4 폐기)
```

### limitRate

하류가 상류에 요청하는 `request(n)` 크기를 제한한다. 프리페치와 보충 전략을 적용한다.

```java
Flux<Data> controlled = dataFlux.limitRate(100);          // 100개씩 요청
Flux<Data> precise = dataFlux.limitRate(100, 50);         // prefetch 100, lowTide 50
```

---

## A.8 연산자 선택 가이드

상황에 따라 어떤 연산자를 사용할지 빠르게 판단하기 위한 의사 결정표이다.

| 요구 사항 | 추천 연산자 |
|-----------|-------------|
| 동기적 1:1 변환 | `map` |
| 비동기 변환, 순서 무관, 최대 처리량 | `flatMap` |
| 비동기 변환, 순서 보장, 병렬 실행 | `flatMapSequential` |
| 비동기 변환, 순서 보장, 직렬 실행 | `concatMap` |
| 최신 입력만 유효 (이전 결과 취소) | `switchMap` |
| N개 소스를 위치별로 쌍 만들기 | `zip` |
| 도착 순서대로 인터리빙 | `merge` |
| 소스를 순차적으로 이어 붙이기 | `concat` |
| 각 소스의 최신 값 결합 | `combineLatest` |
| 에러 시 정적 대체 값 | `onErrorReturn` |
| 에러 시 대체 Publisher 실행 | `onErrorResume` |
| 에러를 다른 예외로 변환 | `onErrorMap` |
| 단순 재시도 | `retry` |
| 백오프/조건부 재시도 | `retryWhen` |
| 모든 요소 보존 (배압) | `onBackpressureBuffer` |
| 유실 허용 (배압) | `onBackpressureDrop` |
| 최신 값만 필요 (배압) | `onBackpressureLatest` |

---

## A.9 자주 사용하는 연산자 조합 패턴

### 패턴 1: 안전한 외부 API 호출

```java
Mono<Response> safeCall = webClient.get()
    .uri("/api/data").retrieve().bodyToMono(Response.class)
    .timeout(Duration.ofSeconds(5))
    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1)))
    .onErrorResume(e -> Mono.just(Response.fallback()))
    .doOnError(e -> log.error("API 호출 최종 실패", e));
```

### 패턴 2: 병렬 호출 후 결합

```java
Mono<Dashboard> dashboard = Mono.zip(
    userService.getProfile(userId),
    orderService.getRecentOrders(userId),
    notificationService.getUnread(userId)
).map(t -> new Dashboard(t.getT1(), t.getT2(), t.getT3()));
```

### 패턴 3: 조건부 스트림 처리

```java
Flux<ProcessedItem> pipeline = itemFlux
    .filterWhen(item -> validationService.isValid(item))
    .flatMap(item -> enrichService.enrich(item))
    .onErrorContinue((e, item) -> log.warn("항목 처리 실패: {}", item))
    .collectList()
    .flatMapMany(items -> saveAll(items));
```

### 패턴 4: 캐싱과 공유

```java
Mono<Config> sharedConfig = configService.load()
    .cache(Duration.ofMinutes(10))
    .doOnSubscribe(s -> log.debug("설정 조회"));
// 여러 곳에서 구독해도 10분간 한 번만 로딩
```

---

> **참고**: 이 부록은 Reactor 3.x 기준으로 작성되었다. 각 연산자의 전체 시그니처와 오버로드 변형은 [Project Reactor 공식 문서](https://projectreactor.io/docs/core/release/api/)를 참조하라.
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
# 부록 D. 참고 자료 및 추천 학습 경로

이 부록에서는 Spring WebFlux와 리액티브 프로그래밍을 더 깊이 학습하기 위한 참고 자료와 체계적인 학습 경로를 안내한다. 각 자료는 카테고리별로 정리하였으며, 실무에서 활용할 수 있는 실질적인 내용을 중심으로 선별하였다.

---

## D.1 공식 문서

공식 문서는 가장 정확하고 최신의 정보를 제공하는 1차 자료다. 새로운 기능이나 변경 사항을 확인할 때 반드시 공식 문서를 먼저 참고하는 습관을 들이자.

### Spring WebFlux

- **Spring Framework Reference - Web Reactive**: https://docs.spring.io/spring-framework/reference/web/webflux.html
  - WebFlux의 아키텍처, 핸들러 함수, 라우터 함수, WebClient 등 핵심 개념을 다룬다.
  - 어노테이션 기반 컨트롤러와 함수형 엔드포인트의 차이를 이해하는 데 필수적이다.

- **Spring Boot Reference - Reactive Web**: https://docs.spring.io/spring-boot/reference/web/reactive.html
  - Spring Boot 환경에서 WebFlux를 자동 구성하는 방법과 설정 옵션을 설명한다.

### Project Reactor

- **Reactor Core Reference Guide**: https://projectreactor.io/docs/core/release/reference/
  - Mono와 Flux의 상세 동작 원리, 연산자 체인, 스케줄러, 에러 처리 전략을 포괄적으로 다룬다.
  - 리액티브 스트림의 기본 원리를 이해하는 데 가장 중요한 문서다.

- **Reactor Operator Reference**: https://projectreactor.io/docs/core/release/api/
  - 모든 연산자의 마블 다이어그램과 사용 예제를 제공한다.
  - 실무에서 적절한 연산자를 선택할 때 수시로 참고하게 된다.

### Spring Data MongoDB

- **Spring Data MongoDB Reference**: https://docs.spring.io/spring-data/mongodb/reference/
  - ReactiveMongoRepository, ReactiveMongoTemplate의 사용법과 쿼리 작성 방법을 설명한다.
  - Tailable Cursor, Change Stream 등 리액티브 전용 기능도 포함되어 있다.

### MongoDB

- **MongoDB Manual**: https://www.mongodb.com/docs/manual/
  - 인덱싱, 집계 파이프라인, 트랜잭션, 레플리카 셋 등 MongoDB의 핵심 기능을 다룬다.

- **MongoDB Reactive Streams Driver**: https://www.mongodb.com/docs/languages/java/reactive-streams-driver/current/
  - Java Reactive Streams 드라이버의 사용법과 연결 풀 설정, 성능 튜닝 방법을 제공한다.

### Spring Security

- **Spring Security Reactive**: https://docs.spring.io/spring-security/reference/reactive/index.html
  - WebFlux 환경에서의 인증/인가 설정, SecurityWebFilterChain 구성, OAuth2 리액티브 지원을 설명한다.
  - 서블릿 기반 보안 설정과의 차이점을 명확히 이해할 수 있다.

---

## D.2 추천 서적

### 리액티브 프로그래밍

- **"Reactive Programming with RxJava"** - Tomasz Nurkiewicz, Ben Christensen (O'Reilly)
  - RxJava 기반이지만 리액티브 프로그래밍의 핵심 개념과 패턴을 깊이 있게 다룬다.
  - Reactor와 연산자 구조가 유사하므로 개념 이해에 큰 도움이 된다.

- **"Reactive Streams in Java"** - Adam L. Davis (Apress)
  - 리액티브 스트림 명세부터 Reactor, RxJava, Akka Streams까지 비교하며 설명한다.
  - 짧은 분량으로 핵심을 빠르게 파악하기 좋다.

- **"Hands-On Reactive Programming in Spring 5"** - Oleh Dokuka, Igor Lozynskyi (Packt)
  - Spring WebFlux와 Project Reactor를 실습 중심으로 학습할 수 있다.
  - 리액티브 시스템 설계 원칙과 테스트 전략까지 포괄한다.

### Spring 프레임워크

- **"Spring in Action, 6th Edition"** - Craig Walls (Manning)
  - Spring Boot와 WebFlux를 포함한 최신 Spring 생태계를 전반적으로 다룬다.
  - WebFlux 챕터에서 리액티브 웹 개발의 기초를 잡을 수 있다.

- **"Spring Boot Up & Running"** - Mark Heckler (O'Reilly)
  - Spring Boot의 자동 구성 원리와 실무 활용법을 체계적으로 설명한다.

- **"Cloud Native Spring in Action"** - Thomas Vitale (Manning)
  - 클라우드 네이티브 환경에서 Spring 애플리케이션을 설계하고 배포하는 방법을 다룬다.
  - Kubernetes, GraalVM Native Image 등 최신 배포 기술과의 통합을 설명한다.

### MongoDB

- **"MongoDB: The Definitive Guide, 3rd Edition"** - Shannon Bradshaw 외 (O'Reilly)
  - 데이터 모델링, 인덱싱 전략, 레플리케이션, 샤딩 등 MongoDB의 모든 영역을 깊이 있게 다룬다.

- **"MongoDB in Action, 2nd Edition"** - Kyle Banker 외 (Manning)
  - 실무 시나리오 중심으로 MongoDB를 학습하기에 적합하다.

### Java 및 Kotlin

- **"Modern Java in Action"** - Raoul-Gabriel Urma 외 (Manning)
  - 람다, 스트림, CompletableFuture 등 리액티브 프로그래밍의 기반이 되는 Java 기능을 다룬다.

- **"Java Concurrency in Practice"** - Brian Goetz 외 (Addison-Wesley)
  - 동시성 프로그래밍의 근본 원리를 이해하기 위한 필독서다.
  - 리액티브 모델이 해결하려는 문제의 본질을 깊이 이해할 수 있다.

- **"Kotlin in Action, 2nd Edition"** - Roman Elizarov 외 (Manning)
  - 코루틴과 Flow를 포함한 Kotlin의 핵심 기능을 체계적으로 설명한다.

---

## D.3 온라인 강의 및 튜토리얼

### 온라인 강의 플랫폼

- **Udemy - "Build Reactive MicroServices using Spring WebFlux/SpringBoot"** (Dilip Sundarraj)
  - WebFlux, WebClient, 리액티브 MongoDB를 활용한 마이크로서비스 구축을 실습한다.

- **Udemy - "Reactive Programming in Modern Java using Project Reactor"** (Dilip Sundarraj)
  - Project Reactor의 Mono, Flux 연산자를 단계별로 학습할 수 있다.

- **Coursera - "Reactive Programming"** (EPFL/Scala 기반)
  - 리액티브 프로그래밍의 학술적 기초를 다지고 싶을 때 추천한다.

- **Spring Academy**: https://spring.academy/
  - VMware(Broadcom)에서 운영하는 공식 Spring 학습 플랫폼이다.
  - Spring Boot, Spring Security 등 공식 인증 과정을 무료로 수강할 수 있다.

### YouTube 채널

- **Spring Developer** (https://www.youtube.com/@SpringSourceDev)
  - SpringOne 컨퍼런스 발표 영상, 기술 데모를 공식적으로 제공한다.

- **Java Brains** (https://www.youtube.com/@Java.Brains)
  - Spring Boot, 리액티브 프로그래밍을 초보자 관점에서 친절하게 설명한다.

- **Telusko** (https://www.youtube.com/@Telusko)
  - Java와 Spring 생태계를 폭넓게 다루는 인도 기반 채널이다.

### 블로그 및 기술 아티클

- **Baeldung** (https://www.baeldung.com/)
  - Spring, Java 관련 튜토리얼의 보고다. WebFlux, Reactor, MongoDB 관련 글이 풍부하다.
  - 코드 예제가 실용적이며 지속적으로 업데이트된다.

- **Spring Blog** (https://spring.io/blog)
  - 새로운 릴리스 정보, 마이그레이션 가이드, 모범 사례를 공식적으로 발행한다.

- **Project Reactor Blog** (https://projectreactor.io/blog)
  - Reactor의 새 기능, 성능 개선 사항, 활용 팁을 제공한다.

- **DZone** (https://dzone.com/)
  - 리액티브 프로그래밍, 마이크로서비스 아키텍처 관련 실무 아티클이 많다.

---

## D.4 커뮤니티 및 도구

### GitHub 레포지토리

- **spring-projects/spring-framework**: https://github.com/spring-projects/spring-framework
  - WebFlux 모듈의 소스 코드를 직접 읽으며 내부 동작을 이해할 수 있다.

- **reactor/reactor-core**: https://github.com/reactor/reactor-core
  - Reactor의 핵심 구현체. 연산자의 실제 동작 원리를 파악하는 데 유용하다.

- **spring-projects/spring-data-examples**: https://github.com/spring-projects/spring-data-examples
  - 리액티브 MongoDB를 포함한 다양한 Spring Data 모듈의 예제 코드를 제공한다.

- **hantsy/spring-reactive-sample**: https://github.com/hantsy/spring-reactive-sample
  - WebFlux 기반 애플리케이션의 다양한 구성 패턴을 보여주는 종합 예제 프로젝트다.

### Stack Overflow 태그

실무에서 문제에 부딪혔을 때 다음 태그를 활용하면 관련 질문과 답변을 효율적으로 찾을 수 있다.

| 태그 | 설명 |
|------|------|
| `spring-webflux` | WebFlux 관련 전반적인 질문 |
| `project-reactor` | Reactor 연산자, 에러 처리 관련 질문 |
| `spring-data-mongodb` | 리액티브 MongoDB 쿼리, 매핑 관련 질문 |
| `reactive-streams` | 리액티브 스트림 명세, 백프레셔 관련 질문 |
| `spring-security` | 리액티브 보안 설정 관련 질문 |
| `r2dbc` | 리액티브 관계형 데이터베이스 관련 질문 |

### 커뮤니티

- **Spring Community Gitter/GitHub Discussions**: Spring 프로젝트별 Discussions 탭에서 공식 질의응답이 이루어진다.
- **Reddit r/java, r/spring**: Java 및 Spring 관련 기술 토론과 최신 동향을 파악할 수 있다.
- **Korean Spring User Group**: 한국 Spring 사용자 모임에서 한국어로 된 기술 교류가 가능하다.

---

## D.5 추천 학습 경로

리액티브 웹 개발을 처음 시작하는 개발자부터 고급 최적화를 목표로 하는 개발자까지, 단계별 학습 경로를 제시한다.

### 초급 단계 (약 8~12주)

**목표**: Java와 Spring Boot의 기초를 다지고, MongoDB의 기본 사용법을 익힌다.

| 주차 | 학습 내용 | 주요 자료 |
|------|-----------|-----------|
| 1~2주 | Java 핵심 문법, 람다, 스트림 API | Modern Java in Action |
| 3~4주 | Spring Boot 기초, REST API 구축 | Spring Academy, Baeldung |
| 5~6주 | MongoDB 기초, CRUD 연산, 인덱싱 | MongoDB Manual, MongoDB University |
| 7~8주 | Spring Data MongoDB 기본 사용법 | 공식 문서, Spring Data Examples |
| 9~12주 | 간단한 CRUD 프로젝트 완성 | GitHub 예제 프로젝트 참고 |

**이정표**: Spring Boot + MongoDB로 간단한 REST API 서버를 독립적으로 구축할 수 있어야 한다.

### 중급 단계 (약 8~12주)

**목표**: 리액티브 프로그래밍 패러다임을 이해하고, WebFlux와 Reactor로 비동기 애플리케이션을 개발한다.

| 주차 | 학습 내용 | 주요 자료 |
|------|-----------|-----------|
| 1~2주 | 리액티브 스트림 개념, 백프레셔 원리 | Reactor Reference Guide |
| 3~4주 | Mono, Flux 연산자 심화 학습 | Reactor Operator Reference |
| 5~6주 | WebFlux 컨트롤러, 함수형 엔드포인트 | Spring WebFlux 공식 문서 |
| 7~8주 | WebClient, 리액티브 보안 설정 | Spring Security Reactive 문서 |
| 9~10주 | 리액티브 MongoDB 연동, Change Stream | Spring Data MongoDB Reference |
| 11~12주 | 리액티브 테스트 전략 (StepVerifier, WebTestClient) | 본서 관련 챕터 |

**이정표**: WebFlux + 리액티브 MongoDB로 완전한 비동기 애플리케이션을 구축하고, 테스트 코드를 작성할 수 있어야 한다.

### 고급 단계 (약 8~16주)

**목표**: 프로덕션 수준의 성능 최적화, 모니터링, 배포 파이프라인을 구축한다.

| 주차 | 학습 내용 | 주요 자료 |
|------|-----------|-----------|
| 1~3주 | 성능 프로파일링, 메모리 최적화, 백프레셔 튜닝 | 본서 관련 챕터, Reactor 공식 문서 |
| 4~6주 | Micrometer, Prometheus, Grafana 모니터링 구축 | Spring Boot Actuator 공식 문서 |
| 7~9주 | Docker 컨테이너화, Kubernetes 배포 | Cloud Native Spring in Action |
| 10~12주 | GraalVM Native Image 빌드 및 최적화 | Spring Boot AOT 공식 문서 |
| 13~16주 | 대규모 트래픽 시나리오 부하 테스트 및 튜닝 | Gatling, k6 공식 문서 |

**이정표**: 프로덕션 환경에서 안정적으로 운영 가능한 리액티브 시스템을 설계하고 배포할 수 있어야 한다.

---

## D.6 관련 기술 스택 로드맵

본서의 내용을 마스터한 후, 다음 기술들을 추가로 학습하면 리액티브 생태계에 대한 이해를 확장할 수 있다.

### Spring Cloud Gateway

- **개요**: 리액티브 기반 API 게이트웨이로, WebFlux 위에 구축되어 있다.
- **학습 포인트**: 라우트 설정, 필터 체인, 속도 제한(Rate Limiting), 서킷 브레이커 통합
- **공식 문서**: https://docs.spring.io/spring-cloud-gateway/reference/
- **선수 지식**: WebFlux, Spring Security Reactive
- **활용 사례**: 마이크로서비스 아키텍처에서 단일 진입점 역할을 하며, 인증, 로깅, 트래픽 제어를 중앙화한다.

### Apache Kafka와 리액티브 연동

- **개요**: 대용량 이벤트 스트리밍 플랫폼과 리액티브 시스템의 결합이다.
- **학습 포인트**: Reactor Kafka, Spring Cloud Stream, 이벤트 드리븐 아키텍처
- **공식 문서**: https://projectreactor.io/docs/kafka/release/reference/
- **선수 지식**: Reactor 연산자, 백프레셔 개념, Kafka 기초
- **활용 사례**: 실시간 데이터 파이프라인, CQRS 패턴, 이벤트 소싱 구현에 활용된다.

### GraphQL과 WebFlux

- **개요**: REST API의 오버페칭/언더페칭 문제를 해결하는 쿼리 언어를 리액티브로 제공한다.
- **학습 포인트**: Spring for GraphQL, 스키마 정의, DataLoader, Subscription(실시간 스트리밍)
- **공식 문서**: https://docs.spring.io/spring-graphql/reference/
- **선수 지식**: WebFlux, GraphQL 기초 문법
- **활용 사례**: 복잡한 데이터 관계를 가진 API에서 클라이언트가 필요한 데이터만 정확히 요청할 수 있다. Subscription을 통해 실시간 업데이트도 가능하다.

### Kotlin Coroutines와 WebFlux

- **개요**: Kotlin의 코루틴을 활용하여 리액티브 코드를 동기 스타일로 작성한다.
- **학습 포인트**: suspend 함수, Flow, 코루틴 컨텍스트, Spring WebFlux의 코루틴 지원
- **공식 문서**: https://docs.spring.io/spring-framework/reference/languages/kotlin/coroutines.html
- **선수 지식**: Kotlin 기본 문법, WebFlux 기초
- **활용 사례**: Reactor의 연산자 체인 대신 순차적 코드 스타일로 비동기 로직을 작성하여 가독성을 높인다. Mono는 suspend 함수로, Flux는 Flow로 자연스럽게 변환된다.

### 추가로 주목할 기술

- **R2DBC**: 리액티브 관계형 데이터베이스 접근. PostgreSQL, MySQL 등을 비동기로 사용할 때 필요하다.
- **RSocket**: 리액티브 스트림 기반의 양방향 통신 프로토콜. 마이크로서비스 간 효율적인 통신에 활용된다.
- **Testcontainers**: 통합 테스트에서 MongoDB, Kafka 등을 Docker 컨테이너로 실행하여 실제 환경과 동일한 테스트를 수행한다.
- **Virtual Threads (Project Loom)**: Java 21에 도입된 가상 스레드와 리액티브 모델의 관계를 이해하고, 적절한 동시성 모델을 선택하는 판단력을 기른다.

---

> **학습 팁**: 기술 서적이나 문서를 읽는 것만으로는 충분하지 않다. 반드시 직접 코드를 작성하고, 실행하고, 실패를 경험하면서 학습해야 한다. 특히 리액티브 프로그래밍은 사고 방식의 전환이 필요하므로, 작은 프로젝트부터 시작하여 점진적으로 복잡도를 높여 나가는 것을 권장한다.
