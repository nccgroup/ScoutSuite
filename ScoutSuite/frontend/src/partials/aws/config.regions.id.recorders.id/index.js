import React from 'react';
import PropTypes from 'prop-types';

import { 
  partialDataShape,
  formatDate,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ConfigRecorders = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div>
        <h4>Informations</h4>
        <PartialValue
          label="Enabled"
          valuePath="enabled"
        />
        <PartialValue
          label="Region"
          valuePath="region"
        />
        <PartialValue
          label="Role ARN"
          valuePath="role_ARN"
        />
        <PartialValue
          label="Last Status"
          valuePath="last_status"
        />
        <PartialValue
          label="Last Status Time"
          valuePath="last_start_time"
          renderValue={formatDate}
        />
        <PartialValue
          label="Last Status Change Time"
          valuePath="last_status_change_time"
          renderValue={formatDate}
        />
      </div>
    </Partial>
  );
};

ConfigRecorders.propTypes = propTypes;

export default ConfigRecorders;
