
// Globals
var loaded_config_array = new Array();


//
// Generic load JSON function
//
function load_aws_config_from_json(script_id, cols) {

    // Abort if data was previously loaded
    if (loaded_config_array.indexOf(script_id) > 0) {
        // When the path does not contain .id.
        return 0
    }
    path_array = script_id.split('.');
    for (i=3; i<path_array.length; i=i+2) {
        console.log('P[' + i + ']: ' + path_array[i]);
        path_array[i] = 'id';
    }
    fixed_path = path_array.join('.');
    if (loaded_config_array.indexOf(fixed_path) > 0) {
        // When the loaded path contains id but browsed-to path contains a specific value
        return 0
    }
    path_array[1] = 'id';
    fixed_path = path_array.join('.');
    if (loaded_config_array.indexOf(fixed_path) > 0) {
        // Special case for services.id.violations
        return 0
    }

    // Build the list based on the path, stopping at the first .id. value
    list = aws_info;
    path_array = script_id.split('.id.')[0].split('.');
    console.log('Item will be at ');
    console.log(path_array);
    for (i in path_array) {
        console.log(i);
        list = list[path_array[i]];
    }

    // Update the DOM
    hideAll();
    if (cols == 0) {
        // Metadata
        process_template(script_id + '.list.template', script_id + '.list', list);
    } else if (cols == 1) {
        // Single-column display
        process_template(script_id + '.details.template', 'single-column', list);
    } else if (cols == 2) {
        console.log('foo');
        // Double-column display
        process_template(script_id + '.list.template', 'double-column-left', list);
        process_template(script_id + '.details.template', 'double-column-right', list);
    }

    // Update the list of loaded data
    loaded_config_array.push(script_id);
    console.log(loaded_config_array);
    return 1;
}


//
// Compile Handlebars templates and update the DOM
//
function process_template(id1, container_id, list) {
    console.log('Getting template script from ID = ' + id1);
    var template_to_compile = document.getElementById(id1).innerHTML;
    var compiled_template = Handlebars.compile(template_to_compile);
    console.log('Done compiling, starting processing...');
    console.log('Setting inner HTML value of ID = ' + container_id);
    document.getElementById(container_id).innerHTML += compiled_template({items: list});
    console.log('Done processing template...');
}


//
// Hide all lists and details 
//
function hideAll() {
    $("[id*='.list']").not("[id='metadata.list']").hide();
    $("[id*='.details']").hide();
}


//
// Show list and details' container for a given path
//
function showRow(path) {
    // Fix ids to *
    path = path.replace(/.id./g, '\.[^.]+\.');
    console.log('showRow:: ' + path);
    // Show list
    $('div').filter(function(){ return this.id.match(path + '.list') }).show();
    // show details' container
    $('div').filter(function(){ return this.id.match(path + '.details') }).show();
}

function hideRow(path) {
    path = path.replace(/.id./g, '\.[^.]+\.');
    $('div').filter(function(){ return this.id.match(path + '.list') }).hide();
    $('div').filter(function(){ return this.id.match(path + '.details') }).hide();
}

//
// Show links and views for a given path
//
function showItems(path) {
    path = path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.';
    console.log('showItems:: ' + path);
    $('div').filter(function(){ return this.id.match(path + 'link') }).show();
    $('div').filter(function(){ return this.id.match(path + 'view') }).show();
}


//
// Hide resource views for a given path
//
function hideItems(resource_path) {
    path = resource_path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.view';
    console.log('hideItems:: ' + path);
    $('div').filter(function(){ return this.id.match(path) }).hide();
}


//
// Hide resource links for a given path
//
function hideLinks(resource_path) {
    path = resource_path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.link';
    console.log('hideLinks:: ' + path);
    $('div').filter(function(){ return this.id.match(path) }).hide();
}


//
// Show list, details' container, links, and view for a given path
//
function showRowWithItems(path) {
    showRow(path);
    showItems(path);
}


