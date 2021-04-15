import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import {
  useTable,
  useSortBy,
  usePagination,
  useAsyncDebounce,
} from 'react-table';
import ArrowDropUpIcon from '@material-ui/icons/ArrowDropUp';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import cx from 'classnames';
import { useParams } from 'react-router-dom';

const propTypes = {
  columns: PropTypes.arrayOf(PropTypes.object).isRequired,
  data: PropTypes.arrayOf(PropTypes.object).isRequired,
  hasPagination: PropTypes.bool.isRequired,
  initialState: PropTypes.object,
  disableSearch: PropTypes.bool,
  disablePagination: PropTypes.bool,
  pageCount: PropTypes.number,
  fetchData: PropTypes.func,
  manualPagination: PropTypes.bool,
  headerRight: PropTypes.element,
};

const TableRender = (props) => {
  const {
    columns,
    data,
    disableSearch,
    disablePagination,
    pageCount: controlledPageCount,
    fetchData,
    manualPagination,
    initialState,
    headerRight
  } = props;

  const [searchQuery, setSearchQuery] = useState('');
  const params = useParams();

  const columnsMemo = React.useMemo(() => columns, [columns]);
  const dataMemo = React.useMemo(() => data, [data]);

  const useTableParams = [
    {
      columns: columnsMemo,
      data: dataMemo,
      initialState: {
        pageIndex: 0,
        ...initialState
      },
      disableMultiSort: true,
      disableSortRemove: true,
      autoResetPage: false,
    },
    useSortBy,
  ];

  if (!disablePagination) {
    useTableParams.push(usePagination);
  }

  if (manualPagination) {
    useTableParams[0].manualPagination = true;
    useTableParams[0].manualSortBy = true;
    useTableParams[0].pageCount = controlledPageCount;
  }

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
    gotoPage,
    state: { pageIndex, sortBy },
  } = tableInstance;

  const onFetchDataDebounced = useAsyncDebounce(fetchData, 100);

  const sortFields = () => {
    const sortField = sortBy && sortBy[0] ? sortBy[0].id : 'name';
    const sortDir = sortBy && sortBy[0] && sortBy[0].desc ? 'desc' : 'asc';
    return {
      sortBy: sortField,
      direction: sortDir,
    };
  };

  useEffect(() => {
    if (manualPagination) {
      onFetchDataDebounced({
        pageIndex,
        search: searchQuery,
        ...sortFields()
      });
    }
  }, [pageIndex, sortBy, searchQuery]);

  const searchTable = (e) => {
    setSearchQuery(e.target.value);
  };

  useEffect(() => {
    gotoPage(0);
  }, [params.service, params.resource, params.finding]);

  return (
    <>
      {!disableSearch && (
        <div className="table-header">
          <div className="search-bar">
            <input onChange={searchTable} placeholder="Search by name or ID" />
          </div>
          <div className="table-header-right">
            {headerRight}
          </div>
        </div>
      )}

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

      {!disablePagination && (
        <div className="pagination">
          <ChevronLeftIcon
            onClick={previousPage}
            className={cx('icon', !canPreviousPage && 'disabled')}
          />
          {pageIndex + 1} / {pageCount}
          <ChevronRightIcon
            onClick={nextPage}
            className={cx('icon', !canNextPage && 'disabled')}
          />
        </div>
      )}
    </>
  );
};

TableRender.propTypes = propTypes;

const TableRenderMemo = React.memo(TableRender);

export default TableRenderMemo;
