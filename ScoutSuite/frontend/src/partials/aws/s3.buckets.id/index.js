import React from 'react';
import PropTypes from 'prop-types';

import { Partial } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import Informations from './Informations';
import BucketPolicies from './BucketPolicies';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Bucket = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="left-pane">
        <Informations />
      </div>
      <BucketPolicies />
    </Partial>
  );
};

Bucket.propTypes = propTypes;

export default Bucket;
