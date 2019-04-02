// Globals
const resultFormats = { 'invalid': 0, 'json': 1, 'sqlite': 2 }
Object.freeze(resultFormats)
const $ = window.$
var loadedConfigArray = []
var runResults

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
    var resourcePath = get_resource_path(path)

    var csvArray = []
    var jsonDict = {}

    var items = get_value_at(path)
    var resourcePathArray = resourcePath.split('.')
    var splitPath = path.split('.')
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

  // When the button is clicked, load the desired page
  $('#paging_buttons').click(function (event) {
    let buttonClicked = event.target.id
    let anchor = window.location.hash.substr(1)
    // Strip the # sign
    let path = decodeURIComponent(anchor.replace('#', ''))
    // Get resource path based on browsed-to path
    let resourcePath = get_resource_path(path)
    let pathArray = resourcePath.split('.')

    if (buttonClicked === 'page_forward') {
      loadPage(pathArray, 1)
    } else if (buttonClicked === 'page_backward') {
      loadPage(pathArray, -1)
    }
  })
}

/**
 * Display the account ID -- use of the generic function + templates result in the div not being at the top of the page
 */
var loadAccountId = function () {
  var element = document.getElementById('aws_account_id')
  var value = '<i class="fa fa-cloud"></i> ' + runResults['provider_name'] +
    ' <i class="fa fa-chevron-right"></i> ' + runResults['aws_account_id']
  if (('organization' in runResults) && (value in runResults['organization'])) {
    value += ' (' + runResults['organization'][value]['Name'] + ')'
  }
  element.innerHTML = value
}

/**
 * Generic load JSON function
 * @param {string} scriptId
 * @param {number} cols
 * @param {boolean} force
 * @returns {number}
 */
function loadConfig (scriptId, cols, force) {
  if (!force) {
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
  }

  // Build the list based on the path, stopping at the first .id. value
  let list = runResults
  let pathArray = scriptId.split('.id.')[0].split('.')
  for (let i in pathArray) {
    // Allows for creation of regions-filter etc...
    if (i.endsWith('-filters')) {
      i = i.replace('-filters', '')
    }
    list = list[pathArray[i]]
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
    processTemplate(scriptId + '.list.template', scriptId + '.list', list, force)
  } else if (cols === 1) {
    // Single-column display
    processTemplate(scriptId + '.details.template', 'single-column', list, force)
  } else if (cols === 2) {
    // Double-column display
    processTemplate(scriptId + '.list.template', 'double-column-left', list, force)
    processTemplate(scriptId + '.details.template', 'double-column-right', list, force)
  }

  // Update the list of loaded data
  loadedConfigArray.push(scriptId)
  return 1
}

/**
 * Compile Handlebars templates and update the DOM
 * @param {string} id1
 * @param {string} containerId
 * @param list
 * @param {boolean} replace
 */
