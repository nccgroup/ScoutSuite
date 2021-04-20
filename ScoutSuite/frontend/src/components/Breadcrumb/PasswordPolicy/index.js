import React from 'react';
import PropTypes from 'prop-types';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

import { Link, useLocation } from 'react-router-dom';

const propTypes = {
  service: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
};

const PasswordPolicy = props => {
  const { service, id } = props;
  const { pathname } = useLocation();

  return (
    <>
      <span>
        {!pathname.endsWith(id) ? (
          <span>Password Policy</span>
        ) : (
          <Link to={`/services/${service}/password_policy`}>
            <span>Password Policy</span>
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

PasswordPolicy.propTypes = propTypes;

export default PasswordPolicy;
