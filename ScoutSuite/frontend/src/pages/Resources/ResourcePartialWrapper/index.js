import React, { Suspense } from 'react';
import { useParams } from '@reach/router';

import { useAPI } from '../../../api/useAPI';
import { getItemEndpoint } from '../../../api/paths';

import './style.scss';

const propTypes = {};

const ResourcePartialWrapper = () => {

  const path = (new URL(document.location)).searchParams.get('path');
  const params = useParams();
  const { data: provider } = useAPI('provider');
  const { data: finding, loading: loading1 } = useAPI(`raw/services/${params.service}/findings/${params.finding}`);
  const { data, loading: loading2 } = useAPI(getItemEndpoint(params.service, params.finding, params.item, path));

  if (loading1 || loading2 || !data) return null;

  const partialPath = finding.display_path || finding.path;

  const DynamicPartial = React.lazy(async () => {
    let md = null;
    try {
      md = await import('../../../partials/' + provider.provider_code + '/' + partialPath + '/index.js'); // Can't use a string literal because of Babel bug
    } catch(e) {
      md = await import('../../../partials/Default');
    }
    return md;
  }); 

  const partialData = {
    level: finding.level,
    ...data,
  };

  return (
    <div className="selected-item-container">
      <div className="header">
        <h3>{data.item.name}</h3>
      </div>
      <div className="content">
        <Suspense fallback={<span>Loading...</span>}>
          <DynamicPartial data={partialData} />
        </Suspense>
      </div>
    </div>
  );
};

ResourcePartialWrapper.propTypes = propTypes;

export default ResourcePartialWrapper;
