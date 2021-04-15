import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { useAPI } from '../../../api/useAPI';
import { getVpcFromPath, getRegionFromPath } from '../../../utils/Api';
import { getRawEndpoint } from '../../../api/paths';
import { Partial, PartialValue } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';
import NetworkInterfaces from './NetworkInterfaces';

import './style.scss';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Ec2Instance = props => {
  const { data } = props;

  const path = get(data, ['item', 'path'], '');
  const region = getRegionFromPath(path);
  const vpcId = getVpcFromPath(path);

  const { data: vpc, loading } = useAPI(
    getRawEndpoint(`services.ec2.regions.${region}.vpcs.${vpcId}.name`)
  );

  if (!data || loading) return null;

  const networkInterfaces = get(data, ['item', 'network_interfaces']);
  const metadata = get(data, ['item', 'metadata_options']);
  const userdata = get(data, ['item', 'user_data']) || '';
  const secrets = get(data, ['item', 'user_data_secrets']);

  if (!isEmpty(vpc)) {
    data.item.vpc = `${vpc} (${vpcId})`;
    data.item.region = region;
  }

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <div className="ec2-instances">
        <TabsMenu>
          <TabPane
            title="Network Interfaces"
            disabled={isEmpty(networkInterfaces)}
          >
            <NetworkInterfaces interfaces={networkInterfaces} />
          </TabPane>
          <TabPane
            title="Metadata Options"
            disabled={isEmpty(metadata)}
          >
            <div>
              <PartialValue
                label="Endpoint"
                value={metadata.HttpEndpoint}
                errorPath="metadata_options"
              />
              <PartialValue
                label="HTTP Tokens"
                value={metadata.HttpTokens}
                errorPath="metadata_options"
              />
            </div>
          </TabPane>
          <TabPane
            title="User Data"
            disabled={isEmpty(userdata)}
          >
            <div>
              <h5>Data</h5>
              {userdata.split('\n').map((data, i) => (
                <code key={i}>
                  {data}
                </code>
              ))}
              {!isEmpty(secrets) && (
                <div>
                  <h5 className="secrets-header">
                    <PartialValue
                      value="Potential Secrets"
                      errorPath="potential_secrets"
                    />
                  </h5>
                  <ul>
                    {Object.entries(secrets).map(([key, values], i) => (
                      <li key={i}>
                        {key}
                        <ul>
                          {values.map((value, i) => (
                            <li key={i}>
                              <code>{value}</code>
                            </li>
                          ))}
                        </ul>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </TabPane>
        </TabsMenu>
      </div>
    </Partial>
  );
};

Ec2Instance.propTypes = propTypes;

export default Ec2Instance;
