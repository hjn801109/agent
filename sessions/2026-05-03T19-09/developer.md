# 💻 Developer — 정의된 스키마를 바탕으로 데이터 수집 API를 구현하고, AES-256 암호화 및 RBAC 보안 정책이 통합된 안정적인 데이터 인제스션(Ingestion) 및 저장 파이프라인을 구축하십시오.

💻 Developer: 작업 시작합니다.

CEO의 지시 사항에 따라, Researcher가 설계한 스키마를 기반으로 **AES-256-GCM 암호화**와 **RBAC(Role-Based Access Control)**가 통합된 보안 데이터 인제스션 파이프라인을 구축합니다.

### 🛠️ 보안 데이터 인제스션 파이프라인 아키텍처

이 구현은 민감한 신체 정보(피부톤, 얼굴 특징 등)를 암호화하여 저장하고, 권한이 있는 사용자/전문가만 데이터에 접근할 수 있도록 설계되었습니다.

#### 1. 암호화 유틸리티 (`lib/crypto.ts`)
`AES-256-GCM`을 사용하여 데이터의 기밀성과 무결성(Auth Tag)을 동시에 보장합니다.

```typescript
import crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY!; // 32 bytes
const IV_LENGTH = 12;

export function encrypt(text: string): string {
  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto.createCipheriv(ALGORITHM, Buffer.from(ENCRYPTION_KEY), iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag().toString('hex');
  
  // 구조: iv:authTag:encryptedData
  return `${iv.toString('hex')}:${authTag}:${encrypted}`;
}

export function decrypt(cipherText: string): string {
  const [ivHex, authTagHex, encryptedData] = cipherText.split(':');
  const iv = Buffer.from(ivHex, 'hex');
  const auth
  const decipher = crypto.createDecipheriv(ALGORITHM, Buffer.from(ENCRYPTION_KEY), iv);
  
  decipher.setAuthTag(Buffer.from(authTagHex, 'hex'));
  
  let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}
```

#### 2. RBAC 및 검증 스키마 (`lib/validation/profile.ts`)
Zod를 사용하여 Researcher의 스키마를 강제하고, 권한 검증 로직을 포함합니다.

```typescript
import { z } from 'zod';

export const UserProfileSchema = z.object({
  user_id: z.string().uuid(),
  skin_features: z.object({
    undertone: z.enum(['Warm', 'Cool', 'Neutral']),
    brightness: z.number().min(0).max(1),
    pigmentation_level: z.number().min(0).max(1),
    skin_type: z.enum(['Oily', 'Dry', 'Combination', 'Normal']),
  }),
  face_features: z.object({
    face_shape: z.enum(['Round', 'Oval', 'Square', 'Heart', 'Long']),
    forehead_height: z.number().min(0).max(1),
    jawline_sharpness: z.number().min(0).max(1),
  }),
  metadata: z.object({
    profile_completeness: z.number(),
    last_updated: z.string().datetime(),
  }),
});

export type UserProfile = z.infer<typeof UserProfileSchema>;

// RBAC Role 정의
export type UserRole = 'USER' | 'EXPERT' | 'ADMIN';

export function checkPermission(userRole: UserRole, requiredRole: UserRole): boolean {
  const roleHierarchy: Record<UserRole, number> = { 'USER': 1, 'EXTPERT': 2, 'ADMIN': 3 };
  return roleHierarchy[userRole] >= roleHierarchy[requiredRole];
}
```

#### 3. 데이터 인제스션 API 엔드포인트 (`app/api/ingest/profile/route.ts`)
데이터 수집, 암호화, 저장 로직이 통합된 핵심 엔드포인트입니다.

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { UserProfileSchema, checkPermission, UserRole } from '@/lib/validation/profile';
import { encrypt } from '@/lib/crypto';

// Mock DB (실제 환경에서는 Prisma/MongoDB 사용)
const db: any[] = [];

export async function POST(req: NextRequest) {
  try {
    // 1. 인증 및 RBAC 체크 (Session에서 role 추출 가정)
    const session = await req.auth(); // NextAuth 예시
    const userRole = (session?.user?.role as UserRole) || 'USER';

    if (!checkPermission(userRole, 'USER')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    // 2. 요청 데이터 파싱 및 검증
    const body = await req.json();
    const validatedData = UserProfileSchema.parse(body);

    // 3. 민감한 데이터 암호화
    const encryptedProfile = {
      user_id: validatedData.user_id,
      skin_features_encrypted: encrypt(JSON.stringify(validatedData.skin_features)),
      face_features_encrypted: encrypt(JSON.stringify(validatedData.face_features)),
      metadata: validatedData.metadata,
    };

    // 4. DB 저장
    db.push(encryptedProfile); // 실제 DB Insert 로직으로 대체

    return NextResponse.json({ message: 'Profile saved securely' }, { status: 201 });
  } catch (error) {
    console.error('Ingestion Error:', error);
    if (error instanceof Error && error.name === 'ZodError') {
      return NextResponse.json({ error: 'Invalid data format' }, { status: 400 });
    }
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
} 


