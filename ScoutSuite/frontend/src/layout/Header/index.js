import React from 'react';

import Logo from './ScoutSuiteLogo/logo.png'; 

import './style.scss';
import { Link } from '@reach/router';

const Header = () => {
  return (
    <div className="nav-header">
      <div className="content">
        <Link to="/"><img src={Logo} /></Link>
        <button>TEMP</button>
      </div>
    </div>
  );
};

export default Header;
