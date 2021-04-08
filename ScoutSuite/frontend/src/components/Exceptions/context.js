import React, { useState, createContext } from 'react';
import merge from 'lodash/merge';
import { PropTypes } from 'prop-types';

const propTypes = {
  children: PropTypes.node.isRequired,
};

export const ExceptionsContext = createContext();

export const ExceptionsContextProvider = ({ children }) => {
  const [exceptions, setExceptions] = useState({});

  const addException = (service, finding, path) => {
    const newException = {
      [service]: {
        [finding]: [path],
      },
    };
    setExceptions(merge(newException, exceptions));
  };

  return (
    <ExceptionsContext.Provider value={{exceptions, addException}}>
      {children}
    </ExceptionsContext.Provider>
  );
};

ExceptionsContextProvider.propTypes = propTypes;
