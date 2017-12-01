package com.mycompany.app;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.task.ShellBolt;
import backtype.storm.spout.ShellSpout;
import backtype.storm.topology.IRichBolt;
import backtype.storm.topology.IRichSpout;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.tuple.Fields;
import java.util.Map;


public class App {

public static class TwitterSpout extends ShellSpout implements IRichSpout {
	public TwitterSpout() {
		super("python", "twitter_spout.py");
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("word"));
	}

	@Override
	public Map<String, Object> getComponentConfiguration() {
		return null;
	}
}

public static class RedditSpout extends ShellSpout implements IRichSpout {
	public RedditSpout() {
		super("python", "reddit_spout.py");
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("word"));
	}

	@Override
	public Map<String, Object> getComponentConfiguration() {
		return null;
	}
}

public static class PriceSpout extends ShellSpout implements IRichSpout {
	public PriceSpout() {
		super("python", "price_spout.py");
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("word"));
	}

	@Override
	public Map<String, Object> getComponentConfiguration() {
		return null;
	}
}

public static class NewsSpout extends ShellSpout implements IRichSpout {
	public NewsSpout() {
		super("python", "news_spout.py");
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("word"));
	}

	@Override
	public Map<String, Object> getComponentConfiguration() {
		return null;
	}
}

public static class DynamoBolt extends ShellBolt implements IRichBolt {
	public DynamoBolt() {
		super("python", "dynamo_bolt.py");
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("word"));
	}

	@Override
	public Map<String, Object> getComponentConfiguration() {
		return null;
	}
}


public static void main(String[] args) throws Exception {

	TopologyBuilder builder = new TopologyBuilder();

	builder.setSpout("twitter_spout", new TwitterSpout(), 5);
	builder.setSpout("reddit_spout", new RedditSpout(), 5);
	builder.setSpout("news_spout", new NewsSpout(), 5);
	builder.setSpout("price_spout", new PriceSpout(), 5);

	builder.setBolt("analysis_bolt", new DynamoBolt(), 20).shuffleGrouping("twitter_spout").shuffleGrouping("news_spout").shuffleGrouping("reddit_spout").shuffleGrouping("price_spout");

	Config conf = new Config();
	conf.setDebug(true);

	if (args != null && args.length > 0) {
		conf.setNumWorkers(5);
		StormSubmitter.submitTopology(args[0], conf, builder.createTopology());
	}
	else {
		conf.setMaxTaskParallelism(3);

		LocalCluster cluster = new LocalCluster();
		cluster.submitTopology("mytopology", conf, builder.createTopology());

		Thread.sleep(10000);

		cluster.shutdown();
	}
}

}
