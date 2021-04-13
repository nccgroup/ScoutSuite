import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const CustomRolesreport = props => {

  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue label="No Administering Resource Locks Role" valuePath="missing_custom_role_administering_resource_locks" />
      </InformationsWrapper>
    </Partial>
  );
};

CustomRolesreport.propTypes = propTypes;

export default CustomRolesreport;
