import React from 'react';
import { useAPI } from '../../../api/useAPI';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

//import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { Link, useLocation, useParams } from 'react-router-dom';
import { getFindingsEndpoint } from '../../../api/paths';

const propTypes = {
  service: PropTypes.string.isRequired,
  finding: PropTypes.string.isRequired
};

const Findings = props => {
  const { service, finding } = props;
  const { data: findings, loading } = useAPI(getFindingsEndpoint(service), []);
  const { pathname } = useLocation();
  const params = useParams();

  if (loading) return null;

  const { dashboard_name } = findings.find(({ name }) => name === finding);

  return (
    <>
      <span><Link to={`/services/${service}/findings`}>Findings</Link></span>

      <ChevronRightIcon />
      <span>
        {pathname.endsWith('/items') ? dashboard_name : <Link to={`/services/${service}/findings/${finding}/items`}>{dashboard_name}</Link>}
      </span>
      <ChevronRightIcon />

      {pathname.endsWith('/items') && <span>All Items</span>}
      {!pathname.endsWith('/items') && <span>{params.item}</span>}
    </>
  );
};

Findings.propTypes = propTypes;

export default Findings;
