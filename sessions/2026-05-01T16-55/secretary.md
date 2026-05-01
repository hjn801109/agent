# 📱 Secretary — 확정된 어드민 페이지 기획안을 요약하여 개발 및 디자인 작업이 즉시 시작될 수 있도록 프로젝트 로드맵과 작업 체크리스트를 생성하라.

📱 Secretary: 작업 시작합니다.

# 🚀 [Project Roadmap] 미드미(midmi) 어드민 대시보드 구축

본 문서는 Business, Researcher, Developer, Designer의 산출물을 통합하여, 개발 및 디자인 팀이 즉시 실행 가능한 단계별 로드맵을 제시합니다.

## 1. 프로젝트 개요
* **프로젝트명:** midmi Admin Dashboard 구축
* **핵젝트 컨셉:** **"Rose-Tech Clarity"** (로즈 톤의 따뜻함 + 데이터의 전문적 가독성)
* **핵심 목표:** AI 진단 데이터 관리, 프리미엄 멤버십 운영, 제휴 미용실(B2B) 네트워크 관리 자동화

---

## 2. 단계별 로드맵 (Phase-based Roadmap)

### Phase 1: 기반 구축 (Foundation) — [Target: 1-2주 차]
* **목표:** 데이터 구조 확립 및 디자인 시스템(Design Token) 구축
* **핵심 작업:**
    * **[Dev]** Prisma 스키마 기반 DB 모델링 및 Migration 실행
    * **[Dev]** Next.js 프로젝트 초기 환경 설정 및 API 기초 구조 설계
    * **[Design]** Rose-Tech 컬러 팔레트 및 Typography(Pretendard) 기반 UI Kit 제작
    * **[Design]** 공통 컴포넌트(Button, Card, Input, Modal) 디자인

### Phase 2: 핵심 도메인 개발 (Core Implementation) — [Target: 3-5주 차]
* **목표:** 사용자 관리 및 AI 진단 데이터 조회 기능 구현
* **핵심 작업:**
    * **[Dev]** User & DiagnosisReport CRUD API 개발
    * **[Dev]** 진단 데이터(FaceShape, HairType 등) 필터링 로직 구현
    * **[Design]** 데이터 테이블(Table) 및 상세 정보 뷰(Detail View) 레이아웃 설계
    * **[Business]** 프리미엄 리포트 결제/멤버십 상태 관리 로직 검증

### Phase 3: 데이터 시각화 및 대시보드 (Visualization) — [Target: 6-7주 차]
* **목표:** KPI 모니터링을 위한 차트 및 통계 대시보드 완성
* **핵심 작업:**
    * **[Dev]** Chart.js 또는 Recharts를 활용한 Line/Bar/Donut 차트 연동
    * **[Dev]** 매출(MRR) 및 전환율(CVR) 계산용 집계(Aggregation) API 개발
    * **[Design]** Researcher 벤치마킹 기반의 KPI Card 및 Heatmap UI 적용
    * **[Design]** 브랜드 정체성이 반영된 Dashboard 메인 화면 완성

### Phase 4: B2B 네트워크 및 확장 (Expansion) — [Target: 8주 차~]
* **목표:** 제휴 미용실 관리 및 마케팅 기능 활성화
* **핵심 작업:**
    * **[Dev]** Partner 등록/승인 프로세스 및 리퍼럴(Referral) 추적 시스템 구현
    * **[Dev]** 타겟 그룹 대상 푸시/알림톡 발송 기능 연동
    * **[Business]** 파트너 정산 및 마케팅 성과(ROAS) 분석 기능 검토

---

## 3. 작업 체크리스트 (Actionable Checklist)

### 🛠️ Development (개발)
- [ ] `schema.prisma` 정의된 Enum 및 Model 기반 DB Migration 완료
- [ ] `DiagnosisReport`의 JSON 필드(StylePreference, AnalysisResult) 데이터 파싱 로직 구현
- [ ] `Stripe` 스타일의 Global Date Picker 컴포넌트 구현
- [ ] `Mixpanel` 스타일의 사용자 여정(Funnel) 데이터 추출 API 구축
- [ ] API 응답 규격(Error Handling, Pagination) 표준화

### 🎨 Design (디자인)
- [ ] Primary (`#E07A5F`) 및 Secondary (`#F4ACB7`) 컬러 적용된 UI 컴포넌트 라이브러리 제작
- [ ] 데이터 가독성을 위한 High-Contrast Typography 위계 설정
- [ ] 대량의 수치 데이터를 위한 Data Table UI (Sorting, Filtering 포함) 설계
- [ ] 지리적 정보를 위한 지도(Map) UI 컴포넌트 디자인

### 📊 Business & QA (기획/검증)
- [ ] 프리미엄 전환율(CVR) 측정을 위한 핵심 이벤트 로그 설계 확인
- [ ] 제휴 미용실 승인/거절 프로세스 워크플로우 확정
- [ ] 어드민 페이지 내 개인정보(사용자 진단 데이터) 접근 권한(RBAC) 정의

---

📊 평가: 완료 — 모든 에이전트의 산출물을 통합하여 실행 가능한 로드맵과 체크리스트로 구조화함.

📝 다음 단계: 개발팀은 Phase 1의 `Prisma` 스키마 구현 및 프로젝트 환경 설정을 시작하십시오.
