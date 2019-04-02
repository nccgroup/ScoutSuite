var querySeparator = '¤'
var reQuerySeparator = new RegExp('\\' + querySeparator + '+$')
var defaultPort = 8000

/**
 * Requests a list corresponding to the resource
 * @param {string} query
 */
function requestDb (query, pageSize, pageIndex) {
  let url = 'http://127.0.0.1:' + defaultPort + '/api/'
  let response =''
  
  if (arguments.length === 1) {
    url += 'data?key=' + query
  } else {
    url += 'page?pagesize=' + pageSize + '&page=' + pageIndex + '&key=' + query
  }

  $.ajax({
   type: 'GET',
   url: url,
   async: false,
   success: function(result) {
    response = result;
  }})

  if (response.data === null || response.data === undefined) {
    console.log('This query returned an empty response:  ' + query)
  }

  return response.data
}

// TODO: change for something that does not throw XML errors
/**
 * Requests a page of resources
 * @param query           : The type of resource requested
 * @param pageSize        : The amount of resources per page
 * @param pageIndex       : The index of the page [0, totalResources / pageSize - 1]
 */
function requestDbPage (query, pageSize, pageIndex) {
  let response =''

  $.ajax({
   type: 'GET',
   url: 'http://127.0.0.1:8000/api/page?pagesize=' + pageSize + '&page=' + pageIndex + '&key=' + query,
   async: false,
   success: function(result) {
    response = result;
  }})

  if (response.data === null || response.data === undefined) {
    console.log('This query returned an empty response:  ' + query)
  }

  return response.data
}

/** 
 * Returns all the data from the server, excepted for resources
*/ 
function getScoutsuiteResultsSqlite () {
  // The layers are named here in this fashion, these names don't always make sense depending in which
  // nested dict you are though since our data structure is not consistent :
  // paths(0) --> groups(1) --> services(2) --> counters(3) --> resources(4) --> items(5)
  let paths = requestDb('').keys
  run_results = {}
  for (let i in paths) { // Layer 0
    let list = {}
    let groups = requestDb(paths[i]) 
    if (groups.keys) {
      groups = groups.keys
    } else {
      run_results[paths[i]] = groups 
      continue
    }
    for (let group in groups) { // Layer 1      
      list[groups[group]] = requestDb(createQuery(paths[i], groups[group]))
      let services = list[groups[group]].keys
      if (services) {        
        for (let service in services) { // Layer 2
          counters = requestDb(createQuery(paths[i], groups[group], services[service]))
          if (!counters.keys) {
            list[groups[group]][services[service]] = counters
          } else {
            counters = counters.keys
            list[groups[group]][services[service]] = { [null] : null }
          }
          // The only elements for which we do not want to fetch everything are the resources which
          // are not filters or findings since they will scale with the environment's size
          if (paths[i] === 'services' && [services[service]] != 'filters' && [services[service]] != 'findings') {
            continue 
          }
          // TODO: Make this amalgalm cleaner   
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
    run_results[paths[i]] = list
  }
  return run_results
}

/**
 * Inserts resource page info into run_results and wipes out the last resource page info from the memory
 * to make sure the memory never gets capped and crashes the browser, also updates page index of the resource
 */
function getResourcePageSqlite (pageIndex, pageSize, service, resource) {
  resources = requestDb(createQuery('services', service, resource), pageSize, pageIndex)
  // Delete the current content
  run_results['services'][service][resource] = null
  // Create a spot where to save data
  run_results['services'][service][resource] = { [null] : null }
  for (let item in resources) {
    let properties = resources[item].keys
    run_results['services'][service][resource][item] = { [null] : null }
    for (let property in properties) {
      run_results['services'][service][resource][item][properties[property]] = 
      requestDb(createQuery('services', service, resource, item, properties[property]))
    }
    delete run_results['services'][service][resource][item].null
  }
  // Save the current page index to remember which page we have saved
  // Originally wanted to save that info under the precise resource, but the handlebar templates create slots for
  // each entry under resource, therefore there were 2 empty slots always added
  run_results['services'][service][resource + '_page_index'] = pageIndex
  // Save the current page size to remember the size of the saved page
  run_results['services'][service][resource + '_page_size'] = pageSize
  delete run_results['services'][service][resource].null
}

/**
 * Creates a query using the query separator to request information from the server
 * Scales with the number of params given
 */
function createQuery () {
  let query = ''
  for (let i = 0; i < arguments.length; i++) {
    query += arguments[i] + querySeparator
  }
  query = query.replace(reQuerySeparator, '');
  return query
}

function testDb () {
  $.ajax({url: "http://127.0.0.1:8000/api/data?key=", success: function(result) {
    console.log(result)
    return result
  }});
}