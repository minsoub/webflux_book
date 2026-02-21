# Chapter 21. 실전 프로젝트: 실시간 게시판 서비스

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
    implementation 'io.jsonwebtoken:jjwt-api:0.13.0'
    runtimeOnly 'io.jsonwebtoken:jjwt-impl:0.13.0'
    runtimeOnly 'io.jsonwebtoken:jjwt-jackson:0.13.0'
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
            @AuthenticationPrincipal String principalId) {
        return userRepository.findById(principalId)
            .flatMap(u -> postService.createPost(request, principalId, u.getNickname()))
            .map(PostResponse::from);
    }

    @GetMapping("/{postId}")
    public Mono<PostResponse> getPost(@PathVariable String postId) {
        return postService.getPost(postId).map(PostResponse::from);
    }

    @PutMapping("/{postId}")
    public Mono<PostResponse> updatePost(@PathVariable String postId,
            @Valid @RequestBody PostRequest request,
            @AuthenticationPrincipal String principalId) {
        return postService.updatePost(postId, request, principalId)
            .map(PostResponse::from);
    }

    @DeleteMapping("/{postId}") @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deletePost(@PathVariable String postId,
            @AuthenticationPrincipal String principalId) {
        return postService.deletePost(postId, principalId);
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
    static MongoDBContainer mongo = new MongoDBContainer("mongo:7.0");

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
