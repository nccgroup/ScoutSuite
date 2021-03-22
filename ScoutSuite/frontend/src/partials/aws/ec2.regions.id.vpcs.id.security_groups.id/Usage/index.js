import React, { useContext }  from 'react';
import CheckCircleOutlineOutlinedIcon from '@material-ui/icons/CheckCircleOutlineOutlined';
import get from 'lodash/get';
import isArray from 'lodash/isArray';

import { 
  PartialContext, 
  PartialPathContext 
} from '../../../../components/Partial/context';
import { 
  makeTitle,
  renderResourcesAsList,
} from '../../../../utils/Partials';
import WarningMessage from '../../../../components/WarningMessage';

import './style.scss';


const Usage = () => {
  const ctx = useContext(PartialContext);
  const basePath = useContext(PartialPathContext);
  const value = get(ctx.item, basePath);

  const renderUsageList = resources => 
    isArray(resources) 
      ? renderResourcesAsList(resources, 'name')
      : (
        Object.entries(resources).map(([name, list], i) => (
          <ul key={i}>
            <li>
              {makeTitle(name)}
              {renderUsageList(list)}
            </li>
          </ul>
        ))
      );

  return (
    <div className="security-group-usage">
      {value && (
        <ul>
          {Object.entries(value).map(([service, { resource_type }]) => (
            Object.entries(resource_type).map(([type, resources], i) => (
              <div key={i}>
                <li>
                  <h5 className="resource-title">
                    {`${makeTitle(service)} ${makeTitle(type)}`}
                  </h5>
                </li>
                {renderUsageList(resources)}
              </div>
            ))
          ))}
        </ul>
      )}
      {!value && (
        <WarningMessage
          message="This security group is not in use."
          icon={<CheckCircleOutlineOutlinedIcon fontSize="inherit" />}
        />
      )}
    </div>
  );
};

export default Usage;
