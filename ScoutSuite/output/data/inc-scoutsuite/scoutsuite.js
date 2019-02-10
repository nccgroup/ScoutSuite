// Globals
var loaded_config_array = new Array();
var run_results;

const DARK_BOOTSTRAP_THEME = "inc-bootstrap/css/bootstrap-dark.min.css";
const LIGHT_BOOTSTRAP_THEME = "inc-bootstrap/css/bootstrap-light.min.css";

const DARK_SCOUT_THEME = "inc-scoutsuite/css/scoutsuite-dark.css";
const LIGHT_SCOUT_THEME = "inc-scoutsuite/css/scoutsuite-light.css";

/**
 * Event handlers
 */
$(document).ready(function () {
    // Loading last theme before window.onload to prevent flickering of styles    
    if (localStorage.getItem("theme_checkbox") == "true") {
        document.getElementById("theme_checkbox").checked = true;
        setBootstrapTheme(DARK_BOOTSTRAP_THEME);
        setScoutTheme(DARK_SCOUT_THEME);
    }

    showPageFromHash();

    // when button is clicked, return CSV with finding
    $('#findings_download_button').click(function (event) {

        var button_clicked = event.target.id;

        var anchor = window.location.hash.substr(1);
        // Strip the # sign
        var path = decodeURIComponent(anchor.replace('#', ''));
        // Get resource path based on browsed-to path
        var resource_path = get_resource_path(path);

        var csv_array = [];
        var json_dict = {};

        var items = get_value_at(path);
        var level = get_value_at(path.replace('items', 'level'));
        var resource_path_array = resource_path.split('.');
        var split_path = path.split('.');
        var finding_service = split_path[1];
        var finding_key = split_path[split_path.length - 2];

        if (button_clicked == 'findings_download_csv_button') {
            var first_entry = 1;
            for (item in items) {
                // get item value
                // when path ends in '.items' (findings)
                if (typeof items[item] === 'string') {
                    var id_array = items[item].split('.');
                    var id = 'services.' + id_array.slice(0, resource_path_array.length).join('.');
                    var i = get_value_at(id)
                }
                // all other cases
                else {
                    var i = items[item];
                };
                ;
                // for first item, put keys at beginning of csv
                if (first_entry == 1) {
                    var key_values_array = []
                    Object.keys(i).forEach(function (key) {
                        key_values_array.push(key);
                    });
                    csv_array.push(key_values_array);
                };
                // put each value in array
                var values_array = []
                Object.keys(i).forEach(function (key) {
                    values_array.push(JSON.stringify(i[key]).replace(/^"(.*)"$/, '$1'));
                });
                // append to csv array
                csv_array.push(values_array);
                first_entry = 0;
            };

            download_as_csv(finding_key + '.csv', csv_array)
        };
        ;

        if (button_clicked == 'findings_download_json_button') {
            json_dict['items'] = [];
            for (item in items) {
                // get item value
                // when path ends in '.items' (findings)
                if (typeof items[item] === 'string') {
                    var id_array = items[item].split('.');
                    var id = 'services.' + id_array.slice(0, resource_path_array.length).join('.');
                    var i = get_value_at(id)
                }
                // all other cases
                else {
                    var i = items[item];
                };
                ;
                // add item to json
                json_dict['items'].push(i);
            };
            download_as_json(finding_key + '.json', json_dict);
        };

    });

});

/**
 * Display the account ID -- use of the generic function + templates result in the div not being at the top of the page
 */
var load_aws_account_id = function () {
    var element = document.getElementById('aws_account_id');
    var value = '<i class="fa fa-cloud"></i> ' + run_results['provider_name'] +
        ' <i class="fa fa-chevron-right"></i> ' + run_results['aws_account_id'];
    if (('organization' in run_results) && (value in run_results['organization'])) {
        value += ' (' + run_results['organization'][value]['Name'] + ')'
    };
    element.innerHTML = value;
};

