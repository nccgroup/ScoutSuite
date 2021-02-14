import React, { useState } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isArray from 'lodash/isArray';

import './style.scss';

const propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.arrayOf(PropTypes.element),
  ]).isRequired,
};

const TabsMenu = props => {
  const children = isArray(props.children) ? props.children : [props.children];

  const [ selectedTab, setSelectedTab ] = useState(0);
  const content = get(children[selectedTab], ['props', 'children']);

  return (
    <>
      <div className="tabs-menu">
        {children.map((child, i) => React.cloneElement(child, {
          isSelected: i === selectedTab,
          key: i,
          onClick: () => setSelectedTab(i),
        }))}
      </div>
      <div className="tab-content">
        {React.isValidElement(content) && content}
      </div>
    </>
  );
};

TabsMenu.propTypes = propTypes;

export default TabsMenu;
