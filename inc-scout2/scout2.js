// Globals
var loaded_config_array = new Array();

// Generic load JSON function
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
        process_template(script_id + '.list.template', 'single-column', list);
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

// Compile Handlebars templates and update the DOM
function process_template(id1, container_id, list) {
    console.log('Getting template script from ID = ' + id1);
    var template_to_compile = document.getElementById(id1).innerHTML;
    var compiled_template = Handlebars.compile(template_to_compile);
    console.log('Done compiling, starting processing...');
    console.log('Setting inner HTML value of ID = ' + container_id);
    document.getElementById(container_id).innerHTML += compiled_template({items: list});
    console.log('Done processing template...');
}

// Highlight violations
function highlight_violations(service) {
    console.log('Service = ' + service);
    for (violation in aws_info['services'][service]['violations']) {
        var level = aws_info['services'][service]['violations'][violation]['level'];
        for (i in aws_info['services'][service]['violations'][violation]['items']) {
            highlight_item(aws_info['services'][service]['violations'][violation]['items'][i], level);
        }
    }
}

// Highlight a single item
function highlight_item(id, level) {
    if ($('[id$="' + id + '"]').hasClass("badge")) {
        $('[id$="' + id + '"]').addClass('btn-' + level);
    } else {
        $('[id$="' + id + '"]').addClass('finding-' + level);
    }
}

// Hide all items Display functions
function hideAll() {
    $("[id$='.row']").hide();
    $("[id*='.list']").not("[id='metadata.list']").hide();
    $("[id*='.details']").hide();
    $("[id*='.view']").hide();
    updateNavbar();
}

