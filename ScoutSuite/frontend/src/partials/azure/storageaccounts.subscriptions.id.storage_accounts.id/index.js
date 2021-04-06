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
import { TabPane, TabsMenu } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const renderBlobContainer = data => {
  return (<div key={data.id}>
    <h2>{data.id}</h2>
    <ul>
      <li>
        Public Access: {convertBoolToEnable(data.public_access_allowed)}
      </li>
    </ul>
  </div>)
}
const renderBlobService = data => {
  return (<div key={data.id}>
    <h2>{data.name}</h2>
    <ul>
      <li>
        Soft Delete: {convertBoolToEnable(data.soft_delete_enabled)}
      </li>
    </ul>
  </div>)
}

const Bucket = (props) => {
  const { data } = props;

  if (!data) return null;


  const blob_containers = get(data, ['item', 'blob_containers']);
  const blob_services = get(data, ['item', 'blob_services']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Storage Account Name"
          path="name"
        />
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
          label="Storage encrypted with Customer Managed Key"
          path="encryption_key_customer_managed"
          renderValue={convertBoolToEnable}
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
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Blob Containers">
          {!isEmpty(blob_containers) ? (
            Object.values(blob_containers).map((value) =>
              renderBlobContainer(value)
            )
          ) : (
            <span>None</span>
          )}
        </TabPane>
        <TabPane title="Blob Services">
          {!isEmpty(blob_services) ? (
            Object.values(blob_services).map((value) =>
              renderBlobService(value)
            )
          ) : (
            <span>None</span>
          )}
        </TabPane>
      </TabsMenu>
    </Partial >
  );
};

Bucket.propTypes = propTypes;

export default Bucket;
