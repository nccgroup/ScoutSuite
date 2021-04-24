import React from 'react';
import PropTypes from 'prop-types';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

import { Link, useLocation } from 'react-router-dom';

const propTypes = {
  service: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
};

const Permissions = props => {
  const { service, id } = props;
  const { pathname } = useLocation();

  return (
    <>
      <span>
        {!pathname.endsWith(id) ? (
          <span>Permissions</span>
        ) : (
          <Link to={`/services/${service}/permissions`}>
            <span>Permissions</span>
          </Link>
        )}
      </span>

      {pathname.endsWith(id) && (
        <>
          <ChevronRightIcon /> <span>{id}</span>
        </>
      )}
    </>
  );
};

Permissions.propTypes = propTypes;

export default Permissions;
