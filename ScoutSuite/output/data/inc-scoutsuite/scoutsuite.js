// Globals
var resultFormats = { 'invalid': 0, 'json': 1, 'sqlite': 2 }
Object.freeze(resultFormats)
var loadedConfigArray = new Array()
var run_results

/**
 * Event handlers
 */
$(document).ready(function () {
  onPageLoad()
})

/**
 * Implements page load functionality
 */
function onPageLoad () {
  showPageFromHash()

  // when button is clicked, return CSV with finding
  $('#findings_download_button').click(function (event) {
    var buttonClicked = event.target.id

    var anchor = window.location.hash.substr(1)
    // Strip the # sign
    var path = decodeURIComponent(anchor.replace('#', ''))
    // Get resource path based on browsed-to path
    var resource_path = get_resource_path(path)

    var csvArray = []
    var jsonDict = {}

    var items = get_value_at(path)
    var level = get_value_at(path.replace('items', 'level'))
    var resourcePathArray = resource_path.split('.')
    var splitPath = path.split('.')
    var findingService = splitPath[1]
    var findingKey = splitPath[splitPath.length - 2]

    if (buttonClicked === 'findings_download_csv_button') {
      var firstEntry = 1
      for (let item in items) {
        // get item value
        // when path ends in '.items' (findings)
        if (typeof items[item] === 'string') {
          var idArray = items[item].split('.')
          var id = 'services.' + idArray.slice(0, resourcePathArray.length).join('.')
          var i = get_value_at(id)
        } else {
          i = items[item]
        }

        // for first item, put keys at beginning of csv
        if (firstEntry === 1) {
          var keyValuesArray = []
          Object.keys(i).forEach(function (key) {
            keyValuesArray.push(key)
          })
          csvArray.push(keyValuesArray)
        }
        // put each value in array
        var valuesArray = []
        Object.keys(i).forEach(function (key) {
          valuesArray.push(JSON.stringify(i[key]).replace(/^"(.*)"$/, '$1'))
        })
        // append to csv array
        csvArray.push(valuesArray)
        firstEntry = 0
      }

      download_as_csv(findingKey + '.csv', csvArray)
    }

    if (buttonClicked === 'findings_download_json_button') {
      jsonDict['items'] = []
      for (let item in items) {
        // get item value
        // when path ends in '.items' (findings)
        if (typeof items[item] === 'string') {
          idArray = items[item].split('.')
          id = 'services.' + idArray.slice(0, resourcePathArray.length).join('.')
          i = get_value_at(id)
        } else {
          i = items[item]
        }
        // add item to json
        jsonDict['items'].push(i)
      }
      downloadAsJson(findingKey + '.json', jsonDict)
    }
  })
}

/**
 * Display the account ID -- use of the generic function + templates result in the div not being at the top of the page
 */
var loadAccountIdJson = function () {
  var element = document.getElementById('aws_account_id')
  var value = '<i class="fa fa-cloud"></i> ' + run_results['provider_name'] +
    ' <i class="fa fa-chevron-right"></i> ' + run_results['aws_account_id']
  if (('organization' in run_results) && (value in run_results['organization'])) {
    value += ' (' + run_results['organization'][value]['Name'] + ')'
  }
  element.innerHTML = value
}

/**
 * Generic load JSON function
 * @param scriptId
 * @param cols
 * @returns {number}
 */
