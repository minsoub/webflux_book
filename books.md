# Chapter 1. 리액티브 프로그래밍 소개

현대 소프트웨어 시스템이 직면한 현실을 생각해 보자. 수백만 사용자의 동시 요청을 처리하고, 밀리초 단위의 응답 시간을 보장하며, 24/7 무중단 운영을 해야 한다는 것은 정말 과도한 요구사항처럼 들린다. 그런데 이미 우리는 그런 시스템들이 존재한다는 것을 알고 있다. 전통적인 명령형 프로그래밍 모델만으로는 이런 요구사항을 충족하기 어렵다는 것도 경험상 알 수 있기 때문이다. 이 장에서는 리액티브 프로그래밍의 핵심 개념을 살펴보면서, Spring WebFlux가 왜 이 패러다임을 선택했는지 그 이유를 함께 이해해 보자.

---

## 1.1 리액티브 프로그래밍이란?

### 1.1.1 정의와 핵심 원칙

리액티브 프로그래밍(Reactive Programming)은 **데이터 스트림과 변화의 전파**에 초점을 맞춘 프로그래밍 패러다임인데, 이 둘의 차이를 한 문장으로 표현하면 쉽게 이해할 수 있다. 기존의 명령형 프로그래밍이 "이 값을 가져와서 이렇게 처리하라"라고 지시하는 방식이라면, 리액티브 프로그래밍은 "데이터가 흘러오면 이렇게 반응하라"라고 선언하는 방식이기 때문이다.

스프레드시트를 떠올려 보자. 셀 A1에 10, B1에 20이 있고, C1에 `=A1+B1`이라는 수식을 넣으면 C1은 30이 된다. 이후 A1의 값을 50으로 바꾸면 C1은 자동으로 70으로 갱신된다. 이것이 리액티브 프로그래밍의 본질이다. C1은 A1과 B1의 **변화에 반응**한다.

이러한 패러다임의 핵심 원칙을 정리하면 대략 이렇게 된다.

- **비동기 데이터 스트림**: 모든 데이터를 시간에 따라 흐르는 스트림으로 모델링하기 때문에 순간 모든 데이터가 메모리에 있을 필요가 없다.
- **변화의 전파**: 상류(upstream)의 변화가 하류(downstream)로 자동 전파되므로 중간에 신경 쓸 필요가 줄어든다.
- **선언적 구성**: 데이터를 어떻게(how) 처리할지가 아니라, 무엇을(what) 할지 선언하는 방식으로 더 간결한 코드가 된다.
- **논블로킹 실행**: 스레드를 차단하지 않고 비동기적으로 작업을 수행할 수 있어 리소스를 훨씬 효율적으로 쓸 수 있다.

### 1.1.2 리액티브 선언문 (Reactive Manifesto)

2014년에 발표된 리액티브 선언문이 있는데, 여기서는 리액티브 시스템이 갖추어야 할 네 가지 속성을 명확히 정의하고 있다.

| 속성 | 설명 |
|------|------|
| **응답성(Responsive)** | 시스템이 가능한 한 즉각적으로 응답한다. 응답성은 사용자 경험의 핵심이다. |
| **탄력성(Resilient)** | 장애가 발생해도 시스템이 응답성을 유지한다. 장애는 각 컴포넌트 내부에 격리된다. |
| **유연성(Elastic)** | 작업 부하가 변화해도 시스템이 응답성을 유지한다. 리소스를 동적으로 확장/축소한다. |
| **메시지 기반(Message Driven)** | 비동기 메시지 전달을 통해 컴포넌트 간 느슨한 결합을 달성한다. |

흥미롭게도 이 네 가지 속성은 독립적이지 않다. 메시지 기반 아키텍처가 토대가 되고, 그 위에 유연성과 탄력성이 구현되며, 최종적으로 응답성이 확보되는 일종의 피라미드 구조를 갖추고 있기 때문이다.

### 1.1.3 데이터 스트림과 변화의 전파

리액티브 프로그래밍에서의 가장 중요한 개념 하나는 "모든 것은 스트림"이라는 것이다. 사용자 클릭 이벤트, HTTP 요청, 데이터베이스 쿼리 결과, 센서 데이터 등 일반적으로 우리가 마주치는 모든 데이터를 시간축 위에 놓인 스트림으로 표현할 수 있다.

스트림이 전달하는 신호는 딱 세 가지로 나뉜다.

1. **onNext(item)**: 다음 데이터 항목을 전달할 때 발행되는 신호다.
2. **onError(error)**: 오류가 발생했을 때 발행되며, 이 신호가 나오면 스트림은 종료된다.
3. **onComplete()**: 더 이상 전달할 데이터가 없을 때 발행되며, 이것도 스트림의 정상적인 종료를 의미한다.

```
시간 →
──[item1]──[item2]──[item3]──|──>   (정상 완료: | = onComplete)
──[item1]──[item2]──X──>            (오류 발생: X = onError)
```

### 1.1.4 옵저버 패턴과의 관계

사실 리액티브 프로그래밍은 이미 존재하는 GoF 디자인 패턴의 옵저버 패턴(Observer Pattern)을 확장한 것이라고 할 수 있다. 옵저버 패턴에서는 Subject가 상태 변화를 Observer에게 통지하는 방식을 사용하는데, 리액티브는 이것을 더 잘 구조화한 것이라고 봐도 된다.

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

그래서 리액티브 프로그래밍은 이 옵저버 패턴에 세 가지를 더 추가했는데, 이것이 정말 핵심적인 개선이라고 할 수 있다.

- **완료 신호**: 데이터 발행이 끝났음을 구독자에게 명시적으로 알릴 수 있도록 한 것이다.
- **오류 처리**: 오류를 스트림의 일부로 다루어 예외 처리처럼 흐름 제어를 할 수 있게 됐다.
- **배압(Backpressure)**: 구독자가 처리할 수 있는 속도에 맞춰 데이터 발행 속도를 조절할 수 있다는 게 가장 중요하다.

---

## 1.2 명령형 프로그래밍 vs 리액티브 프로그래밍

### 1.2.1 명령형 방식의 코드 예시

구체적인 예를 통해 느껴보자. 사용자 목록에서 활성 사용자를 필터링하고, 이름을 대문자로 변환하여 정렬하는 로직을 명령형으로 작성하면 이렇게 된다.

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

이 코드는 읽기 쉽고 직관적이지만, 한 가지 문제가 있다. 처리 시작 전에 모든 사용자 데이터가 메모리에 준비되어 있어야 하고, 정렬이 완료될 때까지 호출 스레드가 계속 차단된다는 것이다.

### 1.2.2 같은 로직의 리액티브 코드 예시

같은 로직을 Project Reactor(리액티브 라이브러리)를 사용해서 작성해 보면 코드가 어떻게 달라질까?

```java
// 리액티브 방식: "무엇을" 할지 선언적으로 기술
public Flux<String> getActiveUserNames(Flux<User> users) {
    return users
            .filter(User::isActive)
            .map(user -> user.getName().toUpperCase())
            .sort();
}
```

보다시피 리액티브 코드는 훨씬 간결하다. 그리고 데이터가 도착할 때마다 파이프라인을 통해 처리되므로 전체 데이터가 메모리에 있어야 한다는 제약이 없다. 무엇보다 호출 스레드가 차단되지 않는다는 것이 가장 큰 장점이다.

### 1.2.3 동기 vs 비동기, 블로킹 vs 논블로킹

실무에서 자주 보는 혼동 사항 중 하나인데, 이 두 쌍의 개념은 서로 다른 차원의 개념이라는 것을 명확히 해야 한다.

**동기(Synchronous) vs 비동기(Asynchronous)**는 호출자 입장에서 결과를 기다리는 방식에 관한 것이다.

- 동기: 호출자가 결과가 반환될 때까지 기다린다는 것이 기본이다.
- 비동기: 호출자가 결과를 기다리지 않고, 결과가 준비되면 콜백이나 이벤트로 통지받는 방식이다.

**블로킹(Blocking) vs 논블로킹(Non-blocking)**은 호출된 함수 입장에서 스레드를 점유하는 방식에 관한 것인데, 동기/비동기와는 다르다.

- 블로킹: 호출된 함수가 작업을 완료할 때까지 스레드를 점유하고 있다.
- 논블로킹: 호출된 함수가 즉시 반환하기 때문에 스레드를 다른 작업에 활용할 수 있다.

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

리액티브 스트림이란 비동기 스트림 처리를 위한 표준 인터페이스 명세를 말한다. Netflix, Lightbend, Pivotal 같은 대형 기업들이 공동으로 개발했으며, Java 9부터는 `java.util.concurrent.Flow` 클래스로 JDK에 포함되기도 했다.

흥미로운 것은 이 표준이 단 4개의 인터페이스로 모든 것을 설명한다는 점이다.

### 1.3.2 Publisher

Publisher는 데이터를 생산하는 주체라고 생각하면 된다. 혼자 일방적으로 데이터를 내보내는 게 아니라, 구독자의 요청에 따라 데이터를 발행하는 방식으로 동작한다.

```java
public interface Publisher<T> {
    void subscribe(Subscriber<? super T> subscriber);
}
```

`subscribe()` 메서드는 구독자를 등록한다. 호출되면 Publisher는 `Subscriber.onSubscribe()`를 호출하여 Subscription 객체를 전달한다.

### 1.3.3 Subscriber

Subscriber는 데이터를 소비하는 쪽인데, Publisher로부터 데이터를 수신하고 처리하는 역할을 한다. 네 개의 메서드로 모든 상황을 처리하도록 설계되어 있다.

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

Publisher와 Subscriber 사이의 연결을 나타내는 인터페이스인데, 사실 배압 제어의 핵심이 여기에 있다고 할 수 있다.

```java
public interface Subscription {
    void request(long n);
    void cancel();
}
```

- `request(n)`: Publisher에게 n개의 데이터를 명시적으로 요청하는 것인데, 이것이 배압의 핵심 메커니즘이 된다.
- `cancel()`: 구독을 중단하고 싶을 때 호출하면, 더 이상 데이터를 수신하지 않게 된다.

### 1.3.5 Processor

Processor는 Publisher와 Subscriber의 두 역할을 동시에 하는 인터페이스다. 데이터를 수신하여 변환한 뒤 다시 발행하는 중간 처리 단계에 쓰인다고 보면 된다.

```java
public interface Processor<T, R> extends Subscriber<T>, Publisher<R> {
}
```

### 1.3.6 상호작용 흐름

이 네 인터페이스가 실제로 어떻게 상호작용하는지 순서대로 정리해 보면 아래와 같은 흐름이 된다.

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

이 책의 나머지 내용에서는 Spring WebFlux의 기본 구현체인 **Project Reactor**를 주로 다룬다. 따라서 이후 코드 예시와 설명은 모두 이를 기반으로 한다.

---

## 1.4 배압(Backpressure)의 개념

### 1.4.1 배압이 필요한 이유

배압이 뭔지 한 문장으로 정의하면, 데이터 소비자가 생산자에게 "너무 빨리 보내지 말고 내 속도에 맞춰 달라"고 요청하는 메커니즘이다.

일상적인 비유로 설명하면, 컨베이어 벨트 위의 물건을 포장하는 작업자를 생각해 보자. 벨트가 너무 빨리 움직이면 물건이 쌓이고 바닥에 떨어진다. 작업자가 "속도를 줄여 주세요"라고 요청할 수 있어야 한다. 이것이 배압이다.

만약 배압 메커니즘이 없다면 소프트웨어 시스템에서 정말 심각한 문제들이 발생한다.

- **메모리 초과(OOM)**: 처리하지 못한 데이터가 버퍼에 계속 쌓여서 결국 메모리가 고갈되어 버린다.
- **응답 지연**: 한 컴포넌트가 과부하 상태에 빠지면 처리 속도가 급격히 떨어진다.
- **시스템 장애**: 한 컴포넌트의 과부하가 다른 컴포넌트로 전파되어 전체 시스템이 먹통이 될 수 있다.

### 1.4.2 배압 전략

이러한 배압 문제를 해결하기 위해 Project Reactor는 다양한 전략을 제공하고 있는데, 상황에 맞게 선택해서 쓸 수 있다.

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

그런데 `request()` 메서드를 사용해서 명시적으로 배압을 제어할 수도 있는데, 이렇게 하면 더 세밀한 제어가 가능해진다.

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

코드를 보면 구독자가 한 번에 10개씩만 요청하는 식으로 처리 속도를 명시적으로 제어하고 있다. 이렇게 `request(BATCH_SIZE)` 호출을 통해 배압을 직접 관리하는 것이 배압의 핵심이라고 할 수 있다.

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

이제 리액티브가 정말 필요한 이유를 실제 구체적인 예를 통해 살펴보자. 전통적인 서블릿 기반 웹 애플리케이션들은 하나의 HTTP 요청이 들어올 때마다 하나의 스레드를 할당하는 thread-per-request 모델을 사용하고 있다.

```
[요청 1] → [스레드 1] → DB 호출 (200ms 대기) → 응답
[요청 2] → [스레드 2] → API 호출 (300ms 대기) → 응답
[요청 3] → [스레드 3] → DB 호출 (200ms 대기) → 응답
  ...
[요청 201] → 스레드 풀 고갈 → 대기열에서 대기
```

이 모델의 문제점을 정리하면 생각보다 심각하다는 것을 알 수 있다.

- **스레드 풀 크기 제한**: Tomcat의 기본 스레드 풀이 200개 정도인데, 201번째 요청은 그냥 대기해야 한다.
- **I/O 대기 중 자원 낭비**: 스레드가 데이터베이스 응답을 기다리는 동안 실제로는 아무것도 안 하는데 메모리(보통 1MB 정도)는 점유하고 있다는 게 큰 문제다.
- **컨텍스트 스위칭 비용**: 스레드가 늘어날수록 OS가 이들 사이를 오가는 컨텍스트 스위칭에 드는 오버헤드가 증가한다.

### 1.5.2 리소스 효율성 비교

구체적인 숫자로 느껴보기 위해, 같은 하드웨어 위에서 10,000개의 동시 연결을 처리해야 한다는 시나리오를 생각해 보자. 두 모델 간의 차이가 정말 크다.

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

여기서 한 가지 중요한 점을 짚고 넘어가야 한다. 리액티브가 모든 상황에서 최선의 선택은 절대 아니라는 것이다. 리액티브가 정말 빛나는 경우와 오히려 과할 수 있는 경우를 명확히 구분해야 한다.

**리액티브가 정말 빛나는 경우들**

- **높은 동시 연결 수**: 채팅, 알림 푸시, 실시간 대시보드 같이 수천~수만 개의 동시 연결을 처리해야 하는 경우
- **I/O 집약적 워크로드**: 외부 API를 많이 호출하거나 데이터베이스 쿼리가 주를 이루는 경우가 대표적이다
- **스트리밍 데이터**: IoT 센서 데이터, 실시간 로그 처리, 주식 시세 같이 연속적으로 흘러들어오는 데이터
- **마이크로서비스 간 통신**: 여러 서비스 간에 비동기 메시지 교환이 자주 일어나는 구조
- **Server-Sent Events / WebSocket**: 서버가 클라이언트로 실시간 데이터를 계속 푸시해야 하는 경우

**리액티브가 과할 수 있는 경우들**

- **CPU 집약적 작업**: 이미지 처리, 복잡한 수학 연산처럼 CPU를 오래 점유해야 하는 작업
- **단순한 CRUD 애플리케이션**: 동시 사용자가 적고 비동기 흐름이 별로 필요 없는 단순한 경우
- **팀의 리액티브 경험 부족**: 학습 곡선이 가파르고 디버깅이 어려워서 팀이 감당하기 힘들 수 있다

### 1.5.4 성능 벤치마크 참고

마지막으로 성능 관점에서 한 가지 더 이해하고 넘어가야 할 것이 있다. 아래는 동시 연결 수에 따른 처리량이 어떻게 달라지는지를 개념적으로 그린 것이다.

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

흥미로운 점은 동시 연결 수가 적을 때는 Spring MVC와 WebFlux의 성능이 거의 비슷하다는 것이다. 오히려 더 간단한 MVC가 약간 더 빠를 수도 있을 정도다. 그런데 동시 연결 수가 증가하기 시작하면 상황이 180도 달라진다. MVC의 처리량은 스레드 풀 크기라는 물리적 한계에 갇혀서 증가하지 않지만, WebFlux는 적은 스레드로도 계속해서 높은 처리량을 유지할 수 있다.

---

## 정리

이 첫 번째 장에서 배운 내용들을 한데 정리하면 다음과 같다.

| 주제 | 핵심 내용 |
|------|----------|
| 리액티브 프로그래밍 | 데이터 스트림과 변화의 전파에 초점을 맞춘 비동기 프로그래밍 패러다임 |
| 리액티브 선언문 | 응답성, 탄력성, 유연성, 메시지 기반의 네 가지 속성 |
| 명령형 vs 리액티브 | 명령형은 "어떻게", 리액티브는 "무엇을" 선언. 각각의 장단점이 존재 |
| 리액티브 스트림 | Publisher, Subscriber, Subscription, Processor 4개 인터페이스로 구성된 표준 |
| 배압 | 소비자가 생산자에게 속도 조절을 요청하는 메커니즘 |
| 리액티브의 필요성 | I/O 집약적이고 높은 동시성이 요구되는 시스템에 적합 |

다음 장으로 나아가면 이 개념들이 실제로 어떻게 구현되는지 구체적으로 볼 차례다. **Project Reactor**를 깊이 있게 살펴보면서, Mono와 Flux를 어떻게 사용하는지, 주요 연산자들은 무엇인지, 그리고 실전에서 자주 쓰이는 패턴들이 무엇인지 배워보게 될 것이다.
# Chapter 2. Spring WebFlux 개요

Spring WebFlux는 Spring Framework 5에서 도입된 리액티브 웹 프레임워크다. 기존 Spring MVC가 서블릿 기반의 동기/블로킹 모델 위에 구축되었다면, WebFlux는 논블로킹 I/O와 리액티브 스트림을 기반으로 완전히 다르게 설계되었다. 이제 WebFlux의 아키텍처를 들여다보고, 내부가 어떻게 움직이는지, 그리고 실제로 이것을 써야 할 때는 언제인지 함께 살펴보자.

---

## 2.1 Spring MVC와 Spring WebFlux 비교

### 2.1.1 아키텍처 차이: 서블릿 스택 vs 리액티브 스택

Spring MVC는 Java Servlet API 위에 구축되어 있다. 클라이언트의 요청이 들어오면 서블릿 컨테이너(Tomcat, Jetty 등)는 스레드 풀에서 하나의 스레드를 할당하고, 그 스레드가 요청의 처음부터 끝까지 계속 담당하게 된다. 이 방식을 **thread-per-request** 모델이라고 부르는데, 이름 그대로 요청 하나당 스레드 하나씩 배치하는 것이다.

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

반면 Spring WebFlux는 리액티브 스택 위에서 완전히 다르게 구축되어 있다. 서블릿 API에는 의존하지 않으며, 기본 런타임으로 Netty를 사용한다. 핵심은 소수의 이벤트 루프 스레드가 많은 요청들을 논블로킹 방식으로 효율적으로 처리할 수 있다는 점이다.

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

**Spring MVC**의 스레드 모델은 직관적이긴 하지만 자원 측면에서는 비효율적이다. 동시에 200개의 요청을 처리하려면 최소 200개의 스레드를 준비해야 한다. 문제는 각 스레드가 데이터베이스 응답을 기다리는 동안에도 계속 점유되고 있다는 기 때문이다.

```
[Spring MVC - Thread-per-Request]

요청 A ──▶ Thread-1: [수신]──[처리]──[DB 대기...]──[응답]──▶ 완료
요청 B ──▶ Thread-2: [수신]──[처리]──[DB 대기...]──[응답]──▶ 완료
요청 C ──▶ Thread-3: [수신]──[처리]──[DB 대기...]──[응답]──▶ 완료
  ...
요청 N ──▶ Thread-N: (스레드 풀 고갈 → 대기 큐에서 대기)
```

**Spring WebFlux**는 이벤트 루프 방식을 채택했기 때문에 상황이 완전히 달라진다. CPU 코어 수 정도의 적은 스레드(기본적으로 코어 수 x 1)가 모든 요청을 논블로킹으로 처리할 수 있다. I/O 대기 시간 동안 해당 스레드가 다른 요청을 처리하면 되기 때문이다.

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

이를 직관적으로 이해하기 위해, 사용자를 조회하는 간단한 API를 두 가지 방식으로 구현해서 비교해보면 좋다.

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

두 방식의 핵심 차이를 표로 정리해보면 이렇다.

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

