import React from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  children: PropTypes.element.isRequired,
};

const MenuElement = props => {
  const {
    children,
  } = props;

  return (
    <li className="menu-element">
      <div>{children}</div>
    </li>
  );
};

MenuElement.propTypes = propTypes;

export default MenuElement;
