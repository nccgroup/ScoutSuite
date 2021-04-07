import React, { useMemo } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import Skeleton from '@material-ui/lab/Skeleton';
import {Link} from 'react-router-dom';

import { Partial, PartialSection, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import {
  partialDataShape,
  formatDate,
  convertBoolToEnable,
} from '../../../utils/Partials';
import {useResources} from '../../../api/useResources';
import InformationsWrapper from '../../../components/InformationsWrapper';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const renderInstances = (items) => {
  if (!items || items.length === 0) return <span>None</span>;

  return <ul>
    {items.map((item, i) => <li key={i}><Link to={`/services/computeengine/resources/instances/${item.id}`}>
      {item.name}
    </Link></li>)}
  </ul>;
};

const Subnetworks = props => {
  const { data } = props;
  const item = get(data, ['item'], {});

  const instanceList = useMemo(() =>  item.instances ? item.instances.map(({ instance_id }) => instance_id) : [], [data]);
  const { data: instances , loading: instancesLoading } = useResources('computeengine', 'instances', instanceList);

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name"
          valuePath="name" />

        <PartialValue
          label="ID"
          valuePath="id" />

        <PartialValue
          label="Project ID"
          valuePath="project_id" />

        <PartialValue
          label="Region"
          valuePath="region" />

        <PartialValue
          label="Creation Date"
          valuePath="creation_timestamp"
          renderValue={formatDate}
        />

        <PartialValue
          label="IP Range"
          valuePath="ip_range" />

        <PartialValue
          label="Gateway Address"
          valuePath="gateway_address" />

        <PartialValue
          label="Private Google Access"
          valuePath="private_ip_google_access"
          renderValue={convertBoolToEnable}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Compute Engine Instances">
          <PartialSection path="instances">
            {renderInstances(instances)}
            {instancesLoading && <Skeleton />}
          </PartialSection>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Subnetworks.propTypes = propTypes;

export default Subnetworks;
