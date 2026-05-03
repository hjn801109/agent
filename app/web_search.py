"""
웹 검색 모듈 — DuckDuckGo 기반 무료 웹 검색
API 키 불필요, 로컬 환경에서 바로 사용 가능합니다.
"""

from ddgs import DDGS
from typing import Optional


async def search_web(query: str, max_results: int = 5, region: str = "ko-kr") -> list[dict]:
    """DuckDuckGo 웹 검색을 수행합니다.
    
    Args:
        query: 검색 키워드
        max_results: 최대 결과 수
        region: 검색 지역 (기본: 한국어)
    
    Returns:
        [{"title": ..., "url": ..., "body": ...}, ...]
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                region=region,
                max_results=max_results,
            ))
            return results
    except Exception as e:
        print(f"⚠️ 웹 검색 실패: {e}")
        return []


async def search_news(query: str, max_results: int = 5, region: str = "ko-kr") -> list[dict]:
    """DuckDuckGo 뉴스 검색을 수행합니다.
    
    Returns:
        [{"title": ..., "url": ..., "body": ..., "date": ...}, ...]
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(
                query,
                region=region,
                max_results=max_results,
            ))
            return results
    except Exception as e:
        print(f"⚠️ 뉴스 검색 실패: {e}")
        return []


def format_search_results(results: list[dict], query: str) -> str:
    """검색 결과를 에이전트에게 전달할 마크다운 형식으로 변환합니다."""
    if not results:
        return f"🔍 '{query}' 검색 결과 없음"

    lines = [f"## 🔍 웹 검색 결과: \"{query}\"\n"]

    for i, r in enumerate(results, 1):
        title = r.get("title", "제목 없음")
        url = r.get("url", r.get("link", ""))
        body = r.get("body", r.get("snippet", ""))[:200]
        lines.append(f"### {i}. {title}")
        if url:
            lines.append(f"🔗 {url}")
        if body:
            lines.append(f"{body}\n")

    return "\n".join(lines)
