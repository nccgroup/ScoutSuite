import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.arrayOf(PropTypes.element),
  ]).isRequired,
  opened: PropTypes.string,
  setOpened: PropTypes.func.isRequired,
};

const SubMenu = props => {
  const { 
    title,
    children,
    opened,
    setOpened,
  } = props;

  const isOpened = opened === title;
  const className = cx('sub-menu', {'is-selected': isOpened});

  const toggle = () => {
    setOpened(opened !== title ? title : null);
  };

  return (
    <li className={className}>
      <div className="title" onClick={toggle}>
        {title}
      </div>
      {isOpened && (
        <ul>
          {children}
        </ul>
      )}
    </li>
  );
};

SubMenu.propTypes = propTypes;

export default SubMenu;
