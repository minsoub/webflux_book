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
