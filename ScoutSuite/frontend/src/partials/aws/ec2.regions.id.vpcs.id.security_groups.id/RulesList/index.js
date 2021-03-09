import React, { useContext }  from 'react';
import ReportProblemOutlinedIcon from '@material-ui/icons/ReportProblemOutlined';
import get from 'lodash/get';


import { PartialContext, PartialPathContext } from '../../../../components/Partial/context';
import { PartialValue } from '../../../../components/Partial';

import './style.scss';


const RulesList = () => {
  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const value = get(ctx.item, basePath);

  const isDefault = get(ctx.item, 'name') === 'default';

  const renderIpAddresses = (addresses, path) => (
    <li>
      IP addresses:
      <ul>
        {addresses.map((address, i) => (
          <li key={i}>
            <PartialValue
              value={address.CIDR}
              errorPath={path}
            />
          </li>
        ))}
      </ul>
    </li>
  );

  const renderIpv6Addresses = addresses => (
    <li>
      IPv6 addresses:
      <ul>
        {addresses.map((address, i) => (
          <li key={i}>
            {/* TODO: actual value for IPv6*/}
            {address}
          </li>
        ))}
      </ul>
    </li>
  );

  const renderSecurityGroups = (groups, path) => (
    <li>
      EC2 security groups:
      <ul>
        {groups.map((group, i) => (
          <li key={i}>
            <PartialValue
              value={`${group.GroupName}\xa0\xa0(${group.GroupId})`}
              errorPath={path}
            />
          </li>
        ))}
      </ul>
    </li>
  );

  return (
    <>
      <ul className="rules-list">
        {Object.entries(value.protocols).map(([name, { ports }], i) => (
          <div key={i}>
            <li>{name}</li>
            <ul>
              <li>
                Ports:
                <ul>
                  {Object.entries(ports).map(([port_name, port], i) => (
                    <div key={i}>
                      <li>
                        <PartialValue
                          value={port_name}
                          errorPath={`protocols.${name}.ports.${port_name}`}
                        />
                      </li>
                      <ul>
                        {port.cidrs && (
                          renderIpAddresses(
                            port.cidrs, 
                            `protocols.${name}.ports.${port_name}.cidrs.${i}.CIDR`,
                          )
                        )}
                        {port.Ipv6Ranges && (
                          renderIpv6Addresses(port.Ipv6Ranges)
                        )}
                        {port.security_groups && (
                          renderSecurityGroups(
                            port.security_groups,
                            `protocols.${name}.ports.${port_name}.security_groups.${i}`,
                          )
                        )}
                      </ul>
                    </div>
                  ))}
                </ul>
              </li>
            </ul>
          </div>
        ))}
      </ul>
      {isDefault && (
        <PartialValue 
          value="Default security groups should have no rules."
          errorPath="default_with_rules"
          renderValue={value => (
            <span className="default-with-rules">
              <ReportProblemOutlinedIcon fontSize="inherit"/> {value}
            </span>
          )}
        />
      )}
    </>
  );
};

export default RulesList;
