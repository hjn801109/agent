# 💻 Developer — 웹사이트 구축을 위한 데이터 스키마(LTV 측정 기반)와 프론트엔드 기술 스택(Glassmorphism, Serif 타이포그래피 구현에 최적화된 구조)에 대한 초기 계획 및 기술 명세서를 작성할 것.

💻 Developer: 작업 시작합니다.

## 🚀 웹사이트 구축을 위한 기술 명세서 및 초기 계획

본 문서는 CEO의 지시사항("웹사이트 구축을 위한 데이터 스키마(LTV 측정 기반)와 프론트엔드 기술 스택에 대한 초기 계획 및 기술 명세서 작성")을 기반으로, 앞선 의사결정 로그와 개인 메모리(보안, 디자인 시스템)를 통합하여 개발 착수를 위한 구체적인 기술 청사진을 제공합니다.

### 1. 아키텍처 개요 (Architectural Overview)

**🎯 목표:** LTV 측정에 최적화된 데이터 흐름과 보안 표준을 만족하는 반응형 웹 애플리케이션 구축.
**🛠️ 기술 스택 제안:** Next.js (App Router 권장), TypeScript, Tailwind CSS (Glassmorphism 구현 용이성 극대화).

| 레이어 | 주요 기술/역할 | 핵심 요구사항 |
| :--- | :--- | :--- |
| **프론트엔드** | Next.js, TypeScript, Tailwind CSS | Glassmorphism 및 Rose Tone 디자인 시스템 완벽 구현. 사용자 경험(UX) 최적화. |
| **백엔드/API** | Next.js API Routes 또는 별도 Node.js 서버 (선택) | 데이터 인증(RBAC), 암호화된 통신(HTTPS 필수), Rate Limiting 적용. |
| **데이터베이스** | PostgreSQL 또는 MongoDB (유연한 스키마 필요 시) | LTV 측정 지표 및 사용자/트랜잭션 데이터를 구조적으로 저장. |
| **보안 모듈** | AES-256, RBAC 구현 | 데이터 암호화(저장/전송), 역할 기반 접근 제어. |

---

### 2. 데이터 스키마 설계 (LTV 측정 기반)

데이터는 LTV 측정과 보안 요구사항(RBAC)을 중심으로 설계하며, 모든 민감 정보는 암호화되어 저장되어야 합니다.

#### 2.1. User Schema (사용자 및 권한 관리)
**목표:** 사용자 인증 및 역할 기반 접근 제어(RBAC)의 근간.
*   `user_id` (UUID/BigInt, Primary Key)
*   `email` (String, Unique, Encrypted by AES-256)
*   `password_hash` (String, Argon2 또는 bcrypt 해시 적용)
*   `role` (Enum: `ADMIN`, `MANAGER`, `USER`) - **RBAC 핵심 필드**
*   `subscription_status` (Enum: `FREE`, `PREMIUM`, `PRO`) - LTV 측정의 기초 데이터.
*   `created_at`, `updated_at`

#### 2.2. Report Schema (AI 진단 및 리포트 데이터)
**목표:** AI 분석 결과와 사용자 데이터를 연결하여 신뢰도를 높임.
*   `report_id` (UUID, Primary Key)
*   `user_id` (Foreign Key to User)
*   `analysis_date` (Date)
*   `style_recommendation` (JSONB/Text: AI가 제시한 스타일 상세 데이터)
*   `trust_score` (Float: 데이터 기반 신뢰도 점수, 0.0 ~ 1.0) - **Glassmorphism 시각화의 핵심 지표.**
*   `data_source_hash` (String: 원본 데이터 무결성 검증용 해시값)

#### 2.3. Transaction Schema (구독 및 결제 기록)
**목표:** LTV 측정을 위한 재정적 흐름 추적.
*   `transaction_id` (UUID, Primary Key)
*   `user_id` (Foreign Key to User)
*   `type` (Enum: `SUBSCRIPTION`, `ADJUSTMENT`, `REFUND`)
*   `amount` (Float/Decimal)
*   `status` (Enum: `SUCCESS`, `PENDING`, `FAILED`)
*   `transaction_date` (Timestamp)

