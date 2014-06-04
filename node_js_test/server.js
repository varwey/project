var http = require('http');
var url = require('url');

function start(route) {
    function onRequest(request, response) {
        var path_name = url.parse(request.url).pathname;
        console.log('request for ' + path_name + ' received.');
        route(path_name);
        response.writeHead(200, {'Content-Type': 'text/plain'});
        response.write('Hello World');
        response.end();
    }
    http.createServer(onRequest).listen(8888);
    console.log('the server id running at http://localhost:8888/');
}

exports.start = start;
