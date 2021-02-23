import React from 'react';

const defaultValues = {
  path_to_issue: [],
  item: {}
};

export const PartialContext = React.createContext(defaultValues);
export const PartialPathContext = React.createContext('');