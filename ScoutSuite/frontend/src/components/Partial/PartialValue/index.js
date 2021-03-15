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
  baseErrorPath: PropTypes.string,
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
    baseErrorPath
  } = props;

  const ctx = useContext(PartialContext);
  const basePathCtx = useContext(PartialPathContext);

  const fullValuePath = concatPaths(typeof baseErrorPath !== 'undefined' ? baseErrorPath  : basePathCtx, valuePath);
  const value = renderValue(props.value || get(ctx.item, fullValuePath));

  if (value === undefined || value === null) {
    return null;
  }
  
  const fullErrorPath = errorPath ? concatPaths(typeof baseErrorPath !== 'undefined' ? baseErrorPath : basePathCtx, errorPath) : fullValuePath;
  const hasError = ctx.path_to_issues.includes(fullErrorPath);
  const level = ctx.level;

  console.info('error path', fullErrorPath, !!baseErrorPath);

  return (
    <div className="partial-value detailed-value"> 
      {label && (
        <span className="label">
          {`${label}${separator}`}
        </span>
      )}
      <span className={cx('value', hasError && level)}>
        {value}
      </span>
    </div>
  );
};

PartialValue.propTypes = propTypes;
PartialValue.defaultProps = defaultProps;

export default PartialValue;
