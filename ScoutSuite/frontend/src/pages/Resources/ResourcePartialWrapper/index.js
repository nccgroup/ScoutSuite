import React from 'react';
import { useParams } from 'react-router-dom';
import merge from 'lodash/merge';
import get from 'lodash/get';

import { useAPI } from '../../../api/useAPI';
import { getRAWEndpoint } from '../../../api/paths';
import LazyPartial from '../../../components/LazyPartial/index';

const propTypes = {};

const ResourcePartialWrapper = () => {

  const path = (new URL(document.location)).searchParams.get('path');
  const params = useParams();

  const { data: metadata, loading: l1 } = useAPI(getRAWEndpoint('metadata'));
  const { data, loading: l2 } = useAPI(getRAWEndpoint(path));

  if (l1 || l2 || !data) return null;

  // TEMPORATY WHILE WAITING FOR THE BACKEND API
  const services = merge(...Object.values(metadata));
  const resourceMeta = get(services, [params.service, 'resources', params.resource]);

  const partialPath = resourceMeta.path.replace('services.', '') + '.id';

  const partialData = {
    item: data,
    path_to_issues: []
  };
 
  return (
    <LazyPartial data={partialData} partial={partialPath} />
  );
};

ResourcePartialWrapper.propTypes = propTypes;

export default ResourcePartialWrapper;
