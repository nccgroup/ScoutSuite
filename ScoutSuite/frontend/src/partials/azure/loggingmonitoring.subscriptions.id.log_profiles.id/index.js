import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const LogProfiles = props => {

  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name"
          valuePath="name"/>

        <PartialValue
          label="Storage Account ID"
          valuePath="storage_account_id" />

        <PartialValue
          label="Captures all activities"
          valuePath="captures_all_activities" />

        <PartialValue
          label="Retention policy enabled"
          valuePath="retention_policy_enabled" />

        <PartialValue
          label="Retention policy days"
          valuePath="retention_policy_days"/>

      </InformationsWrapper>
    </Partial>
  );
};

LogProfiles.propTypes = propTypes;

export default LogProfiles;
