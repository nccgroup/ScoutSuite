// Keeping this for now for manual debugging, should be removed later on
function sqlite_test() {
    var request = new XMLHttpRequest();
    request.open("GET","http://127.0.0.1:8000/api/data?key=aws_account_id", true);
    
    request.onload = function () {
        var data = JSON.parse(this.response);
        console.log(this.response);
    }
    
    request.send();
}

// Example query : http://127.0.0.1:8000/api/data?key=last_run.time
function request_db(query) {
    var request = new XMLHttpRequest();
    request.open("GET","http://127.0.0.1:8000/api/data?key=" + query, false);
    
    var data = undefined;
    request.onload = function () {
        if (this.readyState == 4) {
            data = JSON.parse(this.response);
            console.log(data.data);
        }
    }
    
    request.send();
    return data.data;
}

function load_metadata_sqlite() {
    load_account_id_sqlite();
    hidePleaseWait();
}

/**
 * Display the account ID -- use of the generic function + templates result in the div not being at the top of the page
 */
function load_account_id_sqlite() {
    var element = document.getElementById('aws_account_id');
    var value = '<i class="fa fa-cloud"></i> ' + request_db("provider_name") +
        ' <i class="fa fa-chevron-right"></i> ' + request_db("aws_account_id");
    /*if (('organization' in run_results) && (value in run_results['organization'])) {
        value += ' (' + run_results['organization'][value]['Name'] + ')'
    }*/
    element.innerHTML = value;
};