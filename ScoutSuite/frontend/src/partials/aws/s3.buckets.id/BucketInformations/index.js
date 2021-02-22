import React from 'react';
import PropTypes from 'prop-types';

import DetailedValue from '../../../../components/DetailedValue';

import './style.scss';

const propTypes = {
  data: PropTypes.objectOf({
    arn: PropTypes.string,
    region: PropTypes.string,
    CreationDate: PropTypes.string,
    logging: PropTypes.bool,
    defaultEncryption: PropTypes.bool,
    versioning: PropTypes.bool,
    mfaDelete: PropTypes.bool,
    secureTransport: PropTypes.bool,
    staticWebHosting: PropTypes.bool,
  }).isRequired,
};

const BucketInformations = props => {
  const {
    arn,
    region,
    CreationDate,
    logging,
    default_encryption_enabled,
    versioning_status_enabled,
    version_mfa_delete_enabled,
    secure_transport_enabled,
    web_hosting_enabled,
  } = props.data;

  const convertBoolToEnable = value => value ? 'enabled' : 'disabled';

  return (
    <div className="bucket-informations">
      <h4>Informations</h4>
      <DetailedValue label="ARN" value={arn} />
      <DetailedValue label="Region" value={region} />
      <DetailedValue label="Creation Date" value={CreationDate} />
      <DetailedValue label="Logging" value={logging} renderValue={convertBoolToEnable} />
      <DetailedValue label="Default Encryption" value={default_encryption_enabled} renderValue={convertBoolToEnable} />
      <DetailedValue label="Versioning" value={versioning_status_enabled} renderValue={convertBoolToEnable} />
      <DetailedValue label="MFA Delete" value={version_mfa_delete_enabled} renderValue={convertBoolToEnable} />
      <DetailedValue label="Secure Transport" value={secure_transport_enabled} renderValue={convertBoolToEnable} />
      <DetailedValue label="Static Web Hosting" value={web_hosting_enabled} renderValue={convertBoolToEnable} />
    </div>
  );
};

BucketInformations.propTypes = propTypes;

export default BucketInformations;