/**
 * Generic load JSON function
 * @param script_id
 * @param cols
 * @returns {number};
 */
function load_aws_config_from_json(script_id, cols) {

    // Abort if data was previously loaded
    if (loaded_config_array.indexOf(script_id) > 0) {
        // When the path does not contain .id.
        return 0
    };
    path_array = script_id.split('.');
    for (i = 3; i < path_array.length; i = i + 2) {
        path_array[i] = 'id';
    };
    fixed_path = path_array.join('.');
    if (loaded_config_array.indexOf(fixed_path) > 0) {
        // When the loaded path contains id but browsed-to path contains a specific value
        return 0
    };
    path_array[1] = 'id';
    fixed_path = path_array.join('.');
    if (loaded_config_array.indexOf(fixed_path) > 0) {
        // Special case for services.id.findings
        return 0
    };

    // Build the list based on the path, stopping at the first .id. value
    list = run_results;
    path_array = script_id.split('.id.')[0].split('.');
    for (i in path_array) {
        // Allows for creation of regions-filter etc...
        if (i.endsWith('-filters')) {
            i = i.replace('-filters', '');
        };
        list = list[path_array[i]];
    };

    // Filters
    if (path_array[i] == 'items' && i > 3 && path_array[i - 2] == 'filters') {
        return 1;
    };

    // Default # of columns is 2
    if ((cols === undefined) || (cols === null)) {
        cols = 2;
    };

    // Update the DOM
    hideAll();
    if (cols == 0) {
        // Metadata
        script_id = script_id.replace('services.id.', '');
        process_template(script_id + '.list.template', script_id + '.list', list);
    } else if (cols == 1) {
        // Single-column display
        process_template(script_id + '.details.template', 'single-column', list);
    } else if (cols == 2) {
        // Double-column display
        process_template(script_id + '.list.template', 'double-column-left', list);
        process_template(script_id + '.details.template', 'double-column-right', list);
    };

    // Update the list of loaded data
    loaded_config_array.push(script_id);
    return 1;
};


/**
 * Compile Handlebars templates and update the DOM
 * @param id1
 * @param container_id
 * @param list
 */
function process_template(id1, container_id, list) {
    id1 = id1.replace(/<|>/g, '');
    var template_to_compile = document.getElementById(id1).innerHTML;
    var compiled_template = Handlebars.compile(template_to_compile);
    var inner_html = compiled_template({items: list});
    document.getElementById(container_id).innerHTML += inner_html;
};

/**
 * Hide all lists and details
 */
function hideAll() {
    $("[id*='.list']").not("[id*='metadata.list']").not("[id='regions.list']").not("[id*='filters.list']").hide();
    $("[id*='.details']").hide();
    var element = document.getElementById('scout2_display_account_id_on_all_pages');
    if ((element != undefined) && (element.checked == true)) {
        showRow('aws_account_id');
    };
    current_resource_path = ''
};


/**
 * Show list and details' container for a given path
 * @param path
 */
function showRow(path) {
    path = path.replace(/.id./g, '\.[^.]+\.');
    showList(path);
    showDetails(path);
};

function showList(path) {
    $('div').filter(function () {
        return this.id.match(path + '.list')
    }).show();
}

function showDetails(path) {
    $('div').filter(function () {
        return this.id.match(path + '.details')
    }).show();
}

function hideList(path) {
    $("[id='" + path + "']").hide();
    path = path.replace('.list', '');
    hideItems(path);
};


/**
 * Show links and views for a given path
 * @param path
 */
function showItems(path) {
    path = path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.';
    $('div').filter(function () {
        return this.id.match(path + 'link')
    }).show();
    $('div').filter(function () {
        return this.id.match(path + 'view')
    }).show();
};


/**
 * Hide resource views for a given path
 * @param resource_path
 */
function hideItems(resource_path) {
    path = resource_path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.view';
    $('div').filter(function () {
        return this.id.match(path)
    }).hide();
};


