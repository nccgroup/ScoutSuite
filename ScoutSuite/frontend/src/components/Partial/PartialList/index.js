import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import PartialValue from '../PartialValue/';
import { PartialContext, PartialPathContext } from '../context';
import { concatPaths } from '../../../utils/Partials';

import './style.scss';
import { PartialSection } from '..';

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

  if (!items || items.length === 0) return <ul><li>None</li></ul>;

  return (
    <PartialSection path={valuePath}>
      <ul className="partial-list">
        {list.map((item, i) => {
          if (renderItem) return renderItem(item); 

          const path = item.key ? item.key : '';

          console.log('PATH', )

          return <li key={i}><PartialValue valuePath={path} /></li>;
        })}
      </ul>
    </PartialSection>
  );
};

PartialList.propTypes = propTypes;

export default PartialList;
