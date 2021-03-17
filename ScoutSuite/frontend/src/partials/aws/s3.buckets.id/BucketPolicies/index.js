import React from 'react';

import { TabsMenu, TabPane } from '../../../../components/Tabs';
import { PartialSection } from '../../../../components/Partial';
import AccessControlList from './AccessControlList';
import PoliciesAccessTable from './PoliciesAccessTable';

import './style.scss';

const BucketPolicies = () => {
  return (
    <TabsMenu className="bucket-policies">
      <TabPane title="Bucket ACLs">
        <PartialSection path="grantees">
          <AccessControlList />
        </PartialSection>
      </TabPane>
      <TabPane title="Groups">
        <PartialSection path="groups">
          <PoliciesAccessTable columnName="Groups name"/>
        </PartialSection>
      </TabPane>
      <TabPane title="Roles">
        <PartialSection path="roles">
          <PoliciesAccessTable columnName="Roles name"/>
        </PartialSection>
      </TabPane>
      <TabPane title="Users">
        <PartialSection path="users">
          <PoliciesAccessTable columnName="Users name"/>
        </PartialSection>
      </TabPane>
    </TabsMenu>
  );
};

export default BucketPolicies;
