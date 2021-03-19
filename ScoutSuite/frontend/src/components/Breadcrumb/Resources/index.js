import React from 'react';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

import { useAPI } from '../../../api/useAPI';
import { getServicesEndpoint } from '../../../api/paths';
import PropTypes from 'prop-types';
import { Link, useParams, useLocation } from 'react-router-dom';

const propTypes = {
  service: PropTypes.string.isRequired,
  finding: PropTypes.string.isRequired,
};

const Resources = (props) => {
  const { service } = props;
  const { data: categories, loading } = useAPI(getServicesEndpoint(), []);
  const { pathname } = useLocation();
  const params = useParams();

  if (loading) return null;

  let resourceName = '';

  for (let category of categories) {
    for (let service of category.services) {
      for (let res of service.resources) {
        if (res.id === params.resource) resourceName = res.name;
      }
    }
  }

  return (
    <>
      <span>Resources</span>

      <ChevronRightIcon />

      <span>
        {pathname.endsWith(params.resource) ? (
          resourceName
        ) : (
          <Link to={`/services/${service}/resources/${params.resource}`}>
            {resourceName}
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
