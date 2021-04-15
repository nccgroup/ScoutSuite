import React from 'react';
import { useParams } from 'react-router-dom';

import { useAPI } from '../../../api/useAPI';
import { getItemEndpoint } from '../../../api/paths';
import LazyPartial from '../../../components/LazyPartial';
import ErrorBoundary from '../../../components/ErrorBoundary';

const SelectedItemContainer = () => {
  const path = new URL(document.location).searchParams.get('path');
  const params = useParams();

  const { data: finding, loading: loading1 } = useAPI(
    `raw/services/${params.service}/findings/${params.finding}`,
  );
  const { data, loading: loading2 } = useAPI(
    getItemEndpoint(params.service, params.finding, params.item, path),
  );

  if (loading1 || loading2 || !data) return null;

  const partialPath = finding.display_path || finding.path;

  const partialData = {
    level: finding.level,
    ...data,
  };

  return <ErrorBoundary>
    <LazyPartial
      data={partialData} path={path}
      partial={partialPath} />
  </ErrorBoundary>;
};

export default SelectedItemContainer;