function loadConfigJson (scriptId, cols) {
  // Abort if data was previously loaded
  if (loadedConfigArray.indexOf(scriptId) > 0) {
    // When the path does not contain .id.
    return 0
  }
  let pathArray = scriptId.split('.')
  for (let i = 3; i < pathArray.length; i = i + 2) {
    pathArray[i] = 'id'
  }
  let fixedPath = pathArray.join('.')
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
  let list = run_results
  pathArray = scriptId.split('.id.')[0].split('.')
  for (let i in pathArray) {
    // Allows for creation of regions-filter etc...
    if (i.endsWith('-filters')) {
      i = i.replace('-filters', '')
    }
    list = list[pathArray[i]]
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
 * Compile Handlebars templates and update the DOM
 * @param id1
 * @param containerId
 * @param list
 */
function processTemplate (id1, containerId, list) {
  id1 = id1.replace(/<|>/g, '')
  var templateToCompile = document.getElementById(id1).innerHTML
  var compiledTemplate = Handlebars.compile(templateToCompile)
  var innerHtml = compiledTemplate({ items: list })
  document.getElementById(containerId).innerHTML += innerHtml
}

/**
 * Hide all lists and details
 */
function hideAll () {
  $("[id*='.list']").not("[id*='metadata.list']").not("[id='regions.list']").not("[id*='filters.list']").hide()
  $("[id*='.details']").hide()
  var element = document.getElementById('scoutsuite_display_account_id_on_all_pages')
  if ((element !== undefined) && (element.checked === true)) {
    showRow('aws_account_id')
  }
  currentResourcePath = ''
}

/**
 * Show list and details' container for a given path
 * @param path
 */
function showRow (path) {
  path = path.replace(/.id./g, '\.[^.]+\.')
  showList(path)
  showDetails(path)
}

function showList (path) {
  $('div').filter(function () {
    return this.id.match(path + '.list')
  }).show()
}

function showDetails (path) {
  $('div').filter(function () {
    return this.id.match(path + '.details')
  }).show()
}

function hideList (path) {
  $("[id='" + path + "']").hide()
  path = path.replace('.list', '')
  hideItems(path)
}

/**
 * Show links and views for a given path
 * @param path
 */
function showItems (path) {
  path = path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.'
  $('div').filter(function () {
    return this.id.match(path + 'link')
  }).show()
  $('div').filter(function () {
    return this.id.match(path + 'view')
  }).show()
}

/**
 * Hide resource views for a given path
 * @param resource_path
 */
function hideItems (resource_path) {
  path = resource_path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.view'
  $('div').filter(function () {
    return this.id.match(path)
  }).hide()
}

/**
 * Hide resource links for a given path
 * @param resource_path
 */
function hideLinks (resource_path) {
  // TODO: Handle Region and VPC hiding...
  path = resource_path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.link'
  $('div').filter(function () {
    return this.id.match(path)
  }).hide()
}

/**
 * Show list, details' container, links, and view for a given path
 * @param path
 */
function showRowWithItems (path) {
  showRow(path)
  showItems(path)
}

function showFilters (resource_path) {
  hideFilters()
  service = resource_path.split('.')[1]
  // Show service filters
  $('[id="' + resource_path + '.id.filters"]').show()
  // show region filters
  $('[id*="regionfilters.' + service + '.regions"]').show()
}

function hideFilters () {
  $('[id*=".id.filters"]').hide()
  $('[id*="regionfilters"]').hide()
  // Reset dashboard filters
  $('.dashboard-filter').val('')
  $('.finding_items').filter(function () {
    $(this).show()
  })
}

/**
 * Show findings
 * @param path
 * @param resource_path
 */
function showFindings (path, resource_path) {
  let items = get_value_at(path)
  let level = get_value_at(path.replace('items', 'level'))
  let resourcePathArray = resource_path.split('.')
  let splitPath = path.split('.')
  let findingService = splitPath[1]
  let findingKey = splitPath[splitPath.length - 2]
  for (let item in items) {
    var idArray = items[item].split('.')
    var id = 'services.' + idArray.slice(0, resourcePathArray.length).join('.')
    showSingleItem(id)
    if ($('[id="' + items[item] + '"]').hasClass('badge')) {
      $('[id="' + items[item] + '"]').addClass('finding-title-' + level)
    } else {
      $('[id="' + items[item] + '"]').addClass('finding-' + level)
    }
    $('[id="' + items[item] + '"]').removeClass('finding-hidden')
    $('[id="' + items[item] + '"]').attr('data-finding-service', findingService)
    $('[id="' + items[item] + '"]').attr('data-finding-key', findingKey)
    $('[id="' + items[item] + '"]').click(function (e) {
      finding_id = e.target.id
      if (!(findingService in exceptions)) {
        exceptions[findingService] = new Object()
      }
      if (!(findingKey in exceptions[findingService])) {
        exceptions[findingService][findingKey] = new Array()
      }
      is_exception = confirm('Mark this item as an exception ?')
      if (is_exception && (exceptions[findingService][findingKey].indexOf(finding_id) == -1)) {
        exceptions[findingService][findingKey].push(finding_id)
      }
    })
  }
}

/**
 * Show a single item
 * @param id
 */
function showSingleItem (id) {
  if (!id.endsWith('.view')) {
    id = id + '.view'
  }
  $("[id='" + id + "']").show()
  id = id.replace('.view', '.link')
  $("[id='" + id + "']").show()
}

function toggleDetails (keyword, item) {
  var id = '#' + keyword + '-' + item
  $(id).toggle()
}

/**
 * Update the navigation bar
 * @param service
 */
function updateNavbar (path) {
  const navbarIdSuffix = '_navbar'
  const subnavbarIdSuffix = '_subnavbar'

  let splitPath = path.split('.')

  $('[id*="navbar"]').removeClass('active')

  if (path === '') {
    $('#scoutsuite_navbar').addClass('active')
  } else if (splitPath[0] === 'services') {
    const service = splitPath[1]
    let element = $('#' + service + subnavbarIdSuffix)
    while (element && (!element.attr('id') || !element.attr('id').endsWith(navbarIdSuffix))) {
      element = element.parent()
    }

    if (element) {
      element.addClass('active')
    }
  } else if (splitPath[0] === 'service_groups' && splitPath.length >= 2) {
    const group = splitPath[1]
    $('#' + group + navbarIdSuffix).addClass('active')
  }

  $('[id*="navbar"]').show()
}

function hasNavbarSuffix (element) {
  return element &&
    (!element.attr('id') || element.attr('id') &&
      !element.attr('id').endsWith(navbarIdSuffix))
}

function toggleVisibility (id) {
  let id1 = '#' + id
  $(id1).toggle()
  let id2 = '#bullet-' + id
  if ($(id1).is(':visible')) {
    $(id2).html('<i class="fa fa-caret-square-o-down"></i>')
  } else {
    $(id2).html('<i class="fa fa-caret-square-o-right"></i>')
  }
}

/**
 *
 * @param data
 * @param entities
 * @param callback
 * @param callback_args
 */
function iterateEC2ObjectsAndCall (data, entities, callback, callback_args) {
  if (entities.length > 0) {
    var entity = entities.shift()
    var recurse = entities.length
    for (let i in data[entity]) {
      if (recurse) {
        iterateEC2ObjectsAndCall(data[entity][i], eval(JSON.stringify(entities)), callback, callback_args)
      } else {
        callback(data[entity][i], callback_args)
      }
    }
  }
}

/**
 *
 * @param ec2Data
 * @param entities
 * @param id
 * @returns {*}
 */
function findEC2Object (ec2Data, entities, id) {
  if (entities.length > 0) {
    var entity = entities.shift()
    var recurse = entities.length
    for (let i in ec2Data[entity]) {
      if (recurse) {
        var object = findEC2Object(ec2Data[entity][i], eval(JSON.stringify(entities)), id)
        if (object) {
          return object
        }
      } else if (i === id) {
        return ec2Data[entity][i]
      }
    }
  }
  return ''
}

/**
 *
 * @param ec2Data
 * @param entities
 * @param attributes
 * @returns {*}
 */
function findEC2ObjectByAttr (ec2Data, entities, attributes) {
  if (entities.length > 0) {
    var entity = entities.shift()
    var recurse = entities.length
    for (let i in ec2Data[entity]) {
      if (recurse) {
        var object = findEC2ObjectByAttr(ec2Data[entity][i], eval(JSON.stringify(entities)), attributes)
        if (object) {
          return object
        }
      } else {
        var found = true
        for (let attr in attributes) {
          // h4ck :: EC2 security groups in RDS are lowercased...
          if (ec2Data[entity][i][attr].toLowerCase() != attributes[attr].toLowerCase()) {
            found = false
          }
        }
        if (found) {
          return ec2Data[entity][i]
        }
      }
    }
  }
  return ''
}

/**
 *
 * @param ec2_info
 * @param path
 * @param id
 * @param attribute
 * @returns {*}
 */
function findEC2ObjectAttribute (ec2_info, path, id, attribute) {
  var entities = path.split('.')
  var object = findEC2Object(ec2_info, entities, id)
  if (object[attribute]) {
    return object[attribute]
  }
  return ''
}

/**
 *
 * @param path
 * @param id
 */
function findAndShowEC2Object (path, id) {
  let entities = path.split('.')
  if (getFormat() === resultFormats.json) {
    var object = findEC2Object(run_results['services']['ec2'], entities, id)
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQlite) 1')
  }
  var etype = entities.pop()
  if (etype === 'instances') {
    showPopup(single_ec2_instance_template(object))
  } else if (etype === 'security_groups') {
    showPopup(single_ec2_security_group_template(object))
  } else if (etype === 'vpcs') {
    showPopup(single_vpc_template(object))
  } else if (etype === 'network_acls') {
    object['name'] = id
    showPopup(single_vpc_network_acl_template(object))
  }
}

/**
 *
 * @param path
 * @param attributes
 */
function findAndShowEC2ObjectByAttr (path, attributes) {
  let entities = path.split('.')
  if (getFormat() === resultFormats.json) {
  var object = findEC2ObjectByAttr(run_results['services']['ec2'], entities, attributes)
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 2')
  }
  var etype = entities.pop()
  if (etype === 'security_groups') {
    showPopup(single_ec2_security_group_template(object))
  }
}

/**
 *
 * @param data
 */
function showEC2Instance2 (data) {
  showPopup(single_ec2_instance_template(data))
}

/**
 *
 * @param region
 * @param vpc
 * @param id
 */
function showEC2Instance (region, vpc, id) {
  if (getFormat() === resultFormats.json) {
  var data = run_results['services']['ec2']['regions'][region]['vpcs'][vpc]['instances'][id]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 3')
  }
  showPopup(single_ec2_instance_template(data))
}

/**
 *
 * @param region
 * @param vpc
 * @param id
 */
function showEC2SecurityGroup (region, vpc, id) {
  if (getFormat() === resultFormats.json) {
  var data = run_results['services']['ec2']['regions'][region]['vpcs'][vpc]['security_groups'][id]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 4')
  }
  showPopup(single_ec2_security_group_template(data))
}

/**
 *
 */
function showObject (path, attr_name, attr_value) {
  const pathArray = path.split('.')
  const path_length = pathArray.length
  let data = getResource(path)

  // Adds the resource path values to the data context
  for (let i = 0; i < path_length - 1; i += 2) {
    if (i + 1 >= path_length) break

    const attribute = makeResourceTypeSingular(pathArray[i])
    data[attribute] = pathArray[i + 1]
  }

  // Filter if ...
  let resource_type
  if (attr_name && attr_value) {
    for (const resource in data) {
      if (data[resource][attr_name] !== attr_value) continue
      data = data[resource]
      break
    }

    resource_type = pathArray[1] + '_' + pathArray[path_length - 1]
  } else {
    resource_type = pathArray[1] + '_' + pathArray[path_length - 2]
  }

  let resource = makeResourceTypeSingular(resource_type)
  let template = 'single_' + resource + '_template'
  showPopup(window[template](data))
}

/**
 * Gets a resource from the run results.
 * @param {string} path
 */
function getResource (path) {
  if (getFormat() === resultFormats.json) {
    let data = run_results
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 5')
  }
  for (const attribute of path.split('.')) {
    data = data[attribute]
  }
  return data
}

/**
 * Makes the resource type singular.
 * @param {string} resource_type
 */
function makeResourceTypeSingular (resource_type) {
  return resource_type.substring(0, resource_type.length - 1).replace(/\.?ie$/, 'y')
}

/**
 *
 * @param policy_id
 */
function showIAMManagedPolicy (policy_id) {
  if (getFormat() === resultFormats.json) {
  var data = run_results['services']['iam']['policies'][policy_id]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 6')
  }
  data['policy_id'] = policy_id
  showIAMPolicy(data)
}

/**
 *
 * @param iam_entity_type
 * @param iam_entity_name
 * @param policy_id
 */
function showIAMInlinePolicy (iam_entity_type, iam_entity_name, policy_id) {
  if (getFormat() === resultFormats.json) {
  var data = run_results['services']['iam'][iam_entity_type][iam_entity_name]['inline_policies'][policy_id]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 7')
  }
  data['policy_id'] = policy_id
  showIAMPolicy(data)
}

/**
 *
 * @param data
 */
function showIAMPolicy (data) {
  showPopup(single_iam_policy_template(data))
  var id = '#iam_policy_details-' + data['report_id']
  $(id).toggle()
}

/**
 *
 * @param bucket_name
 */
function showS3Bucket (bucket_name) {
  if (getFormat() === resultFormats.json) {
    var data = run_results['services']['s3']['buckets'][bucket_name]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 8')
  }  
  showPopup(single_s3_bucket_template(data))
}

/**
 *
 * @param bucket_id
 * @param key_id
 */
function showS3Object (bucket_id, key_id) {
  if (getFormat() === resultFormats.json) {
    var data = run_results['services']['s3']['buckets'][bucket_id]['keys'][key_id]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 9')
  }
  data['key_id'] = key_id
  data['bucket_id'] = bucket_id
  showPopup(single_s3_object_template(data))
}

/**
 *
 */
function showPopup (content) {
  $('#modal-container').html(content)
  $('#modal-container').modal()
}

/**
 * Get the format of the results that Scout Suite is reading from
 */
function getFormat () {
  if (document.getElementById('sqlite_format')) {
    return resultFormats.sqlite
  } else if (document.getElementById('json_format')) {
    return resultFormats.json
  }
  return resultFormats.invalid
}

function load_metadata () {
  if (getFormat() === resultFormats.json) {
    loadMetadataJson()
  } else if (getFormat() === resultFormats.sqlite) {
    loadMetadataSqlite()
  } else {
    console.log('Error: the result format could not be determined')
  }
}

/**
 * Set up dashboards and dropdown menus
 */
function loadMetadataJson () {
  run_results = getScoutsuiteResults()

  loadAccountIdJson()

  loadConfigJson('last_run', 1)
  loadConfigJson('metadata', 0)
  loadConfigJson('services.id.findings', 1)
  loadConfigJson('services.id.filters', 0) // service-specific filters
  loadConfigJson('services.id.regions', 0) // region filters

  for (let group in run_results['metadata']) {
    for (let service in run_results['metadata'][group]) {
      if (service === 'summaries') {
        continue
      }
      for (let section in run_results['metadata'][group][service]) {
        for (let resource_type in run_results['metadata'][group][service][section]) {
          add_templates(group, service, section, resource_type,
            run_results['metadata'][group][service][section][resource_type]['path'],
            run_results['metadata'][group][service][section][resource_type]['cols'])
        }
      }
    }
  }
  hidePleaseWait()
}

/// /////////////////////
// Browsing functions //
/// /////////////////////

/**
 * Show About Scout Suite modal
 */
function showAbout () {
  $('#modal-container').html(about_scoutsuite_template())
  $('#modal-container').modal()
}

/**
 * Hides Please Wait modal
 */
function hidePleaseWait () {
  $('#please-wait-modal').fadeOut(500, () => { })
  $('#please-wait-backdrop').fadeOut(500, () => { })
}

/**
 * Shows last run details modal
 */
function showLastRunDetails () {
  if (getFormat() === resultFormats.json) {
    $('#modal-container').html(last_run_details_template(run_results))
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 10')
  }
  $('#modal-container').modal()
}

/**
 * Show main dashboard
 */
function show_main_dashboard () {
  hideAll()
  // Hide filters
  hideFilters()
  $('#findings_download_button').hide()
  showRowWithItems('aws_account_id')
  showRowWithItems('last_run')
  $('#section_title-h2').text('')
  // Remove URL hash
  history.pushState('', document.title, window.location.pathname + window.location.search)
  updateNavbar('')
}

/**
 * Make title from resource path
 * @param resource_path
 * @returns {string}
 */
function makeTitle (resource_path) {
  resource_path = resource_path.replace('service_groups.', '')
  service = getService(resource_path)
  resource = resource_path.split('.').pop()
  resource = resource.replace(/_/g, ' ').replace('<', '').replace('>',
    '').replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  }).replace('Acl', 'ACL').replace('Findings', 'Dashboard')
  return service + ' ' + resource
}

