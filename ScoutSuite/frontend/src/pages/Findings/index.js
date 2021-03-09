import { useParams } from '@reach/router';
import React from 'react';
import CheckCircleOutlineOutlinedIcon from '@material-ui/icons/CheckCircleOutlineOutlined';

// import PropTypes from 'prop-types';

import { useAPI } from '../../api/useAPI';
import { getFindings } from '../../api/paths';
import { sortBySeverity } from '../../utils/Severity/sort';
import Table from '../../components/Table';
import Name from './formatters/Name';
import Description from './formatters/Description/index';
import Severity from './formatters/Severity/index';
import Breadcrumb from '../../components/Breadcrumb/index';

import './style.scss';

const propTypes = {};

const Findings = () => {
  const params = useParams();
  const { data: findings, loading } = useAPI(getFindings(params.service));

  if (loading) return null;

  const columns = [
    { name: 'Severity', key: 'severity', sortInverted: true },
    { name: 'Name', key: 'name' },
    { name: 'Flagged Items', key: 'flagged', sortInverted: true },
    { name: 'Description', key: 'description' },
  ];

  const data = findings.map((item) => ({
    id: item.name,
    severity: item.flagged_items === 0 ? 'success' : item.level,
    name: item.description,
    flagged: `${item.flagged_items}/${item.checked_items}`,
    description: item.rationale,
    references: item.references,
    remediation: item.remediation,
    flagged_items: item.flagged_items,
  }));

  const initialState = {
    sortBy: [
      {
        id: 'severity',
        desc: false,
      },
    ],
    pageSize: 25,
  };

  const formatters = {
    name: Name,
    description: Description,
    severity: Severity,
  };

  const sortBy = {
    severity: sortBySeverity,
  };

  if (findings.length === 0) {
    return (
      <>
        <Breadcrumb />
        <div className="findings">
          <div className="table-card no-items">
            <CheckCircleOutlineOutlinedIcon /> <b>All good!</b> No findings for this service.
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Breadcrumb />
      <div className="findings">
        <div className="table-card">
          <Table
            columns={columns}
            data={data}
            initialState={initialState}
            formatters={formatters}
            sortBy={sortBy}
          />
        </div>
      </div>
    </>
  );
};

Findings.propTypes = propTypes;

export default Findings;
