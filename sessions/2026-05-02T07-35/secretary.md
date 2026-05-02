# 📱 Secretary — MVP 기능 우선순위(초개인화, 전환 유도 구조)에 맞춰 사용자 여정 맵(User Journey Map)을 작성하고, 개발팀이 즉시 구현할 수 있도록 구체적인 단계별 시나리오와 필요한 데이터 흐름을 정리하여 보고하세요.

📱 Secretary: 작업 시작합니다.

## 🗺️ 사용자 여정 맵 및 데이터 흐름 보고서 (MVP 우선순위 기반)

본 보고서는 MVP 핵심 목표인 **초개인화**와 **전환 유도 구조**에 초점을 맞추어, 사용자가 서비스 진입부터 구독 전환까지 경험하는 전체 과정을 시나리오별로 정리하고 개발팀이 즉시 구현할 수 있도록 데이터 흐름을 명시합니다.

---

### 1. 사용자 여정 맵 (User Journey Map) 개요

**목표:** 잠재 고객(스타일 고민자)이 '인지' 단계에서 '구독 전환' 단계까지의 여정을 설계하고, 각 단계별로 초개인화된 경험을 제공하여 이탈률을 최소화합니다.

| 단계 (Stage) | 사용자 목표 (User Goal) | 주요 행동 (Actions) | 핵심 접점 (Touchpoints) | 예상 페인 포인트 (Pain Points) | 기회 영역 (Opportunity) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A. 인지/탐색** | 내 스타일에 대한 객관적인 이해 얻기 | 웹사이트 방문, 무료 진단 요청 | 랜딩 페이지, 스타일 진단 결과 페이지 (Designer 산출물) | 결과가 너무 일반적이거나 복잡함 | 즉각적이고 매력적인 초기 인사이트 제공 |
| **B. 검증/신뢰** | AI의 분석 결과에 신뢰 부여하기 | 상세 데이터 확인, 다른 사용자 비교 | Style Insight 카드, 데이터 시각화 섹션 | 데이터의 깊이가 부족하거나, 전문가 느낌이 약함 | LTV 연관 데이터를 통해 신뢰도 극대화 (Business 산출물 통합) |
| **C. 전환/결정** | 프리미엄 서비스 가치 판단 및 구독 결정 | 가격 비교, 기능 차이 확인 | Tiered Pricing 구조, CTA 버튼 | 어떤 플랜이 나에게 가장 적합한지 모름 | 개인의 니즈에 맞는 맞춤형 패키징 제시 |
| **D. 참여/구독** | 프리미엄 서비스 이용 시작 | 결제 프로세스 완료 및 서비스 사용 시작 | 회원가입/결제 페이지, 온보딩 튜토리얼 | 복잡한 결제 과정 또는 초기 사용의 어려움 | 원활하고 직관적인 온보딩 경험 제공 |

---

### 2. 단계별 상세 시나리오 및 데이터 흐름 (Development Flow)

#### **Stage A: 인지/탐색 (Diagnosis & Discovery)**

**시나리오:** 사용자가 웹사이트에 방문하여 스타일 진단을 요청한다.
**목표:** 최소한의 입력으로 최대의 초기 인사이트를 제공하여 이탈을 방지한다.

| 단계 | 사용자 행동 | 시스템 반응 (UI/UX) | 필요한 데이터 흐름 |
| :--- | :--- | :--- | :--- |
| **A1. 진단 요청** | '스타일 진단 시작' 버튼 클릭 | 입력 필드 제시 (얼굴형, 선호 분위기 등 최소 정보 요구) | `User_Input` $\rightarrow$ `Style_Engine_API` |
| **A2. 초기 분석** | 데이터 처리 대기 | 로딩 애니메이션 및 '당신의 스타일이 분석 중입니다...' 메시지 표시 | `Style_Engine_API` $\rightarrow$ `Raw_Data` |
| **A3. 결과 제시** | 진단 결과 페이지 도착 | Designer 산출물 기반의 Glassmorphism 카드에 결과(Score)와 핵심 인사이트(`Style Insight`) 즉시 노출 | `Raw_Data` + `Brand_Tone` $\rightarrow$ `Result_Page_Render` |
| **A4. 심화 탐색** | 상세 분석 요청 | 데이터 시각화 차트 및 추가 정보 탭 제공 | `Raw_Data` $\rightarrow$ `Visualization_Engine` |

