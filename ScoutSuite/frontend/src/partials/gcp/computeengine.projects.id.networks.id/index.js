import React, { useMemo } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import { Link } from 'react-router-dom';
import Skeleton from '@material-ui/lab/Skeleton';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, formatDate } from '../../../utils/Partials';
import { TabPane, TabsMenu } from '../../../components/Tabs';
import PartialSection from '../../../components/Partial/PartialSection/index';
import { useResources } from '../../../api/useResources';
import InformationsWrapper from '../../../components/InformationsWrapper';

const renderFirewalls = (items) => {
  return <ul>
    {items.map((item, i) => <li key={i}><Link to={`/services/computeengine/resources/firewalls/${item.id}`}>
      {item.name}
    </Link></li>)}
  </ul>;
};

const renderInstances = (items) => {
  return <ul>
    {items.map((item, i) => <li key={i}><Link to={`/services/computeengine/resources/instances/${item.id}`}>
      {item.name}
    </Link></li>)}
  </ul>;
};


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Networks = props => {
  const { data } = props;
  const item = get(data, ['item'], {});

  const { data: firewalls , loading: firewallLoading } = useResources('computeengine', 'firewalls', item.firewalls);
  const instanceList = useMemo(() => item.instances ? item.instances.map(({ instance_id }) => instance_id) : [], [item]);
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
          label="Description"
          valuePath="description" />

        <PartialValue
          label="Creation Date"
          valuePath="creation_timestamp"
          renderValue={formatDate}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Firewall Rules">
          <PartialSection path="firewalls">
            {renderFirewalls(firewalls)}
            {firewallLoading && <Skeleton />}
          </PartialSection>
        </TabPane>

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

Networks.propTypes = propTypes;

export default Networks;
