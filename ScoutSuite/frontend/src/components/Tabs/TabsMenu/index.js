import React, { useState } from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import Tabs from '@material-ui/core/Tabs';
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
        <Tabs
          variant="scrollable"
          scrollButtons="auto"
        >
          {children.map((child, i) => (
            <div key={i}>
              {React.cloneElement(child, {
                isSelected: i === selectedTab,
                onClick: () => setSelectedTab(i),
              })}
            </div>
          ))}
        </Tabs>
      </div>
      <div className="tab-content">
        {content}
      </div>
    </div>
  );
};

TabsMenu.propTypes = propTypes;
TabsMenu.defaultProps = defaultProps;

export default TabsMenu;
