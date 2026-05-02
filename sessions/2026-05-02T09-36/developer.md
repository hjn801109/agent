# 💻 Developer — 확정된 데이터 스키마를 기반으로 MVP 기능 구현 상세 명세서를 작성하여 개발 준비를 완료해 주세요.

💻 Developer: 작업 시작합니다.

요청하신 대로 확정된 데이터 스키마를 기반으로 MVP 기능 구현 상세 명세서를 작성하여 개발 준비를 완료하겠습니다. 현재 세션에서 직접적으로 해당 스키마 파일을 참조할 수 없으므로, 이전 메모리에 기록된 설계 원칙(LTV 측정, 보안 아키텍처)과 정의된 엔티티(User, Report, Partner, Transaction 등)를 기반으로 MVP의 핵심 기능 구현 로드맵 및 기술 명세를 제시합니다.

이 문서는 개발팀이 즉시 코드를 작성할 수 있도록 데이터 흐름, API 명세, 그리고 보안 요구사항을 포함하는 **Architectural Specification**입니다.

---

# 📄 MVP 기능 구현 상세 명세서 (Architectural Specification)

## 1. 목표 및 범위 (Goal & Scope)
본 문서는 미드미(midmi) 플랫폼의 최소 기능 제품(MVP) 구현을 위한 기술적, 기능적 요구사항을 정의합니다. MVP는 **사용자 진단, 맞춤형 리포트 제공, 그리고 기본 보안 구조**에 중점을 둡니다.

*   **핵심 목표:** 데이터 기반 신뢰 구축 (LTV 측정의 기초 마련).
*   **범위:** 사용자 인증/인가, 진단 데이터 입력, 개인화된 리포트 조회 기능 구현.
*   **제외 범위 (Phase 2 이후):** 인플루언서 제휴 네트워크, 복잡한 구독 관리 시스템(다단계 가격 구조)은 Phase 2로 이관합니다.

## 2. 데이터 모델 정의 및 스키마 기반 설계 (Data Model Specification)

확정된 데이터 스키마를 기반으로 핵심 엔티티와 관계를 정의합니다. 모든 데이터는 **LTV 측정에 최적화**되도록 설계됩니다.

### 2.1. 핵심 엔티티 (Core Entities)

| 엔티티 | 주요 역할 | 핵심 필드 (Schema Reference) | 보안/관계 고려사항 |
| :--- | :--- | :--- | :--- |
| **User** | 사용자 인증 및 기본 정보 관리 | `id`, `email`, `name`, `subscriptionStatus` (Enum), `createdAt` | RBAC 적용, AES-256 암호화 필요 |
| **Diagnosis** | 사용자의 초기 진단 결과 저장 | `userId` (FK), `diagnosisData` (JSON/Text), `scoreMetrics`, `timestamp` | 민감 정보 처리 (암호화 고려) |
| **Report** | 사용자에게 제공되는 맞춤형 리포트 | `userId` (FK), `reportType` (Enum), `generatedAt`, `content` (Text, JSON) | 접근 권한(RBAC) 기반 조회 제한 |
| **Partner** | 제휴 미용실/전문가 정보 관리 | `partnerId`, `name`, `specialty`, `contactInfo`, `status` | Admin 전용 접근 |
| **Transaction** | 결제 및 구독 상태 기록 (LTV 핵심) | `userId` (FK), `amount`, `type` (Subscription/OneTime), `status` (Enum), `date` | 데이터 무결성 최우선, 암호화 저장 |

### 2.2. 데이터 흐름 상세 (Data Flow Detail)

1.  **User Onboarding & Auth:** 사용자 가입 시, `User` 엔티티에 기본 정보와 초기 구독 상태(`subscriptionStatus`)를 기록하고, 인증 토큰(JWT) 발급을 통해 세션을 확보합니다.
2.  **Diagnosis Input:** 사용자가 진단 데이터를 입력하면, 해당 데이터는 **암호화된 상태**로 `Diagnosis` 테이블에 저장됩니다. (보안 요구사항 충족)
3.  **Report Generation:** 관리자(또는 시스템)가 특정 기준(예: 진단 점수, 구독 상태)에 따라 `Report`를 생성하고 사용자에게 제공합니다. 이 과정에서 **LTV 지표**가 리포트의 핵심 요소로 포함되어야 합니다.
4.  **Transaction Logging:** 모든 결제 및 구독 변경은 `Transaction` 테이블에 기록되며, 이는 LTV 분석을 위한 가장 중요한 데이터 소스가 됩니다.

