import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import BarChartIcon from '@material-ui/icons/BarChart';
import DevicesOtherIcon from '@material-ui/icons/DevicesOther';
import { useLocation } from 'react-router-dom';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import Dialog from '@material-ui/core/Dialog';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';

import { useAPI } from '../api/useAPI';
import { getDashboardName, getDashboardLink } from '../utils/Dashboard';
import { getServicesEndpoint } from '../api/paths';
import Header from './Header';
import { MenuBar, SubMenu, MenuGroup, MenuElement } from './Menu';
import DownloadException from '../components/Exceptions/DownloadButton';

import './style.scss';


const propTypes = {
  children: PropTypes.node.isRequired,
};

const Layout = props => {
  const location = useLocation();
  const [opened, setOpened] = useState(null);
  const [selected, setSelected] = useState(null);
  const { data: categories, loading } = useAPI(getServicesEndpoint());
  const { children } = props;
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };

  useEffect(() => {
    if (categories) {
      const service = location.pathname.match(/^\/services\/(.*?)\//);
      const navOpen = categories.find(({ services }) =>
        services.map(s => s.id).includes(service ? service[1] : null),
      );
      const pathParts = location.pathname.split('/');
      const selected = pathParts.slice(0, 5).join('/');
      setSelected(selected);
      setOpened(navOpen ? navOpen.name : null);
    }
  }, [categories, location.pathname]);

  if (loading) return null;

  return (
    <>
      <div className="main-layout">
        <Header />
        <MenuBar>
          {categories.map(category => {
            return (
              <SubMenu
                title={category.name}
                opened={opened}
                setOpened={setOpened}
                key={category.id}
              >
                {category.services.map(service => (
                  <MenuGroup
                    title={service.name} key={service.id}
                    size="large">
                    {service.dashboards.map(dashboard => (
                      <MenuElement
                        link={getDashboardLink(dashboard, service.id)}
                        key={dashboard}
                        selected={selected}
                      >
                        <BarChartIcon fontSize="inherit" />{' '}
                        <span>{getDashboardName(dashboard)}</span>
                      </MenuElement>
                    ))}

                    {service.resources.map(res => (
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
            );
          })}
          <DownloadException />
          <div className="about-scout" onClick={handleClickOpen}>
            <InfoOutlinedIcon /> About Scout Suite
          </div>
        </MenuBar>
        <div className="main">{children}</div>
      </div>

      <Dialog
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={open}
      >
        <div className="modal-title" onClose={handleClose}>
          <h2>About Scout Suite</h2>
          <IconButton aria-label="close" onClick={handleClose}>
            <CloseIcon />
          </IconButton>
        </div>
        <div className="modal-content">
          <p>Scout Suite is an open-source tool released by <a href="https://www.nccgroup.trust/">NCC Group</a>.</p>
          <p>Use the top navigation bar to review the configuration of the supported cloud provider services.</p>
          <p>For more information about Scout Suite, please check out the {'project\'s'} page on <a href="https://github.com/nccgroup/ScoutSuite">GitHub</a>.</p>
        </div>
      </Dialog>
    </>
  );
};

Layout.propTypes = propTypes;

export default Layout;
