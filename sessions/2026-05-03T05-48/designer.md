# 🎨 Designer — Business팀이 정의한 'Trust Score'를 Glassmorphism 디자인 요소로 시각화하는 핵심 컴포넌트의 목업(Mockup)을 즉시 제작하여 신뢰감을 극대화할 것. Rose Tone과 데이터 그라데이션을 활용하여 전문성을 표현할 것.

🎨 Designer: 작업 시작합니다.

## Trust Score 시각화 컴포넌트 목업 디자인 브리프

CEO 지시에 따라 'Trust Score'를 Glassmorphism, Rose Tone, 데이터 그라데이션을 활용하여 신뢰감을 극대화하는 핵심 컴포넌트를 아래와 같이 구체적으로 설계합니다. 이 가이드라인은 즉시 Figma 구현에 사용될 수 있습니다.

### 1. 디자인 시스템 재확인 (Reference)

*   **컬러 팔레트 (Rose Tone 기반):**
    *   Primary Rose: `#E07A5F` (메인 강조색, 따뜻한 느낌)
    *   Secondary Accent: `#F4ACB7` (보조 배경/그라데이션 시작점)
    *   Background Base: `#FFFFFF` (Glassmorphism의 투명도를 극대화하기 위함)
    *   Shadow/Border: `rgba(255, 255, 255, 0.3)` (미세한 하이라이트 및 블러 효과를 위한 투명도 설정)

*   **타이포그래피:**
    *   Score Text: Serif 계열 (예: Playfair Display 또는 Lora) - 전문성과 클래식함을 부여합니다.

*   **Glassmorphism 속성:**
    *   Blur Radius: `16px` (개인 메모리 기반 설정 적용)
    *   Background: 반투명(Opacity 85%)의 Rose Tone 그라데이션 배경.

### 2. Trust Score 컴포넌트 상세 목업 (Mockup Specification)

#### A. 컴포넌트 명칭: Data-Driven Trust Meter

#### B. 레이아웃 및 구조 (Layout & Structure)

| 요소 | 속성 | 값/설명 |
| :--- | :--- | :--- |
| **컨테이너** | 크기 | W: 400px, H: 250px (예시) |
| **배경** | 스타일 | Glassmorphism 적용. 배경은 Rose Tone 계열의 부드러운 그라데이션. |
| **Score Display** | 중앙 정렬 | `Trust Score` 텍스트가 가장 크게 표시됨. |
| **Visualization** | 핵심 시각화 | 원형 게이지 또는 바(Bar) 형태의 데이터 흐름 강조. |

#### C. 시각적 구현 상세 (Visual Implementation Details)

1.  **Glassmorphism 효과:**
    *   컨테이너에 `backdrop-filter: blur(16px);`를 적용하여 배경이 흐릿하게 보이도록 처리합니다.
    *   경계선(Border)은 매우 얇고 밝은 Rose Tone으로 설정하여 미니멀함을 유지합니다.

2.  **데이터 그라데이션 활용:**
    *   스코어 바(Meter)의 채움 정도에 따라 색상이 변화하는 **그라데이션**을 적용합니다. (신뢰도가 높을수록 깊고 따뜻한 로즈 톤으로 변화)

3.  **텍스트 및 레이블:**
    *   **최상단 제목:** `Trust Score` (Serif 폰트, 굵게, 색상: `#E07A5F`)
    *   **스코어 값:** 가장 중앙에 크게 표시. (예: **88점**)
    *   **추가 설명:** 점수 아래에 데이터 기반의 신뢰감을 강조하는 문구를 배치합니다.

#### D. 최종 Mockup 레이아웃 예시 (Textual Representation)

```markdown
[Glassmorphism Container Start]
  |---------------------------------------|
  | [Trust Score] (Serif Bold, #E07A5F)   |  <- 상단 제목
  |                                       |
  |       [ 88 ]                         |  <- 핵심 점수 표시 (가장 크게)
  |                                       |
  |  [데이터 그라데이션 바 시각화]         |  <- Glassmorphism 채움 영역
  |  (Rose Tone Gradient: #F4ACB7 -> #E07A5F) |
  |                                       |
  | "당신의 선택은 신뢰를 만듭니다." (Serif Light) | <- 신뢰감 강조 문구
[Glassmorphism Container End]
```

### 3. 디자인 가이드라인 요약 (Design Guideline Summary)

*   **핵심 원칙:** 데이터(Score)는 감성(Rose Tone)과 투명성(Glassmorphism)을 통해 전달되어야 한다.
*   **활용:** 이 컴포넌트는 단순히 점수를 보여주는 것이 아니라, 사용자가 자신의 선택이 얼마나 신뢰할 만한지 **시각적으로 체험**하게 만드는 인터페이스여야 합니다.
*   **적용 범위:** 웹사이트의 핵심 리포트 페이지, 어드민 대시보드의 KPI 섹션에 우선 적용합니다.

📊 평가: 완료 — CEO 지시에 따라 Trust Score를 Glassmorphism과 Rose Tone으로 시각화하는 핵심 컴포넌트 목업 디자인 브리프를 구체적으로 제작했습니다.
📝 다음 단계: 실제 Figma 환경에서 위에 제시된 사양을 기반으로 Trust Score 컴포넌트를 즉시 프로토타입으로 구현합니다.
