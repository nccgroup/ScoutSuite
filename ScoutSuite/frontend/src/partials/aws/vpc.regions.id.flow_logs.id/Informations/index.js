import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';
import { valueOrNone, formatDate } from '../../../../utils/Partials';


const Informations = () => {
  return (
    <>
      <h4>Informations</h4>
      <PartialValue
        label="Name"
        valuePath="name"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Resource ID"
        valuePath="resource_id"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Creation Date"
        valuePath="creation_time"
        renderValue={formatDate}
      />
      <PartialValue
        label="Flow Log Status"
        valuePath="flow_log_status"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Deliver Logs Status"
        valuePath="deliver_logs_status"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Deliver Logs Error Messages"
        valuePath="deliver_logs_error_message"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Traffic Type"
        valuePath="traffic_type"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Log Destination Type"
        valuePath="log_destination_type"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Log Destination"
        valuePath="log_destination"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Log Format"
        valuePath="log_format"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Max Aggregation Interval"
        valuePath="max_aggregation_interval"
        renderValue={valueOrNone}
      />
    </>
  );
};

export default Informations;
