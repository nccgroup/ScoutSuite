import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, convertBoolToEnable, valueOrNone } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const SecurityContacts = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="Name" valuePath="name" />

        <PartialValue label="Email" valuePath="email" />

        <PartialValue
          label="Phone"
          valuePath="phone"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Notify on Alert"
          valuePath="alert_notifications"
          renderValue={convertBoolToEnable}
        />

        <PartialValue
          label="Notify Administrators on Alert"
          valuePath="alerts_to_admins"
          renderValue={convertBoolToEnable}
        />
      </InformationsWrapper>
    </Partial>
  );
};

SecurityContacts.propTypes = propTypes;

export default SecurityContacts;
