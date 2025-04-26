import urllib.request
import requests
import time
import os
import json
import time
import argparse
import threading
import queue
from dotenv import load_dotenv
from urls import endpoint_urls

load_dotenv()

parser = argparse.ArgumentParser(description="Script to collect metric of url response")
parser.add_argument("--url-index", help="The index of the url")
LOKI_URL = os.environ.get('LOKI_URL')
SERVER_LABEL = os.environ.get('SERVER_URL')
LOG_BUFFER_TIME = 5

log_queue = queue.Queue()

def log_worker():
    while True:
        time.sleep(LOG_BUFFER_TIME)
        entries = []
        while not log_queue.empty():
            entry, labels = log_queue.get()
            entries.append(entry)

        if entries:
            send_log_to_loki(entry, labels)

threading.Thread(target=log_worker, daemon=True).start()

def send_log_to_loki(entries, labels=None):
    if labels is None:
        labels = {"job": "url-monitor"}
    payload = {
        "streams": [
            {
                "labels": "{" + ",".join([f'{k}="{v}"' for k, v in labels.items()]) + "}",
                "entries": [{
                    "ts": str(int(time.time() * 1e9)),
                    "line": json.dumps(entries)
                }]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        res = requests.post(f"{LOKI_URL}/loki/api/v1/push", headers=headers, data=json.dumps(payload))
    except Exception as e:
        print(f"[ERROR] Failed to send log to loki: {e}")

def hit_url(url_obj, value=None):
    try:
        start_time =time.time()
        url = url_obj['url'].replace('{{s}}', value) if value else url_obj['url']
        payload = json.dumps(url_obj.get('data')).encode('utf-8') if url_obj.get('url') else None
        req = urllib.request.Request(url,headers={'Content-Type': 'application/json'}, method=url_obj['method'], data=payload)

        with urllib.request.urlopen(req) as response:
            end_time = time.time()

            status = response.getcode()
            time_taken = end_time - start_time
            headers = response.getheaders()
            server = dict(headers).get('Server', 'Unknown')
            content = response.read()
            content_size = len(content)
            data = {
                "status": status,
                "time_taken": time_taken,
                "headers": headers,
                "server": server,
                "content_size": content_size
            }
            labels = {
                "server": SERVER_LABEL
            }
            log_queue.put((data, labels))
    except Exception as e:
        log_queue.put((str(e), {"type": f"{SERVER_LABEL}-error"}))
        error_message = f"[ERROR] {i} {type(e).__name__}: {str(e)}"
        print(error_message, url_obj['url'])

if __name__ == "__main__":
    args = parser.parse_args()

    if (args.url_index):
        url_index = int(args.url_index)
        if url_index > len(endpoint_urls) -1:
            exit
        print(f"Starting url: {endpoint_urls[url_index]} {url_index}")
        while True:
            hit_url(endpoint_urls[url_index])
            time.sleep(1)

    else:
        for url in endpoint_urls:
            print(f"Starting url: {url['url']}")
            for i in range(10000):
                hit_url(url, f"{i}")
                time.sleep(1)
            
    
