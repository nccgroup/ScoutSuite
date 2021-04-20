
import React from 'react';
import PropTypes from 'prop-types';

import { partialDataShape, valueOrNone } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const HostedZones = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div>
        <h4>Informations</h4>
        <PartialValue 
          label="ID"
          valuePath="id"
          renderValue={valueOrNone}
        />
        <PartialValue 
          label="Caller Reference"
          valuePath="caller_reference"
          renderValue={valueOrNone}
        />
        <PartialValue 
          label="Resource Record Set Count"
          valuePath="resource_record_set_count"
          renderValue={valueOrNone}
        />
      </div>
    </Partial>
  );
};

HostedZones.propTypes = propTypes;

export default HostedZones;
