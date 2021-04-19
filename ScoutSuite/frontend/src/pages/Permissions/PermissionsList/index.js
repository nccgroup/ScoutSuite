import React, { useState, useMemo, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import { useParams } from 'react-router-dom';

import Table from '../../../components/Table';
import Name from './formatters/Name';
import PermissionInfos from './PermissionInfos';


const propTypes = {
  service: PropTypes.string.isRequired,
  list: PropTypes.object.isRequired,
};

const PermissionsList = props => {
  const { service, list } = props;
  const params = useParams();

  const listMemo = useMemo(
    () =>
      Object.entries(list).map(([key, values]) => ({ name: key, ...values })),
    [list],
  );
  const [items, setItems] = useState(listMemo);

  const permission = useMemo(
    () => params.id && listMemo.find(item => item.name === decodeURI(params.id)),
    [params.id, listMemo],
  );

  useEffect(() => {
    setItems(listMemo);
  }, [listMemo]);

  const fetchData = useCallback(
    ({ search }) => {
      if (search)
        setItems(
          listMemo.filter(item =>
            item.name.toLowerCase().includes(search.toLowerCase()),
          ),
        );
      else setItems(listMemo);
    },
    [listMemo],
  );

  if (!items) return null;

  const columns = [{ name: 'Name', key: 'name' }];

  const initialState = {
    pageSize: 10,
  };

  const formatters = {
    name: Name,
  };

  return (
    <div className="permissions">
      <div className="table-card">
        <Table
          columns={columns}
          data={items}
          initialState={initialState}
          formatters={formatters}
          fetchData={fetchData}
        />
      </div>

      {!params.id && (
        <div className="selected-item no-items">No selected permission.</div>
      )}

      {params.id && permission && (
        <PermissionInfos
          permission={permission}
          service={service}
        />
      )}
    </div>
  );
};

PermissionsList.propTypes = propTypes;

export default PermissionsList;
