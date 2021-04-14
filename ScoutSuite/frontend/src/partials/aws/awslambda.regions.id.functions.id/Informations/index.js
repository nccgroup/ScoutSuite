import React from 'react';

import { PartialValue } from '../../../../components/Partial/index';
import { valueOrNone, formatDate } from '../../../../utils/Partials';
import ResourceLink from '../../../../components/ResourceLink';


const Informations = () => {
  return (
    <>
      <PartialValue
        label="ARN"
        valuePath="arn"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Description"
        valuePath="description"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Last Modified"
        valuePath="last_modified"
        renderValue={formatDate}
      />
      <PartialValue
        label="Runtime"
        valuePath="runtime"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Version"
        valuePath="version"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Revision ID"
        valuePath="revision_id"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Execution Role"
        valuePath="execution_role"
        renderValue={value => value ? (
          <ResourceLink 
            service="iam"
            resource="roles"
            id={value.RoleId}
            name={value.RoleName}
          />
        ) : (
          'None'
        )}
      />
      <PartialValue
        label="Handler"
        valuePath="handler"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Code Size"
        valuePath="code_size"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Memory Size"
        valuePath="memory_size"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Timeout"
        valuePath="timeout"
        renderValue={valueOrNone}
      />
    </>
  );
};

export default Informations;
