import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

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
    <div 
      className={classNames} 
      onClick={tabOnClick}
    >
      <span className="tab-title">
        {title}
      </span>
      <div className="tab-content">
        {children}
      </div>
    </div>
  );
};

TabPane.propTypes = propTypes;

export default TabPane;
