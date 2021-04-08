import React from 'react';
import PropTypes from 'prop-types';

import DetailedValue from '../../DetailedValue';


const propTypes = {
  data: PropTypes.any.isRequired,
  className: PropTypes.string,
};

const defaultProps = {
  className: '',
};

const GenericObject = props => {
  const { 
    data,
    className,
  } = props;

  if (typeof data !== 'object') {
    return data.toString();
  }

  const invalidKeys = [
    'path',
    'display_path',
  ];

  return (
    <ul className={className}>
      {Object.entries(data).map(([key, value], i) => (
        value !== null && !invalidKeys.includes(key) && (
          <li key={i}>
            <DetailedValue 
              label={key} 
              value={value}
              renderValue={value => (<GenericObject data={value}/>)}
            />
          </li>
        )
      ))}
    </ul>
  );
};

GenericObject.propTypes = propTypes;
GenericObject.defaultProps = defaultProps;

export default GenericObject;
