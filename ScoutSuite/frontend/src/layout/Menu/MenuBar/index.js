import React from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  children: PropTypes.node.isRequired,
};

const MenuBar = props => {
  const { children } = props;

  return (
    <ul className="menu-bar">
      {children}
    </ul>
  );
};

MenuBar.propTypes = propTypes;

export default MenuBar;
