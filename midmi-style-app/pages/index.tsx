import Head from 'next/head';
import GlassCard from '../components/GlassCard';

const HomePage: React.FC = () => {
  return (
    <>
      <Head>
        <title>midmi - AI Style Diagnosis Engine</title>
        <meta name="description" content="AI 기반 스타일 진단 및 트렌드 분석 서비스" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen p-8 md:p-16">
        {/* Header Section */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-serif text-rose-dark mb-4">midmi</h1>
          <p className="text-xl text-gray-600">AI Style Diagnosis Engine</p>
        </header>

        {/* Main Content Section - Example Card */}
        <div className="max-w-4xl mx-auto">
          <GlassCard className="mb-8 p-10">
            <h2 className="text-3xl font-serif text-rose-medium mb-6 border-b pb-2">Style Diagnosis Start</h2>
            <p className="text-gray-700 mb-6">
              당신의 스타일 DNA를 진단하여, 최적의 패션 트렌드와 맞춤형 코디를 제안합니다. 피부톤, 모발 상태, 라이프스타일 등 핵심 정보를 입력해주세요.
            </p>
            <div className="space-y-4">
              {/* Input Fields Placeholder */}
              <label className="block">
                <span className="text-rose-medium font-semibold">피부톤 (예: 밝은/중간/어두운):</span>
                <input type="text" placeholder="입력하세요..." className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring-rose-medium focus:border-rose-medium" />
              </label>
              <label className="block">
                <span className="text-rose-medium font-semibold">모발 상태 (예: 직모/곱슬/숱 많음):</span>
                <input type="text" placeholder="입력하세요..." className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring-rose-medium focus:border-rose-medium" />
              </label>
              <label className="block">
                <span className="text-rose-medium font-semibold">라이프스타일 (예: 오피스/캐주얼/아티스트):</span>
                <input type="text" placeholder="입력하세요..." className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring-rose-medium focus:border-rose-medium" />
              </label>
            </div>
          </GlassCard>

          {/* Call to Action Placeholder */}
          <div className="text-center mt-10">
            <button className="px-8 py-3 bg-rose-medium text-white font-bold rounded-full shadow-md hover:bg-rose-dark transition duration-300">
              스타일 진단 시작하기
            </button>
          </div>
        </div>
      </main>
    </>
  );
};

export default HomePage;