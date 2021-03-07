
/**
 * Get a list of all the services
 */
export const getServices = () => '/services';

/**
 * Get findings for a service 
 * @param {*} service 
 */
export const getFindings = (service) => `services/${service}/findings`;

/**
 * Get external attach service link
 * @param {*} service 
 */
export const getExternalAttachService = (service) => `services/${service}/external-attack-surface`;

/**
 * Get password policy link
 * @param {*} service 
 */
export const getPasswordPolicy = (service) => `services/${service}/password-policy`;

/**
 * Get password policy link
 * @param {*} service 
 */
export const getPermissions = (service) => `services/${service}/permissions`;

/**
 * Get items from a findings
 * @param {*} service 
 * @param {*} finding 
 */
export const getItems = (service, finding) => `${getFindings(service)}/${finding}/items`;

/**
 * Get details for an item
 * @param {*} service 
 * @param {*} finding 
 * @param {*} id 
 * @param {*} path 
 */
export const getItem = (service, finding, id, path) => 
  `${getFindings(service)}/${finding}/items/${id}?path=${path}`;

export const getResource = (service) => `resources/${service}`;
