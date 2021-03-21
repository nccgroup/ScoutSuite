import { useEffect, useState } from 'react';
import * as API from './api';
import * as Cache from './cache';

/**
 * React Hook to fetch API data and re-render the component
 * @param {*} path
 */
export const useAPI = (defaultPath, defaultValue, settings = {}) => {
  const [data, setData] = useState(
    Cache.has(defaultPath) ? Cache.get(defaultPath) : defaultValue,
  );
  const [path, setPath] = useState(defaultPath);
  const [loading, setLoading] = useState(!Cache.has(path));
  const [error, setError] = useState(null);
  const [queryParams, setQueryParams] = useState({
    page: 1,
    sortBy: 'name',
    direction: 'asc',
  });

  useEffect(() => {
    const asyncAPI = async () => {
      try {
        const response = await API.get(path);
        setData(response);
      } catch (e) {
        setError(
          'Oops! Something went wrong loading this content. Is the server working?',
        );
        console.error(e.message);
      }
      setLoading(false);
    };
    asyncAPI();
  }, [path]);

  useEffect(() => {
    var urlQueryParams = new URLSearchParams();

    if (settings.pagination) {
      urlQueryParams.set('current_page', queryParams.page);
      urlQueryParams.set('sort_by', queryParams.sortBy);
      urlQueryParams.set('direction', queryParams.direction);
    }

    setPath(
      urlQueryParams.toString().length > 0
        ? `${defaultPath}?${urlQueryParams.toString()}`
        : defaultPath,
    );
  }, [defaultPath, queryParams]);

  const loadPage = (page, sortBy, direction) => {
    setQueryParams({ page, sortBy, direction });
  };

  return {
    data: Cache.has(path) ? Cache.get(path) : data,
    loading,
    error,
    loadPage,
  };
};
