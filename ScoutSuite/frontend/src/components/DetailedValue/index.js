import React from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.any.isRequired,
  renderValue: PropTypes.func,
};

const defaultProps = {
  renderValue: value => value,
};

const DetailedValue = props => {
  const {
    label,
    value,
    renderValue,
  } = props;

  return (
    <div className="detailed-value"> 
      <span className="label">{label}</span>
      <span className="value">{renderValue(value)}</span>
    </div>
  );
};

DetailedValue.propTypes = propTypes;
DetailedValue.defaultProps = defaultProps;

export default DetailedValue;
