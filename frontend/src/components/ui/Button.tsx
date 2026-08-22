import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
  className?: string;
}

export const Button: React.FC<ButtonProps> = ({ variant = 'primary', children, className = '', ...props }) => {
  const baseStyles = 'w-full rounded-full py-3 px-4 font-semibold transition-colors cursor-pointer text-sm';
  const variants = {
    primary: 'bg-navy text-white hover:bg-[#00287a] border-none',
    secondary: 'bg-white text-text border border-[#d1d1d6] hover:bg-gray-50'
  };

  return (
    <button className={`${baseStyles} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
};
