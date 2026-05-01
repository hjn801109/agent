# 🎨 Designer — 브랜드 컬러(#E07A5F, #F4ACB7)와 고대비 타이포그래피를 적용한 디자인 시스템(UI Kit) 설계 및 컴포넌트 가이드라인 제작

🎨 Designer: 작업 시작합니다.

# 🎨 midmi Design System (UI Kit) 설계안: "Rose-Tech Magazine"

본 설계안은 CEO의 지시사항(고대비 타이포그래피 및 지정 컬러 적용)과 Researcher의 분석(Glassmorphism, Magazine Layout)을 결합하여, **'전문적인 AI 기술력'**과 **'친근한 뷰티 매거진'**의 감각을 동시에 구현하는 것을 목표로 합니다.

## 1. Visual Foundation (기초 시스템)

### 🎨 Color Palette (Rose-Tone & High Contrast)
단순한 색상 나열이 아닌, 역할(Role)에 따른 명확한 사용 가이드를 정의합니다.

| 구분 | Hex Code | 역할 및 사용처 |
| :--- | :--- | :--- |
| **Primary (Main)** | `#E07A5F` | 핵심 액션(CTA), 브랜드 강조 포인트, 로고 |
| **Secondary (Sub)** | `#F4ACB7` | 보조 강조, 카드 배경, 부드러운 영역 구분 |
| **Contrast (Text)** | `#3D405B` | **고대비 타이포그래피용**. 헤드라인 및 본문 핵심 텍스트 |
| **Surface (Bg)** | `#FFFFFF` | 기본 배경, 깨끗한 화이트 스페이스 확보 |
| **Glass (Overlay)** | `rgba(255, 255, 255, 0.6)` | Glassmorphism 효과를 위한 반투명 레이어 |
| **Semantic (Error)** | `#E63946` | 오류 메시지, 경고 알림 |

### 🔡 Typography System (Editorial Style)
매거진의 권위와 AI의 명확성을 위해 Serif와 Sans-serif를 혼용합니다.

*   **Heading (Serif):** `Playfair Display` (또는 프리미엄 명조 계열)
    *   `H1`: 48px / Bold / `#3D405B` (메인 타이틀, 서비스 슬로건)
    *   `H2`: 32px / SemiBold / `#3D405B` (섹션 헤더, 리포트 제목)
    *   `H3`: 24px / Medium / `#E07A5F` (서브 섹션, 강조 문구)
*   **Body (Sans-serif):** `Pretendard` (가독성 최우선)
    *   `Body 1`: 16px / Regular / `#3D405B` (리포트 상세 내용, 설명문)
    *   `Body 2`: 14px / Regular / `#555555` (캡션, 부가 정보)
    *   `Label`: 12px / Bold / `#E07A5F` (태그, 배지, 카테지 레이블)

---

## 2. Core Component Library (컴포넌트 가이드라인)

### 🔘 Buttons (Action)
*   **Primary Button:** 
    *   `Background: #E07A5F` | `Text: #FFFFFF` | `Radius: 8px`
    *   `Effect`: 클릭 시 미세한 Scale Down (0.98x)
*   **Secondary Button (Glass):** 
    *   `Background: rgba(244, 172, 183, 0.2)` | `Border: 1px solid #F4ACB7` | `Text: #E07A5F`
*   **Ghost Button:** 
    *   `Background: Transparent` | `Text: #3D405B` | `Underline: 1px solid #E07A5F`

### 🗂️ Cards (Magazine Layout)
*   **Style:** `Glassmorphism` 적용
*   **Properties:**
    *   `Background`: `rgba(255, 255, 255, 0.7)`
    *   `Blur`: `Backdrop-filter: blur(10px)`
    *   `Border`: `1px solid rgba(255, 255, 255, 0.3)`
    *   `Shadow`: `0 8px 32px rgba(224, 122, 95, 0.1)` (Rose-tone 그림자)
*   **Usage:** AI 진단 결과 카드, 추천 헤어스타일 프리뷰 카드

### 🏷️ Badges & Tags (Information)
*   **Type A (Point):** `Background: #F4ACB7` | `Text: #FFFFFF` (강조할 키워드)
*   **Type B (Neutral):** `Background: #F1F1F1` | `Text: #3D405B` (일반 카테고리)

---

## 3. Design Implementation Strategy (실행 전략)

1.  **Grid System:** 12-Column Grid (Desktop), 4-Column Grid (Mobile)를 사용하여 매거진 특유의 비대칭적 배치를 가능케 함.
2.  **Visual Hierarchy:** `#3D405B`의 굵은 타이포그래피로 시선을 먼저 끈 뒤, `#E07A5F`로 사용자의 클릭을 유도하는 흐름 구축.
3.  **Spacing:** 8px 단위의 배수 시스템(8, 16, 24, 32...)을 적용하여 컴포넌트 간의 일관된 여백(Whitespace) 유지.

📊 평가: 완료 — 요청된 컬러와 타이포그래피 규칙을 반영한 구체적인 UI Kit 설계안을 도출함
📝 다음 단계: Designer — 설계된 가이드라인을 바탕으로 Figma 컴포넌트 제작 및 프로토타입 작업 시작