/**
 * Hide resource links for a given path
 * @param resource_path
 */
function hideLinks(resource_path) {
    // TODO: Handle Region and VPC hiding...
    path = resource_path.replace(/.id./g, '\.[^.]+\.') + '\.[^.]+\.link';
    $('div').filter(function () {
        return this.id.match(path)
    }).hide();
};


/**
 * Show list, details' container, links, and view for a given path
 * @param path
 */
function showRowWithItems(path) {
    showRow(path);
    showItems(path);
};


function showFilters(resource_path) {
    hideFilters();
    service = resource_path.split('.')[1];
    // Show service filters
    $('[id="' + resource_path + '.id.filters"]').show();
    // show region filters
    $('[id*="regionfilters.' + service + '.regions"]').show();
};

function hideFilters() {
    $('[id*=".id.filters"]').hide();
    $('[id*="regionfilters"]').hide();
    // Reset dashboard filters
    $(".dashboard-filter").val("");
    $(".finding_items").filter(function () {
        $(this).show()
    });
};

/**
 * Show findings
 * @param path
 * @param resource_path
 */
function showFindings(path, resource_path) {
    items = get_value_at(path);
    level = get_value_at(path.replace('items', 'level'));
    resource_path_array = resource_path.split('.');
    split_path = path.split('.');
    finding_service = split_path[1];
    finding_key = split_path[split_path.length - 2];
    for (item in items) {
        var id_array = items[item].split('.');
        var id = 'services.' + id_array.slice(0, resource_path_array.length).join('.');
        showSingleItem(id);
        if ($('[id="' + items[item] + '"]').hasClass('badge')) {
            $('[id="' + items[item] + '"]').addClass('finding-title-' + level);
        } else {
            $('[id="' + items[item] + '"]').addClass('finding-' + level);
        };
        $('[id="' + items[item] + '"]').removeClass('finding-hidden');
        $('[id="' + items[item] + '"]').attr('data-finding-service', finding_service);
        $('[id="' + items[item] + '"]').attr('data-finding-key', finding_key);
        $('[id="' + items[item] + '"]').click(function (e) {
            finding_id = e.target.id;
            if (!(finding_service in exceptions)) {
                exceptions[finding_service] = new Object();
            };
            if (!(finding_key in exceptions[finding_service])) {
                exceptions[finding_service][finding_key] = new Array();
            };
            is_exception = confirm('Mark this item as an exception ?');
            if (is_exception && (exceptions[finding_service][finding_key].indexOf(finding_id) == -1)) {
                exceptions[finding_service][finding_key].push(finding_id);
            };
        });
    };
};

/**
 * Show a single item
 * @param id
 */
function showSingleItem(id) {
    if (!id.endsWith('.view')) {
        id = id + '.view';
    };
    $("[id='" + id + "']").show();
    id = id.replace('.view', '.link');
    $("[id='" + id + "']").show();
};

/**
 * Toggles between light and dark themes
 */
function toggleTheme() {
    if (document.getElementById("theme_checkbox").checked) {
        this.setBootstrapTheme(DARK_BOOTSTRAP_THEME)
        this.setScoutTheme(DARK_SCOUT_THEME)
    }
    else {
        this.setBootstrapTheme(LIGHT_BOOTSTRAP_THEME)
        this.setScoutTheme(LIGHT_SCOUT_THEME)
    }
};

/**
 * Sets the css file location received as the bootstrap theme
 * @param file
 */
function setBootstrapTheme(file) {
    var oldlink = document.getElementById("bootstrap-theme");
    oldlink.href = file;
}

/**
 * Sets the css file location received as the scout theme
 * @param file
 */
function setScoutTheme(file) {
    var oldlink = document.getElementById("scout-theme");
    oldlink.href = file;
}


/**
 * Save the current theme on web storage
 */
window.onunload = function() {
    localStorage.setItem("theme_checkbox", document.getElementById("theme_checkbox").checked);
}

