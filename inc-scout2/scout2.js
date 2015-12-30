
// Globals
var loaded_config_array = new Array();


//
// Generic load JSON function
//
function load_aws_config_from_json(script_id, cols) {

    // Abort if data was previously loaded
    if (loaded_config_array.indexOf(script_id) > 0) {
        // When the path does not contain .id.
        return
    }
    path_array = script_id.split('.');
    for (i=3; i<path_array.length; i=i+2) {
        console.log('P[' + i + ']: ' + path_array[i]);
        path_array[i] = 'id';
    }
    fixed_path = path_array.join('.');
    if (loaded_config_array.indexOf(fixed_path) > 0) {
        // When the loaded path contains id but browsed-to path contains a specific value
        return
    }
    path_array[1] = 'id';
    fixed_path = path_array.join('.');
    if (loaded_config_array.indexOf(fixed_path) > 0) {
        // Special case for services.id.violations
        return
    }

    // Build the list based on the path, stopping at the first .id. value
    list = aws_info;
    path_array = script_id.split('.id.')[0].split('.');
    console.log('Item will be at ');
    console.log(path_array);
    for (i in path_array) {
        list = list[path_array[i]];
    }

    // Update the DOM
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
// Hide all items Display functions
//
function hideAll() {
    $("[id$='.row']").hide();
    $("[id*='.list']").not("[id='metadata.list']").hide();
    $("[id*='.link']").hide();
    $("[id*='.details']").hide();
    $("[id*='.view']").hide();
    updateNavbar();
}
function showAll() {
//    $("[id$='.row']").show();
    $("[id*='.list']").show();
//    $("[id*='.details']").show();
//    $("[id*='.view']").show();
    updateNavbar();
}



function showRow(path) {
    path_array = path.split('.id.');
    for (i in path_array) {
        tmp = path_array.slice(0,i+1).join('.');
        $('div').filter(function() { return this.id.match(tmp+'.*.row')}).show();
        $('div').filter(function() { return this.id.match(tmp+'.*.list')}).show();
        $('div').filter(function() { return this.id.match(tmp+'.*.details')}).show();
    }
}

function showRowWithItems(path) {
    showRow(path);
    $('div').filter(function() { return this.id.match(tmp+'.*.link')}).show();
    $('div').filter(function() { return this.id.match(tmp+'.*.view')}).show();
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

// Show a DOM element given its ID
function showElement(id) {
    var element = document.getElementById(id);
    if (element) {
        element.style.display = 'block';
    }
}

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

function about() {
    hideAll();
    showRow('about');
    $('#section_title-h2').text('');
}

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

function updateTitle(title) {
    title = title.replace('_', ' ').replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    title = title.replace("Cloudtrail","CloudTrail").replace("Ec2","EC2").replace("Iam","IAM").replace("Rds","RDS").replace("Elb", "ELB").replace("Acl","ACL").replace("Violations", "Dashboard");
    $("#section_title-h2").text(title);
}


function locationHashChanged() {
    updateDOM(location.hash); // .replace('#'));
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
var old_anchor = ''
function updateDOM(anchor) {
    var old_path = old_anchor.replace('#', '').split('.id.')[0]
    var new_path = anchor.replace('#', '').split('.id.')[0];
    var path = anchor.replace('#', '');
    var path_array = path.split('.');
    var service = path_array[1];
    var resource_type = path_array[path_array.length-1];
    var finding_prefix = 'services.' + service + '.violations.'
    console.log('Old path = ' + old_path);
    console.log('New path = ' + new_path);
    console.log('Finding path = ' + finding_prefix);  
    if (new_path.startsWith(finding_prefix)) {
        // Show findings...
        var finding_path = get_value_at(new_path.replace('items', 'entities'));
        var id_suffix = get_value_at(new_path.replace('items', 'id_suffix'));
        var finding_path_array = finding_path.split('.');        
        finding_path_array.pop();
        finding_path = finding_path_array.join('.');        
        var finding_resource_type = finding_path_array[finding_path_array.length-1];
        if (finding_resource_type in aws_info['metadata'][service]['resources']) {
            var cols = aws_info['metadata'][service]['resources'][finding_resource_type]['cols'];
        } else {
            var cols = 1;
        }
        hideAll();
        load_aws_config_from_json('services.' + finding_path, cols);
        hideAll();
        updateTitle('TODO')
        // Show findings only...
        showRow('services.' + finding_path);
        // Show items
        items = get_value_at(new_path);
        for (item in items) {
            var id = items[item];
            if (id_suffix) {
                id = id.replace('.' + id_suffix, '');
            }
            $('div').filter(function() {
                return this.id.match(id)
            }).show();

        }
    } else if (old_path != '' && new_path.startsWith(old_path) && !new_path.startsWith(finding_path)) {
        // If we're hiding part of what's already there...
        $("[id^='" + old_path + "']").filter("[id$='.view']").hide();
        $("[id^='" + new_path + "']").show();
    } else {
        // Switching view...
        old_anchor = anchor;
        hideAll();
        updateTitle(resource_type);
        console.log('Service = ' + service);
        console.log('Resource = ' + resource_type);
        if (resource_type in aws_info['metadata'][service]['resources']) {
            var cols = aws_info['metadata'][service]['resources'][resource_type]['cols'];
        } else {
  
          var cols = 1;
        }
        // Lazy loading
        load_aws_config_from_json(path, cols);
        // DOM update
        hideAll();
        showRowWithItems(new_path);
    }

    // Coloring here ?

    // Scroll to the top
    window.scrollTo(0,0);

    // Done !
    return
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


