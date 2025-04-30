Isolate brokers

In Pulsar, when namespaces (more specifically, namespace bundles) are assigned dynamically to brokers, the namespace isolation policy limits the set of brokers that can be used for assignment. Before topics are assigned to brokers, you can set the namespace isolation policy with a primary or a secondary regex to select desired brokers.

To set a namespace isolation policy for a broker cluster, you can use one of the following methods.

    Pulsar-admin CLI
    REST API
    Java admin API

pulsar-admin ns-isolation-policy set options

For more information about the command pulsar-admin ns-isolation-policy set options, see Pulsar admin docs.

Example

bin/pulsar-admin ns-isolation-policy set \
--auto-failover-policy-type min_available \
--auto-failover-policy-params min_limit=1,usage_threshold=80 \
--namespaces my-tenant/my-namespace \
--primary 10.193.216.*  my-cluster policy-name

tip

To guarantee all the data that belongs to a namespace is stored in desired bookies, you can isolate the data of the namespace into user-defined groups of bookies. See configure bookie affinity groups for more details.