#### **Stage B: 검증/신뢰 (Validation & Trust Building)**

**시나리오:** 사용자가 제시된 결과에 만족하지 못하고, 더 깊은 분석을 원한다.
**목표:** 데이터의 깊이를 제공하여 서비스에 대한 신뢰도를 극대화하고 전환 기회를 포착한다.

| 단계 | 사용자 행동 | 시스템 반응 (UI/UX) | 필요한 데이터 흐름 |
| :--- | :--- | :--- | :--- |
| **B1. 심층 요청** | '프리미엄 리포트 보기' 버튼 클릭 | Tiered Pricing 구조에 따라 프리미엄 기능의 가치(LTV 연관성)를 명확히 설명하는 팝업 제시 | `Current_User_Tier` $\rightarrow$ `Feature_Mapping` |
| **B2. 데이터 비교** | 다른 스타일 결과 혹은 자신의 과거 데이터를 업로드 | 사용자 데이터베이스 검색 및 비교 UI 제공 | `User_History_DB` $\rightarrow$ `Comparison_Engine` |
| **B3. 신뢰 확보** | 보고서 다운로드 시도 | 보안 검증 후, 전문적이고 로즈 톤 기반의 PDF 리포트 생성 | `Final_Report_Template` + `Raw_Data` $\rightarrow$ `PDF_Generator` |

#### **Stage C: 전환/결정 (Conversion & Decision)**

**시나리오:** 사용자가 구독 플랜을 선택하고 결제한다.
**목표:** 가장 적합한 플랜을 명확히 제시하여 구매 결정의 마찰을 최소화한다.

| 단계 | 사용자 행동 | 시스템 반응 (UI/UX) | 필요한 데이터 흐름 |
| :--- | :--- | :--- | :--- |
| **C1. 플랜 선택** | 프리미엄 플랜 선택 | 각 플랜별 제공 기능(Tiered Pricing 정의 기반)을 명확히 비교하는 테이블 제시 | `Pricing_Model` + `User_Profile` $\rightarrow$ `Plan_Selection` |
| **C2. 최종 확인** | 결제 정보 입력 | 보안 및 법적 준수 항목(Privacy Policy 연동)에 대한 동의 체크박스 강조 | `Compliance_Check` (보안 모듈 통합) |
| **C3. 구독 시작** | 결제 완료 | 성공 메시지 및 다음 단계(온보딩) 안내 | `Payment_Gateway_API` $\rightarrow$ `Subscription_Status` |

---

### 3. 핵심 데이터 흐름 요약 (Data Flow Summary)

모든 여정은 **사용자 입력 $\rightarrow$ AI 분석 $\rightarrow$ 비즈니스 모델 매핑 $\rightarrow$ 최종 전환**의 순환 구조를 따릅니다.

1.  **Input Layer:** 사용자 스타일 선호도, 개인 정보 (Stage A1)
2.  **Processing Layer (Core):** Style Engine이 데이터 처리 후, **LTV 기반으로 가중치 부여된 결과(Raw Data)** 생성.
3.  **Mapping Layer (Business Logic):** Raw Data는 Designer/Business 에이전트의 정의에 따라 **Tiered Pricing 구조 및 기능 매핑 정보**와 결합되어 최종 사용자 경험을 결정.
4.  **Output Layer:** 최종적으로 로즈 톤 기반의 시각화(Designer)와 전환 유도 문구(Business)가 결합된 페이지 제공.

이 데이터 흐름은 개발팀이 프론트엔드 컴포넌트와 백엔드 API 엔드포인트를 설계하는 데 필요한 명확한 요구사항을 제공합니다.

📊 평가: 완료 — CEO의 지시 사항에 따라 MVP 기반 사용자 여정 맵, 시나리오 및 데이터 흐름을 구체적으로 정리하여 보고했습니다.
📝 다음 단계: 개발팀에게 전달할 API 스키마와 프론트엔드 컴포넌트 명세를 작성합니다.
