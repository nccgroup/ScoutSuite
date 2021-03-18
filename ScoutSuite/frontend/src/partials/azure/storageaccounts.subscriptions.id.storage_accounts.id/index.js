import React from 'react';
import { PropTypes } from 'prop-types';
import isEmpty from 'lodash/isEmpty';
import get from 'lodash/get';

import { Partial } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import PartialValue from '../../../components/Partial/PartialValue/index';
import {
  convertBoolToEnable,
  convertValueOrNever,
  convertListToChips,
} from '../../../utils/Partials/index';
import { TabPane, TabsMenu } from '../../../components/Tabs';
import PartialTable from '../../../components/Partial/PartialTable/index';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Bucket = (props) => {
  const { data } = props;

  if (!data) return null;

  const blobColumns = [
    {
      name: 'Key',
      key: 'key',
    },
    {
      name: 'Public Access',
      key: 'public_access_allowed',
    },
  ];

  const blobRenderers = { public_access_allowed: convertBoolToEnable };

  const blob_containers = get(data, ['item', 'blob_containers']);

  return (
    <Partial data={data}>
      <div className="left-pane">
        <PartialValue label="Storage Account Name" path="name" />
        <PartialValue
          label="Public Traffic"
          path="public_traffic_allowed"
          renderValue={convertBoolToEnable}
        />
        <PartialValue
          label="HTTPS Required"
          path="https_traffic_enabled"
          renderValue={convertBoolToEnable}
        />
        <PartialValue
          label="Microsoft Trusted Services"
          path="trusted_microsoft_services_enabled"
          renderValue={convertBoolToEnable}
        />
        <PartialValue
          label="Last Access Key Rotation"
          path="access_keys_rotated"
          renderValue={convertValueOrNever}
        />
        <PartialValue
          label="Tags"
          path="tags"
          renderValue={convertListToChips}
        />
        <PartialValue
          label="Resource group"
          path="resource_group_name"
          renderValue={convertValueOrNever}
        />
      </div>

      <TabsMenu>
        <TabPane title="Blob Containers">
          {!isEmpty(blob_containers) ? (
            <PartialTable
              columns={blobColumns}
              path="blob_containers"
              formatters={blobRenderers}
            />
          ) : (
            <span>None</span>
          )}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Bucket.propTypes = propTypes;

export default Bucket;
