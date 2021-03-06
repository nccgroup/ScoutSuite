import React from 'react';
import { PropTypes } from 'prop-types';


export const convertBoolToEnable = value => value ? 'Enabled' : 'Disabled ✖';

export const convertBoolToCheckmark = value => value ? '✔' : '✖';

export const convertValueOrNever = value => value ? value : 'Never';

export const convertListToChips = list => list && list.length > 0 ? list.map((item, index) => <span className="chip" key={index}>{item}</span>) : 'None';

export const concatPaths = (pathA, pathB) => pathA.length > 0 ? `${pathA}.${pathB}` : pathB;

export const partialDataShape = {
  item: PropTypes.object.isRequired,
  path_to_issues: PropTypes.arrayOf(PropTypes.string).isRequired,
};