/**
 *
 * @param data
 * @param entities
 * @param callback
 * @param callback_args
 */
function iterateEC2ObjectsAndCall(data, entities, callback, callback_args) {
    if (entities.length > 0) {
        var entity = entities.shift();
        var recurse = entities.length;
        for (i in data[entity]) {
            if (recurse) {
                iterateEC2ObjectsAndCall(data[entity][i], eval(JSON.stringify(entities)), callback, callback_args);
            } else {
                callback(data[entity][i], callback_args);
            };
        };
    };
};

/**
 *
 * @param ec2_data
 * @param entities
 * @param id
 * @returns {*}
 */
function findEC2Object(ec2_data, entities, id) {
    if (entities.length > 0) {
        var entity = entities.shift();
        var recurse = entities.length;
        for (i in ec2_data[entity]) {
            if (recurse) {
                var object = findEC2Object(ec2_data[entity][i], eval(JSON.stringify(entities)), id);
                if (object) {
                    return object;
                };
            } else if (i == id) {
                return ec2_data[entity][i];
            };
        };
    };
    return '';
};

/**
 *
 * @param ec2_data
 * @param entities
 * @param attributes
 * @returns {*}
 */
function findEC2ObjectByAttr(ec2_data, entities, attributes) {
    if (entities.length > 0) {
        var entity = entities.shift();
        var recurse = entities.length;
        for (i in ec2_data[entity]) {
            if (recurse) {
                var object = findEC2ObjectByAttr(ec2_data[entity][i], eval(JSON.stringify(entities)), attributes);
                if (object) {
                    return object;
                };
            } else {
                var found = true;
                for (attr in attributes) {
                    // h4ck :: EC2 security groups in RDS are lowercased...
                    if (ec2_data[entity][i][attr].toLowerCase() != attributes[attr].toLowerCase()) {
                        found = false;
                    };
                };
                if (found) {
                    return ec2_data[entity][i];
                };
            };
        };
    };
    return '';
};

/**
 *
 * @param ec2_info
 * @param path
 * @param id
 * @param attribute
 * @returns {*}
 */
function findEC2ObjectAttribute(ec2_info, path, id, attribute) {
    var entities = path.split('.');
    var object = findEC2Object(ec2_info, entities, id);
    if (object[attribute]) {
        return object[attribute];
    };
    return '';
};

/**
 *
 * @param path
 * @param id
 */
function findAndShowEC2Object(path, id) {
    entities = path.split('.');
    var object = findEC2Object(run_results['services']['ec2'], entities, id);
    var etype = entities.pop();
    if (etype == 'instances') {
        showPopup(single_ec2_instance_template(object));
    } else if (etype == 'security_groups') {
        showPopup(single_ec2_security_group_template(object));
    } else if (etype == 'vpcs') {
        showPopup(single_vpc_template(object));
    } else if (etype == 'network_acls') {
        object['name'] = id;
        showPopup(single_vpc_network_acl_template(object));
    };
    
};

/**
 *
 * @param path
 * @param attributes
 */
function findAndShowEC2ObjectByAttr(path, attributes) {
    entities = path.split('.');
    var object = findEC2ObjectByAttr(run_results['services']['ec2'], entities, attributes);
    var etype = entities.pop();
    if (etype == 'security_groups') {
        showPopup(single_ec2_security_group_template(object));
    };
};

/**
 *
 * @param data
 */
function showEC2Instance2(data) {
    showPopup(single_ec2_instance_template(data));
};

/**
 *
 * @param region
 * @param vpc
 * @param id
 */
function showEC2Instance(region, vpc, id) {
    var data = run_results['services']['ec2']['regions'][region]['vpcs'][vpc]['instances'][id];
    showPopup(single_ec2_instance_template(data));
};

/**
 *
 * @param region
 * @param vpc
 * @param id
 */
