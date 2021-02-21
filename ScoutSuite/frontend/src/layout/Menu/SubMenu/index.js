import React, { useState } from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.arrayOf(PropTypes.element),
  ]).isRequired,
  isOpened: PropTypes.bool.isRequired,
};

const SubMenu = props => {
  const { 
    title,
    children,
    isOpened,
  } = props;

  const [isSelected, setIsSelected] = useState(isOpened);
  const className = cx('sub-menu', {'is-selected': isSelected});

  return (
    <li className={className}>
      <div className="title" onClick={() => setIsSelected(!isSelected)}>
        {title}
      </div>
      {isSelected && (
        <ul>
          {children}
        </ul>
      )}
    </li>
  );
};

SubMenu.propTypes = propTypes;

export default SubMenu;
