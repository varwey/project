/*
 * Webbot Status Analysis
 * by Kev++ @ 2013-08-15
 *
 */

result = db.data.find({config_path: site, start_time: {$gt: from}, finish_time: {$lt: to}}).map(function(e){
    reason = e['finish_reason'] || 'unknown';
    rx_count = e['downloader/request_count'] || 0;
    rx_bytes = e['downloader/request_bytes'] || 0;
    tx_count = e['downloader/response_count'] || 0;
    tx_bytes = e['downloader/response_bytes'] || 0;
    err_count = e['downloader/exception_count'] || 0;
    scraped = e['item_scraped_count'] || 0;
    dropped = e['item_dropped_count'] || 0;
    duplicated = e['item_duplicated_count'] || 0;
    elapsed = (e['finish_time']-e['start_time'])/1000;

    return {
        reason: reason,
        rx_count: rx_count,
        rx_bytes: rx_bytes,
        tx_count: tx_count,
        tx_bytes: tx_bytes,
        err_count:err_count,
        scraped:  scraped,
        dropped:  dropped,
        duplicated: duplicated,
        elapsed: elapsed
    };
});

summary = result.reduce(function(pre, cur, idx){
    return {
        site:       site.source,
        count:      idx+1,
        rx_count:   pre.rx_count+cur.rx_count,
        rx_bytes:   pre.rx_bytes+cur.rx_bytes,
        tx_count:   pre.tx_count+cur.tx_count,
        tx_bytes:   pre.tx_bytes+cur.tx_bytes,
        err_count:  pre.err_count+cur.err_count,
        scraped:    pre.scraped+cur.scraped,
        dropped:    pre.dropped+cur.dropped,
        duplicated: pre.duplicated+cur.duplicated,
        elapsed_min:Math.min(pre.elapsed_min||pre.elapsed, cur.elapsed),
        elapsed_max:Math.max(pre.elapsed_max||pre.elapsed, cur.elapsed),
        elapsed_sum:(pre.elapsed_sum||elapsed)+cur.elapsed
    };
});

summary.name = name;
summary.date = format(from);
summary.elapsed_avg = summary.elapsed_sum/summary.count;
delete summary.elapsed_sum;

printjson(summary);

