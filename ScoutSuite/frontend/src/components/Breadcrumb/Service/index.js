import React from 'react';
import { useLocation } from '@reach/router';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import PropTypes from 'prop-types';

import { makeTitle } from '../../../utils/Partials';


const propTypes = {
  service: PropTypes.string.isRequired
};

const Service = props => {
  const { service } = props;
  const { pathname } = useLocation();

  return (
    <>
      <ChevronRightIcon />
      <span>{makeTitle(service)}</span>
      <ChevronRightIcon />

      {pathname.endsWith('/findings') && <span>Findings</span>}
      {pathname.endsWith('/external-attacks') && <span>External Attacks Surface</span>}
    </>
  );
};

Service.propTypes = propTypes;

export default Service;
