import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

async def run_tests():
    print("=== 자율 업무 모드 자동화 테스트 ===")
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 1. 자율 업무 ON 테스트
        print("\n[테스트 1] 자율 업무 시작 (ON)")
        resp1 = await client.post("/api/autopilot/start", json={"interval_minutes": 30})
        print("응답:", resp1.json())
        
        await asyncio.sleep(0.5) # allow background task to start
        
        # 2. 상태 확인
        print("\n[테스트 2] 상태 확인")
        resp2 = await client.get("/api/autopilot/status")
        status = resp2.json()
        print("상태:", status)
        assert status["running"] == True
        assert status["interval_minutes"] == 30
        print("✅ 실행 간격 30분 적용 확인됨")
        
        # 3. 자율 업무 OFF 테스트
        print("\n[테스트 3] 자율 업무 중단 (OFF)")
        resp3 = await client.post("/api/autopilot/stop")
        print("응답:", resp3.json())
        
        # 4. 종료 후 상태 확인
        print("\n[테스트 4] 종료 후 상태 확인")
        resp4 = await client.get("/api/autopilot/status")
        final_status = resp4.json()
        print("상태:", final_status)
        assert final_status["running"] == False
        assert final_status["status"] == "off"
        print("✅ 성공적으로 모든 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(run_tests())
