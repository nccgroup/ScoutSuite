function sqlite_test() {
    var request = new XMLHttpRequest();
    request.open("GET","http://127.0.0.1:8000/api/data?key=last_run.time", true);
    
    request.onload = function () {
        var data = JSON.parse(this.response);
        console.log(this.response);
    }
    
    request.send();
}

// Example query : http://127.0.0.1:8000/api/data?key=last_run.time
function request_db(query, callback) {
    var request = new XMLHttpRequest();
    request.open("GET","http://127.0.0.1:8000/api/data?key=" + query, true);
    
    request.onload = function () {
        var data = JSON.parse(this.response);
        console.log(data);
        callback(data);
    }
    
    request.send();
}

function load_metadata_sqlite() {
    request_db("aws_account_id.data", set_title);
}

function set_title(title) {
    console.log("In set title");
    
    $(function () {
        3
        $(document).attr("title", 'Scout Suite Report [' + title + ']');
        4
    });

    hidePleaseWait();
}

