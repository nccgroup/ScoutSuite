import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';


const Informations = () => {
  return (
    <div className="partial-informations">
      <h4>Informations</h4>
      <PartialValue label="ID" valuePath="id" />
      <PartialValue label="Description" valuePath="description" />
    </div>
  );
};

export default Informations;
