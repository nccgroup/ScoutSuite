import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../../api/useAPI';
import { getItemsEndpoint } from '../../api/paths';
import { sortBySeverity } from '../../utils/Severity/sort';
import Table from '../../components/Table';
import Name from './formatters/Name/index';
import SelectedItemContainer from './SelectedItemContainer';
import Breadcrumb from '../../components/Breadcrumb/index';
import DownloadButton from '../../components/DownloadButton';

import './style.scss';
import ErrorBoundary from '../../components/ErrorBoundary';


const FlaggedItems = () => {
  const params = useParams();
  const { data: response, loading, loadPage } = useAPI(
    getItemsEndpoint(params.service, params.finding),
    [],
    { pagination: true },
  );
  const data = response.results;

  const [defaultObj, setdefaultObj] = useState({});

  useEffect(() => {
    if (
      data &&
      !isEmpty(data[0]) &&
      JSON.stringify(data[0]) !== JSON.stringify(defaultObj)
    ) {
      setdefaultObj(data[0]);
    }
  }, [data]);

  const fetchData = React.useCallback(({ pageIndex, sortBy, direction, filters }) => {
    loadPage(pageIndex + 1, sortBy, direction, null, filters);
  }, []);

  if (loading) {
    return <Breadcrumb />;
  }

  const keys = Object.keys(defaultObj);
  const columns = [{ name: 'Name', key: 'name' }];

  // AWS columns
  if (keys.includes('region')) columns.push({ name: 'Region', key: 'region' });
  if (keys.includes('vpc')) columns.push({ name: 'VPC', key: 'vpc' });
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
      <div className="finding-items">
        <ErrorBoundary>
          <div className="table-card">
            <Table
              columns={columns}
              data={data}
              initialState={initialState}
              formatters={formatters}
              sortBy={sortBy}
              fetchData={fetchData}
              manualPagination={true}
              pageCount={response.meta.total_pages}
              headerRight={downloadButtons}
            />
          </div>
        </ErrorBoundary>

        <div className="selected-item">
          {!params.item ? (
            <span className="no-item">No finding selected</span>
          ) : (
            <SelectedItemContainer />
          )}
        </div>
      </div>
    </>
  );
};

export default FlaggedItems;
