/*
 * Webbot Status Analysis
 * by Kev++ @ 2013-08-15
 *
 */

/* override via `--eval` option */
site = this.site || new RegExp('sina_mblog');
name = this.name || 'unknown';
from = this.from || new Date(2013, 8-1, 9);
to = this.to || new Date(2013, 8-1, 10);
db = this.db || connect('192.168.3.175/result');

