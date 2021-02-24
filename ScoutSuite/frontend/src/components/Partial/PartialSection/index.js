import React, { useContext } from 'react';
import { PropTypes } from 'prop-types';

import {PartialPathContext} from '../context';

const propTypes = {
  path: PropTypes.string.isRequired,
  children: PropTypes.element.isRequired,
};

const PartialSection = (props) => {
  let { path, children } = props;

  let basePath = useContext(PartialPathContext);

  if (path.length > 0) path += '.';

  return (
    <PartialPathContext.Provider value={basePath + path}>
      {children}
    </PartialPathContext.Provider>
  );
};

PartialSection.propTypes = propTypes;

export default PartialSection;
