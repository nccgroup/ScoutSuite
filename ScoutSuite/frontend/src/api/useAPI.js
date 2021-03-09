import { useEffect, useState } from 'react';
import * as API from './api';
import * as Cache from './cache';

/**
 * React Hook to fetch API data and re-render the component
 * @param {*} path
 */
export const useAPI = (path, defaultValue) => {
  const [data, setData] = useState(defaultValue);
  const [loading, setLoading] = useState(!Cache.has(path));
  const [error, setError] = useState(null);

  useEffect(() => {
    const asyncAPI = async () => {
      setLoading(true);
      try {
        const response = await API.get(path);
        setData(response);
      } catch(e) {
        setError('Oops! Something went wrong loading this content. Is the server working?');
        console.error(e.message);
      }
      setLoading(false);
    };
    asyncAPI();
  }, [path]);

  const loadMore = () => {
    // TODO: Load more content when the content is paginated
  };

  return {data: Cache.has(path) ? Cache.get(path) : data, loading, error, loadMore};
};
