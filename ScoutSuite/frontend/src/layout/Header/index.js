import React from 'react';

import Logo from './ScoutSuiteLogo/logo.png'; 

import './style.scss';

const Header = () => {
  return (
    <div className="nav-header">
      <div className="content">
        <img src={Logo} />
        <button>TEMP</button>
      </div>
    </div>
  );
}

export default Header;
