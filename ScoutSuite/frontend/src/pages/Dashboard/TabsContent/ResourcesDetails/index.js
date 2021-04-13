import React from 'react';
import isEmpty from 'lodash/isEmpty';
import flatten from 'lodash/flatten';

import { useAPI } from '../../../../api/useAPI';
import { getServicesEndpoint } from '../../../../api/paths';
import ResourceLink from '../../../../components/ResourceLink';

import './style.scss';


const ResourcesDetails = () => {
  const { data, loading } = useAPI(getServicesEndpoint(), {});

  if (isEmpty(data) || loading) return null;

  const services = flatten(data.map(service => (service.services)));

  return (
    <div className="resources-details">
      {services.map((service, i) => (
        <div key={i}>
          <h3>{service.name}</h3>
          <hr/>
          <table className="details-card">
            <thead>
              <tr>
                <th>Resource</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>
              {service.resources.map((resource, i) => (
                <tr key={i}>
                  <td>
                    <ResourceLink
                      service={service.id}
                      resource={resource.id}
                      name={resource.name}
                    />
                  </td>
                  <td>{resource.count || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
};

export default ResourcesDetails;
