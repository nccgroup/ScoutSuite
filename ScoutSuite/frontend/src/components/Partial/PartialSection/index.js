import React, { useContext } from 'react';
import PropTypes from 'prop-types';

import { PartialPathContext } from '../context';
import { concatPaths } from '../../../utils/Partials';

const propTypes = {
  path: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
};

const PartialSection = (props) => {
  const { path, children } = props;

  const basePath = useContext(PartialPathContext);

  return (
    <PartialPathContext.Provider value={concatPaths(basePath, path)}>
      {children}
    </PartialPathContext.Provider>
  );
};

PartialSection.propTypes = propTypes;

export default PartialSection;
