import urllib.request
import requests
import time
import os
import json
import time
import argparse
import threading
import queue
import signal
import sys
from dotenv import load_dotenv
from urls import endpoint_urls

load_dotenv()

parser = argparse.ArgumentParser(description="Script to collect metric of url response")
parser.add_argument("--url-index", help="The index of the url")
LOKI_URL = os.environ.get('LOKI_URL')
SERVER_LABEL = os.environ.get('SERVER_LABEL')
LOG_BUFFER_TIME = 10; # 10 second
ERROR_LOG_BUFFER_TIME = 30; # 30 second

log_queue = queue.Queue()
error_log_queue = queue.Queue()

labels = {"job": SERVER_LABEL}

def flush_remaining_logs_and_exit(signum, frame):
    print("\n[INFO] Flushing remaining logs before exit...")
    entries = []
    
    timestamp = str(int(time.time() * 1e9))

    while not log_queue.empty():
        entry, timestamp = log_queue.get()
        entries.append([timestamp, entry])

    if entries:
        send_log_to_loki(entries, timestamp, labels)

    print("[INFO] Cleanup complete. Exiting.")
    sys.exit(0)


def log_worker():
    while True:
        time.sleep(LOG_BUFFER_TIME)
        entries = []
        while not log_queue.empty():
            entry, timestamp = log_queue.get()
            entries.append(entry)

        if entries:
            send_log_to_loki(entries, timestamp, labels)

threading.Thread(target=log_worker, daemon=True).start()

def send_log_to_loki(entries, timestamp, labels=None):
    if labels is None:
        labels = {"job": SERVER_LABEL}
    payloadEntries = []
    for entry in entries:
        payloadEntries.append([timestamp, json.dumps(entry)])

    payload = {
        "streams": [
            {
                "stream": labels,
                "values": payloadEntries
            }
        ]
    }
   
    try:
        res = requests.post(f"{LOKI_URL}/loki/api/v1/push", json=payload)
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
                "job": SERVER_LABEL
            }

            log_queue.put((data, str(int(time.time() * 1e9)), labels))
    except Exception as e:
        log_queue.put((str(e),  str(int(time.time() * 1e9)),{"job": f"{SERVER_LABEL}-error"}))
        error_message = f"[ERROR] {i} {type(e).__name__}: {str(e)}"
        print(error_message, url_obj['url'])

if __name__ == "__main__":
    signal.signal(signal.SIGINT, flush_remaining_logs_and_exit)
    signal.signal(signal.SIGTERM, flush_remaining_logs_and_exit)

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
        i = 0
        while True:
            print(f"Starting url: {url['url']}")
            for i in range(10000):
                hit_url(url, f"{i}")
                time.sleep(1)
            
    
