import React from 'react';
import isEmpty from 'lodash/isEmpty';
import flatten from 'lodash/flatten';
import { Button } from '@material-ui/core';
import GetAppOutlinedIcon from '@material-ui/icons/GetAppOutlined';

import { useAPI } from '../../../../api/useAPI';
import { getServicesEndpoint } from '../../../../api/paths';
import ResourceLink from '../../../../components/ResourceLink';
import { exportJSON, exportCSV } from '../../../../utils/Export';

import './style.scss';

const ResourcesDetails = () => {
  const { data, loading } = useAPI(getServicesEndpoint(), {});

  if (isEmpty(data) || loading) return null;

  const services = flatten(data.map(service => service.services));

  const downloadSummary = async type => {
    let servicesList = [];

    services.forEach(service => service.resources.forEach(resource => {
      servicesList.push({
        Service: service.id,
        Resource: resource.id,
        '#': resource.count
      });
    }));

    if (type == 'json') {
      exportJSON(servicesList, 'resource-details');
    } else {
      exportCSV(servicesList, 'resource-details');
    }
  };

  return (
    <div className="resources-details">
      <div className="download-btns">
        <Button
          className="download-btn"
          variant="outlined"
          onClick={() => downloadSummary('json')}
          startIcon={<GetAppOutlinedIcon />}
        >
          JSON
        </Button>
        <Button
          className="download-btn"
          variant="outlined"
          onClick={() => downloadSummary('csv')}
          startIcon={<GetAppOutlinedIcon />}
        >
          CSV
        </Button>
      </div>

      {services.map((service, i) => (
        <div key={i}>
          <h3>{service.name}</h3>
          <hr />
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
                    {resource.count ? (
                      <ResourceLink
                        service={service.id}
                        resource={resource.id}
                        name={resource.name}
                      />
                    ) : (
                      <span className="no-link">{resource.name}</span>
                    )}
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
