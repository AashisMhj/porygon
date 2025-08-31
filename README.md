# Porygon
![porygon](./images/porygon-image.png)

Porygon is a python script which collects response metric like time, size and push it to loki.
- perform continuous or specified number of request
- provide a list of url to collect metric
- provides option to hit a single url or all the urls specified

```bash
python script.py --url_index {{index_from_urls.py}} --hit_count {{no_of_request_to_make}}

## the script has four modes
# 1. continuous mode which makes continuous request to all the urls 
python script.py

# 2. Hit count mode: Make specified no of request to all the urls in the urls.py
python script.py --hit_count {{no_request}}

# 3. specific url mode: Perform continuous request to the specified url by specifying index from urls.py
python script.py --url_index {{url_index}}

# 4. Hit Specific url with hit count: Specified no of request to specified url
python script.py --url_index {{url_index}} --hit_count {{no_request}}

```
## FolderContents
- dev-files: Useful commands 
- kubernetes: yaml files to run the script with multiple instance 
- loki-grafana: contains docker-compose file and command to setup loki and grafana 

## Setup
Although porygon is a simple script there a couple of options when using it.
You can run porygon using three methods.

**1. Running script only**
You can run porygon script as a simple script. But before running be sure to setup the .env and run loki and grafana.
1. Setup loki and grafana

**running using docker**


**running using kubernetes**
