import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const MySQLServers = props => {

  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="MySQL Server Name"
          valuePath="name" />

        <PartialValue
          label="Server SSL connection enforcement"
          valuePath="ssl_enforcement" />

      </InformationsWrapper>
    </Partial>
  );
};

MySQLServers.propTypes = propTypes;

export default MySQLServers;
