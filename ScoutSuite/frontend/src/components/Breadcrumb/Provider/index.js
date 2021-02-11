import React from 'react';
import { useAPI } from '../../../api/useAPI';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

import AWSLogo from './Logos/aws.png';
import { Link } from '@reach/router';

const getProviderLogo = (providerCode) => {
  if (providerCode === 'azure') return AWSLogo;
  else if (providerCode === 'gcp') return AWSLogo;
  else return AWSLogo;
};

const Provider = () => {
  const { data: providerCode } = useAPI('provider_code');
  const { data: providerName, loading: l1 } = useAPI('provider_name');
  const { data: acccountID, loading: l2} = useAPI('account_id');


  if (l1 || l2) return null;

  return (
    <>
      <img className="provider-logo" src={getProviderLogo(providerCode)} />
      <span>{providerName}</span>

      <ChevronRightIcon />

      <span><Link to="/">{acccountID}</Link></span>
    </>
  );
};

export default Provider;
