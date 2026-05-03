"""
자율 업무 모드 (AutoPilot) — 24시간 자동 작업 스케줄러
CEO가 회사 목표를 읽고 다음 작업을 자동 생성하여 에이전트에게 분배합니다.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional

from app import memory, agents, sync
from app.models import AgentID, AGENT_META


# ──────────────────────────────────────────
# AutoPilot 프롬프트
# ──────────────────────────────────────────

AUTOPILOT_PROMPT = """당신은 CEO (Chief Executive Agent)입니다. 🧭
24시간 자율 업무 모드가 활성화되어 있습니다.

## 회사 목표
{goals}

## 최근 의사결정
{decisions}

## 지시
위 회사 목표를 달성하기 위해 **지금 당장 실행할 수 있는 가장 중요한 작업 1가지**를 생성하세요.
이미 완료된 작업은 반복하지 마세요.

반드시 한국어로, 아래 형식의 **1줄 명령문**으로만 응답하세요:
예) "유튜브 첫 영상 기획서를 만들어줘"
예) "인스타그램 브랜드 소개 피드 3개를 기획해줘"
예) "이번 주 콘텐츠 캘린더를 만들어줘"

다른 설명 없이 명령문 1줄만 응답하세요.
"""


class AutoPilot:
    """24시간 자율 업무 스케줄러"""

    def __init__(self):
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._interval_minutes = 60
        self._max_cycles = 24  # 안전장치: 최대 24회 (24시간)
        self._completed_cycles = 0
        self._next_run: Optional[datetime] = None
        self._current_status = "off"  # off, waiting, working
        self._last_command = ""
        self._log: list[dict] = []

    @property
    def status(self) -> dict:
        return {
            "running": self._running,
            "status": self._current_status,
            "interval_minutes": self._interval_minutes,
            "completed_cycles": self._completed_cycles,
            "max_cycles": self._max_cycles,
            "next_run": self._next_run.isoformat() if self._next_run else None,
            "last_command": self._last_command,
            "log": self._log[-10:],  # 최근 10개만
        }

    def start(self, interval_minutes: int = 60):
        """자율 업무 시작"""
        if self._running:
            return {"success": False, "message": "이미 실행 중입니다."}

        self._interval_minutes = max(5, min(interval_minutes, 120))  # 5분~2시간
        self._completed_cycles = 0
        self._running = True
        self._log = []
        self._task = asyncio.create_task(self._run_loop())

        return {
            "success": True,
            "message": f"🌞 24시간 업무 시작! ({self._interval_minutes}분 간격)",
        }

    def stop(self):
        """자율 업무 중단"""
        self._running = False
        self._current_status = "off"
        self._next_run = None
        if self._task and not self._task.done():
            self._task.cancel()

        return {
            "success": True,
            "message": f"🌙 자율 업무 중단. 총 {self._completed_cycles}개 작업 완료.",
            "completed_cycles": self._completed_cycles,
        }

    async def _run_loop(self):
        """메인 루프: 작업 생성 → 실행 → 대기 → 반복"""
        try:
            # 첫 작업은 즉시 실행
            while self._running and self._completed_cycles < self._max_cycles:
                await self._execute_one_cycle()

                if not self._running:
                    break

                # 다음 실행까지 대기
                self._current_status = "waiting"
                self._next_run = datetime.now() + timedelta(minutes=self._interval_minutes)

                # 1분 단위로 체크 (중단 요청 빠르게 반응)
                for _ in range(self._interval_minutes * 60):
                    if not self._running:
                        return
                    await asyncio.sleep(1)

        except asyncio.CancelledError:
            pass
        finally:
            self._current_status = "off"
            self._running = False

    # CEO 실패 시 사용할 기본 작업 목록
    _fallback_tasks = [
        "이번 주 콘텐츠 캘린더를 만들어줘",
        "브랜드 소개 인스타그램 피드 3개를 기획해줘",
        "유튜브 채널 컨셉과 첫 영상 기획서를 만들어줘",
        "경쟁사 분석 보고서를 작성해줘",
        "블로그 SEO 전략과 첫 게시물 초안을 만들어줘",
        "이번 달 매출 목표와 KPI를 설정해줘",
        "고객 페르소나를 정의해줘",
        "소셜미디어 해시태그 전략을 만들어줘",
    ]

    async def _execute_one_cycle(self):
        """1회 자율 작업 실행"""
        self._current_status = "working"

        try:
            # 1. CEO에게 다음 작업 요청
            command = await self._generate_next_task()

            # CEO 실패 시 fallback 목록에서 선택
            if not command:
                idx = self._completed_cycles % len(self._fallback_tasks)
                command = self._fallback_tasks[idx]
                self._add_log("fallback", f"🔄 기본 작업 사용: {command}")

            self._last_command = command
            self._add_log("generated", f"📋 작업 생성: {command}")

            # 2. 워크플로우 실행 (스트리밍을 전체 수집)
            from app import orchestrator
            full_output = []
            async for event_data in orchestrator.run_workflow(
                user_message=f"[AUTO] {command}",
                target_agent=None,
            ):
                full_output.append(event_data)

            self._completed_cycles += 1
            self._add_log("completed", f"✅ 작업 완료 #{self._completed_cycles}: {command}")

        except Exception as e:
            self._add_log("error", f"⚠️ 오류: {str(e)[:100]}")

    async def _generate_next_task(self) -> str:
        """CEO에게 다음 작업을 생성하도록 요청"""
        import re
        import httpx

        goals = memory.get_goals()
        decisions = memory.get_decisions()

        # 최근 세션에서 이미 한 작업 확인
        recent = memory.list_sessions()[:5]
        recent_commands = [s.get("command", "") for s in recent]
        recent_text = "\n".join([f"- {c}" for c in recent_commands if c])

        prompt = AUTOPILOT_PROMPT.format(
            goals=goals[:1000] if goals else "(목표 미설정)",
            decisions=decisions[:500] if decisions else "(없음)",
        )

        if recent_text:
            prompt += f"\n\n## 최근 완료된 작업 (반복 금지)\n{recent_text}"

        payload = {
            "model": agents.get_model(),
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": "지금 가장 중요한 다음 작업 1가지를 명령문으로 알려주세요."},
            ],
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 512,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
                resp = await client.post(f"{agents.OLLAMA_URL}/api/chat", json=payload)
                resp.raise_for_status()
                data = resp.json()

            raw = data.get("message", {}).get("content", "").strip()
            print(f"[AutoPilot] CEO 원문 응답: {raw[:200]}")

            # thinking 태그 제거
            raw = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()

            # 따옴표나 불필요한 접두어 제거
            raw = raw.strip('"\'')
            raw = re.sub(r'^(명령[:\s]*|작업[:\s]*)', '', raw).strip()

            # 첫 줄만 사용 (빈 줄 건너뜀)
            lines = [l.strip() for l in raw.split('\n') if l.strip()]
            command = lines[0] if lines else ""

            # 최소 3글자 이상
            return command if len(command) > 3 else None

        except Exception as e:
            print(f"⚠️ AutoPilot 작업 생성 실패: {e}")
            return None

    def _add_log(self, type: str, message: str):
        """로그 추가"""
        self._log.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": type,
            "message": message,
        })
        print(f"[AutoPilot] {message}")


# 싱글턴 인스턴스
autopilot = AutoPilot()
