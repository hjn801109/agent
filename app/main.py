"""
FastAPI 메인 서버 — 미드미 1인 기업 OS
"""

import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.models import (
    AgentID, AGENT_META, ChatRequest,
    MemoryUpdateRequest, PromptUpdateRequest,
    SettingsUpdateRequest,
)
from app import memory, agents, orchestrator, sync

# ──────────────────────────────────────────
# 앱 초기화
# ──────────────────────────────────────────

app = FastAPI(title="미드미 1인 기업 OS", version="1.0.0")

STATIC_DIR = Path(__file__).parent / "static"


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 GitHub에서 최신 변경사항 가져오기"""
    result = sync.pull()
    if result["success"]:
        print("✅ GitHub 동기화 완료 (pull)")
    else:
        print(f"⚠️ GitHub pull 실패: {result['message']}")


# ──────────────────────────────────────────
# API: 채팅 (SSE 스트리밍)
# ──────────────────────────────────────────

@app.post("/api/chat")
async def chat(req: ChatRequest):
    """사용자 메시지를 처리하고 SSE 스트리밍으로 응답"""

    async def event_stream():
        async for event_data in orchestrator.run_workflow(
            user_message=req.message,
            target_agent=req.target_agent.value if req.target_agent else None,
        ):
            yield f"data: {event_data}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ──────────────────────────────────────────
# API: 에이전트
# ──────────────────────────────────────────

@app.get("/api/agents")
async def list_agents():
    """전체 에이전트 목록"""
    result = []
    for agent_id in AgentID:
        meta = AGENT_META[agent_id]
        result.append({
            "id": agent_id.value,
            "emoji": meta["emoji"],
            "name": meta["name"],
            "title": meta["title"],
            "color": meta["color"],
            "has_goal": bool(memory.get_agent_goal(agent_id.value).strip()),
            "has_memory": bool(memory.get_agent_memory(agent_id.value).strip()),
        })
    return result


@app.get("/api/agents/{agent_id}")
async def get_agent_detail(agent_id: str):
    """특정 에이전트 상세"""
    try:
        aid = AgentID(agent_id)
    except ValueError:
        return JSONResponse({"error": "잘못된 에이전트 ID"}, status_code=404)

    meta = AGENT_META[aid]
    return {
        "id": agent_id,
        **meta,
        "prompt": memory.get_agent_prompt(agent_id),
        "goal": memory.get_agent_goal(agent_id),
        "memory": memory.get_agent_memory(agent_id),
    }


@app.put("/api/agents/{agent_id}/prompt")
async def update_agent_prompt(agent_id: str, req: PromptUpdateRequest):
    """에이전트 페르소나 수정"""
    try:
        AgentID(agent_id)
    except ValueError:
        return JSONResponse({"error": "잘못된 에이전트 ID"}, status_code=404)
    memory.update_agent_prompt(agent_id, req.content)
    return {"status": "ok"}


@app.put("/api/agents/{agent_id}/goal")
async def update_agent_goal(agent_id: str, req: PromptUpdateRequest):
    """에이전트 목표 수정"""
    try:
        AgentID(agent_id)
    except ValueError:
        return JSONResponse({"error": "잘못된 에이전트 ID"}, status_code=404)
    memory.update_agent_goal(agent_id, req.content)
    return {"status": "ok"}


# ──────────────────────────────────────────
# API: 공유 메모리
# ──────────────────────────────────────────

@app.get("/api/memory/shared")
async def get_shared_memory():
    """공유 메모리 전체 조회"""
    return {
        "identity": memory.get_identity(),
        "goals": memory.get_goals(),
        "decisions": memory.get_decisions(),
    }


@app.put("/api/memory/shared/{filename}")
async def update_shared_memory(filename: str, req: MemoryUpdateRequest):
    """공유 메모리 파일 수정"""
    try:
        memory.update_shared_file(filename, req.content)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    return {"status": "ok"}


# ──────────────────────────────────────────
# API: 세션
# ──────────────────────────────────────────

@app.get("/api/sessions")
async def list_sessions():
    """세션 목록"""
    return memory.list_sessions()


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """세션 상세"""
    detail = memory.get_session_detail(session_id)
    if not detail:
        return JSONResponse({"error": "세션 없음"}, status_code=404)
    return detail


# ──────────────────────────────────────────
# API: 설정
# ──────────────────────────────────────────

@app.get("/api/settings")
async def get_settings():
    """현재 설정 조회"""
    models = await agents.list_ollama_models()
    status = await agents.check_ollama_status()
    git_status = sync.check_git_status()
    return {
        "ollama_url": agents.OLLAMA_URL,
        "model": agents.get_model(),
        "available_models": models,
        "ollama_status": status,
        "git": git_status,
    }


@app.put("/api/settings")
async def update_settings(req: SettingsUpdateRequest):
    """설정 변경"""
    if req.model:
        agents.set_model(req.model)
    return {"status": "ok", "model": agents.get_model()}


# ──────────────────────────────────────────
# API: Git 동기화
# ──────────────────────────────────────────

@app.get("/api/sync/status")
async def git_status():
    """Git 동기화 상태"""
    return sync.check_git_status()


@app.post("/api/sync/pull")
async def git_pull():
    """GitHub에서 최신 변경사항 가져오기"""
    return sync.pull()


@app.post("/api/sync/push")
async def git_push():
    """로컬 변경사항을 GitHub에 푸시"""
    return sync.full_sync("수동 동기화")


@app.post("/api/sync/full")
async def git_full_sync():
    """전체 동기화 (pull + commit + push)"""
    return sync.full_sync("전체 동기화")


# ──────────────────────────────────────────
# 정적 파일 서빙 + SPA 라우팅
# ──────────────────────────────────────────

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def serve_index():
    """메인 페이지"""
    index_file = STATIC_DIR / "index.html"
    return HTMLResponse(index_file.read_text(encoding="utf-8"))

