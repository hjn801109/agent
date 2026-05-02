# 🎨 Designer — Admin 페이지의 전체 레이아웃(Glassmorphism, Serif 타이포그래피 적용)과 Rose 톤 컬러 사용에 대한 최종 시각적 가이드라인을 제시해줘.

🎨 Designer: 작업 시작합니다.

## 🖼️ Admin 페이지 최종 시각적 가이드라인 (Glassmorphism & Rose Tone)

Admin 페이지는 '신뢰감'과 '친근함(Rose Tone)'을 기반으로 하면서도 '데이터의 명확성(Clarity)'을 최우선으로 확보하는 것이 핵심 목표입니다. Glassmorphism 기법을 적용하여 깊이감을 주되, 정보 접근성은 극대화해야 합니다.

### 1. 색상 팔레트 (Rose Tone System)

브랜드 정체성인 '로즈 톤'을 중심으로 따뜻함과 전문성을 동시에 확보하는 컬러 시스템입니다.

| 요소 | 역할 | HEX 코드 | 설명 |
| :--- | :--- | :--- | :--- |
| **Primary Rose** | 메인 액센트/CTA (버튼, 활성 상태) | `#E07A5F` | 따뜻하고 친근한 핵심 색상. 사용자의 행동을 유도합니다. |
| **Secondary Rose** | 보조 강조/서브 컬러 | `#F4ACB7` | 배경이나 카드에 부드러운 톤으로 적용하여 깊이를 더합니다. |
| **Glass Background (Light)** | Glassmorphism 기본 배경 | `rgba(255, 255, 255, 0.3)` | 투명도를 활용한 유리 효과의 베이스. |
| **Glass Border/Surface** | 카드 및 패널 경계선 | `rgba(255, 255, 255, 0.15)` | 미묘한 빛 반사와 깊이감을 부여합니다. |
| **Text (Primary)** | 본문 및 핵심 데이터 | `#333333` | 높은 가독성을 위한 진한 회색(Black 대신 사용). |
| **Text (Secondary)** | 보조 정보 및 레이블 | `#6B6B6B` | 부드러운 톤으로 보조 정보를 처리합니다. |

### 2. 타이포그래피 시스템 (Serif & Clarity)

전문성과 친근함을 동시에 전달하기 위해 Serif 계열의 타이포그래피를 사용하며, 데이터 가독성을 확보하는 것이 중요합니다.

*   **Font Family:** **Serif 계열** (예: Playfair Display, Merriweather 또는 유사한 세리프 폰트)
    *   *적용 위치:* 헤더, 섹션 제목, 핵심 데이터 라벨 등 시각적 강조가 필요한 곳에 적용하여 브랜드의 따뜻함을 표현합니다.
*   **Font Family (Body/Data):** **Sans-serif 계열** (예: Inter, Roboto 또는 유사한 산세리프 폰트)
    *   *적용 위치:* 실제 데이터 표(Table), 상세 설정 항목 등 정보 전달이 주 목적인 곳에 적용하여 명확성을 확보합니다.
*   **Hierarchy:**
    *   **H1/H2 (섹션 제목):** Serif 계열, 볼드 처리, 충분한 자간(Letter Spacing) 적용. (브랜드 톤 강조)
    *   **Label/Key:** Sans-serif, 적절한 크기. (명확성 확보)
    *   **Data/Value:** Sans-serif, 높은 대비로 명확하게 표시.

### 3. Glassmorphism 레이아웃 적용 가이드

Admin 페이지의 각 패널(Sidebar, Main Content, Data Cards)에 다음 규칙을 적용합니다.

1.  **배경 처리 (The Glass Effect):**
    *   모든 컨테이너는 반투명한 배경(`rgba(255, 255, 255, 0.3)`)을 사용하며, 경계선은 매우 얇고 희미하게 설정합니다 (`border: 1px solid rgba(255, 255, 255, 0.15);`).
    *   **팁:** 배경색이 너무 어두우면 Glassmorphism 효과가 약해지므로, 메인 배경은 미드톤의 밝은 로즈 톤(`F9F8F7` 등)을 사용하여 전체적인 따뜻함을 유지해야 합니다.

2.  **깊이감 (Depth & Shadow):**
    *   **Soft Shadow:** 부드러운 그림자(Box-shadow)를 사용하여 화면에서 살짝 떠 있는 듯한 입체감을 부여합니다.
        *   `box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);` (매우 은은하고 소프트하게 설정)

3.  **레이아웃 구조:**
    *   **Sidebar/Navigation:** 상대적으로 불투명도를 높여 중요한 내비게이션 요소로 기능하게 합니다. (Glassmorphism의 적용 강도 차등화)
    *   **Data Panels (Cards):** 모든 데이터는 명확한 경계를 가진 카드 형태로 분리하여, 한눈에 정보 구분을 용이하게 합니다. 각 카드는 Secondary Rose 색상을 미묘하게 배경으로 활용할 수 있습니다.

---
📊 평가: 완료 — CEO의 요구사항(Glassmorphism, Serif, Rose Tone 적용)을 구체적인 색상 코드와 레이아웃 원칙으로 명확하게 제시하여 디자인 실행 기반을 마련함.
📝 다음 단계: Admin 페이지에 대한 실제 와이어프레임 및 컴포넌트별 스타일 가이드라인을 세부적으로 작성합니다.