function showEC2SecurityGroup(region, vpc, id) {
    var data = run_results['services']['ec2']['regions'][region]['vpcs'][vpc]['security_groups'][id];
    showPopup(single_ec2_security_group_template(data));
};

/**
 *
 */
function showObject(path, attr_name, attr_value) {
    const path_array = path.split('.');
    const path_length = path_array.length;
    let data = getResource(path);

    // Adds the resource path values to the data context
    for (let i = 0; i < path_length - 1; i += 2) {
        if (i + 1 >= path_length) break;

        const attribute = makeResourceTypeSingular(path_array[i]);
        data[attribute] = path_array[i + 1];
    }

    // Filter if ...
    let resource_type;
    if (attr_name && attr_value) {
        for (const resource in data) {
            if (data[resource][attr_name] !== attr_value) continue;
            data = data[resource];
            break;
        };

        resource_type = path_array[1] + '_' + path_array[path_length - 1];
    } else {
        resource_type = path_array[1] + '_' + path_array[path_length - 2];
    };

    resource = makeResourceTypeSingular(resource_type);
    template = 'single_' + resource + '_template';
    showPopup(window[template](data));
};

/**
 * Gets a resource from the run results.
 * @param {string} path 
 */
function getResource(path) {
    let data = run_results;
    for (const attribute of path.split('.')) {
        data = data[attribute];
    };

    return data;
}

/**
 * Makes the resource type singular.
 * @param {string} resource_type 
 */
function makeResourceTypeSingular(resource_type) {
    return resource_type.substring(0, resource_type.length - 1).replace(/\.?ie$/, "y");
}

/**
 *
 * @param policy_id
 */
function showIAMManagedPolicy(policy_id) {
    var data = run_results['services']['iam']['policies'][policy_id];
    data['policy_id'] = policy_id;
    showIAMPolicy(data);
};

/**
 *
 * @param iam_entity_type
 * @param iam_entity_name
 * @param policy_id
 */
function showIAMInlinePolicy(iam_entity_type, iam_entity_name, policy_id) {
    var data = run_results['services']['iam'][iam_entity_type][iam_entity_name]['inline_policies'][policy_id];
    data['policy_id'] = policy_id;
    showIAMPolicy(data);
};

/**
 *
 * @param data
 */
function showIAMPolicy(data) {
    showPopup(single_iam_policy_template(data));
    var id = '#iam_policy_details-' + data['report_id'];
    $(id).toggle();
};

/**
 *
 * @param bucket_name
 */
function showS3Bucket(bucket_name) {
    var data = run_results['services']['s3']['buckets'][bucket_name];
    showPopup(single_s3_bucket_template(data));
};

/**
 *
 * @param bucket_id
 * @param key_id
 */
function showS3Object(bucket_id, key_id) {
    var data = run_results['services']['s3']['buckets'][bucket_id]['keys'][key_id];
    data['key_id'] = key_id;
    data['bucket_id'] = bucket_id;
    showPopup(single_s3_object_template(data));
};

/**
 *
 */
function showPopup(content) {
    $('#modal-container').html(content);
    $('#modal-container').modal();
};

/**
 * Set up dashboards and dropdown menus
 */
function load_metadata() {

    run_results = get_scoutsuite_results();

    // Set title dynamically
    $(function(){
        3
        $(document).attr("title", 'Scout Suite Report [' + run_results['aws_account_id'] + ']');
        4
    });

    load_aws_account_id();
    load_aws_config_from_json('last_run', 1);
    load_aws_config_from_json('metadata', 0);
    load_aws_config_from_json('services.id.findings', 1);
    load_aws_config_from_json('services.id.filters', 0); // service-specific filters
    load_aws_config_from_json('services.id.regions', 0); // region filters

    for (group in run_results['metadata']) {
        for (service in run_results['metadata'][group]) {
            if (service == 'summaries') {
                continue;
            };
            for (section in run_results['metadata'][group][service]) {
                for (resource_type in run_results['metadata'][group][service][section]) {
                    add_templates(group, service, section, resource_type,
                        run_results['metadata'][group][service][section][resource_type]['path'],
                        run_results['metadata'][group][service][section][resource_type]['cols']);
                };
            };
        };
    };
};


