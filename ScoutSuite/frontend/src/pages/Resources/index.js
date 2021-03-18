import { useParams } from '@reach/router';
import React from 'react';

import { useAPI } from '../../api/useAPI';
import { sortBySeverity } from '../../utils/Severity/sort';
import Table from '../../components/Table';
import Name from './formatters/Name/index';
// import ResourcePartialWrapper from './ResourcePartialWrapper';
import Breadcrumb from '../../components/Breadcrumb/index';

import { getResourcesEndpoint } from '../../api/paths';

import './style.scss';

const Resources = () => {
  const params = useParams();
  const { data: items, loading } = useAPI(getResourcesEndpoint(params.service, params.resource), []);
  const data = items.results;


  if (loading) return <>
    <Breadcrumb />
  </>;

  const keys = Object.keys(data[0]);

  const columns = [
    { name: 'Name', key: 'name' },
  ];

  // AWS columns
  if (keys.includes('AvailabilityZone')) columns.push({ name: 'Availability Zone', key: 'AvailabilityZone' });
  if (keys.includes('DNSName')) columns.push({ name: 'DNS Name', key: 'DNSName' });
  if (keys.includes('SubnetId')) columns.push({ name: 'SubnetId', key: 'SubnetId' });

  // GCP columns
  if (keys.includes('description')) columns.push({ name: 'Description', key: 'description' });
  if (keys.includes('project_id')) columns.push({ name: 'Project ID', key: 'project_id' });
  if (keys.includes('location')) columns.push({ name: 'Location', key: 'location' });

  const initialState = {
    pageSize: 10
  };

  const formatters = {
    name: Name
  };

  const sortBy = {
    severity: sortBySeverity
  };

  return (
    <>
      <Breadcrumb />
      <div className="flagged-items">
        <div className="table-card">
          <Table
            columns={columns}
            data={data}
            initialState={initialState}
            formatters={formatters}
            sortBy={sortBy} />
        </div>

        <div className="selected-item">
          {!params.id ? (
            <span className="no-item">No selected resource</span>
          ) : (
            <span className="no-item">Selected {params.id}</span>
            // <ResourcePartialWrapper title={params.id} />
          )}
        </div>
      </div>
    </>
  );
};

export default Resources;
