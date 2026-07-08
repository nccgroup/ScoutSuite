/**********************
 * Handlebars helpers *
 **********************/

Handlebars.registerHelper('displayPolicy', function (blob) {
    var policy = '{<br/>'
    for (let attr in blob) {
        if (attr === 'Statement') {
            policy += '&nbsp;&nbsp;"Statement": [<br/>'
            for (let sid in blob['Statement']) {
                policy += '<span id="foobar">' + JSON.stringify(blob['Statement'][sid], null, 2) + '</span>,\n'
            }
            policy += '  ]'
        } else {
            policy += '  "' + attr + '": ' + JSON.stringify(blob[attr], null, 2)
        }
        policy += ',\n'
    }

    policy += '}'
    return policy
})

Handlebars.registerHelper('add_policy_path', function () {
    var policy = arguments[0]
    var path = arguments[1]
    for (var i = 2; i < arguments.length - 1; i++) {
        path = path + '\\.' + arguments[i]
    }
    policy['policy_path'] = path
    policy['policy_spath'] = path.replace(/\\/g, '')
})

Handlebars.registerHelper('jsonToString', function (obj) {
    // TODO: find a better way to address Handlebars-specific indentation weirdness in <pre>
    return JSON.stringify(obj, null, 2).replace(/\r\n/g, `\r`).replace(/\n/g, `\r`)
})

Handlebars.registerHelper('has_profiles?', function (logins) {
    if (typeof logins !== 'undefined' && logins !== '') {
        return 'Yes'
    } else {
        return 'No'
    }
})

// Required in addition to has_profiles to allow if conditions
Handlebars.registerHelper('ifHasProfiles', function (logins, options) {
    if (typeof logins !== 'undefined' && logins !== '') {
        return options.fn(this)
    } else {
        return options.inverse(this)
    }
})

Handlebars.registerHelper('has_access_keys?', function (accessKeys) {
    if (typeof accessKeys !== 'undefined' && accessKeys !== '') {
        return accessKeys.length
    } else {
        return 0
    }
})

Handlebars.registerHelper('has_mfa?', function (mfaDevices) {
    if (typeof mfaDevices !== 'undefined' && mfaDevices !== '' && mfaDevices.length > 0) {
        return 'Yes'
    } else {
        return 'No'
    }
})

Handlebars.registerHelper('list_permissions', function (permissions) {
    var r = ''
    if (typeof permissions !== 'undefined' && permissions !== '') {
        r += parse_entities('group', permissions.groups)
        r += parse_entities('role', permissions.roles)
        r += parse_entities('user', permissions.users)
    }
    return r
})

Handlebars.registerHelper('good_bad_icon', function (finding, bucketId, keyId, suffix) {
    var keyPath = 's3.buckets.' + bucketId + '.keys.' + keyId + '.' + suffix
    var index = runResults['services']['s3']['findings'][finding]['items'].indexOf(keyPath)
    var level = runResults['services']['s3']['findings'][finding]['level']
    if (index > -1) {
        return '<i class="fa fa-times finding-' + level + '"></i>'
    } else {
        var keyDetails = runResults['services']['s3']['buckets'][bucketId]['keys'][keyId]
        if ((finding === 's3-object-acls-mismatch-bucket') && ('grantees' in keyDetails)) {
            return '<i class="fa fa-check finding-good"></i>'
        } else if ((finding == 's3-object-unencrypted') && ('ServerSideEncryption' in keyDetails)) {
            return '<i class="fa fa-check finding-good"></i>'
        } else {
            return '<i class="fa fa-question-circle"></i></i>'
        }
    }
})

Handlebars.registerHelper('has_logging?', function (logging) {
    return logging
})

Handlebars.registerHelper('finding_entity', function (prefix, entity) {
    return finding_entity(prefix, entity)
})

Handlebars.registerHelper('count_in', function (service, path) {
    var entities = path.split('.')
    if (service === 'ec2') {
        var input = runResults['services']['ec2']
    } else if (service == 'cloudtrail') {
        input = runResults['services']['cloudtrail']
    } else {
        return 0
    }
    return recursiveCount(input, entities)
})

Handlebars.registerHelper('count_in_new', function (path) {
    var entities = path.split('.')
    return recursiveCount(runResults, entities)
})

Handlebars.registerHelper('count_ec2_in_region', function (region, path) {
    if (typeof runResults['services']['ec2'] != 'undefined') {
        var count = 0
        var entities = path.split('.')
        for (let r in runResults['services']['ec2']['regions']) {
            if (r === region) {
                return recursiveCount(runResults['services']['ec2']['regions'][r], entities)
            }
        }
    } else {
        count = 'N/A'
    }
    return count
})

Handlebars.registerHelper('split_lines', function (text) {
    return text ? text.split('\n') : []
})

Handlebars.registerHelper('count_vpc_network_acls', function (vpcNetworkAcls) {
    var counter = 0
    for (let _ in vpcNetworkAcls) {
        counter = counter + 1
    }
    return counter
})

