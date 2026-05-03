"""
CEO 오케스트레이터 — 작업 분석 및 에이전트 분배
사용자 명령을 받아 CEO가 분석하고, 적절한 에이전트에게 작업을 분배합니다.
"""

import json
from typing import AsyncGenerator

from app.models import AgentID, AGENT_META
from app import agents, memory, sync


# ──────────────────────────────────────────
# CEO가 작업을 분석하고 분배
# ──────────────────────────────────────────

CEO_DISTRIBUTION_PROMPT = """당신은 CEO (Chief Executive Agent)입니다. 🧭
사용자의 명령을 분석하고, 어떤 에이전트에게 어떤 작업을 분배할지 결정하세요.

## 사용 가능한 에이전트
- ceo: 오케스트레이션, 작업 분해, 종합 판단
- youtube: 유튜브 채널 운영, 영상 기획, 트렌드 분석
- instagram: 인스타그램 릴스/피드, 캡션, 해시태그
- designer: 브랜드 디자인, 썸네일, 비주얼 시스템
- developer: 코드, 자동화, API 통합, 웹사이트
- editor: 영상 편집, 컷 구성, 콘텐츠 폴리싱
- writer: 카피라이팅, 스크립트, 블로그, 후크
- researcher: 트렌드 리서치, 경쟁사 분석, 데이터 수집
- business: 수익화, 가격 전략, 시장 분석, KPI
- secretary: 일정 관리, 요약, 브리핑, 알림

## 응답 규칙
반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요.

```json
{
  "summary": "사용자 요청에 대한 한 줄 요약",
  "tasks": [
    {"agent_id": "에이전트ID", "task": "구체적인 작업 지시"}
  ]
}
```

## 분배 원칙
1. 작업의 성격에 따라 1~4명의 에이전트에게 분배하세요.
2. 간단한 질문이면 가장 적합한 에이전트 1명에게만 분배하세요.
3. 복잡한 프로젝트는 여러 에이전트에게 분배하되, 각자의 역할에 맞게 구체적인 지시를 내리세요.
4. CEO 자신은 분배 목록에 포함하지 마세요.
"""


