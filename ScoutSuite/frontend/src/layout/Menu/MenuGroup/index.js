import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.arrayOf(PropTypes.element),
  ]).isRequired,
  size: PropTypes.string
};

const MenuGroup = props => {
  const {
    title,
    children,
    size
  } = props;

  return (
    <li className="menu-group">
      <div className={cx('title', size === 'large' && 'lg')}>
        {title}
      </div>
      <ul>
        {children}
      </ul>
    </li>
  );
};

MenuGroup.propTypes = propTypes;

export default MenuGroup;
