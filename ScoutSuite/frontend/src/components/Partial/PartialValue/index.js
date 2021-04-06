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
import DetailedValue from '../../DetailedValue';

import './style.scss';

const propTypes = {
  label: PropTypes.node,
  separator: PropTypes.string,
  value: PropTypes.any,
  valuePath: PropTypes.string,
  errorPath: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.arrayOf(PropTypes.string),
  ]),
  inline: PropTypes.bool,
  className: PropTypes.string,
  tooltip: PropTypes.bool,
  tooltipProps: PropTypes.object,
  renderValue: PropTypes.func,
};

const defaultProps = {
  label: '',
  separator: ': ',
  value: null,
  valuePath: null,
  errorPath: null,
  inline: false,
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
    className,
    inline,
    tooltip,
    tooltipProps,
    renderValue,
  } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const setIssueLevel = useContext(PartialTabContext);

  const fullValuePath = concatPaths(basePath, valuePath);
  let value = renderValue(
    props.value || get(ctx.item, fullValuePath, props.value)
  );

  if (typeof value === 'boolean') {
    value = String(value);
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

  useEffect(
    () => {
      if (hasError) {
        setIssueLevel(level);
      }
    },
    [level],
  );

  if (value === undefined || value === null) {
    return null;
  }

  const content = (
    <span className={cx(hasError && cx('issue', level))}>
      {value}
    </span>
  );

  return (
    <DetailedValue
      className={cx(className, 'partial-value', { inline })}
      label={label}
      separator={separator}
      value={
        tooltip ? (
          <Tooltip title={value} {...tooltipProps}>
            {content}
          </Tooltip>
        ) : 
          content
      }
    />
  );
};

PartialValue.propTypes = propTypes;
PartialValue.defaultProps = defaultProps;

export default PartialValue;
