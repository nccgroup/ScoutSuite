import React, { useContext } from 'react';
import get from 'lodash/get';

import { PartialContext, PartialPathContext } from '../../../../../components/Partial/context';
import { PartialValue } from '../../../../../components/Partial';
import { convertBoolToCheckmark } from '../../../../../utils/Partials';


const AccessControlList = () => {
  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const value = get(ctx.item, basePath);  

  return (
    <table className="acl-table">
      <thead>
        <tr>
          <th/>
          <th>List</th>
          <th>Upload/Delete</th>
          <th>View Permissions</th>
          <th>Edit Permissions</th>
        </tr>
      </thead>
      <tbody>
        {Object.keys(value).map(id => (
          <tr key={id}>
            <td>
              <PartialValue 
                valuePath={`${id}.DisplayName`} 
                tooltip
              />
            </td>
            <td>
              <PartialValue 
                valuePath={`${id}.permissions.read`}
                errorPath={`${id}.read`}
                renderValue={convertBoolToCheckmark}
              />
            </td>
            <td>
              <PartialValue 
                valuePath={`${id}.permissions.read_acp`}
                errorPath={`${id}.read_acp`}
                renderValue={convertBoolToCheckmark}
              />
            </td>
            <td>
              <PartialValue 
                valuePath={`${id}.permissions.write`}
                errorPath={`${id}.write`}
                renderValue={convertBoolToCheckmark}
              />
            </td>
            <td>
              <PartialValue 
                valuePath={`${id}.permissions.write_acp`}
                errorPath={`${id}.write_acp`}
                renderValue={convertBoolToCheckmark}
              />
            </td>
          </tr>
        ))}
        
      </tbody>
    </table>
  );
};

export default AccessControlList;
