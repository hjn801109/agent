"""
에이전트 엔진 — Ollama API 연동
각 에이전트의 시스템 프롬프트를 조합하고 Ollama에 요청합니다.
"""

import json
import httpx
from typing import AsyncGenerator

from app.models import AgentID, AGENT_META
from app import memory

# ──────────────────────────────────────────
# 설정
# ──────────────────────────────────────────

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "gemma4-long"

_current_model = DEFAULT_MODEL


def get_model() -> str:
    return _current_model

def set_model(model: str):
    global _current_model
    _current_model = model


async def list_ollama_models() -> list[str]:
    """Ollama에 설치된 모델 목록 조회"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            resp.raise_for_status()
            data = resp.json()
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


async def check_ollama_status() -> bool:
    """Ollama 서버 실행 여부 확인"""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False


# ──────────────────────────────────────────
# 에이전트 시스템 프롬프트 생성
# ──────────────────────────────────────────

def build_system_prompt(agent_id: str, task: str = "") -> str:
    """에이전트의 전체 시스템 프롬프트를 생성합니다."""
    meta = AGENT_META.get(AgentID(agent_id), {})
    emoji = meta.get("emoji", "")
    name = meta.get("name", agent_id)
    title = meta.get("title", "")

    # 기존 메모리에서 컨텍스트 로드 (최대 2000자로 제한 — Ollama 토큰 초과 방지)
    context = memory.build_agent_context(agent_id)
    if len(context) > 2000:
        context = context[:2000] + "\n...(생략)..."

    system_prompt = f"""당신은 '{name}' ({title}) 에이전트입니다. {emoji}
당신은 '미드미' 1인 기업의 {title} 역할을 맡고 있습니다.

## 행동 규칙
1. 항상 한국어로 응답하세요.
2. "정리"보다 "다음 액션 1개"를 명시하는 것이 우선입니다.
3. 추상적인 조언 대신 실행 가능한 산출물을 만드세요.
4. 응답 마지막에 📊 평가와 📝 다음 단계를 반드시 포함하세요.
5. 마크다운 형식으로 깔끔하게 작성하세요.
6. 응답은 3000자 이내로 작성하세요.

## 회사 컨텍스트
{context}
"""

    if task:
        system_prompt += f"\n\n## 현재 할당된 작업\n{task}"

    return system_prompt


# ──────────────────────────────────────────
# Ollama 호출 (스트리밍)
# ──────────────────────────────────────────

async def call_agent_stream(
    agent_id: str,
    user_message: str,
    task: str = "",
) -> AsyncGenerator[str, None]:
    """에이전트에게 메시지를 보내고 스트리밍으로 응답을 받습니다."""

    system_prompt = build_system_prompt(agent_id, task)

    payload = {
        "model": _current_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": True,
        "options": {
            "temperature": 0.7,
            "num_predict": 4096,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=10.0)) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_URL}/api/chat",
                json=payload,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        # gemma4 thinking 태그 필터링
                        content = data.get("message", {}).get("content", "")
                        if content:
                            yield content
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
    except httpx.HTTPStatusError as e:
        yield f"\n\n⚠️ Ollama API 에러 ({e.response.status_code}). 모델을 확인해주세요."
    except httpx.TimeoutException:
        yield "\n\n⚠️ 응답 시간 초과. 더 작은 모델을 사용해보세요."
    except Exception as e:
        yield f"\n\n⚠️ 연결 오류: {str(e)[:100]}"


async def call_agent_full(
    agent_id: str,
    user_message: str,
    task: str = "",
) -> str:
    """에이전트에게 메시지를 보내고 전체 응답을 받습니다 (비스트리밍)."""

    system_prompt = build_system_prompt(agent_id, task)

    payload = {
        "model": _current_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 4096,
        },
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=10.0)) as client:
        resp = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("message", {}).get("content", "")
