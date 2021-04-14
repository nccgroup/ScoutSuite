import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../../../api/useAPI';
import { getRawEndpoint } from '../../../api/paths';
import { getRegionFromPath, getVpcFromPath } from '../../../utils/Api';
import { Partial, PartialValue } from '../../../components/Partial';
import { 
  partialDataShape,
  renderList,
  renderSecurityGroupLink,
  renderAwsTags,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ElbV2 = props => {
  const { data } = props;

  const path = get(data, ['item', 'path'], '');
  const region = getRegionFromPath(path);
  const vpcId = getVpcFromPath(path);

  const { data: vpc, loading } = useAPI(
    getRawEndpoint(`services.elbv2.regions.${region}.vpcs.${vpcId}.name`)
  );

  if (!data || loading) return null;

  if (!isEmpty(vpc)) {
    data.item.vpc = `${vpc} (${vpcId})`;
  }

  const listeners = get(data, ['item', 'listeners'], {});
  const attributes = get(data, ['item', 'attributes'], []);
  const securityGroups = get(data, ['item', 'security_groups'], {});
  const tags = get(data, ['item', 'tags'], []);
  const isNetwork = get(data, ['item', 'isNetwork']);

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
                          inline
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
            <div>
              {attributes.map(({ Key, Value }, i) => (
                <PartialValue 
                  key={i}
                  label={Key}
                  value={Value}
                  errorPath={`attributes.${i}`}
                />
              ))}
            </div>
          </TabPane>
          {!isNetwork && (
            <TabPane
              title="Security Groups"
              disabled={isEmpty(securityGroups)}
            >
              {renderList(securityGroups, '', renderSecurityGroupLink)}
            </TabPane>
          )}
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

ElbV2.propTypes = propTypes;

export default ElbV2;
