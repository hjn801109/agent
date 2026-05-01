# 💻 Developer — 정의된 기능을 구현하기 위한 데이터 스키마(User, Report, Partner, Transaction)를 설계하고, Next.js 기반의 Admin API 엔드포인트 및 프론트엔드 컴포넌트 구조를 설계하라.

💻 Developer: 작업 시작합니다.

Business의 PRD와 Researcher의 벤치마킹 리포트를 바탕으로, 확장 가능한 **데이터 스키마**, **API 엔드포인트**, 그리고 **프론트엔드 컴포넌트 아키텍처**를 설계합니다.

---

## 1. 데이터 스키마 설계 (Prisma/TypeScript 기반)
확장성과 데이터 무결성을 위해 `enum`을 적극 활용하며, 분석용 데이터(Diagnosis)는 유연한 구조를 위해 `JSON` 타입을 포함합니다.

```typescript
// schema.prisma (Conceptual)

// 1. 사용자 및 멤버십
enum MembershipType {
  FREE
  PREMIUM
}

model User {
  id            String         @id @default(cuid())
  email         String         @unique
  name          String
  membership    MembershipType @default(FREE)
  reports       DiagnosisReport[]
  transactions  Transaction[]
  createdAt     DateTime       @default(now())
  updatedAt     DateTime       @updatedAt
}

// 2. AI 진단 리포트 (Domain 1)
enum FaceShape {
  ROUND
  OVAL
  SQUARE
  HEART
  LONG
}

model DiagnosisReport {
  id              String    @id @default(cuid())
  userId          String
  user            User      @relation(fields: [userId], references: [id])
  faceShape       FaceShape
  hairType        String    // 모질, 굵기 등
  stylePreference Json      // 선호하는 스타일 리스트 (Array of strings)
  analysisResult  Json      // AI가 생성한 상세 분석 텍스트/데이터
  createdAt       DateTime  @default(now())
}

// 3. 제휴 미용실 (Domain 3)
enum PartnerStatus {
  PENDING
  APPROVED
  REJECTED
}

model Partner {
  id           String        @id @default(cuid())
  name         String
  location     String        // 주소/지역
  status       PartnerStatus @default(PENDING)
  referralCount Int          @default(0) // 리퍼럴 발생 횟수
  contactInfo  String
  createdAt    DateTime      @default(now())
}

// 4. 결제 및 트랜잭션 (Domain 2, 4)
enum TransactionStatus {
  COMPLETED
  CANCELLED
  REFUNDED
}

enum TransactionType {
  REPORT_PURCHASE
  MEMBERSHIP_SUBSCRIPTION
}

model Transaction {
  id              String            @id @default(cuid())
  userId          String
  user            User              @relation(fields: [userId], references: [id])
  amount          Int
  type            TransactionType
  status          TransactionStatus
  paymentMethod   String
  createdAt       DateTime          @default(now())
}
```

---

## 2. Admin API 엔드포인트 설계 (Next.js App Router)
`Next.js`의 Route Handlers를 사용하여 도메인별로 분리된 RESTful API를 구축합니다.

### [Dashboard & Analytics]
- `GET /api/admin/dashboard/summary`: 핵심 KPI(총 매출, 신규 유저, 활성 파트너 수) 요약 데이터.
- `GET /api/admin/dashboard/funnel`: 가입 → 진단 → 결제 단계별 전환율 데이터.
(Researcher의 Funnel Chart 전략 반영)
- `GET /api/admin/dashboard/revenue-trend`: 일별/월별 매출 추이 (Line Chart용).

### [User & Report Management]
- `GET /api/admin/users`: 사용자 목록 조회 (Filter: `membership`, `createdAt`).
- `GET /api/admin/users/[id]/reports`: 특정 사용자의 진단 히스토리 조회.
- `PATCH /api/admin/users/[id]/membership`: 멤버십 등급 강제 변경.

### [Partner & Transaction Management]
- `GET /api/admin/partners`: 제휴 미용실 목록 (Filter: `status`).
- `POST /api/admin/partners/[id]/approve`: 파트너 승인/거절 처리.
- `GET /api/admin/transactions`: 결제 내역 조회 (Filter: `type`, `status`).
- `PATCH /api/admin/transactions/[id]/refund`: 결제 취소/환불 처리.

---

## 3. 프론트엔드 컴포넌트 구조 설계
`shadcn/ui`와 `Tailwind CSS`를 기반으로, 재사용 가능한 원자적 구조로 설계합니다. (Rose-tone 테마 적용)

### 📂 Directory Structure
```text
src/
├── components/
│   ├── admin/
│   │   ├── dashboard/
│   │   │   ├── KpiCard.tsx          // 상단 요약 카드 (Shopify 패턴)
│   │   │   ├── RevenueChart.tsx     // 매출 추이 차트 (Stripe 패턴)
│   │   │   └── ConversionFunnel.tsx // 전환율 깔때기 차트 (Mixpanel 패턴)
│   │   ├── users/
│   │   │   ├── UserTable.tsx        // 사용자 목록 (Data Table)
│   │   │   └── UserDetailModal.tsx  // 사용자 상세/진단 데이터 보기
│   │   ├── partners/
│   │   │   ├── PartnerList.tsx      // 파트너 목록
│   │   │   └── PartnerApprovalCard.tsx // 승인/거절 인터랙션
│   │   └── shared/
│   │       ├── DataTable.tsx        // 공통 테이블 컴포넌트
│   │       └── DateRangePicker.tsx  // 전역 날짜 필터
│   └──
