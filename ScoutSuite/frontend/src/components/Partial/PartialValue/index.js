import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import cx from 'classnames';

import { PartialContext, PartialPathContext } from '../context';
import { concatPaths } from '../../../utils/Partials';

import './style.scss';

const propTypes = {
  label: PropTypes.string,
  separator: PropTypes.string,
  value: PropTypes.any,
  valuePath: PropTypes.string,
  errorPath: PropTypes.string,
  renderValue: PropTypes.func,
};

const defaultProps = {
  label: null,
  separator: ': ',
  value: null,
  valuePath: null,
  errorPath: null,
  renderValue: value => value,
};

const PartialValue = props => {
  const {
    label,
    separator,
    valuePath,
    errorPath,
    renderValue,
  } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);

  const fullValuePath = concatPaths(basePath, valuePath);
  const value = props.value || get(ctx.item, fullValuePath);

  if (value === undefined || value === null) {
    return null;
  }
  
  const fullErrorPath = errorPath ? concatPaths(basePath, errorPath) : fullValuePath;
  const hasError = ctx.path_to_issues.includes(fullErrorPath);

  return (
    <div className="partial-value detailed-value"> 
      {label && (
        <span className="label">
          {`${label}${separator}`}
        </span>
      )}
      <span className={cx('value', hasError && 'error')}>
        {renderValue(value)}
      </span>
    </div>
  );
};

PartialValue.propTypes = propTypes;
PartialValue.defaultProps = defaultProps;

export default PartialValue;
