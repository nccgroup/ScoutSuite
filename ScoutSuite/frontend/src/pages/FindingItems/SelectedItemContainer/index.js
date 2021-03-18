import React from 'react';
import { useParams } from '@reach/router';

import { useAPI } from '../../../api/useAPI';
import { getItemEndpoint } from '../../../api/paths';
import LazyPartial from '../../../components/LazyPartial';

const SelectedItemContainer = () => {
  const path = (new URL(document.location)).searchParams.get('path');
  const params = useParams();

  const { data: finding, loading: loading1 } = useAPI(`raw/services/${params.service}/findings/${params.finding}`);
  const { data, loading: loading2 } = useAPI(getItemEndpoint(params.service, params.finding, params.item, path));

  if (loading1 || loading2 || !data) return null;

  const partialPath = finding.display_path || finding.path;

  const partialData = {
    level: finding.level,
    ...data,
  };

  return (<LazyPartial data={partialData} partial={partialPath} />
  );
};

export default SelectedItemContainer;
