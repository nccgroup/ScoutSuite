import React from 'react';

import { Partial } from '../../../components/Partial';
import BucketInformations from './BucketInformations';
import BucketPolicies from './BucketPolicies';
import { PropTypes } from 'prop-types';


const propTypes = {
  data: PropTypes.objectOf({
    item: PropTypes.object.isRequired,
    path_to_issues: PropTypes.arrayOf(PropTypes.string).isRequired,
  }).isRequired,
};

const Bucket = props => {
  const {
    data
  } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="left-pane">
        <BucketInformations />
      </div>
      <BucketPolicies />
    </Partial>
  );
};

Bucket.propTypes = propTypes;

export default Bucket;
