
import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { 
  partialDataShape,
  
} from '../../../utils/Partials';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Pricings = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Pricing Name"
          valuePath="name" />

        <PartialValue
          label="Pricing Tier"
          valuePath="pricing_tier" />

      </InformationsWrapper>      
    </Partial>
  );
};

Pricings.propTypes = propTypes;

export default Pricings;
