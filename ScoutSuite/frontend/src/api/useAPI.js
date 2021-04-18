import { useEffect, useState } from 'react';
import * as API from './api';
import * as Cache from './cache';
import isEmpty from 'lodash/isEmpty';

/**
 * React Hook to fetch API data and re-render the component
 * @param {*} path
 */
export const useAPI = (defaultPath, defaultValue, settings = {}) => {
  const [data, setData] = useState(null);
  const [path, setPath] = useState(defaultPath);
  const [loading, setLoading] = useState(!Cache.has(path));
  const [reloading, setReloading] = useState(false);
  const [error, setError] = useState(null);
  const [queryParams, setQueryParams] = useState({
    page: 1,
    sortBy: null,
    direction: null,
    filters: {},
  });

  useEffect(() => {
    setReloading(true);
    const asyncAPI = async () => {
      try {
        const response = await API.get(path);
        setData(response);
      } catch (e) {
        setData(defaultValue);
        setError(
          'Oops! Something went wrong loading this content. Is the server working?',
        );
        console.error(e.message);
      }
      setLoading(false);
      setReloading(false);
    };
    asyncAPI();
  }, [path]);

  useEffect(() => {
    var urlQueryParams = new URLSearchParams();

    if (settings.pagination) {
      urlQueryParams.set('current_page', queryParams.page);
      if (queryParams.sortBy) urlQueryParams.set('sort_by', queryParams.sortBy);
      if (queryParams.sortBy && queryParams.direction)
        urlQueryParams.set('direction', queryParams.direction);
      if (queryParams.search && queryParams.search.length > 0)
        urlQueryParams.set('search', queryParams.search);
      if (!isEmpty(queryParams.filters))
        urlQueryParams.set('filter_by', JSON.stringify(queryParams.filters));
    }

    setPath(
      urlQueryParams.toString().length > 0
        ? `${defaultPath}?${urlQueryParams.toString()}`
        : defaultPath,
    );
  }, [defaultPath, queryParams]);

  const loadPage = (page, sortBy, direction, search, filters) => {
    setQueryParams({
      page,
      sortBy: sortBy || null,
      direction: direction || null,
      search,
      filters,
    });
  };

  return {
    data: Cache.has(path) ? Cache.get(path) : data,
    loading,
    error,
    loadPage,
    reloading,
  };
};
