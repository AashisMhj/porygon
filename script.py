import requests
import time
import csv

SERVER_URL = "http://localhost:5000"
ENDPOINTS = [
    { "path": "/fibonacci", "query_param": "?n=value"},
    { "path": "/intensive-cpu", "query_param": "?iterations=value"},
    { "path": "/info"},
    { "path": "/large-data", "query_param": "?size=value"},
    { "path": "/file-write", "query_param": "?size=value"},
    { "path": "/file-read"},
    { "path": "/stream"},
]

RESULT_FILE = "performance_results.csv"

def test_endpoint(endpoint, params=""):
    url = f"{SERVER_URL}{endpoint}{params}"
    start_time = time.time()

    try:
        response = requests.get(url)
        response_time = time.time() - start_time
        status_code = response.status_code
        response_length = len(response.content)

        return {
            "endpoint": endpoint,
            "params": params,
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


    for endpoint in ENDPOINTS:
        for i in range(2000):
            key = 'query_param'
            param = endpoint.get(key).replace('value', f"{i}") if key in endpoint else endpoint.get(key)
            result = test_endpoint(endpoint.get('path'), param)
            results.append(result)
    
    with open(RESULT_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to {RESULT_FILE}")

if __name__ == "__main__":
    run_tests()
