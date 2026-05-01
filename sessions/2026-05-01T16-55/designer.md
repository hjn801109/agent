# 🎨 Designer — 브랜드 아이덴티티(로즈 톤, 전문적이지만 친근한 느낌)를 유지하면서, 대량의 데이터를 가독성 있게 보여줄 수 있는 어드민 대시보드 UI/UX 디자인 브리프를 작성하라.

🎨 Designer: 작업 시작합니다.

# 📊 [Design Brief] midmi Admin Dashboard: "Rose-Tech Clarity"

본 브리프는 미드미(midmi)의 브랜드 정체성인 **'로즈 톤의 따님함'**과 어드민의 필수 기능인 **'데이터의 전문적 가독성'**을 결합한 UI/UX 설계 가이드입니다.

---

## 1. 디자인 컨셉: "Rose-Tech Clarity"
- **Core Concept**: 따뜻한 브랜드 컬러(Rose)를 포인트로 사용하되, 정보의 위계(Hierarchy)를 명확히 하여 데이터의 노이즈를 최소화한 **'Soft-Professional'** 스타일.
- **Visual Strategy**: 
    - **Warmth**: 로즈 톤을 상태값(Status), 강조 포인트, 핵심 지표(KPI)에 적용하여 브랜드 일관성 유지.
    - **Clarity**: 넓은 여백(Whitespace)과 고대비 타이포그래피를 통해 대량의 수치 데이터 가독성 극대화.

## 2. 비주얼 시스템 (Design Tokens)

### 🎨 Color Palette (Rose-Infused System)
| 구분 | Hex Code | 용도 | 비고 |
| :--- | :--- | :--- | :--- |
| **Primary (Brand)** | `#E07A5F` | 핵심 버튼, 활성화 상태, 주요 차트 라인 | 로즈 톤의 중심 |
| **Secondary (Accent)** | `#F4ACB7` | 보조 지표, 하이라이트, 부드러운 배경 요소 | 친근함 부여 |
| **Background (Base)** | `#F8F9FA` | 대시보드 전체 배경 | 눈의 피로도 감소 |
| **Surface (Card)** | `#FFFFFF` | 개별 데이터 카드, 모달, 테이블 배경 | 레이어 분리 |
| **Text (Primary)** | `#2D3436` | 제목, 핵심 수치, 본문 텍스트 | 높은 가독성 |
| **Text (Secondary)** | `#636E72` | 설명문, 날짜, 비활성 데이터 | 정보 위계 형성 |
| **Semantic (Success)** | `#27AE60` | 결제 완료, 승인됨, 활성 상태 | 신뢰감 |
| **Semantic (Error)** | `#D63031` | 결제 실패, 거절됨, 오류 | 경고 |

### 🔡 Typography (Hierarchy)
- **Font Family**: `Pretendard` (Sans-serif) — 가독성과 현대적 감각의 표준.
- **Scale**:
    - **Display (KPI)**: `32px / Bold` — 대시보드 상단 핵심 수치.
    *   **Heading (Card Title)**: `18px / Semi-bold` — 각 섹션의 제목.
    *   **Body (Table/Text)**: `14px / Regular` — 데이터 리스트 및 상세 내용.
    *   **Caption (Metadata)**: `12px / Medium` — 날짜, 단위, 보조 설명.

## 3. UI/UX 레이아웃 및 컴포넌트 전략

### 📐 Layout Structure (Grid System)
- **Navigation**: 좌측 고정 사이드바 (Width: `260px`, Color: `#FFFFFF`, Border-right: `1px solid #E9ECEF`).
- **Global Header**: 상단 고정 (Height: `70px`), Global Date Picker 및 알림 센터 포함.
- **Main Content**: `12-Column Grid` 기반의 카드형 레이아웃.

### 🧩 Key Component Design

#### ① KPI Summary Cards (Top Layer)
- **Design**: 화이트 카드(`Border-radius: 12px`)에 로즈 톤의 **Sparkline(미니 라인 차트)**을 배경에 은은하게 배치.
- **Interaction**: 마우스 호버 시 `Box-shadow: 0 10px 20px rgba(224, 122, 95, 0.1)` 적용.

#### ② Data Table (Middle Layer)
- **Structure**: `Zebra Striping` (행 간격 배경색 차이) 대신 `Border-bottom: 1px solid #F1F3F5` 사용으로 깔끔함 유지.
- **Status Badges**: 
    - `Premium`: Background `#F4ACB7` (Light Rose) / Text `#E07A5F` (Deep Rose).
    - `Partner Approved`: Background `#D1FAE5` / Text `#059669`.
- **Alignment**: 수치 데이터는 `Right-aligned`, 텍스트 데이터는 `Left-aligned`로 정렬하여 비교 용이성 확보.

#### ③ Advanced Filtering (Control Layer)
- **UI**: 드롭다운(Dropdown) 및 멀티 셀렉트(Multi-select) 컴포넌트.
- **Visual**: 선택된 필터는 `Primary Color (#E07A5F)`의 작은 점(Dot) 또는 테두리로 표시하여 현재 적용된 필터 상태를 즉각 인지하게 함.

## 4. 디자인 레퍼런스 가이드 (Implementation Reference)
- **Layout Pattern**: Stripe의 깔끔한 데이터 그리드 + Shopify의 직관적인 KPI 카드.
- **Visual Vibe**: 매거진(Magazine) 스타일의 여백 활용 + 금융 앱의 정밀한 수치 표현.

📊 평가: 완료 — 어드민 페이지의 브랜드 아이덴티티와 기능적 요구사항을 모두 충족하는 구체적인 디자인 가이드를 작성함.

📝 다음 단계: 디자인 가이드를 바탕으로 Figma를 활용한 High-Fidelity 프로토타입 제작 시작.
