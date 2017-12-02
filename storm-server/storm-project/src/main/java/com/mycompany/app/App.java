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

public static class AnalysisBolt extends ShellBolt implements IRichBolt {
	public AnalysisBolt() {
		super("python", "dynamo_bolt.py"); 
		//to be changed later
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

public static class TwitterBolt extends ShellBolt implements IRichBolt {
	public TwitterBolt() {
		super("python", "twitter_bolt.py");
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

public static class RedditBolt extends ShellBolt implements IRichBolt {
	public RedditBolt() {
		super("python", "reddit_bolt.py");
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

public static class NewsBolt extends ShellBolt implements IRichBolt {
	public NewsBolt() {
		super("python", "news_bolt.py");
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

public static class PriceBolt extends ShellBolt implements IRichBolt {
	public PriceBolt() {
		super("python", "price_bolt.py");
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

	builder.setSpout("twitter_spout", new TwitterSpout(), 4);
	builder.setSpout("reddit_spout", new RedditSpout(), 2);
	builder.setSpout("news_spout", new NewsSpout(), 2);
	builder.setSpout("price_spout", new PriceSpout(), 2);

	builder.setBolt("twitter_bolt", new TwitterBolt(), 2).shuffleGrouping("twitter_spout");
	builder.setBolt("reddit_bolt", new RedditBolt(), 2).shuffleGrouping("reddit_spout");
	builder.setBolt("news_bolt", new NewsBolt(), 2).shuffleGrouping("news_spout");
	builder.setBolt("price_bolt", new PriceBolt(), 2).shuffleGrouping("price_spout");	
	
	builder.setBolt("analysis_bolt", new AnalysisBolt(), 2).shuffleGrouping("twitter_bolt").shuffleGrouping("news_bolt").shuffleGrouping("reddit_bolt").shuffleGrouping("price_bolt");

	Config conf = new Config();
	conf.setDebug(true);

	if (args != null && args.length > 0) {
		conf.setNumWorkers(4);
		StormSubmitter.submitTopology(args[0], conf, builder.createTopology());
	}
	else {
		conf.setMaxTaskParallelism(4);

		LocalCluster cluster = new LocalCluster();
		cluster.submitTopology("mytopology", conf, builder.createTopology());

		Thread.sleep(10000);

		cluster.shutdown();
	}
}

}
