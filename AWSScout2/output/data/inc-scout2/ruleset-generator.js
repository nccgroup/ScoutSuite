/**********************************************************/
/* JavaScript code specific to Scout2's Ruleset Generator */
/**********************************************************/

var generate_ruleset = function() {
    var ruleset = new Object();
    ruleset['rules'] = new Object();
    // Find all the rules
    var rules = $("*[id^='rule-']");
    for (var i=0; i < rules.length; i++) {
        var rule = new Object()
        filename = $(rules[i]).find('#filename').val();
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

    var uriContent = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(ruleset, null, 4));
    var dlAnchorElem = document.getElementById('downloadAnchorElem');
    dlAnchorElem.setAttribute("href", uriContent);
    dlAnchorElem.setAttribute("download", aws_info['name'] + '.json');
    dlAnchorElem.click();
}
