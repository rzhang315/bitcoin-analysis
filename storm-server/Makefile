.PHONY: listen deploy build init kill

init:
	sudo pip install -t /usr/local/lib/python2.7/dist-packages -r requirements.txt
	cp config_template.json config.json

build:
	cp config.json storm-project/multilang/resources/config.json
	cd storm-project && mvn clean package

kill:
	storm kill mytopology

deploy:
	(storm kill mytopology || true) && \
	sleep 15 && \
        cd storm-project && \
        storm jar target/storm-project-0.9.3-jar-with-dependencies.jar com.mycompany.app.App mytopology

listen:
	cd listeners && python listeners.py