/**
 *
 * @param resource_path
 * @returns {string}
 */
function getService (resource_path) {
  if (resource_path.startsWith('services')) {
    service = resource_path.split('.')[1]
  } else {
    service = resource_path.split('.')[0]
  }
  service = make_title(service)
  return service
}

/**
 * Update title div's contents
 * @param title
 */
function updateTitle (title) {
  $('#section_title-h2').text(title)
}

/**
 * Update the DOM
 */
function showPageFromHash () {
  if (location.hash) {
    updateDOM(location.hash)
  } else {
    updateDOM('')
  }
}

window.onhashchange = showPageFromHash

/**
 * Get value at given path
 * @param path
 * @returns {*}
 */
function get_value_at (path) {
  let pathArray = path.split('.')
  if (getFormat() === resultFormats.json) {
    let value = run_results
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 11')
  }
  for (let p in pathArray) {
    try {
      value = value[pathArray[p]]
    } catch (err) {
      console.log(err)
    }
  }
  return value
}

var currentResourcePath = ''

/**
 *
 * @param anchor
 */
function updateDOM (anchor) {
  // Strip the # sign
  var path = decodeURIComponent(anchor.replace('#', ''))

  // Get resource path based on browsed-to path
  var resource_path = get_resource_path(path)

  updateNavbar(path)

  // FIXME this is not a very good implementation
  if (!path.endsWith('.findings') &&
    !path.endsWith('.statistics') &&
    !path.endsWith('.password_policy') &&
    !path.endsWith('.permissions') &&
    !path.endsWith('.<root_account>') &&
    !path.endsWith('.external_attack_surface')) {
    $('#findings_download_button').show()
  } else {
    $('#findings_download_button').hide()
  }

  // Update title
  if (path.endsWith('.items')) {
    let title = get_value_at(path.replace('items', 'description'))
    updateTitle(title)
  } else {
    let title = makeTitle(resource_path)
    updateTitle(title)
  }

  // Clear findings highlighting
  $('span').removeClass('finding-danger')
  $('span').removeClass('finding-warning')

  // DOM Update
  if (path === '') {
    show_main_dashboard()
  } else if (path.endsWith('.items')) {
    // Switch view for findings
    if (getFormat() === resultFormats.json) {
      lazyLoadingJson(resource_path)
    } else if (getFormat() === resultFormats.sqlite) {
      console.log('TODO (SQLite) 12')
    }
    hideAll()
    hideItems(resource_path)
    hideLinks(resource_path)
    showRow(resource_path)
    showFindings(path, resource_path)
    currentResourcePath = resource_path
    showFilters(resource_path)
  } else if (lazyLoadingJson(resource_path) == 0) {
    // 0 is returned when the data was already loaded, a DOM update is necessary then
    if (path.endsWith('.view')) {
      // Same details, one item
      hideItems(currentResourcePath)
      showSingleItem(path)
    } else if (currentResourcePath !== '' && resource_path.match(currentResourcePath.replace(/.id./g, '\.[^.]+\.'))) {
      // Same details, multiple items
      hideItems(currentResourcePath)
      showItems(path)
    } else {
      // Switch view for resources
      hideAll()
      showRowWithItems(resource_path)
      showFilters(resource_path)
      currentResourcePath = resource_path
    }
    // TODO: Highlight all findings...
  } else {
    // The DOM was updated by the lazy loading function, save the current resource path
    showFilters(resource_path)
    currentResourcePath = resource_path
  }

  // Scroll to the top
  window.scrollTo(0, 0)
}

