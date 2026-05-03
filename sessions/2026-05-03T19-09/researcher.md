# 🔍 Researcher — 사용자 입력값(피부톤, 모질, 선호 스타일 등)의 패턴을 분석하여, AI 추천 엔진 학습에 최적화된 데이터 스키마(Schema) 초안을 설계하십시오.

🔍 Researcher: 작업 시작합니다.

AI 추천 엔진의 학습 성능(Accuracy)과 서비스의 핵심 지표인 Trust Score 및 LTV 측정을 위해, 데이터의 **수치화(Numericalization)**와 **범주화(Categorability)**를 최우선으로 한 데이터 스키마 초안을 설계하였습니다.

---

### 🧠 AI 학습 최적화 데이터 설계 원칙
1.  **Feature Engineering 기반 설계**: 단순 텍스트가 아닌, 모델이 계산 가능한 수치(Float)와 명확한 레이블(Categorical)로 분리.
2.  **Feedback Loop 통합**: 추천 결과에 대한 사용자의 반응(`is_match`)을 즉시 학습 데이터로 전환할 수 있는 구조.
3.  **Trust Score 연동**: 데이터의 결측치(Null)를 추적하여 `Profile Completeness`를 계산할 수 있는 구조.

---

### 📊 데이터 스키마 초안 (JSON/NoSQL 구조 지향)

#### 1. `User_Profile_Schema` (정적/준정적 데이터)
사용자의 변하지 않는 신체적 특징을 저장하며, AI의 기초 특징값(Base Feature)으로 활용됩니다.

```json
{
  "user_id": "UUID",
  "skin_features": {
    "undertone": "string (Warm | Cool | Neutral)",
    "brightness": "float (0.0 - 1.0)", // 피부 밝기 수치화
    "pigmentation_level": "float (0.0 - 1.0)", // 잡티/색소침착 정도
    "skin_type": "string (Oily | Dry | Combination | Normal)"
  },
  "face_features": {
    "face_shape": "string (Round | Oval | Square | Heart | Long)",
    "forehead_height": "float (0.0 - 1.0)",
    "jawline_sharpness": "float (0.0 - 1.0)"
  },
  "metadata": {
    "profile_completeness": "float (0.0 - 1.0)", // Trust Score 산출용
    "last_updated": "timestamp"
  }
}
```

#### 2. `Hair_Condition_Schema` (동적 데이터)
모질과 현재 상태를 저장하며, 주기적인 업데이트를 통해 AI가 '현재 시점'의 최적 스타일을 제안하게 합니다.

```json
{
  "user_id": "UUID",
  "hair_features": {
    "texture_thickness": "string (Fine | Medium | Coarse)",
    "curl_pattern": "int (1 - 4)", // Andre Walker Scale 기반 (직모~곱슬)
    "density": "string (Low | Medium | High)",
    "damage_level": "float (0.0 - 1.0)", // 손상도 수치화
    "current_color": "string (HEX Code)",
    "hair_length": "string (Short | Medium | Long)"
  },
  "last_measured_at": "timestamp"
}
```

#### 3. `Style_Preference_Schema` (선호도 및 행동 데이터)
사용자가 선호하는 스타일의 벡터(Vector)를 형성하여 추천 엔진의 가중치(Weight)로 활용합니다.

```json
{
  "user_id": "UUID",
  "preference_vector": {
    "style_vibe": ["Chic", "Lovely", "Natural", "Edgy"], // 선호 분위기 태그
    "color_preference": ["Ash", "Gold", "Deep_Brown"], // 선호 색상군
    "length_preference": "string (Short | Medium | Long)",
    "maintenance_tolerance": "float (0.0 - 1.0)" // 손질 난이도 수용도
  },
  "interaction_history": [
    {"style_id": "UUID", "action": "click | save | dislike", "timestamp": "ISO8601"}
  ]
}
```

#### 4. `Recommendation_Feedback_Schema` (학습 피드백 데이터)
**핵심 데이터.** `AI Match Accuracy`를 계산하고 모델을 재학습(Retraining)시키는 Ground Truth(정답지) 역할을 합니다.

```json
{
  "recommendation_id": "UUID",
  "user_id": "UUID",
  "recommended_style_id": "UUID",
  "is_match": boolean,
  "ai_match_accuracy": float (0.0 - 1.0),
  "user_satisfaction": int (1 - 5),
  "feedback_tags": ["Natural", "Too_Short", "Color_Nice"],
  "timestamp": "ISO8601"
}
``` 

# 💻 Developer — 정의된 스키마를 바탕으로 데이터 수집 API를 구현하고, AES-256 암호화 및 RBAC 보안 정책이 통합된 안정적인 데이터 인제스션(Ingestion) 및 저장 파이프라인을 구축하십시오.

