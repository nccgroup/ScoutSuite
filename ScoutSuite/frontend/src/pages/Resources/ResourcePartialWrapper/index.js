import React from 'react';
import { useParams } from 'react-router-dom';
import merge from 'lodash/merge';
import get from 'lodash/get';
import { useAPI } from '../../../api/useAPI';
import { getRawEndpoint, getResourceEndpoint } from '../../../api/paths';
import LazyPartial from '../../../components/LazyPartial/index';
import ErrorBoundary from '../../../components/ErrorBoundary/index';

const propTypes = {};

const ResourcePartialWrapper = () => {

  //const path = (new URL(document.location)).searchParams.get('path');
  const params = useParams();

  const { data: metadata, loading: l1 } = useAPI(getRawEndpoint('metadata'));
  const { data, loading: l2, reloading } = useAPI(getResourceEndpoint(params.service, params.resource, params.id));

  if (l1 || l2 || !data || reloading) return null;

  // TEMPORATY WHILE WAITING FOR THE BACKEND API
  const services = merge(...Object.values(metadata));
  const resourceMeta = get(services, [params.service, 'resources', params.resource]);

  const partialPath = resourceMeta.path.replace('services.', '') + '.id';

  const partialData = {
    item: data,
    path_to_issues: []
  };
 
  return (
    <ErrorBoundary>
      <LazyPartial data={partialData} partial={partialPath} />
    </ErrorBoundary>
  );
};

ResourcePartialWrapper.propTypes = propTypes;

export default ResourcePartialWrapper;
