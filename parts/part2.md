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
