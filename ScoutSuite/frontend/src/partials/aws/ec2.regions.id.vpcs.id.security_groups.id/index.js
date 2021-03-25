import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialSection } from '../../../components/Partial';
import { partialDataShape } from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import Informations from './Informations';
import RulesList from './RulesList';
import Usage from './Usage';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Ec2SecurityGroups = props => {
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
        <TabPane title="Usage">
          <PartialSection path="used_by">
            <Usage />
          </PartialSection>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Ec2SecurityGroups.propTypes = propTypes;

export default Ec2SecurityGroups;
