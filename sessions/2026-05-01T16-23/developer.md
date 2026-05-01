# 💻 Developer — Writer가 정의한 변수 리스트를 바탕으로, Next.js 엔진에서 활용할 수 있는 JSON 데이터 스키마(Schema) 구조를 설계하고, 입력 데이터를 처리하기 위한 API 응답 규격을 초안 작성하세요.

💻 Developer: 작업 시작합니다.

Writer가 설계한 '스타일 DNA' 변수를 기반으로, Next.js(TypeScript) 환경에서 즉시 사용할 수 있는 데이터 스키마와 API 명세서를 설계했습니다. 이 구조는 향후 AI 모델(LLM)의 프롬프트 입력값과 프론트엔드 UI 렌더링의 기준점이 됩니다.

---

## 1. TypeScript Data Schema (`types/style.ts`)

데이터의 무결성을 위해 `enum`과 `interface`를 사용하여 엄격하게 정의합니다.

```typescript
// 1. 기초 데이터 타입 정의
export type FaceShape = 'oval' | 'round' | 'angular' | 'long' | 'heart' | 'inverted-triangle';
export type SkinToneType = 'warm' | 'cool' | 'neutral';
export type SkinBrightness = 'light' | 'medium' | 'dark';
export type HairThickness = 'fine' | 'medium' | 'thick';
export type CurlPattern = 'straight' | 'wavy' | 'curly' | 'coily';
export type HairDensity = 'low' | 'medium' | 'high';
export type HairDamage = 'healthy' | 'dry' | 'damaged';
export type Vibe = 'lovely' | 'chic' | 'casual' | 'formal' | 'hip' | 'classic';
export type MaintenanceLevel = 'low' | 'medium' | 'high';

// 2. 입력 데이터 스키마 (User Input)
export interface UserStyleInput {
  face: {
    shape: FaceShape;
    skinTone: {
      type: SkinToneType;
      brightness: SkinBrightness;
    };
    features: {
      eyeFocus: string; // 예: "deep eyes"
      noseHeight: string; // 예: "high bridge"
      lipThickness: string; // 예: "full lips"
    };
  };
  hair: {
    thickness: HairThickness;
    pattern: CurlPattern;
    density: HairDensity;
    damage: HairDamage;
  };
  lifestyle: {
    desiredVibe: Vibe[];
    maintenance: MaintenanceLevel;
    environment: string; // 예: "office", "artistic"
  };
  accessories: {
    hasGlasses: boolean;
    fashionStyle: string[];
  };
}

// 3. AI 분석 결과 스키마 (AI Response)
export interface StyleAnalysisResponse {
  userId: string;
  timestamp: string;
  summary: {
    keywords: string[];
    score: number; // 0.0 ~ 5.0
    coreIdentity: string;
  };
  detailedAnalysis: {
    faceAnalysis: string;
    hairAnalysis: string;
    lifestyleCompatibility: string;
  };
  recommendations: {
    hairStyles: Array<{
      name: string;
      reason: string;
      imagePrompt: string; // 이미지 생성 AI(DALL-E/Midjourney)용 프롬프트
    }>;
    hairColors: Array<{
      colorName: string;
      reason: string;
    }>;
    maintenanceTips: string[];
  };
}
```

---

## 2. API 명세서 (API Specification)

### `POST /api/v1/analyze-style`

**Description:** 사용자의 스타일 입력 데이터를 받아 AI 엔진을 통해 스타일 DNA 리포트를 생성합니다.

**Request Body (`UserStyleInput`):**
```json
{
  "face": {
    "shape": "heart",
    "skinTone": { "type": "warm", "brightness": "medium" },
    "features": { "eyeFocus": "large", "noseHeight": "medium", "lipThickness": "thin" }
  },
  "hair": {
    "thickness": "medium",
    "pattern": "wavy",
    "density": "high",
    "damage": "healthy"
  },
  "lifestyle": {
    "desiredVibe": ["chic", "classic"],
    "maintenance": "medium",
    "environment": "professional office"
  },
  "accessories": {
    "hasGlasses": true,
    "fashionStyle": ["minimal", "feminine"]
  }
}
```

**Response Body (`StyleAnalysisResponse`):**
*Status: 200 OK*
```json
{
  "userId": "user_12345",
  "timestamp": "2026-05-01T10:00:00Z",
  "summary": {
    "keywords": ["#chic", "#classic", "#warm_glow"],
    "score": 4.5,
    "coreIdentity": "세련된 클래식 무드를 가진 따뜻한 이미지"
  },
  "detailedAnalysis": {
    "faceAnalysis": "하트형 얼굴 라인을 보완하기 위해 볼륨감을 주는 스타일이 적합합니다.",
    "hairAnalysis": "풍성한 모발 밀도를 활용한 웨이브 스타일이 베스트입니다.",
    "lifestyleCompatibility": "단정한 오피스 환경에 어울리는 깔끔한 스타일을 추천합니다."
  },
  "recommendations": {
    "hairStyles": [
      {
        "name": "Soft Layered Bob",
        "reason": "턱선 라인을 부드럽게 감싸 하트형 얼굴의 특징을 보완합니다.",
        "imagePrompt": "A high-quality photo of a woman with a soft layered bob haircut, warm skin tone, professional setting, cinematic lighting"
      }
    ],
    "hairColors": [
      { "colorName": "Warm Chocolate Brown", "reason": "웜톤 피부의 생기를 더해줍니다." }
    ],
    "maintenanceTips": ["매일 아내 에센스로 컬을 유지하세요.", "드라이 시 뿌리 볼륨에 신경 써주세요."]
  }
}
```

**Error Codes:**
- `400 Bad Request`: 입력 데이터의 타입이 정의된 스키마와 일치하지 않
