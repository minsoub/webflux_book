#!/usr/bin/env python3
"""Markdown to HTML converter for the WebFlux book."""

import os
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARTS_DIR = os.path.join(BASE_DIR, "parts")
CONTENTS_DIR = os.path.join(BASE_DIR, "contents")
CSS_PATH_FROM_ROOT = "css/style.css"
CSS_PATH_FROM_CONTENTS = "../css/style.css"

BOOK_TITLE = "Spring Boot + WebFlux + JPA (MongoDB)"

# Chapter navigation order
NAV_ORDER = [
    ("ch01", "Chapter 1. 리액티브 프로그래밍 소개"),
    ("ch02", "Chapter 2. Spring WebFlux 개요"),
    ("ch03", "Chapter 3. Project Reactor 핵심"),
    ("ch04", "Chapter 4. MongoDB 소개"),
    ("ch05", "Chapter 5. 개발 환경 구성"),
    ("ch06", "Chapter 6. 어노테이션 기반 REST API 구현"),
    ("ch07", "Chapter 7. 함수형 엔드포인트"),
    ("ch08", "Chapter 8. MongoDB 리액티브 데이터 접근 심화"),
    ("ch09", "Chapter 9. 데이터 검증과 예외 처리"),
    ("ch10", "Chapter 10. WebFlux 필터와 인터셉터"),
    ("ch11", "Chapter 11. 리액티브 보안"),
    ("ch12", "Chapter 12. Server-Sent Events (SSE)"),
    ("ch13", "Chapter 13. WebSocket"),
    ("ch14", "Chapter 14. WebClient"),
    ("ch15", "Chapter 15. R2DBC와의 통합"),
    ("ch16", "Chapter 16. 리액티브 테스트 전략"),
    ("ch17", "Chapter 17. 문서화와 API 관리"),
    ("ch18", "Chapter 18. 모니터링과 관측 가능성"),
    ("ch19", "Chapter 19. 성능 최적화"),
    ("ch20", "Chapter 20. 컨테이너화와 배포"),
    ("ch21", "Chapter 21. 실전 프로젝트: 실시간 게시판 서비스"),
    ("appendix_a", "부록 A. Reactor 주요 연산자 레퍼런스"),
    ("appendix_b", "부록 B. MongoDB 쿼리 연산자 정리"),
    ("appendix_c", "부록 C. 자주 발생하는 문제와 해결 방법 (FAQ)"),
    ("appendix_d", "부록 D. 참고 자료 및 추천 학습 경로"),
]

# Part files (separate)
PART_FILES = [
    ("part1", "Part 1. 기초 다지기 (Ch.1-4)"),
    ("part2", "Part 2. 프로젝트 시작하기 (Ch.5-7)"),
    ("part3", "Part 3. 심화 개발 (Ch.8-11)"),
    ("part4", "Part 4. 실시간 통신과 고급 기능 (Ch.12-15)"),
    ("part5", "Part 5. 테스트와 품질 (Ch.16-17)"),
    ("part6", "Part 6. 운영과 배포 (Ch.18-20)"),
    ("part7", "Part 7. 실전 프로젝트 (Ch.21)"),
]

md = markdown.Markdown(
    extensions=[
        TableExtension(),
        FencedCodeExtension(),
        TocExtension(permalink=False),
        "pymdownx.superfences",
    ],
    output_format="html5",
)


def convert_md_to_html(md_text):
    """Convert markdown text to HTML body."""
    md.reset()
    return md.convert(md_text)


def make_page(title, body_html, css_path, nav_html="", is_index=False):
    """Wrap body HTML in a full HTML page."""
    content_class = "index-content" if is_index else "content"
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {BOOK_TITLE}</title>
  <link rel="stylesheet" href="{css_path}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
  <header class="site-header">
    <h1><a href="{"index.html" if is_index else "../index.html"}">{BOOK_TITLE}</a></h1>
  </header>
  {nav_html}
  <div class="wrapper">
    <main class="{content_class}">
      {body_html}
    </main>
    <footer class="site-footer">
      &copy; 2024 Spring Boot + WebFlux + JPA (MongoDB) Book
    </footer>
  </div>
