import React, { useContext }  from 'react';
import get from 'lodash/get';

import { PartialContext, PartialPathContext } from '../../../../components/Partial/context';
import { PartialValue } from '../../../../components/Partial';
import ResourceLink from '../../../../components/ResourceLink';
import WarningMessage from '../../../../components/WarningMessage';

import './style.scss';


const RulesList = () => {
  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const rules = get(ctx.item, basePath);

  const isDefault = get(ctx.item, 'name') === 'default';

  const renderIpAddresses = (title, addresses, path) => (
    <li>
      {`${title}:`}
      <ul>
        {addresses.map((address, i) => (
          <li key={i}>
            <PartialValue
              value={address}
              errorPath={path}
              renderValue={value =>
                value.CIDRName 
                  ? `${value.CIDR} (${value.CIDRName})`
                  : value.CIDR
              }
            />
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
              value={group}
              errorPath={path}
              renderValue={value =>
                value.GroupName
                  ? (
                    <span>
                      {`${value.GroupName} (`}
                      <ResourceLink 
                        service="ec2"
                        resource="security_groups"
                        id={value.GroupId}
                        name={value.GroupId}
                      />
                      {')'}
                    </span>
                  ) : `${value.GroupId} (AWS Account ID: ${value.UserId})`
              }
            />
          </li>
        ))}
      </ul>
    </li>
  );

  return (
    <>
      <ul className="rules-list">
        {Object.entries(rules.protocols).map(([name, { ports }], i) => (
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
                            'IP adresses',
                            port.cidrs, 
                            `protocols.${name}.ports.${port_name}.cidrs.${i}.CIDR`,
                          )
                        )}
                        {port.Ipv6Ranges && (
                          renderIpAddresses(
                            'IPv6 addresses',
                            port.Ipv6Ranges,
                            `protocols.${name}.ports.${port_name}.cidrs.${i}.CIDR`,
                          )
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
          errorPath="default_with_rules"
          renderValue={() => (
            <WarningMessage
              className="rules-list__warning-message"
              message="Default security groups should have no rules."
            />
          )}
        />
      )}
    </>
  );
};

export default RulesList;
