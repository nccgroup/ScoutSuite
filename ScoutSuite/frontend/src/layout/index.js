import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import BarChartIcon from '@material-ui/icons/BarChart';
import DevicesOtherIcon from '@material-ui/icons/DevicesOther';

import { useAPI } from '../api/useAPI';
import { 
  getDashboardName,
  getDashboardLink,
} from '../utils/Dashboard';
import { getServicesEndpoint } from '../api/paths';
import Header from './Header';
import { MenuBar, SubMenu, MenuGroup, MenuElement } from './Menu';

import './style.scss';


const propTypes = {
  children: PropTypes.node.isRequired,
};

const Layout = (props) => {
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
      setOpened(navOpen ? navOpen.name : null);
    }
  }, [categories]);

  if (loading) return null;

  return (
    <div className="main-layout">
      <Header />
      <MenuBar>
        {categories.map((category) => {
          return (
            <SubMenu
              title={category.name}
              opened={opened}
              setOpened={setOpened}
              key={category.id}
            >
              {category.services.map((service) => (
                <MenuGroup title={service.name} key={service.id} size="large">
                  {service.dashboards.map((dashboard) => (
                    <MenuElement
                      link={getDashboardLink(dashboard, service.id)}
                      key={dashboard}
                      selected={selected}
                      setSelected={setSelected}
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
                      setSelected={setSelected}
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
          );
        })}
      </MenuBar>
      <div className="main">{children}</div>
    </div>
  );
};

Layout.propTypes = propTypes;

export default Layout;
