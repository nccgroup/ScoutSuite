import React from 'react';
// import PropTypes from 'prop-types';

import Breadcrumb from '../../components/Breadcrumb/index';

import './style.scss';

const propTypes = {};

const ExternalAttack = () => {

  return (
    <>
      <Breadcrumb />
      <div>
        External Attack Surface page
      </div>
    </>
  );
};

ExternalAttack.propTypes = propTypes;

export default ExternalAttack;
