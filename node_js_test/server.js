var http = require('http');
var url = require('url');

function start(route, handle) {
    function onRequest(request, response) {
        var pathname = url.parse(request.url).pathname;
        console.log('request for ' + pathname + ' received.');
        //response.writeHead(200, {'Content-Type': 'text/plain'});
        //var content = route(handle, path_name)
            //response.write(content);
        //response.end();
        
        route(handle, pathname, response);
    }

    http.createServer(onRequest).listen(8888);
    console.log('the server id running at http://localhost:8888/');
}

exports.start = start;
