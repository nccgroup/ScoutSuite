// Query separator, keeping the name truncated it since will be used often
var qS = '¤'

// TODO: change for something that does not throw XML errors
/**
 * Requests a list corresponding to the resource
 * @param query           : The resource requested
 */
function requestDb (query) {
  var request = new XMLHttpRequest()
  request.open('GET', 'http://127.0.0.1:8000/api/data?key=' + query, false)

  var response
  request.onload = function () {
    if (this.readyState === 4) {
      response = JSON.parse(this.response)
      if (response.data === null || response.data === undefined) {
        console.log('Error, bad request: ' + query)
      }
    }
  }

  request.send()
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
  var request = new XMLHttpRequest()
  request.open('GET', 'http://127.0.0.1:8000/api/page?pagesize=' + pageSize + '&page=' + pageIndex + 
    '&key=' + query, false)

  var response
  request.onload = function () {
    if (this.readyState === 4) {
      response = JSON.parse(this.response)
      if (response.data === null || response.data === undefined) {
        console.log('Error, bad request: ' + query)
      }
    }
  }

  request.send()
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
      list[groups[group]] = requestDb(paths[i] + qS + groups[group])
      let services = list[groups[group]].keys
      if (services) {        
        for (let service in services) { // Layer 2
          list[groups[group]][services[service]] = { [null] : null }
          let counters = requestDb(paths[i] + qS + groups[group] + qS + services[service])
          if (counters.keys) {
            counters = counters.keys
          } else {
            continue
          }              
          // The only elements for which we do not want to fetch everything are the resources which
          // are not filters or findings since they will scale with the environment's size
          if (paths[i] === 'services' && [services[service]] != 'filters' && [services[service]] != 'findings') {
            continue 
          }
          // TODO: Make this amalgalm cleaner   
          for (let counter in counters) { // Layer 3
            list[groups[group]][services[service]][counters[counter]] = 
              requestDb(paths[i] + qS + groups[group] + qS + services[service] + qS + counters[counter])           
            let resources = list[groups[group]][services[service]][counters[counter]].keys              
            for (let resource in resources) { // Layer 4
              list[groups[group]][services[service]][counters[counter]][resources[resource]] = requestDb(paths[i] + qS + 
              groups[group] + qS + services[service] + qS + counters[counter] + qS + resources[resource])
              let items = list[groups[group]][services[service]][counters[counter]][resources[resource]].keys
              for (let item in items) { // Layer 5
                list[groups[group]][services[service]][counters[counter]][resources[resource]][items[item]] = 
                requestDb(paths[i] + qS + groups[group] + qS + services[service] + qS + counters[counter] + qS + 
                resources[resource] + qS + items[item])
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
  // e.g. pricings --> run_results.services.securitycenter.pricings
  // Fill the resource elements with the elements of the proper page
  run_results['services'][service][resource] = requestDbPage(createQuery('services', service, resource), 
    pageSize, pageIndex)
  // Save the current page index to remember which page we have saved
  run_results['services'][service][resource]['current_page'] = pageIndex
  console.log(run_results['services'][service][resource])
}

/**
 * Creates a query using the query separators to request information from the server
 * Scales with the number of params given
 */
function createQuery () {
  let query = ''
  for (let i = 0; i < arguments.length; i++) {
    query += arguments[i] + qS
  }
  regex = new RegExp('\\' + qS + '+$');
  query = query.replace(regex, '');
  return query
}