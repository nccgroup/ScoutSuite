import React from 'react';

import BucketInformations from './BucketInformations';
import BucketPolicies from './BucketPolicies';
import { PropTypes } from 'prop-types';

const propTypes = {
  data: PropTypes.object.isRequired,
};

const Bucket = props => {
  const {
    data
  } = props;

  if (!data) return null;

  console.log('DATA', data);

  return (<>
    <div className="left-pane">
      <BucketInformations data={data} />
    </div>
    <BucketPolicies data={data} />
  </>);
};

Bucket.propTypes = propTypes;

export default Bucket;