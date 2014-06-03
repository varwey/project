/*
 * Webbot Status Analysis
 * by Kev++ @ 2013-08-15
 *
 */

function format(dt) {
    y = zfill(dt.getFullYear(), 4);
    m = zfill(dt.getMonth()+1, 2);
    d = zfill(dt.getDate(), 2);
    return y+'-'+m+'-'+d;
}

function zfill(num, len) {
    return (0 > num ? "-" : "") +
        (Math.pow(10, len) <= Math.abs(num) ?
         "0" + Math.abs(num) :
         Math.pow(10, len) + Math.abs(num)).toString().substr(1)
}
