import { Link, useParams } from '@reach/router';
import React from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  value: PropTypes.string.isRequired,
  row: PropTypes.object.isRequired
};

const Name = props => {
  const params = useParams();
  const { value, row: { original } } = props;

  return (
    <Link to={`/services/${params.service}/findings/${params.finding}/items/${original.id}?path=${original.display_path}`}>{value}</Link>
  );
};

Name.propTypes = propTypes;

export default Name;