---

### 3. 프론트엔드 기술 스택 및 디자인 명세서

**🎯 목표:** Glassmorphism, Rose Tone, Serif 타이포그래피를 구현하여 '친절함 + 전문성'을 시각적으로 증명.
**🛠️ 구조 제안:** Next.js App Router 기반의 컴포넌트 중심 아키텍처.

#### 3.1. 디자인 시스템 정의 (Design System Definition)
*   **Color Palette (Rose Tone 기반):**
    *   Primary: `#E07A5F` (강조색)
    *   Secondary: `#F4ACB7` (배경/부드러움)
    *   Accent: 은은한 Rose Gradient 활용.
*   **Typography:** **Serif Font Family** (예: Playfair Display 또는 Lora). 본문 가독성을 위해 Sans-serif를 보조로 사용.
*   **Glassmorphism Implementation:**
    *   `backdrop-filter: blur(16px);` 적용을 모든 카드, 모달, 네비게이션 바에 기본으로 설정.
    *   투명도(Opacity)는 90% ~ 95% 범위로 설정하여 부드러운 느낌 유지.

#### 3.2. 컴포넌트 구조 (Component Structure)
모든 UI 요소는 재사용 가능하도록 Props 기반으로 설계합니다.

1.  **`GlassCard.tsx`:** 배경색, 테두리(Border), 그리고 `backdrop-filter: blur()`를 관리하는 핵심 컴포넌트. (데이터 신뢰도 시각화에 사용)
2.  **`SerifText.tsx`:** 헤드라인 및 중요한 텍스트에 Serif 타이포그래피를 강제 적용하는 래퍼 컴포넌트.
3.  **`RoseGradient.tsx`:** Rose Tone 기반의 부드러운 그라데이션을 동적으로 생성하여 배경 및 CTA에 적용.

---

### 4. 보안 및 데이터 흐름 명세 (Security & Data Flow Specification)

**🎯 목표:** AES-256 암호화와 RBAC를 서비스 전체에 통합.

1.  **데이터 저장 시점 (Persistence):**
    *   사용자 정보(`email`, 민감한 설정)는 DB에 저장 전 **AES-256-GCM** 알고리즘을 사용하여 서버 측에서 암호화하여 저장해야 합니다.
    *   민감 데이터의 키(Key)는 환경 변수(Environment Variables)를 통해 안전하게 관리하며, 절대 코드 내에 하드코딩하지 않습니다.

2.  **API 접근 제어 (RBAC Implementation):**
    *   모든 백엔드 API 엔드포인트(`POST`, `GET` 등) 앞단에서 JWT 검증 및 사용자 역할(`role`) 확인 로직을 필수적으로 삽입합니다.
    *   예: `/api/reports/create` 요청 시, 인증된 사용자가 `MANAGER` 또는 `ADMIN` 역할이어야만 접근 허용.

3.  **데이터 파기 정책 (Data Deletion Policy):**
    *   **Soft Delete:** 사용자 및 트랜잭션 데이터는 즉시 삭제하지 않고, `is_deleted: true` 플래그를 설정하여 논리적 삭제를 수행합니다. 이는 LTV 추적을 위해 필요합니다.
    *   **Hard Delete (복구 불가능한 삭제):** 사용자가 명시적으로 요청하거나, 법적 요구사항 발생 시에만 실제 데이터베이스 레코드에서 암호화 키와 함께 데이터를 **복구 불가능하게 파기(Cryptographic Shredding)**하는 프로세스를 백엔드 레이어에서 구현합니다.

---
📊 평가: 진행중 — 기술 스택과 데이터 구조의 초기 청사진이 명확히 정의되었으나, 실제 코드 구현 단계로 넘어가기 위한 API 및 DB 연결 세부 사항에 대한 추가 입력이 필요함.
📝 다음 단계: 백엔드(API)와 데이터베이스 레이어의 구체적인 CRUD 엔드포인트 및 인증/인가 로직을 설계합니다.
