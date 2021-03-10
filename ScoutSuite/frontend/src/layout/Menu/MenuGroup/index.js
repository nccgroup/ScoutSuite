import React from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.array,
  ]).isRequired,
};


const MenuGroup = props => {
  const {
    title,
    children,
  } = props;

  return (
    <li className="menu-group">
      <div className="title">
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
