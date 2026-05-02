# 🎨 Designer — 확립된 Rose 톤, Glassmorphism, Serif 타이포그래피 가이드라인을 적용하여, Writer가 작성한 문구를 포함한 회원가입(Signup) 페이지와 하단(Footer) UI 디자인 초안을 설계하세요.

🎨 Designer: 작업 시작합니다.

# 🎨 UI Design Draft: Signup & Footer

본 설계안은 확립된 **Rose Tone**, **Glassmorphism**, **Serif Typography** 가이드를 기반으로, Writer가 작성한 문구를 시각적 위계에 맞춰 배치한 디자인 초안입니다.

---

## 1. Visual Identity System (Design Foundation)

*   **Color Palette**
    *   **Primary (Rose):** `#E07A5F` (Deep Rose - CTA 및 강조 포인트)
    *   **Secondary (Soft Rose):** `#F4ACB7` (Light Rose - 배경 그라데이션 및 서브 요소)
    *   **Surface (Glass):** `rgba(255, 255, 255, 0.4)` (Frosted Glass 효과를 위한 반투명 화이트)
    *   **Text (High Contrast):** `#2D2D2D` (Deep Charcoal - 가독성 확보)
*   **Typography**
    *   **Heading (Serif):** `Playfair Display` (우아함과 전문성 전달, 제목 및 Hook에 사용)
    *   **Body/UI (Sans-serif):** `Pretendard` (높은 가독성, 입력창 및 본문에 사용)
*   **Visual Effect**
    *   **Glassmorphism:** `backdrop-filter: blur(16px) saturate(180%);` 적용
    *   **Border:** `1px solid rgba(255, 255, 255, 0.3)` (유리 질감의 경계선)

---

## 2. Signup Page UI Design (Layout & Components)

### [Layout Concept: The Ethereal Entrance]
화면 중앙에 부드러운 Rose 톤의 그라데이션이 흐르는 배경을 배치하고, 그 위에 Glassmorphism이 적용된 카드 레이아포맷을 띄워 몰입감을 극대화합니다.

#### **A. Background Layer**
*   **Visual:** `#F4ACB7`에서 `#FDF0F0`로 이어지는 부드러운 대각선 그라데이션.
*   **Element:** 흐릿한(Blurred) 형태의 유기적 곡선 오브젝트를 배경에 배치하여 깊이감 부여.

#### **B. Main Glass Card (Center Container)**
*   **Properties:** `width: 480px`, `padding: 40px`, `border-radius: 24px`, `background: rgba(255, 255, 255, 0.45)`, `backdrop-filter: blur(20px)`.
*   **Content Structure:**
    1.  **Logo:** 상단 중앙 `midmi` 로고 (Serif 폰트 적용).
    2.  **Hero Text (Writer's Option 1 적용):**
        *   **Hook (Serif):** "미용실 가기 전, 거울 보며 한숨 쉬어본 적 있지 않나요? 💇‍♀️" (Size: 24px, Weight: 700, Color: `#2D2D2D`)
        *   **Body (Sans-serif):** "AI가 당신의 얼굴형과 피부톤을 정밀하게 분석해, '인생 스타일' 리포트를 선물해 드릴게요." (Size: 16px, Color: `#555555`, Line-height: 1.6)
    3.  **Input Fields (Glass UI):**
        *   **Style:** `background: rgba(255, 255, 255, 0.6)`, `border: 1px solid rgba(224, 122, 95, 0.2)`, `border-radius: 12px`.
        *   **Fields:** 이메일, 비밀번호, 이름 입력란.
    4.  **CTA Button (Primary Action):**
        *   **Text:** "지금 바로 나만의 스타일 DNA 확인하기 (무료)"
        *   **Style:** `background: #E07A5F`, `color: #FFFFFF`, `font-weight: 600`, `box-shadow: 0 8px 20px rgba(224, 122, 95, 0.3)`.
    5.  **Secondary Link:** "이미 계정이 있으신가요? 로그인하기" (Text-decoration: underline).

---

## 3. Footer UI Design (Information Hierarchy)

### [Layout Concept: The Professional Foundation]
페이지 최하단에 위치하며, 브랜드의 신뢰도를 높이기 위해 명확한 그리드와 가독성 높은 텍표 레이아웃을 사용합니다.

#### **A. Footer Container**
*   **Properties:** `width: 100%`, `padding: 60px 20px`, `background: rgba(255, 255, 255, 0.2)`, `border-top: 1px solid rgba(224, 122, 95, 0.1)`.

#### **B. Information Grid (3-Column Layout)**
1.  **Column 1: Brand Identity**
    *   **Logo
