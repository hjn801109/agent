# 💻 Developer — Next.js 기반의 초기 웹사이트 아키텍처 및 데이터 스키마(LTV, 구독 상태 포함)를 확정하고, Designer와 Writer가 정의한 시각 시스템 가이드라인을 반영하여 컴포넌트 개발을 시작할 수 있도록 기술 설계 초안을 작성합니다.

💻 Developer: 작업 시작합니다.

## ⚙️ Next.js 기반 웹사이트 기술 설계 초안 (Architecture & Data Schema)

CEO님의 지시와 Designer/Writer가 확립한 시각 시스템 가이드라인(Rose Tone, Glassmorphism)을 반영하여, 데이터의 신뢰성과 사용자 경험을 극대화하는 Next.js 기반 아키텍처 및 핵심 데이터 스키마를 설계합니다. 이 초안은 컴포넌트 개발을 즉시 시작할 수 있는 기반이 됩니다.

---

### 1. 시스템 아키텍처 개요 (Next.js Stack)

**목표:** 높은 성능, 확장성, 보안성을 동시에 확보하며, Glassmorphism 디자인 구현에 최적화된 구조를 구축합니다.

| 영역 | 기술 스택 | 주요 역할 및 고려 사항 |
| :--- | :--- | :--- |
| **프레임워크** | Next.js (App Router) | 서버 컴포넌트(RSC)와 클라이언트 컴포넌트의 혼합 사용을 통해 성능 최적화. 데이터 페칭은 서버에서 처리하여 보안 강화. |
| **스타일링** | Tailwind CSS + CSS Modules | Rose Tone 색상 변수(`--rose-tone-primary`, `--rose-tone-accent`)를 기반으로 모든 디자인 시스템을 일관되게 적용합니다. Glassmorphism 구현 시 `backdrop-blur` 및 투명도 설정을 표준화합니다. |
| **데이터베이스** | PostgreSQL (권장) | 관계형 데이터의 안정성과 복잡한 LTV/트랜잭션 데이터 관리에 적합하며, 향후 RBAC(역할 기반 접근 제어) 확장 용이. |
| **백엔드 / API** | Next.js API Routes 또는 별도 Node.js (Express/NestJS) | 인증(NextAuth.js 연동), 데이터 암호화(AES-256) 로직을 통합하여 데이터 보안을 보장합니다. |
| **인증 및 권한** | NextAuth.js + JWT | 사용자 세션 관리와 RBAC(Admin/User 역할 분리)를 구현하여 데이터 접근 제어의 기반을 마련합니다. |

### 2. 핵심 데이터 스키마 설계 (Schema Definition)

데이터 구조는 LTV 측정과 구독 상태 관리를 최우선으로 하며, 확장성을 위해 Enum 및 명확한 타입 정의(TypeScript)를 원칙으로 합니다.

#### A. 사용자 테이블 (`User`)
사용자의 기본 정보와 권한을 관리합니다.

```typescript
// sessions/2026-05-02T01-02/developer.md 기반 확장
export type SubscriptionStatus = 'Free' | 'Basic' | 'Premium'; // Enum 적용 원칙

interface User {
  id: string;
  email: string;
  name: string;
  role: 'User' | 'Admin'; // RBAC 정의
  subscriptionStatus: SubscriptionStatus; // LTV 기반 상태 관리 핵심 필드
  createdAt: Date;
  updatedAt: Date;
  // 보안 관련 필드 (암호화된 토큰 저장)
  encryptedData?: string; 
}
```

#### B. 리포트/진단 테이블 (`Report`)
사용자가 생성하거나 조회하는 핵심 데이터입니다.

```typescript
interface Report {
  id: string;
  userId: string; // 외래 키 (User 테이블 연결)
  reportType: 'StyleDiagnosis' | 'LTV_Analysis' | 'PartnerReview';
  data: Record<string, any>; // 실제 진단 데이터 (JSON Blob)
  trustScore: number; // Designer가 시각화할 핵심 지표 (0~100)
  createdAt: Date;
}
```

#### C. 트랜잭션 테이블 (`Transaction`)
구독 및 결제 이력 관리를 통해 LTV 산출의 근거를 마련합니다.

