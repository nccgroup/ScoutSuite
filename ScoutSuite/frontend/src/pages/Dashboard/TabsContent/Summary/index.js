import React from 'react';
import PropTypes from 'prop-types';
import sortBy from 'lodash/sortBy';
import { Button } from '@material-ui/core';
import GetAppOutlinedIcon from '@material-ui/icons/GetAppOutlined';

import ServiceCard from '../../../../components/ServiceCard';
import IssuesCharts from './IssuesCharts';
import { getFindingsEndpoint } from '../../../../api/paths';
import { get } from '../../../../api/api.js';
import { exportJSON, exportCSV } from '../../../../utils/Export';

import './style.scss';

const propTypes = {
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
};

const Summary = props => {
  const services = sortBy(props.services, [
    'issues.Critical',
    'issues.High',
    'issues.Medium',
    'issues.Low',
    'issues.Good',
  ]).reverse();

  const downloadSummary = async type => {
    const requests = props.services.map(service =>
      get(getFindingsEndpoint(service.id)),
    );
    const responses = await Promise.all(requests);
    const findings = []
      .concat(...responses)
      .map(({ service, description, flagged_items, level }) => ({
        Service: service,
        Description: description,
        'Affected resources': flagged_items,
        Level: level,
      }));

    if (type == 'json') {
      exportJSON(findings, 'summary');
    } else {
      exportCSV(findings, 'summary');
    }
  };

  return (
    <div className="dashboard-summary">
      <div className="overview">
        <div className="title-section">
          <h2>Overview</h2>
          <div>
            <Button
              className="download-btn"
              variant="outlined"
              size="small"
              onClick={() => downloadSummary('json')}
              startIcon={<GetAppOutlinedIcon />}
            >
              JSON
            </Button>
            <Button
              className="download-btn"
              variant="outlined"
              size="small"
              onClick={() => downloadSummary('csv')}
              startIcon={<GetAppOutlinedIcon />}
            >
              CSV
            </Button>
          </div>
        </div>

        <hr />
        <IssuesCharts services={services} />
      </div>

      <div className="services">
        <h2>Services</h2>
        <hr />
        <div className="cards">
          {services.map((service, i) => (
            <ServiceCard {...service} key={i} />
          ))}
        </div>
      </div>
    </div>
  );
};

Summary.propTypes = propTypes;

export default Summary;