////////////////////////
// Browsing functions //
////////////////////////


/**
 * Show About Scout Suite div
 */
function showAbout() {
    $('#modal-container').html(about_scoutsuite_template());
    $('#modal-container').modal();
};


/**
 * 
 */
function showLastRunDetails() {
    $('#modal-container').html(last_run_details_template(run_results));
    $('#modal-container').modal();
}

/**
 * Show main dashboard
 */
function show_main_dashboard() {
    hideAll();
    // Hide filters
    hideFilters();
    $('#findings_download_button').hide();
    showRowWithItems('aws_account_id');
    showRowWithItems('last_run');
    $('#section_title-h2').text('');
    // Remove URL hash
    history.pushState("", document.title, window.location.pathname + window.location.search);
};

/**
 * Make title from resource path
 * @param resource_path
 * @returns {string};
 */
function makeTitle(resource_path) {
    resource_path = resource_path.replace('service_groups.', '');
    service = getService(resource_path);
    resource = resource_path.split('.').pop();
    resource = resource.replace(/_/g, ' ').replace('<', '').replace('>',
        '').replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    }).replace("Acl", "ACL").replace("Findings", "Dashboard");
    return service + ' ' + resource;
};

/**
 *
 * @param resource_path
 * @returns {string}
 */
function getService(resource_path) {
    if (resource_path.startsWith('services')) {
        service = resource_path.split('.')[1];
    } else {
        service = resource_path.split('.')[0];
    };
    service = make_title(service);
    return service;
};

/**
 * Update title div's contents
 * @param title
 */
function updateTitle(title) {
    $("#section_title-h2").text(title);
};


/**
 * Update the DOM
 */
function showPageFromHash() {
    if (location.hash) {
        updateDOM(location.hash);
    } else {
        updateDOM('');
    };
};

window.onhashchange = showPageFromHash;

/**
 * Get value at given path
 * @param path
 * @returns {*};
 */
function get_value_at(path) {
    path_array = path.split('.');
    value = run_results;
    for (p in path_array) {
        try {
            value = value[path_array[p]];
        } catch (err) {
            console.log(err);
        };
    };
    return value;
};

var current_service_group = ''
var current_resource_path = ''

/**
 *
 * @param anchor
 */
function updateDOM(anchor) {

    // Strip the # sign
    var path = decodeURIComponent(anchor.replace('#', ''));

    // Get resource path based on browsed-to path
    var resource_path = get_resource_path(path);

    // Sub navbar..
    $("*[id^='groups.']").hide();
    if (path.startsWith('groups.')) {
        id = '#metadata\\.' + current_service_group;
        $(id).removeClass('active-dropdown');
        current_service_group = path.replace('groups\.', '').replace('.list', '');
        id = '#metadata\\.' + current_service_group;
        $(id).addClass('active-dropdown');
        id = '#groups\\.' + current_service_group + '\\.list';
        $(id).show();
        return;
    };

    // FIXME this is not a very good implementation
    if (!path.endsWith('.findings') &&
        !path.endsWith('.statistics') &&
        !path.endsWith('.password_policy') &&
        !path.endsWith('.permissions') &&
        !path.endsWith('.<root_account>') &&
        !path.endsWith('.external_attack_surface')) {
        $('#findings_download_button').show();
    } else {
        $('#findings_download_button').hide();
    };

    // Update title
    if (path.endsWith('.items')) {
        title = get_value_at(path.replace('items', 'description'));
        updateTitle(title);
    } else {
        title = makeTitle(resource_path);
        updateTitle(title);
    };

    // Clear findings highlighting
    $('span').removeClass('finding-danger');
    $('span').removeClass('finding-warning');

    // DOM Update
    if (path == '') {
        show_main_dashboard()
    } else if (path.endsWith('.items')) {
        // Switch view for findings
        lazy_loading(resource_path);
        hideAll();
        hideItems(resource_path);
        hideLinks(resource_path);
        showRow(resource_path);
        showFindings(path, resource_path);
        current_resource_path = resource_path;
        showFilters(resource_path);
    } else if (lazy_loading(resource_path) == 0) {
        // 0 is returned when the data was already loaded, a DOM update is necessary then
        if (path.endsWith('.view')) {
            // Same details, one item
            hideItems(current_resource_path);
            showSingleItem(path);
        } else if (current_resource_path != '' && resource_path.match(current_resource_path.replace(/.id./g, '\.[^.]+\.'))) {
            // Same details, multiple items
            hideItems(current_resource_path);
            showItems(path);
        } else {
            // Switch view for resources
            hideAll();
            showRowWithItems(resource_path);
            showFilters(resource_path);
            current_resource_path = resource_path;
        };
        // TODO: Highlight all findings...

    } else {
        // The DOM was updated by the lazy loading function, save the current resource path
        showFilters(resource_path);
        current_resource_path = resource_path;
    };

    // Scroll to the top
    window.scrollTo(0, 0);
};