Netty는 JVM에서 동작하는 비동기 이벤트 기반 네트워크 프레임워크다. 고성능 프로토콜 서버와 클라이언트를 빠르게 구축할 수 있도록 설계되었으며, HTTP부터 WebSocket, TCP, UDP에 이르기까지 다양한 프로토콜을 모두 지원한다.

Spring WebFlux가 Netty를 기본 런타임으로 선택한 이유는 다음 몇 가지로 요약할 수 있다.

- **논블로킹 I/O**: Java NIO 기반으로 소수 스레드로 대량의 동시 연결 처리
- **이벤트 루프 모델**: 효율적인 리소스 활용과 높은 동시성
- **검증된 안정성**: Discord, Apple, Netflix 등 대규모 서비스에서 검증
- **풍부한 프로토콜 지원**: HTTP/1.1, HTTP/2, WebSocket 기본 지원

### 2.2.2 이벤트 루프(Event Loop) 모델

Netty의 이벤트 루프가 정말 핵심인데, 아주 간단히 말하면 하나의 스레드가 **셀렉터(Selector)**라는 도구를 사용해서 여러 채널(연결)의 I/O 이벤트를 감시하고 처리하는 구조다.

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

각 이벤트 루프 스레드는 다음 세 가지를 계속 반복한다.

1. **Selector로 I/O 이벤트 대기**: 등록된 채널 중에 읽거나 쓸 준비가 된 채널이 있는지 확인한다
2. **이벤트 처리**: 준비된 채널에서 데이터를 읽거나 쓴다
3. **태스크 큐 처리**: 예약되어 있던 작업들(스케줄된 태스크)을 실행한다

이 모델에서 기억할 핵심 원칙이 하나 있다. **하나의 채널은 항상 같은 이벤트 루프에 연결**된다는 것인데, 덕분에 복잡한 동기화 코드 없이도 스레드 안전성이 자동으로 보장될 수 있다.

### 2.2.3 HttpHandler, WebHandler, DispatcherHandler 파이프라인

Spring WebFlux의 내부는 여러 계층의 핸들러들이 마치 우편 처리 시스템처럼 서로 연쇄되어 있다.

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

**HttpHandler**는 가장 기본적인 계약(interface)다. 실은 `handle(ServerHttpRequest, ServerHttpResponse)` 하나의 메서드만 정의하고 있는데, Netty나 Undertow, Tomcat(서블릿 3.1+) 같은 각 서버마다 이를 구현하는 어댑터를 두고 있다.

```java
public interface HttpHandler {
    Mono<Void> handle(ServerHttpRequest request, ServerHttpResponse response);
}
```

**DispatcherHandler**는 Spring MVC의 `DispatcherServlet`을 리액티브 방식으로 다시 구현한 것이라고 보면 된다. 요청을 세 단계로 나누어 처리한다.

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

이제 클라이언트의 HTTP 요청이 들어와서 응답이 나갈 때까지 전체 여정을 따라가보자.

1. **Netty가 TCP 연결을 수락**한 다음 HTTP 요청을 파싱한다.
2. **HttpHandler 어댑터**가 Netty의 네이티브 객체들을 Spring 표준인 `ServerHttpRequest`, `ServerHttpResponse`로 변환해준다.
3. **WebHttpHandlerBuilder**가 구성한 필터 체인(`WebFilter`)이 순차적으로 실행되어 요청/응답을 가로챈다 (인증, 로깅 등).
4. **DispatcherHandler**가 `HandlerMapping`을 통해 해당 요청을 처리할 적절한 핸들러를 찾아낸다.
   - `RequestMappingHandlerMapping`: 어노테이션 기반 핸들러 찾기 (`@GetMapping` 등)
   - `RouterFunctionMapping`: 함수형 라우터 찾기
5. **HandlerAdapter**가 찾은 핸들러를 실제로 실행하고 `Mono<HandlerResult>`를 반환한다.
6. **HandlerResultHandler**가 그 결과를 HTTP 응답으로 변환해서 클라이언트에 전송한다.

중요한 것은 모든 단계가 `Mono`와 `Flux`로 연쇄되어 있다는 기 때문이다. 덕분에 전체 파이프라인이 논블로킹으로 동작할 수 있다. 어느 단계도 스레드를 블로킹하지 않으면서 처리를 완료한다.

---

## 2.3 논블로킹 I/O의 원리

### 2.3.1 블로킹 I/O vs 논블로킹 I/O

**블로킹 I/O**는 직관적이지만 비효율적이다. `read()` 또는 `write()` 호출 시 데이터가 준비될 때까지 호출한 스레드는 대기 상태에 빠진다. 이 동안 그 스레드는 아무 일도 못하면서 메모리와 스택 공간만 계속 차지한다.

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

**논블로킹 I/O**는 완전히 다르다. `read()` 호출이 즉시 반환되기 때문에 데이터가 아직 없으면 "아직 없다"는 신호만 받고, 스레드는 바로 다른 일을 할 수 있다.

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

Java NIO(New I/O)의 핵심은 **Selector**다. 이것이 있으면 하나의 스레드가 여러 채널의 I/O 이벤트를 효율적으로 감시할 수 있다. 내부적으로는 운영체제의 `epoll`(Linux) 또는 `kqueue`(macOS) 같은 고효율 시스템 콜을 활용하고 있다.

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

Netty의 이벤트 루프는 Java NIO의 Selector를 기초로 삼되, 여기에 더 정교한 태스크 스케줄링과 파이프라인 처리를 덧붙인 것이다.

이벤트 루프가 한 바퀴 도는(iteration) 과정을 보면 다음과 같다.

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

여기서 기억해야 할 절대 원칙이 하나 있다. **이벤트 루프 스레드에서는 절대 블로킹 작업을 하면 안 된다는 것이다.** 하나의 이벤트 루프가 수천 개의 연결을 동시에 담당하고 있기 때문에, 그 스레드가 한 번 블로킹되면 수천 개의 연결이 모두 함께 지연되는 끔찍한 일이 벌어진다.

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

만약 블로킹 작업이 피할 수 없다면, 반드시 별도의 스케줄러로 그 작업을 위임해야 한다.

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

마이크로서비스 게이트웨이나 API 중개 서비스처럼 여러 외부 서비스를 한꺼번에 호출하고 결과를 조합해야 하는 경우가 대표적이다. 이런 상황에서 WebFlux는 진가를 발휘한다.

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

SSE(Server-Sent Events)나 WebSocket 같은 방식으로 실시간 데이터를 스트리밍해야 할 때, WebFlux의 `Flux`가 자연스럽게 그 역할을 수행할 수 있다.

```java
// 실시간 주가 스트리밍
@GetMapping(value = "/stocks/{symbol}/stream",
            produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<StockPrice> streamStockPrice(@PathVariable String symbol) {
    return stockService.getPriceStream(symbol);  // 무한 스트림
}
```

**3. 대량의 동시 연결을 유지해야 하는 경우**

채팅 서비스나 알림 시스템처럼 수천 개에서 수만 개의 커넥션을 오래 유지해야 할 때는 어떨까? thread-per-request 방식은 메모리 한계에 쉽게 도달하기 때문에 WebFlux가 필수다.

**4. 전체 파이프라인이 리액티브인 경우**

실무에서 자주 보는 패턴인데, 데이터베이스(MongoDB Reactive, R2DBC), 메시지 브로커(Reactor Kafka, Reactor RabbitMQ), HTTP 클라이언트(WebClient) 등 모든 계층에서 리액티브 드라이버를 사용할 수 있을 때만 WebFlux의 이점이 정말로 극대화된다.

### 2.4.2 WebFlux가 부적합한 시나리오

**1. JDBC/JPA(관계형 DB) 블로킹 드라이버를 사용하는 경우**

전통적인 JDBC나 Spring Data JPA는 어쩔 수 없이 블로킹 API다. 이것을 WebFlux 위에서 사용하면 이벤트 루프 스레드를 블로킹하게 되므로 오히려 성능이 나빠진다. R2DBC라는 리액티브 대안이 있기는 하지만, JPA의 편한 기능들(지연 로딩, 캐싱 등)을 모두 포기해야 한다는 트레이드오프가 있다.

**2. CPU 집약적인 작업이 대부분인 경우**

이미지 처리나 복잡한 수학 계산, 암호화 같은 CPU를 오래 사용하는 작업들에서는 논블로킹 I/O가 별로 도움이 되지 않는다. 오히려 리액티브 프로그래밍의 복잡성만 들어올 뿐이다.

**3. 팀의 리액티브 프로그래밍 경험이 부족한 경우**

리액티브 프로그래밍의 학습 곡선은 정말 가파르다. 디버깅도 어렵고, 기존의 명령형 사고방식과는 근본적으로 다른 접근이 필요하기 때문이다. 팀 전체가 충분히 준비되지 않은 채로 도입하면 오히려 생산성이 크게 떨어질 수 있다는 게 문제다.

**4. 동시 요청 수가 적은 내부 관리 도구**

동시 사용자가 수십 명 정도인 백오피스 시스템이라면? Spring MVC만으로 충분하고, WebFlux를 굳이 도입할 필요가 없다.

### 2.4.3 의사결정 기준

결국 WebFlux를 도입할지 말지는 몇 가지 질문에 답하는 것으로 결정할 수 있다.

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

Spring WebFlux를 사용할 때 선택할 수 있는 프로그래밍 방식이 두 가지 있다. 어노테이션 기반 모델과 함수형 엔드포인트 모델인데, 둘 다 동일한 리액티브 런타임 위에서 움직인다. 흥미롭게도 한 프로젝트 내에서 두 방식을 섞어 쓸 수도 있다.

### 2.5.1 어노테이션 기반 모델

Spring MVC를 써본 개발자라면 가장 익숙한 방식이다. `@Controller`, `@RestController`, `@RequestMapping` 같은 어노테이션을 그대로 사용하면서 반환 타입만 `Mono`와 `Flux`로 바꾸면 된다.

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

서비스 계층도 어떻게 구성되는지 보면 감이 올 것이다.

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

함수형 모델은 라우팅과 핸들러를 어노테이션이 아니라 코드로 직접 정의하는 방식이다. `RouterFunction`이 라우팅 규칙을, `HandlerFunction`이 요청 처리를 담당한다.

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

여러 도메인의 라우터들을 조합해서 전체 라우팅을 구성할 수도 있다.

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

- 이미 Spring MVC 경험이 있는 팀
- 빠른 개발 속도를 중요하게 보는 프로젝트
- 표준적인 CRUD API만 필요한 경우
- Bean Validation을 자주 쓰는 경우

**함수형 엔드포인트를 선택하는 경우:**

- 라우팅 규칙이 복잡하거나 동적으로 바뀌어야 하는 경우
- 마이크로서비스처럼 최소한의 프레임워크 의존성이 필요한 경우
- 팀이 함수형 프로그래밍 스타일을 좋아하는 경우
- 테스트할 때 Spring 컨텍스트 없이 핸들러만 단위 테스트하고 싶은 경우

현실적으로 실무에서는 어노테이션 기반 모델이 훨씬 더 광범위하게 쓰인다. Spring MVC에서의 전환 비용이 낮고, 대부분 팀이 이미 익숙하기 때문이다. 함수형 모델은 특별히 라우팅이 복잡한 상황이거나, 팀이 함수형 스타일을 잘 다루는 경우에 고려해볼 만하다.

---

## 정리

이 장을 통해 살펴본 핵심 내용들을 정리하면 다음과 같다.

- **Spring MVC vs WebFlux**: MVC는 서블릿 기반의 thread-per-request 모델이고, WebFlux는 이벤트 루프를 기반으로 한 논블로킹 모델이다. 특히 높은 동시성 상황에서 WebFlux가 적은 리소스로 안정적인 처리량을 유지할 수 있다.
- **Netty와 이벤트 루프**: WebFlux가 기본으로 사용하는 Netty는 이벤트 루프 모델을 통해 소수의 스레드로 수만 개의 동시 연결을 처리해낼 수 있다. 다만 절대로 이벤트 루프 스레드를 블로킹하면 안 된다는 원칙은 철저히 지켜야 한다.
- **논블로킹 I/O**: Java NIO의 Selector를 활용하면 하나의 스레드가 여러 채널의 I/O를 효율적으로 관리할 수 있다. 데이터가 실제로 준비될 때만 처리하기 때문에 스레드 낭비가 거의 없다.
- **도입 판단 기준**: 높은 동시성이 필요하고, 리액티브 파이프라인을 구축할 수 있으며, 팀의 역량이 충분한 세 조건이 모두 만족될 때 WebFlux를 선택해야 한다.
- **두 가지 프로그래밍 모델**: 어노테이션 기반 모델은 Spring MVC 경험을 활용할 수 있어서 접근성이 높고, 함수형 모델은 라우팅의 자유도와 테스트 편의성에서 강점이 있다.

다음 장에서는 WebFlux를 작동하게 하는 심장 같은 존재인 **Project Reactor**를 깊이 있게 살펴본다. `Mono`와 `Flux`가 어떻게 동작하는지, 주요 연산자들은 무엇인지, 에러를 어떻게 처리해야 하는지 등을 자세히 다룰 것이다.
# Chapter 3. Project Reactor 핵심

Project Reactor는 Spring WebFlux의 리액티브 프로그래밍을 뒷받침하는 핵심 라이브러리다. 이 장에서는 Reactor의 두 가지 핵심 타입인 `Mono`와 `Flux`부터 시작하여, 실전에서 자주 마주치는 연산자들, 에러 처리 전략, 스레드 제어를 위한 스케줄러, 그리고 디버깅 기법까지 차근차근 살펴보기로 한다.

---

## 3.1 Mono와 Flux 이해하기

### 3.1.1 Mono: 0..1개의 요소

`Mono<T>`는 **최대 1개의 요소**를 발행하는 Publisher다. 데이터베이스에서 단일 레코드를 조회하거나 HTTP 요청의 응답을 처리할 때 사용하게 되는 기본적인 타입이다.

```java
// 값이 있는 Mono
Mono<String> mono = Mono.just("Hello Reactor");

// 빈 Mono (값 없이 완료)
Mono<String> empty = Mono.empty();

// 에러를 발행하는 Mono
Mono<String> error = Mono.error(new RuntimeException("오류 발생"));
```

### 3.1.2 Flux: 0..N개의 요소

이제 `Flux<T>`는 **0개에서 N개까지의 요소**를 발행할 수 있는 Publisher다. 컬렉션의 데이터를 스트리밍하거나 실시간 이벤트를 계속 흘려 보내야 할 때 자연스럽게 선택하게 되는 타입이기도 하다.

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

실제로 Mono와 Flux를 만드는 방법은 상황에 따라 달라진다. 단순한 값부터 복잡한 비동기 작업까지, 다양한 시나리오에 맞게 여러 팩토리 메서드를 활용할 수 있다.

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

Reactor를 다루면서 가장 먼저 깨닫게 되는 핵심 원칙이 있다. 바로 **"구독이 없으면 아무것도 실행되지 않는다"** 는 점이다. 아무리 화려한 `Mono`와 `Flux` 파이프라인을 구성했어도, `subscribe()`를 명시적으로 호출하기 전까지는 정말 아무 일도 벌어지지 않기 때문이다.

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

Reactor 개발에서 대부분의 시간을 쓰게 되는 부분이 바로 연산자 조합이다. 데이터를 변환하고, 필터링하고, 결합하는 다양한 연산자들을 어떻게 조합하느냐가 리액티브 코드의 질을 크게 좌우한다.

### 3.2.1 변환 연산자

#### map: 동기 변환

가장 기본적인 변환 연산자다. 각 요소를 동기적으로 1:1로 변환한다.

```java
Flux<String> upperCase = Flux.just("spring", "webflux", "reactor")
    .map(String::toUpperCase);
// 결과: "SPRING", "WEBFLUX", "REACTOR"
```

#### flatMap: 비동기 변환 (순서 보장 X)

필자의 경험상, 리액티브 코드에서 가장 자주 사용되는 연산자 중 하나가 바로 이것이다. 각 요소를 `Publisher`로 변환하고 결과들을 병합해주는데, **순서는 보장하지 않는 대신** 동시에 여러 내부 Publisher를 구독하기 때문에 처리량이 우수하다.

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

각 요소를 순차적으로 처리하기 때문에 **순서가 보장**된다는 점이 매력이다. 다만 이전 요소의 처리가 완료되어야 다음 요소를 처리할 수 있으므로, 처리량이 필요한 경우라면 `flatMapSequential`보다는 떨어질 수 밖에 없다.

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

스트림에서 일부 요소를 걸러내거나, 특정 개수만 취하는 작업들은 매우 일반적이다. 이를 위한 필터링 연산자들을 살펴보자.

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

여러 개의 Publisher를 하나로 조합해야 할 때가 있다. 상황에 따라 어떤 방식으로 결합할지 선택하는 것이 중요하다.

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

여러 Publisher의 데이터가 뒤섞여서 흐르도록 만든다. 요소가 발행되는 즉시 하류로 전달되므로, 순서는 결국 도착 순이 된다.

```java
Flux<String> fast = Flux.interval(Duration.ofMillis(100))
    .map(i -> "FAST-" + i).take(3);
Flux<String> slow = Flux.interval(Duration.ofMillis(200))
    .map(i -> "SLOW-" + i).take(3);

Flux<String> merged = Flux.merge(fast, slow);
// 도착 순서대로 병합: FAST-0, FAST-1, SLOW-0, FAST-2, SLOW-1, SLOW-2
```

#### concat: 순서를 유지하며 병합

merge와 달리, concat은 엄격하게 순서를 유지한다. 첫 번째 Publisher가 완료될 때까지 두 번째 Publisher는 구독하지 않기 때문이다.

```java
Flux<String> first = Flux.just("1", "2", "3");
Flux<String> second = Flux.just("A", "B", "C");

Flux<String> concatenated = Flux.concat(first, second);
// 결과: "1", "2", "3", "A", "B", "C" (항상 이 순서)
```

#### combineLatest: 각 Publisher의 최신 값 결합

어느 한 Publisher에서 새로운 값이 나타나면, 다른 Publisher들의 최신 값과 함께 결합해서 내보낸다. 시시각각 변하는 여러 스트림을 조합해야 할 때 매우 유용하다.

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

스트림의 모든 요소를 모아서 하나의 값으로 축약하거나, 컬렉션으로 수집해야 할 때가 있다. 이런 종료 연산자(terminal operator)들을 알아보자.

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

실제 개발에서 자주 만나는 상황들을 다루기 위한 편의 연산자들이 있다. 에러 처리와 부수 효과, 타임아웃 설정 등을 간편하게 처리할 수 있다.

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

리액티브 스트림 세상에서는 에러 발생 시 즉시 스트림이 종료되어 버린다. 따라서 에러를 어떻게 다룰지를 미리 설계하는 것이 매우 중요하다. 다행히 Reactor는 다양한 전략을 구현할 수 있도록 풍부한 에러 처리 연산자들을 제공한다.

### 3.3.1 onErrorReturn: 기본값으로 대체

가장 간단한 에러 처리 방식이다. 에러가 터지면 그냥 정해진 기본값을 반환하고 스트림을 정상적으로 완료해버린다.

```java
Mono<String> result = externalApi.getData()
    .onErrorReturn("기본값");

// 특정 예외 타입에만 적용
Mono<String> result2 = externalApi.getData()
    .onErrorReturn(TimeoutException.class, "시간 초과 - 기본값 사용");
```

### 3.3.2 onErrorResume: 대체 Publisher로 전환

단순한 기본값이 아니라, 복잡한 폴백(fallback) 로직이 필요할 때 사용한다. 에러가 나면 다른 Publisher로 전환해서 재시도하는 식의 고급 처리가 가능하다.

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

하위 계층에서 발생한 저수준의 예외를 비즈니스 계층에 맞는 고수준의 예외로 변환하는 데 쓰인다.

```java
Mono<User> user = userRepository.findById(id)
    .switchIfEmpty(Mono.error(new UserNotFoundException(id)))
    .onErrorMap(DataAccessException.class, e ->
        new ServiceException("데이터 접근 오류", e)
    );
```

### 3.3.4 doOnError: 에러 발생 시 부수 효과

스트림의 흐름 자체는 변경하지 않되, 에러가 발생했을 때 로깅이나 메트릭 수집 같은 부가 작업을 덧붙일 때 사용한다.

```java
Mono<User> user = userRepository.findById(id)
    .doOnError(e -> {
        log.error("사용자 조회 중 에러 발생. id={}", id, e);
        metrics.incrementErrorCount("user.findById");
    })
    .onErrorResume(e -> Mono.empty());
```

### 3.3.5 retry: 단순 재시도

에러가 나면 그냥 정해진 횟수만큼 다시 구독을 시도한다. 간단하지만, 많은 경우 이것만으로도 충분하다.

```java
Mono<String> result = externalApi.call()
    .retry(3); // 최대 3회 재시도
```

### 3.3.6 retryWhen: 고급 재시도 전략

