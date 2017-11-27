# bitcoin-analysis
ECE 4813 cloud computing project for bitcoin price analysis and prediction.

# Quick Start Guide
1. Clone this repository to a machine with Storm server already installed and running.
2. `cd storm-server` to switch to the storm-server directory.
3. `make init` to install the necessary python libraries and create a `config.json`.
4. Fill in the `config.json` with appropriate data. This contains configuration information for the following:
    * Twitter
    * DynamoDB
    * Kafka
5. `make build` to build the Storm `*.jar` file to run.
6. `make deploy` to deploy the build to Storm.
7. `make listen` to start the listeners that will feed data into the Kafka queues.

# View logs
Logs are extremely useful when Storm does not work as expected. They can be found in the following directory:

    /var/log/storm/workers-artifacts/{topology_name}/{worker_id}/worker.log

`topology_name` and `worker_id` depends on the particular instance of the Storm server.