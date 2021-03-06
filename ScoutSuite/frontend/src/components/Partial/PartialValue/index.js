import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import cx from 'classnames';

import { PartialContext, PartialPathContext } from '../context';
import { concatPaths } from '../../../utils/Partials';

import './style.scss';

const propTypes = {
  path: PropTypes.string.isRequired,
  label: PropTypes.string,
  separator: PropTypes.string,
  errorPath: PropTypes.string,
  renderValue: PropTypes.func,
};

const defaultProps = {
  label: null,
  separator: ': ',
  errorPath: null,
  renderValue: value => value,
};

const PartialValue = props => {
  const {
    path,
    label,
    separator,
    errorPath,
    renderValue,
  } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);

  const fullPath = concatPaths(basePath, path);
  const value = get(ctx.item, fullPath);
  
  const fullErrorPath = errorPath ? concatPaths(basePath, errorPath) : fullPath;
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
