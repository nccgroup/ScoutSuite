import React from 'react';
import { PropTypes } from 'prop-types';

import Informations from './Informations/index';


const propTypes = { data: PropTypes.object.isRequired };

const DefaultPartial = (props) => {
  const { data } = props;

  return (
    <>
      <div className="left-pane">
        <Informations data={data.item} />
      </div>

      <b>THIS IS A DEFAULT FALLBACK PARTIAL.</b>
    </>
  );
};

DefaultPartial.propTypes = propTypes;

export default DefaultPartial;
