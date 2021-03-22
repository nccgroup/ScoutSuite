import React from 'react';
import { useAPI } from '../../api/useAPI';
import { getResourceEndpoint } from '../../api/paths';
import Skeleton from '@material-ui/lab/Skeleton';
import { PropTypes } from 'prop-types';

const propTypes = {
  service: PropTypes.string.name,
  resource: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
};

const GetResourceName = ({service, resource, id}) => {
  const { data, loading } = useAPI(getResourceEndpoint(service, resource, id));

  if (loading) return <span>
    <Skeleton width="40" />
  </span>;

  return <span>
    {data.name}
  </span>;
};

GetResourceName.propTypes = propTypes;

export default GetResourceName;
