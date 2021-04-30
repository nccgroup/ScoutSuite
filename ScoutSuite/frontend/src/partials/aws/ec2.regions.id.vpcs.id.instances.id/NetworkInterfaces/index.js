import React from 'react';
import PropTypes from 'prop-types';
import isEmpty from 'lodash/isEmpty';

import { 
  renderList, 
  renderSecurityGroupLink 
} from '../../../../utils/Partials';
import DetailedValue from '../../../../components/DetailedValue';


const propTypes = {
  interfaces: PropTypes.object,
};

const NetworkInterfaces = props => {
  const { interfaces } = props;

  return (
    Object.entries(interfaces).map(([id, networkInterface], i) => (
      <div key={i}>
        <h5>{id}</h5>
        <ul>
          {networkInterface.Description && (
            <li>
              <DetailedValue
                label="Description"
                value={networkInterface.Description}
              />
            </li>
          )}
          {networkInterface.Association && (
            <>
              <li>
                <DetailedValue
                  label="Public IP"
                  value={networkInterface.Association.PublicIp}
                />
              </li>
              <li>
                <DetailedValue
                  label="Public DNS"
                  value={networkInterface.Association.PublicDnsName}
                />
              </li>
            </>
          )}
          {networkInterface.Attachment && (
            <li>
              <DetailedValue
                label="Attached to Instance"
                value={networkInterface.Attachment.InstanceId}
              />
            </li>
          )}
          {!isEmpty(networkInterface.Ipv6Addresses) && (
            <>
              <li>IPv6 Addresses:</li>
              <ul>
                {networkInterface.Ipv6Addresses.map((address, i) => (
                  <li key={i}>
                    {address.Ipv6Address}
                  </li>
                ))}
              </ul>
            </>
          )}
          {networkInterface.PrivateIpAddresses.map((address, i) => (
            <li key={i}>
              <DetailedValue
                label={address.Primary ? 
                  'Primary Private IP' : 'Private IP'
                }
                value={address.PrivateIpAddress}
              />
            </li>
          ))}
          {!isEmpty(networkInterface.Groups) && (
            <li>
              <DetailedValue
                label="Security Groups"
                value={renderList(networkInterface.Groups, '', renderSecurityGroupLink)}
              />
            </li>
          )}
        </ul>
      </div>
    ))
  );
};

NetworkInterfaces.propTypes = propTypes;

export default NetworkInterfaces;
