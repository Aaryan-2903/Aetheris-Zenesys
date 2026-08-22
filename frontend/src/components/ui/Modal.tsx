import React from 'react';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  primaryActionText?: string;
  onPrimaryAction?: () => void;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  description,
  children,
  primaryActionText,
  onPrimaryAction
}) => {
  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 bg-[#00174b55] backdrop-blur-xs flex items-center justify-center z-50 p-4 md:p-5 animate-in fade-in duration-150"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="bg-white rounded-2xl w-full max-w-[560px] p-6 md:p-7 shadow-modal relative max-h-[90vh] overflow-y-auto">
        <button 
          onClick={onClose}
          className="absolute top-5 right-5 w-[30px] h-[30px] bg-[#f1f2f4] rounded-full flex items-center justify-center hover:bg-gray-200 transition-colors"
          aria-label="Close modal"
        >
          <X size={16} className="text-gray-600" />
        </button>
        <h3 className="text-[20px] md:text-[22px] font-semibold text-text mb-1.5 pr-8">{title}</h3>
        {description && <p className="text-[13px] text-muted mb-4">{description}</p>}
        
        <div className="mb-4">
          {children}
        </div>
        
        {primaryActionText && onPrimaryAction && (
          <button 
            className="w-full rounded-full bg-navy text-white py-3 font-semibold text-sm hover:bg-[#00287a] transition-colors mt-2"
            onClick={onPrimaryAction}
          >
            {primaryActionText}
          </button>
        )}
      </div>
    </div>
  );
};
