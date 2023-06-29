// Globals
const resultFormats = {'invalid': 0, 'json': 1, 'sqlite': 2}
Object.freeze(resultFormats)
const $ = window.$
let loadedConfigArray = []
var runResults

/**
 * Event handlers
 */
$(document).ready(function () {
    onPageLoad()
})

/***
 * Generate a unique array
 * @param array
 * @returns {Array.<T>|string}
 */
function arrayUnique(array) {
    var a = array.concat();
    for(var i=0; i<a.length; ++i) {
        for(var j=i+1; j<a.length; ++j) {
            if(a[i] === a[j])
                a.splice(j--, 1);
        }
    }
    return a;
}

/**
 * Implements page load functionality
 */
function onPageLoad() {
    showPageFromHash()

    // when button is clicked, return CSV with finding
    $('#findings_download_button').click(function (event) {
        var buttonClicked = event.target.id
        var anchor = window.location.hash.substr(1)
        // Strip the # sign
        var path = decodeURIComponent(anchor.replace('#', ''))
        // Get resource path based on browsed-to path
        var resourcePath = getResourcePath(path)

        var item_indexes = getValueAt(path);
        var resourcePathArray = resourcePath.split('.')
        var splitPath = path.split('.')
        var findingKey = splitPath[splitPath.length - 2]

        // create array with item values
        var items = [];
        for (let i in item_indexes) {
            // when path ends in '.items' (findings)
            if (typeof item_indexes[i] === 'string') {
                var idArray = item_indexes[i].split('.')
                var id = 'services.' + idArray.slice(0, resourcePathArray.length).join('.')
                var item = getValueAt(id)
            } else {
                var item = item_indexes[i]
            }
            items.push(item)
        }

        if (buttonClicked === 'findings_download_csv_button') {
            var csvArray = []

            // get a list of unique keys from all items
            var unique_keys = [];
            for (let i in items) {
                unique_keys = arrayUnique(unique_keys.concat(Object.keys(items[i])));
            }
            // first row of csv file
            csvArray.push(unique_keys);

            for (let i in items) {

                // put each value in array
                var valuesArray = []
                Object.keys(unique_keys).forEach(function (k) {
                    if(unique_keys[k] in items[i])
                    {
                        valuesArray.push(JSON.stringify(items[i][unique_keys[k]]).replace(/^"(.*)"$/, '$1'));
                    }
                    else {
                        valuesArray.push('');
                    }
                })

                // append to csv array
                csvArray.push(valuesArray)
            }

            downloadAsCsv(findingKey + '.csv', csvArray)
        }

        if (buttonClicked === 'findings_download_json_button') {
            downloadAsJson(findingKey + '.json', items)
        }
    })

    // When the button is clicked, load the desired page
    $('#paging_buttons').click(function (event) {
        let buttonClicked = event.target.id
        let pathArray = getPathArray()
        if (buttonClicked === 'page_forward') {
            loadPage(pathArray, 1)
        } else if (buttonClicked === 'page_backward') {
            loadPage(pathArray, -1)
        }
    })
}

/**
 * Get an array containing the current path subdivided
 * @returns {object}
 */
function getPathArray() {
    let anchor = window.location.hash.substr(1)
    // Strip the # sign
    let path = decodeURIComponent(anchor.replace('#', ''))
    // Get resource path based on browsed-to path
    let resourcePath = getResourcePath(path)
    return resourcePath.split('.')
}

/**
 * Display the account ID -- use of the generic function + templates result in the div not being at the top of the page
 */
