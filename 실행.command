#!/bin/bash
# ──────────────────────────────────────────
# 미드미 1인 기업 OS — 원클릭 실행
# 더블클릭으로 서버를 시작하고 브라우저를 엽니다.
# ──────────────────────────────────────────

cd "$(dirname "$0")"
clear

echo "╔════════════════════════════════════════╗"
echo "║   🏢 미드미 1인 기업 OS               ║"
echo "╚════════════════════════════════════════╝"
echo ""

# ── 1. Python 확인 ──
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
    echo "   먼저 설치.command 를 실행해주세요."
    read -p "아무 키나 누르세요..."
    exit 1
fi

echo "✅ Python: $($PYTHON --version)"

# ── 2. 가상환경 확인 ──
if [ ! -d ".venv" ]; then
    echo "📦 가상환경이 없습니다. 자동 생성합니다..."
    $PYTHON -m venv .venv
fi

source .venv/bin/activate

# ── 3. 의존성 자동 설치/업데이트 ──
if [ ! -f ".venv/.installed" ] || [ "requirements.txt" -nt ".venv/.installed" ]; then
    echo "📦 패키지 설치/업데이트 중..."
    pip install -q -r requirements.txt 2>/dev/null
    touch .venv/.installed
    echo "✅ 패키지 준비 완료"
fi

# ── 4. Ollama 확인 및 시작 ──
if command -v ollama &> /dev/null; then
    echo "✅ Ollama 확인됨"
    
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "🔄 Ollama 서버 시작 중..."
        ollama serve &> /dev/null &
        sleep 3
    fi
    echo "✅ Ollama 서버 실행 중"
else
    echo "⚠️  Ollama 미설치 — https://ollama.com 에서 설치하세요"
fi

# ── 5. 서버 시작 ──
echo ""
echo "🚀 서버 시작: http://localhost:8000"
echo "   종료하려면 Control+C"
echo ""

# 2초 후 브라우저 자동 오픈
(sleep 2 && open "http://localhost:8000") &

# uvicorn 실행
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