/**
 *
 * @param path
 * @returns {number}
 */
// TODO: merge into load_config_from_json...
function lazyLoadingJson (path) {
  if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 13')
    return 0
  }
  var cols = 1
  var resourcePathArray = path.split('.')
  var service = resourcePathArray[1]
  var resource_type = resourcePathArray[resourcePathArray.length - 1]
  for (let group in run_results['metadata']) {
    if (service in run_results['metadata'][group]) {
      if (service === 'summaries') {
        continue
      }
      if (resource_type in run_results['metadata'][group][service]['resources']) {
        cols = run_results['metadata'][group][service]['resources'][resource_type]['cols']
      }
      break
    }
  }
  if (document.getElementById('json_format')) {
    return loadConfigJson(path, cols)
  } else if (document.getElementById('sqlite_format')) {
    return loadConfigFromSqlite(path, cols)
  } else {
    console.log('Error: the specified format could not determined.')
  }
}

/**
 * Get the resource path based on a given path
 * @param path
 * @returns {*|string}
 */
function get_resource_path (path) {
  if (path.endsWith('.items')) {
    var resource_path = get_value_at(path.replace('items', 'display_path'))
    if (resource_path === undefined) {
      resource_path = get_value_at(path.replace('items', 'path'))
    }
    resourcePathArray = resource_path.split('.')
    lastValue = resourcePathArray.pop()
    resource_path = 'services.' + resourcePathArray.join('.')
  } else if (path.endsWith('.view')) {
    // Resource path is not changed (this may break when using `back' button in browser)
    resource_path = currentResourcePath
  } else {
    resource_path = path
  }
  return resource_path
}

