import React from 'react';
import { useParams } from 'react-router-dom';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../../api/useAPI';
import {
  getServiceExternalAttackEndpoint,
  getCategoryExternalAttackEndpoint,
} from '../../api/paths';
import Breadcrumb from '../../components/Breadcrumb/index';
import DetailedValue from '../../components/DetailedValue';

import './style.scss';


const ExternalAttack = () => {
  const { service, category } = useParams();

  const endpoint = service 
    ? getServiceExternalAttackEndpoint(service)
    : getCategoryExternalAttackEndpoint(category);

  const { data, loading } = useAPI(endpoint, {});

  if (loading) return null;

  const renderProtocols = protocols => (
    <ul className="protocols">
      {Object.entries(protocols).map(([name, protocol], i) => (
        <div key={i}>
          <li>{name}</li>
          <ul>
            {Object.entries(protocol.ports).map(([port, { cidrs }], i) => (
              <div key={i}>
                <li>{port}</li>
                <ul>
                  {cidrs.map(({ CIDR, CIDRName }, i) => (
                    <li key={i}>
                      {CIDRName ? `${CIDR} (${CIDRName})`: CIDR}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </ul>
        </div>
      ))}
    </ul>
  );

  return (
    <>
      <Breadcrumb />
      <div className="external-attack">
        <h2>Public IP/DNS and open ports</h2>
        <hr/>
        {isEmpty(data) ? (
          <div className="no-informations">
            No public addresses for this {service ? 'service' : 'category\'s services'}
          </div>
        ) : (
          Object.entries(data).map(([address, infos], i) => (
            <div className="informations-card" key={i}>
              <h3>{address}</h3>
              <div className="content">
                {infos.InstanceName && (
                  <DetailedValue 
                    label="Instance Name"
                    value={infos.InstanceName}
                  />
                )}
                {infos.PublicDnsName && (
                  <DetailedValue 
                    label="Public DNS Name"
                    value={infos.PublicDnsName}
                  />
                )}
                <DetailedValue 
                  label="Protocols"
                  value={infos.protocols}
                  renderValue={renderProtocols}
                />
              </div>
            </div>
          ))
        )}        
      </div>
    </>
  );
};

export default ExternalAttack;
