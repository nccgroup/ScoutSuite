// Query separator, keeping it really short it will be used often, hence the truncated name
var qS = '¤'

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
  getScoutsuiteResultsSqlite()
  hidePleaseWait()

  loadAccountIdJson()
  loadConfig('last_run', 1)
  loadConfig('metadata', 0)
  loadConfig('services.id.findings', 1)
  loadConfig('services.id.filters', 0) // service-specific filters
  loadConfig('services.id.regions', 0) // region filters
  
  let groups = requestDb('metadata')
  for (let groupKey in groups.keys) {
      let group = groups.keys[groupKey]
    let services = requestDb('metadata' + qS + group)
    for (let serviceKey in services.keys) {
        let service = services.keys[serviceKey]
      if (service === 'summaries') {
        continue
      }
      let sections = requestDb('metadata' + qS + group + qS + service)
      for (let sectionKey in sections.keys) {
        let section = sections.keys[sectionKey]
        let resources_types = requestDb('metadata' + qS + group + qS + service + qS + section)
        for (let resource_typeKey in resources_types.keys) {
          let resource_type = resources_types.keys[resource_typeKey]
          add_templates(group, service, section, resource_type,            
            requestDb('metadata' + qS + group + qS + service + qS + section + qS + resource_type + qS + 'path'),
            requestDb('metadata' + qS + group + qS + service + qS + section + qS + resource_type + qS + 'cols'),)
        }
      }
    }
  }
}