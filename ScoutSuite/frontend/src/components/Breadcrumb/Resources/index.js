import React from 'react';
import PropTypes from 'prop-types';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import flatten from 'lodash/flatten';

import { useAPI } from '../../../api/useAPI';
import { getServicesEndpoint } from '../../../api/paths';
import { Link, useParams, useLocation } from 'react-router-dom';

const propTypes = {
  service: PropTypes.string.isRequired,
  finding: PropTypes.string,
};

const Resources = (props) => {
  const { service } = props;
  const { data: categories, loading } = useAPI(getServicesEndpoint(), []);
  const { pathname } = useLocation();
  const params = useParams();

  if (loading) return null;

  const services = flatten(categories.map(c => c.services));
  const resources = flatten(services.map(s => s.resources));
  const resource = resources.find((res) => res.id === params.resource);

  return (
    <>
      <span>Resources</span>

      <ChevronRightIcon />

      <span>
        {pathname.endsWith(params.resource) ? (
          resource.name
        ) : (
          <Link to={`/services/${service}/resources/${params.resource}`}>
            {resource.name}
          </Link>
        )}
      </span>

      <ChevronRightIcon />

      {pathname.endsWith(params.resource) && <span>All Items</span>}
      {!pathname.endsWith(params.resource) && <span>{params.id}</span>}
    </>
  );
};

Resources.propTypes = propTypes;

export default Resources;
