var exec = require('child_process').exec;

/*
function start(response) {
    console.log("Request handler 'start' was called.");
    //阻塞test code
    function sleep(milliSeconds) {
        var startTime = new Date().getTime();
        while (new Date().getTime() < startTime + milliSeconds);
    }
    //sleep(10000);
    
    //非阻塞test code (error)
    //var content = 'empty';
    //exec('ls -lah', function (error, stdout, stderr) {
        //content = stdout;
    //});

    //return content;
    //return 'Hello Start !!!';

    //测试非阻塞
    //exec('ls -lah', function (error, stdout, stderr) {
        //response.writeHead(200, {'Content-Type': 'text/plain'});
        //response.write(stdout);
        //response.end();

    exec('find /',
        {timeout: 1000, maxBuffer: 20000*1024},
        function (error, stdout, stderr) {
            response.writeHead(200, {'Content-Type': 'text/plain'});
            sleep(10000);
            response.write(stdout);
            response.end();
        });
    }
*/

function start(response) {
    console.log("Response handler 'start' was called.");
    var body = '<html>'+
        '<head>'+
        '<meta http-equiv="Content-Type" content="text/html;" charset=UTF-8" />'+
        '</head>'+
        '<body>'+
        '<form action="/upload" method="post">'+
        '<textarea name="text" rows="20" cols="60"></textarea>'+
        '<input type="submit" value="Submit text" />'+
        '</form>'+
        '</body>'+
        '</html>';
    response.writeHead(200, {'Content-Type': 'text/html'});
    response.write(body);
    response.end();
}

function upload(response) {
    console.log("Request handler 'upload' was called.");
    //原始code
    //return 'Hello Upload !!!'

    response.writeHead(200, {'Content-Type': 'text/plain'});
    response.write('Hello Upload');
    response.end();
}

function index(response) {
    console.log("Request handler 'index' was called.");
    response.writeHead(200, {'Content-Type': 'text/plain'});
    response.write('Hello World')
    response.end();
    //return 'Hello World !!!'
}
exports.start = start;
exports.upload = upload;
exports.index = index;
