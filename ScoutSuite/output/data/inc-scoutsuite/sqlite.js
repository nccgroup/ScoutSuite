// TODO: Change this for something less goofy
var querySeparator = '¤'
var reQuerySeparator = new RegExp('\\' + querySeparator + '+$')
var defaultPort = 8000

/**
 * Requests a list corresponding to the resource
 * @param {string} query            The suffix of the url
 * @param {number} pageSize         The amount of resources per page
 * @param {number} pageIndex        The index of the page [0, totalResources / pageSize - 1]
 * @returns {string}
 */
function requestDb (query, pageSize, pageIndex) {
  // TODO: Add the option of using a different port
  let url = 'http://127.0.0.1:' + defaultPort + '/api/'
  let response = ''

  if (arguments.length === 0) {
    url += 'summary'
  } else if (arguments.length === 1) {
    url += 'data?key=' + query
  } else if (arguments.length === 2) {
    url += 'full?key=' + query
  } else {
    url += 'page?pagesize=' + pageSize + '&page=' + pageIndex + '&key=' + query
  }

  $.ajax({
    type: 'GET',
    url: url,
    async: false,
    dataType: 'json',
    success: function (result) {
      response = result
    } })

  return response.data
}

/**
 * Inserts resource page info into runResults and wipes out the last resource page info from the memory
 * to make sure the memory never gets capped and crashes the browser, also updates page index of the resource
 * @param {number} pageSize         The amount of resources per page
 * @param {number} pageIndex        The index of the page [0, totalResources / pageSize - 1]
 * @param {string} service          The service targeted
 * @param {string} resource         The resource targeted
 */
function getResourcePageSqlite (pageIndex, pageSize, service, resource) {
  let resources = requestDb(createQuery('services', service, resource), pageSize, pageIndex)
  // Create an object where to save data and overwrite the current content
  runResults['services'][service][resource] = {}
  for (let item in resources) {
    runResults['services'][service][resource][item] =
      requestDb(createQuery('services', service, resource, item), null)
  }

  // Save the current page index to remember which page we have saved
  // Originally wanted to save that info under the precise resource, but the handlebar templates create slots for
  // each entry under resource, therefore there were 2 empty slots always added
  runResults['services'][service][resource + '_page_index'] = pageIndex
  runResults['services'][service][resource + '_page_size'] = pageSize
}

/**
 * Acts like getResourcePageSqlite but when we're using regions, made a separate function since the order of
 * the variables are different and it was getting confusing
 * @param {number} pageSize         The amount of resources per page
 * @param {number} pageIndex        The index of the page [0, totalResources / pageSize - 1]
 * @param {string} service          The service targeted
 * @param {string} region           The region targeted
 * @param {string} resource         The resource targeted
 */
function getResourcePageSqliteRegions (pageIndex, pageSize, service, region, resource) {
  let resources = requestDb(createQuery('services', service, 'regions', region, resource), pageSize, pageIndex)
  // Create a spot where to save data
  runResults['services'][service]['regions'][region][resource] = {}
  for (let item in resources) {
    Object.assign(runResults['services'][service]['regions'][region][resource], { [item]: 
      requestDb(createQuery('services', service, 'regions', region, resource, item), null) })
  }
  if (runResults['services'][service]['regions']['id'] === undefined) {
    runResults['services'][service]['regions']['id'] = {}
  }
  
  // Save the current page index to remember which page we have saved
  // Originally wanted to save that info under the precise resource, but the handlebar templates create slots for
  // each entry under resource, therefore there were 2 empty slots always added
  runResults['services'][service]['regions']['id'][resource + '_page_index'] = pageIndex
  runResults['services'][service]['regions']['id'][resource + '_page_size'] = pageSize
}

/**
 * Creates a query using the query separator to request information from the server
 * Scales with the number of params given
 * @returns {string}
 */
function createQuery () {
  let query = ''
  for (let i = 0; i < arguments.length; i++) {
    query += arguments[i] + querySeparator
  }
  query = query.replace(reQuerySeparator, '')
  return query
}
