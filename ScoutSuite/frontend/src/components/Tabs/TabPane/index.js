import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import './style.scss';

const propTypes = {
  title: PropTypes.string.isRequired,
  isSelected: PropTypes.bool,
  onClick: PropTypes.func,
};

const TabPane = (props) => {
  const { title, isSelected, onClick } = props;

  const className = cx('tab-pane', { 'is-selected': isSelected });

  return (
    <span className={className} onClick={onClick}>
      {title}
    </span>
  );
};

TabPane.propTypes = propTypes;

export default TabPane;
