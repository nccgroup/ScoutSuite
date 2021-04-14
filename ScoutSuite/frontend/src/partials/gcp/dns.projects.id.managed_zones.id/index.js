import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import PartialSection from '../../../components/Partial/PartialSection/index';
import { formatDate, convertBoolToEnable } from '../../../utils/Partials/index';
import InformationsWrapper from '../../../components/InformationsWrapper';

const renderDnssecKeys = keys => {
  if (!keys || keys.length === 0) return <span>None</span>;

  return (
    <ul>
      {Object.entries(keys).map(([key]) => (
        <PartialSection
          path={`keys.${key}`}
          key={key}>
          <li>
            <b>{key}</b>
            <ul>
              <li>
                <PartialValue
                  label="Key Algorithm"
                  valuePath="key_algorithm" />
              </li>
              <li>
                <PartialValue
                  label="Key Type"
                  valuePath="key_type" />
              </li>
              <li>
                <PartialValue
                  label="Length"
                  valuePath="length"
                />
              </li>
            </ul>
          </li>
        </PartialSection>
      ))}
    </ul>
  );
};

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ManagedZones = props => {
  const { data } = props;
  const item = get(data, ['item'], {});

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
          label="Description"
          valuePath="description" />

        <PartialValue
          label="Creation Date"
          valuePath="creation_timestamp"
          renderValue={formatDate} />

        <PartialValue
          label="DNSSEC"
          valuePath="dnssec_enabled"
          renderValue={convertBoolToEnable} />

        <PartialValue
          label="Visibility"
          valuePath="visibility" />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Keys">
          {renderDnssecKeys(item.managed_zones)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

ManagedZones.propTypes = propTypes;

export default ManagedZones;
