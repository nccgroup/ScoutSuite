import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import './style.scss';


const propTypes = {
  label: PropTypes.node,
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
  let { value } = props;
  const {
    label,
    separator,
    className,
    renderValue,
  } = props;

  if (value === undefined || value === null) {
    return null;
  }

  if (typeof value === 'boolean') {
    value = String(value);
  }

  return (
    <div className={cx(className, 'detailed-value')}>
      {label && (
        <span className="label">
          {typeof(label) === 'string' ? (
            `${label}${separator}`
          ) : (
            label
          )}
        </span>
      )}
      <span className="value">{renderValue(value)}</span>
    </div>
  );
};

DetailedValue.propTypes = propTypes;
DetailedValue.defaultProps = defaultProps;

export default DetailedValue;