Handlebars.registerHelper('count_vpc_instances', function (vpcInstances) {
    var counter = 0
    for (let _ in vpcInstances) {
        counter = counter + 1
    }
    return counter
})

Handlebars.registerHelper('count_role_instances', function (instanceProfiles) {
    var counter = 0
    for (let ip in instanceProfiles) {
        for (let _ in instanceProfiles[ip]['instances']) {
            counter = counter + 1
        }
    }
    return counter
})

var recursiveCount = function (input, entities) {
    var counter = 0
    if (entities.length > 0) {
        var entity = entities.shift()
        for (let i in input[entity]) {
            counter = counter + recursiveCount(input[entity][i], eval(JSON.stringify(entities)))
        }
    } else {
        counter = counter + 1
    }
    return counter
}

Handlebars.registerHelper('find_ec2_object_attribute', function (path, id, attribute) {
    return findEC2ObjectAttribute(runResults['services']['ec2'], path, id, attribute)
})

Handlebars.registerHelper('format_date', function (time) {
    if (!time || time === '') {
        return 'No date available'
    }
    else if (typeof time === 'number') {
        return new Date(time * 1000).toString()
    } else if (typeof time === 'string') {
        return new Date(time)
    } else {
        return 'Invalid date format'
    }
})

Handlebars.registerHelper('makeTitle', function (title) {
    return makeTitle(title)
})

Handlebars.registerHelper('addMember', function (memberName, value) {
    this[memberName] = value
})

Handlebars.registerHelper('ifShow', function (v1, v2, options) {
    if (v1 !== v2) {
        return options.fn(this)
    }
})

Handlebars.registerHelper('ifType', function (v1, v2, options) {
    if (typeof v1 === v2) {
        return options.fn(v1)
    } else {
        return options.inverse(v1)
    }
})

Handlebars.registerHelper('fixBucketName', function (bucketName) {
    if (bucketName !== undefined) {
        return bucketName.replace(/\./g, '-')
    }
})

Handlebars.registerHelper('dashboard_color', function (level, checked, flagged) {
    if (checked === 0) {
        return 'unknown disabled-link'
    } else if (flagged === 0) {
        return 'good disabled-link'
    } else {
        return level
    }
})

Handlebars.registerHelper('ifEqual', function (v1, v2, options) {
    if (v1 === v2) {
        return options.fn(this)
    } else {
        return options.inverse(this)
    }
})

Handlebars.registerHelper('ifLooseEqual', function (v1, v2, options) {
    if (v1 == v2) {
        return options.fn(this)
    } else {
        return options.inverse(this)
    }
})

Handlebars.registerHelper('unlessEqual', function (v1, v2, options) {
    if (v1 !== v2) {
        return options.fn(this)
    } else {
        return options.inverse(this)
    }
})

Handlebars.registerHelper('ifPositive', function (v1, options) {
    if (!v1 || v1 === 'N/A' || v1 === 0) {
        return options.inverse(this)
    } else {
        return options.fn(this)
    }
})

Handlebars.registerHelper('greaterThan', function (v1, v2, options) {
    'use strict';
    if (v1 > v2) {
        return options.fn(this);
    }
    return options.inverse(this);
});

Handlebars.registerHelper('hasKeys', function (obj, options) {
    if (Object.keys(obj).length > 0) {
        return options.fn(this);
    } else {
        return options.inverse(this);
    }
});

Handlebars.registerHelper('has_condition', function (policyInfo) {
    if (('condition' in policyInfo) && (policyInfo['condition'] != null)) {
        return true
    } else {
        return false
    }
})

Handlebars.registerHelper('escape_special_chars', function (value) {
    return value.replace(/\./g, 'nccdot').replace(/,/g, 'ncccoma')
})

Handlebars.registerHelper('getValueAt', function () {
    var path = arguments[0]
    for (var i = 1; i < arguments.length - 1; i++) {
        path = path + '.' + arguments[i]
    }
    return getValueAt(path)
})

Handlebars.registerHelper('greaterLengthThan', function (v1, v2, options) {
    'use strict';
    if (v1.length>v2) {
        return options.fn(this);
    }
    return options.inverse(this);
});

Handlebars.registerHelper('concat', function () {
    var path = arguments[0]
    for (var i = 1; i < arguments.length - 1; i++) {
        path = path + '.' + arguments[i]
    }
    return path
})

Handlebars.registerHelper('append', function () {
    var path = arguments[0]
    for (var i = 1; i < arguments.length - 1; i++) {
        path = path + arguments[i]
    }
    return path
})

Handlebars.registerHelper('concatWith', function (str1, str2, sep) {
    return [str1, str2].join(sep);
})

Handlebars.registerHelper('jsonStringify', function () {
    let body = arguments[0]
    delete body['description']
    delete body['args']
    return JSON.stringify(body, null, 4)
})

Handlebars.registerHelper('get_key', function () {
    let rule = arguments[1]
    if (rule['key']) {
        var key = rule['key']
    } else {
        key = arguments[0]
    }
    return key.replace('.', '')
})

