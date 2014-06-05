var server = require('./server');
var router = require('./router');
var requestHandlers = require('./requestHandlers');
var handle = {}
    handle['/'] = requestHandlers.index;
    handle['/start'] = requestHandlers.start;
    handle['/upload'] = requestHandlers.upload;
console.log(handle);
server.start(router.route, handle);
