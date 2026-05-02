# 📱 Secretary — 완성된 '개인정보 처리방침 개발자 가이드' 전체본을 통합하여 최종 결과물로 정리하고, 이번 작업 완료를 기록하여 업무 리포트를 생성하세요.

📱 Secretary: 작업 시작합니다.

# 🛠 [최종 통합본] 개발자 가이드: 보안 및 컴플라이언스 명세 (Backend & Compliance)

본 문서는 미드미(midmi) 플랫폼의 데이터 무결성 확보와 법적 준거성(Compliance)을 위한 기술적 실행 지침을 정의한다.

## 2. Backend: 데이터 보안 및 로그 관리

### 2.1 AES-256-GCM 암호화 적용
개인정보(이름, 연락도, 이메일 등) 및 민민감한 진단 결과 데이터는 반드시 암호화하여 저장한다.
- **알고리즘:** `AES-256-GCM` (Authenticated Encryption) 사용. (데이터 무결성 검증을 위해 CBC 대신 GCM 권장)
- **키 관리 (Key Management):**
  - 암호화 키는 소스 코드에 포함하지 않으며, `AWS KMS` 또는 `HashiCorp Vault`를 통해 관리한다.
  - 환경 변수(`process.env.ENCRYPTION_KEY`)를 통해 주입하되, 주기적(연 1회) 키 로테이션을 수행한다.
- **구현 로직:**
  - **Encryption:** `Plaintext + Key + IV(Initialization Vector) -> Ciphertext + Auth Tag`
  - **Decryption:** `Ciphertext + Auth Tag + IV + Key -> Plaintext` (태그 검증 실패 시 즉시 에러 처리)

### 2.2 접속 및 감사 로그(Audit Log) 관리
모모든 데이터 접근 및 변경 이력은 추적 가능해야 한다.
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
- **단계별 삭제 로직:**
  1. **Soft Delete (논리적 삭제):** 사용자 탈퇴 즉시 `is_deleted: true` 플래그를 활성화하여 서비스 노출을 차단하고, 데이터 참조 무결성을 유지한다.
  2. **Hard Delete (물리적 삭제):** 전자상거래법 등 관련 법령에 따른 의무 보관 기간(예: 결제 기록 5년)이 경과한 데이터는 `Batch Job`을 통해 데이터베이스에서 물리적으로 완전히 삭제한다.
- **백업 데이터 관리:** S3 등 외부 스토리지에 저장된 백업본 또한 동일한 생명주기 정책(Lifecycle Policy)을 적용하여, 원본 데이터 삭제 시점에 맞춰 물리적 파기가 이루어지도록 설계한다.

### 2.4 권한 관리 및 접근 제어 (RBAC)
- **RBAC(Role-Based Access Control) 구현:** 관리자(Admin), 운영자(Operator), 일반 사용자(User)로 권한을 엄격히 분리한다.
- **최소 권한 원칙:** 모든 API 엔드포인트는 요청자의 Role을 검증하며, 각 역할에 필요한 최소한의 리소스 접근 권한만 부여한다.

***

# 📋 [업무 리포트] 작업 완료 보고

**1. 작업 개요**
- **작업명:** '개인정보 처리방침 개발자 가이드' 통합 및 최종본 완성
- **작업 일시:** 2026-05-02
- **담당 에이전트:** Secretary (통합 및 정리), Developer (초안), Writer (교정)

**2. 수행 내용**
- **데이터 통합:** Developer가 작성한 보안 기술 명세와 Writer가 교정한 문장 구조를 결합하여 단일 문서로 통합.
- **누락 내용 보완:** 끊겼던 `2.3 데이터 파기 프로세스`의 논리적 흐름(Soft/Hard Delete 및 백업 관리)을 완성하여 기술적 완결성 확보.
- **구조 최적화:** 보안, 로그, 파기, 권한 관리로 이어지는 컴플라이언스 체계의 구조적 정리.

**3. 결과물 상태**
- **상태:** **완료 (Done)**
- **산출물:** `개발자 가이드: 보안 및 컴플라이언스 명세 (최종본)`
- **다음 액션:** 해당 가이드를 기반으로 실제 Backend 인프라(KMS, S3 Policy) 설정 및 구현 단계로 전환 가능.

📊 평가: 완료 — 끊겼던 기술 명세를 논리적으로 완결하고 전체 문서를 통합하여 최종 결과물을 생성함.
📝 다음 단계: 개발자(Developer)에게 완성된 가이드를 전달하여 보안 아키텍처 구현 착수 지시.
