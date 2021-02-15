import { useParams } from '@reach/router';
import React from 'react';

// import PropTypes from 'prop-types';

import { useAPI } from '../../api/useAPI';
import { sortBySeverity } from '../../utils/Severity/sort';
import Layout from '../../layout';
import Table from '../../components/Table';
import Name from './formatters/Name';
import Description from './formatters/Description/index';
import Severity from './formatters/Severity/index';


import './style.scss';

const propTypes = {};

const Findings = () => {
  const params = useParams();
  const { data: results } = useAPI(`services.${params.service}.findings`);

  const findings = Object.entries(results);

  const columns = [
    { name: 'Severity', key: 'severity' },
    { name: 'Name', key: 'name' },
    { name: 'Flagged Items', key: 'flagged' },
    { name: 'Description', key: 'description' }
  ];

  const data = findings.map(([key, item]) => ({
    id: key,
    severity: item.flagged_items === 0 ? 'success' : item.level,
    name: item.description,
    flagged: `${item.flagged_items}/${item.checked_items}`,
    description: item.rationale
  }));

  const initialState = {
    sortBy: [{
      id: 'severity', desc: true
    }]
  };

  const formatters = {
    name: Name,
    description: Description,
    severity: Severity
  };

  const sortBy = {
    severity: sortBySeverity
  };

  return (
    <Layout>
      <div className="findings">
        <div className="table-card">
          <Table
            columns={columns}
            data={data}
            initialState={initialState}
            formatters={formatters}
            sortBy={sortBy} />
        </div>
      </div>
    </Layout>
  );
};

Findings.propTypes = propTypes;

export default Findings;
