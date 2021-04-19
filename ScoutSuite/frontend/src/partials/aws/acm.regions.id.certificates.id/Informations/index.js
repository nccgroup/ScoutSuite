import React from 'react';
import isEmpty from 'lodash/isEmpty';

import { PartialValue } from '../../../../components/Partial/index';
import { valueOrNone, formatDate } from '../../../../utils/Partials';


const Informations = () => {
  return (
    <>
      <PartialValue
        label="ARN"
        valuePath="arn"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Domain Name"
        valuePath="DomainName"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Subject"
        valuePath="Subject"
        renderValue={formatDate}
      />
      <PartialValue
        label="Subject Alternative Names"
        valuePath="SubjectAlternativeNames"
        renderValue={value => !isEmpty(value) && (
          <ul>
            {value.map((name, i) => (
              <li key={i}>
                {name}
              </li>
            ))}
          </ul>
        )}
      />
      <PartialValue
        label="Status"
        valuePath="Status"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Issuer"
        valuePath="Issuer"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Type"
        valuePath="Type"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Created"
        valuePath="CreatedAt"
        renderValue={formatDate}
      />
      <PartialValue
        label="Expiration"
        valuePath="NotAfter"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Renewal Eligibility"
        valuePath="RenewalEligibility"
        renderValue={valueOrNone}
      />
      <PartialValue
        label="Transparency Logging Preference"
        valuePath="Options.CertificateTransparencyLoggingPreference"
        errorPath="CertificateTransparencyLoggingPreference"
        renderValue={valueOrNone}
      />
    </>
  );
};

export default Informations;
