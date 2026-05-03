import React from 'react';
import GlassCard from './GlassCard';
import { StyleAnalysisResponse } from '../types';

interface StyleResultProps {
  analysis: StyleAnalysisResponse;
  onReset: () => void;
}

const StyleResult: React.FC<StyleResultProps> = ({ analysis, onReset }) => {
  return (
    <GlassCard className="p-8 animate-fade-in-up">
      <div className="text-center mb-8">
        <h2 className="text-sm uppercase tracking-widest text-gray-500 mb-2 font-semibold">Your Style DNA</h2>
        <h3 className="text-4xl font-serif text-rose-dark">{analysis.styleName}</h3>
        <p className="mt-4 text-gray-700 italic">"{analysis.analysisSummary}"</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        {/* Color Palette */}
        <div>
          <h4 className="text-xl font-serif text-rose-medium border-b pb-2 mb-4">Color Palette</h4>
          <div className="flex gap-4">
            <div className="flex flex-col items-center">
              <div 
                className="w-16 h-16 rounded-full shadow-md border-2 border-white"
                style={{ backgroundColor: analysis.colorPalette.primary }}
              />
              <span className="text-xs text-gray-500 mt-2">Primary</span>
            </div>
            <div className="flex flex-col items-center">
              <div 
                className="w-16 h-16 rounded-full shadow-md border-2 border-white"
                style={{ backgroundColor: analysis.colorPalette.secondary }}
              />
              <span className="text-xs text-gray-500 mt-2">Secondary</span>
            </div>
            <div className="flex flex-col items-center">
              <div 
                className="w-16 h-16 rounded-full shadow-md border-2 border-white"
                style={{ backgroundColor: analysis.colorPalette.accent }}
              />
              <span className="text-xs text-gray-500 mt-2">Accent</span>
            </div>
          </div>
        </div>

        {/* DNA Breakdown */}
        <div>
          <h4 className="text-xl font-serif text-rose-medium border-b pb-2 mb-4">DNA Breakdown</h4>
          <ul className="space-y-3 text-sm text-gray-700">
            <li><span className="font-semibold text-rose-dark">피부톤 매칭:</span> {analysis.styleDNABreakdown.skinToneFit}</li>
            <li><span className="font-semibold text-rose-dark">모발 매칭:</span> {analysis.styleDNABreakdown.hairTextureFit}</li>
            <li><span className="font-semibold text-rose-dark">라이프스타일 매칭:</span> {analysis.styleDNABreakdown.lifestyleMatch}</li>
          </ul>
        </div>
      </div>

      {/* Recommendations */}
      <div className="mb-8">
        <h4 className="text-xl font-serif text-rose-medium border-b pb-2 mb-4">Style Recommendations</h4>
        <ul className="list-disc list-inside space-y-2 text-gray-700">
          {analysis.recommendations.map((rec, index) => (
            <li key={index}>{rec}</li>
          ))}
        </ul>
      </div>

      {/* Visual Guide Text */}
      <div className="bg-rose-light bg-opacity-20 p-4 rounded-lg mb-8 border border-rose-light">
        <p className="text-sm text-rose-dark font-medium whitespace-pre-line">
          {analysis.visualGuide}
        </p>
      </div>

      <button 
        onClick={onReset}
        className="w-full py-3 bg-white text-rose-medium border-2 border-rose-medium font-bold rounded-full shadow hover:bg-rose-50 transition duration-300"
      >
        다시 진단하기
      </button>
    </GlassCard>
  );
};

export default StyleResult;
