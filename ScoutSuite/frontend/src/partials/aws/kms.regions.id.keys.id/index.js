import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape } from '../../../utils/Partials';
import { Partial } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import Informations from './Informations';
import Policy from '../../../components/Partial/Policy';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const Keys = props => {
  const { data } = props;

  if (!data) return null;

  const aliases = get(data, ['item', 'aliases']);
  const policy = get(data, ['item', 'policy']);

  return (
    <Partial data={data}>
      <div className="left-pane">
        <Informations />
      </div>
      <TabsMenu>
        <TabPane 
          title="Aliases"
          disabled={isEmpty(aliases)}
        >
          <ul>
            {aliases.map((alias, i) => (
              <li key={i}>
                {alias.name}
              </li>
            ))}
          </ul>
        </TabPane>
        <TabPane 
          title="Key Policy"
          disabled={isEmpty(policy)}
        >
          <Policy policy={policy} />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

Keys.propTypes = propTypes;

export default Keys;
