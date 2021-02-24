import React, { Suspense } from 'react';
import PropTypes from 'prop-types';
import { useParams } from '@reach/router';

import { useAPI } from '../../../api/useAPI';
import { getItem } from '../../../api/paths';

import './style.scss';

const propTypes = {
  title: PropTypes.string.isRequired,
};

const SelectedItemContainer = props => {
  const {
    title
  } = props;

  const path = (new URL(document.location)).searchParams.get('path');
  const params = useParams();
  const { data: finding, loading: loading1 } = useAPI(`raw/services/${params.service}/findings/${params.finding}`);
  const { data, loading: loading2 }= useAPI(getItem(params.service, params.finding, params.item, path));

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

  return (
    <div className="selected-item-container">
      <div className="header">
        <h3>{title}</h3>
      </div>
      <div className="content">
        <Suspense fallback={() => <span>Loading...</span>}>
          <DynamicPartial data={data} />
        </Suspense>
      </div>
    </div>
  );
};

SelectedItemContainer.propTypes = propTypes;

export default SelectedItemContainer;