/**
 * Format title
 * @param title
 * @returns {string}
 */
function make_title (title) {
  if (typeof (title) !== 'string') {
    console.log('Error: received title ' + title + ' (string expected).')
    return title.toString()
  }
  title = title.toLowerCase()
  if (['ec2', 'efs', 'iam', 'kms', 'rds', 'sns', 'ses', 'sqs', 'vpc', 'elb', 'elbv2', 'emr'].indexOf(title) !== -1) {
    return title.toUpperCase()
  } else if (title === 'cloudtrail') {
    return 'CloudTrail'
  } else if (title === 'cloudwatch') {
    return 'CloudWatch'
  } else if (title === 'cloudformation') {
    return 'CloudFormation'
  } else if (title === 'config') {
    return 'Config'
  } else if (title === 'awslambda') {
    return 'Lambda'
  } else if (title === 'dynamodb') {
    return 'DynamoDB'
  } else if (title === 'elasticache') {
    return 'ElastiCache'
  } else if (title === 'redshift') {
    return 'RedShift'
  } else if (title === 'cloudstorage') {
    return 'Cloud Storage'
  } else if (title === 'cloudsql') {
    return 'Cloud SQL'
  } else if (title === 'stackdriverlogging') {
    return 'Stackdriver Logging'
  } else if (title === 'stackdrivermonitoring') {
    return 'Stackdriver Monitoring'
  } else if (title === 'computeengine') {
    return 'Compute Engine'
  } else if (title === 'kubernetesengine') {
    return 'Kubernetes Engine'
  } else if (title === 'cloudresourcemanager') {
    return 'Cloud Resource Manager'
  } else if (title === 'storageaccounts') {
    return 'Storage Accounts'
  } else if (title === 'monitor') {
    return 'Monitor'
  } else if (title === 'sqldatabase') {
    return 'SQL Database'
  } else if (title === 'securitycenter') {
    return 'Security Center'
  } else if (title === 'network') {
    return 'Network'
  } else if (title === 'keyvault') {
    return 'Key Vault'
  } else if (title === 'appgateway') {
    return 'Application Gateway'
  } else if (title === 'rediscache') {
    return 'Redis Cache'
  } else if (title === 'appservice') {
    return 'App Service'
  } else if (title === 'loadbalancer') {
    return 'Load Balancer'
  } else {
    return (title.charAt(0).toUpperCase() + title.substr(1).toLowerCase()).replace('_', ' ')
  }
}

