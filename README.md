# ir

### Requirements

Requirements to run this project on your system: python 3.6+, pip, docker, docker-compose. Ideally run on a Linux distro of your choice.

```bash
# Clone this repository
git clone https://github.com/aakashhemadri/ir.git
cd ir
```

### Environment setup

```bash
# Install pipenv, This is likely already installed on system
# Use your appropriate python binary in place of `python3`
python3 -m pip --user install pipenv
```

```bash
# Install pipenv environment
cd /path/to/project/root
python3 -m pipenv install
```

Always run the below before running the usage commands.

```bash
# Enter python environment
cd /path/to/project/root
python3 -m pipenv shell
```

### Usage

Run initial setup script

```bash
# To setup the the docker env and do a crawl on ars-technica
# Please inspect the script before running
# If docker/docker-compose was setup correctly kibana should be up on localhost:5601
# Currently one must import csv's externally through kibana after crawling sites.
# Pre-Crawled data is under data/*, Use that. 
cd /path/to/project/root
sh init.sh
```

Crawling custom spiders

```bash
# Specifically crawling with scrapy
cd /path/to/project/root
scrapy crawl ArsTechnica -o ars-technica.new.csv
```

