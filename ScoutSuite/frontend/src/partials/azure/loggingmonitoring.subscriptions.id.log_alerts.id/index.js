import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape, valueOrNone } from '../../../utils/Partials';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const LogAlerts = props => {

  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue 
          label="Create Policy Assignment activity log alert exist" 
          valuePath="create_policy_assignment_exist"
          renderValue={valueOrNone} />
      
        <PartialValue 
          label="Create or update Network Security Group activity log alert exist" 
          valuePath="create_update_NSG_exist"
          renderValue={valueOrNone} />

        <PartialValue 
          label="Delete Network Security Group activity log alert exist" 
          valuePath="delete_NSG_exist"
          renderValue={valueOrNone} />

        <PartialValue 
          label="Create or update Network Security Group Rule activity log alert exist" 
          valuePath="create_update_NSG_rule_exist"
          renderValue={valueOrNone} />

        <PartialValue 
          label="Delete Network Security Group Rule activity log alert exist" 
          valuePath="delete_NSG_rule_exist"
          renderValue={valueOrNone} />

        <PartialValue 
          label="Create or update Security Solution activity log alert exist" 
          valuePath="create_update_security_solution_exist"
          renderValue={valueOrNone} />

        <PartialValue 
          label="Delete Security Solution activity log alert exist" 
          valuePath="delete_security_solution_exist"
          renderValue={valueOrNone}/>

        <PartialValue 
          label="Create our update or delete SQL Server Firewall Rule activity log alert exist" 
          valuePath="create_delete_firewall_rule_exist"
          renderValue={valueOrNone}/>

      </InformationsWrapper>
    </Partial>
  );
};

LogAlerts.propTypes = propTypes;

export default LogAlerts;
