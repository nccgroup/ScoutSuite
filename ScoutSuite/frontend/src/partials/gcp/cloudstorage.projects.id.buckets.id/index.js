import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  convertBoolToEnable,
  formatDate,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';
import PartialSection from '../../../components/Partial/PartialSection/index';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const renderIAM = (iams) => {
  return (
    <ul>
      {iams.map(([key, iam]) => (
        <li key={key}>
          <PartialValue valuePath={key} value={key} />
          <ul>
            {iam.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </li>
      ))}
    </ul>
  );
};

const renderACL = (acls) => {
  return (
    <PartialSection path="acls">
      <ul>
        {acls.map((_, key) => (
          <li key={key}>
            <PartialValue valuePath={key + '.entity'} />
            <ul>
              <li>
                <PartialValue valuePath={key + '.role'} />
              </li>
            </ul>
          </li>
        ))}
      </ul>
    </PartialSection>
  );
};

const renderObjACL = (acls) => {
  return (
    <PartialSection path="default_object_acl">
      <ul>
        {acls.map((acl, key) => (
          <li key={key}>
            <PartialValue valuePath={key + '.' + acl.entity} />
            <ul>
              <li>
                <PartialValue valuePath={key + '.role'} />
              </li>
            </ul>
          </li>
        ))}
      </ul>
    </PartialSection>
  );
};

const Buckets = (props) => {
  const { data } = props;

  if (!data) return null;

  const member_bindings = get(data, ['item', 'member_bindings']);
  const acls = get(data, ['item', 'acls']);
  const default_object_acl = get(data, ['item', 'default_object_acl']);

  return (
    <Partial data={data}>
      <div>
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
      </div>

      <TabsMenu>
        {/*TODO: Tab error highlight */}

        <TabPane title="IAM Permissions">
          {!isEmpty(member_bindings) ? (
            renderIAM(Object.entries(member_bindings))
          ) : (
            <span>None</span>
          )}
        </TabPane>

        <TabPane title="ACL Permissions">
          {!isEmpty(acls) ? renderACL(acls) : <span>None</span>}
        </TabPane>

        <TabPane title="Default Object ACL Permissions">
          {!isEmpty(default_object_acl) ? (
            renderObjACL(default_object_acl)
          ) : (
            <span>None</span>
          )}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Buckets.propTypes = propTypes;

export default Buckets;
