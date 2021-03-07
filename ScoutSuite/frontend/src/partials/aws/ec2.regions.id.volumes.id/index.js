import React from 'react';
import PropTypes from 'prop-types';

import GenericObject from '../../../components/Partial/GenericObject';
import { partialDataShape } from '../../../utils/Partials';

import './style.scss';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Ec2Volumes = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <GenericObject
      className="partial-informations ec2-volumes"
      data={data.item}
    />
  );
};

Ec2Volumes.propTypes = propTypes;

export default Ec2Volumes;
