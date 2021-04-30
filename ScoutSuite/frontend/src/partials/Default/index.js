import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../components/InformationsWrapper';
import Informations from './Informations/index';


const propTypes = { data: PropTypes.object.isRequired };

const DefaultPartial = (props) => {
  const { data } = props;

  return (
    <>
      <InformationsWrapper>
        <Informations data={data.item} />
      </InformationsWrapper>

      <b>THIS IS A DEFAULT FALLBACK PARTIAL.</b>
    </>
  );
};

DefaultPartial.propTypes = propTypes;

export default DefaultPartial;
