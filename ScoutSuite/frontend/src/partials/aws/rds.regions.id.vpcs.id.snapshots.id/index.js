
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  formatDate,
  convertBoolToEnable, 
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Snapshots = props => {
  const { data } = props;

  if (!data) return null;

  const attributes = get(data, ['item', 'attributes']);
  const isCluster = get(data, ['item', 'is_cluster']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        {isCluster ? (
          <PartialValue
            label="DB Cluster"
            valuePath="DBClusterIdentifier"
          />
        ) : (
          <PartialValue
            // TODO: Link to resource
            label="RDS Instance"
            valuePath="DBInstanceIdentifier"
          />
        )}
        <PartialValue
          label="Cluster Snapshot"
          valuePath="is_cluster"
        />
        <PartialValue
          label="Creation Time"
          valuePath="SnapshotCreateTime"
          renderValue={formatDate}
        />
        <PartialValue
          label="Encryption"
          valuePath="Encrypted"
          errorPath="snapshot-not-encrypted"
          renderValue={convertBoolToEnable}
        />
        {!isCluster && (
          <PartialValue
            label="Option Group"
            valuePath="OptionGroupName"
          />
        )}
      </InformationsWrapper>

      <TabsMenu>
        <TabPane 
          title="Attributes"
          disabled={isEmpty(attributes)}
        >
          <ul>
            {attributes.map((attribute, i) => (
              <li key={i}>
                <PartialValue
                  label={attribute.AttributeName}
                  value={attribute.AttributeValues}
                  errorPath={`attributes.${i}`}
                  renderValue={values => (
                    <ul>
                      {!isEmpty(values) ? (
                        values.map((value, i) => (
                          <li key={i}>
                            {value}
                          </li>
                        ))
                      ) : (
                        <li>No value</li>
                      )}
                    </ul>
                  )}
                />
              </li>
            ))}
          </ul>
        </TabPane>
      </TabsMenu> 
    </Partial>
  );
};

Snapshots.propTypes = propTypes;

export default Snapshots;