function processTemplate (id1, containerId, list, replace) {
  id1 = id1.replace(/<|>/g, '')
  var templateToCompile = document.getElementById(id1).innerHTML
  var compiledTemplate = Handlebars.compile(templateToCompile)
  var innerHtml = compiledTemplate({ items: list })
  if (replace) {
    document.getElementById(containerId).innerHTML = innerHtml
  } else {
    document.getElementById(containerId).innerHTML += innerHtml
  }
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

/**
 * Shows the list
 * @param {string} path
 */
function showList (path) {
  $('div').filter(function () {
    return this.id.match(path + '.list')
  }).show()
}

/**
 * Shows the details
 * @param {string} path
 */
function showDetails (path) {
  $('div').filter(function () {
    return this.id.match(path + '.details')
  }).show()
}

/**
 *  Hides the list
 * @param {string} path
 */
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
  let path = resource_path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.view'
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
  let path = resource_path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.link'
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

/**
 * Shows filters
 * @param {string} resourcePath
 */
function showFilters (resourcePath) {
  hideFilters()
  let service = resourcePath.split('.')[1]
  // Show service filters
  $('[id="' + resourcePath + '.id.filters"]').show()
  // show region filters
  $('[id*="regionfilters.' + service + '.regions"]').show()
}

/**
 * Hides filters
 */
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
 * @param {string} path
 * @param {string} resourcePath
 */
function showFindings (path, resourcePath) {
  let items = get_value_at(path)
  let level = get_value_at(path.replace('items', 'level'))
  let resourcePathArray = resourcePath.split('.')
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
      let findingId = e.target.id
      if (!(findingService in exceptions)) {
        exceptions[findingService] = {}
      }
      if (!(findingKey in exceptions[findingService])) {
        exceptions[findingService][findingKey] = []
      }
      let isException = confirm('Mark this item as an exception ?')
      if (isException && (exceptions[findingService][findingKey].indexOf(findingId) == -1)) {
        exceptions[findingService][findingKey].push(findingId)
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

/**
 * Toggles details
 * @param {string} keyword
 * @param {string} item
 */
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

/**
 * Tells if navbar has suff
 * @param {*} element
 */
function hasNavbarSuffix (element) {
  return element &&
    (!element.attr('id') || element.attr('id') &&
      !element.attr('id').endsWith(navbarIdSuffix))
}

/**
 * Toggles visibility
 * @param {string} id 
 */
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
 * Iterates through EC2 objects and calls
 * @param data
 * @param entities
 * @param callback
 * @param callbackArgs
 */
function iterateEC2ObjectsAndCall (data, entities, callback, callbackArgs) {
  if (entities.length > 0) {
    var entity = entities.shift()
    var recurse = entities.length
    for (let i in data[entity]) {
      if (recurse) {
        iterateEC2ObjectsAndCall(data[entity][i], eval(JSON.stringify(entities)), callback, callbackArgs)
      } else {
        callback(data[entity][i], callbackArgs)
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
 * Finds EC2 object by attribute
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
 * Finds EC2 object attribute
 * @param ec2Info
 * @param path
 * @param id
 * @param attribute
 * @returns {*}
 */
function findEC2ObjectAttribute (ec2Info, path, id, attribute) {
  var entities = path.split('.')
  var object = findEC2Object(ec2Info, entities, id)
  if (object[attribute]) {
    return object[attribute]
  }
  return ''
}

/**
 * Finds and shows EC2 object
 * @param path
 * @param id
 */
function findAndShowEC2Object (path, id) {
  let entities = path.split('.')
  if (getFormat() === resultFormats.json) {
    var object = findEC2Object(runResults['services']['ec2'], entities, id)
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
 * Finds and shows EC2 object by attribute
 * @param path
 * @param attributes
 */
function findAndShowEC2ObjectByAttr (path, attributes) {
  let entities = path.split('.')
  if (getFormat() === resultFormats.json) {
    var object = findEC2ObjectByAttr(runResults['services']['ec2'], entities, attributes)
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 2')
  }
  var etype = entities.pop()
  if (etype === 'security_groups') {
    showPopup(single_ec2_security_group_template(object))
  }
}

/**
 * Shows EC2 instance
 * @param data
 */
function showEC2Instance2 (data) {
  showPopup(single_ec2_instance_template(data))
}

/**
 * Shows EC2 instance
 * @param region
 * @param vpc
 * @param id
 */
function showEC2Instance (region, vpc, id) {
  if (getFormat() === resultFormats.json) {
    var data = runResults['services']['ec2']['regions'][region]['vpcs'][vpc]['instances'][id]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 3')
  }
  showPopup(single_ec2_instance_template(data))
}

/**
 * Shows EC2 security group
 * @param region
 * @param vpc
 * @param id
 */
function showEC2SecurityGroup (region, vpc, id) {
  if (getFormat() === resultFormats.json) {
    var data = runResults['services']['ec2']['regions'][region]['vpcs'][vpc]['security_groups'][id]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 4')
  }
  showPopup(single_ec2_security_group_template(data))
}

/**
 * Shows object
 * @param {string} path
 * @param {string} attrName
 * @param {string} attrValue
 */
function showObject (path, attrName, attrValue) {
  console.log('Path: ' + path + ' with attrName ' + attrName + ' with attrValue ' + attrValue)
  const pathArray = path.split('.')
  const pathLength = pathArray.length
  let data = getResource(path)

  // Adds the resource path values to the data context
  for (let i = 0; i < pathLength - 1; i += 2) {
    if (i + 1 >= pathLength) break

    const attribute = makeResourceTypeSingular(pathArray[i])
    data[attribute] = pathArray[i + 1]
  }

  // Filter if ...
  let resourceType
  if (attrName && attrValue) {
    for (const resource in data) {
      if (data[resource][attrName] !== attrValue) continue
      data = data[resource]
      break
    }

    resourceType = pathArray[1] + '_' + pathArray[pathLength - 1]
  } else {
    resourceType = pathArray[1] + '_' + pathArray[pathLength - 2]
  }

  let resource = makeResourceTypeSingular(resourceType)
  let template = 'single_' + resource + '_template'
  showPopup(window[template](data))
}

/**
 * Gets a resource from the run results.
 * @param {string} path
 */
function getResource (path) {
  let data = runResults
  for (const attribute of path.split('.')) {
    data = data[attribute]
  }
  return data
}

/**
 * Makes the resource type singular.
 * @param {string} resourceType
 */
function makeResourceTypeSingular (resourceType) {
  return resourceType.substring(0, resourceType.length - 1).replace(/\.?ie$/, 'y')
}

/**
 * Displays IAM Managed Policy
 * @param policyId
 */
function showIAMManagedPolicy (policyId) {
  if (getFormat() === resultFormats.json) {
    var data = runResults['services']['iam']['policies'][policyId]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 6')
  }
  data['policy_id'] = policyId
  showIAMPolicy(data)
}

/**
 * Displays IAM Inline Policy
 * @param iamEntityType
 * @param iamEntityName
 * @param policyId
 */
function showIAMInlinePolicy (iamEntityType, iamEntityName, policyId) {
  if (getFormat() === resultFormats.json) {
    var data = runResults['services']['iam'][iamEntityType][iamEntityName]['inline_policies'][policyId]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 7')
  }
  data['policy_id'] = policyId
  showIAMPolicy(data)
}

/**
 * Displays IAM Policy
 * @param data
 */
function showIAMPolicy (data) {
  showPopup(single_iam_policy_template(data))
  var id = '#iam_policy_details-' + data['report_id']
  $(id).toggle()
}

/**
 * Display S3 bucket
 * @param bucketName
 */
function showS3Bucket (bucketName) {
  if (getFormat() === resultFormats.json) {
    var data = runResults['services']['s3']['buckets'][bucketName]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 8')
  }  
  showPopup(single_s3_bucket_template(data))
}

/**
 * Displays S3 object
 * @param bucketId
 * @param keyId
 */
function showS3Object (bucketId, keyId) {
  if (getFormat() === resultFormats.json) {
    var data = runResults['services']['s3']['buckets'][bucketId]['keys'][keyId]
  } else if (getFormat() === resultFormats.sqlite) {
    console.log('TODO (SQLite) 9')
  }
  data['key_id'] = keyId
  data['bucket_id'] = bucketId
  showPopup(single_s3_object_template(data))
}

/**
 * Displays the popup
 * @param {*} content
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

/**
 * Set up dashboards and dropdown menus
 */
function loadMetadata () {
  if (getFormat() === resultFormats.json) {
    runResults = getScoutsuiteResultsJson() 
  } else if (getFormat() === resultFormats.sqlite) {
    runResults = getScoutsuiteResultsSqlite()
    loadFirstPageEverywhere()
  }

  loadAccountId()

  loadConfig('last_run', 1, false)
  loadConfig('metadata', 0, false)
  loadConfig('services.id.findings', 1, false)
  loadConfig('services.id.filters', 0, false) // service-specific filters
  loadConfig('services.id.regions', 0, false) // region filters

  for (let group in runResults['metadata']) {
    for (let service in runResults['metadata'][group]) {
      if (service === 'summaries') {
        continue
      }
      for (let section in runResults['metadata'][group][service]) {
        for (let resourceType in runResults['metadata'][group][service][section]) {
          add_templates(group, service, section, resourceType,
            runResults['metadata'][group][service][section][resourceType]['path'],
            runResults['metadata'][group][service][section][resourceType]['cols'])
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
  $('#modal-container').html(last_run_details_template(runResults))
  $('#modal-container').modal()
}

/**
 * Shows resources details modal
 */
function showResourcesDetails() {
  $('#modal-container').html(resources_details_template(runResults));
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
  $('#paging_buttons').hide()
  showRowWithItems('aws_account_id')
  showRowWithItems('last_run')
  $('#section_title-h2').text('')
  $('#section_paging-h2').text('')
  // Remove URL hash
  history.pushState('', document.title, window.location.pathname + window.location.search)
  updateNavbar('')
}

/**
 * Make title from resource path
 * @param {string} resourcePath
 * @returns {string}
 */
function makeTitle (resourcePath) {
  resourcePath = resourcePath.replace('service_groups.', '')
  let service = getService(resourcePath)
  let resource = resourcePath.split('.').pop()
  resource = resource.replace(/_/g, ' ').replace('<', '').replace('>',
    '').replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  }).replace('Acl', 'ACL').replace('Findings', 'Dashboard')
  return service + ' ' + resource
}

/**
 * Returns the service
 * @param {string} resourcePath
 * @returns {string}
 */
function getService (resourcePath) {
  if (resourcePath.startsWith('services')) {
    var service = resourcePath.split('.')[1]
  } else {
    service = resourcePath.split('.')[0]
  }
  service = make_title(service)
  return service
}

/**
 * Update title div's contents
 * @param {string} title
 */
function updateTitle (title) {
  $('#section_title-h2').text(title)
}

/**
 * Updates the Document Object Model
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
 * @param {string} path
 * @returns {string}
 */
function get_value_at (path) {
  let pathArray = path.split('.')
  let value = runResults
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
 * Updates the Document Object Model
 * @param {string} anchor
 */
function updateDOM (anchor) {
  // Strip the # sign
  var path = decodeURIComponent(anchor.replace('#', ''))

  // Get resource path based on browsed-to path
  var resourcePath = get_resource_path(path)

  updateNavbar(path)

  // FIXME this is not a very good implementation
  if (!path.endsWith('.findings') &&
    !path.endsWith('.statistics') &&
    !path.endsWith('.password_policy') &&
    !path.endsWith('.permissions') &&
    !path.endsWith('.<root_account>') &&
    !path.endsWith('.external_attack_surface')) {
    $('#findings_download_button').show()
    $('#paging_buttons').show()
  } else {
    $('#findings_download_button').hide()
    $('#paging_buttons').hide()
  }

  // Update title
  if (path.endsWith('.items')) {
    let title = get_value_at(path.replace('items', 'description'))
    updateTitle(title)
  } else {
    let title = makeTitle(resourcePath)
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
    lazyLoadingJson(resourcePath)
    hideAll()
    hideItems(resourcePath)
    hideLinks(resourcePath)
    showRow(resourcePath)
    showFindings(path, resourcePath)
    currentResourcePath = resourcePath
    showFilters(resourcePath)
  } else if (lazyLoadingJson(resourcePath) == 0) {
    // 0 is returned when the data was already loaded, a DOM update is necessary then
    if (path.endsWith('.view')) {
      // Same details, one item
      hideItems(currentResourcePath)
      showSingleItem(path)
    } else if (currentResourcePath !== '' && resourcePath.match(currentResourcePath.replace(/.id./g, '\.[^.]+\.'))) {
      // Same details, multiple items
      hideItems(currentResourcePath)
      showItems(path)
    } else {
      // Switch view for resources
      hideAll()
      showRowWithItems(resourcePath)
      showFilters(resourcePath)
      currentResourcePath = resourcePath
    }
  } else {
    // The DOM was updated by the lazy loading function, save the current resource path
    showFilters(resourcePath)
    currentResourcePath = resourcePath
  }

  // Scroll to the top
  window.scrollTo(0, 0)
}

/**
 * Lazy loading
 * @param {string} path
 * @returns {number}
 */
function lazyLoadingJson (path) {
  var cols = 1
  var resourcePathArray = path.split('.')
  var service = resourcePathArray[1]
  var resourceType = resourcePathArray[resourcePathArray.length - 1]
  for (let group in runResults['metadata']) {
    if (service in runResults['metadata'][group]) {
      if (resourceType in runResults['metadata'][group][service]['resources']) {
        cols = runResults['metadata'][group][service]['resources'][resourceType]['cols']
      }
      break
    }
  }
  return loadConfig(path, cols, false)
}

/**
 * Get the resource path based on a given path
 * @param path
 * @returns {string}
 */
function get_resource_path (path) {
  if (path.endsWith('.items')) {
    var resourcePath = get_value_at(path.replace('items', 'display_path'))
    if (resourcePath === undefined) {
      resourcePath = get_value_at(path.replace('items', 'path'))
    }
    let resourcePathArray = resourcePath.split('.')
    resourcePathArray.pop()
    resourcePath = 'services.' + resourcePathArray.join('.')
  } else if (path.endsWith('.view')) {
    // Resource path is not changed (this may break when using `back' button in browser)
    resourcePath = currentResourcePath
  } else {
    resourcePath = path
  }
  return resourcePath
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
 * Toggles between truncated and full lenght bucket name
 * @param {string} name           Name of the bucket
 */
function toggleName(name) {
  if (name.style.display !== 'contents') {
    name.style.display = 'contents'
  } else {
    name.style.display = 'block'
  }
}

/**
 * Add one or multiple
 * @param group
 * @param service
 * @param section
 * @param resourceType
 * @param path
 * @param cols
 */
function add_templates (group, service, section, resourceType, path, cols) {
  if (cols === undefined) {
    cols = 2
  }
  add_template(group, service, section, resourceType, path, 'details')
  if (cols > 1) {
    add_template(group, service, section, resourceType, path, 'list')
  }
}

/**
 * Add resource templates
 * @param group
 * @param service
 * @param section
 * @param resourceType
 * @param path
 * @param suffix
 */
function add_template (group, service, section, resourceType, path, suffix) {
  var template = document.createElement('script')
  var partialName = ''
  template.type = 'text/x-handlebars-template'
  template.id = path + '.' + suffix + '.template'
  if (section === 'resources') {
    if (suffix === 'list') {
      if (path.indexOf('.vpcs.id.') > 0) {
        partialName = 'left_menu_for_vpc'
      } else if (path.indexOf('.regions.id.') > 0) {
        partialName = 'left_menu_for_region'
      } else {
        partialName = 'left_menu'
      }
    } else if (suffix === 'details') {
      if (path.indexOf('.vpcs.id.') > 0) {
        partialName = 'details_for_vpc'
      } else if (path.indexOf('.regions.id.') > 0) {
        partialName = 'details_for_region'
      } else {
        partialName = 'details'
      }
    } else {
      console.log('Invalid suffix (' + suffix + ') for resources template.')
    }
    template.innerHTML = '{{> ' + partialName + " service_group = '" + group + "' service_name = '" + service + "' resource_type = '" + resourceType + "' partial_name = '" + path + "'}}"
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

/**
 * Downloads the configuration
 * @param {object} configuration
 * @param {string} name
 * @param {string} prefix
 */
function downloadConfiguration (configuration, name, prefix) {
  var uriContent = 'data:text/json;charset=utf-8,' + encodeURIComponent(prefix + JSON.stringify(configuration, null, 4))
  var dlAnchorElem = document.getElementById('downloadAnchorElem')
  dlAnchorElem.setAttribute('href', uriContent)
  dlAnchorElem.setAttribute('download', name + '.json')
  dlAnchorElem.click()
}

/**
 * Downloads execptions
 */
function download_exceptions () {
  var url = window.location.pathname
  var profileName = url.substring(url.lastIndexOf('/') + 1).replace('report-', '').replace('.html', '')
  console.log(exceptions)
  downloadConfiguration(exceptions, 'exceptions-' + profileName, 'exceptions = \n')
}

/**
 * Shows an element
 * @param {string} elementId
 */
var showElement = function (elementId) {
  $('#' + elementId).show()
}

/**
 * Hides an element
 * @param {string} elementId
 */
var hideElement = function (elementId) {
  $('#' + elementId).hide()
}

/**
 * Toggles an element
 * @param {string} elementId
 */
var toggle_element = function (elementId) {
  $('#' + elementId).toggle()
}

/**
 * Sets the url to filter a specific region
 * @param {string} region
 */
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

/**
  * Downloads the dictionary as a .json file
  * @param {string} filename
  * @param {object} dict
  */
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