/**
 * Add one or
 * @param group
 * @param service
 * @param section
 * @param resource_type
 * @param path
 * @param cols
 */
function add_templates (group, service, section, resource_type, path, cols) {
  if (cols === undefined) {
    cols = 2
  }
  add_template(group, service, section, resource_type, path, 'details')
  if (cols > 1) {
    add_template(group, service, section, resource_type, path, 'list')
  }
}

/**
 * Add resource templates
 * @param group
 * @param service
 * @param section
 * @param resource_type
 * @param path
 * @param suffix
 */
function add_template (group, service, section, resource_type, path, suffix) {
  var template = document.createElement('script')
  var partial_name = ''
  template.type = 'text/x-handlebars-template'
  template.id = path + '.' + suffix + '.template'
  if (section === 'resources') {
    if (suffix === 'list') {
      if (path.indexOf('.vpcs.id.') > 0) {
        partial_name = 'left_menu_for_vpc'
      } else if (path.indexOf('.regions.id.') > 0) {
        partial_name = 'left_menu_for_region'
      } else {
        partial_name = 'left_menu'
      }
    } else if (suffix == 'details') {
      if (path.indexOf('.vpcs.id.') > 0) {
        partial_name = 'details_for_vpc'
      } else if (path.indexOf('.regions.id.') > 0) {
        partial_name = 'details_for_region'
      } else {
        partial_name = 'details'
      }
    } else {
      console.log('Invalid suffix (' + suffix + ') for resources template.')
    }
    template.innerHTML = '{{> ' + partial_name + " service_group = '" + group + "' service_name = '" + service + "' resource_type = '" + resource_type + "' partial_name = '" + path + "'}}"
    $('body').append(template)
  }
}

