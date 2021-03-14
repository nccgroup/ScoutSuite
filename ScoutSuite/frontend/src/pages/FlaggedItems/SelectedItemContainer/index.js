import React, { Suspense } from 'react';
import { useParams } from '@reach/router';
import get from 'lodash/get';

import { useAPI } from '../../../api/useAPI';
import { getItem } from '../../../api/paths';

import './style.scss';


const SelectedItemContainer = () => {
  const path = (new URL(document.location)).searchParams.get('path');
  const params = useParams();
  const { data: finding, loading: loading1 } = useAPI(`raw/services/${params.service}/findings/${params.finding}`);
  const { data, loading: loading2 } = useAPI(getItem(params.service, params.finding, params.item, path));

  if (loading1 || loading2 || !data) return null;

  const partialPath = finding.display_path || finding.path;

  const DynamicPartial = React.lazy(async () => {
    let md = null;
    try {
      md = await import('../../../partials/aws/' + partialPath + '/index.js'); // Can't use a string literal because of Babel bug
    } catch(e) {
      md = await import('../../../partials/Default');
    }
    return md;
  }); 

  const partialData = {
    level: finding.level,
    ...data,
  };

  console.log(data, finding);

  return (
    <div className="selected-item-container">
      <div className="header">
        <h3>{get(data, ['item', 'name'])}</h3>
      </div>
      <div className="content">
        <Suspense fallback={<span>Loading...</span>}>
          <DynamicPartial data={partialData} />
        </Suspense>
      </div>
    </div>
  );
};

export default SelectedItemContainer;
