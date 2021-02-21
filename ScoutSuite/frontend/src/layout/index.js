import React from 'react';
import PropTypes from 'prop-types';

import { useAPI } from '../api/useAPI';
import { getServices } from '../api/paths';
import Header from './Header';
import { MenuBar, SubMenu, MenuGroup, MenuElement } from './Menu';
import Breadcrumb from '../components/Breadcrumb';

import './style.scss';
import { getDashboardName } from '../utils/Dashboard';
import { getDashboardLink } from '../utils/Dashboard/index';
import { useParams, Link } from '@reach/router';

const propTypes = {
  children: PropTypes.element.isRequired,
};

const Layout = (props) => {
  const { data: categories, loading } = useAPI(getServices());
  const { children } = props;
  const params = useParams();

  if (loading) return null;

  return (
    <div className="main-layout">
      <Header />

      <MenuBar>
        <MenuElement>
          <span>
            <Link to="/">Home</Link>
          </span>
        </MenuElement>
        {categories.map((category) => {
          const isOpened = !!category.services.find(
            (service) => service.id === params.service,
          );

          return (
            <SubMenu
              title={category.name}
              isOpened={isOpened}
              key={category.id}
            >
              <MenuGroup title="Summaries" size="large">
                {category.services.map((service) => (
                  <MenuGroup title={`${service.name}`} key={service.id}>
                    {service.dashboards.map((dashboard) => (
                      <MenuElement
                        link={getDashboardLink(dashboard, service.id)}
                        key={dashboard}
                      >
                        <span>{getDashboardName(dashboard)}</span>
                      </MenuElement>
                    ))}
                  </MenuGroup>
                ))}
              </MenuGroup>

              <MenuGroup title="Resources" size="large">
                {category.services.map((service) => (
                  <MenuElement key={service.id}>
                    <span>{service.name}</span>
                  </MenuElement>
                ))}
              </MenuGroup>
            </SubMenu>
          );
        })}
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
