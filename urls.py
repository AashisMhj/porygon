import os
from dotenv import load_dotenv

load_dotenv()
SERVER_URL = os.environ.get('SERVER_URL')

endpoint_urls = [
    {
        "method": 'GET',
        "url": f"{SERVER_URL}/data",
    },
    {
        "method": "GET",
        "url": f"{SERVER_URL}/large-data?n=%n%",
    },
    {
        "method": "POST",
        "url": f"{SERVER_URL}/add",
        "data": [
            {
            "name": "The Name"
        }]
    },
    {
        "method": "GET",
        "url": f"{SERVER_URL}/fibonacci?n=%n%"
    },
    {
        "method": "GET",
        "url": f"{SERVER_URL}/info"
    },
    {
        "method": "GET",
        "url": f"{SERVER_URL}/generate-file"
    },
    {
        "method": "GET",
        "url": f"{SERVER_URL}/file"
    },
    {
        "method": "GET",
        "url": f"{SERVER_URL}/stream"
    }

]