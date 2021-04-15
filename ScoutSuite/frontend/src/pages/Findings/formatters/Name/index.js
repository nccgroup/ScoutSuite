import { Link, useParams } from 'react-router-dom';
import React from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  value: PropTypes.string.isRequired,
  row: PropTypes.object.isRequired
};

const Name = props => {
  const params = useParams();
  const { value, row: { original } } = props;

  const link = original.redirect_to 
    ? `${original.redirect_to}/${original.id}`
    : `/services/${params.service}/findings/${original.id}/items`;

  if (original.flagged_items && original.flagged_items > 0) {
    return (
      <Link to={link}>
        {value}
      </Link>
    );
  }

  return value;
  
};

Name.propTypes = propTypes;

export default Name;
