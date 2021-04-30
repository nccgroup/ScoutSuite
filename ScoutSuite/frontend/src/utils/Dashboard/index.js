import React from 'react';
import ReportProblemOutlinedIcon from '@material-ui/icons/ReportProblemOutlined';
import ErrorOutlineOutlinedIcon from '@material-ui/icons/ErrorOutlineOutlined';
import CheckCircleOutlineOutlinedIcon from '@material-ui/icons/CheckCircleOutlineOutlined';

import { 
  getFindingsEndpoint, 
  getPasswordPolicyEndpoint, 
  getServiceExternalAttackEndpoint,
  getCategoryExternalAttackEndpoint,
  getPermissionsEndpoint 
} from '../../api/paths';


export const TAB_NAMES = {
  SUMMARY: 'Summary',
  EXECUTION_DETAILS: 'Execution Details',
  RESOURCES_DETAILS: 'Resources Details',
};

export const SEVERITIES = {
  critical: {
    text: 'Critical',
    icon: <ReportProblemOutlinedIcon fontSize="inherit" />
  },
  danger: {
    text: 'High',
    icon: <ReportProblemOutlinedIcon fontSize="inherit" />
  },
  high: {
    text: 'High',
    icon: <ReportProblemOutlinedIcon fontSize="inherit" />
  },
  warning: {
    text: 'Medium',
    icon: <ErrorOutlineOutlinedIcon fontSize="inherit" />
  },
  medium: {
    text: 'Medium',
    icon: <ErrorOutlineOutlinedIcon fontSize="inherit" />
  },
  low: {
    text: 'Low',
    icon: <ErrorOutlineOutlinedIcon fontSize="inherit" />
  },
  info: {
    text: 'Info',
    icon: <ReportProblemOutlinedIcon fontSize="inherit" />
  },
  success: {
    text: 'Good',
    icon: <CheckCircleOutlineOutlinedIcon fontSize="inherit" />
  },
};

export const getDashboardName = (dashboard) => {
  const names = {
    findings: 'Findings',
    'external attack surface': 'External Attack Surface',
    password_policy: 'Password Policy',
    permissions: 'Permissions',
    statistics: 'Statistics'
  };

  return names[dashboard];
};

export const getServiceDashboardLink = (dashboard, service) => {
  const links = {
    findings: getFindingsEndpoint(service),
    'external attack surface': getServiceExternalAttackEndpoint(service),
    password_policy: getPasswordPolicyEndpoint(service),
    permissions: getPermissionsEndpoint(service),
  };

  return links[dashboard];
};

export const getCategoryDashboardLink = (dashboard, category) => {
  const links = {
    'external attack surface': getCategoryExternalAttackEndpoint(category),
  };

  return links[dashboard];
};
