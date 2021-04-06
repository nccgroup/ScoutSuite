import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';
import isObject from 'lodash/isObject';
import isArray from 'lodash/isArray';

import { useAPI } from '../../../api/useAPI';
import { getVpcFromPath, getRegionFromPath } from '../../../utils/Api';
import { getRawEndpoint } from '../../../api/paths';
import { Partial, PartialValue } from '../../../components/Partial';
import { 
  partialDataShape,
  renderResourcesAsList,
  renderAwsTags,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ELBs = props => {
  const { data } = props;

  const path = get(data, ['item', 'path'], '');
  const region = getRegionFromPath(path);
  const vpcId = getVpcFromPath(path);

  const { data: vpc, loading } = useAPI(
    getRawEndpoint(`services.elb.regions.${region}.vpcs.${vpcId}`)
  );

  if (!data || loading) return null;

  if (!isEmpty(vpc)) {
    data.item.arn = vpc.arn;
    data.item.vpc = `${vpc.name} (${vpcId})`;
  }

  const listeners = get(data, ['item', 'listeners']);
  const attributes = get(data, ['item', 'attributes']);
  const securityGroups = get(data, ['item', 'security_groups'], {});
  const instances = get(data, ['item', 'instances'], []);
  const subnets = get(data, ['item', 'Subnets'], []);
  const tags = get(data, ['item', 'tags'], []);

  const renderAttributes = (attribute, path = []) => {
    const label = path.join('.');
    if (!isObject(attribute)) {
      return (
        <li key={label}>
          <PartialValue
            label={label}
            value={attribute}
            errorPath={`attributes.${label}`}
          />
        </li>
      );
    }
  
    if (isArray(attribute)) {
      return (
        <li key={label}>
          <PartialValue
            label={label}
            value={attribute}
            renderValue={value => value.map((x, i) => (
              <ul key={i}>
                {renderAttributes(x.Value, [x.Key])}
              </ul>
            ))}
          />
        </li>
      ); 
    }
  
    return Object.entries(attribute).map(([key, value]) => (
      renderAttributes(value, [...path, key])
    ));
  };

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <div>
        <TabsMenu>
          <TabPane title="Listeners">
            <ul>
              {Object.entries(listeners).map(([port, listener], i) => (
                <li key={i}>
                  <PartialValue
                    value={{
                      port,
                      ...listener,
                    }}
                    errorPath={`listeners.${port}`}
                    renderValue={value => value.SslPolicy ? (
                      <>
                        {`${value.port} (${value.Protocol}, `}
                        <PartialValue
                          value={value.SslPolicy}
                          errorPath={`listeners.${value.port}.SslPolicy`}
                        />
                        {')'}
                      </>
                    ) : (
                      `${value.port} (${value.Protocol})`
                    )}
                  />
                </li>
              ))}
            </ul>
          </TabPane>
          <TabPane title="Attributes">
            <ul>
              {renderAttributes(attributes)}
            </ul>
          </TabPane>
          <TabPane
            title="Security Groups"
            disabled={isEmpty(securityGroups)}
          >
            {renderResourcesAsList(securityGroups, 'GroupId')}
          </TabPane>
          <TabPane
            title="Destination"
            disabled={isEmpty(instances) && isEmpty(subnets)}
          >
            <div>
              {!isEmpty(instances) && (
                <>
                  <h5>Instances</h5>
                  {renderResourcesAsList(instances)}
                </>
              )}
              {!isEmpty(subnets) && (
                <>
                  <h5>Subnets</h5>
                  {renderResourcesAsList(subnets)}
                </>
              )}
            </div>
          </TabPane>
          {!isEmpty(tags) && (
            <TabPane title="Tags">
              {renderAwsTags(tags)}
            </TabPane>
          )}
        </TabsMenu>
      </div>
    </Partial>
  );
};

ELBs.propTypes = propTypes;

export default ELBs;