/**
 * Rules generator
 * @param group
 * @param service
 */
function filter_rules (group, service) {
  if (service === undefined) {
    $("[id*='rule-']").show()
  } else {
    $("[id*='rule-']").not("[id*='rule-" + service + "']").hide()
    $("[id*='rule-" + service + "']").show()
  }
  var id = 'groups.' + group + '.list'
  $("[id='" + id + "']").hide()
}

function downloadConfiguration (configuration, name, prefix) {
  var uriContent = 'data:text/json;charset=utf-8,' + encodeURIComponent(prefix + JSON.stringify(configuration, null, 4))
  var dlAnchorElem = document.getElementById('downloadAnchorElem')
  dlAnchorElem.setAttribute('href', uriContent)
  dlAnchorElem.setAttribute('download', name + '.json')
  dlAnchorElem.click()
}

function download_exceptions () {
  var url = window.location.pathname
  var profile_name = url.substring(url.lastIndexOf('/') + 1).replace('report-', '').replace('.html', '')
  console.log(exceptions)
  downloadConfiguration(exceptions, 'exceptions-' + profile_name, 'exceptions = \n')
}

var showElement = function (element_id) {
  $('#' + element_id).show()
}

var hideElement = function (element_id) {
  $('#' + element_id).hide()
}

var toggle_element = function (element_id) {
  $('#' + element_id).toggle()
}

