import React, { useState } from 'react';
import GlassCard from './GlassCard';
import { StyleDNAInput, StyleAnalysisResponse } from '../types';

interface StyleFormProps {
  onAnalyze: (input: StyleDNAInput) => void;
  analysis?: StyleAnalysisResponse | null;
}

const StyleForm: React.FC<StyleFormProps> = ({ onAnalyze, analysis }) => {
  const [inputData, setInputData] = useState<StyleDNAInput>({
    skinTone: 'medium',
    hairType: 'wavy',
    lifestyle: 'casual',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setInputData({ ...inputData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAnalyze(inputData);
  };

  return (
    <GlassCard className="p-8">
      <h2 className="text-3xl font-serif text-rose-medium mb-6 border-b pb-2">Style DNA 진단</h2>
      
      {/* Input Fields */}
      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-gray-700 mb-2">
            <span className="font-semibold text-rose-medium block">피부톤:</span>
            <select name="skinTone" value={inputData.skinTone} onChange={handleChange} className="w-full p-3 border rounded-lg focus:ring-rose-medium focus:border-rose-medium">
              <option value="light">밝은 (Light)</option>
              <option value="medium">중간 (Medium)</option>
              <option value="dark">어두운 (Dark)</option>
            </select>
          </label>
        </div>

        <div>
          <label className="block text-gray-700 mb-2">
            <span className="font-semibold text-rose-medium block">모발 상태:</span>
            <select name="hairType" value={inputData.hairType} onChange={handleChange} className="w-full p-3 border rounded-lg focus:ring-rose-medium focus:border-rose-medium">
              <option value="straight">직모 (Straight)</option>
              <option value="wavy">웨이브 (Wavy)</option>
              <option value="curly">곱슬 (Curly)</option>
            </select>
          </label>
        </div>

        <div>
          <label className="block text-gray-700 mb-2">
            <span className="font-semibold text-rose-medium block">라이프스타일:</span>
            <select name="lifestyle" value={inputData.lifestyle} onChange={handleChange} className="w-full p-3 border rounded-lg focus:ring-rose-medium focus:border-rose-medium">
              <option value="office">오피스 (Office)</option>
              <option value="casual">캐주얼 (Casual)</option>
              <option value="artist">아티스트 (Artist)</option>
            </select>
          </label>
        </div>

        <button 
          type="submit" 
          className="w-full py-3 bg-rose-medium text-white font-bold rounded-full shadow-md hover:bg-rose-dark transition duration-300 mt-6"
        >
          스타일 진단 실행
        </button>
      </form>
    </GlassCard>
  );
};

export default StyleForm;