import React, { useState, createContext } from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';
import size from 'lodash/size';
import omit from 'lodash/omit';


const propTypes = {
  children: PropTypes.node.isRequired,
};

export const ExceptionsContext = createContext();

export const ExceptionsContextProvider = ({ children }) => {
  const [exceptions, setExceptions] = useState({});

  const addException = (service, finding, path) => {
    const newFindings = [
      ...get(exceptions, [service, finding], []),
      path,
    ];
    
    setExceptions({
      ...exceptions,
      [service]: {
        ...get(exceptions, service, {}),
        [finding]: [
          ...newFindings,
        ]
      }
    });
  };

  const removeException = (service, finding, path) => {
    const newFindings = get(exceptions, [service, finding], [])
      .filter(exceptionPath => exceptionPath != path);

    let newExceptions = {
      ...exceptions,
      [service]: {
        ...get(exceptions, service, {}),
        [finding]: newFindings,
      }
    };

    if (isEmpty(newFindings)) {
      if (size(newExceptions[service]) === 1) {
        newExceptions = omit(newExceptions, service);
      } else {
        newExceptions[service] = omit(newExceptions[service], finding);
      }
    }
    
    setExceptions(newExceptions);
  };

  return (
    <ExceptionsContext.Provider value={{exceptions, addException, removeException}}>
      {children}
    </ExceptionsContext.Provider>
  );
};

ExceptionsContextProvider.propTypes = propTypes;
