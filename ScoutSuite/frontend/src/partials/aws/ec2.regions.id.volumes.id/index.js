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
    <div className="ec2-volume">
      <h3>Attributes</h3>
      <GenericObject
        data={data.item}
      />
    </div>
  );
};

Ec2Volumes.propTypes = propTypes;

export default Ec2Volumes;
