import React from 'react';
import Switch from '@material-ui/core/Switch';
import { Link } from '@reach/router';

import Logo from './ScoutSuiteLogo/logo.png'; 

import './style.scss';

const Header = () => {
  const [darkMode, setDarkMode] = React.useState(false);

  const handleChange = (e) => {
    document.body.classList.toggle('dark-mode');
    setDarkMode(e.target.checked);
  };

  return (
    <div className="nav-header">
      <div className="content">
        <Link to="/"><img src={Logo} /></Link>
        <Switch
          checked={darkMode}
          onChange={handleChange}
          label="Dark Mode"
          labelPlacement="start"
        />
      </div>
    </div>
  );
};

export default Header;
