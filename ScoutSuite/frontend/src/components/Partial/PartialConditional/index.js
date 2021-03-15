import { useContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { PartialContext, PartialPathContext } from '../context';
import { concatPaths } from '../../../utils/Partials';

const propTypes = {
  valuePath: PropTypes.string.isRequired,
  equalsTo: PropTypes.string,
  notEqualTo: PropTypes.string,
  children: PropTypes.element.isRequired,
  fallback: PropTypes.element,
};

const PartialConditional = (props) => {
  const { valuePath, eq, neq, children, fallback } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);

  const fullPath = concatPaths(basePath, valuePath);
  const item = get(ctx.item, fullPath);

  const validItem = Array.isArray(item) ? item && item.length > 0 : !!item;

  if (
    (eq && eq === item) ||
    (neq && neq !== item) ||
    (!eq && !neq && validItem)
  )
    return children;

  return fallback || null;
};

PartialConditional.propTypes = propTypes;

export default PartialConditional;
