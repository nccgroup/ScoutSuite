import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import './style.scss'

const propTypes = {
  tabs: PropTypes.objectOf(PropTypes.string).isRequired,
  selectedTab: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
}

const TabsMenu = props => {
  const {
    tabs, 
    selectedTab,
    onClick,
  } = props;

  return (
    <div className="tabs-menu">
      {Object.entries(tabs).map(([key, tabName]) => (
        <span 
          className={cx('tab', {'is-selected': selectedTab === tabName})}
          onClick={onClick}
          value={tabName}
          key={key}
        >
          {tabName}
        </span>
      ))}
    </div>
  );
}

TabsMenu.propTypes = propTypes;

export default TabsMenu;
