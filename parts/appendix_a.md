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
    .doOnError(e -> log.error("API 호출 최종 실패", e))
    .onErrorResume(e -> Mono.just(Response.fallback()));
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
