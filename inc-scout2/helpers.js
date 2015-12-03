
////////////////////////
// Handlebars helpers //
////////////////////////

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

Handlebars.registerHelper('friendly_name', function(entity) {
    return 'friendly_name';
    var name = entity.split('.').pop();
    name = name.replace('_', ' ');
    return name.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
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

Handlebars.registerHelper('count_in_new', function(path) {
    var entities = path.split('.');
    console.log('Counting ' + path);
    /*
    if (service == 'ec2') {
        var input = aws_info['services']['ec2'];
    } else if(service == 'cloudtrail') {
        var input = aws_info['services']['cloudtrail'];
    } else {
        return 0;
    }
    */
    return recursive_count(aws_info, entities);
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
    console.log('Entities left: ' + entities + ' (length = ' + entities.length + ')');
    if (entities.length > 0) {
        var entity = entities.shift();
        for (i in input[entity]) {
            count = count + recursive_count(input[entity][i], eval(JSON.stringify(entities)));
        }
    } else {
        console.log('Found one...');
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

