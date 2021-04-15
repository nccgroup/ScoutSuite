import React from 'react';
import PropTypes from 'prop-types';

import GenericObject from '../../../components/Partial/GenericObject';
import { partialDataShape } from '../../../utils/Partials';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Clusters = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <div>
      <h4>Attributes</h4>
      <GenericObject
        data={data.item}
      />
    </div>
  );
};

Clusters.propTypes = propTypes;

export default Clusters;
