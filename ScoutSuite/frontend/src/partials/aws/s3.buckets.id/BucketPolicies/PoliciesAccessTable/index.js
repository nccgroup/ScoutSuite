import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { PartialContext, PartialPathContext } from '../../../../../components/Partial/context';

const propTypes = {
  columnName: PropTypes.string.isRequired,
};

const PoliciesAccessTable = props => {
  const { columnName } = props;

  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const value = get(ctx.item, basePath);

  return (
    <table>
      <thead>
        <tr>
          <th>{columnName}</th>
          <th>Policy Name</th>
          <th>Condition</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(value).map(([id, accessGroup]) => {
          const policies = accessGroup.policies || accessGroup.inline_policies;
          
          return Object.entries(policies).map(([policy_id, policy], i) => (
            <tr key={policy_id}>
              {i == 0 && (
                <td rowSpan={Object.keys(policies).length}>
                  {id}
                </td>
              )}
              <td>
                {policy_id}
              </td>
              <td>
                {(get(policy, 'condition', null) != null).toString()}
              </td>
            </tr>
          ));
        })}
      </tbody>
    </table>
  );
};

PoliciesAccessTable.propTypes = propTypes;

export default PoliciesAccessTable;