function set_filter_url (region) {
  let tmp = location.hash.split('.')
  tmp[3] = region
  location.hash = tmp.join('.')
}

/**
 * Returns a csv file to download
 *   example input:
 *   exportToCsv('export.csv', [
 *   ['name','description'],
 *   ['david','123'],
 *   ['jona','""'],
 *   ['a','b'],
 *   ])
 * @param filename
 * @param rows
 */
function download_as_csv (filename, rows) {
  var processRow = function (row) {
    var finalVal = ''
    for (var j = 0; j < row.length; j++) {
      var innerValue = row[j] === null ? '' : row[j].toString()
      if (row[j] instanceof Date) {
        innerValue = row[j].toLocaleString()
      }

      var result = innerValue.replace(/"/g, '""')
      if (result.search(/("|,|\n)/g) >= 0) {
        result = '"' + result + '"'
      }
      if (j > 0) {
        finalVal += ','
      }
      finalVal += result
    }
    return finalVal + '\n'
  }

  var csvFile = ''
  for (var i = 0; i < rows.length; i++) {
    csvFile += processRow(rows[i])
  }

  var blob = new Blob([csvFile], { type: 'text/csv;charset=utf-8;' })
  if (navigator.msSaveBlob) { // IE 10+
    navigator.msSaveBlob(blob, filename)
  } else {
    var link = document.createElement('a')
    if (link.download !== undefined) { // feature detection
      // Browsers that support HTML5 download attribute
      var url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', filename)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }
}

function downloadAsJson (filename, dict) {
  var jsonStr = JSON.stringify(dict)

  var blob = new Blob([jsonStr], { type: 'application/json;' })
  if (navigator.msSaveBlob) { // IE 10+
    navigator.msSaveBlob(blob, filename)
  } else {
    var link = document.createElement('a')
    if (link.download !== undefined) { // feature detection
      // Browsers that support HTML5 download attribute
      var url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', filename)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }
}
