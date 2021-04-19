import React, { useContext } from 'react';
import get from 'lodash/get';

import { PartialContext, PartialPathContext } from '../../../../components/Partial/context';
import { PartialValue } from '../../../../components/Partial';
import { convertBoolToCheckmark } from '../../../../utils/Partials';


const AccessControlList = () => {
  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const value = get(ctx.item, basePath);  

  return (
    <table className="acl-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Encrypted</th>
          <th>Permissions</th>
        </tr>
      </thead>
      <tbody>
        {Object.keys(value).map(id => (
          <tr key={id}>
            <td>
              {id.name}
            </td>
            <td>
              {/* TODO: this hasn't been tested */}
              <PartialValue 
                valuePath={`${id}.ServerSideEncryption`}
                errorPath={`${id}.unencrypted`}
                renderValue={convertBoolToCheckmark}
              />
            </td>
            <td>
              <PartialValue 
                valuePath={`${id}.grantees`}
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
