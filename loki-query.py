import requests
import time
from datetime import datetime

# Set your Loki URL here
LOKI_URL = "http://localhost:3100/loki/api/v1/query_range"

# Query parameters (adjust to your needs)
query = '{server="gin-server"}'  # Example: replace with your log query
limit = 100  # Max number of log entries to retrieve

# Time range (last 1 hour)
end = int(time.time() + (3600 * 24 * 5))  # Current time (in seconds)
start = end - (3600 * 24 * 10)  # 1 hour ago (in seconds)

# Convert to nanoseconds (Loki expects Unix timestamps in nanoseconds)
start_ns = start * 1000000000  # Convert start time to nanoseconds
end_ns = end * 1000000000  # Convert end time to nanoseconds

# Make the GET request to Loki API
params = {
    'query': query,
    'start': "1745236803446085110",
    'end': "1745236803446085125",
    'limit': str(limit)
}

headers = {
    'Content-Type': 'application/json'
}

try:
    response = requests.get(LOKI_URL, params=params, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()  # Get the JSON response
        if data.get('streams'):
            # Print logs in a readable format
            for stream in data['streams']:
                for entry in stream['entries']:
                    timestamp = entry['ts']
                    log_message = entry['line']
                    print(f"{timestamp}: {log_message}")
        else:
            print("No logs found for the given query and time range.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

except Exception as e:
    print(f"Failed to query Loki: {e}")
