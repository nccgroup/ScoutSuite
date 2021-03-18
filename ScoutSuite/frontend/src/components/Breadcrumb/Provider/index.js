import React from 'react';
import { useAPI } from '../../../api/useAPI';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

import AWSLogo from './Logos/aws.png';
import { Link, useParams } from 'react-router-dom';

const getProviderLogo = (providerCode) => {
  if (providerCode === 'azure') return AWSLogo;
  else if (providerCode === 'gcp') return AWSLogo;
  else return AWSLogo;
};

const Provider = () => {
  const params = useParams();
  const { data: provider, loading } = useAPI('provider');

  if (loading) return null;

  return (
    <>
      <img
        className="provider-logo"
        src={getProviderLogo(provider.provider_code)}
      />
      <span>{provider.provider_name}</span>

      <ChevronRightIcon />

      {params.service ? (
        <span>
          <Link to="/">{provider.account_id}</Link>
        </span>
      ) : (
        <span>{provider.account_id}</span>
      )}
    </>
  );
};

export default Provider;
