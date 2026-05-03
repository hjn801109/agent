from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

print("1. Testing AutoPilot Start...")
resp = client.post("/api/autopilot/start", json={"interval_minutes": 30})
print(resp.json())

print("2. Checking Status...")
resp = client.get("/api/autopilot/status")
status = resp.json()
print("Running:", status["running"])
print("Interval:", status["interval_minutes"])

print("3. Testing AutoPilot Stop...")
resp = client.post("/api/autopilot/stop")
print(resp.json())

print("4. Checking Status Again...")
resp = client.get("/api/autopilot/status")
status = resp.json()
print("Running:", status["running"])
