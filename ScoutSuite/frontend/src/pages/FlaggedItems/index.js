import { useParams } from '@reach/router';
import React from 'react';

import { useAPI } from '../../api/useAPI';
import { sortBySeverity } from '../../utils/Severity/sort';
import Table from '../../components/Table';
import Name from './formatters/Name/index';
import SelectedItemContainer from './SelectedItemContainer';
import Breadcrumb from '../../components/Breadcrumb/index';

import { getItems } from '../../api/paths';

import './style.scss';

const FlaggedItems = () => {
  const params = useParams();
  const { data: items, loading } = useAPI(getItems(params.service, params.finding), []);

  if (loading) return <>
    <Breadcrumb />
  </>;

  const columns = [
    { name: 'ID', key: 'id' },
    { name: 'Name', key: 'name' },
  ];

  for (let [key] of Object.entries(items[0])) {
    if (key !== 'item') columns.push({ name: key, key });
  }

  const data = items.map((item) => {
    let newItem = item.item;

    for (let [key, value] of Object.entries(item)) {
      if (key !== 'item') newItem[key] = value.id;
    }

    return newItem;
  });

  const initialState = {
    pageSize: 5
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
            <SelectedItemContainer title={params.item} />
          )}
        </div>
      </div>
    </>
  );
};

export default FlaggedItems;
