import React, { useEffect, useState } from 'react';
import Switch from '@material-ui/core/Switch';
import { Link } from 'react-router-dom';

import Logo from './ScoutSuiteLogo/logo.png'; 

import './style.scss';

const Header = () => {
  const [darkMode, setDarkMode] = useState(localStorage.getItem('ss-theme') === 'dark');

  useEffect(() => {
    if (localStorage.getItem('ss-theme') === 'dark') {
      document.body.classList.add('dark-mode');
      setDarkMode(true);
    }
  }, []);

  const handleChange = (e) => {
    if (e.target.checked) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    setDarkMode(e.target.checked);
    localStorage.setItem('ss-theme', e.target.checked ? 'dark' : 'light');
  };

  return (
    <div className="nav-header">
      <div className="content">
        <Link to="/"><img src={Logo} /></Link>
        <Switch
          checked={darkMode}
          onChange={handleChange}
          label="Dark Mode"
          labelplacement="start"
        />
      </div>
    </div>
  );
};

export default Header;
