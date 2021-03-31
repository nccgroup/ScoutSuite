import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { 
  partialDataShape, 
  convertBoolToEnable,
  formatDate,
  valueOrNone,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import WarningMessage from '../../../components/WarningMessage';

import './style.scss';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const RegionDomain = props => {
  const { data } = props;

  if (!data) return null;

  const isLogging = get(data, ['item', 'IsLogging']);
  const scoutLink = get(data, ['item', 'scout_link']);

  return (
    <Partial data={data}>
      <div className="cloudtrail-trails">
        <h4>Informations</h4>
        <PartialValue
          label="ARN"
          valuePath="arn"
        />
        <PartialValue
          label="Region"
          valuePath="HomeRegion"
        />
        {scoutLink ? (
          <WarningMessage
            message="Multi-trail region"
          />
        ) : (
          <>
            <PartialValue
              label="Logging"
              valuePath="IsLogging"
              renderValue={convertBoolToEnable}
            />
            <PartialValue
              label="Start Logging Time"
              valuePath="StartLoggingTime"
              renderValue={formatDate}
            />
            <PartialValue
              label="Stop Logging Time"
              valuePath="StopLoggingTime"
              renderValue={formatDate}
            />
            <PartialValue
              label="Multi Region"
              valuePath="IsMultiRegionTrail"
              errorPath="IsLogging"
              renderValue={convertBoolToEnable}
            />
            <PartialValue
              label="Management Events"
              valuePath="ManagementEventsEnabled"
              errorPath="cloudtrail-management-events-disabled"
              renderValue={convertBoolToEnable}
            />
            <PartialValue
              label="Data Events"
              valuePath="DataEventsEnabled"
              errorPath="cloudtrail-data-events-disabled"
              renderValue={convertBoolToEnable}
            />
            <PartialValue
              label="Include Global Services"
              valuePath="IncludeGlobalServiceEvents"
              errorPath={[
                'GlobalServicesDuplicated',
                'IncludeGlobalServiceEvents',
              ]}
              renderValue={value => convertBoolToEnable(value && isLogging)}
            />
            {/* TODO: Link to resource */}
            <PartialValue
              label="Destination S3 Bucket Name"
              valuePath="bucket_id"
            />
            <PartialValue
              label="Log File Validation Enabled"
              valuePath="LogFileValidationEnabled"
              errorPath="LogFileValidationDisabled"
              renderValue={convertBoolToEnable}
            />
            <PartialValue
              label="KMS Key"
              valuePath="KmsKeyId"
              errorPath="cloudtrail-kms-key-unused"
              renderValue={valueOrNone}
            />
            <PartialValue
              label="Latest CloudWatch Logs Delivery Time"
              valuePath="LatestCloudWatchLogsDeliveryTime"
              errorPath="TrailCloudwatchNoIntegration"
              renderValue={formatDate}
            />
          </>
        )}
      </div>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
