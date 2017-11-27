.PHONY: listen deploy build init

init:
	pip install -r requirements.txt
	cp config_template.json config.json

build:
	cp config.json storm-project/multilang/resources/config.json
	cd storm-project && mvn clean package

deploy:
	cd storm-project && storm jar target/storm-project-0.9.3-jar-with-dependencies.jar com.mycompany.app.App mytopology

listen:
	python listeners/tweepy_listener.py