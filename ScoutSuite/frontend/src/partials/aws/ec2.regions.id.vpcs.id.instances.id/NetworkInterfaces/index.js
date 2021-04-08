import React from 'react';
import PropTypes from 'prop-types';
import isEmpty from 'lodash/isEmpty';

import { renderResourcesAsList } from '../../../../utils/Partials';
import DetailedValue from '../../../../components/DetailedValue';


const propTypes = {
  interfaces: PropTypes.object,
};

const NetworkInterfaces = props => {
  const { interfaces } = props;

  return (
    Object.entries(interfaces).map(([id, value], i) => (
      <div key={i}>
        <h5>{id}</h5>
        <ul>
          {value.Description && (
            <li>
              <DetailedValue
                label="Description"
                value={value.Description}
              />
            </li>
          )}
          {value.Association && (
            <>
              <li>
                <DetailedValue
                  label="Public IP"
                  value={value.Association.PublicIp}
                />
              </li>
              <li>
                <DetailedValue
                  label="Public DNS"
                  value={value.Association.PublicDnsName}
                />
              </li>
            </>
          )}
          {value.Attachment && (
            <li>
              <DetailedValue
                label="Attached to Instance"
                value={value.Attachment.InstanceId}
              />
            </li>
          )}
          {!isEmpty(value.Ipv6Addresses) && (
            <>
              <li>IPv6 Addresses:</li>
              <ul>
                {value.Ipv6Addresses.map((address, i) => (
                  <li key={i}>
                    {address.Ipv6Address}
                  </li>
                ))}
              </ul>
            </>
          )}
          {value.PrivateIpAddresses.map((address, i) => (
            <li key={i}>
              <DetailedValue
                label={address.Primary ? 
                  'Primary Private IP' : 'Private IP'
                }
                value={address.PrivateIpAddress}
              />
            </li>
          ))}
          {!isEmpty(value.Groups) && (
            <li>
              <DetailedValue
                label="Security Groups"
                value={renderResourcesAsList(value.Groups, 'GroupName')}
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
