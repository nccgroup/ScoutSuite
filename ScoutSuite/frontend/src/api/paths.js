/**
 * Endpoint for the list of all the services
 */
export const getServicesEndpoint = () => 'services';

/**
 * Endpoint for ScoutSuite executions details
 */
export const getExecutionDetailsEndpoint = () => 'execution-details';

/**
 * Endpoint for the findings of a service
 * @param {*} service
 */
export const getFindingsEndpoint = (service) => `services/${service}/findings`;

/**
 * Endpoint for a service's External Attack Surface infos 
 * @param {*} service
 */
export const getServiceExternalAttackEndpoint = (service) =>
  `services/${service}/external_attack_surface`;

/**
 * Endpoint for a category's External Attack Surface infos 
 * @param {*} service
 */
export const getCategoryExternalAttackEndpoint = (category) =>
  `categories/${category}/external_attack_surface`;

/**
 * Endpoint for a service's Password Policy infos
 * @param {*} service
 */
export const getPasswordPolicyEndpoint = service =>
  `services/${service}/password_policy`;

/**
 * Endpoint for a service's Permissions infos
 * @param {*} service
 */
export const getPermissionsEndpoint = (service) => `services/${service}/permissions`;

/**
 * Endpoint for the items of a service's finding
 * @param {*} service
 * @param {*} finding
 */
export const getItemsEndpoint = (service, finding) =>
  `${getFindingsEndpoint(service)}/${finding}/items`;

/**
 * Endpoint for a finding's item infos
 * @param {*} service
 * @param {*} finding
 * @param {*} id
 * @param {*} path
 */
export const getItemEndpoint = (service, finding, id, path) =>
  `${getFindingsEndpoint(service)}/${finding}/items/${id}?path=${path}`;

/**
 * Endpoint for the items of a service's resource
 * @param {*} service 
 * @param {*} resource 
 * @returns 
 */
export const getResourcesEndpoint = (service, resource) =>
  `services/${service}/resources/${resource}`;

/**
 * Enpoint for getting a resource's infos
 * @param {*} service 
 * @param {*} resource 
 * @param {*} id 
 * @returns 
 */
export const getResourceEndpoint = (service, resource, id) =>
  `services/${service}/resources/${resource}/${id}`;

export const getResourceFilterAttributeEndpoint = (service, resource, attribute) =>
  `services/${service}/resources/${resource}/options/${attribute}`;

export const getFindingFilterAttributeEndpoint = (service, finding, attribute) =>
  `services/${service}/findings/${finding}/items/options/${attribute}`;  

/**
 * Endpoint for raw access to the JSON report
 * @param {*} raw 
 * @returns 
 */
export const getRawEndpoint = (raw) => `raw/${raw.replace(/\./g, '/')}`;