// Show row and details
function showRowWithDetails(id) {
    showElement(id + '.row');
    showElement(id + '.list');
    showElement(id + '.details');
    showElement(id + '.view');
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

// Generic toggle filter function
function toggle_filter(data, filter_name) {
    var filter = data['filters'][filter_name];
    var entities = filter['entity'].split('.');
    var entity = finding_entity(filter['keyword_prefix'], filter['entity']);
    var checkbox = $("#" + entity + '-filtericon-' + filter_name);
    if (checkbox.hasClass("glyphicon-check")) {
        checkbox.removeClass("glyphicon-check");
        checkbox.addClass("glyphicon-unchecked");
        filter['enabled'] = false;
    } else {
        checkbox.removeClass("glyphicon-unchecked");
        checkbox.addClass("glyphicon-check");
        filter['enabled'] = true;
    }
    // Iterate through the objects and update visibility
    iterateEC2ObjectsAndCall(data, entities, toggle_filter_callback, new Array(entity, data['filters']));
}
// Generic toggle filter callback
function toggle_filter_callback(object, args) {
    var must_hide = false;
    var entity = args[0];
    var filters = args[1];
    // Go through each active filter
    for (f in filters) {
        if (filters[f]['enabled']) {
            if ($.inArray(object['id'], filters[f]['items']) > -1) {
                must_hide = true;
            }
        }
    }
    if (must_hide) {
        hideItem(entity, object['id']);
    } else {
        showItem(entity, object['id']);
    }
}

// Region filter functions
function toggle_region(service_name, region_name) {
    var entity = service_name + '_region';
    var checkbox = $("#" + entity + '-filtericon-' + region_name);
    if (checkbox.hasClass("glyphicon-check")) {
        hideRegion(service_name, region_name);
    } else {
        showRegion(service_name, region_name);
    }
}
function clear_all_regions(service_name) {
    for (region in aws_info['services'][service_name]['regions']) {
        hideRegion(service_name, region);
    }
    $('[id="' + service_name  + '_region-filter-select_all"]').show();
    $('[id="' + service_name  + '_region-filter-select_none"]').hide();
}
function select_all_regions(service_name) {
    for (region in aws_info['services'][service_name]['regions']) {
        showRegion(service_name, region);
    }
    $('[id="' + service_name  + '_region-filter-select_all"]').hide();
    $('[id="' + service_name  + '_region-filter-select_none"]').show();
}
function hideRegion(service_name, region_name) {
    var checkbox = $("#" + service_name + '_region-filtericon-' + region_name);
    checkbox.removeClass("glyphicon-check");
    checkbox.addClass("glyphicon-unchecked");
    hideItem(service_name + '_region', region_name);
}
function showRegion(service_name, region_name) {
    var checkbox = $("#" + service_name + '_region-filtericon-' + region_name);
    checkbox.removeClass("glyphicon-unchecked");
    checkbox.addClass("glyphicon-check");
    showItem(service_name + '_region', region_name);
}

// Set up dashboards and dropdown menus
function load_dashboards() {
//    load_aws_config_from_json('about_run', 'last_run', 1);
    load_aws_config_from_json('services.violations', 'services', 1);
    load_aws_config_from_json('dropdown', 'metadata', 1);
    show_main_dashboard();
}

function load_metadata() {
    load_aws_config_from_json('last_run', 1);
    load_aws_config_from_json('metadata', 0);
    load_aws_config_from_json('services.id.violations', 1);
    show_main_dashboard();
    for (service in aws_info['metadata']) {
    if (service != 'iam' && service != 's3') {
        for (section in aws_info['metadata'][service]) {
        if (section == 'resources') {
            for (resource_type in aws_info['metadata'][service][section]) {
                add_templates(service, resource_type, aws_info['metadata'][service][section][resource_type]['path'], aws_info['metadata'][service][section][resource_type]['cols']);
            }
        }
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
    showRowWithDetails('last_run');
    $('#section_title-h2').text('');
}

function list_generic(script_id, path, cols) {
    path_array = path.split('.');
    service = script_id.split('.')[1];
    /* Clear */
    hideAll();
    /* Load if not existing */
    if (loaded_config_array.indexOf(script_id) < 0) {
        $('[id="please_wait.row"]').show();
        setTimeout(function(){
            load_aws_config_from_json(script_id, path, cols);
            highlight_violations(service);
            $('[id="please_wait.row"]').hide();
        }, 50);
    } else {
        /* TODO: maybe optimize by item only, not the whole service... */
        highlight_violations(service);
    }
    /* Display */
    updateNavbar(service);
/*
    if (script_id.endsWith('violations')) {
        showRowWithDetails('services.violations');
    }
*/
    hideAll();
    showAllResources(script_id);

/*
    showRowWithDetails(script_id);
    for (var i=1;i<=path_array.length;i+=2) {
        var id=path_array.slice(0,i+1).join('.');
        console.log('ID = ' + id);
        showRowWithDetails(id);
    }
*/

    /* Update Title */
    partial_array = script_id.split('.');
    title = partial_array[1] + ' ' + partial_array[partial_array.length-1];
    title = title.replace(/_/g, ' ');
    updateTitle(title);
    window.scrollTo(0,0);
}

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
    myBrowse(location.hash);
}
window.onhashchange = locationHashChanged;

var old_anchor = ''
function myBrowse(anchor) {
    var old_path = old_anchor.replace('#', '').split('.id.')[0]
    var new_path = anchor.replace('#', '').split('.id.')[0];
    console.log('Old path = ' + old_path);
    console.log('New path = ' + new_path);
    // If we're hiding part of what's already there...
    if (old_path != '' && new_path.startsWith(old_path)) {
        $("[id^='" + old_path + "']").filter("[id$='.view']").hide();
        $("[id^='" + new_path + "']").show();
    } else {
        old_anchor = anchor;
        hideAll();
        // Lazy Loading
//    var path = anchor.replace('#', '').split('*').split('.id.')[0];
        var path = anchor.replace('#', '');
        var path_array = path.split('.');
        var service = path_array[1];
        var resource_type = path_array[path_array.length-1];
        var head = path.split('.id.')[0];

//        var path = anchor.replace('#', '').split('.id.')[0];

        updateTitle(resource_type);
        console.log('Service = ' + service);
        console.log('Resource = ' + resource_type);
        if (resource_type in aws_info['metadata'][service]['resources']) {
            var cols = aws_info['metadata'][service]['resources'][resource_type]['cols'];
        } else {
            var cols = 1;
        }
        load_aws_config_from_json(path, cols);

        // DOM update
        var id = anchor.replace('#', '');
        $('div').filter(function() {
            return this.id.match(id)
        }).show();

    }

    // Scroll to the top
    window.scrollTo(0,0);
    return

    if (anchor.indexOf('*') > 0) {
        /* "Show All" */
        parts = anchor.replace('#', '').split('*');
        $('div').filter("[id^='"+parts[0]+"']").filter("[id*='"+parts[1]+"']").show();
        return
    } else {
        /* "Show one" */
        path = anchor.replace('#', '').split('.');
        var p1 = path.shift() + '.' + path.shift();
        var p2 = '';
        // Hide non-selected items
        while (resource_type = path.shift()) {
            console.log('Resource type = ' + resource_type);
            p1 = p1 + '.' + resource_type;
            resource_id = path.shift();
            if (resource_id == undefined || resource_id == 'undefined') {
                break;
            }
            p2 = p1 + '.' + resource_id;
            $('div').filter("[id^='"+p1+"']").not("[id$='row']").not("[id$='list']").not("[id$='details']").not("[id^='"+p2+"']").hide();
            p1 = p2;
        }
        // Show previously-hidden items
        path = p1.split('.');
        path.pop();
        while (path.length > 0) {
            showRowWithDetails(path.join('.'));
            path.pop();
        }
        if (! p1.endsWith('view')) {
            $('div').filter("[id^='"+p1+"']").show();
        }
    }
    // Scroll to the top
    window.scrollTo(0,0);
}

function foo(items) {
    console.log('In foo with ');
    console.log(items);
    var new_array = {};
    for (item in items) {
        showRowWithDetails('services.' + item);
        path_array = item.split('.')
        if (path_array.length > 1) {
            path_array.pop();
            new_array[path_array.join('.')] = 1;
        }
    }
    if (Object.keys(new_array).length > 0) {
        console.log('Will call foo with ');
        console.log(new_array);
        foo(new_array);
    }
}
function list_findings(service, violation) {
    updateNavbar();
    hideAll();
    updateTitle(aws_info['services'][service]['violations'][violation]['description']);
    var resource_type = aws_info['services'][service]['violations'][violation]['items'][0].split('.');
    if (resource_type[1] != 'regions') {
        resource_type = resource_type[1].toLowerCase();
    } else if (resource_type[3] != 'vpcs') {
        resource_type = resource_type[3].toLowerCase();
    } else {
        resource_type = resource_type[5].toLowerCase();
    }
    console.log('Resource type = ' + resource_type);
    var script_id = aws_info['metadata'][service]['resources'][resource_type]['script'];

    if (loaded_config_array.indexOf(script_id) < 0) {
        setTimeout(function(){
            var path = aws_info['metadata'][service]['resources'][resource_type]['path'];
            var cols = aws_info['metadata'][service]['resources'][resource_type]['cols'];
            list_generic(script_id, path, cols);
            $('[id="please_wait.row"]').hide();
        }, 50);
    }    
    var new_array = {};
    for (i in aws_info['services'][service]['violations'][violation]['items']) {
        path = aws_info['services'][service]['violations'][violation]['items'][i];
        showRowWithDetails('services.' + path);
        path_array = path.split('.');
        path_array.pop();
        var tmp = path_array.join('.');
        console.log(tmp);
        new_array[tmp] = 1;
    }
    console.log('Will call foo with ');
    console.log(new_array);
    foo(new_array);
    window.scrollTo(0,0);
}

var gc = {}; gc['group'] = 0; gc['role'] = 0; gc['user'] = 0;
function parse_entities(keyword, permissions) {
    var p = '';
    var r = '';
    for (i in permissions) {
        p += format_entity(keyword, permissions[i].name, permissions[i].policy_name, gc[keyword]++);
    }
    if (p != '') {
        r = '<p>' + keyword.charAt(0).toUpperCase() + keyword.slice(1) + 's:</p><ul>' + p + '</ul>';
    }
    return r;
}
function format_entity(keyword, name, policy_name, c) {
    var r = '';
    r += "<li>" + name + " [<a href=\"javascript:toggleDetails('" + keyword + "'," + c + ")\">Details</a>]";
    r += "<div class=\"row\" style=\"display:none\" id=\"" + keyword + "-" + c + "\">" + policy_name + "</div></li>";
    return r;
}

function finding_entity(prefix, entity) {
    return '';
    entity = entity.split('.').pop();
    elength = entity.length;
    if (entity.substring(elength - 1, elength) == 's') {
        return prefix + '_' + entity.substring(0, elength - 1);
    } else {
        return prefix + '_' + entity;
    }
}

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


var add_templates = function(service, resource_type, path, cols) {
    add_template(service, resource_type, path, 'details');
    if (cols > 1) {
        add_template(service, resource_type, path, 'list');
    }
}

var add_template = function(service, resource_type, path, suffix) {
    var template = document.createElement("script");
    template.type = "text/x-handlebars-template";
    template.id = path + "." + suffix + ".template";
    if (suffix == 'list') {
        if (path.indexOf('.vpcs.id.') > 0) {
            partial_name = 'left_menu_for_vpc';
        } else if (path.indexOf('.regions.id.') > 0) {
            partial_name = 'left_menu_for_region';
        } else {
            console.log('Error');
        }
    } else if (suffix == 'details') {
        if (path.indexOf('.vpcs.id.') > 0) {
            partial_name = 'details_for_vpc';
        } else if (path.indexOf('.regions.id.') > 0) {
            partial_name = 'details_for_region';
        } else {
            console.log('Error');
        }
    }
    template.innerHTML = "{{> " + partial_name + " service_name = '" + service + "' resource_type = '" + resource_type + "' partial_name = '" + path + "'}}";
    $('body').append(template);
    console.log('Appended to body:')
    console.log(template)
}