```typescript
interface Transaction {
  id: string;
  userId: string;
  type: 'Subscription' | 'Payment'; // 구독 또는 일반 결제
  amount: number;
  status: 'Success' | 'Failed' | 'Pending';
  date: Date;
  // LTV 계산에 필수적인 데이터 (구독 시작일, 갱신 주기 등)
}
```

### 3. 디자인 시스템 및 컴포넌트 설계 지침

Designer의 시각 시스템을 코드로 구현하기 위한 핵심 규칙입니다. 모든 컴포넌트는 이 규칙을 따르도록 설계되어야 합니다.

#### A. 색상 및 타이포그래피 변수 정의 (Tailwind/CSS)
Rose Tone과 Serif 스타일을 전역으로 설정합니다.

```css
/* globals.css 또는 Tailwind 설정 파일에 정의 */
:root {
  /* Rose Tone 팔레트 */
  --rose-tone-primary: #E07A5F; /* 핵심 강조 색상 */
  --rose-tone-light: #F4ACB7; /* 배경/보조 색상 */
  --rose-tone-dark: #B86D51; /* 깊이감 있는 톤 */

  /* 타이포그래피 설정 */
  --font-serif: 'Playfair Display', serif; /* 전문성 부여 */
}
```

#### B. Glassmorphism 컴포넌트 구현 원칙 (핵심)

Glassmorphism은 데이터의 투명성과 신뢰감을 시각화하는 핵심 요소입니다.

1.  **배경:** 배경은 부드러운 Rose Tone 그라데이션을 사용합니다.
    *   `bg-gradient-to-br from-rose-tone-light to-white`
2.  **Glassmorphism 패널:** 컨테이너에 `backdrop-blur`와 낮은 투명도를 적용하여 '유리' 느낌을 연출합니다.
    *   `bg-white/15 backdrop-blur-md border border-white/30 shadow-lg`
3.  **신뢰도 시각화:** 데이터의 신뢰 점수(`trustScore`)는 Glassmorphism 카드 내부에 배치하여, **데이터 자체에 대한 신뢰감**을 시각적으로 전달합니다. (예: `trustScore` 텍스트를 Rose Tone으로 강조)

### 4. 초기 컴포넌트 구조 예시 (Example Component Structure)

다음은 Hero Section의 핵심 아이디어를 Glassmorphism 기반으로 구현하는 방법입니다.

```jsx
// components/HeroSection.tsx (클라이언트 컴포넌트)
import React from 'react';

const HeroSection = ({ headline, subcopy, trustScore }) => {
  return (
    <div className="min-h-[60vh] flex items-center justify-center p-8 
                       bg-gradient-to-br from-rose-tone-light to-white">
      
      {/* Glassmorphism Container: 신뢰감을 담는 유리 패널 */}
      <div className="max-w-4xl mx-auto p-10 rounded-3xl shadow-2xl 
                      bg-white/20 backdrop-blur-lg border border-white/50">
        
        {/* A. 헤드라인 (H1) - Serif 적용 */}
        <h1 className={`text-5xl md:text-7xl font-serif text-gray-800 mb-4 leading-tight`}>
          {headline}
        </h1>

        {/* B. 서브 카피 */}
        <p className="text-lg text-gray-600 mb-8">
          {subcopy}
        </p>

        {/* C. 핵심 비주얼/신뢰도 시각화 (데이터 투명성) */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-200">
          <p className="text-sm font-medium text-rose-tone-dark">
            AI 기반 신뢰 점수: 
          </p>
          {/* 데이터 시각화 (그라데이션 활용) */}
          <div className={`w-32 h-10 rounded-full bg-gradient-to-r from-rose-tone-primary to-pink-300 flex items-center justify-center text-white font-bold text-xl shadow-inner`}>
            {trustScore}%
          </div>
        </div>

        {/* D. CTA 버튼 */}
        <button className={`mt-10 px-8 py-3 font-semibold rounded-full 
                            bg-rose-tone-primary text-white 
                            hover:bg-rose-tone-dark transition duration-300 shadow-md`}>
          나만의 정밀 리포트 확인하기
        </button>

      </div>
    </div>
  );
};

export default HeroSection;
```

---
📊 평가: 진행중 — 기술 설계의 기반이 마련되었으며, 이제 이 설계에 따라 실제 코드를 구현하는 단계로 넘어갈 준비가 되었습니다.
📝 다음 단계: 데이터베이스 마이그레이션 계획 및 NextAuth.js 인증 흐름 상세 설계
