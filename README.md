# bitcoin-analysis
ECE 4813 cloud computing project for bitcoin price analysis and prediction.

![ScreenShot](https://github.com/boalinlai/bitcoin-analysis/blob/master/img/web_screenshot.png)


# Quick Start Guide
1. Clone this repository to a machine with Storm server already installed and running.
2. `cd storm-server` to switch to the storm-server directory.
3. `make init` to install the necessary python libraries and create a `config.json`.
4. Create the following tables in DynamoDB:

    | Table Name                | Partition Key         | Sort Key              |
    | -----------------         |:---------------------:|:---------------------:|
    | bitcoin_analysis          | date (String)         | timestamp (String)    |
    | bitcoin_price             | timestamp (String)    |                       |
    | bitcoin_price_prediction  | timestamp (String)    |                       |
    | tweet_sentiment           | date (String)         | timestamp (String)    |
    | news_sentiment            | date (String)         | timestamp (String)    |
    | reddit_sentiment          | date (String)         | title (String)        |
5. Fill in the `config.json` with appropriate data. This contains configuration information for the following:
    * Twitter API Keys
    * AWS DynamoDB Access Keys
    * Kafka Queue Names
    * Reddit API Keys
    * Google News API Key
6. `make build` to build the Storm `*.jar` file to run.
7. `make deploy` to deploy the build to Storm (this will automatically kill an existing deployment before deploying a new one)
8. `make listen` to start the listeners that will feed data into the Kafka queues.

9. `make web` to start the web server. the default host is the public ip of ec2 instance

# View logs
Logs are extremely useful when Storm does not work as expected. They can be found in the following directory:

    /var/log/storm/workers-artifacts/{topology_name}/{worker_id}/worker.log

`topology_name` and `worker_id` depends on the particular instance of the Storm server.

# Run web server

in /frondend/ folder :

`sudo python app.py`

host and port can be tweaked.

default is 0,0,0,0 with port 80


