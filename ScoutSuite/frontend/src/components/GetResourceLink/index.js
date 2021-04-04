import React from 'react';
import { PropTypes } from 'prop-types';
import { Link } from 'react-router-dom';
import GetResourceName from '../GetResourceName/index';

const propTypes = {
  service: PropTypes.string.name,
  resource: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
};

const GetResourceLink = ({ service, resource, id }) => {
  return (
    <Link to={`/services/${service}/resources/${resource}/${id}`}>
      <GetResourceName
        service={service} resource={resource}
        id={id} />
    </Link>
  );
};

GetResourceLink.propTypes = propTypes;

export default GetResourceLink;
