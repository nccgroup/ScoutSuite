import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, convertBoolToEnable, formatDate } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import PartialList from '../../../components/Partial/PartialList';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const renderIAM = (iam) => {
  return <li>
    <PartialValue errorPath={iam.key} baseErrorPath="" value={iam.key} />
    <ul>{iam.item.map((item) => <li key={item}>{item}</li> )}</ul>
  </li>;
};

const renderACL = (acl) => {
  return <li>
    <PartialValue valuePath={acl.key + '.entity'} />
    <ul>
      <li><PartialValue valuePath={acl.key + '.role'} /></li>
    </ul>
  </li>;
};

const renderObjACL = (acl) => {
  return <li>
    <PartialValue valuePath={acl.key + '.entity'} />
    <ul>
      <li><PartialValue valuePath={acl.key + '.role'} /></li>
    </ul>
  </li>;
};

const Buckets = (props) => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="partial-informations">
        <PartialValue label="Project ID" valuePath="project_id" />

        <PartialValue
          label="Creation Date"
          valuePath="creation_date"
          renderValue={formatDate}
        />

        <PartialValue label="Location" valuePath="location" />

        <PartialValue label="Storage Class" valuePath="storage_class" />

        <PartialValue
          label="Logging"
          valuePath="logging_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Versioning"
          valuePath="versioning_enabled"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Uniform Bucket-Level Access"
          valuePath="uniform_bucket_level_access"
          renderValue={convertBoolToEnable}
        />
      </div>

      <TabsMenu>

        {/*TODO: Tab error highlight */}
        <TabPane title="IAM Permissions">
          <PartialList
            valuePath="member_bindings"
            renderItem={renderIAM} />
        </TabPane>

        <TabPane title="ACL Permissions">
          <PartialList
            valuePath="acls"
            renderItem={renderACL} />
        </TabPane>

        <TabPane title="Default Object ACL Permissions">
          <PartialList
            valuePath="default_object_acl"
            renderItem={renderObjACL} />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Buckets.propTypes = propTypes;

export default Buckets;
