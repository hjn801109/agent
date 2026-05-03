#!/bin/bash
# ──────────────────────────────────────────
# 미드미 1인 기업 OS — 원클릭 실행
# 더블클릭으로 서버를 시작하고 브라우저를 엽니다.
# ──────────────────────────────────────────

cd "$(dirname "$0")"

echo "🏢 미드미 1인 기업 OS 시작..."
echo ""

# ── 1. Python 확인 (3.12 우선) ──
PYTHON=""
if [ -f "/opt/homebrew/bin/python3.12" ]; then
    PYTHON="/opt/homebrew/bin/python3.12"
elif command -v python3.12 &> /dev/null; then
    PYTHON="python3.12"
elif command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "❌ Python이 설치되어 있지 않습니다."
    echo "   brew install python@3.12 으로 설치해주세요."
    read -p "아무 키나 누르세요..."
    exit 1
fi

echo "✅ Python: $($PYTHON --version)"

# ── 2. 가상환경 생성 (최초 1회) ──
if [ ! -d ".venv" ]; then
    echo "📦 가상환경 생성 중..."
    $PYTHON -m venv .venv
fi

# ── 3. 가상환경 활성화 ──
source .venv/bin/activate

# ── 4. 의존성 설치 (최초 1회 또는 업데이트) ──
if [ ! -f ".venv/.installed" ] || [ "app/requirements.txt" -nt ".venv/.installed" ]; then
    echo "📦 패키지 설치 중..."
    pip install -q -r app/requirements.txt
    touch .venv/.installed
    echo "✅ 패키지 설치 완료"
fi

# ── 5. Ollama 확인 ──
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama가 설치되어 있지 않습니다."
    echo "   https://ollama.com 에서 설치해주세요."
else
    echo "✅ Ollama: $(ollama --version 2>/dev/null || echo 'OK')"
    
    # Ollama 서버 실행 확인
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "🔄 Ollama 서버 시작 중..."
        ollama serve &> /dev/null &
        sleep 2
    fi
    echo "✅ Ollama 서버 실행 중"
fi

# ── 6. 서버 시작 ──
echo ""
echo "🚀 서버 시작: http://localhost:8000"
echo "   종료하려면 Control+C"
echo ""

# 2초 후 브라우저 자동 오픈
(sleep 2 && open "http://localhost:8000") &

# uvicorn 실행
$PYTHON -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
