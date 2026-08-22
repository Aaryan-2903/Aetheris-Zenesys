export const formatEnumLabel = (val: string | null | undefined): string => {
  if (!val) return '';

  const knownMap: Record<string, string> = {
    'APPROVAL_REQUIRED': 'Approval Required',
    'REVIEW_PRICE': 'Review Price',
    'REVIEW_DELIVERY': 'Review Delivery',
    'VENDOR_REVIEW': 'Vendor Review',
    'PAYMENT_REVIEW': 'Payment Review',
    'MANUAL_REVIEW': 'Manual Review',
    'PROCEED': 'Proceed',
    'ACTION_REQUIRED': 'Action Required',
    'NO_ACTION_REQUIRED': 'No Action Required',
    'HIGH': 'High Priority',
    'MEDIUM': 'Medium Priority',
    'LOW': 'Low Priority',
    'ml_prediction': 'ML Prediction Signal',
    'price_signal': 'Price Variance Signal',
    'delivery_performance': 'Delivery Reliability Signal',
    'quality_performance': 'Quality Performance Signal',
    'payment_risk': 'Payment Terms Signal',
    'financial_exposure': 'Financial Exposure Signal',
    'strong_procurement_decision': 'Procurement Performance Signal',
  };

  if (knownMap[val]) {
    return knownMap[val];
  }

  // Fallback: convert SNAKE_CASE or snake_case to Title Case
  return val
    .replace(/[_-]+/g, ' ')
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};
