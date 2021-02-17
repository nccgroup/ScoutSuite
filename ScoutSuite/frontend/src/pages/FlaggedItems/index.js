import { useParams } from '@reach/router';
import React from 'react';

import { useAPI } from '../../api/useAPI';
import { sortBySeverity } from '../../utils/Severity/sort';
import Layout from '../../layout';
import Table from '../../components/Table';
import Name from './formatters/Name/index';
import SelectedItemContainer from './SelectedItemContainer';
import BucketInformations from '../../partials/S3/BucketInformations';

import fakeData from '../../api/temp/details.json';

import './style.scss';

const FlaggedItems = () => {
  const params = useParams();
  const { data: items, loading } = useAPI(`services.${params.service}.findings.${params.finding}.items`);

  if (loading) return (
    <Layout> 
      <div/>
    </Layout>
  );

  const columns = [
    { name: 'ID', key: 'id' },
    { name: 'Name', key: 'name' },
  ];

  for (let [key,value] of Object.entries(items[0].extra)) {
    columns.push({ name: value.name, key });
  }

  const data = items.map((item) => {
    let newItem = item;

    for (let [key, extra] of Object.entries(item.extra)) {
      newItem[key] = extra.value;
    }

    return newItem;
  });

  const initialState = {};

  const formatters = {
    name: Name
  };

  const sortBy = {
    severity: sortBySeverity
  };

  return (
    <Layout>
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
            <SelectedItemContainer title={params.item} leftPane={<BucketInformations data={fakeData}/>}>
              <div>
                <span>random data</span>
                <span>random data</span>
                <span>random data</span>
                <span>random data</span>
              </div>
            </SelectedItemContainer>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default FlaggedItems;
