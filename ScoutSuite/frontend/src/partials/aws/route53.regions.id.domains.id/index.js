
import React from 'react';
import PropTypes from 'prop-types';

import { 
  partialDataShape,
  valueOrNone,
  convertBoolToEnable,
  formatDate,
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

  return (
    <Partial data={data}>
      <div>
        <h4>Informations</h4>
        <PartialValue
          label="ARN"
          valuePath="arn"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Auto Renew"
          valuePath="auto_renew"
          renderValue={convertBoolToEnable}
        />
        <div className="transfer-lock">
          <PartialValue
            label="Transfer Lock"
            valuePath="transfer_lock"
            renderValue={convertBoolToEnable}
          />
          <PartialValue
            errorPath="transfer_lock_unauthorized"
            renderValue={() => (
              <WarningMessage 
                message="This domain's top-level domain (TLD) does not support domain locking."
              />
            )}
          />
        </div>
        <PartialValue
          label="Expiry"
          valuePath="expiry"
          renderValue={formatDate}
        />
      </div>
    </Partial>
  );
};

RegionDomain.propTypes = propTypes;

export default RegionDomain;
