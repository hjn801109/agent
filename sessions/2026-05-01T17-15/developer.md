# 💻 Developer — 설계된 디자인 시스템의 Next.js 및 Tailwind CSS 구현 가능성을 검토하고, 재사용 가능한 컴포넌트 구조(Props 및 데이터 구조) 정의

💻 Developer: 작업 시작합니다.

# 🛠️ Design System Implementation Blueprint: "Rose-Tech"

Designer가 제안한 시각적 요소를 Next.js와 Tailwind CSS 환경에서 구현하기 위한 기술적 설계안입니다. Tailwind의 `theme.extend`를 활용하여 디자인 시스템을 코드 레벨에서 확정하고, 재사용 가능한 컴포넌트의 Props 구조를 정의합니다.

## 1. 구현 가능성 검토 (Feasibility Study)
- **Tailwind CSS**: Designer가 정의한 Hex Code 및 Typography(Serif/Sans)를 `tailwind.config.ts`에 1:1 매핑 가능. Glassmorphism(backdrop-blur) 및 Gradient 구현에 최적화됨.
- **Next.js (App Router)**: 매거진 스타일의 비대형 그리드(Asymmetric Grid)를 위한 레이아웃 컴포넌트 설계 및 SEO를 위한 Server Component 활용 가능.
- **결론**: **[매우 높음]** 추가적인 라이브러리 없이 Tailwind 기본 기능과 `clsx`/`tailwind-merge`만으로 완벽 구현 가능.

## 2. Foundation: `tailwind.config.ts` 설정
디자인 시스템의 핵심 컬러와 폰트를 시스템에 주입합니다.

```typescript
// tailwind.config.ts
import type { Config } Alt } from 'tailwindcss'

const config: Config = {
  theme: {
    extend: {
      colors: {
        rose: {
          primary: '#E07A5F',    // Main CTA
          secondary: '#F4ACB7',  // Sub/Card Bg
          accent: '#E07A5F',
        },
        navy: {
          contrast: '#3D405B',   // High Contrast Text
          deep: '#2D3047',
        },
        surface: {
          white: '#FFFFFF',
          glass: 'rgba(204, 255, 255, 0.6)', // Glassmorphism Base
        }
      },
      fontFamily: {
        serif: ['Playfair Display', 'serif'], // Magazine Heading
        sans: ['Pretendard', 'sans-serif'],   // Body/UI
      },
      backgroundImage: {
        'rose-gradient': 'linear-gradient(to bottom right, #E07A5F, #F4ACB7)',
      }
    },
  },
  plugins: [require('tailwindcss-animate')], // Micro-interactions용
}
export default config
```

## 3. Reusable Component Architecture (Atomic Design)

### A. `Typography` Component (Text Engine)
모든 텍스트의 일관성을 유지하기 위해 단일 컴포넌트로 제어합니다.

```typescript
// types/typography.ts
export type TextVariant = 'h1' | 'h2' | 'h3' | 'body1' | 'body2' | 'label';

// components/ui/Typography.tsx
interface TypographyProps {
  variant: TextVariant;
  children: React.ReactNode;
  className?: string;
}

export const Typography = ({ variant, children, className }: TypographyProps) => {
  const variants = {
    h1: 'font-serif text-4xl md:text-5xl font-bold text-navy-contrast leading-tight',
    h2: 'font-serif text-2xl md:text-3xl font-semibold text-navy-contrast',
    h3: 'font-sans text-lg font-medium text-rose-primary',
    body1: 'font-sans text-base text-navy-contrast leading-relaxed',
    body2: 'font-sans text-sm text-gray-600',
    label: 'font-sans text-xs font-bold uppercase tracking-wider text-rose-primary',
  };

  return <div className={`${variants[variant]} ${className}`}>{children}</div>;
};
```

### B. `Button` Component (Action Engine)
브랜드 톤에 맞춘 상태(Hover, Active)와 변형(Variant)을 정의합니다.

```typescript
// components/ui/Button.tsx
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

export const Button = ({ variant = 'primary', size = 'md', className, ...props }: ButtonProps) => {
  const variants = {
    primary: 'bg-rose-primary text-white hover:bg-opacity-90 shadow-md',
    secondary: 'bg-rose-secondary text-navy-contrast hover:bg-opacity-80',
    outline: 'border-2 border-rose-primary text-rose-primary hover:bg-rose-primary hover:text-white',
    ghost: 'text-navy-contrast hover:bg-rose-secondary/20',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-5
