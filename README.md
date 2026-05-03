# 🏢 미드미 — 1인 기업 OS

10명의 AI 에이전트가 당신의 사업을 도와드립니다.

## 🚀 설치 방법

### 사전 준비
1. **Python 3.10+** — [brew install python@3.12](https://brew.sh)
2. **Ollama** — [ollama.com](https://ollama.com) 에서 설치
3. **LLM 모델** — 터미널에서 `ollama pull gemma3` 실행

### 원클릭 설치
```
📂 설치.command 더블클릭
```
가상환경 생성, 패키지 설치, 디렉토리 확인을 자동으로 합니다.

## ▶️ 실행 방법

```
📂 실행.command 더블클릭
```
서버가 시작되고 브라우저가 자동으로 열립니다.

또는 터미널에서:
```bash
./실행.command
```

## 📁 프로젝트 구조

```
에이전트/
├── 설치.command          # 원클릭 설치
├── 실행.command          # 원클릭 실행
├── requirements.txt     # Python 의존성
├── app/                 # 서버 코드
│   ├── main.py         # FastAPI 메인
│   ├── agents.py       # Ollama 에이전트 엔진
│   ├── orchestrator.py # CEO 오케스트레이터
│   ├── autopilot.py    # 24시간 자율 업무
│   ├── web_search.py   # 웹 검색 모듈
│   ├── memory.py       # 메모리 매니저
│   ├── sync.py         # GitHub 동기화
│   ├── models.py       # 데이터 모델
│   └── static/         # 프론트엔드 UI
├── _shared/             # 공유 메모리
├── _agents/             # 에이전트 개인 메모리
├── sessions/            # 작업 산출물
└── 00_Raw/              # 원시 대화 로그
```

## 🤖 에이전트 목록

| 에이전트 | 역할 |
|:---|:---|
| 🧭 CEO | 작업 분석, 분배, 종합 보고 |
| 🎬 YouTube | 유튜브 채널 운영, 영상 기획 |
| 📸 Instagram | 인스타그램 콘텐츠 전략 |
| 🎨 Designer | 브랜드 디자인, 비주얼 |
| 💻 Developer | 코드, 자동화, 웹사이트 |
| 🎞 Editor | 영상 편집, 컷 구성 |
| ✍️ Writer | 카피라이팅, 스크립트 |
| 🔍 Researcher | 트렌드 리서치, 데이터 |
| 💰 Business | 수익화, 가격 전략 |
| 📋 Secretary | 일정 관리, 요약 |

## ✨ 주요 기능

- **CEO 자동 분배**: 명령을 분석하여 적합한 에이전트에게 자동 할당
- **24시간 자율 업무**: 토글 ON으로 에이전트가 자동으로 작업 수행
- **웹 검색**: "최신", "트렌드" 등 키워드 감지 시 자동 인터넷 검색
- **GitHub 동기화**: 작업 결과물을 자동으로 커밋 & 푸시
- **LLM 모델 선택**: Ollama에 설치된 모델 자유롭게 전환
- **세션 관리**: 모든 작업이 날짜별 마크다운으로 저장

## 📌 참고사항

- 서버 기본 포트: `8000`
- Ollama 기본 포트: `11434`
- 종료: 터미널에서 `Control+C`