/**
 *
 * @param path
 * @returns {number};
 */
// TODO: merge into load_aws_config_from_json...
function lazy_loading(path) {
    var cols = 1;
    var resource_path_array = path.split('.')
    var service = resource_path_array[1];
    var resource_type = resource_path_array[resource_path_array.length - 1];
    for (group in run_results['metadata']) {
        if (service in run_results['metadata'][group]) {
            if (service == 'summaries') {
                continue;
            };
            if (resource_type in run_results['metadata'][group][service]['resources']) {
                var cols = run_results['metadata'][group][service]['resources'][resource_type]['cols'];
            };
            break
        };
    };
    return load_aws_config_from_json(path, cols);
};


/**
 * Get the resource path based on a given path
 * @param path
 * @returns {*|string};
 */
function get_resource_path(path) {
    if (path.endsWith('.items')) {
        var resource_path = get_value_at(path.replace('items', 'display_path'));
        if (resource_path == undefined) {
            resource_path = get_value_at(path.replace('items', 'path'));
        };
        resource_path_array = resource_path.split('.');
        last_value = resource_path_array.pop();
        resource_path = 'services.' + resource_path_array.join('.');
    } else if (path.endsWith('.view')) {
        // Resource path is not changed (this may break when using `back' button in browser)
        var resource_path = current_resource_path;
    } else {
        var resource_path = path; 
    };
    return resource_path;
};


/**
 * Format title
 * @param title
 * @returns {string};
 */
function make_title (title) {
    if (typeof(title) != "string") {
        console.log("Error: received title " + title + " (string expected).");
        return title.toString();
    };
    title = title.toLowerCase();
    if (['ec2', 'efs', 'iam', 'kms', 'rds', 'sns', 'ses', 'sqs', 'vpc', 'elb', 'elbv2', 'emr'].indexOf(title) != -1) {
        return title.toUpperCase();
    } else if (title == 'cloudtrail') {
        return 'CloudTrail';
    } else if (title == 'cloudwatch') {
        return 'CloudWatch';
    } else if (title == 'cloudformation') {
        return 'CloudFormation';
    } else if (title == 'awslambda') {
        return 'Lambda';
    } else if (title == 'elasticache') {
        return 'ElastiCache';
    } else if (title == 'redshift') {
        return 'RedShift';
    } else if (title == 'cloudstorage') {

        return 'Cloud Storage';
    } else if (title == 'cloudsql') {
        return 'Cloud SQL';
    } else if (title == 'stackdriverlogging') {
        return 'Stackdriver Logging';
    } else if (title == 'stackdrivermonitoring') {
        return 'Stackdriver Monitoring';
    } else if (title == 'computeengine') {
        return 'Compute Engine';
    } else if (title == 'kubernetesengine') {
        return 'Kubernetes Engine';
    } else if (title == 'cloudresourcemanager') {
        return 'Cloud Resource Manager';
    } else if (title == 'storageaccounts') {
        return 'Storage Accounts';
    } else if (title == 'monitor') {
        return 'Monitor';
    } else if (title == 'sqldatabase') {
        return 'SQL Database';
    } else {
        return (title.charAt(0).toUpperCase() + title.substr(1).toLowerCase()).replace('_', ' ');
    };
};

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
    if (cols == undefined) {
        cols = 2;
    };
    add_template(group, service, section, resource_type, path, 'details');
    if (cols > 1) {
        add_template(group, service, section, resource_type, path, 'list');
    };
};