단순 재시도로는 부족할 때, `Retry` 스펙을 활용하면 백오프(backoff) 전략이나 조건부 재시도 같은 정교한 정책을 구현할 수 있다.

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

이제까지 배운 기법들을 모두 조합하면, 실제 서비스 계층에서 견고한 에러 처리를 만들 수 있다. 다음 코드는 캐시 조회, DB 폴백, 타임아웃, 재시도를 모두 포함한 현실적인 예제다.

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

기본적으로 Reactor는 **호출자 스레드**(caller's thread)에서 동작한다는 점을 먼저 이해해야 한다. 이를 원하지 않는다면, 스케줄러를 통해 작업을 다른 스레드로 옮길 수 있다.

### 3.4.1 주요 스케줄러 종류

| 스케줄러 | 설명 | 스레드 수 | 사용 시기 |
|---------|------|----------|----------|
| `Schedulers.parallel()` | CPU 집약적 작업 | CPU 코어 수 | 계산, 변환 작업 |
| `Schedulers.boundedElastic()` | 블로킹 I/O 래핑 | 최대 10 * CPU 코어 | 블로킹 코드 감싸기 |
| `Schedulers.single()` | 단일 재사용 스레드 | 1 | 순차 실행 보장 |
| `Schedulers.immediate()` | 현재 스레드 | - | 테스트, 디폴트 |
| `Schedulers.fromExecutorService()` | 커스텀 스레드 풀 | 사용자 지정 | 특수한 요구사항 |

### 3.4.2 publishOn vs subscribeOn

이 둘은 이름이 비슷해서 자주 헷갈리지만, 실제로는 전혀 다른 동작을 한다. 정확히 이해하는 것이 리액티브 프로그래밍의 핵심이다.

#### publishOn: 하류 연산자의 실행 스레드를 변경

`publishOn`을 삽입한 지점 이후의 연산자들이 지정한 스케줄러에서 실행되도록 만든다. 파이프라인 중간에 갑자기 스레드를 바꿔야 할 때 딱 맞다.

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

이것은 소스의 구독 시점부터 시작되는 스레드를 변경한다. 파이프라인의 어디에 놓든 **소스 발행 부분의 스레드에만 영향**을 미친다는 점이 핵심이다.

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

리액티브 파이프라인 안에서 블로킹 코드를 부주의하게 호출하면 시스템 전체의 처리량이 참담해진다. 이벤트 루프 스레드 자체가 블로킹되기 때문이다. 불가피하게 레거시 블로킹 코드를 다뤄야 한다면, 반드시 `boundedElastic` 스케줄러로 격리해서 실행해야 한다.

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

실무에서 자주 보는 패턴인데, Mono와 Flux가 모두 같은 식으로 동작하는 것은 아니다. 언제 데이터를 발행하기 시작하고, 구독자들이 어떻게 그 데이터를 받는지에 따라 두 가지로 나뉜다.

### 3.5.1 Cold Publisher

Cold Publisher는 **구독이 들어올 때마다 데이터를 처음부터 새로 발행**한다. 대부분의 Reactor 연산자가 기본적으로 이런 식으로 작동한다.

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

Hot Publisher는 정반대다. **구독 여부와 상관없이 계속 데이터를 발행**하며, 구독자들은 자신이 구독한 시점 이후의 데이터만 수신한다.

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

Hot Publisher를 명시적으로 만들기 위해서는 `Sinks`를 사용한다. Reactor 3.4부터 도입된 이것은 기존의 `Processor`를 현대적으로 개선한 버전으로, 스레드 안전성을 내장하고 있다.

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

Cold Publisher와 Hot Publisher의 특성을 상황에 맞게 조절할 수 있는 유틸리티 메서드들이 있다.

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

한 번 실행된 결과를 메모리에 보관했다가 이후 구독자들에게 재사용시킬 수 있다.

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

리액티브 코드를 디버깅하는 일은 명령형 코드보다 훨씬 까다롭다. 스택 트레이스가 비동기 실행 때문에 원래 코드의 위치를 정확히 가리키지 못하는 까닭이다. 다행히 Reactor가 이 문제를 푸는 여러 도구를 제공한다.

### 3.6.1 log(): 리액티브 신호 로깅

구독부터 완료까지, 리액티브 파이프라인을 흐르는 모든 신호를 로깅할 수 있다. `log()` 연산자를 체인에 끼워넣으면 그 지점의 모든 이벤트를 볼 수 있다.

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

에러가 터졌을 때 정확히 어느 연산자에서 문제가 났는지 찾기는 어렵다. `checkpoint()`로 마킹해두면 에러 메시지에 그 정보를 포함시켜 추적을 한결 쉽게 만든다.

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

모든 연산자에 대해 생성 시점의 스택 트레이스를 자동 캡처하는 강력한 도구다. 다만 **성능 오버헤드가 크기 때문에** 개발 환경에서만 켜야 한다.

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

활성화되면 에러 발생 시 스택 트레이스에 연산자가 정의된 정확한 소스 위치(클래스명, 줄 번호)를 포함시키므로, 원인 파악이 훨씬 빨라진다.

### 3.6.4 ReactorDebugAgent: 프로덕션 친화적 디버깅

`Hooks.onOperatorDebug()`의 성능 문제를 극복한 고급 옵션이다. Java Agent가 바이트코드 수준에서 변환을 하므로, 런타임 오버헤드 없이도 상세한 디버그 정보를 얻을 수 있다.

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

차근차근 이 순서로 접근하면 대부분의 문제를 찾을 수 있다.

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

이 장에서 배운 Project Reactor의 핵심 개념을 한번 정리해보자.

- **Mono와 Flux**는 리액티브 스트림의 두 기둥이다. 최대 1개의 값을 다루거나 여러 개의 값을 흐르게 해야 할 때, 어떤 것을 선택할지는 자연스럽게 결정된다.
- **연산자 체인**으로 선언적인 데이터 처리 파이프라인을 만든다. `map`, `flatMap`, `concatMap` 같은 각 연산자의 특성을 정확히 이해하는 것이 리액티브 코드의 품질을 결정한다.
- **에러 처리**는 단순한 기본값 반환부터 복잡한 재시도 전략까지, 상황에 맞는 도구를 선택할 수 있다. `retryWhen`과 `Retry.backoff()`를 조합하면 실제 서비스에 필요한 정교한 에러 대응을 구현할 수 있기 때문이다.
- **스케줄러**로 작업이 실행될 스레드를 제어한다. `publishOn`과 `subscribeOn`은 비슷하지만 전혀 다르다는 점을 잘 기억해야 하고, 레거시 블로킹 코드는 `boundedElastic`으로 반드시 격리해야 한다.
- **Cold와 Hot Publisher**의 차이를 이해하면, 데이터를 언제 생성하고 여러 구독자에게 어떻게 공유할지를 올바르게 설계할 수 있다. `Sinks`는 Hot Publisher를 직접 만드는 현대적인 방식이다.
- **디버깅**은 `log()`와 `checkpoint()`로 시작하여, 필요시 `ReactorDebugAgent`를 활용하면 복잡한 비동기 문제도 추적할 수 있다.

이제 Spring WebFlux와 Reactor를 이루는 기초를 다졌다. 다음 장에서는 MongoDB의 기본과 리액티브 드라이버를 자세히 살펴보기로 한다.
# Chapter 4. MongoDB 소개

앞서 리액티브 프로그래밍과 Project Reactor의 기초를 갖췄다면, 이제는 이들과 자연스럽게 어울리는 데이터베이스와의 만남이 필요하다. MongoDB가 왜 리액티브 애플리케이션에 강력한지, 그리고 도큐먼트 모델이 어떻게 작동하는지 직접 경험해보자. 설치부터 CRUD 조작까지 손으로 해보며, 리액티브 드라이버의 동작 방식까지 이해하게 될 것이다.

---

## 4.1 NoSQL과 MongoDB의 특징

### 4.1.1 RDBMS vs NoSQL 비교

전통적인 관계형 데이터베이스(RDBMS)에서는 정규화된 테이블, SQL 쿼리, ACID 트랜잭션이 중심이다. 반면 NoSQL은 특정 사용 사례에 최적화된 다양한 데이터 모델을 제공하기 때문에, 프로젝트의 특성에 맞는 선택이 가능해진다.

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

같은 컬렉션 안에 서로 다른 구조의 도큐먼트를 저장할 수 있다는 점이 MongoDB의 큰 매력이다. 애플리케이션이 빠르게 변화할 때 스키마 마이그레이션 부담을 크게 덜 수 있기 때문이다.

```javascript
// 같은 컬렉션에 서로 다른 구조의 도큐먼트가 공존 가능
{ name: "Alice", email: "alice@example.com" }
{ name: "Bob", email: "bob@example.com", phone: "010-1234-5678", address: { city: "Seoul" } }
```

**수평 확장 (Sharding)**

데이터가 늘어나도 샤드를 추가하여 여러 서버에 나눠 저장할 수 있다. 그러면서도 애플리케이션 코드는 손댈 필요가 없는 셈이다.

**높은 가용성 (Replica Set)**

복제 세트(Replica Set)는 여러 노드에 데이터 복제본을 유지하기 때문에, 프라이머리 노드에 장애가 발생하면 세컨더리 노드가 자동으로 프라이머리로 승격된다.

### 4.1.3 CAP 정리에서의 MongoDB 위치

분산 시스템의 세 가지 요구사항을 살펴보자. 일관성(Consistency), 가용성(Availability), 분단 내성(Partition Tolerance)인데, CAP 정리는 이 세 가지를 동시에 모두 만족할 수 없다는 것을 말한다.

- **C (Consistency)**: 모든 노드가 같은 시점에 같은 데이터를 반환한다.
- **A (Availability)**: 모든 요청에 대해 응답을 반환한다.
- **P (Partition Tolerance)**: 네트워크 분단이 발생해도 시스템이 동작한다.

MongoDB는 기본적으로 **CP 시스템**이다. 프라이머리 노드에 쓰기를 집중하여 일관성을 보장하고, 네트워크 분단이 생기면 가용성보다 일관성을 우선한다. 다만 `readPreference`와 `writeConcern` 설정을 조정하면, 가용성과 일관성 사이의 균형을 프로젝트의 요구에 맞게 조절할 수 있기 때문에 실제로는 더 유연한 선택이 가능하다.

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

MongoDB 내부에서 데이터가 어떤 형태로 저장될까? **BSON**(Binary JSON) 형식이 그 답이다. BSON은 JSON을 확장한 것으로, JSON이 제공하지 못하는 여러 데이터 타입을 추가로 지원한다.

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

도큐먼트의 기본 구조를 보면 다음과 같은데, 이 예시를 보며 각 요소를 이해해보자.

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

`_id` 필드는 컬렉션 내에서 도큐먼트의 유일한 식별자 역할을 한다. 개발자가 값을 지정하지 않으면 MongoDB가 자동으로 `ObjectId`를 생성해주는 것도 편리한 부분이다.

### 4.2.2 컬렉션 개념

컬렉션(Collection)은 RDBMS의 테이블과 비슷한 역할을 한다. 하지만 결정적인 차이가 있다—컬렉션의 도큐먼트들이 반드시 같은 스키마를 따를 필요가 없다는 점 말이다.

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

MongoDB 스키마 설계에서 가장 고민이 되는 순간이 바로 **데이터를 내장할 것인가, 참조할 것인가**를 결정하는 때다.

**내장 도큐먼트 방식**

관련된 데이터를 하나의 도큐먼트 안에 중첩시켜 모두 저장하는 방식이다.

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

반대로 데이터를 별도의 컬렉션에 보관하고, `_id`로 참조하는 방식이다.

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

MongoDB 커뮤니티에서 시간이 지나며 검증된 설계 패턴들을 살펴보자.

**버킷 패턴 (Bucket Pattern)**: 시계열 데이터처럼 연속적으로 들어오는 데이터를 일정한 단위(시간 또는 개수)로 묶어, 하나의 도큐먼트에 저장하는 방식이다.

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

**다형성 패턴 (Polymorphic Pattern)**: 기본적으로 유사하지만 세부 구조가 조금씩 다른 데이터들을 같은 컬렉션에 보관할 수 있게 해주는 패턴이다. `type` 필드로 각 도큐먼트의 종류를 구분한다.

```javascript
// products 컬렉션
{ type: "book", title: "MongoDB 가이드", author: "홍길동", pages: 500 }
{ type: "electronics", title: "무선 마우스", brand: "Logitech", weight: 85 }
```

---

## 4.3 MongoDB 설치 및 기본 CRUD

### 4.3.1 Docker를 통한 설치

개발할 때는 Docker를 활용하면 MongoDB를 가장 빠르고 깔끔하게 띄울 수 있다. 로컬 시스템에 영향을 주지 않으면서도 필요한 대로 시작하고 종료할 수 있기 때문이다.

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

`mongosh`는 MongoDB의 공식 셸 클라이언트다. Docker 컨테이너 안에서 직접 실행하여 데이터베이스와 상호작용할 수 있다.

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

MongoDB Compass는 공식 GUI 클라이언트로, mongosh의 명령어 방식이 불편하다면 시각적으로 데이터를 다루는 것을 선호하는 개발자들에게 훌륭한 도구가 된다. 주요 기능을 살펴보자.

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

작은 도큐먼트로 테스트할 때는 문제가 없지만, 데이터가 커지는 순간 성능이 급격히 떨어지는 경험을 할 수 있다. 인덱스가 없으면 MongoDB가 컬렉션 전체를 스캔(COLLSCAN)해야 하기 때문이다. 반대로 적절한 인덱스를 미리 준비하면, 쿼리 성능을 크게 향상시킬 수 있다.

**단일 필드 인덱스**

```javascript
// author 필드에 오름차순 인덱스 생성
db.books.createIndex({ author: 1 })

// price 필드에 내림차순 인덱스 생성
db.books.createIndex({ price: -1 })
```

**복합 인덱스 (Compound Index)**

여러 필드를 함께 인덱싱하는 방식인데, 여기서 필드의 순서가 굉장히 중요하다는 점을 반드시 기억해야 한다. **ESR 규칙**(Equality, Sort, Range)을 따르면 효율적인 복합 인덱스를 설계할 수 있다—동등 조건 필드를 앞에, 정렬 필드를 중간에, 범위 조건 필드를 뒤에 배치하는 식이다.

```javascript
// author(동등) + publishedAt(정렬/범위)에 복합 인덱스
db.books.createIndex({ author: 1, publishedAt: -1 })

// 활용 쿼리: 특정 저자의 책을 최신순으로 조회
db.books.find({ author: "홍길동" }).sort({ publishedAt: -1 })
```

**멀티키 인덱스 (Multikey Index)**

배열 필드에 인덱스를 만들면, MongoDB가 자동으로 멀티키 인덱스를 생성한다. 배열의 각 요소 하나하나에 대해 인덱스 항목이 만들어지는 것이다.

```javascript
// tags 배열 필드에 인덱스
db.books.createIndex({ tags: 1 })

// 활용: tags에 "webflux"가 포함된 도큐먼트 조회
db.books.find({ tags: "webflux" })
```

**텍스트 인덱스 (Text Index)**

사용자가 입력한 문자열로 문서를 검색하고 싶을 때 필요한 것이 전문 검색(Full-Text Search)이고, 이를 지원하는 인덱스다.

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

지정한 시간이 지나면 도큐먼트를 백그라운드에서 자동으로 삭제해주는 기능이다. 세션 정보나 로그 같이 일정 기간이 지나면 더 이상 필요 없는 데이터를 관리할 때 매우 유용하다.

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

우리가 작성한 쿼리가 실제로 어떻게 동작하고 있는지 궁금한 적이 있을까? `explain()` 메서드를 사용하면 쿼리의 실행 계획을 상세히 볼 수 있다.

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

**COLLSCAN이 나타나는 것을 보면**, 그 쿼리 조건에 맞는 인덱스를 만들어야 한다는 신호다.

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

이제 MongoDB를 리액티브 방식으로 다루는 방법을 살펴보자. MongoDB는 공식적으로 **Reactive Streams** 사양을 구현한 Java 드라이버를 제공하는데, 이것이 논블로킹 I/O를 기반으로 동작하며 Netty를 내부 네트워크 계층으로 쓴다.

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

동기 드라이버와 리액티브 드라이버의 근본적인 차이를 경험해보자. 동기 드라이버에서 `find()`를 호출하면, 결과가 모두 돌아올 때까지 해당 스레드가 계속 기다리고 있다. 반면 리액티브 드라이버는 `Publisher`를 즉시 반환하고, 구독이 이루어지면 데이터가 준비되는 대로 비동기로 스트리밍하는 방식이다.

```java
// 동기 드라이버 — 스레드가 결과 반환까지 대기
List<Document> books = syncCollection.find().into(new ArrayList<>());

// 리액티브 드라이버 — 논블로킹, 데이터가 준비되면 콜백
Flux.from(reactiveCollection.find())
    .collectList()
    .subscribe(books -> { /* 결과 처리 */ });
```

### 4.5.3 Spring Data MongoDB Reactive 모듈 소개

실제 개발 현장에서 Reactive Streams Driver를 직접 다루는 경우는 거의 없다. 그 대신 **Spring Data MongoDB Reactive** 모듈이 드라이버를 깔끔하게 추상화하여, 개발자가 훨씬 편하게 작업할 수 있는 프로그래밍 모델을 제공한다는 점이 중요하다.

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

위 코드에서 눈여겨봐야 할 부분이 있다. **반환 타입이 모두 `Mono` 또는 `Flux`라는 것**이 바로 그것인데, 이게 리액티브 스택의 핵심이다. 컨트롤러에서 `Mono`나 `Flux`를 반환하면 WebFlux가 구독을 담당하고, 데이터가 준비되는 순간순간 논블로킹 방식으로 HTTP 응답을 클라이언트에게 흘려보낸다. 필자의 경험상 이런 방식이 동기 방식보다 고속 처리 환경에서 훨씬 효율적이라는 것을 여러 번 확인했다—데이터베이스 쿼리부터 HTTP 응답까지, 전체 흐름에서 스레드 하나가 오래 묶여있지 않기 때문이다.

**application.yml 설정**

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://admin:secret1234@localhost:27017/webflux_demo?authSource=admin
```

> **Spring Data MongoDB Reactive의 핵심 구성 요소**들은 Chapter 5에서 프로젝트를 직접 세팅하면서 자세히 학습하고, Chapter 6에서 실제 REST API를 만들며 손으로 익히게 된다. 더 나아가 Chapter 8에서는 `ReactiveMongoTemplate`, Aggregation, Change Streams처럼 더 심화된 기능들을 깊이 있게 다룬다.

---

## 4장 정리

지금까지 MongoDB와 리액티브 드라이버의 전반적인 개념을 살펴봤다. 다음 표는 각 주제별로 핵심을 간추린 것이니, 필요할 때마다 참고하자.

| 주제 | 핵심 요약 |
|------|----------|
| NoSQL vs RDBMS | MongoDB는 유연한 스키마, 수평 확장, 높은 가용성을 제공하는 도큐먼트 DB |
| CAP 정리 | MongoDB는 CP 시스템. `writeConcern`, `readPreference`로 균형 조절 가능 |
| 도큐먼트 모델 | BSON 형식, 내장 vs 참조 설계 결정이 핵심 |
| 기본 CRUD | `insertOne/Many`, `find`, `updateOne/Many`, `deleteOne/Many` |
| 인덱스 | 단일, 복합, 멀티키, 텍스트, TTL. `explain()`으로 실행 계획 분석 |
| 리액티브 드라이버 | 논블로킹 I/O, `Publisher<T>` 반환, Spring Data MongoDB Reactive로 추상화 |

다음 Chapter 5에서는 이론을 실제로 옮겨놓는 작업을 시작한다. Spring Boot + WebFlux + MongoDB Reactive 프로젝트를 하나하나 세팅하면서, 지금까지 배운 개념들이 어떻게 실무에서 연결되는지 경험하게 될 것이다.
# Chapter 5. 개발 환경 구성

Part 1에서 리액티브 프로그래밍, WebFlux, Reactor, MongoDB의 이론적 토대를 다졌다. 이제 실제 코드를 작성해 볼 차례인데, 먼저 개발 환경을 제대로 갖춰야 한다. JDK 설치부터 IDE 설정, Docker 기반 MongoDB 실행, 프로젝트 생성, 의존성 구성, 그리고 팀 협업에서도 유용한 프로젝트 구조까지 이 장 하나에서 한 번에 다룬다.

---

## 5.1 JDK, IDE, Docker 설치

### 5.1.1 JDK 17+ 설치 — SDKMAN 활용

Spring Boot 3.x는 Java 17 이상을 필요로 한다. 프로젝트마다 JDK 버전을 달리 사용해야 하는 경우가 많기 때문에, 이런 상황에서 **SDKMAN**이 유용하다.

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

**프로젝트별 JDK 자동 전환** -- 프로젝트 루트에 `.sdkmanrc`를 만들어두면, 해당 디렉터리에 들어갈 때 자동으로 JDK 버전이 전환되는 기능이 있다.

```properties
# .sdkmanrc
java=21.0.5-amzn
```

### 5.1.2 IntelliJ IDEA 설정

**권장 에디션**: IntelliJ IDEA Ultimate가 Spring Boot 개발에 최적화되어 있다. Community Edition을 써도 되지만, Spring 관련 고급 기능 지원에서는 다소 제한이 있을 수 있다.

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

MongoDB를 로컬에서 실행하려면 Docker를 활용하는 것이 좋다. 설치와 제거가 간단해질 뿐 아니라 팀원들이 동일한 환경을 쉽게 구성할 수 있기 때문이다.

```bash
# macOS — Homebrew를 통한 설치
brew install --cask docker

# 설치 확인
docker --version
docker compose version
```

Docker Desktop을 실행한 후 **Resources** 설정에서 메모리를 최소 4GB 이상 할당해 두면 좋다. MongoDB와 애플리케이션을 함께 실행할 때 여유 있게 돌아가기 때문이다.

---

## 5.2 Spring Initializr로 프로젝트 생성

### 5.2.1 start.spring.io 사용법

[https://start.spring.io](https://start.spring.io)에 접속하면 직관적인 폼이 나온다. 다음 항목들을 설정하면 된다.

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

이제 필요한 라이브러리들을 추가해야 한다.

| 의존성 | 설명 |
|--------|------|
| **Spring Reactive Web** | WebFlux 핵심 (Netty 내장) |
| **Spring Data Reactive MongoDB** | 리액티브 MongoDB 드라이버 + Repository |
| **Lombok** | 보일러플레이트 코드 제거 |
| **Spring Boot DevTools** | 핫 리로드, 자동 재시작 |
| **Validation** | Bean Validation (jakarta.validation) |
| **Spring Boot Actuator** | 헬스 체크, 메트릭 |

**GENERATE** 버튼을 누르면 ZIP 파일이 내려온다. 압축을 풀고 IntelliJ에서 프로젝트를 열면 된다.

> **팁**: IDE에서 직접 프로젝트를 만들 수도 있다. `File → New → Project → Spring Boot`를 선택하면 Initializr의 같은 기능을 IDE 내부에서 사용할 수 있다.

### 5.2.3 초기 프로젝트 구조

Initializr가 만들어주는 기본 구조는 `build.gradle.kts`, 메인 클래스, `application.properties`, 테스트 클래스 정도로 간단하다. 실제 개발할 때는 `application.properties` 대신 `application.yml`을 쓰는 것이 계층 구조를 표현하기에 더 낫다.

---

## 5.3 주요 의존성 설정 및 빌드 파일 구성

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

> **주의**: `spring-boot-starter-web`(Spring MVC)을 함께 추가하지 않도록 주의해야 한다. 만약 둘을 함께 설정하면 Spring이 MVC를 우선 적용하여 Netty 대신 Tomcat이 구동되기 때문이다.

### 5.3.3 Gradle Wrapper 버전 관리

```bash
./gradlew --version                        # 현재 버전 확인
./gradlew wrapper --gradle-version=8.12    # 업그레이드
```

---

## 5.4 application.yml 설정

기본으로 생성되는 `application.properties` 파일은 삭제하고 `application.yml`을 새로 만든다. YAML 형식이 설정 항목의 위계를 표현하는 데 훨씬 편하기 때문이다.

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

Spring Boot에서는 `application-{profile}.yml` 형식으로 파일을 나누면, 환경에 따라 다른 설정을 쉽게 적용할 수 있다.

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

MongoDB 연결 문자열의 형식을 제대로 알아두면, 여러 환경에 유연하게 대응할 수 있다.

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

이제 MongoDB를 Docker로 실행하기 위한 설정 파일을 만들어보자.

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

MongoDB 컨테이너가 처음 시작될 때 자동으로 애플리케이션용 사용자와 데이터베이스를 만들어두면 편하다. `docker/mongo-init.js` 파일로 이를 구현한다.

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

docker-compose.yml에 비밀번호를 하드코딩하는 것은 좋지 않다. `.env` 파일로 분리하고 `.gitignore`에 추가하면 더 안전하다.

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

프로젝트 규모가 커질수록 패키지 조직이 중요해진다. 코드를 찾기 쉽고 수정하기 좋으려면 초반부터 좋은 구조를 잡아야 한다. 널리 쓰이는 두 가지 접근법을 비교해보고, 이 책에서 권장하는 방식을 소개한다.

### 5.6.1 계층형 vs 도메인형 비교

| 구분 | 계층형 (Layer-based) | 도메인형 (Domain-based) |
|------|---------------------|------------------------|
| 패키지 분류 기준 | 기술적 역할 (`controller/`, `service/`, `repository/`) | 비즈니스 도메인 (`user/`, `post/`, `comment/`) |
| 장점 | 구조 단순, Spring 입문자에게 친숙 | 관련 코드가 한 곳에 모여 파악·수정 용이, MSA 분리에 유리 |
| 단점 | 프로젝트가 커지면 도메인 간 경계 불명확, 수정 시 패키지 넘나듦 | 초반에 과도한 분리처럼 느껴질 수 있음 |

### 5.6.2 본서의 권장 구조 — 도메인형 하이브리드

이 책에서는 도메인형 구조를 기본으로 삼으면서도, 설정이나 예외 처리처럼 여러 도메인에서 공통으로 쓰는 코드는 `global/` 패키지에 모아둔다. 이런 절충적인 방식이 실무에서 잘 먹혀간다.

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

구조를 설정했으니 이제 각 계층의 기본 틀을 만들어 보자. 세부 로직은 다음 장에서 채워 넣을 것이다.

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

> `ReactiveMongoRepository`는 `ReactiveCrudRepository`를 상속받으면서 메서드들이 모두 `Mono`나 `Flux`를 반환한다. 덕분에 어디서도 블로킹이 일어나지 않는다.

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

정상적으로 구동되면 `Netty started on port 8080` 같은 로그가 나타날 것이다. 간단한 헬스 체크로 검증해 보자.

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

이 장에서 다룬 개발 환경 구성을 한눈에 정리하면 이렇다.

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

다음 장부터 이 환경 위에서 실제 REST API를 구현해 보자. 도메인 모델을 정의하고 Repository, Service, Controller의 구체적인 로직을 채워 넣은 뒤, API를 테스트해 보는 과정까지 다룰 것이다.
# Chapter 6. 어노테이션 기반 REST API 구현

Chapter 5에서 프로젝트 구조와 개발 환경을 다 갖추었으니, 이제 본격적으로 API를 만들어보자. 먼저 도메인 모델을 정의하고, 리포지토리와 서비스 계층을 거쳐 컨트롤러까지 순서대로 구축하면 완전한 CRUD REST API가 완성된다. 이 과정에서 모든 계층이 `Mono`와 `Flux`를 반환하며, 요청에서부터 응답까지 논블로킹으로 동작하는 리액티브 파이프라인을 구성하게 된다.

---

## 6.1 도메인 모델(Document) 정의

### 6.1.1 주요 어노테이션 정리

Spring Data MongoDB는 Java 객체를 MongoDB 도큐먼트에 매핑할 때 여러 어노테이션을 제공한다. 각각이 어떤 역할을 하는지 살펴보자.

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

`@Version` 필드를 추가해두면, 여러 요청이 동시에 같은 사용자를 수정할 때 `OptimisticLockingFailureException`이 발생해서 데이터 정합성을 지켜준다.

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

`@CompoundIndex`로 `authorId` 오름차순과 `createdAt` 내림차순의 복합 인덱스를 만들면, 특정 작성자의 최신 게시글을 조회할 때 쿼리가 훨씬 빨라진다.

### 6.1.4 Auditing 설정

`@CreatedDate`와 `@LastModifiedDate`가 실제로 동작하려면, Auditing 기능을 명시적으로 활성화해야 한다.

```java
package com.example.webfluxdemo.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.EnableReactiveMongoAuditing;

@Configuration
@EnableReactiveMongoAuditing
public class MongoConfig {
}
```

리액티브 환경에서는 꼭 `EnableReactiveMongoAuditing`을 써야 한다는 점을 잊지 말자. 일반적인 `@EnableMongoAuditing`은 여기서 작동하지 않기 때문이다. 그리고 자동 인덱스 생성을 켜려면 `application.yml`에 다음을 추가하면 된다.

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

이제 데이터베이스 접근 계층을 만들어보자. Spring Data가 제공하는 리액티브 리포지토리를 활용하면 기본 CRUD 메서드를 자동으로 얻을 수 있다.

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

`ReactiveMongoRepository<T, ID>`는 `ReactiveCrudRepository`를 상속받으므로, 기본적으로 다음과 같은 메서드들을 제공한다.

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

Spring Data의 매력적인 점 중 하나가 메서드 이름만 보고도 쿼리를 자동으로 만들어준다는 것이다. 주요 키워드들을 정리하면 다음과 같다.

| 키워드 | 예시 | 생성 쿼리 |
|--------|-----|-----------|
| `Is` / `Equals` | `findByName(String)` | `{ 'name': ?0 }` |
| `Between` | `findByAgeBetween(int, int)` | `{ 'age': { $gte: ?0, $lte: ?1 } }` |
| `Containing` | `findByTitleContaining(String)` | `{ 'title': { $regex: ?0 } }` |
| `In` | `findByRoleIn(List)` | `{ 'role': { $in: ?0 } }` |
| `OrderBy` | `findByAuthorIdOrderByCreatedAtDesc` | 정렬 추가 |
| `IgnoreCase` | `findByNameIgnoreCase(String)` | 대소문자 무시 |

### 6.2.4 페이징 처리

리액티브 환경에서 페이징을 할 때는 약간 다른 접근이 필요하다. `Pageable`을 전달하되, 총 개수는 별도로 조회해야 한다.

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

서비스 계층은 리포지토리와 컨트롤러 사이에서 비즈니스 로직을 담당한다. 리액티브 패턴을 제대로 이해하는 것이 이 계층에서 가장 중요하다.

### 6.3.1 커스텀 예외 정의

먼저 서비스에서 사용할 커스텀 예외들을 정의해두자.

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

이제 실제 CRUD 로직을 구현해보자. 인터페이스에서 `Mono<User> createUser(User)`, `Mono<User> getUserById(String)`, `Flux<User> getAllUsers()` 같은 메서드를 선언했다면, 구현체에서는 리액티브 패턴을 활용해서 이를 구현한다.

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

이 코드에서 핵심적으로 봐야 할 패턴들이 있다. `switchIfEmpty`는 `null` 검사를 리액티브 방식으로 대체하는 것이고, `flatMap`은 비동기 작업을 체인처럼 연결해준다. 그리고 `doOnSuccess`는 로깅처럼 사이드 이펙트를 일으키는 부분이다. 이 세 가지를 조합하면 리액티브하면서도 안전한 서비스 로직을 만들 수 있기 때문이다.

### 6.3.3 PostService 구현체

`PostService`도 UserService와 거의 동일한 패턴을 따른다. 여기서는 게시글 관련 핵심 메서드만 보여주겠다.

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

마지막으로 클라이언트 요청을 받아서 처리하는 컨트롤러를 만든다. 리액티브 컨트롤러는 동기식 방식과 몇 가지 다른 점이 있다.

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

컨트롤러를 작성할 때 기억해야 할 패턴들이 있다. `@ResponseStatus`를 쓰면 `ResponseEntity` 없이 깔끔하게 상태 코드를 지정할 수 있다. 그리고 `ResponseEntity`를 `Mono`로 감싸서 `map(ResponseEntity::ok)`로 200 응답을 만들거나, `defaultIfEmpty`로 404를 처리하는 것이 관례다. 마지막으로 `then()`을 사용하면 `Mono<Void>`가 완료된 후 새로운 값을 내보낼 수 있는데, 삭제 후 204 응답을 줄 때 자주 쓰인다.

### 6.4.2 PostController

`PostController`도 UserController와 똑같은 패턴으로 작성된다. 여기서는 게시글 엔드포인트 중에서도 페이징 조회 부분을 중심으로 살펴보자.

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

Java 16부터 `record`라는 새로운 클래스 타입이 추가되었는데, 이것은 DTO로 쓰기에 정말 좋다. 불변 데이터를 담는 용도로 설계되었고, 생성자나 `equals()`, `hashCode()`, `toString()` 같은 메서드를 자동으로 만들어주기 때문이다.

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

Post DTO도 User와 동일한 방식으로 만들면 된다. 여기서는 `PostResponse`의 `from()` 정적 팩토리 메서드만 보여주겠다.

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

도메인 모델을 그대로 API 응답으로 주지 않고 DTO를 따로 만드는 이유가 있다. 첫째, `password`나 `version` 같은 민감한 내부 필드가 노출되는 것을 막을 수 있다는 보안상 이점이다. 둘째, 도메인 모델이 바뀌어도 API 계약이 깨지지 않으므로 안정성이 좋다. 셋째, 용도에 따라 다른 DTO를 제공할 수 있어 유연하다. 그리고 넷째, 나중에 Bean Validation을 적용할 때도 DTO 단계에서 검증하는 것이 깔끔하다. 이런 여러 이유가 조합되어 있기 때문이다.

### 6.5.3 페이징 응답 DTO

페이징 결과를 감싸는 범용 DTO를 하나 만들어두면, 모든 페이징 응답에서 일관되게 페이징 메타 정보를 클라이언트에 전달할 수 있다.

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

`Mono.zip`을 사용하면 콘텐츠 조회와 총 개수 조회를 **동시에** 실행할 수 있고, 나중에 두 결과를 조합해서 `PageResponse`로 만든다. 이것이 리액티브 환경에서 여러 비동기 작업을 병렬로 처리하는 관용적인 방법이다.

---

## 6.6 API 테스트

API를 제대로 만들었는지 확인하는 가장 좋은 방법은 직접 호출해보는 것이다. 여러 도구를 이용해서 이를 해보자.

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

cURL도 좋지만, HTTPie라는 도구를 쓰면 더 직관적으로 API를 테스트할 수 있다.

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

IntelliJ IDEA를 쓰는 개발자라면, 내장된 HTTP Client 기능을 활용하는 게 제일 편하다. `.http` 파일로 모든 API 요청을 관리할 수 있기 때문이다. 프로젝트 루트에 `.http` 파일을 만들어보자.

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

`{{userId}}`처럼 변수화한 부분은 `http-client.env.json`에서 환경별로 관리한다. 그리고 `.http` 파일을 Git에 넣어서 관리하면 팀원들과 같은 API 테스트를 공유할 수 있다는 게 정말 큰 장점이다.

---

## 6장 정리

이번 장에서 배운 것들을 한번 정리해보자.

| 주제 | 핵심 요약 |
|------|----------|
| 도메인 모델 | `@Document`, `@Id`, `@Indexed`, `@CompoundIndex`로 도큐먼트 매핑. Auditing으로 생성/수정 시각 자동 관리 |
| 리포지토리 | `ReactiveMongoRepository`로 기본 CRUD 자동 제공. 쿼리 메서드 이름 규칙, `@Query`, 페이징 지원 |
| 서비스 계층 | `switchIfEmpty`로 존재 여부 검증, `flatMap`으로 비동기 체이닝, 커스텀 예외로 의미 있는 에러 전달 |
| 컨트롤러 | `@RestController`로 CRUD 엔드포인트 구성. `ResponseEntity`로 상태 코드 제어, `Mono`/`Flux` 반환 |
| DTO 설계 | Java `record`로 불변 DTO 정의. 도메인과 API 계약을 분리하여 보안과 유지보수성 확보 |
| API 테스트 | cURL, HTTPie, IntelliJ HTTP Client로 엔드포인트 검증 |

이제 기본적인 REST API를 어노테이션 방식으로 만들어봤다. 다음 Chapter 7에서는 다른 방식으로 **함수형 엔드포인트(Router Functions)** 를 사용해서 똑같은 API를 구현해보고, 어떤 차이가 있는지 비교해볼 예정이다.
# Chapter 7. 함수형 엔드포인트 (Router Functions)

Chapter 6에서는 `@RestController`와 어노테이션 기반 방식으로 REST API를 구현했는데, Spring WebFlux는 이와는 다른 접근 방식을 하나 더 제공한다. 바로 **함수형 엔드포인트(Functional Endpoints)**라는 프로그래밍 모델이다. 이번 장에서는 `RouterFunction`과 `HandlerFunction`을 활용해 동일한 API를 함수형 방식으로 구현해보고, 두 방식 사이의 장단점을 실제로 비교해볼 것이다.

---

## 7.1 HandlerFunction과 RouterFunction 이해

### 7.1.1 함수형 엔드포인트의 핵심 구성 요소

함수형 엔드포인트는 사실 그리 복잡하지 않다. 두 가지 핵심 인터페이스만 이해하면 충분하다.

| 구성 요소 | 역할 | 대응하는 어노테이션 방식 |
|-----------|------|------------------------|
| `HandlerFunction` | 요청을 받아 응답을 생성하는 함수 | `@RequestMapping` 메서드 본문 |
| `RouterFunction` | 요청을 적절한 HandlerFunction으로 라우팅 | `@RequestMapping`, `@GetMapping` 등 |
| `ServerRequest` | 불변(immutable) HTTP 요청 객체 | 메서드 파라미터 (`@RequestBody`, `@PathVariable` 등) |
| `ServerResponse` | HTTP 응답을 빌더 패턴으로 생성 | 컨트롤러 반환값 |

### 7.1.2 HandlerFunction 인터페이스

`HandlerFunction<T extends ServerResponse>`를 먼저 살펴보자. 이것은 `ServerRequest`를 받아 `Mono<T>`를 반환하는 함수형 인터페이스이기 때문에

```java
@FunctionalInterface
public interface HandlerFunction<T extends ServerResponse> {
    Mono<T> handle(ServerRequest request);
}
```

개념상으로는 `Function<ServerRequest, Mono<ServerResponse>>`와 다를 바 없다. 그래서 이 단순한 시그니처 덕분에 람다로 아주 간결하게 핸들러를 작성할 수 있는 장점이 생기는 거다.

```java
// 람다로 작성한 간단한 핸들러
HandlerFunction<ServerResponse> helloHandler = request ->
    ServerResponse.ok()
        .contentType(MediaType.TEXT_PLAIN)
        .bodyValue("Hello, WebFlux!");
```

### 7.1.3 RouterFunction 인터페이스

한편 `RouterFunction<T extends ServerResponse>`는 들어오는 요청을 분석해서 적절한 `HandlerFunction`으로 보내주는 역할을 담당한다.

```java
@FunctionalInterface
public interface RouterFunction<T extends ServerResponse> {
    Mono<HandlerFunction<T>> route(ServerRequest request);
}
```

물론 직접 구현할 수도 있지만, 보통은 `RouterFunctions.route()` 같은 헬퍼 메서드를 사용해서 선언적으로 라우팅을 정의하는 방식을 선호한다.

### 7.1.4 ServerRequest와 ServerResponse

**ServerRequest**는 불변 객체인데, HTTP 메서드, URI, 헤더, 쿼리 파라미터, 요청 바디 등 필요한 모든 정보에 접근할 수 있는 메서드들을 제공한다.

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

한편 **ServerResponse**는 빌더 패턴을 사용해서 HTTP 응답을 유연하게 구성할 수 있도록 해준다.

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

실제로 라우팅을 정의할 때는 `RouterFunctions.route()`와 `RequestPredicates`를 조합해서 사용한다. 어렵지 않으니 바로 코드로 살펴보자.

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

같은 경로 접두사를 쓰는 라우트들이 많을 때는 `nest()`를 사용해서 그룹화하면 중복 코드를 줄일 수 있다. 또한 코드도 훨씬 읽기 쉬워진다.

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

당연히 여러 리소스를 함께 관리하는 것도 가능하다. 한 설정 클래스에서 `products`, `categories`, `orders` 같은 여러 엔드포인트를 한 번에 정의할 수 있다.

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

`RouterFunction`에 `filter()`를 적용해서 요청과 응답을 가로채고 공통 로직을 추가할 수 있다. 어노테이션 방식의 `WebFilter`나 `HandlerInterceptor`와 비슷한 역할을 한다고 생각하면 된다.

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

만약 요청 전/후 처리를 좀 더 깔끔하게 분리하고 싶다면, `filter()` 대신 `before()`와 `after()`를 사용할 수 있다.

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

실제 프로젝트에서는 핸들러를 별도의 클래스로 빼서 관리한다. 어노테이션 방식의 컨트롤러처럼 생각하면 된다.

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

핸들러를 위한 도메인 모델과 서비스 계층은 어노테이션 방식과 완전히 같은 방식으로 작성할 수 있다. 결국 비즈니스 로직은 바뀌지 않으니까.

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

실무에서는 입력값 검증, 리소스 없음 등 여러 가지 에러 상황을 처리해야 한다. 함수형 방식에서는 이를 어떻게 다룰까.

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

경로에서 값을 추출하려면 `{변수명}` 형태로 선언해야 하고, 핸들러에서 `ServerRequest.pathVariable()`로 꺼내면 된다.

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

경로 변수가 여러 개인 경우도 마찬가지다. 각각 `pathVariable()`로 꺼내면 된다.

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

쿼리 파라미터는 `ServerRequest.queryParam()`으로 꺼내는데, 이 메서드는 `Optional<String>`을 반환한다기 때문에 존재 여부 확인을 명시적으로 해야 한다. 필요하면 `queryParams()`로 전체 파라미터 맵을 받을 수도 있다.

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

요청 바디는 포함된 데이터의 특성에 따라 다르게 처리하면 된다. 단일 객체면 `bodyToMono()`, 여러 개의 스트리밍 데이터면 `bodyToFlux()`를 쓰자.

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

복잡한 제네릭 타입이 포함된 데이터를 역직렬화해야 할 때가 있다. 이 경우 `ParameterizedTypeReference`를 사용해야 하기 때문에 알아두면 유용하다.

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

요청에 포함된 헤더와 쿠키도 당연히 접근할 수 있다. 다음과 같이 처리한다.

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

파일 업로드 같은 멀티파트 요청도 함수형 방식에서 충분히 처리할 수 있다. 어렵지도 않다.

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

만약 여러 파트를 세분화해서 처리해야 하면 `BodyExtractors.toMultipartData()`를 쓰면 텍스트 필드(`FormFieldPart`)와 파일(`FilePart`)을 구분해서 다룰 수 있다.

---

## 7.5 어노테이션 방식과 함수형 방식 비교

### 7.5.1 같은 API를 두 방식으로 구현

이제 실제로 같은 기능을 하는 API를 어노테이션 방식과 함수형 방식으로 각각 만들어보고, 어떤 차이가 있는지 살펴보자. 상품 CRUD API를 예로 든다.

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

두 방식을 찬찬히 비교해보면 여러 차이점이 눈에 띈다.

**라우팅 정의**: 어노테이션 방식에서는 라우팅 정보(`@GetMapping`)와 비즈니스 로직이 같은 클래스, 같은 메서드에 있다. 함수형 방식은 Router에서 라우팅을 정의하고, Handler에서 로직을 구현하기 때문에 역할이 명확히 분리된다는 게 큰 특징이다.

**파라미터 바인딩**: 어노테이션 방식이 `@PathVariable`, `@RequestBody` 같은 어노테이션으로 자동으로 바인딩해주는 반면, 함수형 방식에서는 `ServerRequest.pathVariable()`, `bodyToMono()` 같은 메서드를 직접 호출해야 한다. 더 명시적이라고 볼 수 있다.

**검증 처리**: 어노테이션 방식은 `@Valid` 어노테이션 하나로 자동 검증이 되는데, 함수형 방식에서는 `Validator`를 직접 주입받아서 수동으로 호출해야 한다.

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

흥미로운 점은 두 방식을 같은 애플리케이션에 섞어서 쓸 수 있다는 것이다. 둘 다 결국 같은 `DispatcherHandler`에서 처리되기 때문이다. 따라서 팀의 상황과 필요에 맞춰 선택하면 된다.

**어노테이션 방식이 적합한 경우**

- 팀 내에 Spring MVC를 이미 경험한 개발자가 많다면 학습 곡선이 낮은 편이다.
- 대부분이 CRUD 중심의 표준적인 REST API라면 어노테이션으로 충분하다.
- Spring의 자동 검증(`@Valid`)이나 전역 예외 처리(`@ControllerAdvice`) 같은 기능을 활용하고 싶을 때.
- Swagger/OpenAPI 문서를 자동으로 생성하는 것이 중요한 프로젝트.

**함수형 방식이 적합한 경우**

- 라우팅이 동적으로 변해야 하는 경우가 있다면 프로그래밍 방식의 유연성이 빛난다.
- 라우팅과 로직을 명확히 분리해야 한다는 설계 원칙이 있을 때.
- 특정 엔드포인트 그룹에만 필터를 적용하고 싶을 때 함수형 방식이 더 수월하다.
- 경량 마이크로서비스에서 리플렉션 기반의 어노테이션 처리 오버헤드를 줄이고 싶을 때.
- 팀이 함수형 프로그래밍 스타일을 좋아하거나 이미 익숙한 경우.

**혼합 사용 예시**

필자의 경험상, 실제 프로젝트에서는 두 방식을 함께 쓰는 게 가장 실용적이다. 예를 들어, 표준 CRUD는 어노테이션으로 빠르게 구현하고, 복잡한 라우팅이 필요한 부분만 함수형으로 구현하는 식이다.

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

함수형 방식의 유일한 단점을 꼽으라면, SpringDoc 라이브러리가 라우팅을 자동으로 감지하지 못한다는 것이다. OpenAPI 문서를 원하면 `@RouterOperation`으로 수동 추가해야 한다.

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

이번 장에서 배운 핵심 내용을 간단히 정리해보자.

| 주제 | 핵심 내용 |
|------|----------|
| **HandlerFunction** | `ServerRequest -> Mono<ServerResponse>` 시그니처의 함수형 인터페이스 |
| **RouterFunction** | `route()`, `nest()`로 선언적 라우팅 정의, `filter()`로 공통 로직 적용 |
| **ServerRequest** | 불변 요청 객체, `pathVariable()`, `queryParam()`, `bodyToMono()` 등으로 데이터 추출 |
| **ServerResponse** | 빌더 패턴으로 상태 코드, 헤더, 바디를 설정하여 응답 생성 |
| **멀티파트 처리** | `multipartData()`, `BodyExtractors.toMultipartData()`로 파일 업로드 처리 |
| **어노테이션 vs 함수형** | 같은 애플리케이션에 공존 가능, 상황에 따라 적합한 방식 선택 |

다음 장에서는 MongoDB와의 반응형 데이터 접근을 좀 더 깊이 있게 다룬다. `ReactiveMongoTemplate`, 커스텀 쿼리, Aggregation Pipeline, 변경 스트림(Change Stream) 같은 고급 기능들을 살펴보게 될 것이다.
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
            .defaultUriVariables(Map.of("appid", apiKey)).build();
    }

    public Mono<WeatherResponse> getCurrentWeather(String city) {
        return webClient.get()
            .uri(uriBuilder -> uriBuilder.path("/weather")
                .queryParam("q", city).queryParam("appid", "{appid}")
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
# Chapter 16. 리액티브 테스트 전략

리액티브 프로그래밍을 다룰 때 테스트 방식이 완전히 달라진다는 걸 깨닫게 된다. `Mono`와 `Flux`는 누군가 구독(subscribe)하기 전까지는 말 그대로 아무것도 실행되지 않고, 데이터가 비동기적으로 흘러가므로 전통적인 동기식 테스트처럼 단순히 반환값을 `assertEquals()`로 검증하는 방식은 통하지 않기 때문이다. 이 장에서는 실제로 리액티브 코드를 검증할 수 있는 핵심 도구들을 배우게 될 것이다. **StepVerifier**부터 **WebTestClient**까지, 그리고 Embedded MongoDB, Testcontainers, MockWebServer 등을 활용하는 실무적인 테스트 전략들을 살펴보자.

---

## 16.1 StepVerifier를 활용한 단위 테스트

### 16.1.1 StepVerifier란?

`StepVerifier`는 Reactor 라이브러리에서 제공하는 테스트 헬퍼로, `Publisher`(Mono나 Flux)가 방출하는 데이터 시퀀스를 단계별로 검증하는 데 사용한다. `reactor-test` 모듈을 추가하면 바로 쓸 수 있다.

```groovy
dependencies {
    testImplementation 'io.projectreactor:reactor-test'
}
```

기본 사용 패턴은 이렇다.

```java
StepVerifier.create(publisher)   // 1. Publisher를 감싼다
    .expectNext(value)            // 2. 기대하는 값을 선언한다
    .verifyComplete();            // 3. 완료 신호를 검증하고 구독을 시작한다
```

중요한 포인트는 `verifyComplete()`를 호출해야 실제 구독이 시작된다는 점이다. 없으면 테스트는 아무것도 하지 않고 그냥 통과해버린다.

### 16.1.2 expectNext, expectComplete, expectError

리액티브 시퀀스를 검증할 때 가장 자주 쓰는 메서드들을 살펴보자.

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

방출된 값에 대해 좀 더 복잡한 검증이 필요할 때는 `assertNext()`를 쓴다. `Consumer<T>`를 입력받기 때문에 AssertJ와 함께 써도 깔끔하다.

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

`Flux.interval()`이나 `Mono.delay()`처럼 시간에 의존하는 연산들을 테스트하려면 좀 다른 접근이 필요하다. 실제 시간을 기다리면 테스트 속도가 엄청 느려지니까, `withVirtualTime()`을 사용해서 시간을 스뮬레이션하는 게 훨씬 낫다.

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

이제 실제로 서비스 계층을 테스트해보자. Mockito로 리포지토리를 모킹하고 StepVerifier로 검증하는 방식이다.

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

`WebTestClient`는 WebFlux 애플리케이션의 HTTP 엔드포인트를 테스트할 때 쓰는 논블로킹 테스트 클라이언트이다. 서버를 실행하지 않고도 컨트롤러에 직접 요청을 보낼 수 있고, 원한다면 실제 HTTP 요청을 보내는 방식도 지원한다.

### 16.2.2 바인딩 방식

WebTestClient를 설정하는 방법은 몇 가지가 있다. 각각의 상황에 맞춰 선택하면 된다.

**bindToController** -- 특정 컨트롤러만 떼어내서 테스트하는 방식이다. Spring 컨텍스트를 로드하지 않으므로 속도가 빠르다.

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

**bindToApplicationContext** -- 반대로 전체 애플리케이션 컨텍스트를 로드해서 테스트하려면 이 방식을 쓴다.

```java
@SpringBootTest
@AutoConfigureWebTestClient
class ProductIntegrationTest {

    @Autowired
    private WebTestClient webTestClient;
}
```

**bindToRouterFunction** -- 함수형으로 라우팅을 정의했다면 이걸 사용하면 된다.

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

응답을 더 정교하게 검증하는 방법들을 알아보자.

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

리포지토리 계층을 테스트할 때 실제 MongoDB를 쓸 필요는 없다. JVM 내에서 가벼운 MongoDB를 띄워서 쓰는 게 훨씬 편하다. 필자의 경험상 로컬 개발 환경에서는 이 방식이 가장 실용적이다.

```groovy
dependencies {
    testImplementation 'de.flapdoodle.embed:de.flapdoodle.embed.mongo.spring3x:4.11.0'
}
```

### 16.3.2 @DataMongoTest

`@DataMongoTest`를 쓰면 MongoDB 관련 컴포넌트만 로드되는데, 이게 테스트를 훨씬 빠르게 해준다.

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

여러 테스트에서 동일한 형태의 테스트 데이터를 반복해서 만들어야 할 때가 많다. 이럴 땐 **팩토리 메서드 패턴**을 쓰면 깔끔하다.

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

리포지토리 인터페이스만으로는 표현할 수 없는 좀 더 복잡한 쿼리들이 있다. 이런 경우들을 다뤄보자.

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

Embedded MongoDB는 분명 편하지만, 실제 MongoDB와 동작이 완전히 일치하지 않을 수 있다는 게 문제다. 더 정확한 테스트를 원한다면 **Testcontainers**를 써보자. Docker를 활용해서 실제 MongoDB 인스턴스를 테스트할 때마다 띄워주니까 프로덕션과 정확하게 같은 환경에서 테스트할 수 있다.

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

하지만 여기서 주의할 점이 있다. 매번 새로운 컨테이너를 띄우면 테스트가 상당히 느려진다. 필자의 경험상 여러 테스트가 같은 MongoDB 컨테이너를 공유하도록 하면 훨씬 빠르다.

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

MongoDB의 트랜잭션 기능을 테스트하려면 Replica Set이 필요한데, Testcontainers가 기본적으로 이를 지원한다.

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

우리 애플리케이션이 외부 API를 호출해야 한다면 어떻게 테스트할까? `MockWebServer`는 OkHttp 라이브러리에서 제공하는 경량 HTTP 서버로, `WebClient`로 호출하는 외부 API를 로컬에서 모킹할 수 있게 해준다.

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

응답 검증도 중요하지만, 우리 클라이언트가 올바른 요청을 보냈는지 확인하는 것도 마찬가지다. `MockWebServer`는 수신한 요청을 기록해두므로 이를 검증할 수 있다.

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

지금까지 배운 도구들을 정리해보면, 테스트 방식이 꽤 다양하다는 걸 알 수 있다. Spring Boot의 **테스트 슬라이스(Test Slice)**는 이 여러 테스트 방식을 체계적으로 정리한 개념이다. 특정 계층만 로드해서 테스트하는 것인데, 이렇게 하면 전체 컨텍스트를 로드하는 것보다 훨씬 빠르다.

| 어노테이션 | 테스트 대상 | 로드 범위 |
|-----------|-----------|----------|
| `@WebFluxTest` | 컨트롤러 (웹 계층) | WebFlux 관련 빈만 |
| `@DataMongoTest` | MongoDB 리포지토리 | MongoDB 관련 빈만 |
| `@SpringBootTest` | 전체 통합 | 모든 빈 |

### 16.6.2 @WebFluxTest

가장 많이 쓰는 테스트 슬라이스는 `@WebFluxTest`다. 웹 계층만 로드하고 서비스나 리포지토리는 로드하지 않으므로, `@MockBean`으로 의존성을 모킹해줘야 한다.

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

단위 테스트나 슬라이스 테스트로는 한계가 있다. 시스템 전체가 제대로 동작하는지 확인하려면 전체 통합 테스트가 필요하다.

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

리액티브 환경에서 Mockito를 쓸 때는 동기 환경과는 조금 다르다. 몇 가지 주의할 점들을 정리해봤다.

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

테스트 작성할 때는 **테스트 피라미드(Test Pyramid)**라는 원칙을 따르는 게 좋다. 피라미드 형태로 테스트를 구성하면 테스트 속도와 신뢰성의 균형을 잘 맞출 수 있다.

- **단위 테스트(StepVerifier + Mockito)**: 70% -- 빠르니까 많이 작성해도 된다
- **슬라이스 테스트(@WebFluxTest, @DataMongoTest)**: 20% -- 각 계층을 검증한다
- **통합 테스트(@SpringBootTest)**: 10% -- 정말 중요한 엔드투엔드 시나리오만

### 16.6.6 테스트 작성 시 주의사항

리액티브 테스트를 쓰다 보면 자주 하는 실수들이 있다. 필자의 경험상 이런 실수들을 피하면 훨씬 튼튼한 테스트를 만들 수 있다.

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

여기까지 리액티브 애플리케이션을 테스트하는 여러 방법들을 살펴봤다. 각 도구와 기법들을 정리하면 다음과 같다.

| 주제 | 핵심 내용 |
|------|----------|
| **StepVerifier** | `expectNext`, `assertNext`, `expectError`로 Mono/Flux 시퀀스를 단계별 검증. `withVirtualTime()`으로 시간 의존 테스트 |
| **WebTestClient** | `bindToController`(격리), `bindToApplicationContext`(통합)으로 HTTP 엔드포인트 테스트. `jsonPath()`로 JSON 검증 |
| **Embedded MongoDB** | `@DataMongoTest`로 리포지토리 슬라이스 테스트. JVM 내 MongoDB 인스턴스로 빠른 테스트 |
| **Testcontainers** | `@Testcontainers`, `@Container`, `@DynamicPropertySource`로 실제 MongoDB Docker 컨테이너 사용. 프로덕션 호환성 보장 |
| **MockWebServer** | `MockResponse`로 외부 API 응답 시뮬레이션. `RecordedRequest`로 전송된 요청 검증 |
| **테스트 슬라이스** | `@WebFluxTest`(웹), `@DataMongoTest`(DB), `@SpringBootTest`(전체). Mockito로 의존성 모킹 |

리액티브 테스트에서 핵심은 **`block()`으로 무리하게 동기로 변환하지 않는 것**이다. 대신 `StepVerifier`로 비동기 시퀀스를 정직하게 검증해야 한다. 각 계층에 맞는 테스트 도구를 올바르게 선택하면, 빠르면서도 신뢰성 높은 테스트 스위트를 만들 수 있다.

다음 장에서는 SpringDoc OpenAPI를 활용한 리액티브 API 문서화와 버전 관리 전략을 다룬다.
# Chapter 17. 문서화와 API 관리

훌륭한 API를 설계하는 것은 중요하지만, 정직하게 말하자면 그것만으로는 부족하다. 아무리 좋은 리액티브 API를 만들어도 팀 동료, 프론트엔드 개발자, 외부 파트너가 그것을 어떻게 써야 할지 몰라버리면 의미가 없다. 필자의 경험상, API는 구현하는 그 순간보다 **유지보수되는 기간이 훨씬 길다**. 그리고 그 긴 기간 동안 그 API를 사용하는 사람들은 대부분 문서를 읽는다.

이 장에서는 Spring WebFlux 환경에서 API 문서를 체계적으로 만들고 관리하는 방법을 살펴본다. SpringDoc OpenAPI(Swagger)를 통한 자동 문서 생성부터, 리액티브 타입의 문서화 처리, 그리고 API 버전을 어떻게 관리할지까지 다룰 예정이다.

---

## 17.1 SpringDoc OpenAPI(Swagger) 연동

### 17.1.1 SpringDoc OpenAPI란?

SpringDoc OpenAPI는 Spring Boot 애플리케이션에서 **OpenAPI 3.0/3.1 명세**를 자동으로 생성해주는 라이브러리 정도로 이해하면 된다. 한때는 Springfox(Swagger 2)라는 도구를 많이 썼는데, Spring Boot 3.x가 나오면서 SpringDoc이 실질적인 표준이 되었다.

| 구분 | Springfox | SpringDoc |
|------|-----------|-----------|
| **OpenAPI 버전** | Swagger 2.0 | OpenAPI 3.0/3.1 |
| **Spring Boot 3 지원** | 미지원 | 지원 |
| **WebFlux 지원** | 제한적 | 네이티브 지원 |
| **유지보수 상태** | 사실상 중단 | 활발히 유지보수 |
| **RouterFunction 지원** | 미지원 | 지원 |

### 17.1.2 의존성 설정

WebFlux를 사용한다면 `springdoc-openapi-starter-webflux-ui` 의존성을 추가하면 된다. 주의할 점은 일반 MVC용인 `springdoc-openapi-starter-webmvc-ui`와 헷갈리는 것인데, 프로젝트 특성에 맞는 것을 선택해야 한다.

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

`application.yml`에 설정을 조금 추가하면 SpringDoc의 동작을 원하는 대로 제어할 수 있다.

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

운영 환경에서는 보안을 생각해서 Swagger UI를 꺼두는 게 관례다.

```yaml
# application-prod.yml
springdoc:
  api-docs:
    enabled: false
  swagger-ui:
    enabled: false
```

### 17.1.4 OpenAPI 전역 설정 빈

API 문서 전체의 제목, 설명, 버전 정보 같은 것들은 `OpenAPI` 빈으로 따로 정의하는 것이 깔끔하다.

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

`@Operation` 어노테이션을 메서드에 붙이면 각 API마다 설명을 달 수 있고, `@ApiResponse`로는 응답 코드를 상세히 문서화할 수 있다.

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

DTO에 `@Schema`를 붙여놓으면, Swagger UI에서 필드별 설명, 필수 여부, 예시 같은 정보가 깔끔하게 표시된다.

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

SpringDoc은 `Mono`나 `Flux` 같은 리액티브 타입을 아주 잘 이해한다. 내부에 감싸진 타입이 뭔지 파악해서 자동으로 스키마를 만들어낸다.

| 메서드 반환 타입 | OpenAPI 스키마 |
|----------------|---------------|
| `Mono<Product>` | `Product` (단일 객체) |
| `Flux<Product>` | `Product[]` (배열) |
| `Mono<Void>` | 응답 본문 없음 |
| `Mono<ResponseEntity<Product>>` | `Product` + 상태 코드 |
| `Flux<ServerSentEvent<Product>>` | SSE 스트림으로 표현 |

스트리밍 응답을 다룬다면, `produces` 미디어 타입을 명시적으로 지정해두는 게 문서 작성 입장에서도 명확하다.

```java
@Operation(summary = "상품 실시간 스트림")
@GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ProductResponse> streamProducts() {
    return productService.streamAll();
}
```

### 17.2.2 RouterFunction 문서화

함수형 라우터(`RouterFunction`)는 일반 컨트롤러와 달라서 리플렉션으로 메타데이터를 뽑아낼 수 없다. 그래서 SpringDoc은 별도로 두 가지 방법을 제공한다: `@RouterOperation` 어노테이션 방식과 `OpenApiCustomizer` 프로그래밍 방식이다.

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

라우트가 많다거나, 문서 정보를 동적으로 관리하고 싶은 경우 `OpenApiCustomizer` 빈을 만들어서 `openApi.getPaths().addPathItem()` 같은 메서드로 경로와 오퍼레이션을 프로그래밍 방식으로 등록할 수 있다.

### 17.2.3 SecurityScheme 설정

JWT 인증을 쓰는 API라면, Swagger UI에 직접 토큰을 입력하고 테스트하고 싶을 테니 `SecurityScheme`을 설정해두자.

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

그런데 어떤 엔드포인트는 인증이 필요하고 어떤 건 불필요하다면? `@SecurityRequirement`를 메서드마다 붙여서 선택적으로 적용하면 된다.

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

프로젝트가 커지면 API가 여러 도메인에 흩어진다. 문서도 그에 맞춰 그룹 단위로 분리하는 게 읽기 훨씬 편하다.

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

Swagger UI의 상단 드롭다운에서 그룹을 고르면, 선택한 그룹의 API만 보이는 식으로 작동한다.

---

## 17.3 API 버전 관리 전략

### 17.3.1 왜 API 버전 관리가 필요한가?

API를 한 번 공개하면, 그 순간부터 누군가는 그걸 사용하고 있다. 필자의 경험상 가장 많이 실수하는 부분이 바로 이것이다: 기존 API 사용자를 깨뜨리면서 마음대로 변경하면 안 된다. 체계적인 버전 관리가 없으면, 어느 날 갑자기 누군가의 클라이언트가 멈춰있고, 왜 변경되었는지 추적할 수도 없게 된다.

### 17.3.2 URL 경로 기반 버전 관리

가장 간단하고 직관적인 방법이다. 그냥 URL에 버전 번호를 넣어버리는 것이다.

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

이렇게 하면 버전마다 DTO를 따로 만들어야 한다.

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

URL을 깔끔하게 놔두고 싶다면, 헤더에다가 버전을 넣는 방법도 있다.

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

또 다른 방법은 `Accept` 헤더에 버전을 넣는 것이다. GitHub API가 이렇게 한다고 알려져 있다.

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

다만 이 방식은 구현이 좀 복잡하다. Spring이 커스텀 미디어 타입을 JSON으로 처리하도록 `WebFluxConfigurer`의 `configureHttpMessageCodecs` 메서드에서 코덱을 등록해야 한다.

| 장점 | 단점 |
|------|------|
| RESTful 원칙에 가장 부합 | 구현 복잡도 높음 |
| URL과 헤더 모두 깨끗 | 클라이언트가 Accept 헤더를 올바르게 설정해야 함 |
| HTTP 콘텐츠 협상 표준 활용 | 코덱 설정 필요 |

### 17.3.5 하위 호환성 유지 전략

어떤 방식으로 버전을 관리하든, **하위 호환성(Backward Compatibility)**을 지키는 게 최고의 전략이다. 필자의 경험상, 새 버전을 만드는 건 정말 마지막 수단으로 남겨두어야 한다.

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

만약 정말로 API의 어떤 필드나 엔드포인트를 없애야 한다면, 충분한 유예 기간을 두고 미리 경고해야 한다.

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

1. **URL 경로 기반을 기본으로 사용하자.** 제일 직관적이고 문제 추적도 쉽다.
2. **하위 호환이 유지되는 변경이라면 버전을 올리지 않는다.** 필드 추가나 선택 파라미터 추가 정도면 기존 버전에 포함시킨다.
3. **Breaking Change는 정말 피할 수 없을 때만 새 버전을 만든다.**
4. **이전 버전도 최소 6개월 정도는 유지해야 한다.** Sunset 헤더로 언제 종료될지 미리 알려준다.
5. **동시 운영하는 버전은 최대 2개로 제한해야 한다.** 3개 이상이면 유지보수 비용이 지수적으로 늘어난다.

---

## 17.4 정리

이 장에서 나눈 내용을 빠르게 정리해보면 다음과 같다.

| 주제 | 핵심 내용 |
|------|----------|
| **SpringDoc 연동** | `springdoc-openapi-starter-webflux-ui` 의존성 추가만으로 자동 문서 생성 |
| **어노테이션 활용** | `@Operation`, `@Parameter`, `@ApiResponse`, `@Schema`로 상세 문서화 |
| **리액티브 타입** | `Mono`/`Flux`를 자동 인식하여 내부 타입 기준으로 스키마 생성 |
| **RouterFunction** | `@RouterOperation` 또는 `OpenApiCustomizer`로 문서화 |
| **SecurityScheme** | JWT Bearer 인증을 Swagger UI에서 테스트 가능하도록 설정 |
| **버전 관리** | URL 경로 기반이 가장 실용적, 하위 호환성 유지가 최우선 |

마지막으로 한 가지 더. API 문서화와 버전 관리는 프레임워크나 도구보다 **팀의 규칙과 일관성**이 훨씬 더 중요하다. SpringDoc이 아무리 훌륭해도, 팀원들이 문서화를 제대로 하지 않으면 소용없다. 반대로 규칙이 정해져 있으면 좋은 도구가 없어도 충분히 잘할 수 있다.

다음 장에서는 이제 프로덕션 환경으로 나간다. 애플리케이션이 실제로 돌아가는 상황에서 뭐가 일어나는지 관찰하고 모니터링하는 **Observability** 전략을 다루려고 한다.
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
    public void setValue() { MDC.remove(KEY); }
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

컨테이너화와 CI/CD를 제대로 구축해놓으면, 이후 배포는 거의 자동화된다. 개발팀은 코드만 푸시하면 되고, 나머지는 파이프라인이 알아서 처리한다. 다음 장에서는 이런 환경에서 문제가 생겼을 때 **장애 대응과 트러블슈팅**을 어떻게 하는지 다룬다.# Chapter 21. 실전 프로젝트: 실시간 게시판 서비스

이제 앞서 배운 WebFlux, MongoDB 리액티브, JWT 인증, SSE, 테스트 같은 개념들을 모두 모아서 하나의 실제 프로젝트에 적용할 시간이다. 이 장에서는 **실시간 게시판 서비스**를 밑바닥부터 만들어볼 것인데, 회원가입과 JWT 인증은 물론 게시글 CRUD, 댓글 시스템, MongoDB Change Streams로 구현한 실시간 알림, 페이징과 검색, GridFS를 이용한 파일 업로드, 그리고 테스트 작성과 Docker Compose를 통한 배포까지 실무에서 자주 마주치는 거의 모든 것을 다뤄보겠다.

---

## 21.1 요구사항 분석 및 설계

### 21.1.1 기능 요구사항과 기술 스택

먼저 어떤 기능이 필요하고 그걸 구현하기 위해 어떤 기술을 쓸지 정리해보자.

| 기능 영역 | 세부 기능 | 기술 |
|-----------|----------|------|
| **사용자 관리** | 회원가입, 로그인, JWT 토큰 발급 | Spring Security + jjwt |
| **게시글** | 작성, 조회, 수정, 삭제, 페이징 | ReactiveMongoRepository |
| **댓글** | 작성, 조회, 삭제 | ReactiveMongoTemplate |
| **실시간 알림** | 새 댓글 알림 | Change Streams + SSE |
| **검색** | 제목/본문 키워드 검색 | ReactiveMongoTemplate |
| **파일 업로드** | 첨부파일 업로드/다운로드 | GridFS |

기술 스택은 Spring Boot 3.x + WebFlux + MongoDB 7.x(Reactive) + Testcontainers + Docker Compose 조합으로 구성할 것이다.

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

필요한 의존성을 먼저 추가해보자.

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

사용자 정보를 저장할 기본 도메인 모델을 정의하자.

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

JWT 토큰 생성과 검증을 담당하는 컴포넌트를 만들어보자. 필자의 경험상 JWT 구현에서 가장 자주 실수하는 부분은 토큰 만료 처리인데, 여기서는 명확하게 처리했다.

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

WebFlux에서는 서블릿 필터 대신 `WebFilter`를 사용해야 한다. Bearer 토큰을 추출한 후, 유효성을 검증하고 `ReactiveSecurityContextHolder`에 인증 정보를 저장하는 방식인데, 리액티브 컨텍스트 전파에 주의해야 한다.

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

다음으로 Security 설정에서 어떤 엔드포인트는 인증 없이 허용하고, 어떤 것은 인증을 요구할지 명시하고 JWT 필터를 연결해야 한다.

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

이제 실제 인증 로직을 구현해보자. 회원가입 시 이메일 중복 체크가 중요한데, 리액티브 환경에서는 예외 처리 방식이 약간 다르다.

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

게시글에는 기본적인 제목, 내용 외에 조회수와 댓글 수를 추적해야 한다. 이들은 이후에 집계(aggregation) 작업 없이 빠르게 조회하기 위함이다.

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

게시글 조회수 증가는 `ReactiveMongoTemplate`의 원자적(atomic) 업데이트를 활용해야 경합 문제(race condition)를 피할 수 있다. 수정과 삭제에서는 반드시 작성자 권한을 검증하는 것이 중요하다.

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

Controller는 다양한 엔드포인트를 제공해야 한다. 특히 목록 조회 시 검색과 페이징을 함께 처리한다.

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

댓글을 저장하는 방식을 선택할 때는 여러 가지를 고려해야 한다. 아래 표를 보자.

| 기준 | 임베디드(Embedded) | 참조(Reference) |
|------|-------------------|----------------|
| **문서 크기** | 댓글 증가 시 16MB 제한 위험 | 안정적 |
| **독립 쿼리** | 댓글만 별도 조회 어려움 | 페이징/정렬 가능 |
| **Change Stream** | 활용 제한적 | 댓글 컬렉션 감시 가능 |

우리 프로젝트에서는 댓글 수가 무제한으로 증가할 수 있고, 곧 다룰 Change Streams 기반의 실시간 알림 기능이 필요하므로 **참조 방식**이 최선의 선택이다.

### 21.4.2 Comment 모델과 서비스

댓글 모델과 이를 처리하는 서비스를 구현해보자.

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

이제 게시글에 새 댓글이 달리면 브라우저에 즉시 알림을 보내는 기능을 구현해보자. MongoDB Change Streams로 `comments` 컬렉션의 insert 이벤트를 감지하고, `Sinks.Many`를 통해 SSE로 클라이언트에 전송하는 방식이다. 필자의 경험상 이 부분이 가장 흥미로우면서도 까다로운데, 특히 메모리 누수를 방지하기 위해 onBackpressureBuffer 크기를 신중하게 설정해야 한다.

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

한 가지 중요한 제약이 있는데, Change Streams는 MongoDB **레플리카 셋(Replica Set)** 모드에서만 동작한다. 로컬 개발 환경에서도 레플리카 셋을 구성해야 하는데, 21.9절에서 Docker Compose로 이를 설정하는 방법을 다루겠다.

---

## 21.6 페이징과 검색 기능

리액티브 환경에서 조금 까다로운 부분 중 하나가 페이징이다. Spring Data의 `Page` 객체를 리액티브 스트림과 직접 함께 사용할 수 없기 때문에, 커스텀 DTO로 직접 구성해야 한다.

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

이제 `ReactiveMongoTemplate`을 사용해서 동적 쿼리, 정렬, 페이징을 한 번에 처리해보자.

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

검색 성능을 조금 더 끌어올리려면 MongoDB의 텍스트 인덱스(Text Index)를 활용할 수 있다. 정규표현식보다 훨씬 효율적이다.

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

게시글에 파일을 첨부하는 기능도 필요할 것이다. MongoDB의 GridFS 기능을 활용하면 파일을 청크(Chunk) 단위로 쪼개서 저장할 수 있고, 리액티브 환경에서는 `ReactiveGridFsTemplate`을 사용하면 된다.

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

업로드 후 반환된 `fileId`를 게시글의 `attachmentIds` 리스트에 저장하면 게시글과 첨부파일의 관계를 유지할 수 있다.

---

## 21.8 전체 테스트 작성

이번엔 우리가 만든 기능들이 제대로 작동하는지 테스트해야 한다. Testcontainers로 실제 MongoDB를 띄워서 테스트하는 방식을 사용할 것인데, Change Streams를 지원하려면 레플리카 셋으로 시작해야 한다.

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

이제 각 서비스의 단위 테스트를 작성해보자. Mock을 사용해서 의존성을 주입하고, StepVerifier로 리액티브 스트림을 검증한다.

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

단위 테스트만으로는 부족하다. WebTestClient를 사용해서 전체 통합 테스트도 작성해야 한다.

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

개발 환경에서 테스트한 코드를 이제 컨테이너화해서 배포해야 한다. 먼저 설정 파일부터 준비하자.

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

이제 docker-compose.yml을 작성할 차례인데, 여기서 핵심은 MongoDB를 레플리카 셋으로 구성하는 것이다. 그래야만 Change Streams가 제대로 동작한다.

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

이제 빌드해서 실제로 띄워보고 API가 잘 작동하는지 확인해보자.

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

시스템이 실제로 어떻게 동작하는지 한 번 그려보자.

```
[사용자 A] POST /api/posts → JWT 검증 → MongoDB insert → 201 Created
[사용자 B] GET /api/notifications/stream (SSE 연결 유지)
[사용자 C] POST /api/posts/{id}/comments → MongoDB insert → Change Stream → SSE 알림 전송
```

---

이렇게 해서 실시간 게시판 서비스를 완성했다. 우리가 앞에서 배운 Reactor 기반의 논블로킹 처리, MongoDB 리액티브 드라이버, JWT 인증, SSE 실시간 통신, GridFS 파일 관리, StepVerifier와 WebTestClient를 사용한 테스트, 그리고 Docker Compose를 통한 배포까지 모든 것을 한 프로젝트에 녹여냈다. 필자의 경험상 이 정도 규모의 프로젝트를 직접 만들어보면 WebFlux의 리액티브 패러다임이 훨씬 더 명확하게 이해된다. 다음 장에서는 이 프로젝트를 한 단계 더 발전시켜서 실시간 채팅 서비스를 구축해보면서 WebSocket과 고급 메시징 패턴까지 살펴보겠다.
# 부록 A. Reactor 주요 연산자 레퍼런스

이 부록은 실무에서 자주 마주치는 Reactor 연산자들을 카테고리별로 정리해 놓은 참고 자료다. 각 연산자마다 핵심만 짚은 설명, 실행 가능한 코드 예제, 마블 다이어그램으로 한눈에 동작을 파악할 수 있게 구성했다. 본문 3장~5장의 내용을 빠르게 찾아볼 수 있으니 필요할 때마다 펼쳐 보면 좋다.

> **표기 규칙**: 마블 다이어그램에서 `──>` 는 시간 흐름, `|` 는 onComplete, `X` 는 onError를 나타낸다.

---

## A.1 생성 연산자 (Creation Operators)

리액티브 파이프라인은 어딘가에서 출발해야 하는데, 이 역할을 맡는 연산자들을 소개한다. 기존의 데이터 소스를 리액티브 스트림으로 변환하거나, 처음부터 새로운 스트림을 만들어낼 수 있다.

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

가장 단순한 경우부터 생각해 보자. `just`는 주어진 값을 바로 흘려보내고, `empty`는 아무것도 하지 않고 끝내며, `error`는 즉각 예외를 던진다.

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

이미 있는 컬렉션이나 스트림, 또는 간단한 정수 범위를 리액티브 형태로 바꾸고 싶을 때 쓴다.

```java
Flux<String> fromList = Flux.fromIterable(List.of("A", "B", "C"));
Flux<String> fromStream = Flux.fromStream(List.of("A", "B").stream()); // 일회성
Flux<Integer> range = Flux.range(1, 5); // 1, 2, 3, 4, 5
```

```
range:  ──(1)──(2)──(3)──(4)──(5)──|──>
```

### interval

주기적으로 계속 신호를 보내는 상황이라면 `interval`을 쓰면 된다. 0부터 1, 2, 3... 하는 식으로 증가하는 숫자를 일정 간격으로 무한히 내보낸다. 기본적으로 `Schedulers.parallel()` 스레드에서 동작한다.

```java
Flux<Long> tick = Flux.interval(Duration.ofSeconds(1));       // 0, 1, 2, ...
Flux<Long> delayed = Flux.interval(Duration.ofSeconds(5), Duration.ofSeconds(1));
```

```
시간:  0s     1s     2s     3s
소스: ──(0)──(1)──(2)──(3)──...──>
```

### defer

필자의 경험상, `defer`는 '뭔가 늦게 결정하고 싶을 때'의 해답이다. 구독되는 순간에 Publisher를 만들도록 미루는 것인데, 그 시점의 상태를 반영할 수 있어서 동적 로직에 매우 유용하다.

```java
Mono<Long> deferred = Mono.defer(() -> Mono.just(System.currentTimeMillis()));
// 구독할 때마다 다른 타임스탬프가 발행된다
```

### create

콜백 중심의 레거시 API를 리액티브 세계로 끌어들일 때 `create`를 쓰면 된다. `FluxSink`를 통해 프로그래밍 방식으로 원하는 시점에 요소를 발행할 수 있다.

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

이제 흘러오는 데이터를 가공하는 차례다. 각 요소를 다른 형태로 바꾸거나 스트림 전체의 구조를 뜯어고칠 수 있다.

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

가장 단순한 변환. 각 요소에 함수를 먹이면 1:1로 매핑되어 나온다. 동기적으로만 작동하니 주의하자.

```java
Flux<String> upper = Flux.just("a", "b", "c").map(String::toUpperCase);
// 결과: "A", "B", "C"
```

```
소스:   ──(a)──(b)──(c)──|──>        결과:   ──(A)──(B)──(C)──|──>
```

### flatMap

복잡한 변환이 필요하면 flatMap으로 간다. 각 요소를 Publisher로 바꾼 뒤 펼쳐서 섞는다. 다만 **순서가 섞일 수 있으니** 주의—가장 빨리 도착하는 결과부터 나간다.

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

이 두 연산자는 flatMap의 순서 문제를 해결해 준다. `flatMapSequential`은 여러 개를 동시에 돌리되 결과는 원래 순서를 지킨다. 반면 `concatMap`은 하나씩 꼬박꼬박 기다렸다가 다음 것을 시작한다(순서는 당연히 보장).

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

사용자가 검색어를 계속 바꾼다면? 매번 새로운 검색을 시작할 때 이전 것을 버려야 한다. `switchMap`이 바로 그 역할—새 요소가 들어오는 순간 기존 작업을 **싹 날린다**.

```java
Flux<String> results = userInput.switchMap(query -> searchService.search(query));
```

```
소스:    ──(A)────(AB)────(ABC)──|──>
내부1:   ──...X (취소)   내부2: ──...X (취소)   내부3: ──(결과)──|
결과:    ────────────────(결과)──|──>
```

### collectList / collectMap / reduce / scan

한곳으로 모아서 처리해야 할 때가 있다. 아래 예제를 보면 차이를 알 수 있다:

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

들어오는 데이터 중에 필요한 것만 고르거나, 앞에서 몇 개만 따내는 식의 선별 작업들이다.

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

단순히 불(Boolean)로 판단하면 되면 `filter`를 쓴다. 조건 검사 자체가 비동기(DB 조회 같은)라면 `filterWhen`을 써야 한다.

```java
Flux<Integer> even = Flux.range(1, 10).filter(n -> n % 2 == 0);   // 2,4,6,8,10
Flux<User> active = userFlux.filterWhen(u -> userRepo.isActive(u.getId()));
```

```
소스:   ──(1)──(2)──(3)──(4)──(5)──|──>
결과:   ──(2)──(4)──|──>
```

### distinct

중복을 없애고 싶다면 이걸 쓴다. 특정 필드 기준으로 중복을 판단하도록 함수를 따로 줄 수도 있다.

```java
Flux.just("A", "B", "A", "C", "B").distinct();            // "A", "B", "C"
userFlux.distinct(User::getName);                           // 이름 기준 중복 제거
```

### take / skip

처음 n개만 원하면 `take`, 처음 n개를 버리려면 `skip`을 쓰면 된다. 시간 기반으로도 가능하다.

```java
Flux.range(1, 10).take(3);    // 1, 2, 3
Flux.range(1, 10).skip(3);    // 4, 5, 6, 7, 8, 9, 10
Flux.interval(Duration.ofSeconds(1)).take(Duration.ofSeconds(5));
```

```
take(3): ──(1)──(2)──(3)──|──>   (이후 상류 취소)
```

### next / last / elementAt

단일 요소만 뽑아내는 방법들:

```java
Flux.just("A", "B", "C").next();         // Mono<"A">
Flux.just("A", "B", "C").last();         // Mono<"C">
Flux.just("A", "B", "C").elementAt(1);   // Mono<"B">
```

---

## A.4 결합 연산자 (Combining Operators)

여러 스트림을 한데 모으는 방법들이다. 어떻게 합치느냐에 따라 완전히 달라진다.

| 연산자 | 설명 | 순서 보장 | 동시 구독 |
|--------|------|-----------|-----------|
| `zip` / `zipWith` | 각 소스의 요소를 쌍으로 결합 | 예 | 예 |
| `merge` / `mergeWith` | 도착 순서대로 인터리빙 | 아니오 | 예 |
| `concat` / `concatWith` | 순차적으로 연결 | 예 | 아니오 |
| `combineLatest` | 각 소스의 최신 값을 결합 | - | 예 |

### zip / zipWith

위치 기반으로 맞춰서 짝을 만든다. 첫 번째끼리, 두 번째끼리 묶는 식이다. 가장 짧은 쪽이 끝나면 전체가 끝난다.

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

여러 개를 동시에 받아놓고, 빨리 도착하는 순서대로 내보낸다. 순서는 무시한다.

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

하나가 다 끝난 뒤에 다음을 시작한다. 순서는 절대 섞이지 않는다.

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

어느 한쪽에서 새 값이 나올 때마다 반대쪽의 최신 값과 짝을 만든다. 두 스트림의 최신 상태를 항상 조합하고 싶을 때 유용하다.

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

뭔가 잘못되었을 때 어떻게 대응할지를 정하는 연산자들이다. 복구하기도, 재시도하기도, 때론 포기하기도 한다.

| 연산자 | 설명 |
|--------|------|
| `onErrorReturn` | 에러 시 대체 값을 발행하고 완료한다 |
| `onErrorResume` | 에러 시 대체 Publisher로 전환한다 |
| `onErrorMap` | 에러를 다른 예외로 변환한다 |
| `retry` | 에러 시 지정 횟수만큼 재구독한다 |
| `retryWhen` | 커스텀 재시도 전략을 적용한다 |
| `timeout` | 지정 시간 초과 시 에러를 발생시킨다 |

### onErrorReturn / onErrorResume / onErrorMap

에러가 나면 어떻게 할지에 따라 고르면 된다:

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

단순히 다시 시도만 하면 되면 `retry(n)`을 쓴다. 지수 백오프나 특정 에러만 재시도하는 식의 세밀한 제어가 필요하면 `retryWhen`으로 전략을 짠다.

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

어떤 작업이 너무 오래 걸리면? 시간을 초과하면 에러를 던진다. 아니면 대신 기본값을 건네줄 수도 있다.

```java
Mono<String> result = callSlowApi().timeout(Duration.ofSeconds(5));
Mono<String> withFallback = callSlowApi()
    .timeout(Duration.ofSeconds(5), Mono.just("타임아웃 대체 응답"));
```

---

## A.6 유틸리티 연산자 (Utility Operators)

데이터 자체는 건드리지 않으면서 옆에서 뭔가 일을 하거나, 흐름을 들여다보거나, 여러 곳에 공유한다.

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

스트림이 흘러가는 걸 봐야 할 때가 있다. 로깅, 메트릭 수집, 부수 효과 같은 것들에 쓴다. 데이터는 그대로 통과한다.

```java
Flux<User> pipeline = userService.findAll()
    .doOnSubscribe(sub -> log.info("사용자 조회 시작"))
    .doOnNext(user -> log.debug("사용자 발행: {}", user.getName()))
    .doOnError(e -> log.error("사용자 조회 실패", e))
    .doOnComplete(() -> log.info("사용자 조회 완료"));
```

### doFinally

스트림이 어떻게 끝나든(성공, 실패, 취소) 반드시 실행된다. 리소스 정리가 필요할 때 딱이다.

```java
Flux<Data> stream = dataSource.stream()
    .doFinally(signalType -> {
        log.info("종료 원인: {}", signalType); // ON_COMPLETE, ON_ERROR, CANCEL
        resourceCleanup();
    });
```

### log

파이프라인을 추적하고 싶을 땐 이걸 끼워넣으면 SLF4J로 모든 신호가 로깅된다. 디버깅할 때 매우 유용하다.

```java
Flux<Integer> traced = Flux.range(1, 3).log("my.category").map(i -> i * 10);
// [my.category] onNext(1) -> [after.map] onNext(10) -> ...
```

### delayElements / cache

발행을 의도적으로 늦추거나, 계산 결과를 임시 저장하고 싶을 때:

```java
Flux.just("A", "B", "C").delayElements(Duration.ofMillis(500));  // 500ms 간격 발행
Mono<Config> config = configService.load().cache(Duration.ofMinutes(5)); // 5분 캐싱
```

### share / replay

여러 곳에서 같은 스트림을 구독할 때, `share`면 하나의 구독을 나눠 쓴다. `replay`를 쓰면 예전 값들을 새 구독자에게도 줄 수 있다.

```java
Flux<Long> shared = Flux.interval(Duration.ofSeconds(1)).share();
// 이후 구독자는 진행 중인 스트림에 합류 (과거 요소 유실)

Flux<Long> replayed = Flux.interval(Duration.ofSeconds(1))
    .replay(3).autoConnect();
// 새 구독자에게 최근 3개 요소를 재생 후 실시간 합류
```

---

## A.7 배압 연산자 (Backpressure Operators)

생산자가 너무 빨리 내보내는데 소비자가 못 따라가면? 그럴 때 초과분을 어떻게 처리할지 정한다.

| 연산자 | 초과 요소 처리 방식 |
|--------|---------------------|
| `onBackpressureBuffer` | 내부 버퍼에 저장 (용량 초과 시 에러 또는 드롭) |
| `onBackpressureDrop` | 즉시 폐기 |
| `onBackpressureLatest` | 최신 1개만 유지, 나머지 폐기 |
| `limitRate` | 하류의 request 크기를 제한 |

### onBackpressureBuffer / onBackpressureDrop / onBackpressureLatest

초과분을 어떻게 처리할지:

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

상류에 요청하는 양을 조절한다. 한 번에 얼마나 가져올지, 언제 다시 채울지를 정할 수 있다.

```java
Flux<Data> controlled = dataFlux.limitRate(100);          // 100개씩 요청
Flux<Data> precise = dataFlux.limitRate(100, 50);         // prefetch 100, lowTide 50
```

---

## A.8 연산자 선택 가이드

뭔가 하려고 할 때 어떤 연산자를 써야 할지 모르겠다면 이 표를 보면 된다.

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

실제 코드에서 자주 보는 패턴들을 모아봤다. 이런 식으로 여러 연산자를 조합하면 견고한 리액티브 파이프라인을 만들 수 있다.

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

여러 작업을 동시에 실행하되 결과를 합쳐야 할 때:

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

필자의 경험상, 자주 접근하는 데이터는 캐싱해서 반복 호출을 줄이는 게 좋다:

```java
Mono<Config> sharedConfig = configService.load()
    .cache(Duration.ofMinutes(10))
    .doOnSubscribe(s -> log.debug("설정 조회"));
// 여러 곳에서 구독해도 10분간 한 번만 로딩
```

---

> **참고**: 이 부록은 Reactor 3.x 기준으로 작성했다. 각 연산자의 세부 사항과 여러 오버로드는 [Project Reactor 공식 문서](https://projectreactor.io/docs/core/release/api/)를 참고하면 된다.
# 부록 B. MongoDB 쿼리 연산자 정리

MongoDB를 다루다 보면 반복해서 찾게 되는 쿼리 연산자들이 있다. 이 부록은 그런 연산자들을 카테고리별로 모아 놓고, MongoDB 네이티브 쿼리와 Spring Data MongoDB(Criteria API)의 Java 코드를 함께 보여주는 것이 목표다. 필자의 경험상 실무에서는 이 정도 연산자들만 잘 이해해도 대부분의 쿼리를 충분히 작성할 수 있다.

---

## B.1 비교 연산자

가장 자주 마주하는 연산자들이다. 값을 비교하거나 범위를 지정할 때 필요한 것들.

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

실제로는 여러 조건을 조합해서 쓰는 경우가 많으니 예제를 살펴보자.

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

복잡한 조건을 만들어야 할 때 논리 연산자가 나온다. AND, OR 같은 연산들인데, Criteria API를 쓸 때는 직관적으로 처리할 수 있다.

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

특정 필드의 존재 여부나 타입을 확인할 때 사용한다. 데이터가 불완전하거나 스키마 마이그레이션 과정에서 유용하게 쓸 수 있다.

| 연산자 | 설명 | MongoDB 쿼리 예제 | Spring Data Criteria |
|--------|------|-------------------|---------------------|
| `$exists` | 필드 존재 여부 확인 | `{ email: { $exists: true } }` | `Criteria.where("email").exists(true)` |
| `$type` | 필드의 BSON 타입 확인 | `{ age: { $type: "int" } }` | `Criteria.where("age").type(Type.INT32)` |

---

## B.4 배열 연산자

배열 필드를 다루는 데 필요한 연산자들이다. tags나 scores 같은 배열을 검색할 때 자주 쓰게 된다.

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

문자열 검색이 필요할 때가 있다. 정확한 일치가 아니라 패턴 기반의 검색을 해야 한다면 정규식을 활용하자.

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

SELECT와 함께 UPDATE도 중요하다. 도큐먼트를 수정할 때 사용하는 연산자들을 정리했다.

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

Aggregation Pipeline은 MongoDB의 강력한 기능이다. 여러 단계를 거쳐서 복잡한 데이터 변환과 집계를 할 수 있으며, 필자의 경험상 실무에서 리포팅 기능을 구현할 때 정말 유용하게 쓰인다.

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

이론만으로는 와닿지 않으니 실전 예제를 살펴보자. 카테고리별 매출 상위 5개를 조회하는 파이프라인이다.

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

인덱스는 쿼리 성능을 좌우하는 핵심 요소다. 어떤 인덱스 전략을 쓰느냐에 따라 조회 성능이 크게 달라진다.

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

일상적인 작업들을 패턴으로 정리했다. 이 정도는 프로젝트마다 거의 똑같이 쓰는 코드들이다.

### 페이징 처리

```java
Query query = Query.query(Criteria.where("status").is("active"))
    .with(Sort.by(Sort.Direction.DESC, "createdAt"))
    .skip(page * size).limit(size);
reactiveMongoTemplate.find(query, Article.class);
```

### Upsert - 존재하면 수정, 없으면 삽입

```java
Query query = Query.query(Criteria.where("userId").is(userId).and("date").is(today));
Update update = new Update()
    .set("lastAccess", LocalDateTime.now())
    .inc("visitCount", 1)
    .setOnInsert("createdAt", LocalDateTime.now());
reactiveMongoTemplate.upsert(query, update, UserActivity.class);
```

### 동적 쿼리 생성

검색 기능을 구현할 때는 사용자가 입력한 조건에 따라 쿼리를 동적으로 만들어야 한다. 다음은 그런 상황을 처리하는 예제다.

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

> **참고**: 여기서 다룬 연산자들은 가장 자주 쓰이는 것들일 뿐, MongoDB는 훨씬 더 많은 기능을 제공한다. 더 알아보려면 [MongoDB 공식 문서](https://www.mongodb.com/docs/manual/reference/operator/)를 참고하고, Spring Data MongoDB의 Criteria API에 대해서는 [Spring Data MongoDB 레퍼런스](https://docs.spring.io/spring-data/mongodb/reference/)를 확인하자.
# 부록 C. 자주 발생하는 문제와 해결 방법 (FAQ)

Spring WebFlux와 MongoDB 리액티브 스택을 사용하며 프로젝트를 진행하다 보면, 명령형 프로그래밍에서는 경험하지 못했던 새로운 종류의 이슈들과 마주하게 된다. 필자의 경험상 이런 문제들은 대부분 리액티브의 핵심 개념—특히 스레드 모델과 Context 전파 메커니즘—을 명확히 이해하면 자연스럽게 해결된다.

이 부록에서는 실무에서 가장 자주 발생하는 15가지 문제를 모았다. 각 항목마다 증상을 먼저 보여주고, 왜 그런 일이 생기는지 원인을 분석한 뒤, 어떻게 대처할 수 있을지 구체적인 해결책을 제시했다.

---

## FAQ 1. "block()/blockFirst()/blockLast() are blocking" 에러

**증상**: 리액티브 파이프라인 내부에서 `block()`을 호출하면 `IllegalStateException`이 튀어나온다.

**원인 분석**: Netty의 이벤트 루프 스레드에서 `block()`을 부르면 그 스레드가 대기 상태(blocking)로 빠진다. 이벤트 루프 스레드가 멈추는 순간 다른 모든 요청들의 처리가 중단되어 버린다. Reactor는 이 위험한 상황을 미리 감지하고 예외를 던져서 문제를 드러낸다.

**해결 방법**: `block()` 대신 `flatMap`, `zip`, `then` 같은 리액티브 연산자로 흐름을 이어가자.

```java
// 잘못된 코드
User user = userRepository.findById(userId).block(); // 예외 발생!

// 올바른 코드
return userRepository.findById(userId)
    .flatMap(user -> profileRepository.findByUser(user));
```

혹시 레거시 코드를 호출해야 하거나, 부득이하게 블로킹 호출이 필요하다면 `Schedulers.boundedElastic()`으로 스레드를 전환해서 처리한다.

```java
Mono.fromCallable(() -> legacyBlockingService.call())
    .subscribeOn(Schedulers.boundedElastic());
```

---

## FAQ 2. "Scheduler was blocked" 에러와 BlockHound

**증상**: BlockHound를 켜면 갑자기 `BlockingOperationError: Blocking call!` 같은 에러가 날아온다.

**원인 분석**: BlockHound는 개발/테스트 단계에서 코드의 블로킹 호출(파일 I/O, `Thread.sleep` 등)을 런타임에 적발하는 도구다. 의도하지 않은 블로킹이 발견되는데, 특히 서드파티 라이브러리나 드라이버에 숨어 있는 경우가 많다.

**해결 방법**: BlockHound를 테스트 의존성으로 등록한 후, 불가피한 블로킹 호출들을 화이트리스트에 추가해서 허용한다.

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

**증상**: 운영 중에 갑자기 `MongoTimeoutException: Timed out after 30000 ms while waiting for a server` 같은 에러가 터진다.

**원인 분석**: 원인은 여러 가지일 수 있다. 커넥션 풀이 꽉 찬 경우, 네트워크 지연이 심한 경우, MongoDB 레플리카 셋 구성이 변경된 경우, DNS 조회가 지연되는 경우 등 다양한 시나리오가 있다.

**해결 방법**: `MongoClientSettings`를 적절하게 구성해서 커넥션 풀 크기와 타임아웃 값들을 직접 조정해 보자.

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

**증상**: `ReactiveSecurityContextHolder.getContext()`를 호출했는데 빈 `Mono`만 돌아온다.

**원인 분석**: Spring Security의 리액티브 구현은 전통적인 `ThreadLocal` 방식이 아니라 Reactor Context를 기반으로 동작한다. 리액티브 체인이 끊어지거나 맥락을 잃으면, 보안 정보도 함께 사라진다.

**해결 방법**: 가장 좋은 방법은 리액티브 체인을 계속 유지하는 것이고, 그것이 어렵다면 컨트롤러의 메서드 파라미터로 직접 주입받자.

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

**증상**: `@Transactional` 어노테이션을 달았는데 MongoDB 작업이 트랜잭션으로 처리되지 않는 것처럼 보인다.

**원인 분석**: MongoDB 트랜잭션을 지원하려면 먼저 레플리카 셋(Replica Set) 구성이 있어야 한다. 추가로 Spring이 제공하는 `ReactiveMongoTransactionManager` 빈이 정확히 등록되어 있어야 작동한다.

**해결 방법**: MongoDB를 레플리카 셋으로 초기화하고, Spring 설정에서 트랜잭션 매니저를 명시적으로 빈으로 등록한다.

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

**증상**: 같은 `Flux`를 여러 군데서 구독하면, DB 쿼리가 구독할 때마다 중복 실행된다.

**원인 분석**: Reactor의 `Flux`와 `Mono`는 기본적으로 Cold Publisher 패턴으로 설계되어 있다. 즉, 새로운 구독자가 나타날 때마다 데이터 생성 로직이 처음부터 독립적으로 시작되므로, 데이터베이스 쿼리도 반복해서 실행되는 것이다.

**해결 방법**: 상황에 맞춰 `cache()` 또는 `share()`를 사용해서 Hot Publisher 특성으로 변환하자.

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

**증상**: 서버에서 큰 파일이나 응답을 받으려고 하면 `Exceeded limit on max bytes to buffer : 262144` 같은 에러가 뜬다.

**원인 분석**: WebClient는 기본값으로 응답 전체를 메모리에 버퍼링할 때 256KB 제한을 두고 있다. 그 이상의 데이터를 받으려고 하면 자동으로 차단한다.

**해결 방법**: 버퍼 크기를 늘리거나, 대용량 응답은 스트리밍 방식으로 처리한다.

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

**증상**: MDC에 넣어놓은 `traceId` 값이 리액티브 파이프라인을 거치면서 어느 순간 `null`이 되어 있다.

**원인 분석**: MDC는 `ThreadLocal` 메커니즘에 의존한다. 한 번의 요청이 여러 스레드를 거쳐 처리되는 리액티브 환경에서는, 스레드가 바뀔 때마다 MDC 값이 전달되지 않는다.

**해결 방법**: Micrometer Context Propagation 라이브러리를 사용하면, Context 값이 자동으로 동기화되도록 할 수 있다.

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

**증상**: Change Streams로 변경 이벤트를 수신하다가 MongoDB 장애나 네트워크 단절이 발생하면 스트림이 완전히 끊어져 버린다.

**원인 분석**: 네트워크가 끊기거나 MongoDB 레플리카 셋의 프라이머리가 바뀌면 자동으로 롱 커넥션이 종료된다. 이때 자동 재연결 및 재시작 로직이 없으면, 애플리케이션은 이벤트를 받을 수 없는 상태에 빠진다.

**해결 방법**: `retryWhen`으로 재시도 로직을 구성하고, Resume Token을 저장했다가 활용하면 끊긴 지점부터 다시 받을 수 있다.

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

**증상**: `StepVerifier` 테스트를 실행했는데 기본 타임아웃인 10초를 넘기고 `AssertionError`로 실패한다.

**원인 분석**: 테스트하는 코드가 완료 신호(`onComplete`)를 발행하지 않으면, `StepVerifier`는 계속 대기한다. 빈 결과가 나오거나, 구독이 제대로 안 되었거나, 의도하지 않은 무한 스트림이 있는 경우들이 원인이다.

**해결 방법**: 테스트 상황에 맞춰 적절한 검증 메서드를 선택해서 사용한다.

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

**증상**: GraalVM Native Image로 빌드한 후 실행하면 `ClassNotFoundException`이 터진다.

**원인 분석**: Native Image는 빌드 당시의 정적 분석만으로 어떤 클래스들이 필요한지 판단한다. 런타임에 리플렉션으로 동적으로 로드하는 클래스들은 빌드 결과에 포함되지 않을 가능성이 높다.

**해결 방법**: Spring Boot 3.x부터 제공하는 AOT(Ahead-of-Time) 기능을 활용하고, 필요한 클래스들을 힌트로 명시한다.

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

**증상**: 프론트엔드 애플리케이션에서 백엔드 API를 호출했는데 브라우저 콘솔에 CORS 에러가 떠 있다.

**원인 분석**: 브라우저는 보안상 다른 도메인이나 포트로의 요청을 차단하는 정책을 기본으로 가지고 있다. Spring Security를 사용하는 경우, WebFlux 레벨의 CORS 설정만으로는 부족하고 보안 필터 레벨에서도 별도로 설정해야 한다.

**해결 방법**: WebFlux 설정과 Security 설정 두 곳 모두에서 CORS를 제대로 구성해야 한다.

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

**증상**: WebSocket 연결을 맺은 후 한동안 놔두면 일정 시간이 지나서 자동으로 끊어진다.

**원인 분석**: 필자의 경험상 이것은 대부분 중간의 프록시나 로드밸런서의 유휴 타임아웃 때문이다. Nginx는 기본으로 60초 동안 활동이 없는 연결을 종료한다.

**해결 방법**: WebSocket 연결을 주기적으로 ping/pong 메시지로 살려두면 타임아웃을 피할 수 있다.

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

Nginx 설정에서 `proxy_read_timeout`을 충분히 큰 값으로 늘려주는 것도 좋은 방법이다(예: `3600s`).

---

## FAQ 14. 메모리 누수 (구독 해제 미처리)

**증상**: 애플리케이션이 오래 실행될수록 힙 메모리가 계속 증가해서 결국 `OutOfMemoryError`가 난다.

**원인 분석**: `interval`, SSE, WebSocket 등으로 만든 무한 `Flux`를 구독한 후 제대로 종료하지 않으면, 구독 객체와 내부 버퍼들이 GC의 대상이 되지 않아 메모리에 계속 쌓인다.

**해결 방법**: `Disposable` 객체를 적절히 관리하고, 애플리케이션이나 컴포넌트의 생명주기에 맞춰 제때 해제해야 한다.

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

SSE 엔드포인트의 경우, `doOnCancel()` 콜백으로 클라이언트 연결이 끊어지는 순간을 감지해서 필요한 리소스를 즉시 정리하는 것이 좋은 패턴이다.

---

## FAQ 15. Reactor Context 전파 문제

**증상**: `contextWrite()`로 값을 저장하고 `deferContextual()`로 읽으려 하는데 값이 없다고 나온다.

**원인 분석**: Reactor Context는 구독자 쪽에서 발행자 쪽으로(즉, 아래에서 위로) 향해 전파된다. 만약 `contextWrite()`가 체인의 상류에 있으면, 그 아래의 연산자들은 해당 Context를 볼 수 없다.

**해결 방법**: `contextWrite()`를 체인의 하류(구독자가 있는 쪽)에 배치해야 값이 제대로 전파된다.

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

실무에서는 여러 레이어를 거치는 Context를 일관되게 전파하려면, `WebFilter`에서 한 번에 설정하는 방식이 가장 깔끔하다.

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

15가지 문제를 훑어본 결과, 리액티브 프로그래밍에서 발생하는 대부분의 이슈는 근본적으로 다음 세 가지 원칙과 맞닿아 있음을 알 수 있다.

1. **체인을 끊지 마라**: 리액티브 파이프라인은 연속된 하나의 체인으로 유지되어야 한다. `block()` 호출, 새로운 구독 시점 추가, 중간에 변수로 빼내기 등으로 체인을 끊으면, Context 전파가 끊어지고 에러 처리와 백프레셔가 제대로 작동하지 않는다.

2. **스레드를 가정하지 마라**: 리액티브 코드는 어떤 스레드에서 실행될지 예측할 수 없다. 따라서 `ThreadLocal`, `synchronized` 블록, 특정 스레드에 고정된 가변 상태 같은 것은 피해야 한다.

3. **구독 생명주기를 관리하라**: 모든 구독은 정상적으로 완료되거나 명시적으로 해제되어야 한다. 특히 무한 스트림(`interval`, SSE, WebSocket 등)을 구독할 때는 반드시 해제 로직을 함께 작성해야 한다.

이 세 가지 원칙을 머릿속에 새기고 개발한다면, 이 부록에서 다룬 거의 모든 문제를 미리 방지할 수 있을 것이다.
# 부록 D. 참고 자료 및 추천 학습 경로

이 부록에서는 Spring WebFlux와 리액티브 프로그래밍을 더 깊이 있게 학습하기 위한 참고 자료들을 소개하고, 체계적인 학습 로드맵을 제시한다. 각 카테고리별로 정리된 자료들은 모두 실전에서 직접 활용할 수 있는 것들만 모아봤다.

---

## D.1 공식 문서

공식 문서가 가장 정확하고 최신 정보의 가장 확실한 출처다. 뭔가 헷갈릴 때나 새로운 기능을 알아봐야 할 땐 공식 문서부터 살펴보는 습관이 필수다.

### Spring WebFlux

- **Spring Framework Reference - Web Reactive**: https://docs.spring.io/spring-framework/reference/web/webflux.html
  - WebFlux의 아키텍처부터 핸들러 함수, 라우터 함수, WebClient 같은 핵심 개념들을 담고 있다.
  - 어노테이션 기반 컨트롤러와 함수형 엔드포인트의 차이가 궁금할 땐 꼭 읽어봐야 할 문서다.

- **Spring Boot Reference - Reactive Web**: https://docs.spring.io/spring-boot/reference/web/reactive.html
  - Spring Boot에서 WebFlux를 어떻게 자동 구성하는지, 어떤 옵션들을 쓸 수 있는지 정리되어 있다.

### Project Reactor

- **Reactor Core Reference Guide**: https://projectreactor.io/docs/core/release/reference/
  - Mono와 Flux가 어떻게 동작하는지, 연산자를 어떻게 체인으로 엮는지, 스케줄러와 에러 처리까지 모두 다룬다.
  - 리액티브 스트림을 제대로 이해하려면 반드시 봐야 할 필수 문서다.

- **Reactor Operator Reference**: https://projectreactor.io/docs/core/release/api/
  - 모든 연산자의 마블 다이어그램과 사용 예제가 들어있다.
  - 실무에서 어떤 연산자를 써야 할지 모를 때 정말 자주 찾게 되는 자료다.

### Spring Data MongoDB

- **Spring Data MongoDB Reference**: https://docs.spring.io/spring-data/mongodb/reference/
  - ReactiveMongoRepository나 ReactiveMongoTemplate을 어떻게 쓰는지, 쿼리를 어떻게 작성하는지 설명된다.
  - Tailable Cursor, Change Stream처럼 리액티브에만 있는 기능들도 함께 담겨 있다.

### MongoDB

- **MongoDB Manual**: https://www.mongodb.com/docs/manual/
  - 인덱싱부터 집계 파이프라인, 트랜잭션, 레플리카 셋까지 MongoDB의 핵심 기능들이 모두 들어있다.

- **MongoDB Reactive Streams Driver**: https://www.mongodb.com/docs/languages/java/reactive-streams-driver/current/
  - Java Reactive Streams 드라이버를 어떻게 사용하는지, 연결 풀은 어떻게 설정하는지, 성능을 어떻게 튜닝하는지 나와있다.

### Spring Security

- **Spring Security Reactive**: https://docs.spring.io/spring-security/reference/reactive/index.html
  - WebFlux에서 인증과 인가를 어떻게 설정하고, SecurityWebFilterChain은 어떻게 구성하는지, OAuth2 리액티브 지원은 어떤지 설명된다.
  - 기존 서블릿 기반 보안 설정과 뭐가 다른지 명확하게 알 수 있다.

---

## D.2 추천 서적

### 리액티브 프로그래밍

- **"Reactive Programming with RxJava"** - Tomasz Nurkiewicz, Ben Christensen (O'Reilly)
  - RxJava 기반이긴 하지만, 리액티브 프로그래밍의 핵심 개념과 패턴을 깊이 있게 다룬다는 게 장점이다.
  - Reactor의 연산자 구조와 유사해서 개념을 이해하는 데 정말 많은 도움이 된다.

- **"Reactive Streams in Java"** - Adam L. Davis (Apress)
  - 리액티브 스트림 명세부터 시작해서 Reactor, RxJava, Akka Streams를 비교하며 설명한다.
  - 책의 분량이 짧은 편이라 핵심을 빨리 파악하기에 딱 좋다.

- **"Hands-On Reactive Programming in Spring 5"** - Oleh Dokuka, Igor Lozynskyi (Packt)
  - Spring WebFlux와 Project Reactor를 실제로 손으로 직접 짜보면서 배울 수 있다.
  - 리액티브 시스템을 어떻게 설계하는지, 테스트는 어떻게 하는지까지 다룬다.

### Spring 프레임워크

- **"Spring in Action, 6th Edition"** - Craig Walls (Manning)
  - Spring Boot와 WebFlux를 포함한 최신 Spring 생태계 전반을 다룬다.
  - WebFlux 챕터에서 리액티브 웹 개발의 기초를 확실히 다질 수 있다.

- **"Spring Boot Up & Running"** - Mark Heckler (O'Reilly)
  - Spring Boot가 어떻게 자동으로 설정되는지 그 원리부터 실무에서는 어떻게 활용하는지 체계적으로 설명한다.

- **"Cloud Native Spring in Action"** - Thomas Vitale (Manning)
  - 클라우드 네이티브 환경에서 Spring 애플리케이션을 어떻게 설계하고 배포할 것인지 다룬다.
  - Kubernetes나 GraalVM Native Image 같은 최신 배포 기술들을 어떻게 적용하는지 설명되어 있다.

### MongoDB

- **"MongoDB: The Definitive Guide, 3rd Edition"** - Shannon Bradshaw 외 (O'Reilly)
  - 데이터 모델링부터 인덱싱 전략, 레플리케이션, 샤딩까지 MongoDB의 거의 모든 영역을 깊이 있게 다룬다.

- **"MongoDB in Action, 2nd Edition"** - Kyle Banker 외 (Manning)
  - 실제 업무에서 마주칠 만한 시나리오들을 중심으로 MongoDB를 학습할 수 있게 구성되어 있다.

### Java 및 Kotlin

- **"Modern Java in Action"** - Raoul-Gabriel Urma 외 (Manning)
  - 람다, 스트림, CompletableFuture 같은 Java 기능들이 리액티브 프로그래밍의 기반이 되는데, 이들을 다룬다.

- **"Java Concurrency in Practice"** - Brian Goetz 외 (Addison-Wesley)
  - 동시성 프로그래밍이 어떻게 작동하는지 근본부터 이해하려면 반드시 봐야 할 책다.
  - 리액티브 모델이 결국 어떤 문제를 풀려고 하는 건지도 깊게 이해할 수 있다.

- **"Kotlin in Action, 2nd Edition"** - Roman Elizarov 외 (Manning)
  - 코루틴과 Flow를 포함해서 Kotlin의 핵심 기능들을 체계적으로 설명한다.

---

## D.3 온라인 강의 및 튜토리얼

### 온라인 강의 플랫폼

- **Udemy - "Build Reactive MicroServices using Spring WebFlux/SpringBoot"** (Dilip Sundarraj)
  - WebFlux, WebClient, 리액티브 MongoDB를 활용해서 실제 마이크로서비스를 구축하는 실습을 한다.

- **Udemy - "Reactive Programming in Modern Java using Project Reactor"** (Dilip Sundarraj)
  - Project Reactor의 Mono와 Flux 연산자를 단계적으로 배워나갈 수 있다.

- **Coursera - "Reactive Programming"** (EPFL/Scala 기반)
  - 리액티브 프로그래밍을 학술적인 관점에서 기초부터 다지고 싶다면 괜찮다.

- **Spring Academy**: https://spring.academy/
  - VMware(Broadcom)에서 운영하는 공식 Spring 학습 플랫폼이다.
  - Spring Boot, Spring Security 같은 과정들을 무료로 수강할 수 있고, 공식 인증까지 받을 수 있다.

### YouTube 채널

- **Spring Developer** (https://www.youtube.com/@SpringSourceDev)
  - SpringOne 컨퍼런스의 발표 영상이나 기술 데모들을 공식적으로 올려준다.

- **Java Brains** (https://www.youtube.com/@Java.Brains)
  - Spring Boot와 리액티브 프로그래밍을 초보자 입장에서 친절하게 설명해준다.

- **Telusko** (https://www.youtube.com/@Telusko)
  - Java와 Spring 생태계를 깊고 넓게 다루는 인도 기반 채널이다.

### 블로그 및 기술 아티클

- **Baeldung** (https://www.baeldung.com/)
  - Spring과 Java 관련 튜토리얼이 정말 많이 있다. WebFlux, Reactor, MongoDB 관련 글들도 풍부하다.
  - 코드 예제들이 모두 실용적이고 시간이 지나도 꾸준히 업데이트되는 편이다.

- **Spring Blog** (https://spring.io/blog)
  - 새 버전 릴리스 정보, 마이그레이션 가이드, 모범 사례 같은 것들을 공식적으로 발행한다.

- **Project Reactor Blog** (https://projectreactor.io/blog)
  - Reactor의 새로운 기능이 뭐가 추가됐고, 성능이 어떻게 개선됐고, 어떻게 활용하면 좋을지 정보를 제공한다.

- **DZone** (https://dzone.com/)
  - 리액티브 프로그래밍이나 마이크로서비스 아키텍처 같은 실무 아티클들을 많이 볼 수 있다.

---

## D.4 커뮤니티 및 도구

### GitHub 레포지토리

- **spring-projects/spring-framework**: https://github.com/spring-projects/spring-framework
  - WebFlux 모듈의 소스 코드를 직접 읽어볼 수 있어서 내부가 어떻게 동작하는지 이해할 수 있다.

- **reactor/reactor-core**: https://github.com/reactor/reactor-core
  - Reactor의 핵심 구현 코드다. 각 연산자가 실제로 어떻게 동작하는지 궁금할 땐 여기를 봐야 한다.

- **spring-projects/spring-data-examples**: https://github.com/spring-projects/spring-data-examples
  - 리액티브 MongoDB를 포함해서 여러 Spring Data 모듈의 예제 코드들이 들어있다.

- **hantsy/spring-reactive-sample**: https://github.com/hantsy/spring-reactive-sample
  - WebFlux 기반 애플리케이션을 어떻게 다양하게 구성할 수 있는지 보여주는 종합 예제 프로젝트다.

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

- **Spring Community Gitter/GitHub Discussions**: Spring 프로젝트별 Discussions 탭에서 공식적인 질의응답이 이루어진다.
- **Reddit r/java, r/spring**: Java와 Spring 관련 기술 토론을 보고, 최신 동향도 따라잡을 수 있다.
- **Korean Spring User Group**: 한국 Spring 사용자 모임에서 한국어로 기술 교류를 할 수 있다.

---

## D.5 추천 학습 경로

초보 개발자부터 고급 최적화를 목표로 하는 개발자까지, 각 수준별로 단계적으로 학습할 수 있는 경로를 제시해본다. 필자의 경험상 이 순서대로 따라가면 리액티브 프로그래밍을 가장 무리 없이 습득할 수 있다.

### 초급 단계 (약 8~12주)

**목표**: Java와 Spring Boot의 기초를 다지고, MongoDB의 기본 사용법을 익힌다.

| 주차 | 학습 내용 | 주요 자료 |
|------|-----------|-----------|
| 1~2주 | Java 핵심 문법, 람다, 스트림 API | Modern Java in Action |
| 3~4주 | Spring Boot 기초, REST API 구축 | Spring Academy, Baeldung |
| 5~6주 | MongoDB 기초, CRUD 연산, 인덱싱 | MongoDB Manual, MongoDB University |
| 7~8주 | Spring Data MongoDB 기본 사용법 | 공식 문서, Spring Data Examples |
| 9~12주 | 간단한 CRUD 프로젝트 완성 | GitHub 예제 프로젝트 참고 |

**이정표**: Spring Boot와 MongoDB로 간단한 REST API 서버를 직접 만들어볼 수 있으면 이 단계는 충분하다.

### 중급 단계 (약 8~12주)

**목표**: 리액티브 프로그래밍의 패러다임을 제대로 이해하고, WebFlux와 Reactor로 비동기 애플리케이션을 구축한다.

| 주차 | 학습 내용 | 주요 자료 |
|------|-----------|-----------|
| 1~2주 | 리액티브 스트림 개념, 백프레셔 원리 | Reactor Reference Guide |
| 3~4주 | Mono, Flux 연산자 심화 학습 | Reactor Operator Reference |
| 5~6주 | WebFlux 컨트롤러, 함수형 엔드포인트 | Spring WebFlux 공식 문서 |
| 7~8주 | WebClient, 리액티브 보안 설정 | Spring Security Reactive 문서 |
| 9~10주 | 리액티브 MongoDB 연동, Change Stream | Spring Data MongoDB Reference |
| 11~12주 | 리액티브 테스트 전략 (StepVerifier, WebTestClient) | 본서 관련 챕터 |

**이정표**: WebFlux와 리액티브 MongoDB를 조합해서 완전한 비동기 애플리케이션을 만들고, 제대로 테스트할 수 있으면 좋다.

### 고급 단계 (약 8~16주)

**목표**: 프로덕션 환경에서 실제로 돌아가는 성능 최적화, 모니터링, 배포까지 모두 아우른다.

| 주차 | 학습 내용 | 주요 자료 |
|------|-----------|-----------|
| 1~3주 | 성능 프로파일링, 메모리 최적화, 백프레셔 튜닝 | 본서 관련 챕터, Reactor 공식 문서 |
| 4~6주 | Micrometer, Prometheus, Grafana 모니터링 구축 | Spring Boot Actuator 공식 문서 |
| 7~9주 | Docker 컨테이너화, Kubernetes 배포 | Cloud Native Spring in Action |
| 10~12주 | GraalVM Native Image 빌드 및 최적화 | Spring Boot AOT 공식 문서 |
| 13~16주 | 대규모 트래픽 시나리오 부하 테스트 및 튜닝 | Gatling, k6 공식 문서 |

**이정표**: 프로덕션 환경에서 안정적으로 운영 가능한 리액티브 시스템을 직접 설계하고 배포할 수 있으면 충분하다.

---

## D.6 관련 기술 스택 로드맵

이 책의 내용을 잘 이해한 후에 다음 기술들을 추가로 공부하면 리액티브 생태계를 훨씬 더 깊이 있게 이해할 수 있다.

### Spring Cloud Gateway

- **개요**: WebFlux 위에 구축된 리액티브 기반 API 게이트웨이다.
- **학습 포인트**: 라우트 설정, 필터 체인, 속도 제한(Rate Limiting), 서킷 브레이커 통합
- **공식 문서**: https://docs.spring.io/spring-cloud-gateway/reference/
- **선수 지식**: WebFlux, Spring Security Reactive
- **활용 사례**: 마이크로서비스 아키텍처에서 모든 요청의 진입점이 되고, 인증, 로깅, 트래픽 제어 같은 걸 한곳에서 관리한다.

### Apache Kafka와 리액티브 연동

- **개요**: 대용량 이벤트를 처리하는 Kafka를 리액티브 시스템과 함께 쓰는 거다.
- **학습 포인트**: Reactor Kafka, Spring Cloud Stream, 이벤트 드리븐 아키텍처
- **공식 문서**: https://projectreactor.io/docs/kafka/release/reference/
- **선수 지식**: Reactor 연산자, 백프레셔 개념, Kafka 기초
- **활용 사례**: 실시간 데이터 파이프라인, CQRS 패턴, 이벤트 소싱 같은 게 필요할 때 쓴다.

### GraphQL과 WebFlux

- **개요**: REST API의 오버페칭/언더페칭 문제를 해결하는 쿼리 언어를 리액티브로 구현한 거다.
- **학습 포인트**: Spring for GraphQL, 스키마 정의, DataLoader, Subscription(실시간 스트리밍)
- **공식 문서**: https://docs.spring.io/spring-graphql/reference/
- **선수 지식**: WebFlux, GraphQL 기초 문법
- **활용 사례**: 데이터 관계가 복잡한 API를 만들 때 클라이언트가 필요한 데이터만 정확히 받을 수 있고, Subscription으로 실시간 업데이트도 가능하다.

### Kotlin Coroutines와 WebFlux

- **개요**: Kotlin의 코루틴을 쓰면 리액티브 코드를 마치 동기 코드처럼 작성할 수 있다.
- **학습 포인트**: suspend 함수, Flow, 코루틴 컨텍스트, Spring WebFlux의 코루틴 지원
- **공식 문서**: https://docs.spring.io/spring-framework/reference/languages/kotlin/coroutines.html
- **선수 지식**: Kotlin 기본 문법, WebFlux 기초
- **활용 사례**: Reactor 연산자 체인 대신 일반적인 순차 코드 스타일로 비동기 로직을 짜면 훨씬 읽기 쉬워진다. Mono는 suspend 함수로, Flux는 Flow로 자연스럽게 변환할 수 있다.

### 추가로 주목할 기술

- **R2DBC**: 리액티브 관계형 데이터베이스 접근 방식이다. PostgreSQL이나 MySQL 같은 DB를 비동기로 써야 할 땐 필수다.
- **RSocket**: 리액티브 스트림 기반의 양방향 통신 프로토콜다. 마이크로서비스 간 통신이 효율적이 돼야 할 때 써본 만하다.
- **Testcontainers**: 통합 테스트할 때 MongoDB나 Kafka 같은 걸 Docker 컨테이너로 띄워서 실제 환경처럼 테스트할 수 있다.
- **Virtual Threads (Project Loom)**: Java 21부터 생긴 가상 스레드인데, 리액티브 모델과의 관계를 이해하고 상황에 맞게 동시성 모델을 선택하는 감각을 키운다.

---

> **학습 팁**: 책이나 문서를 읽는 것만으로는 절대 부족하다. 직접 손으로 코드를 짜보고, 실행해보고, 실패도 경험하면서 배워야 한다. 특히 리액티브 프로그래밍은 사고 방식 자체가 달라져야 하기 때문에, 작은 프로젝트부터 차근차근 시작해서 조금씩 난이도를 올려나가는 게 가장 좋다.
