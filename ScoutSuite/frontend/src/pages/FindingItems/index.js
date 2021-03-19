import { useParams } from '@reach/router';
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
  const { data: items, loading } = useAPI(getItemsEndpoint(params.service, params.finding), []);

  if (isEmpty(items) || isEmpty(items.results)) {
    return (
      <>
        <Breadcrumb />
        <div>Server request failed</div>
      </>
    );
  }

  if (loading) {
    return (
      <Breadcrumb />
    );
  }

  const columns = [
    { name: 'ID', key: 'id' },
    { name: 'Name', key: 'name' },
  ];

  for (let [key] of Object.entries(items.results[0])) {
    if (key !== 'item') columns.push({ name: key, key });
  }

  const data = items.results.map((item) => {
    let newItem = item.item;

    for (let [key, value] of Object.entries(item)) {
      if (key !== 'item') newItem[key] = value.id;
    }

    return newItem;
  });

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
