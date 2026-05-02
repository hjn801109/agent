# 💻 Developer — 텍스트 생성 및 데이터 처리 시 5000자 초과 여부를 체크하고, 초과 시 데이터를 자동으로 분할(Chunking)하거나 사용자에게 알림을 보내는 로직을 검토하여 반영하세요.

💻 Developer: 작업 시작합니다.

CEO의 지시 사항에 따라, 텍스트 생성 및 데이터 처리 시 5,000자 제한을 준수하기 위한 **'자동 분할(Chunking) 및 검증 로직'** 설계안과 구현 코드를 제안합니다. 이 로직은 에이전트의 응답 생성 전/후 단계에서 작동하도록 설계되었습니다.

### 🛠️ 5,000자 제한 관리 시스템 설계 (Limit Management System)

#### 1. 핵심 알고직 (Algorithm Flow)
1.  **Pre-Check (예측):** 생성할 작업의 규모(Task Complexity)를 분석하여 예상 글자 수를 산출합니다.
2.  **Threshold Detection (임계치 감지):** 생성된 결과물의 `length`가 5,000자(공백 포함)에 근접하거나 초과했는지 확인합니다.
3.  **Smart Chunking (스마트 분할):** 단순히 글자 수로 자르는 것이 아니라, 문장(`.` 혹은 `\n`) 단위로 텍스트를 분석하여 논리적 맥락이 깨지지 않는 최적의 지점에서 분할합니다.
4.  **User Notification (알림):** 분할이 발생했을 경우, 사용자에게 `[Part N/Total]` 태그와 함께 다음 파트 생성을 위한 트리거(예: "계속해줘")를 안내합니다.

#### 2. 구현 코드 (TypeScript/Next.js 환경 기준)
에이전트의 출력 엔진이나 API Route에서 활용할 수 있는 유틸리티 함수입니다.

```typescript
/**
 * 5000자 제한을 준수하기 위한 텍스트 분할 유틸리티
 * @param content 전체 텍스트 내용
 * @param limit 글자 수 제한 (기본 5000자)
 * @returns { parts: string[], isSplit: boolean } 분할된 배열과 분할 여부
 */
export function validateAndChunkContent(content: string, limit: number = 5000): { parts: string[]; isSplit: boolean } {
  if (content.length <= limit) {
    return { parts: [content], isSplit: false };
  }

  const parts: string[] = [];
  let remainingText = content;

  while (remainingText.length > 0) {
    if (remainingText.length <= limit) {
      parts.push(remainingText);
      break;
    }

    // 5000자 지점에서 가장 가까운 줄바꿈(\n) 또는 마침표(.)를 찾아 분할 지점 결정
    let splitIndex = remainingText.lastIndexOf('\n', limit);
    
    // 줄바꿈이 없으면 마침표로 시도
    if (splitIndex === -1 || splitIndex < limit * 0.8) {
      splitIndex = remainingText.lastIndexOf('.', limit);
    }

    // 만약 논리적 분할 지점을 찾지 못했다면 강제로 5000자에서 절단
    if (splitIndex === -1) {
      splitIndex = limit;
    }

    const chunk = remainingText.substring(0, splitIndex + 1).trim();
    parts.push(chunk);
    remainingText = remainingText.substring(splitIndex + 1).trim();
  }

  return { parts, isSplit: true };
}

// 사용 예시 (API Endpoint 또는 Agent Logic)
const rawOutput = "매우 긴 텍스트 데이터..."; 
const { parts, isSplit } = validateAndChunkContent(rawOutput);

if (isSplit) {
  console.log(`⚠️ 경고: 5000자 초과로 인해 ${parts.length}개로 분할되었습니다.`);
  // 이후 parts[0]은 즉시 출력, parts[1...n]은 세션 대기 또는 사용자 요청 시 출력 로직 실행
}
```

#### 3. 에이전트 워크플로우 적용 계획
- **Step 1 (Generation):** 에이전트가 답변을 생성합니다.
- **Step 2 (Validation):** 위 `validateAndChunkContent` 함수를 통과시킵니다.
- **Step 3 (Action):**
    - `isSplit: false` $\rightarrow$ 즉시 사용자에게 전달.
    - `isSplit: true` $\rightarrow$ `parts[0]`을 먼저 전달하며 하단에 `[Part 1/N] 내용이 길어 분할되었습니다. 계속하려면 "계속해줘"라고 입력하세요.` 메시지 강제 삽출.

#### 4. 데이터 파이프라인 적용 (Backend)
- 대량의 로그나 데이터 처리 시, API 응답 규격(Response Schema)에 `pagination` 또는 `chunk_info` 필드를 추가하여 클라이언트가 다음 데이터를 요청할 수 있는 인터페이스를 구축하겠습니다.

📊 평가: 완료 — 5,000자 제한을 준수하기 위한 알고리즘 설계 및 구현 코드를 완성함.
📝 다음 단계: 위 유틸리티 함수를 에이전트 응답 출력 모듈(Output Module)에 통합하여 자동 분할 시스템 적용.
