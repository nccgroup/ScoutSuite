export const convertBoolToEnable = value => value ? 'enabled' : 'disabled';

export const convertBoolToCheckmark = value => value ? '✔' : '✖';

export const concatPaths = (pathA, pathB) => pathA.length > 0 ? `${pathA}.${pathB}` : pathB;
