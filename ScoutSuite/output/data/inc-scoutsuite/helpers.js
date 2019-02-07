
////////////////////////
// Handlebars helpers //
////////////////////////

Handlebars.registerHelper('displayPolicy', function(blob) {
    var policy = '{<br/>';
    for (attr in blob) {
        if (attr == 'Statement') {
            policy += '&nbsp;&nbsp;"Statement": [<br/>';
            for (sid in blob['Statement']) {
                policy += '<span id="foobar">' + JSON.stringify(blob['Statement'][sid], null, 2) + '</span>,\n';
            }
            policy += '  ]';
        } else {
            policy += '  "' + attr + '": ' + JSON.stringify(blob[attr], null, 2);
        }
        policy += ',\n';
        
    }
    policy += '}';
    return policy;
});

Handlebars.registerHelper('add_policy_path', function() {
    var policy = arguments[0];
    var path = arguments[1];
    for (var i = 2; i < arguments.length -1; i++) {
        path = path + '\\.' + arguments[i];
    }
    policy['policy_path'] = path;
    policy['policy_spath'] = path.replace(/\\/g, '');
});

Handlebars.registerHelper('displayKey', function(key_name, blob) {
    var key = JSON.stringify(blob, null, 2);
    key = key.replace(/ /g, '&nbsp;');
    key = key.replace(/\n/g, '<br/>');
    return key;
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

Handlebars.registerHelper('s3_grant_2_icon', function(value) {
    return '<i class="' + ((value == true) ? 'fa fa-check' : '') +'"></i>';
});

Handlebars.registerHelper('good_bad_icon', function(finding, bucket_id, key_id, suffix) {
    var key_path = 's3.buckets.' + bucket_id + '.keys.' + key_id + '.' + suffix;
    var index = run_results['services']['s3']['findings'][finding]['items'].indexOf(key_path);
    var level = run_results['services']['s3']['findings'][finding]['level'];
    if (index > -1) {
        return '<i class="fa fa-times finding-' + level +'"></i>';
    } else {
        var key_details = run_results['services']['s3']['buckets'][bucket_id]['keys'][key_id];
        if ((finding == 's3-object-acls-mismatch-bucket') && ('grantees' in key_details)) {
            return '<i class="fa fa-check finding-good"></i>';
        } else if ((finding == 's3-object-unencrypted') && ('ServerSideEncryption' in key_details)) {
            return '<i class="fa fa-check finding-good"></i>';
        } else {
            return '<i class="fa fa-question-circle"></i></i>';
        }
    } 
});

Handlebars.registerHelper('has_logging?', function(logging) {
    return logging;
});

Handlebars.registerHelper('finding_entity', function(prefix, entity) {
    return finding_entity(prefix, entity);
});

Handlebars.registerHelper('count_in', function(service, path) {
    var entities = path.split('.');
    if (service == 'ec2') {
        var input = run_results['services']['ec2'];
    } else if(service == 'cloudtrail') {
        var input = run_results['services']['cloudtrail'];
    } else {
        return 0;
    }
    return recursive_count(input, entities);
});

Handlebars.registerHelper('count_in_new', function(path) {
    var entities = path.split('.');
    return recursive_count(run_results, entities);
});

Handlebars.registerHelper('count_ec2_in_region', function(region, path) {
    if (typeof run_results['services']['ec2'] != 'undefined') {
        var count = 0;
        var entities = path.split('.');
        for (r in run_results['services']['ec2']['regions']) {
            if (r == region) {
                return recursive_count(run_results['services']['ec2']['regions'][r], entities);
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
};

Handlebars.registerHelper('find_ec2_object_attribute', function(path, id, attribute ) {
    return findEC2ObjectAttribute(run_results['services']['ec2'], path, id, attribute);
});

Handlebars.registerHelper('format_date', function(time) {
    if(typeof time === 'number') {
        return new Date(time * 1000).toString();
    }
    else if(typeof time === 'string') {
        return new Date(time);
    }
    else if(!time || time === null) {
        return 'No date available'
    }
    else {
        return 'Invalid date format';
    }
});

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

Handlebars.registerHelper('ifType', function(v1, v2, options) {
    if(typeof v1 == v2) {
        return options.fn(v1);
    } else {
        return options.inverse(v1);
    }
});

Handlebars.registerHelper('fixBucketName', function(bucket_name) {
    if (bucket_name != undefined) {
        return bucket_name.replace(/\./g, '-');
    }
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

Handlebars.registerHelper('ifEqual', function(v1, v2, options) {
    if (v1 === v2) {
        return options.fn(this);
    } else {
        return options.inverse(this);
    }
});

Handlebars.registerHelper('unlessEqual', function(v1, v2, options) {
    if (v1 !== v2) {
        return options.fn(this);
    } else {
        return options.inverse(this);
    }
});

Handlebars.registerHelper('ifPositive', function(v1, options) {
    if (v1 === 'N/A' || v1 === 0) {
        return options.inverse(this);
    } else {
        return options.fn(this);
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

Handlebars.registerHelper('get_value_at', function() {
    var path = arguments[0];
    for (var i = 1; i < arguments.length -1; i++) {
        path = path + '.' + arguments[i];
    }
    return get_value_at(path);
});

Handlebars.registerHelper('concat', function() {
    var path = arguments[0];
    for (var i = 1; i < arguments.length -1; i++) {
        path = path + '.' + arguments[i];
    }
    return path;
});

Handlebars.registerHelper('json_stringify', function() {
    body = arguments[0];
    delete body['description'];
    delete body['args'];
    return JSON.stringify(body, null, 4)
});

Handlebars.registerHelper('get_key', function() {
    rule = arguments[1];
    if (rule['key']) {
        key = rule['key'];
    } else {
        key = arguments[0];
    }
    return key.replace('.', '');
});

Handlebars.registerHelper('other_level', function() {
    if (arguments[0] == 'warning') {
        return 'danger';
    } else {
        return 'warning';
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

// Takes a dict and returns a sorted list
// The key for each element of the dict is added as an attribute of each list object
Handlebars.registerHelper('each_dict_as_sorted_list', function(context, options) {
    var ret = "";

    var sorted_findings_keys = Object.keys(context).sort(function(a,b) {
        if(context[a].flagged_items == 0 && context[b].flagged_items == 0){
            if(context[a].checked_items == 0 && context[b].checked_items != 0) return 1;
            if(context[a].checked_items != 0 && context[b].checked_items == 0) return -1;
            if(context[a].description.toLowerCase() < context[b].description.toLowerCase()) return -1;
            if(context[a].description.toLowerCase() > context[b].description.toLowerCase()) return 1;
        }
        if((context[a].flagged_items == 0 && context[b].flagged_items > 0)
            || (context[a].flagged_items > 0 && context[b].flagged_items == 0)){
            if(context[a].flagged_items > context[b].flagged_items) return -1;
            return 1
        }
        if(context[a].flagged_items > 0 && context[b].flagged_items > 0){
            if(context[a].level == context[b].level){
                if(context[a].description.toLowerCase() < context[b].description.toLowerCase()) return -1;
                if(context[a].description.toLowerCase() > context[b].description.toLowerCase()) return 1;
            }
            else {
                if(context[a].level.toLowerCase() === 'danger') return -1;
                if(context[b].level.toLowerCase() === 'danger') return 1;
                if(context[a].level.toLowerCase() === 'warning') return -1;
                if(context[b].level.toLowerCase() === 'warning') return 1;
                if(context[a].level.toLowerCase() === 'warning') return -1;
                if(context[b].level.toLowerCase() === 'warning') return 1;
            }
        }
        return 0;
    });

    sorted_findings_keys.forEach(function(key) {
        var obj = context[key];
        obj['key'] = key;
        // sorted_findings.push(obj);
        ret += options.fn(obj);
    });

    return ret
});

Handlebars.registerHelper('sorted_each', function(array, key, opts) {
    newarray = array.sort(function(a, b) {
        if (a[key] < b[key]) return -1;
        if (a[key] > b[key]) return 1;
        return 0;
    });
    return opts.fn(newarray);
});

Handlebars.registerHelper('escape_dots', function() {
    return arguments[0].replace(/\./g, '\\.');
});

/**
 * Converts a boolean value to 'Enabled' or 'Disabled'. If the value is undefined or null, then it returns 'Unknown'.
 */
Handlebars.registerHelper('convert_bool_to_enabled', function (value) {
    if (value === undefined || value === null) return 'Unknown';
    return value ? 'Enabled' : 'Disabled';
});


/*********************/
/* Ruleset generator */
/*********************/

Handlebars.registerHelper('get_rule', function(rule_filename, attribute) {
    if (attribute == 'service') {
        return rule_filename.split('-')[0];
    } else {
        rule = run_results['rule_definitions'][rule_filename];
        // Clean up some ruleset generator artifacts
        attribute_cleanup = ['file_name', 'file_path', 'rule_dirs', 'rule_types', 'rules_data_path', 'string_definition'];
        for (ac in attribute_cleanup) {
            rule = rule_cleanup(rule, attribute_cleanup[ac]);
        }
        if (attribute == '') {
            return rule;
        } else {
            return rule[attribute];
        }
    }
});

var rule_cleanup = function(rule, attribute) {
    if (attribute in rule) {
        delete rule[attribute];
    }
    return rule;
};

Handlebars.registerHelper('get_arg_name', function(rule_filename, arg_index) {
    if ('arg_names' in run_results['rule_definitions'][rule_filename]) {
        return  run_results['rule_definitions'][rule_filename]['arg_names'][arg_index];
    } else {
        return '';
    }
});

