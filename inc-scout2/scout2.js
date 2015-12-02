var loaded_config_array = new Array();
var violations_array = new Array();

// Generic load JSON function
//function load_aws_config_from_json(path, parent_id, base_id, cols) {
//function list_generic(script_id, path, cols) {
function load_aws_config_from_json(script_id, path, cols) {
    list = aws_info;
    path_array = path.split('.');   
    for (i in path_array) {
        list = list[path_array[i]];
    }
    var id1 = script_id + '.list.template';
    var id2 = script_id + '.list';
    process_template(id1, id2, list);
    if (cols >= 2) {
        var id3 = script_id + '.details.template';
        var id4 = script_id + '.details';
        process_template(id3, id4, list);
    }
    loaded_config_array.push(script_id);
    console.log('Loaded data:');
    console.log(loaded_config_array);
}

function process_template(id1, id2, list) {
    console.log('Getting template script from ID = ' + id1);
    var template_to_compile = document.getElementById(id1).innerHTML;
    var compiled_template = Handlebars.compile(template_to_compile);
    console.log('Done compiling, starting processing...');
    console.log('Setting inner HTML value of ID = ' + id2);
    document.getElementById(id2).innerHTML += compiled_template({items: list});
    console.log('Done processing template...');
}


// Generic highlight finding function
function highlight_violations(violations, keyword) {
    console.log(violations);
    for (v in violations) {
        var level = violations[v]['level'];
        for (i in violations[v]['items']) {
            id = violations[v]['items'][i];
            console.log('Will add class ' + level + ' to the ID ' + id);
//            var element = $("#cloudtrail\\.regions\\.ap-southeast-1\\.trails\\.Default\\.IsLogging");
//            var element = document.getElementById("cloudtrail.regions.ap-southeast-1.trails.Default.IsLogging");
//            console.log('Element has value ' + element.text());
//            console.log(element);
//            element.addClass('finding-' + level);
            if ($('[id$="' + id + '"]').hasClass("badge")) {
                $('[id$="' + id + '"]').addClass('btn-' + level);
            } else {
                $('[id$="' + id + '"]').addClass('finding-' + level);
            }
        }
    }
/*
    for (i in violations) {
        var vkey = ''; 
        var read_macro_items = false;
        var vkey = violations[i]['keyword_prefix'] + '_' + violations[i]['entity'].split('.').pop() + '-' + i;
        violations_array[vkey] = new Array();
        if (violations[i]['macro_items'].length == violations[i]['items'].length ) {
            read_macro_items = true;
        }
        for (j in violations[i]['items']) {
            var id = vkey;
            if (read_macro_items) {
                id = id + '-' + violations[i]['macro_items'][j];
            }
            id = id + '-' + violations[i]['items'][j];
            if ($('[id$="' + id + '"]').hasClass("badge")) {
                $('[id$="' + id + '"]').addClass('btn-' + violations[i]['level']);
            } else {
                $('[id$="' + id + '"]').addClass('finding-' + violations[i]['level']);
            }
            if (read_macro_items) {
                violations_array[vkey].push(violations[i]['macro_items'][j]);
            } else {
                violations_array[vkey].push(violations[i]['items'][j]);
            }
        }
    }*/
    load_aws_config_from_json(violations, keyword + '_violation', 1);
}

// Generic list filters
function load_filters_from_json(list) {
    var id1 = '#filter-list-template';
    var id2 = '#filters-list';
    var compiler = Handlebars.compile($(id1).html());
    $(id2).append(compiler({items: list}));
}
function load_region_filters(keyword, list) {
    var id1 = '#region-filter-list-template';
    var id2 = '#region-filters-list';
    var compiler = Handlebars.compile($(id1).html());
    $(id2).append(compiler({items: list, keyword: keyword}));
    $('[id="' + keyword  + '_region-filter-select_all"]').hide();
}

