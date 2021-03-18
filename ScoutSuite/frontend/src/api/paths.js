/**
 * Get a list of all the services
 */
export const getServicesEndpoint = () => '/services';

/**
 * Get findings for a service
 * @param {*} service
 */
export const getFindingsEndpoint = (service) => `services/${service}/findings`;

/**
 * Get external attach service link
 * @param {*} service
 */
export const getExternalAttachServiceEndpoint = (service) =>
  `services/${service}/external-attack-surface`;

/**
 * Get password policy link
 * @param {*} service
 */
export const getPasswordPolicyEndpoint = (service) =>
  `services/${service}/password-policy`;

/**
 * Get password policy link
 * @param {*} service
 */
export const getPermissionsEndpoint = (service) => `services/${service}/permissions`;

/**
 * Get items from a findings
 * @param {*} service
 * @param {*} finding
 */
export const getItemsEndpoint = (service, finding) =>
  `${getFindingsEndpoint(service)}/${finding}/items`;

/**
 * Get details for an item
 * @param {*} service
 * @param {*} finding
 * @param {*} id
 * @param {*} path
 */
export const getItemEndpoint = (service, finding, id, path) =>
  `${getFindingsEndpoint(service)}/${finding}/items/${id}?path=${path}`;

/**
 * Get a list of resources
 * @param {*} service 
 * @param {*} resource 
 * @returns 
 */
export const getResourcesEndpoint = (service, resource) =>
  `/services/${service}/resources/${resource}`;

/**
 * Enpoint for getting a resource
 * @param {*} service 
 * @param {*} resource 
 * @param {*} id 
 * @returns 
 */
export const getResourceEndpoint = (service, resource, id) =>
  `/services/${service}/resources/${resource}/${id}`;
