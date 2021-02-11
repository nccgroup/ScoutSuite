import React from 'react';
//import { useAPI } from '../../../api/useAPI';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

//import { Link } from '@reach/router';
import { PropTypes } from 'prop-types';
import { useLocation } from '@reach/router';

const propTypes = {
  service: PropTypes.string.isRequied
};

const Service = props => {
  const { service } = props;
  const { pathname } = useLocation();

  console.log(pathname);

  return (
    <>
      <ChevronRightIcon />
      <span>{service}</span>
      <ChevronRightIcon />

      {pathname.endsWith('/findings') && <span>Findings</span>}
      {pathname.endsWith('/external-attacks') && <span>External Attacks Surface</span>}
    </>
  );
};

Service.propTypes = propTypes;

export default Service;
