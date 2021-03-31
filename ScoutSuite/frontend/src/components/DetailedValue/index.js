import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import './style.scss';


const propTypes = {
  label: PropTypes.string,
  value: PropTypes.any.isRequired,
  separator: PropTypes.string,
  className: PropTypes.string,
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
    className,
    renderValue,
  } = props;

  if (value === undefined || value === null) {
    return null;
  }

  return (
    <div className={cx(className, 'detailed-value')}>
      {label && (
        <span className="label">
          {`${label}${separator}`}
        </span>
      )}
      <span className="value">{renderValue(value)}</span>
    </div>
  );
};

DetailedValue.propTypes = propTypes;
DetailedValue.defaultProps = defaultProps;

export default DetailedValue;
