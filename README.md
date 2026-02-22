# Spring Boot WebFlux + MongoDB

리액티브 프로그래밍으로 구현하는 고성능 웹 애플리케이션 — 한국어 기술 서적 프로젝트

## 개요

Spring Boot 기반의 WebFlux와 MongoDB를 활용한 리액티브 웹 애플리케이션 개발을 다루는 기술 서적입니다. Markdown으로 작성된 원고를 HTML(웹) 및 DOCX(출판용) 형식으로 변환하는 빌드 시스템을 포함합니다.

## 목차 구성

| 파트 | 내용 | 챕터 |
|------|------|------|
| Part 1 | 기초 다지기 | Ch.1 리액티브 프로그래밍 소개 ~ Ch.4 MongoDB 소개 |
| Part 2 | 프로젝트 시작하기 | Ch.5 개발 환경 구성 ~ Ch.7 함수형 엔드포인트 |
| Part 3 | 심화 개발 | Ch.8 데이터 접근 심화 ~ Ch.11 리액티브 보안 |
| Part 4 | 실시간 통신과 고급 기능 | Ch.12 SSE ~ Ch.15 R2DBC 통합 |
| Part 5 | 테스트와 품질 | Ch.16 테스트 전략 ~ Ch.17 문서화 |
| Part 6 | 운영과 배포 | Ch.18 모니터링 ~ Ch.20 컨테이너화 |
| Part 7 | 실전 프로젝트 | Ch.21 실시간 게시판 서비스 |
| 부록 | 레퍼런스 | 부록 A~D |

총 21개 챕터 + 4개 부록으로 구성되어 있습니다.

## 프로젝트 구조

```
parts/                # Markdown 원고 (원본 소스)
  ch01.md ~ ch21.md   # 개별 챕터
  part1.md ~ part7.md  # 파트별 병합 파일
  appendix_a~d.md     # 부록
contents/             # 생성된 HTML (직접 편집 금지)
css/style.css         # 공통 스타일시트
convert.py            # Markdown → HTML 변환기
build_docx.py         # Markdown → DOCX(부크크 B5) 변환기
list.md               # 목차 원본
index.html            # 생성된 목차 페이지
books.md              # 전체 병합 파일 (모든 파트 연결)
```

## 빌드 방법

### 사전 요구사항

```bash
pip3 install markdown pymdown-extensions lxml
```

시스템에 `pandoc`이 설치되어 있어야 합니다.

### HTML 빌드 (웹 열람용)

```bash
python3 convert.py
```

`parts/*.md` 파일을 읽어 `contents/*.html` 및 `index.html`을 생성합니다.

### DOCX 빌드 (부크크 출판용)

```bash
python3 build_docx.py
```

`books.md`를 B5(46배판) 부크크 서식의 DOCX로 변환합니다. 빌드 과정은 다음과 같습니다:

1. pandoc 기본 reference.docx 추출
2. 테마 폰트를 부크크 폰트로 변경 (부크크 명조 Light / 부크크 고딕 Light)
3. 스타일 수정 (본문 10pt, 코드 7.5pt, 제목 부크크 고딕)
4. B5 페이지 크기(188×263mm) 및 여백 설정
5. pandoc으로 Markdown → DOCX 변환
6. 테이블 후처리 (테두리, 컬럼 너비, 고정 레이아웃)
7. 앞부분 추가 (속표지, 판권, 목차)

출력 파일: `SpringBoot_WebFlux_MongoDB_B5.docx`

## 콘텐츠 파이프라인

원고를 수정하고 빌드하는 전체 과정입니다.

```bash
# 1. 챕터 수정
#    parts/chXX.md 파일 편집

# 2. 파트 병합
cat parts/ch01.md parts/ch02.md parts/ch03.md parts/ch04.md > parts/part1.md
# ... (각 파트별 반복)

# 3. 전체 병합
cat parts/part1.md parts/part2.md parts/part3.md parts/part4.md \
    parts/part5.md parts/part6.md parts/part7.md \
    parts/appendix_a.md parts/appendix_b.md \
    parts/appendix_c.md parts/appendix_d.md > books.md

# 4. HTML 생성
python3 convert.py

# 5. DOCX 생성
python3 build_docx.py
```

## 새 챕터 추가

1. `parts/chNN.md` 파일 생성
2. `convert.py`의 `NAV_ORDER` 리스트에 항목 추가
3. `convert.py`의 `build_index_html()` 함수에 챕터 정보 추가
4. `list.md` 목차 업데이트
5. 관련 `partN.md` 및 `books.md` 재병합
6. `python3 convert.py` 및 `python3 build_docx.py` 실행

## 작성 규칙

- 한국어로 작성하되, 기술 용어는 영문을 병기: "배압(Backpressure)"
- 각 챕터: 500~800줄
- 코드 블록은 언어 식별자와 함께 fenced 문법 사용: ` ```java `, ` ```yaml `, ` ```bash ` 등
- 설명, Java 코드 예제, 비교 표, 팁/주의 인용문 포함

## 라이선스

이 프로젝트의 콘텐츠는 저작권으로 보호됩니다. 무단 복제 및 배포를 금합니다.
