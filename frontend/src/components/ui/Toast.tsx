import React, { useEffect } from 'react';

interface ToastProps {
  message: string | null;
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, onClose }) => {
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        onClose();
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [message, onClose]);

  if (!message) return null;

  return (
    <div className={`fixed right-7 bottom-7 bg-navy text-white py-3.5 px-[18px] rounded-xl shadow-toast z-50 transition-all duration-300 transform translate-y-0 opacity-100`}>
      {message}
    </div>
  );
};
