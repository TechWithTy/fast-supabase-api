Performance Tuning Best Practices
Redis Enterprise Software
Redis Cloud
Redis CE and Stack
performance

Last updated 18, Apr 2024
Question

In this article, you can find best practices for operating a Redis Enterprise database. Some recommendations are also good for a Redis Community deployment, especially when dealing with the suitable data types and commands, keeping an eye on command complexity.
Redis Commands

    Check the slow log for EVALSHA, HGETALL, HMGET, MGET, and all types of SCAN commands. Lower the slow log threshold to capture more slow commands. You can configure the threshold using CONFIG SET slowlog-log-slower-than <THRESHOLD_MICROSECONDS>
    Avoid the KEYS command, which does a scan of the entire keyspace.
    Take into account MGET commands when calculating the true ops/s. E.g. MGET of 10 keys at 32k ops/s would equate to 320k ops/s.

Hot and Big Keys

    Verify the size of keys using redis-cli --bigkeys and redis-cli --hotkeys(it works only with non-CRDB databases). With high CPU usage caused by operations on a huge key (such as scans), sharding won't help. Large keys can be split into smaller ones to ease the load
    The recommendation is also to limit the size of the range, either command (ZREVRANGE, ZRANGE, ZREVRANGEBYSCORE etc.) will be fine, just don't perform full range (0 -1). The more the range can be limited the better. Then on large sets, we recommend using ZRANGE (or other range scanning commands) with a defined range and not a full scan
    If possible, avoid unbounded LRANGE calls: they can generate high latency. Use a range. If it's a time series it can be treated more efficiently in a different data structure.

Deletion

Delete huge keys using the asynchronous UNLINK rather than the synchronous DEL.

To perform massive key deletion in Redis without impacting performance, use either redis-cli or Redis Insight with bulk actions. Using redis-cli, you can indicate a pattern and make sure you:

    Use -i option so you don’t block the execution of the shard
    Use UNLINK, so you execute tasks in the background

  -i <interval>      
    When -r is used, waits <interval> seconds per command.                     
    It is possible to specify sub-second times like -i 0.1.

Copy code

So an example using the command would be:

redis-cli -p <PORT> --scan --pattern city:* -i 0.01 | xargs redis-cli -p <PORT> unlink

Copy code

Alternatively, it is possible to use xargs with the -L option (max lines) to reduce the chance of blocking the service for other commands.

man xargs

[...]

-L number   Call utility for every number non-empty lines read.

Copy code

Redis Insight has a "BULK ACTIONS" tab and it has the option to Delete Keys.

    In the “Find keys” form field it is possible to provide a pattern
    Click on “DRY RUN” button
    The Preview Pane returns a list of keys that will UNLINK
    Click on 'EXECUTE' button to perform the deletion of keys

Persistence and Backups

Non-replicated databases may cause delays when backups are executed or persistence (AOF/snapshots) is enabled. Replicated databases resolve the side effect, backup is collected on replica shards. The same behavior applies to persistence.
LUA scripts

Verify LUA scripts do not keep the state machine busy with long executions. Check metric "Other cmds", which means anything but commands, like non-read/write commands taking place. For example, auth/ping/eval/evalsha/type commands.
Scalability and shards placement

    Scale-up. Reshard the database so to take advantage of multiple cores. Keep the single proxy policy if the shards are in the same node.
    Scale-out. Redistribute shards across nodes if the CPUs are hogged (if the database is not clustered, make sure operations are cluster-safe).
    Optimize shard placement using the corresponding REST API endpoint and evaluate the recommendations for a given database.
    DMC proxy scaling. If a database has shards on multiple nodes, consider also changing the proxy policy (all-master-shards), so the DMC proxy can also scale.
    Configure and benchmark a different number of threads for the DMC proxy (max_threads) to make sure the proxy does not represent a bottleneck.
    Check if shards are balanced: unbalancing may be caused by nodes having different characteristics. The use of hashing policies or huge keys can cause unbalancing, too.

Resources

    Check for AOF errors in slave shard logs: that implies a slow disk. The Management UI can also report "Unable to write to disk due to reaching disk I/O limit" on the nodes summary page. The alert is about the disk I/O limit, not the storage limit. The disk may not be full but cannot keep up its speed. This may happen, for instance, if all the shards in a node have persistence via AOF enabled. It has something to do with the underlying hardware.
    Use logtop to capture spikes caused by any heavy command together with slow log analysis
    Make sure swapping is disabled. Linux systems may swap memory even if the box isn’t low on memory (especially with a high swappiness value)
    Low memory can also cause costly evictions. Massive key eviction can cause latency spikes as the database must release the memory. This may happen if the cluster is low on memory and the eviction policy is configured for volatile-lru or simply because the massive amount of keys was set with EXPIRE
    Redis Enterprise Active-Active databases now support the MEMORY USAGE command from version 6.2.18, which simplifies troubleshooting and lets applications detect anomalous behavior and dangerous trends.

Network Latency

    Check if the master shard and endpoint are located on the different nodes, which also might increase the latency (best if all master shards are close to the proxy)
    Are the client and database on the same VPC or a different VPC with peering? Both running in the same VPC could help multiply the number of packets per second.

Connection pooling

It is always recommended to use connection pooling. Otherwise, each request will open a new connection. This exposes many possible momentary problems that could prevent the opening of the connection. In addition, opening and closing connections cause additional overhead.

A few connections will serve all the requests using connection pooling and will not close after each request. This eliminates the problems above and will ensure better performance because no time will be wasted on opening and closing connections.

Redis Enterprise keeps connections open forever unless clients close them or don't reply to TCP keep-alive messages. Idle connections that do not answer keepalives for 5 consecutive minutes are closed: Redis Enterprise assumes that clients closed their connections. Verifying the number of active connections is possible using the CLIENT LIST command.

If using a pool, you may need to increase the minimum number of connections in the pool so no new thread creation will delay operations on the client. If not using a pool, evaluate using it.

Examples of clients supporting connection pooling:

    redis-py
    jedis

Not all the clients make the connection pooling feature available: StackExchange, as an example, multiplexes a single connection.
Pipelining

Using client pipelining, it is possible to save on round-trip time by packing multiple commands in batches. In addition to reducing the cumulative latency of multiple commands down to the latency of the batches, fewer socket read operations are needed to read the incoming messages, thus saving on system calls and reducing the overall latency. Read more in the documentation.
Uneven load is observed on different shards

Having more shards for a database to exploit parallelism offered by multiple cores is possible, but it may not always help. There could be a few reasons for having a hot shard. One is that there is a big key or keys on that shard. To find that, you can run the redis-cli command with --bigkeys flag.

redis-cli -h <hostname> -p <port> -a <password> --bigkeys

Copy code

You could also have a hot key. To identify that, you could run the MONITOR command for a very short monitor period of time (a few seconds) in a low-traffic period. Please note that this command is dangerous and can affect latency. Please run it for a very short period of time and test it out first on a dev DB or other low-traffic non-production DB. Read more about the MONITOR command.