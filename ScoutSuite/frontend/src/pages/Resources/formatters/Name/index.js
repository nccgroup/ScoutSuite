import { useParams } from 'react-router-dom';
import React from 'react';
import PropTypes from 'prop-types';
import ResourceLink from '../../../../components/ResourceLink/index';

const propTypes = {
  value: PropTypes.string.isRequired,
  row: PropTypes.object.isRequired
};

const Name = props => {
  const params = useParams();
  const { value, row: { original } } = props;

  return (
    <ResourceLink
      service={params.service} resource={params.resource}
      id={original.id} name={value} />
  );
};

Name.propTypes = propTypes;

export default Name;
