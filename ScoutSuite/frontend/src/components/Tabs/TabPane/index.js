import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import Tab from '@material-ui/core/Tab';

import './style.scss';


const propTypes = {
  title: PropTypes.node.isRequired,
  className: PropTypes.string,
  isSelected: PropTypes.bool,
  disabled: PropTypes.bool,
  onClick: PropTypes.func,
  children: PropTypes.any.isRequired,
};

const TabPane = props => {
  const {
    title,
    className,
    isSelected,
    disabled,
    onClick,
    children,
  } = props;

  const classNames = cx(
    className,
    'tab-pane', 
    {
      'is-selected': isSelected,
      'disabled': disabled
    }
  );

  const tabOnClick = disabled ? null : onClick;

  return (
    <div>
      <Tab
        label={title}
        classes={{
          root: classNames,
        }}
        disableRipple
        onClick={tabOnClick}
      />
      <div className="hidden-content">
        {children}
      </div>
    </div>
  );
};

TabPane.propTypes = propTypes;

export default TabPane;
