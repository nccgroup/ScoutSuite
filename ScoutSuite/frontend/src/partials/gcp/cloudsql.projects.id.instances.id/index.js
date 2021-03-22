
import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { 
  partialDataShape,
  convertBoolToEnable, 
  formatDate, 
  valueOrNone
} from '../../../utils/Partials';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const SQLInstances = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="left-pane">
        <PartialValue
          label="Project ID"
          valuePath="project_id" />

        <PartialValue
          label="Automatic Backups"
          valuePath="automatic_backup_enabled"
          renderValue={convertBoolToEnable} />

        <PartialValue
          label="Last Backup"
          valuePath="last_backup_timestamp"
          renderValue={formatDate} />

        <PartialValue
          label="Logs"
          valuePath="log_enabled"
          renderValue={convertBoolToEnable} />

        <PartialValue
          label="SSL Required"
          valuePath="ssl_required"
          renderValue={convertBoolToEnable} />

        <PartialValue
          label="Public IP Address"
          valuePath="public_ip"
          renderValue={valueOrNone} />

        <PartialValue
          label="Private IP Address"
          valuePath="private_ip"
          renderValue={valueOrNone} />


      </div>

      
    </Partial>
  );
};

SQLInstances.propTypes = propTypes;

export default SQLInstances;