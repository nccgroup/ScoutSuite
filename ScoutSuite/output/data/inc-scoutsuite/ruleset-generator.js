/**********************************************************/
/* JavaScript code specific to Scout2's Ruleset Generator */
/**********************************************************/

var generate_ruleset = function() {
    var ruleset = new Object();
    ruleset['about'] =run_results['about'];
    ruleset['rules'] = new Object();
    // Find all the rules
    var rules = $("*[id^='rule-']");
    for (var i=0; i < rules.length; i++) {
        var filename = $(rules[i]).find('#filename').val();
        var rule = {};
        rule['level'] = $(rules[i]).find('#level').val();
        rule['enabled'] = $(rules[i]).find('#enabled').is(':checked');
        args = $(rules[i]).find("[id^='parameter_']");
        if (args.length > 0) {
            tmp = {};
            for (var j=0; j < args.length; j++) {
                id = $(args[j]).attr('id').replace('parameter_', '');
                val = $(args[j]).val();
                tmp[id] = val;
            }
            rule['args'] = [];
            for (k in tmp) {
                rule['args'].push(tmp[k]);
            }
        }

        if (!(filename in ruleset['rules'])) {
            ruleset['rules'][filename] = [];
        }
        ruleset['rules'][filename].push(rule);
    }

    download_configuration(ruleset, run_results['name'], '');
}
