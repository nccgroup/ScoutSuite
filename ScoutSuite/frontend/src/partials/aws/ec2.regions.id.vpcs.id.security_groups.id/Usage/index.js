import React, { useContext }  from 'react';
import CheckCircleOutlineOutlinedIcon from '@material-ui/icons/CheckCircleOutlineOutlined';
import get from 'lodash/get';
import isArray from 'lodash/isArray';

import { PartialContext, PartialPathContext } from '../../../../components/Partial/context';
import { makeTitle } from '../../../../utils/Partials';

import './style.scss';


const Usage = () => {
  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const value = get(ctx.item, basePath);

  // TODO: `resource.name` should be rendered as a link.
  const renderResourcesList = resources => {
    if (isArray(resources)) {
      return resources.map(resource => (
        <li key={resource.id}>
          {resource.name} 
        </li>
      ));
    } else {
      return Object.entries(resources).map(([name, list], i) => (
        <li key={i}>
          {makeTitle(name)}
          <ul>
            {renderResourcesList(list)}
          </ul>
        </li>
      ));
    }
  };

  return (
    <div className="security-group-usage">
      {value && (
        <ul>
          {Object.entries(value).map(([service, { resource_type }]) => (
            Object.entries(resource_type).map(([type, resources], i) => (
              <div key={i}>
                <li>
                  <h4 className="resource-title">
                    {`${makeTitle(service)} ${makeTitle(type)}`}
                  </h4>
                </li>
                <ul>
                  {renderResourcesList(resources)}
                </ul> 
              </div>
            ))
          ))}
        </ul>
      )}
      {!value && (
        <span className="not-in-use">
          <CheckCircleOutlineOutlinedIcon fontSize="inherit" /> This security group is not in use.
        </span>
      )}
    </div>
  );
};

export default Usage;
