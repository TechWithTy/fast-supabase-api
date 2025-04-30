Pulsar Shell

Pulsar shell is a fast and flexible shell for Pulsar cluster management, messaging, and more. It's great for quickly switching between different clusters, and can modify cluster or tenant configurations in an instant.
Use case

    Administration: find all the Admin API features under the admin command.
    Client: find all the pulsar-client features under the client command.

Install Pulsar Shell

Download the tarball from the download page and extract it.

curl -LO "https://www.apache.org/dyn/closer.lua/pulsar/pulsar-4.0.4/apache-pulsar-shell-4.0.4-bin.tar.gz?action=download"
tar xzvf apache-pulsar-shell-4.0.4-bin.tar.gz
cd apache-pulsar-shell-4.0.4/

Now you can enter Pulsar shell's interactive mode:

./bin/pulsar-shell
Welcome to Pulsar shell!
Service URL: pulsar://localhost:6650/
Admin URL: http://localhost:8080/

Type help to get started or try the autocompletion (TAB button).
Type exit or quit to end the shell session.

default(localhost)>

Connect to your cluster

By default, the shell tries to connect to a local Pulsar instance. To connect to a different cluster, you have to register the cluster with Pulsar shell. You can do this in a few different ways depending on where your config file is located:
note

The configuration file must be a valid client.conf file, the same one you use for pulsar-admin, pulsar-client and other client tools.

    Remote URL
    File
    Inline

The --url value must point to a valid remote file.

default(localhost)> config create --url https://<url_to_my_client.conf> mycluster

Once you've configured your cluster, set it as current:

default(localhost)> config use mycluster
Welcome to Pulsar shell!
Service URL: pulsar+ssl://mycluster:6651/
Admin URL: https://mycluster:8443/

Type help to get started or try the autocompletion (TAB button).
Type exit or quit to end the shell session.

my-cluster(mycluster)>

Run commands sequentially

To run a bunch of admin commands sequentially, you can use Pulsar shell's non-interactive mode. For example, to set up a new tenant with policies, you would normally need to run multiple pulsar-admin commands.

Let's say you want to create a new tenant new-tenant with a namespace new-namespace in it. There are multiple ways to do this with Pulsar shell non-interactive mode:

    Single command
    File
    Unix pipe

Specify a multi-line command with the -e option.

./bin/pulsar-shell -e "
config use my-cluster
admin tenants create new-tenant
admin namespaces create new-tenant/new-namespace
" --fail-on-error
