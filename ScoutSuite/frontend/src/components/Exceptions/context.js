import React, { useState, createContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';


const propTypes = {
  children: PropTypes.node.isRequired,
};

export const ExceptionsContext = createContext();

export const ExceptionsContextProvider = ({ children }) => {
  const [exceptions, setExceptions] = useState({});

  const addException = (service, finding, path) => {
    const newExceptions = [
      ...get(exceptions, [service, finding], []),
      path,
    ];
    
    setExceptions({
      ...exceptions,
      [service]: {
        [finding]: [
          ...newExceptions,
        ]
      }
    });
  };

  return (
    <ExceptionsContext.Provider value={{exceptions, addException}}>
      {children}
    </ExceptionsContext.Provider>
  );
};

ExceptionsContextProvider.propTypes = propTypes;
