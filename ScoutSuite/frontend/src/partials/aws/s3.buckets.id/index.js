import React from 'react';
import PropTypes from 'prop-types';

import { Partial } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import InformationsWrapper from '../../../components/InformationsWrapper';
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
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <BucketPolicies />
    </Partial>
  );
};

Bucket.propTypes = propTypes;

export default Bucket;
