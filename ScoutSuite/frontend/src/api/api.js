/**
 * Handle the communication with the API.
 * If you are trying to access the API in a React component, use the "useAPI" hook.
 * IMPORTANT: This is a temporary mock API. It will be updated to an official version later.
 */
import axios from 'axios';
import * as Cache from './cache';

export const BASE_URL = process.env.SERVER_URL || 'http://localhost:5000';

/***
 * Make a "GET" call to the server
 * @param {string} path
 */
export const get = async (path) => {

  // Check path firt
  if (Cache.has(path)) {
    return Cache.get(path);
  }

  const { data } = await axios.get(BASE_URL + '/api/' + path);
  Cache.set(path, data);
  
  return data;
};
