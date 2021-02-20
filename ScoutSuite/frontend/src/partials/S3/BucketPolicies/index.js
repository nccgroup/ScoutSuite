import React from 'react';

import { TabsMenu, TabPane } from '../../../components/Tabs';

import './style.scss';

const BucketPolicies = () => {
  return (
    <TabsMenu className="bucket-policies">
      <TabPane title="Bucket ACLs">
        <table>
          <thead>
            <tr>
              <th/>
              <th>List</th>
              <th>Upload/Delete</th>
              <th>View Permissions</th>
              <th>Edit Permissions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>rami.mccarthy+BASCworkshop</td>
              <td>&#10003;</td>
              <td>&#10003;</td>
              <td>&#10003;</td>
              <td>&#10003;</td>
            </tr>
          </tbody>
        </table>
      </TabPane>
      <TabPane title="Groups">
        <div>groups</div>
      </TabPane>
      <TabPane title="Roles">
        <div>roles</div>
      </TabPane>
      <TabPane title="Users">
        <div>users</div>
      </TabPane>
    </TabsMenu>
  );
};

export default BucketPolicies;
