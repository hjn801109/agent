# 🎨 Designer — Writer가 제공한 카피와 앞서 확립된 시각 시스템 가이드라인(Rose Tone, Glassmorphism, 데이터 시각화)을 적용하여 고품질의 Hero Section Mockup을 즉시 제작하세요. LTV 및 Trust Score를 시각적으로 강조해야 합니다.

🎨 Designer: 작업 시작합니다.

## ✨ Hero Section Mockup 디자인 스펙 (최종)

본 Mockup은 Writer가 제공한 카피와 확립된 시각 시스템 가이드라인(Rose Tone, Glassmorphism, 데이터 시각화)을 기반으로, **데이터 기반 신뢰감**을 극대화하는 인터페이스 디자인 사양입니다.

### 1. 시각 시스템 적용 상세

| 요소 | 세부 설정 | 코드/설명 |
| :--- | :--- | :--- |
| **배경 컬러 (Rose Tone)** | 메인 배경 및 그라데이션 베이스 | `#F9E3DD` (밝은 로즈 톤)에서 `#F4ACB7` (약간 더 진한 로즈 톤)으로 부드러운 선형 그라데이션 적용. |
| **Glassmorphism** | 카드, CTA 버튼 배경 처리 | `backdrop-filter: blur(16px);` 및 낮은 불투명도(`opacity: 0.9`); 은은하게 빛나는 테두리 (`border: 1px solid rgba(255, 255, 255, 0.3);`). |
| **타이포그래피** | 헤드라인 및 본문 | Serif 계열 (예: Playfair Display 또는 Lora) 사용. 강조 시 Bold 처리하여 전문성 부여. |
| **데이터 시각화** | Trust Score | Rose Tone 기반의 그라데이션을 활용하여 점수와 신뢰도를 표현. |

### 2. 레이아웃 및 컴포넌트 구조 (Wireframe Blueprint)

**[레이아웃: 중앙 집중형 & 깊이감 강조]**

| 영역 | 내용 | 디자인 적용 방식 |
| :--- | :--- | :--- |
| **A. 헤드라인 영역 (상단)** | Headline (가장 큰 텍스트) | 중앙 정렬, 가장 크고 두꺼운 Serif 폰트 사용. Rose Tone의 밝은 부분에 배치하여 시선 집중. |
| **B. 서브헤드라인 영역** | Subheadline (설명 문구) | 헤드라인 아래에 배치. 약간 작은 크기의 세리프체로 전문성을 유지하며, Glassmorphism 박스 내부에 배치. |
| **C. 핵심 CTA 영역** | Call to Action (버튼) | 중앙에 배치. Rose Tone의 짙은 톤을 사용하여 대비를 주고, 버튼 자체는 은은한 Glassmorphism 효과를 부여하여 클릭 유도. |
| **D. 신뢰 시각화 영역 (핵심)** | Trust Score Visualization | Hero 섹션 중앙 또는 우측에 별도의 Glassmorphism 카드 형태로 배치. LTV와 Trust Score를 그라데이션으로 표현. |

### 3. 상세 컴포넌트 디자인 명세

#### 3.1. 헤드라인 및 서브헤드라인 (Section B & A)

*   **Headline:** 나만을 위한 완벽한 헤어스타일, 이제 AI가 증명합니다.
    *   폰트: Serif Bold, 크기: 64px 이상. 색상: 짙은 로즈 계열 (`#8A495F`).
*   **Subheadline:** 복잡한 고민은 끝! 당신의 피부톤, 모발 상태, 라이프스타일을 AI가 정밀 분석하여 가장 잘 어울리는 스타일을 추천하고, 그 신뢰를 데이터로 보여드립니다.
    *   폰트: Serif Regular, 크기: 18px 내외. 색상: 부드러운 회갈색 (`#6B4E5A`).
    *   **배치:** Headline 바로 아래에 배치하며, 전체 영역을 감싸는 은은한 Rose Tone 배경 위에 Glassmorphism 카드 형태로 구성.

#### 3.2. Trust Score 시각화 컴포넌트 (Section D - 가장 중요)

이 컴포넌트는 데이터 기반 신뢰를 시각적으로 증명하는 핵심 요소입니다.

*   **컴포넌트 형태:** 직사각형 또는 원형의 Glassmorphism 카드.
*   **데이터 표시:**
    *   **Trust Score:** `92%` (가장 크고 굵게 표시).
    *   **Label:** '스타일 만족도' 또는 '데이터 신뢰도'.
    *   **시각화 기법:** Trust Score를 표현하는 배경에 Rose Tone의 그라데이션을 적용하여 데이터 자체에서 깊이감을 느끼게 합니다. (예: 92%가 높은 곳은 더 밝고 따뜻한 로즈톤으로, 낮은 곳은 약간 어두운 톤으로 그라데이션 처리).
*   **추가 정보:** 하단에 작은 글씨로 "LTV 기반 정밀 분석 완료" 문구를 추가하여 데이터의 근거를 제시합니다.

#### 3.3. Call to Action (CTA) 버튼

*   **텍스트:** 나만의 스타일 진단받기 (무료 시작)
*   **스타일:** 배경은 Rose Tone의 가장 깊은 색상(`#8A495F`)을 사용하며, 마우스 오버 시 미세하게 밝아지는 Glassmorphism 효과를 부여합니다. 버튼의 그림자(Shadow)는 부드러운 로즈톤 그라데이션으로 처리하여 친근함을 유지합니다.

### 4. 최종 레이아웃 요약 (Flow)

1.  **상단:** Headline (최대 강조)
2.  **중앙 상단:** Subheadline + Trust Score 시각화 카드 (신뢰도 즉시 제시)
3.  **중앙 하단:** CTA 버튼 (행동 유도)

---
📊 평가: 완료 — 요청된 모든 카피와 디자인 원칙을 기반으로 실행 가능한 상세 Mockup 스펙이 제공되었습니다.
📝 다음 단계: Figma 내에서 위 명세를 바탕으로 시각 디자인 초안(Wireframe/Mockup) 제작에 착수합니다.
