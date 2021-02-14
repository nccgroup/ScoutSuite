import { severityLevel } from './index';

export const sortBySeverity = (rowA, rowB, columnId) => {

  if (!rowA || !rowB) return 0;

  const diff = severityLevel(rowA.values[columnId]) - severityLevel(rowB.values[columnId]);

  if (diff < 0) return -1;
  else if (diff > 0) return 1;

  return 0;
};