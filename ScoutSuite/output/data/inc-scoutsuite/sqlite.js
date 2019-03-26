// Keeping this for now for manual debugging, should be removed later on
function sqliteTest () {
  var request = new XMLHttpRequest()
  request.open('GET', 'http://127.0.0.1:8000/api/data?key=', true)

  request.onload = function () {
    var data = JSON.parse(this.response)
    console.log(data.data)
  }

  request.send()
}

// Example query : http://127.0.0.1:8000/api/data?key=last_run.time
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

function loadMetadataSqlite () {
  loadAccountIdSqlite()
  loadConfigSqlite('last_run', 1)
  loadConfigSqlite('metadata', 0)
  hidePleaseWait()
  loadConfigSqlite('services.id.findings', 1)
  loadConfigSqlite('services.id.filters', 0) // service-specific filters
  loadConfigSqlite('services.id.regions', 0) // region filters
  
  let groups = requestDb('metadata')
  for (let groupKey in groups.keys) {
      let group = groups.keys[groupKey]
    let services = requestDb('metadata.' + group)
    for (let serviceKey in services.keys) {
        let service = services.keys[serviceKey]
      if (service === 'summaries') {
        continue
      }
      let sections = requestDb('metadata.' + group + '.' + service)
      for (let sectionKey in sections.keys) {
        let section = sections.keys[sectionKey]
        let resources_types = requestDb('metadata.' + group + '.' + service + '.' + section)
        for (let resource_typeKey in resources_types.keys) {
          let resource_type = resources_types.keys[resource_typeKey]
          add_templates(group, service, section, resource_type,            
            requestDb('metadata.' + group + '.' + service + '.' + section + '.' + resource_type + '.path'),
            requestDb('metadata.' + group + '.' + service + '.' + section + '.' + resource_type + '.cols'),)
        }
      }
    }
  }
}

/**
 * Display the account ID -- use of the generic function + templates result in the div not being at the top of the page
 */
function loadAccountIdSqlite () {
  var element = document.getElementById('aws_account_id')
  var value = '<i class="fa fa-cloud"></i> ' + requestDb('provider_name') +
    ' <i class="fa fa-chevron-right"></i> ' + requestDb('aws_account_id')
  // This following section has been modeled after the one already existing, I doubt it works
  if (requestDb('organization') != null && value in requestDb('organization')) {
    value += ' (' + requestDb('organization.' + value + '.Name') + ')'
  }
  element.innerHTML = value
}

/**
 * Generic sqlite function
 * @param scriptId
 * @param cols
 * @returns {number}
 */
function loadConfigSqlite (scriptId, cols) {
  // Abort if data was previously loaded
  if (loadedConfigArray.indexOf(scriptId) > 0) {
    // When the path does not contain .id.
    return 0
  }
  var pathArray = scriptId.split('.')
  for (let i = 3; i < pathArray.length; i = i + 2) {
    pathArray[i] = 'id'
  }
  fixedPath = pathArray.join('.')
  if (loadedConfigArray.indexOf(fixedPath) > 0) {
    // When the loaded path contains id but browsed-to path contains a specific value
    return 0
  }
  pathArray[1] = 'id'
  fixedPath = pathArray.join('.')
  if (loadedConfigArray.indexOf(fixedPath) > 0) {
    // Special case for services.id.findings
    return 0
  }

  // Build the list based on the path, stopping at the first .id. value
  var list = {}
  pathArray = scriptId.split('.id.')[0].split('.')
  for (let i in pathArray) {
    // Allows for creation of regions-filter etc...
    if (i.endsWith('-filters')) {
      i = i.replace('-filters', '')
    }
    groups = requestDb(pathArray[i])
    if (groups === null) {
      return 0
    } else {
      groups = groups.keys
    }
    for (let group in groups) {
      list[groups[group]] = requestDb(pathArray[i] + '.' + groups[group])
      let services = list[groups[group]].keys
      if (services) {        
        for (let service in services) {
          list[groups[group]][services[service]] = { [null] : null }
          // If it's a summary we need to go deeper to fill the dashboard
          if (groups[group] === 'summary') {
            let counters = requestDb('last_run.' + groups[group] + '.' + services[service]).keys
            for (counter in counters) {
              list[groups[group]][services[service]][counters[counter]] = 
                requestDb('last_run.summary.' + services[service] + '.' + counters[counter])
            }
            delete list[groups[group]][services[service]].null
          }
          if (pathArray[i] === 'services') {
            let counters = requestDb('services.' + groups[group] + '.' + services[service])
            if (counters.keys) {
              counters = counters.keys
            }
            list[groups[group]][services[service]] = counters
            delete list[groups[group]][services[service]].null
          }
        }
        delete list[groups[group]].type
        delete list[groups[group]].keys
      }
    }
    console.log(list)
    // Filters
    if (pathArray[i] === 'items' && i > 3 && pathArray[i - 2] === 'filters') {
      return 1
    }
  }

  // Default # of columns is 2
  if ((cols === undefined) || (cols === null)) {
    cols = 2
  }

  // Update the DOM
  hideAll()
  if (cols === 0) {
    // Metadata
    scriptId = scriptId.replace('services.id.', '')
    processTemplate(scriptId + '.list.template', scriptId + '.list', list)
  } else if (cols === 1) {
    // Single-column display
    processTemplate(scriptId + '.details.template', 'single-column', list)
  } else if (cols === 2) {
    // Double-column display
    processTemplate(scriptId + '.list.template', 'double-column-left', list)
    processTemplate(scriptId + '.details.template', 'double-column-right', list)
  }

  // Update the list of loaded data
  loadedConfigArray.push(scriptId)
  return 1
}

/**
 *
 * @param path
 * @returns {number}
 */
function lazyLoadingSqlite (path) {
  var cols = 1
  var list = {}
  groups = requestDb('metadata').keys
  for (let group in groups) {
    list[groups[group]] = requestDb('metadata.' + groups[group])
    let services = list[groups[group]].keys
    if (services) {        
      for (let service in services) {        
        let resources = requestDb('metadata.' + groups[group] + '.' + services[service] + '.resources').keys
        if (resources) {
          for (let resource in resources) {
            cols = requestDb('metadata.' + groups[group] + '.' + services[service] + '.resources.' +
              resources[resource] + '.cols')
          }
        }
      }
      delete list[groups[group]].type
      delete list[groups[group]].keys
    }
  }
  return loadConfigSqlite(path, cols)
}

function getLastRunResultsSqlite () {
  groups = requestDb('last_run').keys
  let list = {}
  for (let group in groups) {
    list[groups[group]] = requestDb('last_run.' + groups[group])
    let services = list[groups[group]].keys
    if (services) {        
      for (let service in services) {
        list[groups[group]][services[service]] = { [null] : null }
        // Summary is not needed for the last run details modal
        if (groups[group] === 'summary') {
          break
        }
      }
    }
  }
  let run_results = { last_run : list }
  return run_results
}

