import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.arrayOf(PropTypes.element),
  ]).isRequired,
  isOpened: PropTypes.bool.isRequired,
  setOpened: PropTypes.func.isRequired,
};

const SubMenu = props => {
  const { 
    title,
    children,
    isOpened,
    setOpened,
  } = props;

  const className = cx('sub-menu', {'is-selected': isOpened});

  return (
    <li className={className}>
      <div className="title" onClick={() => setOpened(title)}>
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
