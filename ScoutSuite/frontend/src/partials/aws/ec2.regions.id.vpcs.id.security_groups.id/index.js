import React from 'react';
import { PropTypes } from 'prop-types';

import { Partial, PartialSection } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import Informations from './Informations';
import RulesList from './RulesList';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Bucket = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div className="left-pane">
        <Informations />
      </div>

      <TabsMenu>
        <TabPane title="Egress Rules">
          <PartialSection path="rules.egress">
            <RulesList />
          </PartialSection>
        </TabPane>
        <TabPane title="Ingress Rules">
          <PartialSection path="rules.ingress">
            <RulesList />
          </PartialSection>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Bucket.propTypes = propTypes;

export default Bucket;