// Display functions
function hideAll() {
    $("[id$='.row']").hide();
    $("dropdown\\.list").show();
    $("[id*='.list']").hide();
    $("[id*='.details']").hide();
//    $("[id*='.filter-']").hide();
}
function hideRowItems(keyword) {
    $("[id*='" + keyword + "-list']").hide();
    $("[id*='" + keyword + "-details']").hide();
}
function showEmptyRow(keyword) {
    id = '[id*="' + prefix + '_region-"]';
    $(id).show();
    id = "#" + keyword + "s-row";
    $(id).show();
    hideRowItems(keyword);
}
function showItem(keyword, id) {
    var id1 = '[id="' + keyword + '-list-' + id + '"]';
    var id2 = '[id="' + keyword + '-details-' + id+ '"]';
    $(id1).show();
    $(id2).show();
}
function hideItem(keyword, id) {
    var id1 = '[id="' + keyword + '-list-' + id + '"]';
    var id2 = '[id="' + keyword + '-details-' + id+ '"]';
    $(id1).hide();
    $(id2).hide();
}
function showRow(path) {
//    id = '[id*="' + prefix + '_region-"]';
    id = '[id="' + path + '-row"]';
    $(id).show();
//    id = "#" + keyword + "-row";
//    $(id).show();

     

}
function showRowWithDetails(keyword) {
    showRow(keyword);
    showAll(keyword);
}
function showAllNew(path) {
    $("[id^='" + path + "']").show();
}
function showAll(keyword) {
    prefix = keyword.split('_')[0];
    $("[id*='" + keyword + "-list']").show();
    $("[id*='" + keyword + "-details']").show();
    $("[id*='" + keyword + "-filter']").show();
    $("[id*='" + keyword + "-filtericon']").removeClass('glyphicon-check');
    $("[id*='" + keyword + "-filtericon']").addClass('glyphicon-unchecked');
    $("[id*='" + prefix + "_region-']").show();
    $("[id*='" + prefix + "_region-filtericon']").removeClass('glyphicon-unchecked');
    $("[id*='" + prefix + "_region-filtericon']").addClass('glyphicon-check');
}
function toggleDetails(keyword, item) {
    var id = '#' + keyword + '-' + item;
    $(id).toggle();
}

