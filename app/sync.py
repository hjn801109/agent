"""
Git 동기화 모듈 — GitHub와 로컬 자동 동기화
세션 완료 후 자동으로 commit + push, 시작 시 pull
"""

import subprocess
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent


def _run_git(*args, cwd=None) -> tuple[bool, str]:
    """git 명령 실행"""
    try:
        result = subprocess.run(
            ["git"] + list(args),
            cwd=str(cwd or BASE_DIR),
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Git 명령 시간 초과 (30초)"
    except FileNotFoundError:
        return False, "Git이 설치되어 있지 않습니다."
    except Exception as e:
        return False, str(e)


def check_git_status() -> dict:
    """Git 상태 확인"""
    # repo 확인
    ok, _ = _run_git("status", "--porcelain")
    if not ok:
        return {"initialized": False, "remote": None, "branch": None}

    # remote 확인
    _, remote = _run_git("remote", "get-url", "origin")

    # branch 확인
    _, branch = _run_git("rev-parse", "--abbrev-ref", "HEAD")

    # 변경 파일 수
    _, status = _run_git("status", "--porcelain")
    changed = len([l for l in status.split("\n") if l.strip()]) if status else 0

    return {
        "initialized": True,
        "remote": remote if remote else None,
        "branch": branch if branch else "main",
        "changed_files": changed,
    }


def pull() -> dict:
    """GitHub에서 최신 변경사항 가져오기 (pull)"""
    ok, output = _run_git("pull", "origin", "main", "--no-edit")
    return {
        "success": ok,
        "message": output,
        "timestamp": datetime.now().isoformat(),
    }


def sync_after_session(session_id: str, message: str = "") -> dict:
    """세션 완료 후 자동 동기화 (add + commit + push)
    
    Args:
        session_id: 세션 ID (커밋 메시지에 포함)
        message: 원래 사용자 명령 (커밋 메시지에 포함)
    """
    results = []

    # 1. 모든 변경 파일 스테이징
    ok, out = _run_git("add", "-A")
    results.append(f"add: {'✅' if ok else '❌'} {out}")

    if not ok:
        return {"success": False, "steps": results, "timestamp": datetime.now().isoformat()}

    # 2. 변경사항 확인
    _, status = _run_git("diff", "--cached", "--stat")
    if not status:
        return {"success": True, "steps": ["변경사항 없음"], "timestamp": datetime.now().isoformat()}

    # 3. 커밋
    commit_msg = f"[{session_id}] {message[:80]}" if message else f"세션 {session_id} 자동 동기화"
    ok, out = _run_git("commit", "-m", commit_msg)
    results.append(f"commit: {'✅' if ok else '❌'} {out[:200]}")

    if not ok:
        return {"success": False, "steps": results, "timestamp": datetime.now().isoformat()}

    # 4. 푸시
    ok, out = _run_git("push", "origin", "main")
    results.append(f"push: {'✅' if ok else '❌'} {out[:200]}")

    return {
        "success": ok,
        "steps": results,
        "timestamp": datetime.now().isoformat(),
    }


def full_sync(message: str = "수동 동기화") -> dict:
    """전체 동기화: pull → add → commit → push"""
    results = []

    # 1. Pull
    pull_result = pull()
    results.append(f"pull: {'✅' if pull_result['success'] else '❌'} {pull_result['message'][:200]}")

    # 2. Add + Commit + Push
    ok, out = _run_git("add", "-A")
    results.append(f"add: {'✅' if ok else '❌'}")

    _, status = _run_git("diff", "--cached", "--stat")
    if status:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        ok, out = _run_git("commit", "-m", f"[{now}] {message}")
        results.append(f"commit: {'✅' if ok else '❌'} {out[:200]}")

        if ok:
            ok, out = _run_git("push", "origin", "main")
            results.append(f"push: {'✅' if ok else '❌'} {out[:200]}")
    else:
        results.append("변경사항 없음 — push 생략")

    return {
        "success": True,
        "steps": results,
        "timestamp": datetime.now().isoformat(),
    }
