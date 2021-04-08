import React from 'react';
import PropTypes from 'prop-types';

import './style.scss';


const propTypes = {
  children: PropTypes.node.isRequired,
};

const InformationsWrapper = props => {
  const { children } = props;

  return (
    <div className="informations-wrapper">
      <h4 className="title">Informations</h4>
      {children}
    </div>
  );
};


InformationsWrapper.propTypes = propTypes;

export default InformationsWrapper;
