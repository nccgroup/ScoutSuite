import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import PartialSection from '../../../components/Partial/PartialSection/index';
import { formatDate, valueOrNone } from '../../../utils/Partials/index';
import InformationsWrapper from '../../../components/InformationsWrapper';

const renderKmsPolicy = policies => {

  if (isEmpty(policies)) return <ul><li>None</li></ul>;

  return (
    <ul>
      {Object.entries(policies).map(([key, policy]) => (
        <PartialSection
          path={`kms_iam_policy.${key}`}
          key={key}>
          <li>
            <b>{policy.name}</b>
            <ul>
              <li>
                <PartialValue
                  label="Title"
                  valuePath="title" />
              </li>
              <li>
                <PartialValue
                  label="Description"
                  valuePath="description" />
              </li>
              <li>
                <PartialValue
                  label="Custom Role"
                  valuePath="custom_role"
                />
              </li>
              <li>
                <PartialValue
                  label="Not anonymously or publicly accessible"
                  valuePath="anonymous_public_accessible"
                />
              </li>
            </ul>
          </li>
        </PartialSection>
      ))}
    </ul>
  );
};

const renderKeys = keys => {
  if (isEmpty(keys)) return <span>None</span>;

  return (
    <ul>
      {Object.entries(keys).map(([key, value]) => (
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
              <li>
                <PartialValue
                  label="Days Until Next Rotation"
                  valuePath="next_rotation_time_days"
                  renderValue={valueOrNone}
                />
              </li>
              <li><b>Bindings</b></li>
              {
                renderKmsPolicy(value.kms_iam_policy)
              }
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
          {renderKeys(item.keys)}
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Keyrings.propTypes = propTypes;

export default Keyrings;
