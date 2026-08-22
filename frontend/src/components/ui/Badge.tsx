import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'red';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = 'default', className = '' }) => {
  const baseStyles = 'inline-flex px-2.5 py-1.5 rounded-md text-[11px] font-bold tracking-[0.05em] uppercase';
  const variants = {
    default: 'bg-gray-100 text-gray-800',
    red: 'bg-redbg text-[#b42318]'
  };

  return (
    <span className={`${baseStyles} ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};
