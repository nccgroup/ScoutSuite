import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import cx from 'classnames';

import { PartialContext, PartialPathContext } from '../context';


const propTypes = {
  label: PropTypes.string.isRequired,
  path: PropTypes.string.isRequired,
  separator: PropTypes.string,
  renderValue: PropTypes.func,
};

const defaultProps = {
  separator: ': ',
  renderValue: value => value,
};

const PartialValue = props => {
  const {
    label,
    path,
    separator,
    renderValue,
  } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);

  const fullPath = basePath + path;
  const value = get(ctx.item, fullPath);

  console.log('CTX', ctx, basePath, fullPath, value);

  if (value === undefined || value === null) {
    return null;
  }
  
  const hasError = ctx.path_to_issues.includes(fullPath);

  return (
    <div className="detailed-value"> 
      <span className="label">{`${label}${separator}`}</span>
      <span className={cx('value', hasError && 'error')}>{renderValue(value)}</span>
    </div>
  );
};

PartialValue.propTypes = propTypes;
PartialValue.defaultProps = defaultProps;

export default PartialValue;
