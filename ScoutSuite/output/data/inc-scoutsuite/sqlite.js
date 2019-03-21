// Keeping this for now for manual debugging, should be removed later on
function sqlite_test() {
  var request = new XMLHttpRequest()
  request.open("GET","http://127.0.0.1:8000/api/data?key=", true)
  
  request.onload = function () {
    var data = JSON.parse(this.response)
    console.log(this.response)
  }
  
  request.send()
}

// Example query : http://127.0.0.1:8000/api/data?key=last_run.time
function request_db(query) {
  var request = new XMLHttpRequest()
  request.open("GET","http://127.0.0.1:8000/api/data?key=" + query, false)
  
  var data = undefined
  request.onload = function () {
    if (this.readyState == 4) {
      data = JSON.parse(this.response)
      console.log(data.data)
    }
  }
  
  request.send()
  return data.data
}

function load_metadata_sqlite() {
  load_account_id_sqlite()
  load_config_sqlite('last_run', 1)
  load_config_sqlite('metadata', 0)
  load_config_sqlite('services.id.findings', 1)
  load_config_sqlite('services.id.filters', 0) // service-specific filters
  load_config_sqlite('services.id.regions', 0) // region filters
  /*
  for (group in run_results['metadata']) {
    for (service in run_results['metadata'][group]) {
      if (service == 'summaries') {
        continue
      }
      for (section in run_results['metadata'][group][service]) {
        for (resource_type in run_results['metadata'][group][service][section]) {
          add_templates(group, service, section, resource_type,
            run_results['metadata'][group][service][section][resource_type]['path'],
            run_results['metadata'][group][service][section][resource_type]['cols'])
        }
      }
    }
  }*/

  hidePleaseWait()
}

/**
 * Display the account ID -- use of the generic function + templates result in the div not being at the top of the page
 */
function load_account_id_sqlite() {
  var element = document.getElementById('aws_account_id')
  var value = '<i class="fa fa-cloud"></i> ' + request_db("provider_name") +
    ' <i class="fa fa-chevron-right"></i> ' + request_db("aws_account_id")
  // This following section has been modeled after the one already existing, I doubt it works
  if (request_db("organization") != null && value in request_db("organization")) {
    value += ' (' + request_db('organization.' + value + '.Name') + ')'
  }
  element.innerHTML = value
}


/**
 * Generic sqlite function
 * @param script_id
 * @param cols
 * @returns {number}
 */
function load_config_sqlite(script_id, cols) {
  // Abort if data was previously loaded
  if (loaded_config_array.indexOf(script_id) > 0) {
    // When the path does not contain .id.
    return 0
  }
  path_array = script_id.split('.')
  for (i = 3; i < path_array.length; i = i + 2) {
    path_array[i] = 'id'
  }
  fixed_path = path_array.join('.')
  if (loaded_config_array.indexOf(fixed_path) > 0) {
    // When the loaded path contains id but browsed-to path contains a specific value
    return 0
  }
  path_array[1] = 'id'
  fixed_path = path_array.join('.')
  if (loaded_config_array.indexOf(fixed_path) > 0) {
    // Special case for services.id.findings
    return 0
  }

  // Build the list based on the path, stopping at the first .id. value
  list = request_db("")
  path_array = script_id.split('.id.')[0].split('.')
  for (i in path_array) {
    // Allows for creation of regions-filter etc...
    if (i.endsWith('-filters')) {
      i = i.replace('-filters', '')
    }
    for (key in list) {
      if (key === path_array[i]) {
        list = request_db(key)
      }
    }
  }

  // Filters
  if (path_array[i] == 'items' && i > 3 && path_array[i - 2] == 'filters') {
    return 1
  }

  // Default # of columns is 2
  if ((cols === undefined) || (cols === null)) {
    cols = 2
  }

  // Update the DOM
  hideAll()
  if (cols == 0) {
    // Metadata
    script_id = script_id.replace('services.id.', '')
    process_template(script_id + '.list.template', script_id + '.list', list)
  } else if (cols == 1) {
    // Single-column display
    process_template(script_id + '.details.template', 'single-column', list)
  } else if (cols == 2) {
    // Double-column display
    process_template(script_id + '.list.template', 'double-column-left', list)
    process_template(script_id + '.details.template', 'double-column-right', list)
  }

  // Update the list of loaded data
  loaded_config_array.push(script_id)
  return 1
}