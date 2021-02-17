import React from 'react';
import PropTypes from 'prop-types';

import Header from './Header';
import { MenuBar, SubMenu, MenuGroup, MenuElement } from './Menu';
import Breadcrumb from '../components/Breadcrumb';

import './style.scss';

const propTypes = {
  children: PropTypes.element.isRequired,
};

const Layout = (props) => {
  const { children } = props;

  return (
    <div className="main-layout">
      <Header />
      <MenuBar>
        <MenuElement>
          <span>Home</span>
        </MenuElement>
        <SubMenu title="Analytics">
          <MenuGroup title="Summaries">
            <MenuElement>
              <span>Lambda</span>
            </MenuElement>
            <MenuElement>
              <span>EC2</span>
            </MenuElement>
            <MenuElement>
              <span>ELB</span>
            </MenuElement>
          </MenuGroup>
          <MenuGroup title="Resources">
            <MenuElement>
              <span>Lambda</span>
            </MenuElement>
            <MenuElement>
              <span>EC2</span>
            </MenuElement>
            <MenuElement>
              <span>ELB</span>
            </MenuElement>
          </MenuGroup>
        </SubMenu>
        <SubMenu title="Compute">
          <MenuGroup title="Summaries">
            <MenuElement>
              <span>Lambda</span>
            </MenuElement>
            <MenuElement>
              <span>EC2</span>
            </MenuElement>
            <MenuElement>
              <span>ELB</span>
            </MenuElement>
          </MenuGroup>
          <MenuGroup title="Resources">
            <MenuElement>
              <span>Lambda</span>
            </MenuElement>
            <MenuElement>
              <span>EC2</span>
            </MenuElement>
            <MenuElement>
              <span>ELB</span>
            </MenuElement>
          </MenuGroup>
        </SubMenu>
      </MenuBar>
      <div className="main">
        <Breadcrumb />
        {children}
      </div>
    </div>
  );
};

Layout.propTypes = propTypes;

export default Layout;
