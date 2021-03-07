import React from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.any.isRequired,
  separator: PropTypes.string,
  renderValue: PropTypes.func,
};

const defaultProps = {
  separator: ': ',
  renderValue: value => value,
};

const DetailedValue = props => {
  const {
    label,
    value,
    separator,
    renderValue,
  } = props;

  if (value === undefined || value === null) {
    return null;
  }

  return (
    <div className="detailed-value"> 
      <span className="label">{`${label}${separator}`}</span>
      <span className="value">{renderValue(value)}</span>
    </div>
  );
};

DetailedValue.propTypes = propTypes;
DetailedValue.defaultProps = defaultProps;

export default DetailedValue;
