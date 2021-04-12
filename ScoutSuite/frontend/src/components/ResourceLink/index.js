import React from 'react';
import { PropTypes } from 'prop-types';
import { Link } from 'react-router-dom';
import ResourceName from '../ResourceName/index';


const propTypes = {
  service: PropTypes.string.isRequired,
  resource: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  name: PropTypes.string,
  nameProps: PropTypes.object,
};

const ResourceLink = props => {
  const {
    service,
    resource,
    id,
    name,
    nameProps
  } = props;

  return (
    <Link to={`/services/${service}/resources/${resource}/${id}`}>
      {name || (
        <ResourceName
          service={service} 
          resource={resource}
          id={id}
          {...nameProps}
        />
      )}
    </Link>
  );
};

ResourceLink.propTypes = propTypes;

export default ResourceLink;
