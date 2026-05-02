# 💻 Developer — Next.js 환경에서의 인증(NextAuth.js/JWT), 데이터 암호화(AES-256), API Rate Limiting, 이미지 데이터 저장소(S3) 보안 권한 설정 및 인프라 보안 아키텍처 설계

💻 Developer: 작업 시작합니다.

CEO의 지시 사항과 Researcher/Business 에이론트의 보안 리스크 분석을 통합하여, **Next.js 기반의 보안 아키텍처 설계안**을 제시합니다. 이 설계는 PIPA(개인정보보호법) 준수와 데이터 등급별(Level 1~3) 차등 보안을 핵심으로 합니다.

---

# 🛡️ 미드미(midmi) 보안 아키텍처 설계서

## 1. 인증 및 인가 레이어 (Authentication & Authorization)
**목표:** NextAuth.js를 활용한 세션 관리 및 RBAC(역할 기반 접근 제어) 구현

*   **NextAuth.js + JWT 전략:**
    *   **Session Strategy:** `jwt` 전략 사용. 세션 데이터에 `role` (USER, ADMIN) 및 `userId`를 포함하여 클라이언트/서버 모두에서 즉각적인 권한 확인 가능하도록 설계.
    *   **Token Security:** JWT 서명 시 `AUTH_SECRET`을 사용하여 변조 방지. `HttpOnly`, `Secure`, `SameSite=Lax` 쿠키 설정을 통해 XSS 및 CSRF 공격 차단.
*   **RBAC (Role-Based Access Control):**
    *   **Middleware 활용:** Next.js Middleware에서 `/admin/*` 경로에 대해 `role === 'ADMIN'` 체크 로직 강제 적용.
    *   **API Route Guard:** 모든 API 엔드포인트 상단에 `getServerSession`을 통한 세션 유효성 및 권한 검증 로직 표준화.

## 2. 데이터 보호 레이어 (Data Encryption & Integrity)
**목표:** Level 3(민감정보) 데이터의 물리적/논리적 암호화

*   **At-Rest Encryption (저장 시 암호화):**
    *   **AES-256-GCM 적용:** 생체 특징점 및 개인 식별 데이터는 Node.js `crypto` 모듈의 `aes-256-gcm` 알고리즘을 사용하여 암호화. (GCM 모드를 사용하여 데이터 무결성(Integrity)까지 검증)
    *   **Key Management:** 암호화 키는 코드에 포함하지 않으며, AWS Secrets Manager 또는 Vercel Environment Variables를 통해 주입.
*   **In-Transit Encryption (전송 시 암호화):**
    *   **TLS 1.3 강제:** 모든 통신은 HTTPS를 통해서만 이루어지도록 HSTS(HTTP Strict Transport Security) 설정.
*   **Input Validation (Injection 방지):**
    *   **Zod 스키마 검증:** 모든 API 요청 Body, Query, Params는 `Zod`를 통해 타입 및 패턴 검사. (SQL Injection 및 NoSQL Injection 원천 차단)

## 3. API 보안 및 트래픽 제어 (API Security & Rate Limiting)
**목표:** DoS 공격 방지 및 서비스 가용성 확보

*   **API Rate Limiting:**
    *   **Upstash Redis 기반 구현:** Vercel Edge Middleware에서 Upstash(Redis)를 사용하여 IP 및 User ID 기반의 요청 횟수 제한.
    *   **Tier별 제한:** 
        *   `Public API`: 초당 10회 제한.
        *   `Authenticated API`: 초당 50회 제한.
        *   `Admin API`: 초당 5회 제한 (보안 극대화).
*   **CORS Policy:** `midmi.com` 도메인 외의 모든 외부 호출을 차단하도록 화이트리스트 기반 설정.

## 4. 스토리지 보안 (S3 Security Architecture)
**목표:** 사용자 얼굴 원본 이미지(Level 3)의 비인가 접근 차단

*   **Private Bucket 구성:** S3 Bucket의 `Public Access`를 완전히 차단하고, 모든 객체에 대해 `Block Public Access` 설정.
*   **Presigned URL 패턴:**
    *   이미지 조회 시 클라이언트가 S3에 직접 접근하는 것이 아니라, 서버(Next.js API)가 **유효 기간이 극히 짧은(예: 60초) Presigned URL**을 생성하여 전달.
    *   이를 통해 URL 탈취 시에도 재사용 불가능하게 설계.
*   **IAM Least Privilege:** Next.js 서버가 사용하는 IAM Role에는 해당 Bucket에 대한 `s3:PutObject`, `s3:GetObject` 권한만 부여 (전체 권한 부여 금지).

## 5. 인프라 및 운영 보안 (Infrastructure & DevOps)
**목표:** 환경 변수 관리 및 시스템 가시성 확보

*   **Secret Management:** `.env` 파일은 로컬 개발용으로만 사용하며, 운영 환경에서는 Vercel/AWS의 보안 저장소를 사용.
*   **Logging & Monitoring:** 
    *   **Audit Log:** 데이터 수정/삭제/권한 변경 등 주요 액션은 별도의 `audit_logs` 테이블에 기록 (누가, 언제, 무엇을).
    *   **Error Tracking:** Sentry를 연동하여 보안 관련 에러(Unauthorized, Forbidden) 발생 시 즉시 알림.

---

### 🛠️ 핵심 구현 코드 예시 (AES-256-GCM)
```typescript
import crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 12;
const KEY = Buffer.from(process.env.ENCRYPTION_KEY!, 'hex'); // 32 bytes

export function encrypt(text: string) {
  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto
