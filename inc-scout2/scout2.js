var violations_array = new Array();

// Generic load JSON function
function load_aws_config_from_json(list, keyword, cols) {
    var id1 = '#' + keyword + '-list-template';
    var id2 = keyword + 's-list';
    var tmp = Handlebars.compile($(id1).html());
    document.getElementById(id2).innerHTML = tmp({items: list});
    if (cols >= 2) {
        var id3 = '#' + keyword + '-detail-template';
        var id4 = keyword + 's-details';
        var tmp = Handlebars.compile($(id3).html());
        document.getElementById(id4).innerHTML = tmp({items: list});
    }
}

// Generic highlight finding function
function highlight_violations(violations) {
    for (i in violations) {
        var idprefix = violations[i]['keyword_prefix'] + '_' + violations[i]['entity'].split('.').pop();
        if (violations[i]['idprefix'] != '') {
            var idprefix = idprefix + '-' + violations[i]['idprefix'];
        }
        var vkey = idprefix + '-' + i;
        violations_array[vkey] = new Array();
        for (j in violations[i]['items']) {
            var id = vkey + '-' + violations[i]['items'][j];
            var style = "finding-" + violations[i]['level'];
            $('[id$="' + id + '"]').addClass(style);
            violations_array[vkey].push(violations[i]['macro_items'][j]);
        }
    }
}

