import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
}

const GlassCard: React.FC<GlassCardProps> = ({ children, className = '' }) => {
  return (
    <div className={`glass-card p-6 rounded-xl shadow-lg transition duration-300 ${className}`}>
      {children}
    </div>
  );
};

export default GlassCard;