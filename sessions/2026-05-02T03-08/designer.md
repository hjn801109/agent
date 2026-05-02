# 🎨 Designer — 결정된 브랜드 가이드(Rose 톤, Glassmorphism, Serif 타이포그래피)를 적용하여 Admin 페이지의 핵심 UI 컴포넌트 및 대시보드 디자인 시스템을 설계하세요.

🎨 Designer: 작업 시작합니다.

# 💎 Admin Dashboard Design System: "Rose Clarity"

Admin 페이지는 브랜드의 **Rose 톤**을 유지하되, 대량의 데이터를 관리해야 하는 특성상 **Clarity(명확성)**를 최우선으로 합니다. Glassmorphism을 통해 고급스러운 레이어감을 부여하고, Serif 타이포그래피로 전문적인 권위를 부여합니다.

## 1. Visual Identity System

### 🎨 Color Palette (Rose & High-Contrast)
데이터 가독성을 위해 배경은 투명도가 있는 밝은 톤을 사용하고, 강조점은 Rose 톤을 사용합니다.

*   **Primary (Brand):** `#E07A5F` (Deep Rose - 버튼, 활성 상태)
*   **Secondary (Accent):** `#F4ACB7` (Soft Rose - 강조 그래픽, 그래프)
*   **Surface (Glass):** `rgba(255, 255, 255, 0.6)` (Glassmorphism Card 배경)
*   **Background:** `#FFF8F7` (매우 연한 Rose 톤의 Base 배경)
*   **Text (Primary):** `#2D2D2D` (Charcoal - 높은 가독성)
*   **Text (Secondary):** `#6B7280` (Muted Grey - 부가 정보)
*   **Status (Enum-based):**
    *   `Active`: `#4ADE80` (Green)
    *   `Pending`: `#FBBF24` (Amber)
    *   `Expired/Canceled`: `#F87171` (Red)

### 🖋️ Typography (Serif & Sans-serif)
*   **Heading (Serif):** `Playfair Display` 또는 `Noto Serif KR`
    *   사용처: Dashboard Title, Section Header, Metric Label
    *   특징: 우아함과 전문성 전달
*   **Body & Data (Sans-serif):** `Pretendard` 또는 `Inter`
    *   사용처: Table Data, Button Text, Input, Navigation
    *   특징: 수치 데이터의 높은 가독성 확보

## 2. UI Component Specification

### 🧊 Glassmorphism Card (The Core Element)
모든 위젯과 섹션은 유리 질감을 가집니다.
*   **Properties:**
    *   `background: rgba(255, 255, 255, 0.6)`
    *   `backdrop-filter: blur(12px) saturate(180%)`
    *   `border: 1px solid rgba(255, 255, 255, 0.3)`
    *   `border-radius: 16px`
    *   `box-shadow: 0 8px 32px 0 rgba(224, 122, 95, 0.1)`

### 🔘 Button System
*   **Primary Button:**
    *   `background: linear-gradient(135deg, #E07A5F 0%, #F4ACB7 100%)`
    *   `color: #FFFFFF`
    *   `font-weight: 600`
*   **Ghost Button (Secondary):**
    *   `background: transparent`
    *   `border: 1px solid #E07A5F`
    *   `color: #E07A5F`

### 📊 Data Badges (Enum Integration)
Developer가 정의한 `SubscriptionStatus` Enum을 시각화합니다.
*   **Style:** Pill shape, Low opacity background + High opacity text.
    *   `Active`: `bg: rgba(74, 222, 128, 0.2)`, `text: #166534`
    *   `Expired`: `bg: rgba(248, 113, 113, 0.2)`, `text: #991B1B`

## 3. Dashboard Layout Concept

### 📐 Grid Structure
*   **Sidebar:** `width: 280px`, Glassmorphism 적용, Serif Font Navigation.
*   **Main Content Area:**
    *   **Top Row (KPI Widgets):** 4개의 Glass Card (Total Users, New Signups, LTV, Active Subscriptions).
    *   **Middle Row (Main Charts):** 2개의 대형 Card (User Growth Line Chart, Revenue Bar Chart).
    *   **Bottom Row (Data Table):** 1개의 넓은 Card (Recent Transactions/User Logs Table).

### 📍 Component Coordinate Example (Dashboard Widget)
*   **Widget: "LTV Overview"**
    *   `Position: Top-Row, 3rd Slot`
    *   `Title: Serif, 18px, #2D2D2D`
    *   `Value: Sans-serif, 32px, #E07A5F`
    *   `Trend Indicator: Small Rose Arrow Up/Down`

📊 평가: 완료 — Admin 페이지를 위한 구체적인 컬러, 타이포그래피, 컴포넌트 가이드라인을 설계함
📝 다음 단계: 대기 — Developer가 설계된 디자인 시스템(Glassmorphism, Color Palette)을 기반으로 UI 컴포넌트(React/Next.js) 구현 시작
