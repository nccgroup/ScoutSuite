import React from 'react';
import { useParams } from 'react-router-dom';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../../api/useAPI';
import { getResourcesEndpoint } from '../../api/paths';
import { sortBySeverity } from '../../utils/Severity/sort';
import Table from '../../components/Table';
import Name from './formatters/Name/index';
import ResourcePartialWrapper from './ResourcePartialWrapper';
import Breadcrumb from '../../components/Breadcrumb/index';
import DownloadButton from '../../components/DownloadButton/index';

import './style.scss';
import ErrorBoundary from '../../components/ErrorBoundary';


const Resources = () => {
  const params = useParams();
  const { data: response, loading, loadPage } = useAPI(
    getResourcesEndpoint(params.service, params.resource),
    [],
    { pagination: true },
  );
  const data = response.results;

  const fetchData = React.useCallback(({ pageIndex, sortBy, direction }) => {
    loadPage(pageIndex + 1, sortBy, direction);
  }, []);

  if (loading) return null;

  if (isEmpty(data)) {
    return (
      <>
        <Breadcrumb />
        <div className="findings">
          <div className="table-card no-items">
            No resources of this type present
          </div>
        </div>
      </>
    );
  }

  const keys = Object.keys(data[0]);

  const columns = [{ name: 'Name', key: 'name' }];

  // AWS columns
  if (keys.includes('region')) 
    columns.push({ name: 'Region', key: 'region' });
  if (keys.includes('vpc')) 
    columns.push({ name: 'VPC', key: 'vpc' });
  if (keys.includes('AvailabilityZone'))
    columns.push({ name: 'Availability Zone', key: 'AvailabilityZone' });
  if (keys.includes('availability_zone'))
    columns.push({ name: 'Availability Zone', key: 'availability_zone' });
  if (keys.includes('DNSName'))
    columns.push({ name: 'DNS Name', key: 'DNSName' });
  if (keys.includes('SubnetId'))
    columns.push({ name: 'SubnetId', key: 'SubnetId' });

  // GCP columns
  if (keys.includes('description'))
    columns.push({ name: 'Description', key: 'description' });
  if (keys.includes('project_id'))
    columns.push({ name: 'Project ID', key: 'project_id' });
  if (keys.includes('location'))
    columns.push({ name: 'Location', key: 'location' });

  const initialState = {
    pageSize: 10,
  };

  const formatters = {
    name: Name,
  };

  const sortBy = {
    severity: sortBySeverity,
  };

  const downloadButtons = (
    <>
      <DownloadButton
        service={params.service}
        resource={params.resource}
        type="json"
      />
      <DownloadButton
        service={params.service}
        resource={params.resource}
        type="csv"
      />
    </>
  );

  return (
    <>
      <Breadcrumb />
      <div className="resources">
        <ErrorBoundary>
          <div className="table-card">
            <Table
              columns={columns}
              data={data}
              formatters={formatters}
              sortBy={sortBy}
              fetchData={fetchData}
              manualPagination={true}
              pageCount={response.meta.total_pages}
              initialState={initialState}
              headerRight={downloadButtons}
            />
          </div>
        </ErrorBoundary>


        <div className="selected-item">
          {!params.id ? (
            <span className="no-item">No resource selected</span>
          ) : (
            <ResourcePartialWrapper title={params.id} />
          )}
        </div>
      </div>
    </>
  );
};

export default Resources;
