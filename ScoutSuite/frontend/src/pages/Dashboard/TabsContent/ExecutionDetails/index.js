import React from 'react';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../../../../api/useAPI';
import { getExecutionDetailsEndpoint } from '../../../../api/paths';
import { formatDate } from '../../../../utils/Partials';
import DetailedValue from '../../../../components/DetailedValue';

import './style.scss';


const ExecutionDetails = () => {
  const { data, loading } = useAPI(getExecutionDetailsEndpoint(), {});

  if (isEmpty(data) || loading) return null;

  return (
    <div className="execution-details">
      <div>
        <h3>Report Details</h3>
        <hr/>
        <div className="details-card">
          <DetailedValue 
            label="Provider"
            value={data.provider_name}
          />
          <DetailedValue 
            label="Time"
            value={data.time}
            renderValue={formatDate}
          />
          <div className="report-version">
            Report generated with <b>ScoutSuite version {`${data.version}`}</b>
          </div>
        </div>
      </div>

      <div>
        <h3>Ruleset</h3>
        <hr/>
        <div className="details-card">
          <div>
            Using ruleset <b>{`${data.ruleset_name}:`}</b>
          </div>
          <div className="ruleset-about">
            {data.ruleset_about}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExecutionDetails;
