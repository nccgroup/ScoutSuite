import { getFindings, getPasswordPolicy, getExternalAttachService, getPermissions } from '../../api/paths';

export const TAB_NAMES = {
  SUMMARY: 'Summary',
  EXECUTION_DETAILS: 'Execution Details',
  RESOURCES_DETAILS: 'Resources Details',
};

export const getDashboardName = (dashboard) => {
  const names = {
    findings: 'Findings',
    'external attack surface': 'External Attack Surface',
    password_policy: 'Password Policy',
    permissions: 'Permissions',
  };

  return names[dashboard];
};

export const getDashboardLink = (dashboard, service) => {
  const links = {
    findings: getFindings(service),
    'external attack surface': getExternalAttachService(service),
    password_policy: getPasswordPolicy(service),
    permissions: getPermissions(service),
  };

  return links[dashboard];
};
