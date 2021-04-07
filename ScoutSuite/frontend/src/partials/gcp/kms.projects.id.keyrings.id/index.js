import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import PartialSection from '../../../components/Partial/PartialSection/index';
import { formatDate, valueOrNone } from '../../../utils/Partials/index';
import InformationsWrapper from '../../../components/InformationsWrapper';

const renderKeys = keys => {
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
                  label="State"
                  valuePath="state" />
              </li>
              <li>
                <PartialValue
                  label="Protection Level"
                  valuePath="protection_level" />
              </li>
              <li>
                <PartialValue
                  label="Algorithm"
                  valuePath="algorithm"
                />
              </li>
              <li>
                <PartialValue
                  label="Purpose"
                  valuePath="purpose"
                />
              </li>
              <li>
                <PartialValue
                  label="Purpose"
                  valuePath="purpose"
                />
              </li>
              <li>
                <PartialValue
                  label="Creation Date"
                  valuePath="creation_datetime"
                  renderValue={formatDate}
                />
              </li>
              <li>
                <PartialValue
                  label="Rotation Period"
                  valuePath="rotation_period"
                  renderValue={valueOrNone}
                />
              </li>
              <li>
                <PartialValue
                  label="Next Rotation Date"
                  valuePath="next_rotation_datetime"
                  renderValue={valueOrNone}
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

const Keyrings = props => {
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
          label="Project ID"
          errorPath="project_id"
          valuePath="project" />

        <PartialValue
          label="Location"
          valuePath="location" />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Keys">
          {renderKeys(item.keyrings)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Keyrings.propTypes = propTypes;

export default Keyrings;
