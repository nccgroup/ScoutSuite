
import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { 
  partialDataShape,
  valueOrNone, 
  convertBoolToEnable, 
  renderList
} from '../../../utils/Partials';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Vaults = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="ID"
          valuePath="id" />

        <PartialValue
          label="Location"
          valuePath="location"
          renderValue={valueOrNone} />

        <PartialValue
          label="Public Access"
          valuePath="public_access_allowed"
          renderValue={convertBoolToEnable} />

        <PartialValue
          label="Tags"
          valuePath="tags"
          renderValue={tags => renderList(tags, valueOrNone)} />

        <PartialValue
          label="Resource group"
          valuePath="resource_group_name"
          renderValue={valueOrNone} />


      </InformationsWrapper>

      
    </Partial>
  );
};

Vaults.propTypes = propTypes;

export default Vaults;