//
// Show findings
//
function showFindings(path, resource_path) {
    console.log('showFindings:: ' + path);
    items = get_value_at(path);
    resource_path_array = resource_path.split('.');
    for (item in items) {
        var id1 = items[item];
        console.log('Id = ' + id1);
        id_array = id1.split('.');
        var id2 = 'services.' + id_array.slice(0, resource_path_array.length).join('.');
        showSingleItem(id2);
    }
}


//
// Show a single item
//
function showSingleItem(id) {
    if (!id.endsWith('.view')) {
        id = id + '.view';
    }
    console.log('showSingleItem:: ' + id);
    $("[id='" + id + "']").show();
    id = id.replace('.view', '.link');
    $("[id='" + id + "']").show();
}


/*
    prefix = keyword.split('_')[0];
    $("[id*='" + keyword + "-list']").show();
    $("[id*='" + keyword + "-details']").show();
    $("[id*='" + keyword + "-filter']").show();
    $("[id*='" + keyword + "-filtericon']").removeClass('glyphicon-check');
    $("[id*='" + keyword + "-filtericon']").addClass('glyphicon-unchecked');
    $("[id*='" + prefix + "_region-']").show();
    $("[id*='" + prefix + "_region-filtericon']").removeClass('glyphicon-unchecked');
    $("[id*='" + prefix + "_region-filtericon']").addClass('glyphicon-check');
*/


function toggleDetails(keyword, item) {
    var id = '#' + keyword + '-' + item;
    $(id).toggle();
}

// Update the navigation bar
function updateNavbar(service) {
    $('[id*="dropdown"]').removeClass('active-dropdown');
    $('#' + service + '_dropdown').addClass('active-dropdown');
    $('[id*="dropdown"]').show();
}

