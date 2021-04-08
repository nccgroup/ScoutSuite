
import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { 
  partialDataShape,
  valueOrNone,
  formatDate,
  convertBoolToEnable,
  renderAwsTags,
} from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const DynamoDbTables = props => {
  const { data } = props;

  if (!data) return null;

  const tags = get(data, ['item', 'tags']);

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="ID"
          valuePath="id"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="ARN"
          valuePath="arn"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Status"
          valuePath="table_status"
          renderValue={valueOrNone}
        />
        <PartialValue
          label="Creation Date"
          valuePath="creation_date_time"
          renderValue={formatDate}
        />
        <PartialValue
          label="Automatic Backups"
          valuePath="automatic_backups_enabled"
          renderValue={convertBoolToEnable}
        />
        <PartialValue
          label="Item Count"
          valuePath="item_count"
          renderValue={valueOrNone}
        />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane 
          title="Tags"
          disabled={isEmpty(tags)}
        >
          {renderAwsTags(tags)}
        </TabPane>
      </TabsMenu> 
    </Partial>
  );
};

DynamoDbTables.propTypes = propTypes;

export default DynamoDbTables;
