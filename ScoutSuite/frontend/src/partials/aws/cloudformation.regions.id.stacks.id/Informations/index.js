import React from 'react';
import isEmpty from 'lodash/isEmpty';
import ReportProblemOutlinedIcon from '@material-ui/icons/ReportProblemOutlined';

import { PartialValue } from '../../../../components/Partial/index';
import { formatDate } from '../../../../utils/Partials';

import './style.scss';


const Informations = () => {
  return (
    <>
      <PartialValue
        label="ARN"
        valuePath="arn"
      />
      <PartialValue
        label="Region"
        valuePath="region"
      />
      <PartialValue
        label="Created on"
        valuePath="CreationTime"
        renderValue={formatDate}
      />
      <PartialValue
        label="Role"
        valuePath="iam_role.name"
        renderValue={
          // TODO: link to resource
          value => value ? (
            <>
              {value}
              <PartialValue
                className="role-icon"
                errorPath={value}
                renderValue={() => <ReportProblemOutlinedIcon fontSize="inherit" />}
              />
            </>
          ) : 'None'
        }
      />
      <PartialValue
        label="Termination protection enabled"
        valuePath="EnableTerminationProtection"
        errorPath="cloudformation_stack_no_termination_protection"
      />
      <PartialValue
        label="Configuration has drifted"
        valuePath="drifted"
        errorPath="cloudformation_stack_drifted"
      />
      <PartialValue
        label="Deletion policy"
        valuePath="deletion_policy"
        errorPath="cloudformation_stack_no_deletion_policy"
      />
      <PartialValue
        label="Notification ARNs"
        valuePath="notificationARNs"
        errorPath="cloudformation_stack_lacks_notifications"
        renderValue={value => !isEmpty(value) ? (
          <ul>
            {value.map((arn, i) => (
              <li key={i}>
                {arn}
              </li>
            ))}
          </ul>
        ) : 'None'}
      />
      <PartialValue
        className="stack-description"
        valuePath="Description"
        renderValue={value => value && (
          <>
            <h4>Description</h4>
            {value}
          </>
        )}
      />
    </>
  );
};

export default Informations;
