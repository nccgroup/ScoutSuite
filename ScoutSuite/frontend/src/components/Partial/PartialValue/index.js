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
  label: PropTypes.string,
  separator: PropTypes.string,
  value: PropTypes.any,
  valuePath: PropTypes.string,
  errorPath: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.arrayOf(PropTypes.string),
  ]),
  className: PropTypes.string,
  tooltip: PropTypes.bool,
  tooltipProps: PropTypes.object,
  renderValue: PropTypes.func,
  baseErrorPath: PropTypes.string,
};

const defaultProps = {
  label: '',
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
    className,
    tooltip,
    tooltipProps,
    renderValue,
    baseErrorPath
  } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const setIssueLevel = useContext(PartialTabContext);

  const fullValuePath = concatPaths(typeof baseErrorPath !== 'undefined' ? baseErrorPath  : basePath, valuePath);
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
    <span className={cx(hasError && cx('issue', level))}>
      {value}
    </span>
  );

  return (
    <DetailedValue
      className={cx(className, 'partial-value')}
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
