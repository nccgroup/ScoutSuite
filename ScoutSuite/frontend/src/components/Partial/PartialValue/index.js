import React, { useContext, useEffect } from 'react';
import PropTypes from 'prop-types';
import Tooltip from '@material-ui/core/Tooltip';
import cx from 'classnames';
import get from 'lodash/get';
import isArray from 'lodash/isArray';

import { 
  PartialContext, 
  PartialPathContext,
  PartialTabContext,
} from '../context';
import { concatPaths } from '../../../utils/Partials';

import './style.scss';

const propTypes = {
  label: PropTypes.string,
  separator: PropTypes.string,
  value: PropTypes.any,
  valuePath: PropTypes.string,
  errorPath: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.arrayOf(PropTypes.string),
  ]),
  tooltip: PropTypes.bool,
  tooltipProps: PropTypes.object,
  renderValue: PropTypes.func,
};

const defaultProps = {
  label: null,
  separator: ': ',
  value: null,
  valuePath: null,
  errorPath: null,
  tooltip: false,
  tooltipProps: {
    enterDelay: 1000,
    placement: 'top-start',
  },
  renderValue: value => value,
};

const PartialValue = props => {
  const {
    label,
    separator,
    valuePath,
    errorPath,
    tooltip,
    tooltipProps,
    renderValue,
  } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const setIssueLevel = useContext(PartialTabContext);

  const fullValuePath = concatPaths(basePath, valuePath);
  const value = renderValue(props.value || get(ctx.item, fullValuePath));

  if (value === undefined || value === null) {
    return null;
  }

  let fullErrorPaths;
  if (errorPath) {
    const paths = isArray(errorPath) ? errorPath : [errorPath];
    fullErrorPaths = paths.map(path => concatPaths(basePath, path));
  } else {
    fullErrorPaths = [fullValuePath];
  }

  const hasError = fullErrorPaths.some(path => ctx.path_to_issues.includes(path));
  const level = ctx.level;

  if (hasError) {
    useEffect(
      () => {
        setIssueLevel(level);
      },
      [hasError],
    );
  }

  const content = (
    <span className={cx('value', hasError && level)}>
      {value}
    </span>
  );

  return (
    <div className="partial-value detailed-value"> 
      {label && (
        <span className="label">
          {`${label}${separator}`}
        </span>
      )}
      {tooltip ? (
        <Tooltip title={value} {...tooltipProps}>
          {content}
        </Tooltip>
      ) : 
        content
      }
    </div>
  );
};

PartialValue.propTypes = propTypes;
PartialValue.defaultProps = defaultProps;

export default PartialValue;
