import React from 'react';
import { PropTypes } from 'prop-types';

import Header from './Header';
import Menu from './Menu';
import Breadcrumb from '../components/Breadcrumb';

import './style.scss';


const propTypes = {
  children: PropTypes.elem
};


const Layout = (props) => {
  const { children } = props;

  return (
    <div className="main-layout">
      <Header />
      <Menu />
      <div className="main">
        <Breadcrumb />
        {children}
      </div>
    </div>
  );
};

Layout.propTypes = propTypes;

export default Layout;
