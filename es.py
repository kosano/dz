import requests
import json


HOST = 'http://node01:9200/poi/info/_search'

def search(kw):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"query": {"term": {"poiCenter.keyword": f"{kw}"}}})
    return requests.post(HOST, headers=headers, data=data).json()