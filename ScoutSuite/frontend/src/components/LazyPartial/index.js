import React, { Suspense } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { useAPI } from '../../api/useAPI';

import './style.scss';

const propTypes = {
  data: PropTypes.shape({
    item: PropTypes.object,
    path_to_issues: PropTypes.arrayOf(PropTypes.string)
  }).isRequired,
  partial: PropTypes.string.isRequired,
};

const LazyPartial = (props) => {
  const {
    data,
    partial
  } = props;

  const { data: provider } = useAPI('provider');

  const DynamicPartial = React.lazy(async () => {
    let md = null;
    try {
      md = await import('../../partials/' + provider.provider_code + '/' + partial + '/index.js'); // Can't use a string literal because of Babel bug
    } catch(e) {
      md = await import('../../partials/Default');
    }

    console.log('PARTIAL NAME', partial);
    return md;
  });

  const item = get(data, ['item'], {});

  return (
    <div className="selected-item-container">
      <div className="header">
        <h3>{data.item.name}</h3>
      </div>
      <div className="content">
        <Suspense fallback={<span>Loading...</span>}>
          <DynamicPartial data={data} item={item} />
        </Suspense>
      </div>
    </div>
  );
};

LazyPartial.propTypes = propTypes;

export default LazyPartial;
