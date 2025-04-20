import requests
import time
import csv
import os


SERVER_URL = os.environ['REQUEST_HOST']
RESULT_FILE = "performance_results.csv"

def test_endpoint(endpoint, index):
    url = f"{SERVER_URL}{endpoint.replace("value", f"{index}")}"
    start_time = time.time()

    try:
        response = requests.get(url)
        response_time = time.time() - start_time
        status_code = response.status_code
        response_length = len(response.content)

        return {
            "endpoint": endpoint,
            "index": index,
            "status_code": status_code,
            "response_time": response_time,
            "response_length": response_length
        }
    except Exception as e: 
        return {
            "endpoint": endpoint,
            "status_code": "Error",
            "response_time": "N/A",
            "response_length": "N/A",
            "error": str(e)
        }
    

def run_tests():
    results = []


    with open(RESULT_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        while True:
            result = test_endpoint(endpoint.get('path'))
            results.append(result)
    


if __name__ == "__main__":
    run_tests()
