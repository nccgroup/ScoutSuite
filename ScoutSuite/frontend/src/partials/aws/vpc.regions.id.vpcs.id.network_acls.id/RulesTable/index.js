import React from 'react';
import PropTypes from 'prop-types';

import { PartialValue } from '../../../../components/Partial';

import './style.scss';


const propTypes = {
  rules: PropTypes.object.isRequired,
  type: PropTypes.oneOf([
    'egress', 
    'ingress'
  ]).isRequired,
};

const RulesTable = props => {
  const {
    rules,
    type,
  } = props;

  return (
    <table className="rules-table">
      <thead>
        <tr>
          <th>Rule Number</th>
          <th>Port</th>
          <th>Protocol</th>
          <th>IP Address</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(rules[type]).map(([rule_id, rule]) => (
          <tr key={rule_id}>
            <td>
              <PartialValue
                value={rule_id}
                errorPath={`${type}.${rule_id}`}
              />
            </td>
            <td>
              <PartialValue
                value={rule.port_range}
                errorPath={`${type}.${rule_id}`}
              />
            </td>
            <td>
              <PartialValue
                value={rule.protocol}
                errorPath={`${type}.${rule_id}`}
              />
            </td>
            <td>
              <PartialValue
                value={rule.CidrBlock}
                errorPath={`${type}.${rule_id}`}
              />
              
            </td>
            <td>
              <PartialValue
                value={rule.RuleAction}
                errorPath={`${type}.${rule_id}`}
              />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

RulesTable.propTypes = propTypes;

export default RulesTable;
