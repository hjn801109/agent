# 💻 Developer — 기획된 핵심 기능(사용자 관리, 진단 데이터 입력)의 데이터 스키마 및 확장성을 위한 최종 데이터 구조 설계를 제안해줘.

💻 Developer: 작업 시작합니다.

## 📋 데이터 스키마 최종 설계 제안

CEO님의 지시에 따라, 사용자 관리 및 진단 데이터 입력의 확장성과 안정성을 극대화하는 최종 데이터 구조를 Next.js 기반 API와 연동하기 용이하도록 설계했습니다. 모든 핵심 엔티티는 관계형 데이터베이스(PostgreSQL 등)에 최적화되어 있으며, 확장성을 위해 `enum` 사용을 원칙으로 적용했습니다.

### 1. 핵심 엔티티 정의 (Entity Definitions)

#### A. User (사용자 정보)
사용자의 계정 및 구독 상태를 관리합니다. 수익화 모델(LTV/Churn) 측정의 기반이 됩니다.

| 필드명 | 타입 | 제약 조건 / 설명 | 확장성 고려 사항 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | |
| `email` | String | Unique, 필수 입력 | 로그인 및 커뮤니케이션의 핵심 |
| `name` | String | 사용자 이름 | |
| `subscription_status` | Enum | `FREE`, `PREMIUM`, `BUSINESS` (구독 상태) | 가격 정책 및 접근 권한 관리 |
| `created_at` | Timestamp | 자동 기록 | 리텐션 분석의 시작점 |
| `last_login` | Timestamp | 마지막 로그인 시간 | 이탈 예측 모델에 활용 |
| `partner_id` | UUID (FK) | 연결된 제휴사 ID (선택 사항) | 네트워크 확장성 확보 |

#### B. DiagnosisReport (진단 리포트 데이터)
사용자가 받은 모든 진단 결과와 상세 데이터를 저장합니다. 핵심 수익화 지표(ARPU, 전환율) 측정의 원천 데이터입니다.

| 필드명 | 타입 | 제약 조건 / 설명 | 확장성 고려 사항 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | |
| `user_id` | UUID (FK) | 해당 진단을 받은 사용자 ID | 사용자별 데이터 분리 |
| `report_type` | Enum | `HAIR_STYLE`, `COLOR_ANALYSIS`, `CUSTOM_PROFILE` 등 | AI 모델의 다양한 출력 유형 관리 |
| `diagnosis_date` | Date | 진단이 완료된 날짜 | 시계열 분석 및 트렌드 파악 |
| `raw_data` | JSONB | AI가 생성한 원본 데이터 (매우 중요) | 추후 모델 재학습 또는 상세 분석용 |
| `analysis_score` | Float | 종합 만족도 점수 (1-100점) | 품질 평가 지표 |
| `generated_at` | Timestamp | 리포트가 생성된 시간 | |

#### C. Partner (제휴사/미용실 정보)
네트워크 확장 목표를 지원합니다.

| 필드명 | 타입 | 제약 조건 / 설명 | 확장성 고려 사항 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | |
| `name` | String | 미용실/파트너 이름 | |
| `contact_info` | JSONB | 전화번호, 주소 등 연락 정보 | |
| `location` | GeoPoint | 지리적 위치 (Google Maps 연동 준비) | 지역 기반 마케팅 확장 |

#### D. Transaction (거래 및 수익 기록)
수익화 모델의 핵심입니다. 결제 내역과 수익 흐름을 추적합니다.

| 필드명 | 타입 | 제약 조건 / 설명 | 확장성 고려 사항 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | |
| `user_id` | UUID (FK) | 구매를 한 사용자 ID | 수익 집계의 기준 |
| `report_id` | UUID (FK) | 구매한 리포트 ID (선택 사항) | 어떤 상품에 대한 결제인지 추적 |
| `amount` | Decimal | 실제 결제 금액 | |
| `currency` | String | 통화 코드 (예: KRW, USD) | 다중 통화 지원 준비 |
| `transaction_type` | Enum | `REPORT_PURCHASE`, `SUBSCRIPTION_UPDATE`, `PARTNER_REFERRAL` | 수익 모델별 분류 |
| `status` | Enum | `COMPLETED`, `PENDING`, `FAILED` | 결제 상태 관리 |
| `transaction_date` | Timestamp | 거래 일시 | |

### 2. API 엔드포인트 구조 제안 (Admin Focus)

개발팀이 즉시 구현할 수 있도록 핵심 Admin API의 엔드포인트 및 데이터 흐름을 정의합니다.

| Endpoint | HTTP Method | 설명 | 필요한 데이터/로직 | 보안 레벨 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/admin/users` | GET | 모든 사용자 목록 조회 (필터링 가능) | `User` 테이블 데이터 | Admin Only |
| `/api/admin/users/:id` | GET/PUT | 특정 사용자 상세 정보 조회 및 수정 | `User` 테이블 | Admin Only |
| `/api/admin/diagnoses` | GET | 모든 진단 리포트 목록 조회 (사용자별) | `DiagnosisReport` 테이블 | Admin Only |
| `/api/admin/transactions` | GET | 전체 거래 내역 조회 및 필터링 | `Transaction` 테이블 | Admin Only |
| `/api/admin/reports/:id` | GET | 특정 진단 리포트 상세 데이터 조회 | `DiagnosisReport.raw_data` 포함 | Admin Only |
| `/api/admin/partners` | POST/GET | 제휴사 목록 관리 및 등록 | `Partner` 테이블 | Admin Only |

---
📊 평가: 완료 — CEO의 요구사항(핵심 기능의 확장성 있는 데이터 스키마)에 따라 실행 가능한 최종 데이터 구조를 제공했습니다.
📝 다음 단계: 사용자 인터페이스 컴포넌트에서 위 정의된 JSON 스키마 타입을 기반으로 Props 및 State 관리 로직을 개발합니다.
