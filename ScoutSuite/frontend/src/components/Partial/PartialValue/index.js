import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import Tooltip from '@material-ui/core/Tooltip';
import cx from 'classnames';
import get from 'lodash/get';

import { PartialContext, PartialPathContext } from '../context';
import { concatPaths } from '../../../utils/Partials';

import './style.scss';

const propTypes = {
  label: PropTypes.string,
  separator: PropTypes.string,
  value: PropTypes.any,
  valuePath: PropTypes.string,
  errorPath: PropTypes.string,
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

  const fullValuePath = concatPaths(basePath, valuePath);
  const value = renderValue(props.value || get(ctx.item, fullValuePath));

  if (value === undefined || value === null) {
    return null;
  }
  
  const fullErrorPath = errorPath ? concatPaths(basePath, errorPath) : fullValuePath;
  const hasError = ctx.path_to_issues.includes(fullErrorPath);
  const level = ctx.level;

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
