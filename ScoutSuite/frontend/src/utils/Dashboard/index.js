import { getFindingsEndpoint, getPasswordPolicyEndpoint, getExternalAttachServiceEndpoint, getPermissionsEndpoint } from '../../api/paths';

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
    statistics: 'Statistics'
  };

  return names[dashboard];
};

export const getDashboardLink = (dashboard, service) => {
  const links = {
    findings: getFindingsEndpoint(service),
    'external attack surface': getExternalAttachServiceEndpoint(service),
    password_policy: getPasswordPolicyEndpoint(service),
    permissions: getPermissionsEndpoint(service),
  };

  return links[dashboard];
};
