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
                          <li>
                            IP addresses:
                            <ul>
                              {port.cidrs.map((address, i) => (
                                <li key={i}>
                                  <PartialValue
                                    value={address.CIDR}
                                    errorPath={`protocols.${name}.ports.${port_name}.cidrs.${i}.CIDR`}
                                  />
                                </li>
                              ))}
                            </ul>
                          </li>
                        )}
                        {port.Ipv6Ranges && (
                          <li>
                            IPv6 addresses:
                            <ul>
                              {port.Ipv6Ranges.map((address, i) => (
                                <li key={i}>
                                  {/* TODO: actual value for IPv6*/}
                                  {address}
                                </li>
                              ))}
                            </ul>
                          </li>
                        )}
                        {port.security_groups && (
                          <li>
                            EC2 security groups:
                            <ul>
                              {port.security_groups.map((group, i) => (
                                <li key={i}>
                                  <PartialValue
                                    value={`${group.GroupName}\xa0\xa0(${group.GroupId})`}
                                    errorPath={`protocols.${name}.ports.${port_name}.security_groups.${i}`}
                                  />
                                </li>
                              ))}
                            </ul>
                          </li>
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