async def analyze_and_distribute(user_message: str) -> dict:
    """CEO가 사용자 명령을 분석하여 에이전트에게 분배합니다."""
    import re
    import httpx

    # CEO에게 분배 요청 (컨텍스트는 짧게 — 500 에러 방지)
    system_prompt = CEO_DISTRIBUTION_PROMPT

    payload = {
        "model": agents.get_model(),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"다음 사용자 명령을 분석하고 에이전트에게 분배하세요:\n\n{user_message}"},
        ],
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 1024,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
            resp = await client.post(f"{agents.OLLAMA_URL}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        # Ollama 500 에러 시 기본 분배로 폴백
        print(f"⚠️ Ollama API 에러 ({e.response.status_code}): 기본 분배로 처리합니다.")
        return _fallback_distribute(user_message)
    except Exception as e:
        print(f"⚠️ Ollama 연결 에러: {e}")
        return _fallback_distribute(user_message)

    raw = data.get("message", {}).get("content", "")

    # thinking 태그가 있으면 제거
    raw = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()

    # JSON 파싱
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # JSON 블록 추출 시도
        match = re.search(r'\{[\s\S]*?"tasks"[\s\S]*?\}', raw)
        if match:
            try:
                result = json.loads(match.group())
            except json.JSONDecodeError:
                result = None
        else:
            result = None

        if not result:
            # 파싱 완전 실패 → 키워드 기반 분배
            return _fallback_distribute(user_message)

    # 유효성 검증
    valid_ids = {a.value for a in AgentID}
    validated_tasks = []
    for t in result.get("tasks", []):
        aid = t.get("agent_id", "")
        if aid in valid_ids and aid != "ceo":
            validated_tasks.append(t)

    if not validated_tasks:
        validated_tasks = [{"agent_id": "secretary", "task": user_message}]

    result["tasks"] = validated_tasks
    return result


def _fallback_distribute(user_message: str) -> dict:
    """CEO 분석 실패 시 키워드 기반 자동 분배"""
    msg = user_message.lower()

    tasks = []

    # 키워드 기반 매칭
    keyword_map = {
        "youtube": ["유튜브", "영상", "동영상", "youtube"],
        "instagram": ["인스타", "릴스", "피드", "instagram"],
        "designer": ["디자인", "로고", "썸네일", "UI", "비주얼"],
        "developer": ["코드", "개발", "프로그래밍", "웹사이트", "API", "자동화"],
        "editor": ["편집", "컷", "영상 편집"],
        "writer": ["글", "카피", "블로그", "스크립트", "기획서"],
        "researcher": ["분석", "리서치", "조사", "트렌드", "경쟁사"],
        "business": ["수익", "매출", "가격", "전략", "KPI", "사업"],
        "secretary": ["일정", "정리", "요약", "브리핑", "할 일"],
    }

    for agent_id, keywords in keyword_map.items():
        if any(k in msg for k in keywords):
            tasks.append({"agent_id": agent_id, "task": user_message})

    # 매칭 없으면 secretary
    if not tasks:
        tasks = [{"agent_id": "secretary", "task": user_message}]

    # 최대 3개만
    tasks = tasks[:3]

    return {
        "summary": user_message,
        "tasks": tasks,
    }


# ──────────────────────────────────────────
# 전체 워크플로우 실행 (스트리밍)
# ──────────────────────────────────────────

async def run_workflow(user_message: str, target_agent: str = None) -> AsyncGenerator[str, None]:
    """
    전체 워크플로우:
    1. 특정 에이전트 지정 시 → 바로 해당 에이전트 호출
    2. 미지정 시 → CEO가 분석 → 에이전트 순차 실행 → CEO 종합
    
    SSE 이벤트 형식으로 yield 합니다.
    """
    session_id = memory.create_session_id()

    # ── 특정 에이전트 직접 호출 ──
    if target_agent and target_agent != "ceo":
        meta = AGENT_META.get(AgentID(target_agent), {})
        emoji = meta.get("emoji", "")
        name = meta.get("name", target_agent)

        yield _sse_event("agent_start", {
            "agent_id": target_agent,
            "emoji": emoji,
            "name": name,
            "task": user_message,
        })

        full_response = ""
        async for chunk in agents.call_agent_stream(target_agent, user_message):
            full_response += chunk
            yield _sse_event("agent_chunk", {
                "agent_id": target_agent,
                "content": chunk,
            })

        yield _sse_event("agent_done", {
            "agent_id": target_agent,
            "content": full_response,
        })

        # 세션에 저장
        memory.save_session_output(session_id, target_agent, full_response)
        memory.append_conversation_log(target_agent, emoji, name, full_response)

        yield _sse_event("workflow_done", {"session_id": session_id})

        # GitHub 자동 동기화
        yield _sse_event("syncing", {"message": "🔄 GitHub 동기화 중..."})
        sync_result = sync.sync_after_session(session_id, user_message)
        yield _sse_event("sync_done", sync_result)
        return

    # ── CEO 자동 분배 모드 ──

    # 1. CEO 분석 단계
    yield _sse_event("ceo_analyzing", {"message": "🧭 CEO가 명령을 분석하고 있습니다..."})

    try:
        distribution = await analyze_and_distribute(user_message)
    except Exception as e:
        yield _sse_event("error", {"message": f"CEO 분석 실패: {str(e)}"})
        return

    summary = distribution.get("summary", user_message)
    tasks = distribution.get("tasks", [])

    # 태스크에 메타정보 추가
    enriched_tasks = []
    for t in tasks:
        aid = t["agent_id"]
        meta = AGENT_META.get(AgentID(aid), {})
        enriched_tasks.append({
            **t,
            "emoji": meta.get("emoji", ""),
            "name": meta.get("name", aid),
        })

    yield _sse_event("ceo_distributed", {
        "summary": summary,
        "tasks": enriched_tasks,
    })

    # 세션 브리프 저장
    memory.save_session_brief(session_id, user_message, summary, enriched_tasks)

    # 2. 각 에이전트 순차 실행
    all_outputs = {}

    for t in enriched_tasks:
        aid = t["agent_id"]
        task_desc = t["task"]
        emoji = t["emoji"]
        name = t["name"]

        yield _sse_event("agent_start", {
            "agent_id": aid,
            "emoji": emoji,
            "name": name,
            "task": task_desc,
        })

        full_response = ""
        try:
            async for chunk in agents.call_agent_stream(aid, user_message, task=task_desc):
                full_response += chunk
                yield _sse_event("agent_chunk", {
                    "agent_id": aid,
                    "content": chunk,
                })
        except Exception as e:
            full_response = f"⚠️ 오류 발생: {str(e)}"
            yield _sse_event("agent_chunk", {
                "agent_id": aid,
                "content": full_response,
            })

        yield _sse_event("agent_done", {
            "agent_id": aid,
            "content": full_response,
        })

        all_outputs[aid] = full_response

        # 세션에 산출물 저장
        memory.save_session_output(session_id, aid, full_response)
        memory.append_conversation_log(aid, emoji, name, full_response)

        # 에이전트 메모리에 기록
        memory.append_agent_memory(
            aid,
            f"{user_message[:50]}... → 산출물 sessions/{session_id}/{aid}.md"
        )

    # 3. CEO 종합 보고서
    yield _sse_event("ceo_summarizing", {"message": "🧭 CEO가 종합 보고서를 작성하고 있습니다..."})

    report_prompt = _build_report_prompt(all_outputs, user_message)

    ceo_report = ""
    async for chunk in agents.call_agent_stream("ceo", report_prompt):
        ceo_report += chunk
        yield _sse_event("agent_chunk", {
            "agent_id": "ceo",
            "content": chunk,
        })

    yield _sse_event("agent_done", {
        "agent_id": "ceo",
        "content": ceo_report,
    })

    # 보고서 저장
    memory.save_session_report(session_id, ceo_report)
    memory.append_conversation_log("ceo", "🧭", "CEO", ceo_report)
    memory.append_agent_memory("ceo", f"{user_message[:50]}... → 보고서 sessions/{session_id}/_report.md")

    # 의사결정 로그 업데이트
    _update_decisions(session_id, user_message, ceo_report)

    yield _sse_event("workflow_done", {"session_id": session_id})

    # GitHub 자동 동기화
    yield _sse_event("syncing", {"message": "🔄 GitHub 동기화 중..."})
    sync_result = sync.sync_after_session(session_id, user_message)
    yield _sse_event("sync_done", sync_result)


# ──────────────────────────────────────────
# 헬퍼 함수
# ──────────────────────────────────────────

def _sse_event(event_type: str, data: dict) -> str:
    """SSE 이벤트 포맷 생성"""
    return json.dumps({"event": event_type, "data": data}, ensure_ascii=False)


def _build_report_prompt(outputs: dict, original_message: str) -> str:
    """CEO 종합 보고서 작성용 프롬프트 (간결하게)"""
    sections = []
    for aid, content in outputs.items():
        meta = AGENT_META.get(AgentID(aid), {})
        name = meta.get("name", aid)
        emoji = meta.get("emoji", "")
        # 각 산출물을 800자로 제한하여 토큰 초과 방지
        sections.append(f"### {emoji} {name}:\n{content[:800]}")

    all_outputs_text = "\n\n".join(sections)

    return f"""사용자 명령: "{original_message}"

각 에이전트 산출물을 종합하여 CEO 보고서를 작성하세요.
보고서는 2000자 이내로 작성하세요.

{all_outputs_text}

## 보고서 형식
1. **✅ 완료된 작업** — 요약
2. **🚀 다음 액션 (Top 3)**
3. **💡 인사이트**
"""


def _update_decisions(session_id: str, user_message: str, report: str):
    """의사결정 로그에 세션 결과 추가"""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    # 보고서에서 핵심 결정 추출 (간단히 첫 2줄)
    lines = [l.strip() for l in report.split("\n") if l.strip() and l.strip().startswith("-")][:3]
    decisions_text = "\n".join(lines) if lines else "- 산출물 확인 필요"

    entry = f"\n\n## [{today}] {user_message[:50]}\n{decisions_text}\n_세션: {session_id}_\n"
    memory.append_file(memory.SHARED_DIR / "decisions.md", entry)
