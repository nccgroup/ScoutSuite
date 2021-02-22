import React from 'react';
import PropTypes from 'prop-types';

import DetailedValue from '../../../components/DetailedValue';

import './style.scss';

const propTypes = {
  data: PropTypes.objectOf({
    arn: PropTypes.string,
    region: PropTypes.string,
    creationDate: PropTypes.string,
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
    creationDate,
    logging,
    defaultEncryption,
    versioning,
    mfaDelete,
    secureTransport,
    staticWebHosting,
  } = props.data;

  const convertBoolToEnable = value => value ? 'enabled' : 'disabled';

  return (
    <div className="bucket-informations">
      <h4>Informations</h4>
      <DetailedValue label="ARN" value={arn} />
      <DetailedValue label="Region" value={region} />
      <DetailedValue label="Creation Date" value={creationDate} />
      <DetailedValue label="Logging" value={logging} renderValue={convertBoolToEnable} />
      <DetailedValue label="Default Encryption" value={defaultEncryption} renderValue={convertBoolToEnable} />
      <DetailedValue label="Versioning" value={versioning} renderValue={convertBoolToEnable} />
      <DetailedValue label="MFA Delete" value={mfaDelete} renderValue={convertBoolToEnable} />
      <DetailedValue label="Secure Transport" value={secureTransport} renderValue={convertBoolToEnable} />
      <DetailedValue label="Static Web Hosting" value={staticWebHosting} renderValue={convertBoolToEnable} />
    </div>
  );
};

BucketInformations.propTypes = propTypes;

export default BucketInformations;
