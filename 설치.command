#!/bin/bash
# ──────────────────────────────────────────
# 미드미 1인 기업 OS — 설치 스크립트
# 더블클릭으로 모든 의존성을 자동 설치합니다.
# ──────────────────────────────────────────

cd "$(dirname "$0")"
clear

echo "╔════════════════════════════════════════╗"
echo "║   🏢 미드미 1인 기업 OS — 설치        ║"
echo "╚════════════════════════════════════════╝"
echo ""

# ── 1. Python 확인 ──
echo "🔍 Python 확인 중..."
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
    echo ""
    echo "   아래 명령어로 설치해주세요:"
    echo "   brew install python@3.12"
    echo ""
    read -p "아무 키나 누르세요..."
    exit 1
fi
echo "   ✅ $($PYTHON --version)"
echo ""

# ── 2. 가상환경 생성 ──
echo "📦 가상환경 설정 중..."
if [ ! -d ".venv" ]; then
    $PYTHON -m venv .venv
    echo "   ✅ 가상환경 생성 완료"
else
    echo "   ✅ 가상환경 이미 존재"
fi

# 활성화
source .venv/bin/activate
echo ""

# ── 3. 패키지 설치 ──
echo "📦 패키지 설치 중..."
pip install --upgrade pip -q 2>/dev/null
pip install -r requirements.txt -q 2>&1 | tail -3

echo "   ✅ 패키지 설치 완료"
echo ""

# ── 4. Ollama 확인 ──
echo "🤖 Ollama 확인 중..."
if command -v ollama &> /dev/null; then
    echo "   ✅ Ollama 설치됨"
    
    # 모델 확인
    MODEL_COUNT=$(ollama list 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
    if [ "$MODEL_COUNT" -gt "0" ]; then
        echo "   ✅ 설치된 모델: ${MODEL_COUNT}개"
        ollama list 2>/dev/null | tail -n +2 | while read line; do
            echo "      🧠 $line"
        done
    else
        echo "   ⚠️  설치된 모델이 없습니다."
        echo "      ollama pull gemma3 으로 모델을 설치해주세요."
    fi
else
    echo "   ⚠️  Ollama가 설치되어 있지 않습니다."
    echo "      https://ollama.com 에서 설치해주세요."
fi
echo ""

# ── 5. Git 확인 ──
echo "🔗 Git 확인 중..."
if [ -d ".git" ]; then
    REMOTE=$(git remote get-url origin 2>/dev/null)
    echo "   ✅ Git 연결됨: $REMOTE"
else
    echo "   ℹ️  Git 저장소가 아닙니다."
fi
echo ""

# ── 6. 디렉토리 확인 ──
echo "📁 디렉토리 확인 중..."
mkdir -p sessions
mkdir -p _shared
mkdir -p _agents
mkdir -p 00_Raw/conversations
echo "   ✅ 필수 디렉토리 확인 완료"
echo ""

# ── 7. 실행 스크립트 권한 설정 ──
chmod +x 실행.command 2>/dev/null
chmod +x 설치.command 2>/dev/null
echo "   ✅ 실행 스크립트 권한 설정 완료"
echo ""

# ── 완료 ──
echo "╔════════════════════════════════════════╗"
echo "║   ✅ 설치 완료!                        ║"
echo "║                                        ║"
echo "║   실행 방법:                            ║"
echo "║   📂 실행.command 를 더블클릭하세요     ║"
echo "║                                        ║"
echo "║   또는 터미널에서:                      ║"
echo "║   ./실행.command                        ║"
echo "╚════════════════════════════════════════╝"
echo ""
read -p "아무 키나 눌러서 종료..."
