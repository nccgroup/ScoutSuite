var querySeparator = '¤'
var reQuerySeparator = new RegExp('\\' + querySeparator + '+$')
var defaultPort = 8000

/**
 * Requests a list corresponding to the resource
 * @param {string} query              The suffix of the url
 * @returns {string}
 */
function requestDb (query, pageSize, pageIndex) {
  let url = 'http://127.0.0.1:' + defaultPort + '/api/'
  let response = ''

  if (arguments.length === 1) {
    url += 'data?key=' + query
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

  if (response.data === null || response.data === undefined) {
    console.log('This query returned an empty response:  ' + query)
  }

  return response.data
}

/**
 * Returns all the data from the server, excepted for resources
 * @returns {object}
 */
function getScoutsuiteResultsSqlite () {
  // The layers are named here in this fashion, these names don't always make sense depending in which
  // nested dict you are though since our data structure is not consistent :
  // paths(0) --> groups(1) --> services(2) --> counters(3) --> resources(4) --> items(5)
  let paths = requestDb('').keys
  runResults = {}
  for (let i in paths) { // Layer 0
    let list = {}
    let groups = requestDb(paths[i]) 
    if (groups.keys) {
      groups = groups.keys
    } else {
      runResults[paths[i]] = groups
      continue
    }
    for (let group in groups) { // Layer 1    
      list[groups[group]] = requestDb(createQuery(paths[i], groups[group]))
      let services = list[groups[group]].keys
      if (services) {        
        for (let service in services) { // Layer 2
          let counters = requestDb(createQuery(paths[i], groups[group], services[service]))
          if (!counters.keys) {
            list[groups[group]][services[service]] = counters
          } else {
            counters = counters.keys
            list[groups[group]][services[service]] = { [null]: null }
          }
          // The only elements for which we do not want to fetch everything are the resources which
          // are not filters or findings since they will scale with the environment's size
          if (paths[i] === 'services' && [services[service]] != 'filters' && [services[service]] != 'findings') {
            continue
          }
          for (let counter in counters) { // Layer 3
            list[groups[group]][services[service]][counters[counter]] =
              requestDb(createQuery(paths[i], groups[group], services[service], counters[counter]))
            if (!list[groups[group]][services[service]][counters[counter]]) { continue }
            let resources = list[groups[group]][services[service]][counters[counter]].keys
            for (let resource in resources) { // Layer 4
              list[groups[group]][services[service]][counters[counter]][resources[resource]] = requestDb(
                createQuery(paths[i], groups[group], services[service], counters[counter], resources[resource]))
              let items = list[groups[group]][services[service]][counters[counter]][resources[resource]].keys
              for (let item in items) { // Layer 5          
                list[groups[group]][services[service]][counters[counter]][resources[resource]][items[item]] =
                requestDb(createQuery(paths[i], groups[group], services[service], counters[counter], resources[resource],
                  items[item]))
                delete list[groups[group]][services[service]][counters[counter]].type
                delete list[groups[group]][services[service]][counters[counter]].keys
              }
            }
          }
          delete list[groups[group]][services[service]].null
        }
        delete list[groups[group]].type
        delete list[groups[group]].keys
      }
    }
    runResults[paths[i]] = list
  }
  return runResults
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
  // Delete the current content
  runResults['services'][service][resource] = null
  // Create a spot where to save data
  runResults['services'][service][resource] = { [null]: null }
  for (let item in resources) {
    let properties = resources[item].keys
    runResults['services'][service][resource][item] = { [null]: null }
    for (let property in properties) {
      runResults['services'][service][resource][item][properties[property]] =
      requestDb(createQuery('services', service, resource, item, properties[property]))
    }
    delete runResults['services'][service][resource][item].null
  }
  // Save the current page index to remember which page we have saved
  // Originally wanted to save that info under the precise resource, but the handlebar templates create slots for
  // each entry under resource, therefore there were 2 empty slots always added
  runResults['services'][service][resource + '_page_index'] = pageIndex
  // Save the current page size to remember the size of the saved page
  runResults['services'][service][resource + '_page_size'] = pageSize
  delete runResults['services'][service][resource].null
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
