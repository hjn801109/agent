# 💻 Developer — 끊겼던 개발자 가이드의 2번(Backend: 데이터 보안 및 로그 관리)과 3번(Compliance: 운영 및 유지보수) 항목을 작성하세요. 특히 AES-256 암호화 적용, 접속 로그 보관(1~2년) 로직, 데이터 파기 프로세스(복구 불가능한 삭제)에 대한 기술적 명세를 포함해야 합니다.

💻 Developer: 작업 시작합니다.

# 🛠 개발자 가이드: 보안 및 컴플라이언스 명세 (Backend & Compliance)

본 문서는 미드미(midmi) 플랫폼의 데이터 무결성 확보와 법적 준거성(Compliance)을 위한 기술적 실행 지침을 정의한다.

## 2. Backend: 데이터 보안 및 로그 관리

### 2.1 AES-256-GCM 암호화 적용
개인정보(이름, 연락처, 이메일 등) 및 민감한 진단 결과 데이터는 반드시 암호화하여 저장한다.
- **알고리즘:** `AES-256-GCM` (Authenticated Encryption) 사용. (데이터 무결성 검증을 위해 CBC 대신 GCM 권장)
- **키 관리 (Key Management):**
  - 암호화 키는 소스 코드에 포함하지 않으며, `AWS KMS` 또는 `HashiCorp Vault`를 통해 관리한다.
  - 환경 변수(`process.env.ENCRYPTION_KEY`)를 통해 주입하되, 주기적(연 1회) 키 로테이션을 수행한다.
- **구현 로직:**
  - **Encryption:** `Plaintext + Key + IV(Initialization Vector) -> Ciphertext + Auth Tag`
  - **Decryption:** `Ciphertext + Auth Tag + IV + Key -> Plaintext` (태그 검증 실패 시 즉시 에러 처리)

### 2.2 접속 및 감사 로그(Audit Log) 관리
모든 데이터 접근 및 변경 이력은 추적 가능해야 한다.
- **로그 기록 대상:** 사용자 인증(Login/Logout), 권한 변경(RBAC), 개인정보 조회/수정/삭제, API 호출 이력.
- **로그 구조 (JSON Format):**
  ```json
  {
    "timestamp": "ISO8601",
    "actor_id": "user_uuid",
    "action": "DATA_ACCESS | DATA_UPDATE",
    "resource": "user_profile",
    "ip_address": "xxx.xxx.xxx.xxx",
    "user_agent": "...",
    "status": "SUCCESS | FAILURE"
  }
  ```
- **보관 주기 및 계층화 저장:**
  - **Hot Storage (최근 3개월):** `Elasticsearch` 또는 `CloudWatch Logs`에 저장하여 즉시 검색 가능하도록 유지.
  - **Cold Storage (3개월 ~ 2년):** `Amazon S3` (Glacier Instant Retrieval)로 아카이빙. `S3 Lifecycle Policy`를 통해 2년 경과 시 자동 삭제 설정.

### 2.3 데이터 파기 프로세스 (Data Destruction)
사용자 탈퇴 또는 법적 보관 기간 만료 시, 복구가 불가능한 상태로 삭제한다.
- **논리적 삭제(Soft Delete) 후 물리적 삭제(Hard Delete):**
  - 탈퇴 즉시 `is_deleted: true` 처리하여 서비스 노출 차단.
  - 배치 작업(Cron Job)을 통해 30일 경과 후 DB에서 `DELETE` 쿼리 실행.
- **Crypto-shredding (암호화 키 파기):**
  - 특정 사용자의 데이터 전용 키를 별도 관리할 경우, 해당 사용자의 암호화 키를 삭제함으로써 데이터의 복구 가능성을 원천 차단한다.
- **백업 데이터 관리:** 백업본 내 개인정보 역시 동일한 파기 주기를 따르도록 백업 스냅샷 삭제 정책을 동기화한다.

---

## 3. Compliance: 운영 및 유지보수

### 3.1 모니터링 및 장애 대응 (Observability)
- **Error Tracking:** `Sentry`를 통합하여 런타임 에러 및 API 5xx 에러 실시간 감지 및 알림.
- **Performance Monitoring:** `New Relic` 또는 `Datadog`을 통해 API 응답 시간(Latency) 및 DB 부하 모니터링.
- **Health Check:** `/api/health` 엔드포인트를 운영하여 인프라 상태를 주기적으로 체크하고, 장애 시 Slack 알림 연동.

### 3.2 백업 및 재해 복구 (Backup & DR)
- **DB 백업:** `Amazon RDS`의 `Automated Backups`를 활성화하여 Point-in-Time Recovery(PITR)를 지원한다. (최대 35일 보관)
- **RTO/RPO 설정:**
  - **RPO (Recovery Point Objective):** 최대 5분 이내 데이터 손실 허용.
  - **RTO (Recovery Time Objective):** 장애 발생 후 1시간 이내 서비스 정상화 목표.

### 3.3 CI/CD 및 코드 품질 관리
- **Automated Testing:** `Jest` (Unit Test) 및 `Cypress` (E2E Test)를 파이프라인에 포함하여 배포 전 정적/동적 검증 수행.
- **Dependency Security:** `GitHub Dependabot`을 활성화하여 취약점이 발견된 라이브러리 자동 알림 및 PR 생성.
- **Deployment:** `GitHub Actions`를 통한 Blue-Green 또는 Canary 배포 전략을 사용하여 배포 중 중단 없는 서비스 유지.

📊 평가: 완료 — 요청된 보안
