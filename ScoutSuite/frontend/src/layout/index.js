import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import BarChartIcon from '@material-ui/icons/BarChart';
import DevicesOtherIcon from '@material-ui/icons/DevicesOther';
import { useLocation } from 'react-router-dom';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../api/useAPI';
import {
  getDashboardName,
  getCategoryDashboardLink,
  getServiceDashboardLink,
} from '../utils/Dashboard';
import { getServicesEndpoint } from '../api/paths';
import Header from './Header';
import { MenuBar, SubMenu, MenuGroup, MenuElement } from './Menu';
import DownloadException from '../components/Exceptions/DownloadButton';

import './style.scss';


const propTypes = {
  children: PropTypes.node.isRequired,
};

const Layout = (props) => {
  const location = useLocation();
  const [opened, setOpened] = useState(null);
  const [selected, setSelected] = useState(null);
  const { data: categories, loading } = useAPI(getServicesEndpoint());
  const { children } = props;

  useEffect(() => {
    if (categories) {
      const service = location.pathname.match(/^\/services\/(.*?)\//);
      const navOpen = categories.find(({ services }) =>
        services.map((s) => s.id).includes(service ? service[1] : null),
      );
      const pathParts = location.pathname.split('/');
      const selected = pathParts.slice(0,5).join('/');
      setSelected(selected);
      setOpened(navOpen ? navOpen.name : null);
    }
  }, [categories, location.pathname]);

  if (loading) return null;

  return (
    <div className="main-layout">
      <Header />
      <MenuBar>
        {categories.map((category) => (
          <SubMenu
            title={category.name}
            opened={opened}
            setOpened={setOpened}
            key={category.id}
          >
            {!isEmpty(category.dashboard) && (
              <MenuGroup
                title="Summaries"
                size="large"
              >
                {category.dashboard.map((dashboard, i) => (
                  <MenuElement
                    link={getCategoryDashboardLink(dashboard, category.id)}
                    selected={selected}
                    key={i}
                  >
                    <BarChartIcon fontSize="inherit" />{' '}
                    <span>{getDashboardName(dashboard)}</span>
                  </MenuElement>
                ))}
              </MenuGroup>
            )}
            {category.services.map(service => (
              <MenuGroup
                title={service.name} 
                size="large"
                key={service.id}
              >
                {service.dashboards.map((dashboard) => (
                  <MenuElement
                    link={getServiceDashboardLink(dashboard, service.id)}
                    selected={selected}
                    key={dashboard}
                  >
                    <BarChartIcon fontSize="inherit" />{' '}
                    <span>{getDashboardName(dashboard)}</span>
                  </MenuElement>
                ))}

                {service.resources.map((res) => (
                  <MenuElement
                    link={`services/${service.id}/resources/${res.id}`}
                    disabled={!res.count}
                    selected={selected}
                    key={res.id}
                  >
                    <DevicesOtherIcon fontSize="inherit" />{' '}
                    <span>
                      {res.name} ({res.count || 0})
                    </span>
                  </MenuElement>
                ))}
              </MenuGroup>
            ))}
          </SubMenu>
        ))}
        <DownloadException />
      </MenuBar>
      <div className="main">
        {children}
      </div>
    </div>
  );
};

Layout.propTypes = propTypes;

export default Layout;
