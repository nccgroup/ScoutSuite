import { useParams } from '@reach/router';
import React from 'react';

// import PropTypes from 'prop-types';

import { useAPI } from '../../api/useAPI';
import { sortBySeverity } from '../../utils/Severity/sort';
import Layout from '../../layout';
import Table from '../../components/Table';

import './style.scss';
import Name from './formatters/Name/index';

const propTypes = {};

const FlaggedItems = () => {
  const params = useParams();
  const { data: items, loading } = useAPI(`services.${params.service}.findings.${params.finding}.items`);

  if (loading) return (
    <Layout />
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

        <div className="table-card">
          {!params.item ? 'No selected item.' : params.item}
        </div>
      </div>
    </Layout>
  );
};

FlaggedItems.propTypes = propTypes;

export default FlaggedItems;
