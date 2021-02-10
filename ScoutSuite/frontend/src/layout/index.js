import React from 'react';

import Header from './Header';
import Menu from './Menu';
import Content from './Content';

import './style.scss';

const Layout = () => {
  return (
    <div className="main-layout">
      <Header />
      <Menu />
      <div className="main">
        <Content />
      </div>
    </div>
  );
};

export default Layout;
