# Porygon
![porygon](./images/porygon-image.png)

Porygon is a python script to make continus request to you server and collect response metric. 
The script makes request to a url and sends the logs to loki in the batch every 10 seconds.

You can either run the script to make continous request to a single or multiple urls.
Specify the urls that you would like to hit in the urls.py.

```bash
# make continus request to single url
python script.py --url_index {{index_from_urls.py}}

## to make continus request to all the urls in urls.py
python script.py
## this will make continuous request making 10000 request to each urls as a time
```

## Contents
- dev-files:
- kubernetes:
- loki-grafana:

## Setup
You can run the application using docker, kubernetes or just script.

**running script only**
You run the script directly 

**running using docker**


**running using kubernetes**
