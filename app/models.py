"""
Pydantic 데이터 모델 — 미드미 1인 기업 OS
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ──────────────────────────────────────────
# 에이전트 정의
# ──────────────────────────────────────────

class AgentID(str, Enum):
    CEO = "ceo"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    DESIGNER = "designer"
    DEVELOPER = "developer"
    EDITOR = "editor"
    WRITER = "writer"
    RESEARCHER = "researcher"
    BUSINESS = "business"
    SECRETARY = "secretary"


AGENT_META = {
    AgentID.CEO:        {"emoji": "🧭", "name": "CEO",        "title": "Chief Executive Agent",     "color": "#FFD700"},
    AgentID.YOUTUBE:    {"emoji": "📺", "name": "YouTube",    "title": "Head of YouTube",           "color": "#FF0000"},
    AgentID.INSTAGRAM:  {"emoji": "📷", "name": "Instagram",  "title": "Head of Instagram",         "color": "#E1306C"},
    AgentID.DESIGNER:   {"emoji": "🎨", "name": "Designer",   "title": "Lead Designer",             "color": "#9B59B6"},
    AgentID.DEVELOPER:  {"emoji": "💻", "name": "Developer",  "title": "Lead Engineer",             "color": "#3498DB"},
    AgentID.EDITOR:     {"emoji": "✂️", "name": "Editor",     "title": "Video & Content Editor",    "color": "#E67E22"},
    AgentID.WRITER:     {"emoji": "✍️", "name": "Writer",     "title": "Copywriter",                "color": "#2ECC71"},
    AgentID.RESEARCHER: {"emoji": "🔍", "name": "Researcher", "title": "Trend & Data Researcher",   "color": "#1ABC9C"},
    AgentID.BUSINESS:   {"emoji": "💰", "name": "Business",   "title": "Head of Business",          "color": "#F39C12"},
    AgentID.SECRETARY:  {"emoji": "📱", "name": "Secretary",  "title": "Personal Assistant",        "color": "#E84393"},
}


# ──────────────────────────────────────────
# API 요청/응답 모델
# ──────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    target_agent: Optional[AgentID] = None  # None이면 CEO가 자동 분배
    session_id: Optional[str] = None


class AgentTask(BaseModel):
    agent_id: AgentID
    task: str


class CEODistribution(BaseModel):
    summary: str
    tasks: list[AgentTask]


class AgentResponse(BaseModel):
    agent_id: str
    emoji: str
    name: str
    content: str


class MemoryUpdateRequest(BaseModel):
    content: str


class PromptUpdateRequest(BaseModel):
    content: str


class SettingsResponse(BaseModel):
    ollama_url: str
    model: str
    available_models: list[str]


class SettingsUpdateRequest(BaseModel):
    model: Optional[str] = None
