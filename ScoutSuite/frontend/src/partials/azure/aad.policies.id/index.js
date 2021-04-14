import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { convertBoolToEnable, partialDataShape, valueOrNone } from '../../../utils/Partials';



const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Policies = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name" valuePath="name"
          renderValue={valueOrNone} />
        <PartialValue
          label="Allow Invites From" valuePath="allow_invites_from"
          renderValue={valueOrNone} />
        <PartialValue
          label="Allowed To Create Apps" valuePath="allowed_to_create_apps"
          renderValue={convertBoolToEnable} />
        <PartialValue
          label="Allowed To Create Security Groups" valuePath="allowed_to_create_security_groups"
          renderValue={convertBoolToEnable} />
        <PartialValue
          label="Allowed To Read Other Users" valuePath="allowed_to_read_other_users"
          renderValue={convertBoolToEnable} />
        <PartialValue
          label="Allow Email Verified Users To Join Organization" valuePath="allow_email_verified_users_to_join_organization"
          renderValue={convertBoolToEnable} />

      </InformationsWrapper>
    </Partial>
  );
};

Policies.propTypes = propTypes;

export default Policies;
