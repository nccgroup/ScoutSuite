import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';

import { Partial } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import DetailedValue from '../../../components/DetailedValue';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ELBs = props => {
  const { data } = props;

  if (!data) return null;

  const protocols = get(data, ['item', 'protocols'], {});
  const options = get(data, ['item', 'options'], {});
  const ciphers = get(data, ['item', 'ciphers'], {});
  const attributes = get(data, ['item', 'PolicyAttributeDescriptions'], []);
  const isSslPolicy = get(data, ['item', 'PolicyTypeName']) === 'SSLNegotiationPolicyType';

  const renderEntries = entry => (
    <div>
      {entry.map(([key, value], i) => (
        <DetailedValue
          key={i}
          label={key}
          value={value}
        />
      ))}
    </div>
  );

  return (
    <Partial data={data}>
      {isSslPolicy ? (
        <TabsMenu>
          <TabPane title="Protocols">
            {renderEntries(Object.entries(protocols))}
          </TabPane>
          <TabPane title="Options">
            {renderEntries(Object.entries(options))}
          </TabPane>
          <TabPane title="Ciphers">
            {renderEntries(Object.entries(ciphers)
              .filter(([, value]) => value === 'true')
            )}
          </TabPane>
        </TabsMenu>
      ) : (
        <TabsMenu>
          <TabPane title="Attributes">
            {renderEntries(attributes.map(x => [
              x.AttributeName, x.AttributeValue
            ]))}
          </TabPane>
        </TabsMenu>
      )}
    </Partial>
  );
};

ELBs.propTypes = propTypes;

export default ELBs;