Handlebars.registerHelper('other_level', function () {
    if (arguments[0] === 'warning') {
        return 'danger'
    } else {
        return 'warning'
    }
})

// http://funkjedi.com/technology/412-every-nth-item-in-handlebars, slightly tweaked to work with a dictionary
Handlebars.registerHelper('grouped_each', function (every, context, options) {
    var out = ''
    var i
    var keys = Object.keys(context)
    var count = keys.length
    var subcontext = {}
    if (context && count > 0) {
        for (i = 0; i < count; i++) {
            if (i > 0 && i % every === 0) {
                out += options.fn(subcontext)
                subcontext = {}
            }
            subcontext[keys[i]] = context[keys[i]]
        }
        out += options.fn(subcontext)
    }
    return out
})

// Takes a dict and returns a sorted list
// The key for each element of the dict is added as an attribute of each list object
Handlebars.registerHelper('each_dict_as_sorted_list', function (context, options) {
    var ret = ''

    var sortedFindingsKeys = Object.keys(context).sort(function (a, b) {
        if (context[a].flagged_items === 0 && context[b].flagged_items === 0) {
            if (context[a].checked_items === 0 && context[b].checked_items !== 0) return 1
            if (context[a].checked_items !== 0 && context[b].checked_items === 0) return -1
            if (context[a].description.toLowerCase() < context[b].description.toLowerCase()) return -1
            if (context[a].description.toLowerCase() > context[b].description.toLowerCase()) return 1
        }
        if ((context[a].flagged_items == 0 && context[b].flagged_items > 0) ||
            (context[a].flagged_items > 0 && context[b].flagged_items === 0)) {
            if (context[a].flagged_items > context[b].flagged_items) return -1
            return 1
        }
        if (context[a].flagged_items > 0 && context[b].flagged_items > 0) {
            if (context[a].level === context[b].level) {
                if (context[a].description.toLowerCase() < context[b].description.toLowerCase()) return -1
                if (context[a].description.toLowerCase() > context[b].description.toLowerCase()) return 1
            } else {
                if (context[a].level.toLowerCase() === 'danger') return -1
                if (context[b].level.toLowerCase() === 'danger') return 1
                if (context[a].level.toLowerCase() === 'warning') return -1 // FIXME - these are duplicated for nothing?
                if (context[b].level.toLowerCase() === 'warning') return 1
                if (context[a].level.toLowerCase() === 'warning') return -1
                if (context[b].level.toLowerCase() === 'warning') return 1
            }
        }
        return 0
    })

    sortedFindingsKeys.forEach(function (key) {
        var obj = context[key]
        obj['key'] = key
        // sorted_findings.push(obj)
        ret += options.fn(obj)
    })

    return ret
})

// Sorts a dict by an arbitrary key
Handlebars.registerHelper('each_dict_sorted', function (dict, key, opts) {
    // convert dict to an array
    var array = [];
    for (var k in dict) {
        if (dict.hasOwnProperty(k)) {
            array.push(dict[k]);
        }
    }
    // sort array
    var output = '';
    var contextSorted = array.concat().sort( function(a,b) { return a[key] - b[key] } );
    for(var i=0, j=contextSorted.length; i<j; i++) {
        output += opts.fn(contextSorted[i]);
    }
    // return resolt
    return output;
})

Handlebars.registerHelper('escape_dots', function () {
    return arguments[0].replace(/\./g, '\\.') // lgtm [js/incomplete-sanitization]
})

/**
 * Converts a boolean value to 'Enabled' or 'Disabled'. If the value is undefined or null, then it returns 'Unknown'.
 */
Handlebars.registerHelper('convert_bool_to_enabled', function (value) {
    if (value === undefined || value === null) return 'Unknown'
    return value ? 'Enabled' : 'Disabled'
})

/**
 * Checks if value is indefined/null and returns 'None', otherwise returns value
 */
Handlebars.registerHelper('value_or_none', function (value) {
    if (value === undefined || value === null || value === '' || value === [] || value === {}) return 'None'
    return value
})

/*********************
 * Ruleset generator *
 *********************/

Handlebars.registerHelper('get_rule', function (ruleFilename, attribute) {
    if (attribute === 'service') {
        return ruleFilename.split('-')[0]
    } else {
        let rule = runResults['rule_definitions'][ruleFilename]
        // Clean up some ruleset generator artifacts
        let attributeCleanup = ['file_name', 'file_path', 'rule_dirs', 'rule_types', 'rules_data_path', 'string_definition']
        for (let ac in attributeCleanup) {
            rule = ruleCleanup(rule, attributeCleanup[ac])
        }
        if (attribute === '') {
            return rule
        } else {
            return rule[attribute]
        }
    }
})

var ruleCleanup = function (rule, attribute) {
    if (attribute in rule) {
        delete rule[attribute]
    }
    return rule
}

Handlebars.registerHelper('get_arg_name', function (ruleFilename, argIndex) {
    if ('arg_names' in runResults['rule_definitions'][ruleFilename]) {
        return runResults['rule_definitions'][ruleFilename]['arg_names'][argIndex]
    } else {
        return ''
    }
})
  
