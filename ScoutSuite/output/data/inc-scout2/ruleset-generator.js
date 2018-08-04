/**********************************************************/
/* JavaScript code specific to Scout2's Ruleset Generator */
/**********************************************************/

var generate_ruleset = function() {
    var ruleset = new Object();
    ruleset['about'] = aws_info['about'];
    ruleset['rules'] = new Object();
    // Find all the rules
    var rules = $("*[id^='rule-']");
    for (var i=0; i < rules.length; i++) {
        var filename = $(rules[i]).find('#filename').val();
        var rule = new Object();
        rule['level'] = $(rules[i]).find('#level').val();
        rule['enabled'] = $(rules[i]).find('#enabled').is(':checked');
        args = $(rules[i]).find("[id^='parameter_']")
        if (args.length > 0) {
            tmp = new Object();
            for (var j=0; j < args.length; j++) {
                id = $(args[j]).attr('id').replace('parameter_', '');
                val = $(args[j]).val();
                tmp[id] = val;
            }
            rule['args'] = new Array();
            for (k in tmp) {
                rule['args'].push(tmp[k]);
            }
        }

        if (!(filename in ruleset['rules'])) {
            ruleset['rules'][filename] = new Array();
        }
        ruleset['rules'][filename].push(rule);
    }

    download_configuration(ruleset, aws_info['name'], '');
}