/**
 * Add resource templates
 * @param group
 * @param service
 * @param section
 * @param resource_type
 * @param path
 * @param suffix
 */
function add_template(group, service, section, resource_type, path, suffix) {
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
            };
        } else if (suffix == 'details') {
            if (path.indexOf('.vpcs.id.') > 0) {
                partial_name = 'details_for_vpc';
            } else if (path.indexOf('.regions.id.') > 0) {
                partial_name = 'details_for_region';
            } else {
                partial_name = 'details';
            };
        } else {
            console.log('Invalid suffix (' + suffix + ') for resources template.');
        };
        template.innerHTML = "{{> " + partial_name + " service_group = '" + group + "' service_name = '" + service + "' resource_type = '" + resource_type + "' partial_name = '" + path + "'}}";
        $('body').append(template);
    };
};

/**
 * Rules generator
 * @param group
 * @param service
 */
function filter_rules(group, service) {
    if (service == undefined) {
        $("[id*='rule-']").show();
    } else {
        $("[id*='rule-']").not("[id*='rule-" + service + "']").hide();
        $("[id*='rule-" + service + "']").show();
    };
    var id = "groups." + group + ".list";
    $("[id='" + id + "']").hide();
};

function download_configuration(configuration, name, prefix) {

    var uriContent = "data:text/json;charset=utf-8," + encodeURIComponent(prefix + JSON.stringify(configuration, null, 4));
    var dlAnchorElem = document.getElementById('downloadAnchorElem');
    dlAnchorElem.setAttribute("href", uriContent);
    dlAnchorElem.setAttribute("download", name + '.json');
    dlAnchorElem.click();
};

function download_exceptions() {
    var url = window.location.pathname;
    var profile_name = url.substring(url.lastIndexOf('/') + 1).replace('report-', '').replace('.html', '');
    console.log(exceptions);
    download_configuration(exceptions, 'exceptions-' + profile_name, 'exceptions = \n');
};

function set_filter_url(region) {
    tmp = location.hash.split('.');
    tmp[3] = region;
    location.hash = tmp.join('.');
};

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
function download_as_csv(filename, rows) {
    var processRow = function (row) {
        var finalVal = '';
        for (var j = 0; j < row.length; j++) {
            var innerValue = row[j] === null ? '' : row[j].toString();
            if (row[j] instanceof Date) {
                innerValue = row[j].toLocaleString();
            };
            ;
            var result = innerValue.replace(/"/g, '""');
            if (result.search(/("|,|\n)/g) >= 0)
                result = '"' + result + '"';
            if (j > 0)
                finalVal += ',';
            finalVal += result;
        };
        return finalVal + '\n';
    };

    var csvFile = '';
    for (var i = 0; i < rows.length; i++) {
        csvFile += processRow(rows[i]);
    };

    var blob = new Blob([csvFile], {type: 'text/csv;charset=utf-8;'});
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, filename);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        };
    };
};

function download_as_json(filename, dict) {

    var json_str = JSON.stringify(dict);

    var blob = new Blob([json_str], {type: 'application/json;'});
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, filename);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        };
    };
}