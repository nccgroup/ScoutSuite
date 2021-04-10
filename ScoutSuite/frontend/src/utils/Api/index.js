import get from 'lodash/get';


export const getRegionFromPath = path => get(path.match(/regions\.([^.]*)/), 1);

export const getVpcFromPath = path => get(path.match(/vpcs\.([^.]*)/), 1);