function updateNavbar(service) {
    $('[id*="_dropdown"]').removeClass('active-dropdown');
    $('#' + service + '_dropdown').addClass('active-dropdown');
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

// Contents loading
function load_config(service) {
    var info = {};
    $("#section_title-h2").text('');
    if (!(service in loaded_config_array)) {
//        hideAll();
        $('[id="please_wait-row"]').show();
        setTimeout(function(){
            if (service == 'cloudtrail') {
                load_aws_config_from_json(aws_info['services']['cloudtrail']['regions'], 'cloudtrail.trails', 2);
                highlight_violations(aws_info['services']['cloudtrail']['violations'], 'cloudtrail');
            }
            else if (service == 'ec2') {
                load_aws_config_from_json(aws_info['services']['ec2']['regions'], 'ec2_elb', 2);
                load_aws_config_from_json(aws_info['services']['ec2']['regions'], 'ec2_vpc', 2);
                load_aws_config_from_json(aws_info['services']['ec2']['regions'], 'ec2_security_group', 2);
                load_aws_config_from_json(aws_info['services']['ec2']['regions'], 'ec2_network_acl', 2);
                load_aws_config_from_json(aws_info['services']['ec2']['regions'], 'ec2_instance', 2);
                load_aws_config_from_json(aws_info['services']['ec2']['attack_surface'], 'ec2_attack_surface', 1);
                highlight_violations(aws_info['services']['ec2']['violations'], 'ec2');
                load_filters_from_json(aws_info['services']['ec2']['filters']);
            }
            else if (service == 'iam') {
                load_aws_config_from_json(aws_info['services']['iam']['Groups'], 'iam_Group', 2);
                load_aws_config_from_json(aws_info['services']['iam']['Permissions'], 'iam_Permission', 1);
                load_aws_config_from_json(aws_info['services']['iam']['Roles'], 'iam_Role', 2);
                load_aws_config_from_json(aws_info['services']['iam']['Users'], 'iam_User', 2);
                if ('CredentialReport' in aws_info['services']['iam']) {
                    load_aws_config_from_json(aws_info['services']['iam']['CredentialReport']['<root_account>'], 'iam_CredentialReport', 1);
                }
                load_aws_config_from_json(aws_info['services']['iam']['PasswordPolicy'], 'iam_PasswordPolicy', 1);
                highlight_violations(aws_info['services']['iam']['violations'], 'iam');
                load_filters_from_json(aws_info['services']['iam']['filters']);
            }
            else if (service == 'rds') {
                load_aws_config_from_json(aws_info['services']['rds']['regions'], 'rds_security_group', 2);
                load_aws_config_from_json(aws_info['services']['rds']['regions'], 'rds_instance', 2);
                highlight_violations(aws_info['services']['rds']['violations'], 'rds');
            }
            else if (service == 'redshift') {
                load_aws_config_from_json(aws_info['services']['redshift']['regions'], 'redshift_cluster', 2);
                load_aws_config_from_json(aws_info['services']['redshift']['regions'], 'redshift_security_group', 2);
                load_aws_config_from_json(aws_info['services']['redshift']['regions'], 'redshift_parameter_group', 2);
                highlight_violations(aws_info['services']['redshift']['violations'], 'redshift');
            }
            else if (service == 's3') {
                load_aws_config_from_json(aws_info['services']['s3']['buckets'], 's3_bucket', 2);
                highlight_violations(aws_info['services']['s3']['violations'], 's3');
            }
/*
            if ('regions' in aws_info['services'][service]) {
                load_region_filters(service, aws_info['services'][service]['regions']);
            }
*/
            $('[id="' + service + '_load_button"]').hide();
            $('[id="please_wait-row"]').hide();
            loaded_config_array.push(service);
        }, 50);
    }
}

// Set up dashboards and dropdown menus
function load_dashboards() {
    load_aws_config_from_json('about_run', 'about_run', 'about_run', 1);
    load_aws_config_from_json('services.violations', 'services', 1);
    load_aws_config_from_json('dropdown', 'metadata', 1);
    show_main_dashboard();
}

// Browsing functions
function about() {
    hideAll();
    $('#about-row').show();
    $('#section_title-h2').text('');
}
function show_main_dashboard() {
//    hideAll()
    $('#about_run-row').show();
    $('#section_title-h2').text('');
}

//if ("onhashchange" in window) {
//    alert("The browser supports the hashchange event!");
//}

function locationHashChanged() {
    myBrowse(location.hash);
}
window.onhashchange = locationHashChanged;

function myBrowse(anchor) {
    path = anchor.replace('#', '').split('/');
    var p1 = '';
    var p2 = '';
    // Hide all
    while (val1 = path.shift()) {
        val2 = path.shift();
        if (val2 == 'undefined') {
            break;
        }
        if (p1 == '') {
            p1 = val1 + '\\\/';
        } else {
            p1 = p1 + val1 + '\\\/';
        }
        p2 = p1 + val2 + '\\\/';
        $('div').filter("[id^='"+p1+"']").not("[id^='"+p2+"']").hide();
        p1 = p2;
    }
    // Show one
    $(document.getElementById(anchor.replace('#', ''))).show();
    // TODO: handle show all
    // Scroll to the top
    window.scrollTo(0,0);
}

function browseTo(keyword, id) {
    // Hide similar details
    $("[id*='" + keyword + "-details-']").hide();
    // Show the requested details
    $("[id='" + keyword + "-details-" + id + "']").show();
    // Scroll to the top
    window.scrollTo(0,0);
}

function list_generic(script_id, path, cols) {
    /* Load if not existing */
    if (!(script_id in loaded_config_array)) {
        setTimeout(function(){
            load_aws_config_from_json(script_id, path, cols);
        }, 50);
    }
    path_array = path.split('.');
    service = path_array[0];
    hideAll();
    updateNavbar(service);
/*
    // Show stuff
    if(path_array.lastIndexOf('metadata') > 0) {
        var element = document.getElementById('dashboard-row');
        if (element) { element.style.display = 'block' }
        var element = document.getElementById('dashboard-list');
        if (element) { element.style.display = 'block' }
    }
*/
    var element = document.getElementById(script_id + '.row');
    if (element) { element.style.display = 'block' }
    var element = document.getElementById(script_id + '.list');
    if (element) { element.style.display = 'block' }
    var element = document.getElementById(script_id + '.details');
    if (element) { element.style.display = 'block' }    
    for (var i=1;i<=path_array.length;i+=2) {
        var id=path_array.slice(0,i+1).join('.');
        var element = document.getElementById(id + '.row');
        if (element) { element.style.display = 'block' }
        var element = document.getElementById(id + '.list');
        if (element) { element.style.display = 'block' }
        var element = document.getElementById(id + '.details');
        if (element) { element.style.display = 'block' }
    }
//    showRowWithDetails(keyword);
//    prefix = keyword.split('_')[0];
//    $('[id="' + prefix  + '_region-filter-select_all"]').hide();
    partial_array = script_id.split('.');
    title = partial_array[1] + ' ' + partial_array[partial_array.length-1];
    title = title.replace(/_/g, ' ');
    title = title.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    title = title.replace("Cloudtrail","CloudTrail").replace("Ec2","EC2").replace("Iam","IAM").replace("Rds","RDS").replace("Elb", "ELB").replace("Acl","ACL");
    $("#section_title-h2").text(title);
    window.scrollTo(0,0);
}
function list_findings(service, finding_name) {
    updateNavbar(service);
//    hideAll();
//    showEmptyRow(service);
    $("#section_title-h2").text(aws_info['services'][service]['violations'][finding_name]['description']);
    return
    if (violations[finding]['macro_items'].length == violations[finding]['items'].length ) {
        items = [];
        dict  = {};
        for (mi in violations[finding]['macro_items']) {
            if (dict.hasOwnProperty(violations[finding]['macro_items'][mi])) {
                continue;
            }
            items.push(violations[finding]['macro_items'][mi]);
            dict[violations[finding]['macro_items'][mi]] = 1;
        }
    } else {
        items = violations[finding]['items'];
    }
    for (item in items) {
        showItem(keyword, items[item]);
    }
    window.scrollTo(0,0);
}

// Handlebars helpers
Handlebars.registerHelper('displayPolicy', function(blob) {
    // this fails now that the policies are all JSON... check in chrome though
    //policy = JSON.stringify(eval("(" + blob + ")"), null, 2);
    var policy = JSON.stringify(blob, null, 2);
    policy = policy.replace(/ /g, '&nbsp;');
    policy = policy.replace(/\n/g, '<br />');
    return policy;
});
Handlebars.registerHelper("has_profiles?", function(logins) {
    if(typeof logins != 'undefined' && logins != '') {
        return 'Yes';
    } else {
        return 'No';
    }
});
Handlebars.registerHelper('has_access_keys?', function(access_keys) {
    if (typeof access_keys != 'undefined' && access_keys != '') {
        return access_keys.length;
    } else {
        return 0;
    }
});
Handlebars.registerHelper('has_mfa?', function(mfa_devices) {
    if (typeof mfa_devices != 'undefined' && mfa_devices != '') {
        return 'Yes';
    } else {
        return 'No';
    }
});
Handlebars.registerHelper('list_permissions', function(permissions) {
    var r = '';
    if (typeof permissions != 'undefined' && permissions != '') {
        r += parse_entities('group', permissions.groups);
        r += parse_entities('role', permissions.roles);
        r += parse_entities('user', permissions.users);
    }
    return r;
});
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
Handlebars.registerHelper('s3_grant_2_icon', function(value) {
    return '<i class="' + ((value == true) ? 'glyphicon glyphicon-ok' : '') +'"></i>';
});
Handlebars.registerHelper('good_bad_icon', function(violation, bucket_name, item) {
    index = -1;
    /* TODO: this shouldn't happen in JS... will take forever on buckets that contain many files */
    for (i in aws_info['services']['s3']['violations'][violation]['macro_items']) {
        if (aws_info['services']['s3']['violations'][violation]['macro_items'][i] == bucket_name) {
            if (aws_info['services']['s3']['violations'][violation]['items'][i] == item) {
                index = i;
                break;
            }
        }
    }
    if (index > -1) {
        return '<i class="glyphicon glyphicon-remove"></i>';
    } else {
        var key_details = aws_info['services']['s3']['buckets'][bucket_name]['keys'][item];
        if (((violation == 'object-perms-mismatch-bucket-perms') && !('grantees' in key_details))
            ||((violation == 'unencrypted-s3-objects') && !('ServerSideEncryption' in key_details))) {
            /* Say that we don't know if there's no corresponding attribute for the key */
            return '<i class="glyphicon glyphicon-question-sign"></i>';
        } else {
            /* Mark as good */
            return '<i class="glyphicon glyphicon-ok finding-good"></i>';
        }
    }
});
Handlebars.registerHelper('has_logging?', function(logging) {
    return logging;
});
Handlebars.registerHelper('finding_entity', function(prefix, entity) {
    return finding_entity(prefix, entity);
});
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
Handlebars.registerHelper('friendly_name', function(entity) {
    return 'friendly_name';
    var name = entity.split('.').pop();
    name = name.replace('_', ' ');
    return name.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
});
Handlebars.registerHelper('count', function(items) {
    var c = 0;
    for (i in items) {
        c = c + 1;
    }
    return c;
});
Handlebars.registerHelper('count_in', function(service, path) {
    var entities = path.split('.');
    if (service == 'ec2') {
        var input = aws_info['services']['ec2'];
    } else if(service == 'cloudtrail') {
        var input = aws_info['services']['cloudtrail'];
    } else {
        return 0;
    }
    return recursive_count(input, entities);
});
Handlebars.registerHelper('count_ec2_in_region', function(region, path) {
    if (typeof aws_info['services']['ec2'] != 'undefined') {
        var count = 0;
        var entities = path.split('.');
        for (r in aws_info['services']['ec2']['regions']) {
            if (r == region) {
                return recursive_count(aws_info['services']['ec2']['regions'][r], entities);
            }
        }
    } else {
        count = 'N/A';
    }
    return count;
});
Handlebars.registerHelper('count_vpc_network_acls', function(vpc_network_acls) {
    var c = 0;
    for (x in vpc_network_acls) {
            c = c + 1;
    }
    return c;
});
Handlebars.registerHelper('count_vpc_instances', function(vpc_instances) {
    var c = 0;
    for (x in vpc_instances) {
            c = c + 1;
    }
    return c;
});
Handlebars.registerHelper('count_role_instances', function(instance_profiles) {
    var c = 0;
    for (ip in instance_profiles) {
        for (i in instance_profiles[ip]['instances']) {
            c = c + 1;
        }
    }
    return c;
});
var recursive_count = function(input, entities) {
    var count = 0;
    if (entities.length > 0) {
        var entity = entities.shift();
        for (i in input[entity]) {
            count = count + recursive_count(input[entity][i], eval(JSON.stringify(entities)));
        }
    } else {
        count = count + 1;
    }
    return count;
}
Handlebars.registerHelper('find_ec2_object_attribute', function(path, id, attribute ) {
    return findEC2ObjectAttribute(aws_info['services']['ec2'], path, id, attribute);
});
Handlebars.registerHelper('format_date', function(timestamp) {
    return new Date(timestamp * 1000).toString();
});
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
Handlebars.registerHelper('make_title', function(title) {
    return make_title(title);
});
Handlebars.registerHelper('addMember', function(member_name, value) {
    this[member_name] = value;
});
Handlebars.registerHelper('ifShow', function(v1, v2, options) {
  if(v1 !== v2) {
    return options.fn(this);
  }
});
Handlebars.registerHelper('fixBucketName', function(bucket_name) {
    if (bucket_name != undefined) {
        return bucket_name.replace(/\./g, '-');
    }
});
// http://funkjedi.com/technology/412-every-nth-item-in-handlebars, slightly tweaked to work with a dictionary
Handlebars.registerHelper('grouped_each', function(every, context, options) {
    var out = "", subcontext = [], i;
    var keys = Object.keys(context);
    var count = keys.length;
    var subcontext = {};
    if (context && count > 0) {
        for (i = 0; i < count; i++) {
            if (i > 0 && i % every === 0) {
                out += options.fn(subcontext);
                subcontext = {};
            }
            subcontext[keys[i]] = context[keys[i]];
        }
        out += options.fn(subcontext);
    }
    return out;
});
Handlebars.registerHelper('dashboard_color', function(level, checked, flagged) {
    if (checked == 0) {
        return 'unknown disabled-link';
    } else if (flagged == 0) {
        return 'good disabled-link';
    } else {
        return level;
    }
});
Handlebars.registerHelper('policy_friendly_name', function(arn) {
    return policy_friendly_name(arn);
});
var policy_friendly_name = function(arn) {
    return arn.split(':policy/').pop();
}
Handlebars.registerHelper('policy_report_id', function(policy, a, b, c) {
    policy['ReportId'] = a + '-' + b + '-' + c;
});
Handlebars.registerHelper('ifEqual', function(v1, v2, options) {
    if (v1 === v2) {
        return options.fn(this);
    } else {
        return options.inverse(this);
    }
});
Handlebars.registerHelper('has_condition', function(policy_info) {
    if (('condition' in policy_info) && (policy_info['condition'] != null)) {
        return true;
    } else {
        return false;
    }
});
Handlebars.registerHelper('escape_special_chars', function(value) {
    return value.replace(/\./g, 'nccdot').replace(/,/g, 'ncccoma');
});
