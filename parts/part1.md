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
