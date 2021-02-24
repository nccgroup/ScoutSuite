import { Link, useParams } from '@reach/router';
import React from 'react';
import { PropTypes } from 'prop-types';

const propTypes = {
  value: PropTypes.string.isRequired,
  row: PropTypes.object.isRequired
};

const Name = props => {
  const params = useParams();
  const { value, row: { original } } = props;

  if (original.flagged_items && original.flagged_items > 0) {
    return (
      <Link to={`/services/${params.service}/findings/${original.id}/items`}>{value}</Link>
    );
  }

  return value;
  
};

Name.propTypes = propTypes;

export default Name;
