"""
메모리 매니저 — 마크다운 파일 읽기/쓰기
기존 에이전트 폴더 구조를 그대로 활용합니다.
"""

import os
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 (app/ 의 상위 디렉토리 = 에이전트/)
BASE_DIR = Path(__file__).resolve().parent.parent
SHARED_DIR = BASE_DIR / "_shared"
AGENTS_DIR = BASE_DIR / "_agents"
SESSIONS_DIR = BASE_DIR / "sessions"
RAW_DIR = BASE_DIR / "00_Raw" / "conversations"


def read_file(path: Path) -> str:
    """파일 내용을 읽어서 반환. 없으면 빈 문자열."""
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def write_file(path: Path, content: str):
    """파일에 내용 쓰기. 디렉토리 자동 생성."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_file(path: Path, content: str):
    """파일 끝에 내용 추가."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


# ──────────────────────────────────────────
# 공유 메모리 읽기
# ──────────────────────────────────────────

def get_system() -> str:
    return read_file(SHARED_DIR / "_system.md")

def get_identity() -> str:
    return read_file(SHARED_DIR / "identity.md")

def get_goals() -> str:
    return read_file(SHARED_DIR / "goals.md")

def get_decisions() -> str:
    return read_file(SHARED_DIR / "decisions.md")

def update_shared_file(filename: str, content: str):
    """공유 메모리 파일 업데이트 (identity.md, goals.md, decisions.md)"""
    allowed = {"identity.md", "goals.md", "decisions.md"}
    if filename not in allowed:
        raise ValueError(f"수정 불가: {filename}")
    write_file(SHARED_DIR / filename, content)


# ──────────────────────────────────────────
# 에이전트 개인 메모리 읽기/쓰기
# ──────────────────────────────────────────

def get_agent_prompt(agent_id: str) -> str:
    return read_file(AGENTS_DIR / agent_id / "prompt.md")

def get_agent_goal(agent_id: str) -> str:
    return read_file(AGENTS_DIR / agent_id / "goal.md")

def get_agent_memory(agent_id: str) -> str:
    return read_file(AGENTS_DIR / agent_id / "memory.md")

def update_agent_prompt(agent_id: str, content: str):
    write_file(AGENTS_DIR / agent_id / "prompt.md", content)

def update_agent_goal(agent_id: str, content: str):
    write_file(AGENTS_DIR / agent_id / "goal.md", content)

def append_agent_memory(agent_id: str, entry: str):
    """에이전트 메모리에 학습 기록 추가"""
    today = datetime.now().strftime("%Y-%m-%d")
    append_file(
        AGENTS_DIR / agent_id / "memory.md",
        f"\n- [{today}] {entry}"
    )


# ──────────────────────────────────────────
# 에이전트 전체 컨텍스트 조합
# ──────────────────────────────────────────

def build_agent_context(agent_id: str) -> str:
    """에이전트 호출 시 시스템 프롬프트에 주입할 전체 컨텍스트를 조합합니다.
    메모리 위계: decisions > identity > goals > 개인 메모리 > 지식 베이스
    """
    parts = []

    # 1. 공유 시스템
    system = get_system()
    if system:
        parts.append(f"# 시스템 매뉴얼\n{system}")

    # 2. 회사 정체성
    identity = get_identity()
    if identity:
        parts.append(identity)

    # 3. 공동 목표
    goals = get_goals()
    if goals:
        parts.append(goals)

    # 4. 의사결정 로그 (최우선)
    decisions = get_decisions()
    if decisions:
        parts.append(decisions)

    # 5. 개인 페르소나
    prompt = get_agent_prompt(agent_id)
    if prompt:
        parts.append(f"# 나의 페르소나 디테일\n{prompt}")

    # 6. 개인 목표
    goal = get_agent_goal(agent_id)
    if goal:
        parts.append(goal)

    # 7. 개인 메모리
    memory = get_agent_memory(agent_id)
    if memory:
        parts.append(f"# 나의 학습 기록\n{memory}")

    return "\n\n---\n\n".join(parts)


# ──────────────────────────────────────────
# 세션 관리
# ──────────────────────────────────────────

def create_session_id() -> str:
    """새 세션 ID 생성 (타임스탬프 기반)"""
    return datetime.now().strftime("%Y-%m-%dT%H-%M")


def save_session_brief(session_id: str, user_message: str, summary: str, tasks: list):
    """세션 브리프 저장"""
    session_dir = SESSIONS_DIR / session_id
    task_lines = "\n".join(
        [f"- **{t['emoji']} {t['name']}**: {t['task']}" for t in tasks]
    )
    content = f"""# 📋 작업 브리프

**원 명령:** {user_message}

## 요약
{summary}

## 분배
{task_lines}
"""
    write_file(session_dir / "_brief.md", content)


def save_session_output(session_id: str, agent_id: str, content: str):
    """에이전트 산출물을 세션에 저장"""
    session_dir = SESSIONS_DIR / session_id
    write_file(session_dir / f"{agent_id}.md", content)


def save_session_report(session_id: str, content: str):
    """CEO 종합 보고서 저장"""
    session_dir = SESSIONS_DIR / session_id
    write_file(session_dir / "_report.md", content)


def append_conversation_log(agent_id: str, emoji: str, name: str, content: str):
    """대화록에 기록 추가"""
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")
    log_file = RAW_DIR / f"{today}.md"

    if not log_file.exists():
        write_file(log_file, f"# 📜 {today} 회사 대화록\n\n_모든 명령·분배·산출물·대화가 시간순으로 누적됩니다._\n\n")

    # 내용이 너무 길면 요약만 기록
    preview = content[:200] + "..." if len(content) > 200 else content
    append_file(
        log_file,
        f"\n## [{now}] {emoji} **{name}** · _{preview}_\n\n{content}\n"
    )


def list_sessions() -> list[dict]:
    """세션 목록을 최신순으로 반환"""
    sessions = []
    if not SESSIONS_DIR.exists():
        return sessions

    for d in sorted(SESSIONS_DIR.iterdir(), reverse=True):
        if d.is_dir() and not d.name.startswith("."):
            brief = read_file(d / "_brief.md")
            # 원 명령 추출
            command = ""
            for line in brief.split("\n"):
                if line.startswith("**원 명령:**"):
                    command = line.replace("**원 명령:**", "").strip()
                    break
            sessions.append({
                "id": d.name,
                "command": command,
                "has_report": (d / "_report.md").exists(),
                "files": [f.name for f in d.iterdir() if f.is_file()],
            })

    return sessions


def get_session_detail(session_id: str) -> dict:
    """세션 상세 정보"""
    session_dir = SESSIONS_DIR / session_id
    if not session_dir.exists():
        return {}

    files = {}
    for f in sorted(session_dir.iterdir()):
        if f.is_file():
            files[f.stem] = read_file(f)

    return {"id": session_id, "files": files}
