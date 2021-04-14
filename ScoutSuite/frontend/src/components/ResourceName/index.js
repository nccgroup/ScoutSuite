import React from 'react';
import { useAPI } from '../../api/useAPI';
import { getResourceEndpoint } from '../../api/paths';
import Skeleton from '@material-ui/lab/Skeleton';
import { PropTypes } from 'prop-types';


const propTypes = {
  service: PropTypes.string.isRequired,
  resource: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  renderData: PropTypes.func,
};

const defaultProps = {
  renderData: data => data.name,
};

const ResourceName = ({service, resource, id, renderData }) => {
  const { data, loading } = useAPI(getResourceEndpoint(service, resource, id));

  if (loading) return (
    <span>
      <Skeleton width="40" />
    </span>
  );

  return <span>{renderData(data)}</span>;
};

ResourceName.propTypes = propTypes;
ResourceName.defaultProps = defaultProps;

export default ResourceName;
