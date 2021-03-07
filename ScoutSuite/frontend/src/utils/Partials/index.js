import PropTypes from 'prop-types';


export const convertBoolToEnable = value => value ? 'enabled' : 'disabled';

export const convertBoolToCheckmark = value => value ? '✔' : '✖';

export const concatPaths = (pathA, pathB) => pathA.length > 0 ? `${pathA}.${pathB}` : pathB;

export const partialDataShape = {
  item: PropTypes.object.isRequired,
  path_to_issues: PropTypes.arrayOf(PropTypes.string).isRequired,
};
