import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';

import './style.scss';


const Informations = () => {
  return (
    <>
      <PartialValue
        label="Name"
        valuePath="name"
      />
      <PartialValue
        label="Region"
        valuePath="region"
      />
      <PartialValue
        label="Actions Enabled"
        valuePath="ActionsEnabled"
      />
      <PartialValue
        label="State"
        valuePath="StateValue"
      />
      <div className="alarm-metrics">
        <PartialValue
          label="Metric"
          valuePath="Namespace"
        />
        <span>::</span>
        <PartialValue
          valuePath="MetricName"
        />
      </div>
    </>
  );
};

export default Informations;
