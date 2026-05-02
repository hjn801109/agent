# ✍️ Writer — 완성된 개발자 가이드의 문맥을 검토하여, 끊겼던 부분부터 이어지는 흐름이 자연스러운지 확인하고 미드미의 전문적인 톤앤매너로 최종 교정하세요.

✍️ Writer: 작업 시작합니다.

끊겼던 `2.3 데이터 파기 프로세스` 부분을 논리적으로 완결하고, 전체적인 문서의 기술적 전문성과 미드미의 신뢰감을 높이기 위해 문장 구조와 용어를 정밀하게 교정하였습니다.

***

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
- **로그 기록 대상:** 사용자 인증(Login/Logout), 권액 변경(RBAC), 개인정보 조회/수정/삭제, API 호출 이력.
- **로그 구조 (JSON Format):**
  ```json
  {
    
