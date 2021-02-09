import React, { useState } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import './style.scss'

const propTypes = {
  children: PropTypes.array.isRequired,
}

const TabsMenu = props => {
  const { children } = props;

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
}

TabsMenu.propTypes = propTypes;

export default TabsMenu;
