import { Link, useParams } from 'react-router-dom';
import React from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  value: PropTypes.string.isRequired,
};

const Name = props => {
  const params = useParams();
  const { value } = props;

  const id = encodeURI(value);
  const link = `/services/${params.service}/permissions/${id}`;

  if (params.id && params.id === value) {
    return <b>{value}</b>;
  }

  return (
    <Link to={link}>
      {value}
    </Link>
  );  
};

Name.propTypes = propTypes;

export default Name;
