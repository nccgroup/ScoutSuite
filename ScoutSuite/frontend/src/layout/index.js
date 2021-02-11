import React from 'react';

import Header from './Header';
import { MenuBar, SubMenu, MenuGroup, MenuElement } from './Menu';

import './style.scss';

const propTypes = {
  children: PropTypes.elem
};

const Layout = (props) => {
  const { children } = props;

  return (
    <div className="main-layout">
      <Header />
      <MenuBar>
        <MenuElement>Home</MenuElement>
        <SubMenu title="Analytics">
          <MenuGroup title="Summaries">
            <MenuElement>Lambda</MenuElement>
            <MenuElement>EC2</MenuElement>
            <MenuElement>ELB</MenuElement>
          </MenuGroup>
          <MenuGroup title="Resources">
            <MenuElement>Lambda</MenuElement>
            <MenuElement>EC2</MenuElement>
            <MenuElement>ELB</MenuElement>
          </MenuGroup>
        </SubMenu>
        <SubMenu title="Compute">
          <MenuGroup title="Summaries">
            <MenuElement>Lambda</MenuElement>
            <MenuElement>EC2</MenuElement>
            <MenuElement>ELB</MenuElement>
          </MenuGroup>
          <MenuGroup title="Resources">
            <MenuElement>Lambda</MenuElement>
            <MenuElement>EC2</MenuElement>
            <MenuElement>ELB</MenuElement>
          </MenuGroup>
        </SubMenu>
      </MenuBar>
      <div className="main">
        <Breadcrumb />
        {children}
      </div>
    </div>
  );
}

Layout.propTypes = propTypes;

export default Layout;
