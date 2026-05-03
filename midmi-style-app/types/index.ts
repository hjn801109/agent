export interface StyleDNAInput {
  skinTone: 'light' | 'medium' | 'dark'; // 피부톤 (Light, Medium, Dark)
  hairType: 'straight' | 'wavy' | 'curly'; // 모발 상태 (Straight, Wavy, Curly)
  lifestyle: 'office' | 'casual' | 'artist'; // 라이프스타일 (Office, Casual, Artist)
}

export interface StyleAnalysisResponse {
  styleName: string; // 진단된 스타일 이름 (예: Rose Chic, Soft Bohemian)
  analysisSummary: string; // 핵심 분석 요약
  colorPalette: {
    primary: string; // 주 색상 (Rose Tone 기반)
    secondary: string; // 보조 색상
    accent: string; // 강조 색상
  };
  recommendations: string[]; // 구체적인 스타일 추천
  styleDNABreakdown: {
    skinToneFit: string;
    hairTextureFit: string;
    lifestyleMatch: string;
  };
  visualGuide: string; // 시각적 가이드 (디자이너 요구사항 반영)
}