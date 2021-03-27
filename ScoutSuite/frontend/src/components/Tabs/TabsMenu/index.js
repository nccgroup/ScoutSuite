import React, { useState } from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import get from 'lodash/get';
import isArray from 'lodash/isArray';

import './style.scss';


const propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
};

const defaultProps = {
  className: '',
};

const TabsMenu = props => {
  const { className } = props;
  let children = isArray(props.children) ? props.children : [props.children];
  children = children.filter(x => x);

  const [ selectedTab, setSelectedTab ] = useState(
    children.findIndex(tab => !tab.props.disabled)  // selects first non-disabled tab
  );
  const content = get(children[selectedTab], ['props', 'children']);

  return (
    <div className={cx(className, 'tabs')}>
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
    </div>
  );
};

TabsMenu.propTypes = propTypes;
TabsMenu.defaultProps = defaultProps;

export default TabsMenu;
