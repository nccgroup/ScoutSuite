import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { PartialContext, PartialPathContext } from '../context';
import { concatPaths } from '../../../utils/Partials';

import './style.scss';
import Table from '../../Table/index';

const propTypes = {
  columns: PropTypes.arrayOf(PropTypes.string).isRequired,
  path: PropTypes.string.isRequired
};

const PartialTable = props => {
  const {
    columns,
    path,
    ...tableProps
  } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);

  const fullPath = concatPaths(basePath, path);
  const items = get(ctx.item, fullPath);
  const itemsList = Array.isArray(items) ? items : Object.entries(items).map(([key, item]) => ({ key, ...item }));

  const data = itemsList;

  return (
    <div className="partial-table"> 
      <Table
        columns={columns}
        data={data}
        disableSearch
        disablePagination
        {...tableProps} />
    </div>
  );
};

PartialTable.propTypes = propTypes;

export default PartialTable;
