import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape } from '../../../utils/Partials';
import { Partial, PartialSection } from '../../../components/Partial';
import Policy from '../../../components/Partial/Policy';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import Informations from './Informations';
import AccessControlList from './AccessControlList';
import PoliciesAccessTable from './PoliciesAccessTable';
import Keys from './Keys';

import './style.scss';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Bucket = props => {
  const { data } = props;

  if (!data) return null;

  const policy = get(data, ['item', 'policy']);
  const keys = get(data, ['item', 'keys']);

  return (
    <Partial data={data}>
      <div className="left-pane">
        <Informations />
      </div>

      <TabsMenu className="bucket-policies">
        {!isEmpty(policy) && (
          <TabPane title="Bucket Policy">
            <Policy 
              policy={policy}
            />
          </TabPane>
        )}
        <TabPane title="Bucket ACLs">
          <PartialSection path="grantees">
            <AccessControlList />
          </PartialSection>
        </TabPane>
        <TabPane title="Groups">
          <PartialSection path="groups">
            <PoliciesAccessTable columnName="Groups name"/>
          </PartialSection>
        </TabPane>
        <TabPane title="Roles">
          <PartialSection path="roles">
            <PoliciesAccessTable columnName="Roles name"/>
          </PartialSection>
        </TabPane>
        <TabPane title="Users">
          <PartialSection path="users">
            <PoliciesAccessTable columnName="Users name"/>
          </PartialSection>
        </TabPane>
        {!isEmpty(keys) && (
          <TabPane title="Keys">
            <PartialSection path="keys">
              <Keys />
            </PartialSection>
          </TabPane>
        )}
      </TabsMenu>
    </Partial>
  );
};

Bucket.propTypes = propTypes;

export default Bucket;