</body>
</html>"""


def make_nav(prev_item, next_item, is_contents=True):
    """Create navigation bar HTML."""
    prefix = "" if not is_contents else ""
    home = "../index.html" if is_contents else "index.html"

    if prev_item:
        prev_link = f'<a href="{prefix}{prev_item[0]}.html">&larr; {prev_item[1]}</a>'
    else:
        prev_link = '<span class="disabled">&larr; 이전</span>'

    if next_item:
        next_link = f'<a href="{prefix}{next_item[0]}.html">{next_item[1]} &rarr;</a>'
    else:
        next_link = '<span class="disabled">다음 &rarr;</span>'

    return f"""  <nav class="nav-bar">
    {prev_link}
    <a href="{home}">목차</a>
    {next_link}
  </nav>"""


def build_index_html():
    """Build the index.html from list.md structure."""
    parts = [
        {
            "title": "Part 1. 기초 다지기",
            "chapters": [
                ("ch01", "Chapter 1", "리액티브 프로그래밍 소개", [
                    "1.1 리액티브 프로그래밍이란?",
                    "1.2 명령형 프로그래밍 vs 리액티브 프로그래밍",
                    "1.3 리액티브 스트림(Reactive Streams) 표준",
                    "1.4 배압(Backpressure)의 개념",
                    "1.5 왜 리액티브가 필요한가?",
                ]),
                ("ch02", "Chapter 2", "Spring WebFlux 개요", [
                    "2.1 Spring MVC와 Spring WebFlux 비교",
                    "2.2 WebFlux의 내부 구조와 Netty",
                    "2.3 논블로킹 I/O의 원리",
                    "2.4 WebFlux를 선택해야 하는 경우와 그렇지 않은 경우",
                    "2.5 WebFlux의 두 가지 프로그래밍 모델",
                ]),
                ("ch03", "Chapter 3", "Project Reactor 핵심", [
                    "3.1 Mono와 Flux 이해하기",
                    "3.2 Reactor의 주요 연산자",
                    "3.3 에러 처리 전략",
                    "3.4 스케줄러와 스레드 모델",
                    "3.5 Cold vs Hot Publisher",
                    "3.6 Reactor 디버깅 기법",
                ]),
                ("ch04", "Chapter 4", "MongoDB 소개", [
                    "4.1 NoSQL과 MongoDB의 특징",
                    "4.2 도큐먼트 모델과 컬렉션",
                    "4.3 MongoDB 설치 및 기본 CRUD",
                    "4.4 인덱싱과 쿼리 최적화 기초",
                    "4.5 MongoDB와 리액티브 드라이버",
                ]),
            ],
        },
        {
            "title": "Part 2. 프로젝트 시작하기",
            "chapters": [
                ("ch05", "Chapter 5", "개발 환경 구성", [
                    "5.1 JDK, IDE, Docker 설치",
                    "5.2 Spring Initializr로 프로젝트 생성",
                    "5.3 주요 의존성 설정",
                    "5.4 application.yml 설정",
                    "5.5 MongoDB Docker 컨테이너 구성",
                    "5.6 프로젝트 구조 설계",
                ]),
                ("ch06", "Chapter 6", "어노테이션 기반 REST API 구현", [
                    "6.1 도메인 모델(Document) 정의",
                    "6.2 ReactiveMongoRepository 활용",
                    "6.3 서비스 계층 구현",
                    "6.4 @RestController로 CRUD API 만들기",
                    "6.5 요청/응답 DTO 설계",
                    "6.6 API 테스트",
                ]),
                ("ch07", "Chapter 7", "함수형 엔드포인트 (Router Functions)", [
                    "7.1 HandlerFunction과 RouterFunction 이해",
                    "7.2 RouterFunction으로 라우팅 정의하기",
                    "7.3 HandlerFunction 구현",
                    "7.4 요청 파라미터 및 바디 처리",
                    "7.5 어노테이션 방식과 함수형 방식 비교",
                ]),
            ],
        },
        {
            "title": "Part 3. 심화 개발",
            "chapters": [
                ("ch08", "Chapter 8", "MongoDB 리액티브 데이터 접근 심화", [
                    "8.1 ReactiveMongoTemplate 활용",
                    "8.2 커스텀 쿼리와 Criteria API",
                    "8.3 Aggregation Pipeline 사용",
                    "8.4 변경 스트림(Change Streams) 활용",
                    "8.5 트랜잭션 처리",
                    "8.6 인덱스 관리와 쿼리 성능 최적화",
                ]),
                ("ch09", "Chapter 9", "데이터 검증과 예외 처리", [
                    "9.1 Bean Validation을 활용한 입력 검증",
                    "9.2 커스텀 Validator 구현",
                    "9.3 글로벌 예외 처리 (@ControllerAdvice)",
                    "9.4 ErrorWebExceptionHandler 활용",
                    "9.5 에러 응답 표준화 (Problem Details)",
                ]),
                ("ch10", "Chapter 10", "WebFlux 필터와 인터셉터", [
                    "10.1 WebFilter 구현",
                    "10.2 HandlerFilterFunction 활용",
                    "10.3 요청/응답 로깅",
                    "10.4 CORS 설정",
                    "10.5 요청 속도 제한(Rate Limiting)",
                ]),
                ("ch11", "Chapter 11", "리액티브 보안 (Spring Security WebFlux)", [
                    "11.1 Spring Security Reactive 설정",
                    "11.2 SecurityWebFilterChain 구성",
                    "11.3 인증과 인가 구현",
                    "11.4 JWT 기반 인증 구현",
                    "11.5 리액티브 환경에서의 SecurityContext 관리",
                    "11.6 OAuth2 / OpenID Connect 연동",
                ]),
            ],
        },
        {
            "title": "Part 4. 실시간 통신과 고급 기능",
            "chapters": [
                ("ch12", "Chapter 12", "Server-Sent Events (SSE)", [
                    "12.1 SSE란 무엇인가?",
                    "12.2 Flux를 활용한 SSE 엔드포인트 구현",
                    "12.3 실시간 알림 시스템 구축",
                    "12.4 MongoDB Change Streams + SSE 연동",
                ]),
                ("ch13", "Chapter 13", "WebSocket", [
                    "13.1 WebSocket 프로토콜 이해",
                    "13.2 WebFlux에서 WebSocket 핸들러 구현",
                    "13.3 실시간 채팅 애플리케이션 구축",
                    "13.4 WebSocket 세션 관리",
                ]),
                ("ch14", "Chapter 14", "WebClient: 리액티브 HTTP 클라이언트", [
                    "14.1 WebClient 설정과 기본 사용법",
                    "14.2 요청/응답 처리",
                    "14.3 에러 핸들링과 재시도 전략",
                    "14.4 타임아웃 설정",
                    "14.5 외부 API 연동 실전 예제",
                    "14.6 WebClient 필터와 인터셉터",
                ]),
                ("ch15", "Chapter 15", "R2DBC와의 통합 (보너스)", [
                    "15.1 R2DBC란?",
                    "15.2 MongoDB + R2DBC 멀티 데이터소스 구성",
                    "15.3 리액티브 환경에서 여러 데이터소스 조합하기",
                ]),
            ],
        },
        {
            "title": "Part 5. 테스트와 품질",
            "chapters": [
                ("ch16", "Chapter 16", "리액티브 테스트 전략", [
                    "16.1 StepVerifier를 활용한 단위 테스트",
                    "16.2 WebTestClient를 활용한 통합 테스트",
                    "16.3 Embedded MongoDB를 활용한 리포지토리 테스트",
                    "16.4 Testcontainers로 MongoDB 테스트 환경 구성",
                    "16.5 MockWebServer를 활용한 외부 API 모킹",
                    "16.6 테스트 슬라이스",
                ]),
                ("ch17", "Chapter 17", "문서화와 API 관리", [
                    "17.1 SpringDoc OpenAPI(Swagger) 연동",
                    "17.2 리액티브 API 문서 자동 생성",
                    "17.3 API 버전 관리 전략",
                ]),
            ],
        },
        {
            "title": "Part 6. 운영과 배포",
            "chapters": [
                ("ch18", "Chapter 18", "모니터링과 관측 가능성", [
                    "18.1 Spring Boot Actuator 설정",
                    "18.2 Micrometer와 Prometheus 연동",
                    "18.3 Grafana 대시보드 구성",
                    "18.4 리액티브 스트림 메트릭 수집",
                    "18.5 분산 추적 (Zipkin / Jaeger)",
                    "18.6 구조화된 로깅 (Logback + MDC)",
                ]),
                ("ch19", "Chapter 19", "성능 최적화", [
                    "19.1 리액티브 애플리케이션 성능 측정",
                    "19.2 MongoDB 커넥션 풀 튜닝",
                    "19.3 Netty 이벤트 루프 최적화",
                    "19.4 캐싱 전략 (Caffeine, Redis)",
                    "19.5 블로킹 코드 탐지 및 제거 (BlockHound)",
                    "19.6 부하 테스트 (Gatling, k6)",
                ]),
                ("ch20", "Chapter 20", "컨테이너화와 배포", [
                    "20.1 Docker 이미지 빌드 (Jib, Buildpacks)",
                    "20.2 Docker Compose로 전체 스택 구성",
                    "20.3 Kubernetes 배포 기초",
                    "20.4 MongoDB Atlas 클라우드 연동",
                    "20.5 CI/CD 파이프라인 구성 (GitHub Actions)",
                    "20.6 GraalVM Native Image 빌드",
                ]),
            ],
        },
        {
            "title": "Part 7. 실전 프로젝트",
            "chapters": [
                ("ch21", "Chapter 21", "실전 프로젝트: 실시간 게시판 서비스", [
                    "21.1 요구사항 분석 및 설계",
                    "21.2 사용자 관리 (회원가입, 로그인, JWT)",
                    "21.3 게시글 CRUD API 구현",
                    "21.4 댓글 시스템",
                    "21.5 실시간 알림 (SSE)",
                    "21.6 페이징과 검색 기능",
                    "21.7 파일 업로드 (GridFS)",
                    "21.8 전체 테스트 작성",
                    "21.9 Docker Compose로 배포",
                ]),
            ],
        },
    ]

    appendices = [
        ("appendix_a", "부록 A", "Reactor 주요 연산자 레퍼런스"),
        ("appendix_b", "부록 B", "MongoDB 쿼리 연산자 정리"),
        ("appendix_c", "부록 C", "자주 발생하는 문제와 해결 방법 (FAQ)"),
        ("appendix_d", "부록 D", "참고 자료 및 추천 학습 경로"),
    ]

    body = f'<h1>{BOOK_TITLE}</h1>\n'

    for part in parts:
        body += f'<div class="part-section">\n'
        body += f'  <div class="part-title">{part["title"]}</div>\n'
        body += f'  <ul class="chapter-list">\n'
        for file_id, ch_num, ch_title, sections in part["chapters"]:
            body += f'    <li>\n'
            body += f'      <a href="contents/{file_id}.html">'
            body += f'<span class="chapter-number">{ch_num.split(".")[0].replace("Chapter ", "Ch.")}</span> '
            body += f'{ch_title}</a>\n'
            body += f'      <ul class="section-items">\n'
            for sec in sections:
                body += f"        <li>{sec}</li>\n"
            body += f"      </ul>\n"
            body += f"    </li>\n"
        body += f"  </ul>\n"
        body += f"</div>\n"

    # Appendices
    body += '<div class="part-section">\n'
    body += '  <div class="part-title">부록</div>\n'
    body += '  <ul class="chapter-list">\n'
    for file_id, label, title in appendices:
        body += f'    <li><a href="contents/{file_id}.html">'
        body += f'<span class="chapter-number">{label.split(".")[0].replace("부록 ", "")}</span> '
        body += f"{title}</a></li>\n"
    body += "  </ul>\n"
    body += "</div>\n"

    # Part merged files
    body += '<div class="part-section">\n'
    body += '  <div class="part-title">파트별 통합본</div>\n'
    body += '  <ul class="chapter-list">\n'
    for file_id, title in PART_FILES:
        body += f'    <li><a href="contents/{file_id}.html">{title}</a></li>\n'
    body += "  </ul>\n"
    body += "</div>\n"

    return make_page("목차", body, CSS_PATH_FROM_ROOT, is_index=True)


def main():
    os.makedirs(CONTENTS_DIR, exist_ok=True)

    # 1. Build index.html
    index_html = build_index_html()
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Created: index.html")

    # 2. Convert chapter/appendix files with navigation
    for i, (file_id, title) in enumerate(NAV_ORDER):
        md_path = os.path.join(PARTS_DIR, f"{file_id}.md")
        if not os.path.exists(md_path):
            print(f"SKIP (not found): {md_path}")
            continue

        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        body_html = convert_md_to_html(md_text)

        prev_item = NAV_ORDER[i - 1] if i > 0 else None
        next_item = NAV_ORDER[i + 1] if i < len(NAV_ORDER) - 1 else None
        nav_html = make_nav(prev_item, next_item, is_contents=True)

        html = make_page(title, body_html, CSS_PATH_FROM_CONTENTS, nav_html)

        out_path = os.path.join(CONTENTS_DIR, f"{file_id}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Created: contents/{file_id}.html")

    # 3. Convert part files (no chapter nav, just home link)
    for i, (file_id, title) in enumerate(PART_FILES):
        md_path = os.path.join(PARTS_DIR, f"{file_id}.md")
        if not os.path.exists(md_path):
            print(f"SKIP (not found): {md_path}")
            continue

        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        body_html = convert_md_to_html(md_text)

        prev_part = PART_FILES[i - 1] if i > 0 else None
        next_part = PART_FILES[i + 1] if i < len(PART_FILES) - 1 else None
        nav_html = make_nav(prev_part, next_part, is_contents=True)

        html = make_page(title, body_html, CSS_PATH_FROM_CONTENTS, nav_html)

        out_path = os.path.join(CONTENTS_DIR, f"{file_id}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Created: contents/{file_id}.html")

    print("\nDone! All files converted.")


if __name__ == "__main__":
    main()
