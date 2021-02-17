/**
 * Handle the communication with the API.
 * If you are trying to access the API in a React component, use the "useAPI" hook.
 * IMPORTANT: This is a temporary mock API. It will be updated to an official version later.
 */
import * as Cache from './cache';

import json from './temp/scoutsuite_results_aws.json'; // TEMP
import items from './temp/items.json'; // TEMP

// const BASE_URL = 'http://localhost:5000'

/**
 * Gets a resource from the run results.
 * @param {string} path
 */
const getResource = (path) => {
  let data = json; // TEMP
  for (const attribute of path.split('.')) {
    data = data[attribute] || {};
  }
  return data;
};

/***
 * Make a "GET" call to the server
 * @param {string} path
 */
export const get = async (path) => {

  // Check path firt
  if (Cache.has(path)) {
    return Cache.get(path);
  }

  if (path === 'dashboards.home') {
    // TEMP
    Cache.set(path, json.last_run.summary);
    return json.last_run.summary;
  }

  if (path.endsWith('.items')) {
    // TEMP
    Cache.set(path, items);
    return items;
  }

  const data = getResource(path);
  Cache.set(path, data);

  return data;
};
