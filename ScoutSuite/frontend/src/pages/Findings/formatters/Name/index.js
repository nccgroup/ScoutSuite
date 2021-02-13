import { Link } from '@reach/router';
import React from 'react';
import { PropTypes } from 'prop-types';

const propTypes = {
  value: PropTypes.string.isRequired,
  row: PropTypes.object.isRequired
};

const Name = props => {
  const { value, row: { original } } = props;

  return (
    <Link to={`/services/s3/findings/${original.id}/items`}>{value}</Link>
  );
};

Name.propTypes = propTypes;

export default Name;
