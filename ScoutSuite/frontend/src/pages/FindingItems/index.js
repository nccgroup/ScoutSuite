import { useParams } from 'react-router-dom';
import React from 'react';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../../api/useAPI';
import { getItemsEndpoint } from '../../api/paths';
import { sortBySeverity } from '../../utils/Severity/sort';
import Table from '../../components/Table';
import Name from './formatters/Name/index';
import SelectedItemContainer from './SelectedItemContainer';
import Breadcrumb from '../../components/Breadcrumb/index';

import './style.scss';

const FlaggedItems = () => {
  const params = useParams();
  const { data: items, loading, loadPage } = useAPI(
    getItemsEndpoint(params.service, params.finding),
    [],
    { pagination: true },
  );

  const fetchData = React.useCallback(({ pageIndex, sortBy, direction }) => {
    loadPage(pageIndex + 1, sortBy, direction);
  }, []);

  if (isEmpty(items) || isEmpty(items.results)) {
    return (
      <>
        <Breadcrumb />
        <div>Server request failed</div>
      </>
    );
  }

  if (loading) {
    return <Breadcrumb />;
  }

  const columns = [
  ];

  for (let key of Object.keys(items.results[0])) {
    if (key !== 'display_path') columns.push({ name: key, key });
  }

  const data = items.results;

  const initialState = {
    pageSize: 10,
  };

  const formatters = {
    name: Name,
  };

  const sortBy = {
    severity: sortBySeverity,
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
            sortBy={sortBy}
            fetchData={fetchData}
            manualPagination={true}
            pageCount={items.meta.total_pages}
          />
        </div>

        <div className="selected-item">
          {!params.item ? (
            <span className="no-item">No selected item</span>
          ) : (
            <SelectedItemContainer />
          )}
        </div>
      </div>
    </>
  );
};

export default FlaggedItems;
