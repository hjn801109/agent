import Head from 'next/head';
import { useState } from 'react';
import StyleForm from '../components/StyleForm';
import StyleResult from '../components/StyleResult';
import { StyleDNAInput, StyleAnalysisResponse } from '../types';

const HomePage: React.FC = () => {
  const [analysis, setAnalysis] = useState<StyleAnalysisResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleAnalyze = (input: StyleDNAInput) => {
    setLoading(true);
    
    // Simulate API Call delay
    setTimeout(() => {
      // Mock Data Generation based on input
      const mockResult: StyleAnalysisResponse = {
        styleName: input.lifestyle === 'office' ? 'Modern Rose Elegance' : 'Soft Bohemian Chic',
        analysisSummary: '당신의 라이프스타일과 톤에 맞춘 부드러우면서도 세련된 로즈 톤 스타일입니다.',
        colorPalette: {
          primary: '#E07A5F', // rose-medium
          secondary: '#F4ACB7', // rose-light
          accent: '#C95B43', // rose-dark
        },
        recommendations: [
          '로즈 톤을 베이스로 한 메이크업 활용',
          input.hairType === 'straight' ? '깔끔한 스트레이트 헤어에 포인트 볼륨' : '자연스러운 웨이브 질감 살리기',
          '글래스모피즘이 가미된 반투명 액세서리 매치',
        ],
        styleDNABreakdown: {
          skinToneFit: '따뜻한 로즈 계열이 피부에 생기를 부여합니다.',
          hairTextureFit: '텍스처가 살아있는 스타일링이 분위기를 더합니다.',
          lifestyleMatch: '일상과 업무를 모두 아우를 수 있는 실용적이면서도 우아한 룩.',
        },
        visualGuide: '시스루 블라우스나 은은한 광택감의 소재를 매치해보세요. 로즈 골드 주얼리가 찰떡입니다.',
      };
      
      setAnalysis(mockResult);
      setLoading(false);
    }, 1500);
  };

  const handleReset = () => {
    setAnalysis(null);
  };

  return (
    <>
      <Head>
        <title>midmi - AI Style Diagnosis Engine</title>
        <meta name="description" content="AI 기반 스타일 진단 및 트렌드 분석 서비스" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen p-8 md:p-16 relative overflow-hidden">
        {/* Background decorative elements for Glassmorphism feel */}
        <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-rose-light rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
        <div className="absolute top-[-10%] right-[-10%] w-96 h-96 bg-rose-medium rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-[-20%] left-[20%] w-96 h-96 bg-rose-dark rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>

        <div className="relative z-10">
          {/* Header Section */}
          <header className="text-center mb-12">
            <h1 className="text-5xl font-serif text-rose-dark mb-4 drop-shadow-sm cursor-pointer" onClick={handleReset}>midmi</h1>
            <p className="text-xl text-gray-600 font-light tracking-wider">AI Style Diagnosis Engine</p>
          </header>

          {/* Main Content Section */}
          <div className="max-w-4xl mx-auto transition-all duration-500">
            {loading ? (
              <div className="flex flex-col items-center justify-center p-20">
                <div className="w-16 h-16 border-4 border-rose-light border-t-rose-dark rounded-full animate-spin mb-6"></div>
                <p className="text-rose-medium font-serif text-xl animate-pulse">Analyzing your Style DNA...</p>
              </div>
            ) : analysis ? (
              <StyleResult analysis={analysis} onReset={handleReset} />
            ) : (
              <StyleForm onAnalyze={handleAnalyze} />
            )}
          </div>
        </div>
      </main>
    </>
  );
};

export default HomePage;