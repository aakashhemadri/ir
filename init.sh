#/usr/bin/env bash
docker-compose up -d
until $(curl --output /dev/null --silent --head --fail -X GET "localhost:9200/_cat/nodes?v&pretty"); do
	print '.'
	sleep 2
done
curl -X GET "localhost:9200/_cat/nodes?v&pretty"
scrapy crawl ArsTechnica -o ars-technica.sh.csv
