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
    }
  }

  request.send()
  return response.data
}

function loadMetadataSqlite () {
  loadAccountIdSqlite()
  loadConfigSqlite('last_run', 1)
  loadConfigSqlite('metadata', 0)
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
  hidePleaseWait()
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
  pathArray = scriptId.split('.')
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
  pathArray = scriptId.split('.id.')[0].split('.')
  for (let i in pathArray) {
    // Allows for creation of regions-filter etc...
    if (i.endsWith('-filters')) {
      i = i.replace('-filters', '')
    }
    // Returns an array with everything in the second layer
    list = requestDb(pathArray).keys
    listDict = {}
    for (let group in list) {
      listDict[list[group]] = requestDb(pathArray + '.' + list[group])
    }
    list = listDict
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
