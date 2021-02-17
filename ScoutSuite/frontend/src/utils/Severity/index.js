export const severityLevel = (code) => {

  const severities = {
    critical: 5,
    danger: 4,
    high: 4,
    warning: 3,
    medium: 3,
    low: 2,
    info: 1,
    success: 0
  };

  return severities[code];

};
