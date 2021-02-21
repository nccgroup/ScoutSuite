import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.arrayOf(PropTypes.element),
  ]).isRequired,
  type: PropTypes.string
};

const MenuGroup = props => {
  const {
    title,
    children,
    type
  } = props;

  return (
    <li className="menu-group">
      <div className={cx('title', type === 'parent' && 'lg')}>
        {title}
      </div>
      <ul className={cx(type !== 'parent' && 'child')}>
        {children}
      </ul>
    </li>
  );
};

MenuGroup.propTypes = propTypes;

export default MenuGroup;
