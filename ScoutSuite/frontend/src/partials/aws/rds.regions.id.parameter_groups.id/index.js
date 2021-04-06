
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';
import Tooltip from '@material-ui/core/Tooltip';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';

import { partialDataShape } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';

import './style.scss';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ParameterGroups = props => {
  const { data } = props;

  if (!data) return null;

  const parameters = get(data, ['item', 'parameters']);

  const parameterLabel = (name, description) => (
    <span className="parameter-label">
      <Tooltip 
        title={description}
        placement="top"
        arrow
      > 
        <InfoOutlinedIcon 
          fontSize="inherit"
        />
      </Tooltip>
      {`${name}: `}
    </span>
  );

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Group Family"
          valuePath="DBParameterGroupFamily"
        />
        <PartialValue
          label="Descripition"
          valuePath="Description"
        />
        <PartialValue
          label="ARN"
          valuePath="arn"
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane 
          title="Parameters"
          disabled={isEmpty(parameters)}
        >
          <div className="rds-parameters">
            {Object.entries(parameters)
              .filter(([, value]) => value.ParameterValue)
              .map(([name, parameter], i) => (
                <PartialValue
                  key={i}
                  label={parameterLabel(name, parameter.Description)}
                  value={parameter.ParameterValue || ''}
                  errorPath={name}
                />
              ))
            }
          </div>
        </TabPane>
      </TabsMenu> 
    </Partial>
  );
};

ParameterGroups.propTypes = propTypes;

export default ParameterGroups;
