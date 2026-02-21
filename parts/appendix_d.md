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
