import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import PartialValue from '../PartialValue/';
import { PartialContext, PartialPathContext } from '../context';
import { concatPaths } from '../../../utils/Partials';

import './style.scss';

const propTypes = {
  valuePath: PropTypes.string.isRequired,
  renderItem: PropTypes.func,
  values: PropTypes.arrayOf(PropTypes.any)
};

const PartialList = (props) => {
  const { valuePath, renderItem, values } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);

  const fullPath = concatPaths(basePath, valuePath);
  const items = values ? values: get(ctx.item, fullPath);
  const list = Array.isArray(items)
    ? items.map((item, i) => ({ key: i, item }))
    : Object.entries(items).map(([key, item]) => ({ key, item }));

  if (items.length === 0) return <span>None</span>;

  return (
    <ul className="partial-list">
      {list.map((item, i) => {
        if (renderItem) return renderItem(item); 

        const path = item.key ? valuePath + '.' + item.key : valuePath;

        return <PartialValue key={i} valuePath={path} />;
      })}
    </ul>
  );
};

PartialList.propTypes = propTypes;

export default PartialList;
