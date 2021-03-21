import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import './style.scss';

const propTypes = {
  title: PropTypes.string.isRequired,
  isSelected: PropTypes.bool,
  disabled: PropTypes.bool,
  onClick: PropTypes.func,
};

const TabPane = props => {
  const {
    title,
    isSelected,
    disabled,
    onClick,
  } = props;

  const className = cx(
    'tab-pane', 
    {
      'is-selected': isSelected,
      'disabled': disabled
    }
  );

  const tabOnClick = disabled ? null : onClick;

  return (
    <span className={className} onClick={tabOnClick}>
      {title}
    </span>
  );
};

TabPane.propTypes = propTypes;

export default TabPane;