var loadAccountId = function () {
    var element = document.getElementById('account_id')
    var value = '<i class="fa fa-cloud"></i> ' + runResults['provider_name'] +
        ' <i class="fa fa-chevron-right"></i> ' + runResults['account_id']
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
function loadConfig(scriptId, cols, force) {
    if (!force && !scriptId.endsWith('.external_attack_surface')) {
        console.log('Script ID: ' + scriptId);
        // Abort if data was previously loaded
        if (loadedConfigArray.indexOf(scriptId) > -1 ) {
            // When the path does not contain .id.
            console.log('Data was already loaded');
            return 0
        }
        let pathArray = scriptId.split('.')
        for (let i = 3; i < pathArray.length; i = i + 2) {
            pathArray[i] = 'id'
        }
        let fixedPath = pathArray.join('.')
        if (loadedConfigArray.indexOf(fixedPath) > -1) {
            // When the loaded path contains id but browsed-to path contains a specific value
            console.log('Fixed path: ' + fixedPath);
            console.log('ID was already substituted');
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
    let list = runResults;
    let pathArray = scriptId.split('.id.')[0].split('.')
    for (let i in pathArray) {
        // Allows for creation of regions-filter etc...
        if (pathArray[i].endsWith('-filters')) {
            pathArray[i] = pathArray[i].replace('-filters', '')
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
    hideAll();
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
    if (loadedConfigArray.indexOf(scriptId) === -1) {
        loadedConfigArray.push(scriptId);
    }
    return 1
}

/**
 * Compile Handlebars templates and update the DOM
 * @param {string} id1
 * @param {string} containerId
 * @param {object} list
 * @param {boolean} replace
 */
function processTemplate(id1, containerId, list, replace) {
    id1 = id1.replace(/<|>/g, '')
    if (document.getElementById(id1)) {
        var templateToCompile = document.getElementById(id1).innerHTML
        var compiledTemplate = Handlebars.compile(templateToCompile)
        var innerHtml = compiledTemplate({items: list})
        if (replace) {
            document.getElementById(containerId).innerHTML = innerHtml
        } else {
            document.getElementById(containerId).innerHTML += innerHtml
        }
    }
}

/**
 * Hide all lists and details
 */
function hideAll() {
    $("[id$='.list']").not("[id='metadata.list']").not("[id='regions.list']").not("[id='filters.list']").hide()

    $("[id*='.details']").hide()
    var element = document.getElementById('scout_display_account_id_on_all_pages')
    if ((element !== undefined) && (element.checked === true)) {
        showRow('account_id')
    }
    currentResourcePath = ''
}

/**
 * Show list and details' container for a given path
 * @param path
 */
function showRow(path) {
    path = path.replace(/.id./g, '.[^.]+.')
    showList(path)
    showDetails(path)
}

/**
 * Shows the list
 * @param {string} path
 */
function showList(path) {
    $('div').filter(function () {
        return this.id.match(path + '.list')
    }).show()
}

/**
 * Shows the details
 * @param {string} path
 */
function showDetails(path) {
    $('div').filter(function () {
        return this.id.match(path + '.details')
    }).show()
}

/**
 *  Hides the list
 * @param {string} path
 */
function hideList(path) {
    $("[id='" + path + "']").hide()
    path = path.replace('.list', '')
    hideItems(path)
}

/**
 * Show links and views for a given path
 * @param path
 */
function showItems(path) {
    path = path.replace(/.id./g, '.[^.]+.') + '.[^.]+.'
    $('div').filter(function () {
        return this.id.match(path + 'link')
    }).show()
    $('div').filter(function () {
        return this.id.match(path + 'view')
    }).show()
}

/**
 * Hide resource views for a given path
 * @param resourcePath
 */
function hideItems(resourcePath) {
    let path = resourcePath.replace(/.id./g, '.[^.]+.') + '.[^.]+.view'
    $('div').filter(function () {
        return this.id.match(path)
    }).hide()
}

/**
 * Hide resource links for a given path
 * @param resourcePath
 */
function hideLinks(resourcePath) {
    // TODO: Handle Region and VPC hiding...
    let path = resourcePath.replace(/.id./g, '.[^.]+.') + '.[^.]+.link'
    $('div').filter(function () {
        return this.id.match(path)
    }).hide()
}

/**
 * Updates the hash with a given path
 * @param path
 */
function updateHash(path) {
    window.location.hash = path;
    showRowWithItems(path); // this handles the case where the hash is the same as that's being updated, e.g. when clicking "Show All"
}

/**
 * Show list, details' container, links, and view for a given path
 * @param path
 */
function showRowWithItems(path) {
    showRow(path)
    showItems(path)
}

/**
 * Shows filters
 * @param {string} resourcePath
 */
function showFilters(resourcePath) {
    hideFilters()
    // Show service filters
    $('[id="' + resourcePath + '.id.filters"]').show()
    // show region filters
    let service = resourcePath.split('.')[1]
    $('[id*="regionfilters.' + service + '.regions"]').show()
}

/**
 * Hides filters
 */
function hideFilters() {
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
function showFindings(path, resourcePath) {
    let items = getValueAt(path)
    let level = getValueAt(path.replace('items', 'level'))
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
            $('[class="' + items[item] + '"]').addClass('finding-' + level)
        }
        $('[id="' + items[item] + '"]').removeClass('finding-hidden')
        $('[id="' + items[item] + '"]').attr('data-finding-service', findingService)
        $('[id="' + items[item] + '"]').attr('data-finding-key', findingKey)
        $('[id="' + items[item] + '"]').click(function (e) {
            let findingId = getId(e.target);
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
 * Returns the ID from an element - if none is found, returns the ID of the closest parent that does
 * @param element
 */
function getId(element) {
    return $(element).closest('[id]').attr('id');
}

/**
 * Show a single item
 * @param id
 */
function showSingleItem(id) {
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
function toggleDetails(keyword, item) {
    var id = '#' + keyword + '-' + item
    $(id).toggle()
}

/**
 * Update the navigation bar
 * @param service
 */
function updateNavbar(path) {
    const navbarIdSuffix = '_navbar'
    const subnavbarIdSuffix = '_subnavbar'

    let splitPath = path.split('.')

    $('[id*="navbar"]').removeClass('active')

    if (path === '') {
        $('#scoutsuite_navbar').addClass('active')
    } else if (splitPath[0] === 'services') {
        const service = splitPath[1]
        let element = $('#' + service + subnavbarIdSuffix)
        while (element.length > 0 && (!element.attr('id') || !element.attr('id').endsWith(navbarIdSuffix))) {
            element = element.parent()
        }

        if (element.length > 0) {
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
function hasNavbarSuffix(element) {
    return element &&
        (!element.attr('id') || element.attr('id') && !element.attr('id').endsWith(navbarIdSuffix))
}

/**
 * Toggles visibility
 * @param {string} id
 */
function toggleVisibility(id) {
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
function iterateEC2ObjectsAndCall(data, entities, callback, callbackArgs) {
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
function findEC2Object(ec2Data, entities, id) {
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
function findEC2ObjectByAttr(ec2Data, entities, attributes) {
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
function findEC2ObjectAttribute(ec2Info, path, id, attribute) {
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
function findAndShowEC2Object(path, id) {
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
function findAndShowEC2ObjectByAttr(path, attributes) {
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
function showEC2Instance2(data) {
    showPopup(single_ec2_instance_template(data))
}

/**
 * Shows EC2 instance
 * @param region
 * @param vpc
 * @param id
 */
function showEC2Instance(region, vpc, id) {
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
function showEC2SecurityGroup(region, vpc, id) {
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
function showObject(path, attrName, attrValue) {
    const pathArray = path.split('.')
    const pathLength = pathArray.length
    let data = getResource(path)

    // Adds the resource path values to the data context
    for (let i = 0; i < pathLength - 1; i += 2) {
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
function getResource(path) {
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
function makeResourceTypeSingular(resourceType) {
    return resourceType.substring(0, resourceType.length - 1).replace(/\.?ie$/, 'y')
}

/**
 * Displays IAM Managed Policy
 * @param policyId
 */
function showIAMManagedPolicy(policyId) {
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
function showIAMInlinePolicy(iamEntityType, iamEntityName, policyId) {
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
function showIAMPolicy(data) {
    showPopup(single_iam_policy_template(data))
    var id = '#iam_policy_details-' + data['report_id']
    $(id).toggle()
}

/**
 * Display S3 bucket
 * @param bucketName
 */
function showS3Bucket(bucketName) {
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
function showS3Object(bucketId, keyId) {
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
function showPopup(content) {
    $('#modal-container').html(content)
    $('#modal-container').modal()
}

/**
 * Get the format of the results that Scout Suite is reading from
 */
function getFormat() {
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
function loadMetadata() {
    if (getFormat() === resultFormats.json) {
        runResults = getScoutsuiteResultsJson()
    } else if (getFormat() === resultFormats.sqlite) {
        runResults = requestDb()
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
                    addTemplates(group, service, section, resourceType,
                        runResults['metadata'][group][service][section][resourceType]['path'],
                        runResults['metadata'][group][service][section][resourceType]['cols'])
                }
            }
        }
    }
    hidePleaseWait()
}

/**********************
 * Browsing functions *
 **********************/

/**
 * Summary
 */
function exportSummary() {
    var anchor = window.location.hash.substr(1)
    // Strip the # sign
    // Get resource path based on browsed-to path
    var item_indexes = getValueAt("");

    // create array with item values
        var items = [];
        var index = 0;
        items[index] = ["Service", "Description", "Affected resources", "Risk level"]
        Object.entries(item_indexes.services).forEach((service) =>{
            Object.entries(service[1].findings).forEach((finding) => {
                index++;
                items[index] = [finding[1].service, finding[1].description, finding[1].flagged_items, finding[1].level];
            })
        });

    downloadAsCsv('summary.csv', items)
}


/**
 * Show About Scout Suite modal
 */
function showAbout() {
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
function showLastRunDetails() {
    $('#modal-container').html(last_run_details_template(runResults))
    $('#modal-container').modal()
}

/**
 * Shows resources details modal
 */
function showResourcesDetails() {
    $('#modal-container').html(resources_details_template(runResults));
    $('#modal-container').modal()

    $('#resources_details_download_csv_button').click(function(){
            var anchor = window.location.hash.substr(1)
            var item_indexes = getValueAt("")
            var items = []
            var index = 0
            items[index] = ["Service", "Resource", "#"]
            var serviceName = ""
            Object.entries(item_indexes.services).forEach((service) => {
                serviceName = service[0]
                Object.entries(service[1]).forEach((attr) => {
                        if ((attr[0].split("_")[1] == "count" || attr[0].split("_")[2] == "count") && attr[1] != 0 && attr[0].split("_")[0] != "regions"){
                                index++;
                                items[index] = [serviceName, attr[0].split("_")[0], attr[1].toString()];
                            }
                })
            })
            downloadAsCsv('findings_summary.csv', items)
        }
    )
}


/**
 * Show main dashboard
 */
function showMainDashboard() {
    hideAll()
    // Hide filters
    hideFilters()
    $('#findings_download_button').hide()
    $('#paging_buttons').hide()
    showRowWithItems('account_id')
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
function makeTitleAcl(resourcePath) {
    resourcePath = resourcePath.replace('service_groups.', '')
    let service = getService(resourcePath)

    const parts = resourcePath.split('.').pop().split('_').map(part => `${part.charAt(0).toUpperCase()}${part.substring(1).toLowerCase()}`)
    let formatted = ''
    do {
        const part = parts.shift()
        formatted += part.length > 1 ? ` ${part} ` : part
    } while (parts.length > 0)

    formatted = formatted.replace(/Acl/g, 'ACL').replace('Findings', 'Dashboard').replace(/</g, '').replace(/>/g, '').trim()

    return service + ' ' + formatted
}

/**
 * Returns the service
 * @param {string} resourcePath
 * @returns {string}
 */
function getService(resourcePath) {
    if (resourcePath.startsWith('services')) {
        var service = resourcePath.split('.')[1]
    } else {
        service = resourcePath.split('.')[0]
    }
    service = makeTitle(service)
    return service
}

/**
 * Update title div's contents
 * @param {string} title
 */
function updateTitle(title) {
    $('#section_title-h2').text(title)
}

/**
 * Updates the Document Object Model
 */
function showPageFromHash() {
    myhash = location.hash.replace(/[^a-zA-Z|0-9|.#-_]/gi,'')
    if (myhash) {
        updateDOM(myhash)
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
function getValueAt(path) {
    return getValueAtRecursive(path, runResults)
}

function getValueAtRecursive(path, source) {
    let value = source;
    let current_path = path;
    let key;
    // iterate over each path elements
    while (current_path) {
        // check if there are more elements to the path
        if(current_path.indexOf('.') != -1){
            key = current_path.substr(0, current_path.indexOf('.'));
        }
        // last element
        else {
            key = current_path;
        }

        try {
            // path containing an ".id"
            if(key == 'id')
            {
                let v = [];
                let w;
                for(let k in value){
                    // process recursively
                    w = getValueAtRecursive(k + current_path.substr(current_path.indexOf('.'), current_path.length), value);
                    v = v.concat(
                        Object.values(w) // get values from array, otherwise it will be an array of key/values
                    );
                }
                return v;
            }
            // simple path, just return element in value
            else {
                value = value[key];
            }
        } catch (err) {
            console.log('Error: ' + err)
        }

        // check if there are more elements to process
        if(current_path.indexOf('.') != -1){
            current_path = current_path.substr(current_path.indexOf('.')+1, current_path.length);
        }
        // otherwise we're done
        else {
            current_path = false;
        }
    }
    return value;
}

var currentResourcePath = ''

/**
 * Updates the Document Object Model
 * @param {string} anchor
 */
function updateDOM(anchor) {
    // Enable or disable the buttons depending on which page you are
    updateButtons()

    // Strip the # sign
    var path = decodeURIComponent(anchor.replace('#', ''))

    // Get resource path based on browsed-to path
    var resourcePath = getResourcePath(path)

    updateNavbar(path)

    const pathSuffixes = [
        'findings',
        'statistics',
        'password_policy',
        'security_policy',
        'permissions',
        '<root_account>',
        'external_attack_surface',
        'output',
    ]

    let show = true
    for (const suffix of pathSuffixes) {
        if (!path.endsWith(`.${suffix}`)) continue
        show = false
        break
    }
    if (show) {
        $('#findings_download_button').show()
        $('#paging_buttons').show()
    } else {
        $('#findings_download_button').hide()
        $('#paging_buttons').hide()
    }

    // Update title
    if (path.endsWith('.items')) {
        let title = getValueAt(path.replace('items', 'description'))
        updateTitle(title)
    } else {
        let title = makeTitleAcl(resourcePath)
        updateTitle(title)
    }

    // Clear findings highlighting
    $('span').removeClass('finding-danger')
    $('span').removeClass('finding-warning')

    // DOM Update
    if (path === '') {
        showMainDashboard()
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
        console.log(resourcePath + ' has already been loaded');
        // 0 is returned when the data was already loaded, a DOM update is necessary then
        if (path.endsWith('.view')) {
            // Same details, one item
            hideItems(currentResourcePath)
            showSingleItem(path)
        } else if (currentResourcePath !== '' && resourcePath.match(currentResourcePath.replace(/.id./g, '.[^.]+.'))) {
            // Same details, multiple items
            hideItems(currentResourcePath)
            showItems(path)
        } else {
            // Switch view for resources
            console.log('Switching view to ' + resourcePath);
            hideAll()
            showRowWithItems(resourcePath)
            // showFilters(resourcePath)
            currentResourcePath = resourcePath
        }
    } else {
        // The DOM was updated by the lazy loading function, save the current resource path
        console.log('View was updated via lazyloading');
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
function lazyLoadingJson(path) {
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
    return loadConfig(path, cols, false);
}

/**
 * Get the resource path based on a given path
 * @param path
 * @returns {string}
 */
function getResourcePath(path) {
    if (path.endsWith('.items')) {
        var resourcePath = getValueAt(path.replace('items', 'display_path'))
        if (resourcePath === undefined) {
            resourcePath = getValueAt(path.replace('items', 'path'))
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
function makeTitle(title) {
    if (typeof (title) !== 'string') {
        console.log('Error: received title ' + title + ' (string expected).')
        return title.toString()
    }

    const uppercaseTitles = [
        'acm', 'aks', 'ec2', 'ecr', 'ecs', 'efs', 'eks', 'gke', 'iam', 'kms', 'rbac',
        'rds', 'sns', 'ses', 'sqs', 'vpc', 'elb', 'elbv2', 'emr', 'dns', 'oss', 'ram',
    ]

    const formattedTitles = {
        'cloudtrail': 'CloudTrail',
        'cloudwatch': 'CloudWatch',
        'cloudformation': 'CloudFormation',
        'cloudfront': 'CloudFront',
        'awslambda': 'Lambda',
        'docdb': 'DocumentDB',
        'dynamodb': 'DynamoDB',
        'guardduty': 'GuardDuty',
        'secretsmanager': 'Secrets Manager',
        'ssm': 'Systems Manager',
        'elasticache': 'ElastiCache',
        'redshift': 'RedShift',
        'cloudstorage': 'Cloud Storage',
        'cloudsql': 'Cloud SQL',
        'stackdriverlogging': 'Stackdriver Logging',
        'stackdrivermonitoring': 'Stackdriver Monitoring',
        'computeengine': 'Compute Engine',
        'kubernetesengine': 'Kubernetes Engine',
        'cloudmemorystore': 'Cloud Memorystore',
        'aad': 'Azure Active Directory',
        'storageaccounts': 'Storage Accounts',
        'sqldatabase': 'SQL Database',
        'virtualmachines': 'Virtual Machines',
        'securitycenter': 'Security Center',
        'keyvault': 'Key Vault',
        'appgateway': 'Application Gateway',
        'rediscache': 'Redis Cache',
        'appservice': 'App Services',
        'loadbalancer': 'Load Balancer',
        'actiontrail': 'ActionTrail',
        'objectstorage': 'Object Storage',

        // Azure and Kubernetes
        'loggingmonitoring': 'Azure Monitor',

        // Kubernetes
        'kubernetesengine': 'GKE'
    }

    title = title.toLowerCase()
    if (uppercaseTitles.indexOf(title) !== -1) {
        return title.toUpperCase()
    } else if (formattedTitles[title.split('_')[0]]) {
        return formattedTitles[title]
    } else {
        const parts = title.split('_').map(part => `${part.charAt(0).toUpperCase()}${part.substring(1).toLowerCase()}`)
        let formatted = ''
        do {
            const part = parts.shift()
            formatted += part.length > 1 ? ` ${part} ` : part
        } while (parts.length > 0)
        return formatted.trim()
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
function addTemplates(group, service, section, resourceType, path, cols) {
    if (cols === undefined) {
        cols = 2
    }
    addTemplate(group, service, section, resourceType, path, 'details')
    if (cols > 1) {
        addTemplate(group, service, section, resourceType, path, 'list')
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
function addTemplate(group, service, section, resourceType, path, suffix) {
    var template = document.createElement('script')
    var partialName = ''
    template.type = 'text/x-handlebars-template'
    template.id = path + '.' + suffix + '.template'
    if (section === 'resources') {
        if (suffix === 'list') {
            if (path.indexOf('.vpcs.id.') > 0) {
                partialName = 'left_menu_for_vpc'
            } else if (path.indexOf('.subscriptions.id.') > 0) {
                partialName = 'left_menu_for_subscription'
            } else if (path.indexOf('projects.id.zones.id.') > 0) {
                partialName = 'left_menu_for_gcp_zone';
            } else if (path.indexOf('projects.id.regions.id.') > 0) {
                partialName = 'left_menu_for_gcp_region';
            } else if (path.indexOf('.regions.id.') > 0) {
                partialName = 'left_menu_for_region'
            } else if (path.indexOf('.projects.id.') > 0) {
                partialName = 'left_menu_for_project'
            } else if (group === '_scout_suite_aggregation' || group.length === 1 && resourceType.startsWith('v')) {
                // no real way to categorize Kubernetes resources
                // hopefully in the future this huge JavaScript file will be decoupled
                partialName = 'left_menu_for_kubernetes_resource'
            } else {
                partialName = 'left_menu'
            }
        } else if (suffix === 'details') {
            if (path.indexOf('.vpcs.id.') > 0) {
                partialName = 'details_for_vpc'
            } else if (path.indexOf('.subscriptions.id.') > 0) {
                partialName = 'details_for_subscription'
            } else if (path.indexOf('projects.id.zones.id') > 0) {
                partialName = 'details_for_gcp_zone';
            } else if (path.indexOf('projects.id.regions.id') > 0) {
                partialName = 'details_for_gcp_region';
            } else if (path.indexOf('.regions.id.') > 0) {
                partialName = 'details_for_region'
            } else if (path.indexOf('.projects.id.') > 0) {
                partialName = 'details_for_project'
            } else if (group === '_scout_suite_aggregation' || group.length === 1 && resourceType.startsWith('v')) {
                // no real way to categorize Kubernetes resources
                // hopefully in the future this huge JavaScript file will be decoupled
                partialName = 'details_for_kubernetes_resource'
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
function filterRules(group, service) {
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
function downloadConfiguration(configuration, name, prefix) {
    var uriContent = 'data:text/json;charset=utf-8,' + encodeURIComponent(prefix + JSON.stringify(configuration, null, 4))
    var dlAnchorElem = document.getElementById('downloadAnchorElem')
    dlAnchorElem.setAttribute('href', uriContent)
    dlAnchorElem.setAttribute('download', name + '.json')
    dlAnchorElem.click()
}

/**
 * Downloads execptions
 */
function downloadExceptions() {
    var url = window.location.pathname
    var profileName = url.substring(url.lastIndexOf('/') + 1).replace('report-', '').replace('.html', '')
    console.log('Download exceptions: ' + exceptions)
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
var toggleElement = function (elementId) {
    $('#' + elementId).toggle()
}

/**
 * Sets the url to filter a specific region
 * @param {string} region
 */
function setFilterUrl(region) {
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
function downloadAsCsv(filename, rows) {
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

    var blob = new Blob([csvFile], {type: 'text/csv;charset=utf-8;'})
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
function downloadAsJson(filename, dict) {
    var jsonStr = JSON.stringify(dict)

    var blob = new Blob([jsonStr], {type: 'application/json;'})
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
