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