// Display functions
function hideAll() {
    $("[id$='-row']").hide();
    $("[id*='-details-']").hide();
}
function hideRowItems(keyword) {
    $("[id*='" + keyword + "-list']").hide();
    $("[id*='" + keyword + "-details']").hide();
}
function showEmptyRow(keyword) {
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
function showRow(keyword) {
    id = "#" + keyword + "s-row";
    $(id).show();
}
function showRowWithDetails(keyword) {
    showRow(keyword);
    showAll(keyword);
}
function showAll(keyword) {
    $("[id*='" + keyword + "-list']").show();
    $("[id*='" + keyword + "-details']").show();
}
function toggleDetails(keyword, item) {
    var id = '#' + keyword + '-' + item;
    $(id).toggle();
}
function updateNavbar(active) {
    $('[id^="navbar-item-"]').removeClass('active');
    $('#navbar-item-'+active).addClass('active');
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

// Browsing functions
function browseTo(keyword, id) {
    hideAll();
    showRow(keyword);
    var html_id = "[id=\"" + keyword + "-details-" + id + "\"]";
    $(html_id).show();
    window.scrollTo(0,0);
}
function list_generic(keyword) {
    updateNavbar(keyword);
    hideAll();
    showRowWithDetails(keyword);
    window.scrollTo(0,0);
}
function list_findings(keyword_prefix, keyword, finding) {
    keyword = keyword_prefix + '_' + keyword;
    updateNavbar(keyword);
    hideAll();
    showEmptyRow(keyword);
    var violation_id = keyword + '-' + finding;
    for (item in  violations_array[violation_id]) {
        showItem(keyword, violations_array[violation_id][item]);
    }
    window.scrollTo(0,0);
}

// Handlebars helpers
Handlebars.registerHelper("decodeURIComponent", function(blob) {
    var test = decodeURIComponent(blob);
    test = test.replace(/ /g, '&nbsp;');
    test = test.replace(/\n/g, '<br />');
    return test;
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
Handlebars.registerHelper('has_mfa?', function(mfa_devices, user_name) {
    if (typeof mfa_devices != 'undefined' && mfa_devices != '') {
        return 'Yes';
    } else {
        return '<span id="iam_user-no-mfa-' + user_name + '">No</span>';
    }
});
Handlebars.registerHelper('format_grant', function(grants) {
    if (grants.match(/.*\(.*\)/)) {
        return 'EC2 Group: ';
    } else {
        return 'Source IP: ';
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
Handlebars.registerHelper('list_group_instances', function(group_id, running, stopped) {
    var rc = count_instances(running);
    var sc = count_instances(stopped);
    var r = '';
    r += format_instances(group_id, running, rc, 'Running');
    r += format_instances(group_id, stopped, sc, 'Stopped');
    return r;
});
function count_instances(instances) {
    if (typeof instances != 'undefined' && instances != '') {
        return instances.length;
    } else {
        return 0;
    }
}
function format_instances(group_id, instances, count, title) {
    var r = '';
    r += '<ul class="no-bullet">';
    if (count > 0) {
        r += '<li>';
        r += '<a href="javascript:toggleVisibility(\'ec2_instances-' + group_id + '-' + title +'\')">';
        r += '<span id="bullet-ec2_instances-' + group_id + '-' + title + '">';
        r += '<i class="glyphicon glyphicon-expand"></i></span></a> ';
        r += title + ': ' + count;
        r += '</li><div id="ec2_instances-' + group_id + '-' + title +'"><ul>';
        for (i in instances) {
            r += '<li class="list-group-item-text"><a href="javascript:browseTo(\'ec2_instance\',\'' + instances[i] + '\')">' + instances[i] + '</a></li>';
        }
        r += '</ul></div>';
    } else {
        r += '<li>' + title + ': ' + count + '</li>';
    }
    r += '</ul>';
    return r;
}
Handlebars.registerHelper('format_grants', function(bucket_name, grants) {
    r = '';
    for (g in grants) {
        r += list_s3_permissions(bucket_name, g, grants[g]);
    }
    return r;
});
function list_s3_permissions(bucket_name, grantee_name, grants) {
    var r = '';
    r += '<tr><td width="20%">' + grantee_name + '</td>';
    for (grant in grants) {
        r += '<td width="20%" class="text-center">' + format_s3_grant(bucket_name, grantee_name, grant, grants[grant]) + '</td>';
    }
    r += '</tr>';
    return r;
}
function format_s3_grant(bucket_name, grantee_name, grant, value) {
    var icon = '<i class="' + ((value == true) ? 'glyphicon glyphicon-ok' : '') +'"></i>';
    if (grantee_name == 'All users') {
        return '<span id="s3_bucket-world-' + grant + '-' + bucket_name + '">' + icon + '</span>';
    } else {
        return icon;
    }
}
Handlebars.registerHelper('has_logging?', function(logging) {
    return logging;
});
Handlebars.registerHelper('format_finding_menu', function(key, finding) {
    r = '';
    if (finding['macro_items'].length != 0) {
        r += '<li>';
        r += '<a href="javascript:list_findings(\'' + finding['keyword_prefix'] + '\',\'' + finding['entity'].split('.').pop() + '\',\'' + key + '\')">';
        r += finding['description'] + ' (' + finding['macro_items'].length + ')';
        r += '</a></li>';
    }
    return r;
});
Handlebars.registerHelper('format_users', function(users) {
    var len = users.length;
    if (len == 0) {
        return '';
    }
    len = len % 3;
    r = '<table width="100%" class="table">';
    for (u in users) {
        if (u%3 == 0) {
            r += '<tr>';
        }
        r += '<td width="33%" style="padding-left: 10px; text-align: center;"><a href="javascript:browseTo(\'iam_user\', \'' + users[u] + '\')">' + users[u] + '</td>';
        if (u%3 == 2) {
            r += '</tr>';
        }
    }
    if (len != 0) {
        for (i = len; i <3; i++) {
            r += '<td width="33%" style="padding-left: 10px; text-align: center;"></td>';
        }
        r += '</tr>';
    }
    r += '</table>';
    return r;
});
Handlebars.registerHelper('count', function(items) {
    var c = 0;
    for (i in items) {
        c = c + 1;
    }
    return c;
});
Handlebars.registerHelper('count_sg', function(regions) {
    var sgc = 0;
    for (r in regions) {
        for (vpc in regions[r]) {
            for (sg in regions[r][vpc]) {
                sgc = sgc +1;
            }
        }
    }
    return sgc;
});
Handlebars.registerHelper('count_acl', function(regions) {
    var aclc = 0;
    for (r in regions) {
        for (vpc in regions[r]) {
            for (acl in regions[r][vpc]['network_acls']) {
                aclc = aclc +1;
            }
        }
    }
    return aclc;
});
Handlebars.registerHelper('format_network_acls', function (acls, direction) {
    r = '<table class="table-striped" width="100%">';
    r += '<tr><td width="20%" class="text-center">Rule number</td>';
    r += '<td width="20%" class="text-center">Port</td>';
    r += '<td width="20%" class="text-center">Protocol</td>';
    r += '<td width="20%" class="text-center">' + direction + '</td>';
    r += '<td width="20%" class="text-center">Action</td></tr>';
    for (a in acls) {
        r += '<tr>';
        r += '<td width="20%" class="text-center">' + acls[a]['rule_number'] + '</td>';
        r += '<td width="20%" class="text-center">' + acls[a]['port_range'] + '</td>';
        r += '<td width="20%" class="text-center">' + acls[a]['protocol'] + '</td>';
        r += '<td width="20%" class="text-center">' + acls[a]['cidr_block'] + '</td>';
        r += '<td width="20%" class="text-center">' + acls[a]['rule_action'] + '</td>';
        r += '</tr>';
    }
    r += '</table>';
    return r;
});
Handlebars.registerHelper('ifPasswordAndKey', function(logins, access_keys, block) {
    if ((typeof logins != 'undefined' && logins != '') && (typeof access_keys != 'undefined' && access_keys != '')) {
        return block.fn(this);
    } else {
        return block.inverse(this);
    }
});