## 3. API 명세 (API Specification)

모든 API 엔드포인트는 **RESTful 원칙**을 따르며, 보안(RBAC)과 데이터 무결성을 최우선으로 합니다.

### 3.1. 인증 및 사용자 API (Authentication & User API)

| Endpoint | Method | 설명 | 접근 권한 | 요구 스키마 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/auth/register` | POST | 신규 사용자 등록 | Public | User Schema Input |
| `/api/auth/login` | POST | 사용자 로그인 및 JWT 발급 | Public | - |
| `/api/user/profile` | GET | 현재 사용자 프로필 조회 | Authenticated (Self) | User Schema Output |
| `/api/user/diagnosis` | POST | 새로운 진단 데이터 저장 | Authenticated (Self) | Diagnosis Schema Input |

### 3.2. 리포트 및 데이터 API (Report & Data API)

| Endpoint | Method | 설명 | 접근 권한 | 요구 스키마 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/report/:id` | GET | 특정 사용자 리포트 조회 | Authenticated (Self/Admin) | Report Schema Output |
| `/api/reports/dashboard` | GET | 사용자 대시보드 데이터 집계 (LTV 포함) | Authenticated (Self) | Aggregated Data |
| `/api/partners` | GET | 제휴 파트너 목록 조회 | Admin Only | Partner Schema List |

### 3.3. 관리자 API (Admin API - RBAC 적용)

*   **권한:** `ADMIN` 역할에 한해 접근 허용.
*   **기능:** 사용자 및 데이터 관리, 시스템 설정 변경.
*   **보안:** 모든 요청은 **AES-256 암호화된 세션 키**와 **RBAC 토큰 검증**을 거쳐야 합니다.

## 4. 기술 구현 상세 (Technical Implementation Details)

### 4.1. 프론트엔드 요구사항 (Next.js / Glassmorphism 적용)
*   **스타일 시스템:** Tailwind CSS 기반으로 Rose Tone(주요 색상), Serif 타이포그래피, Glassmorphism 효과(블러 16px)를 모든 컴포넌트에 일관되게 적용합니다.
*   **데이터 시각화:** `Transaction` 및 `Diagnosis` 데이터는 **그라데이션**을 활용하여 전문성과 따뜻함을 동시에 표현하며 시각화합니다. (마케팅 문구 옵션 1 기반)

### 4.2. 백엔드 보안 아키텍처 (Security Architecture)
*   **암호화:** 민감한 사용자 데이터(`Diagnosis`, `Transaction` 내의 상세 정보)는 **AES-256-GCM** 알고리즘을 사용하여 저장합니다. 키 관리는 환경 변수 및 별도 Key Vault를 통해 관리합니다.
*   **접근 제어 (RBAC):** 모든 API 요청은 JWT 기반으로 사용자 역할(`Role`)과 접근 권한(`Permission`)을 검증하는 미들웨어를 반드시 거칩니다.
*   **데이터 파기:** `Soft Delete` 및 `Hard Delete` 로직을 구현합니다. Hard Delete 시, 암호화된 데이터 블록에 대한 복구 불가능한 삭제 프로세스를 보장합니다.

### 4.3. 개발 우선순위 (MVP Focus)

1.  **Phase 1: Security & Schema Foundation:** RBAC, JWT 인증/인가 시스템 및 모든 엔티티의 DB 스키마 구현 (가장 중요).
2.  **Phase 2: Core Data Flow:** User 등록 → 진단 입력 → 데이터 저장(암호화) 흐름 완벽 구현.
3.  **Phase 3: Reporting & UI:** 사용자에게 맞춤 리포트 제공 및 Glassmorphism 기반의 대시보드 UI 구현.

---

📊 평가: 진행중 — 요청된 명세서의 프레임워크를 성공적으로 구축했으나, 실제 데이터 스키마 파일이 없어 구체적인 DB/코드 구현은 다음 단계에서 필요합니다.
📝 다음 단계: Phase 1에 따라 `User`, `Diagnosis`, `Transaction` 테이블의 상세 SQL DDL 및 Next.js API Route 핸들러(보안 로직 포함) 초안 작성을 시작합니다.
