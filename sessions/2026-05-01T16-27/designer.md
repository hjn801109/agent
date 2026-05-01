# 🎨 Designer — 정의된 API 응답 데이터(StyleAnalysisResponse)를 기반으로, 사용자가 자신의 스타일을 한눈에 파악할 수 있는 '스타일 DNA 리포트'의 UI/UX 와이어프레임과 시각적 컨셉을 설계하세요.

🎨 Designer: 작업 시작합니다.

# [Design Specification] 스타일 DNA 리포트 UI/UX 설계안

본 설계안은 `StyleAnalysisResponse` 데이터를 시각적 가치로 변환하여, 사용자가 자신의 특징을 '발견'하고 '신뢰'할 수 있는 **"Premium Magazine Dashboard"** 컨셉을 지향합니다.

---

## 1. Visual Concept: "The Beauty Blueprint"
*   **Concept Keyword:** 정밀한(Precise), 우아한(Elegant), 따뜻한(Warm)
*   **Design Direction:** 데이터 중심의 대시보드 레이아웃에 잡지(Magazine)의 감성적인 타이포그래피와 로즈 톤의 부드러운 컬러를 결합하여, 단순한 결과값이 아닌 '나를 위한 특별한 리포트'라는 경험을 제공합니다.

---

## 2. Visual System (Design Tokens)

### 🎨 Color Palette
*   **Primary (Rose Identity):** `#E9967A` (Deep Rose) - 강조 포인트, 핵심 분석 결과
*   **Secondary (Soft Warmth):** `#FFF5F5` (Soft Shell) - 카드 배경, 섹션 구분
*   **Accent (Trust):** `#4A4A4A` (Charcoal) - 텍스트 가독성, 전문성 확보
*   **Neutral (Base):** `#FFFFFF` (Pure White) - 기본 배경
*   **Status (Analysis):** `#FFB6C1` (Light Pink) - 진행 중 또는 부드러한 강조

### 🔡 Typography
*   **Heading (Title):** `Pretendard Bold` - 정보의 위계 설정 및 가독성
*   **Sub-heading (Label):** `Pretendard Medium` - 데이터 라벨링
*   **Body (Description):** `Pretendard Regular` - 상세 설명 및 팁
*   **Accent (Decorative):** `Playfair Display` (Serif) - 리포트 상단 타이틀 등 감성적 요소 (영문 전용)

---

## 3. UI/UX Wireframe (Structure & Layout)

리포트는 상단에서 하단으로 **[Identity $\rightarrow$ Analysis $\rightarrow$ Solution $\rightarrow$ Guide]** 순서로 흐릅니다.

### [Section 1: Hero Header - "The Identity"]
*   **Layout:** 상단 중앙 정렬 (Center Aligned)
*   **Content:**
    *   `Text`: "Hello, [User Name]! 당신의 아름다움이 발견되었습니다." (Playfair Display, Italic)
    *   `Visual`: 사용자의 분석 완료를 상징하는 로즈 톤의 추상적인 그래픽 애니메이션.

### [Section 2: Core DNA - "Face & Color"]
*   **Layout:** 2-Column Card Layout (좌: 얼굴형 / 우: 퍼스널 컬러)
*   **Component:**
    *   **Card A (Face Shape):** `faceShape` 데이터를 텍mat 텍스트와 함께 얼굴형을 형상화한 미니멀한 라인 아이콘으로 표시.
    *   **Card B (Personal Color):** `personalColor` 데이터를 해당 톤을 상징하는 컬러 스와치(Large Circle)와 명칭으로 표시.
    *   **Interaction:** 카드 터치 시 해당 톤에 어울리는 메이크업/헤어 팁 팝업.

### [Section 3: Detailed Analysis - "Hair Profile"]
*   **Layout:** Vertical List with Progress Bars
*   **Component:**
    *   **Hair Texture/Volume:** `hairTexture`, `hairVolume` 데이터를 수평 프로그레스 바(Progress Bar) 형태로 시각화. (예: 굵기 - [|||||||---] 70%)
    *   **Visual Style:** 로즈 톤의 부드러운 바(Bar)를 사용하여 딱딱한 수치 느낌을 제거.

### [Section 4: Curated Solution - "Recommended Styles"]
*   **Layout:** Horizontal Scrollable Card Carousel
*   **Component:**
    *   **Card Item:** `recommendedStyles` 배열의 각 항목을 대형 이미지 카드로 구성.
    *   **Overlay:** 이미지 하단에 스타일 명칭과 '이 스타일을 추천하는 이유(Reasoning)'를 반투명한 로즈 톤 레이어로 표시.
    *   **Action:** "이 스타일 예약하기" 버튼 (Primary Color 적용).

### [Section 5: Maintenance Guide - "Expert's Tip"]
*   **Layout:** Full-width Box (Soft Beige Background)
*   **Content:**
    *   `Icon`: 전문성을 상징하는 미용사 아이콘.
    *   `Text`: `maintenanceTips` 데이터를 불렛 포인트로 정리. "전문가가 전하는 오늘의 관리법"

---

## 4. Implementation Guide (For Developers)

| Element | CSS Property / Value | Note |
| :--- | :--- | :--- |
| **Card Border Radius** | `24px` | 부드럽고 친근한 인상 |
| **Card Shadow** | `0 8px 30px rgba(233, 150, 122, 0.15)` | 로즈 톤이 가미된 은은한 그림자 |
| **Section Spacing** | `padding: 40px 20px;` | 여백을 통한 고급
