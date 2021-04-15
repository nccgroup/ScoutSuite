import React from 'react';
import PropTypes from 'prop-types';
import isEmpty from 'lodash/isEmpty';

import DetailedValue from '../../../../components/DetailedValue';
import { convertBoolToEnable } from '../../../../utils/Partials';


const propTypes = {
  connectionInfos: PropTypes.object.isRequired,
};

const PeeringConnection = props => {
  const { connectionInfos } = props;

  return (
    <ul>
      <li>
        <DetailedValue 
          label="Account ID"
          value={connectionInfos.OwnerId}
        />
      </li>
      <li>
        <DetailedValue 
          label="VPC ID"
          value={connectionInfos.VpcId}
        />
      </li>
      <li>
        <DetailedValue 
          label="CIDR"
          value={connectionInfos.CidrBlock}
        />
      </li>
      {!isEmpty(connectionInfos.PeeringOptions) && (
        <li>
          <DetailedValue
            label="Peering Options"
            value={(
              <ul>
                {Object.entries(connectionInfos.PeeringOptions)
                  .map(([option, value], i) => (
                    <li key={i}>
                      <DetailedValue
                        label={option}
                        value={convertBoolToEnable(value)}
                      />
                    </li>
                  ))
                }
              </ul>
            )}
          />
        </li>
      )}
    </ul>
  );
};

PeeringConnection.propTypes = propTypes;

export default PeeringConnection;
