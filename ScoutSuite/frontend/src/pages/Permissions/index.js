import React from 'react';
import { useParams } from 'react-router-dom';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../../api/useAPI';
import { getPermissionsEndpoint } from '../../api/paths';
import Breadcrumb from '../../components/Breadcrumb/index';
import { TabsMenu, TabPane } from '../../components/Tabs';
import PermissionsList from './PermissionsList';

import './style.scss';


const Permissions = () => {
  const { service } = useParams();

  const { data, loading } = useAPI(getPermissionsEndpoint(service), {});

  if (loading) return null;

  return (
    <>
      <Breadcrumb />
      <TabsMenu className="permissions">
        <TabPane
          title="Action Permissions"
          disabled={isEmpty(data.Action)}
        >
          <PermissionsList
            service={service} 
            list={data.Action}
          />
        </TabPane>
        <TabPane
          title="Not Action Permissions"
          disabled={isEmpty(data.NotAction)}
        >
          <PermissionsList 
            service={service}
            list={data.NotAction}
          />
        </TabPane>
      </TabsMenu>
    </>
  );
};

export default Permissions;
