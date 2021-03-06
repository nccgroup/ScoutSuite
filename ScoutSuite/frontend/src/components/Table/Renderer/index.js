import React from 'react';
import { PropTypes } from 'prop-types';
import { useTable, useSortBy, usePagination } from 'react-table';
import ArrowDropUpIcon from '@material-ui/icons/ArrowDropUp';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import cx from 'classnames';

const propTypes = {
  columns: PropTypes.arrayOf(PropTypes.object).isRequired,
  data: PropTypes.arrayOf(PropTypes.object).isRequired,
  hasPagination: PropTypes.bool.isRequired,
  initialState: PropTypes.object,
  disableSearch: PropTypes.bool,
  disablePagination: PropTypes.bool,
};

const TableRender = (props) => {
  const {
    columns,
    data,
    initialState,
    disableSearch,
    disablePagination,
  } = props;

  const columnsMemo = React.useMemo(() => columns);
  const dataMemo = React.useMemo(() => data);

  const useTableParams = [
    {
      columns: columnsMemo,
      data: dataMemo,
      initialState,
      disableMultiSort: true,
      disableSortRemove: true,
    },
    useSortBy,
  ];

  if (!disablePagination) useTableParams.push(usePagination);

  const tableInstance = useTable(...useTableParams);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    page,
    prepareRow,
    canPreviousPage,
    canNextPage,
    previousPage,
    nextPage,
    pageCount,
    state: { pageIndex },
  } = tableInstance;

  return (
    <>
      {!disableSearch && <div className="search-bar">
        <input placeholder="Search in this table" />
      </div>}

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
                  {column.canSort && (
                    <div className="sort-icons">
                      <ArrowDropUpIcon
                        color={
                          column.isSorted && !column.isSortedDesc
                            ? 'primary'
                            : undefined
                        }
                        fontSize="small"
                      />
                      <ArrowDropDownIcon
                        color={
                          column.isSorted && column.isSortedDesc
                            ? 'primary'
                            : undefined
                        }
                        fontSize="small"
                      />
                    </div>
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {(page || rows).map((row, rowKey) => {
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

      {!disablePagination && <div className="pagination">
        <ChevronLeftIcon
          onClick={previousPage}
          className={cx('icon', !canPreviousPage && 'disabled')}
        />
        {pageIndex + 1} / {pageCount}
        <ChevronRightIcon
          onClick={nextPage}
          className={cx('icon', !canNextPage && 'disabled')}
        />
      </div>}
    </>
  );
};

TableRender.propTypes = propTypes;

export default TableRender;