function toggleVisibility(id) {
    id1 = '#' + id;
    $(id1).toggle()
    id2 = '#bullet-' + id;
    if ($(id1).is(":visible")) {
        $(id2).html('<i class="glyphicon glyphicon-collapse-down"></i>');
    } else {
        $(id2).html('<i class="glyphicon glyphicon-expand"></i>');
    }
}
function iterateEC2ObjectsAndCall(data, entities, callback, callback_args) {
    if (entities.length > 0) {
        var entity = entities.shift();
        var recurse = entities.length;
        for (i in data[entity]) {
            if (recurse) {
                iterateEC2ObjectsAndCall(data[entity][i], eval(JSON.stringify(entities)), callback, callback_args);
            } else {
                callback(data[entity][i], callback_args);
            }
        }
    }
}
function findEC2Object(ec2_data, entities, id) {
    if (entities.length > 0) {
        var entity = entities.shift();
        var recurse = entities.length;
        for (i in ec2_data[entity]) {
            if (recurse) {
                var object = findEC2Object(ec2_data[entity][i], eval(JSON.stringify(entities)), id);
                if (object) {
                    return object;
                }
            } else if(i == id) {
                return ec2_data[entity][i];
            }
        }
    }
    return '';
}
function findEC2ObjectByAttr(ec2_data, entities, attributes) {
    if (entities.length > 0) {
        var entity = entities.shift();
        var recurse = entities.length;
        for (i in ec2_data[entity]) {
            if (recurse) {
                var object = findEC2ObjectByAttr(ec2_data[entity][i], eval(JSON.stringify(entities)), attributes);
                if (object) {
                    return object;
                }
            } else {
                var found = true;
                for (attr in attributes) {
                    // h4ck :: EC2 security groups in RDS are lowercased...
                    if (ec2_data[entity][i][attr].toLowerCase() != attributes[attr].toLowerCase()) {
                        found = false;
                    }
                }
                if (found) {
                    return ec2_data[entity][i];
                }
            }
        }
    }
    return '';
}
function findEC2ObjectAttribute(ec2_info, path, id, attribute) {
    var entities = path.split('.');
    var object = findEC2Object(ec2_info, entities, id);
    if (object[attribute]) {
        return object[attribute];
    }
    return '';
}
function findAndShowEC2Object(path, id) {
    entities = path.split('.');
    var object = findEC2Object(aws_info['services']['ec2'], entities, id);
    var etype = entities.pop();
    if (etype == 'instances') {
        $('#overlay-details').html(single_ec2_instance_template(object));
    } else if(etype == 'security_groups') {
        $('#overlay-details').html(single_ec2_security_group_template(object));
    } else if (etype == 'vpcs') {
        $('#overlay-details').html(single_ec2_vpc_template(object));
    } else if (etype == 'network_acls') {
        object['name']=id;
        $('#overlay-details').html(single_ec2_network_acl_template(object));
    }
    showPopup();
}
function findAndShowEC2ObjectByAttr(path, attributes) {
    entities = path.split('.');
    var object = findEC2ObjectByAttr(aws_info['services']['ec2'], entities, attributes);
    var etype = entities.pop();
    if (etype == 'security_groups') {
        $('#overlay-details').html(single_ec2_security_group_template(object));
    }
    showPopup();
}
function showEC2Instance2(data) {
    $('#overlay-details').html(single_ec2_instance_template(data));
    showPopup();
}
function showEC2Instance(region, vpc, id) {
    var data = aws_info['services']['ec2']['regions'][region]['vpcs'][vpc]['instances'][id];
    $('#overlay-details').html(single_ec2_instance_template(data));
    showPopup();
}
function showEC2SecurityGroup(region, vpc, id) {
    var data = aws_info['services']['ec2']['regions'][region]['vpcs'][vpc]['security_groups'][id];
    $('#overlay-details').html(single_ec2_security_group_template(data));
    showPopup();
}
function showObject(path) {
    var plen = path.length
    var data = aws_info;
    for (var i = 0; i < plen; i++) {
        data = data[path[i]];
    }
    var resource_type = path[1] + '_' + path[plen-2];
    switch(resource_type) {
        case "iam_Groups":
            $('#overlay-details').html(single_iam_group_template(data));
        break;
        case "iam_Roles":
            $('#overlay-details').html(single_iam_role_template(data));
        break;
        case "iam_Users":
            $('#overlay-details').html(single_iam_user_template(data));
        break;
        case "ec2_instances":
            $('#overlay-details').html(single_ec2_instance_template(data));
        break;
        case "ec2_security_groups":
            $('#overlay-details').html(single_ec2_security_group_template(data));
        break;
        case "rds_instances":
            $('#overlay-details').html(single_rds_instance_template(data));
        break;
        case "redshift_clusters":
            $('#overlay-details').html(single_redshift_cluster_template(data));
        break;
    }
    showPopup();
}
function showIAMManagedPolicy(policy_arn) {
    var data = aws_info['services']['iam']['ManagedPolicies'][policy_arn];
    data['PolicyName'] = policy_friendly_name(policy_arn);
    data['ReportId'] = policy_arn.replace(/:/g, '-').replace(/\//g, '-');
    showIAMPolicy(data);
}
function showIAMInlinePolicy(iam_entity_type, iam_entity_name, policy_name) {
    var data = aws_info['services']['iam'][make_title(iam_entity_type)][iam_entity_name]['Policies'][policy_name];
    data['PolicyName'] = policy_name;
    data['ReportId'] = iam_entity_type + '-' + iam_entity_name + '-' + policy_name;
    showIAMPolicy(data);
}
function showIAMPolicy(data) {
    $('#overlay-details').html(single_iam_policy_template(data));
    showPopup();
    var id = '#iam_policy_details-' + data['report_id'];
    $(id).toggle();
}
function showS3Bucket(bucket_name) {
    var data = aws_info['services']['s3']['buckets'][bucket_name];
    $('#overlay-details').html(single_s3_bucket_template(data));
    showPopup();
}
function showS3Object(bucket_name, object_name) {
    var data = aws_info['services']['s3']['buckets'][bucket_name]['keys'][object_name];
    data['name'] = object_name;
    data['bucket_name'] = bucket_name;
    $('#overlay-details').html(single_s3_object_template(data));
    showPopup();
}
function showPopup() {
    $("#overlay-background").show();
    $("#overlay-details").show();
}
function hidePopup() {
    $("#overlay-background").hide();
    $("#overlay-details").hide();
}


//
// Set up dashboards and dropdown menus
//
function load_metadata() {
    load_aws_config_from_json('last_run', 1);
    load_aws_config_from_json('metadata', 0);
    load_aws_config_from_json('services.id.violations', 1);
    show_main_dashboard();
    for (service in aws_info['metadata']) {
        for (section in aws_info['metadata'][service]) {
            for (resource_type in aws_info['metadata'][service][section]) {
                add_templates(service, section, resource_type, aws_info['metadata'][service][section][resource_type]['path'], aws_info['metadata'][service][section][resource_type]['cols']);
            }
        }
    }
}


////////////////////////
// Browsing functions //
////////////////////////


//
// Show About Scout2 div
//
function about() {
    hideAll();
    showRow('about');
    $('#section_title-h2').text('');
}


//
// Show main dashboard
//
function show_main_dashboard() {
    hideAll()
    showRowWithItems('last_run');
    $('#section_title-h2').text('');
}


//
// Show All Resources
// 
function showAllResources(script_id) {
    var path_array = script_id.split('.');
    var selector = "[id^='" + path_array.shift() + "." + path_array.shift() + ".']"
    for (p in path_array) {
        console.log('Selector = ' + selector);
        $(selector).show();
        selector = selector + "[id*='." + path_array[p] + "']";
    }
}


//
// Make title from resource path
//
function makeTitle(resource_path) {
    service = resource_path.split('.')[1];
    resource = resource_path.split('.').pop();
    title = (service + ' ' + resource).replace('_', ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    title = title.replace("Cloudtrail","CloudTrail").replace("Ec2","EC2").replace("Iam","IAM").replace("Rds","RDS").replace("Elb", "ELB").replace("Acl","ACL").replace("Violations", "Dashboard");
    return title
}


//
// Update title div's contents
//
function updateTitle(title) {
    $("#section_title-h2").text(title);
}


//
// Update the DOM
//
function locationHashChanged() {
    updateDOM(location.hash);
}
window.onhashchange = locationHashChanged;


//
// Get value at given path
//
function get_value_at(path) {
    path_array = path.split('.');
    value = aws_info;
    for (p in path_array) {
        value = value[path_array[p]];
    }
    return value;
}

//
// Browsing
//
var current_resource_path = ''
function updateDOM(anchor) {

    // Strip the # sign
    var path = anchor.replace('#', '');

    // Get resource path based on browsed-to path
    var resource_path = get_resource_path(path);
    console.log('Current resource path: ' + current_resource_path);

    // Update title
    if (path.endsWith('.items')) {
        title = get_value_at(path.replace('items', 'description'));
        updateTitle(title);
    } else {
        title = makeTitle(resource_path);
        updateTitle(title);
    }

    // DOM Update
    if (path.endsWith('.items')) {
        // Switch view for findings
        lazy_loading(resource_path);
        hideAll();
        console.log('Resource path for showRow:: ' + resource_path);
        hideItems(resource_path);
        hideLinks(resource_path);
        showRow(resource_path);
        showFindings(path, resource_path);
        current_resource_path = resource_path; // .replace(/.id./g, '\.[^.]+\.');
    } else if (lazy_loading(resource_path) == 0) {
        // 0 is returned when the data was already loaded, a DOM update is necessary then
        if (path.endsWith('.view')) {
            // Same details, one item
            hideItems(current_resource_path);
            showSingleItem(path);
        } else if (current_resource_path != '' && resource_path.match(current_resource_path.replace(/.id./g, '\.[^.]+\.'))) {
            // Same details, multiple items
            console.log('Success !! path = ' + path);
            hideItems(current_resource_path);
            showItems(path);
        } else {
            // Switch view for resources
            console.log('Switch view');
            hideAll();
            showRowWithItems(resource_path);
            current_resource_path = resource_path; // .replace(/.id./g, '\.[^.]+\.');
        }
    } else {
        // The DOM was updated by the lazy loading function, save the current resource path
        current_resource_path = resource_path; // .replace(/.id./g, '\.[^.]+\.');
    }

    // TODO: Findings highlighting

    // Scroll to the top
    window.scrollTo(0,0);
}


//
// TODO: merge into load_aws_config_from_json...
//
function lazy_loading(path) {
    console.log('Lazy loading from ' + path);
    var resource_path_array = path.split('.')
    var service = resource_path_array[1];
    var resource_type = resource_path_array[resource_path_array.length - 1];
    if (resource_type in aws_info['metadata'][service]['resources']) {
        var cols = aws_info['metadata'][service]['resources'][resource_type]['cols'];
    } else {  
        var cols = 1;
    }
    return load_aws_config_from_json(path, cols);
}


//
// Get the resource path based on a given path
//
function get_resource_path(path) {
    var path_array = path.split('.');
    if (path.endsWith('.items')) {
        var resource_path = get_value_at(path.replace('items', 'display_path'));
        if (resource_path == undefined) {
            resource_path = get_value_at(path.replace('items', 'entities'));
        }
        resource_path_array = resource_path.split('.');
        resource_path_array.pop();
        resource_path = 'services.' + resource_path_array.join('.');
    } else if (path.endsWith('.view')) {
        // Resource path is not changed (this may break when using `back' button in browser)
        var resource_path = current_resource_path;
    } else {
        var resource_path = path; // path_array[path_array.length-1];
    }
    console.log('Resource path:: ' + resource_path);
    return resource_path;
}


//
// Format title
//
var make_title = function(title) {
    title = title.toLowerCase();
    if (title == 'cloudtrail') {
        return 'CloudTrail';
    } else if (title == 'ec2') {
        return 'EC2';
    } else if (title == 'iam') {
        return 'IAM';
    } else if (title == 'rds') {
        return 'RDS';
    } else {
        return (title.charAt(0).toUpperCase() + title.substr(1).toLowerCase()).replace('_', ' ');
    }
}

var policy_friendly_name = function(arn) {
    return arn.split(':policy/').pop();
}

// Add one or
var add_templates = function(service, section, resource_type, path, cols) {
    add_template(service, section, resource_type, path, 'details');
    if (cols > 1) {
        add_template(service, section, resource_type, path, 'list');
    }
}

var add_template = function(service, section, resource_type, path, suffix) {
    var template = document.createElement("script");
    template.type = "text/x-handlebars-template";
    template.id = path + "." + suffix + ".template";
    if (section == 'resources') {
        if (suffix == 'list') {
            if (path.indexOf('.vpcs.id.') > 0) {
                partial_name = 'left_menu_for_vpc';
            } else if (path.indexOf('.regions.id.') > 0) {
                partial_name = 'left_menu_for_region';
            } else {
                partial_name = 'left_menu';
            }
        } else if (suffix == 'details') {
            if (path.indexOf('.vpcs.id.') > 0) {
                partial_name = 'details_for_vpc';
            } else if (path.indexOf('.regions.id.') > 0) {
                partial_name = 'details_for_region';
            } else {
                partial_name = 'details';
            }
        } else {
            console.log('Invalid suffix (' + suffix + ') for resources template.');
        }
        template.innerHTML = "{{> " + partial_name + " service_name = '" + service + "' resource_type = '" + resource_type + "' partial_name = '" + path + "'}}";
    } else if (section == 'summaries') {
        template.innerHTML = "{{> " + path + "'}}";
    } else if (section == 'risks') {
        console.log('TBD...');
        return;
    } else {
        console.log('Unsupported dropdown section: ' + section);
        return;
    }
    $('body').append(template);
}

var add_summary_template = function(path) {
    var template = document.createElement("script");
    template.type = "text/x-handlebars-template";
    template.id = path + ".details.template";
    template.innerHTML = "{{> " + partial_name + " service_name = '" + service + "' resource_type = '" + resource_type + "' partial_name = '" + path + "'}}";
    $('body').append(template);
}


