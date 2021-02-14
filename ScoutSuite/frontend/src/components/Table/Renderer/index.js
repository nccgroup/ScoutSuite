import React from 'react';
import { PropTypes } from 'prop-types';
import { useTable, useSortBy } from 'react-table';
import ArrowDownwardOutlinedIcon from '@material-ui/icons/ArrowDownwardOutlined';
import ArrowUpwardOutlinedIcon from '@material-ui/icons/ArrowUpwardOutlined';

const propTypes = {
  columns: PropTypes.arrayOf(PropTypes.object).isRequired,
  data: PropTypes.arrayOf(PropTypes.object).isRequired,
  initialState: PropTypes.object,
};

const TableRender = (props) => {
  const { columns, data, initialState } = props;

  const columnsMemo = React.useMemo(() => columns);
  const dataMemo = React.useMemo(() => data);

  const tableInstance = useTable(
    {
      columns: columnsMemo,
      data: dataMemo,
      initialState,
      disableMultiSort: true, 
      disableSortRemove: true
    },
    useSortBy,
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = tableInstance;

  return (
    <div>
      <table className="table" {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup, headerKey) => (
            <tr {...headerGroup.getHeaderGroupProps()} key={headerKey}>
              {headerGroup.headers.map((column, columnKey) => (
                <th
                  {...column.getHeaderProps(column.getSortByToggleProps())}
                  key={columnKey}
                >
                  <span>{column.render('Header')}</span>

                  <span>
                    {column.isSorted ? (
                      column.isSortedDesc ? (
                        <ArrowDownwardOutlinedIcon fontSize="inherit" />
                      ) : (
                        <ArrowUpwardOutlinedIcon fontSize="inherit" />
                      )
                    ) : (
                      ''
                    )}
                  </span>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row, rowKey) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()} key={rowKey}>
                {row.cells.map((cell, cellKey) => {
                  return (
                    <td {...cell.getCellProps()} key={cellKey}>
                      {cell.render('Cell')}
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

TableRender.propTypes = propTypes;

export default TableRender;
