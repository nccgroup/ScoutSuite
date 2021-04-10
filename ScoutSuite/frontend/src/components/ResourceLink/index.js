import React from 'react';
import { PropTypes } from 'prop-types';
import { Link } from 'react-router-dom';
import ResourceName from '../ResourceName/index';

const propTypes = {
  service: PropTypes.string.isRequired,
  resource: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  name: PropTypes.string,
};

const ResourceLink = ({ service, resource, id, name }) => {
  return (
    <Link to={`/services/${service}/resources/${resource}/${id}`}>
      {name || (
        <ResourceName
          service={service} 
          resource={resource}
          id={id} 
        />
      )}
    </Link>
  );
};

ResourceLink.propTypes = propTypes;

export default ResourceLink;
