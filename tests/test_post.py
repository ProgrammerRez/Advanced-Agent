import requests
from schema import APIInput


url = 'http://127.0.0.1:8000/research_agent'
topic = 'String Theory'
mode = 'shallow'

state = APIInput(query=topic,mode=mode)

try:
    response = requests.post(url=url, json=state.model_dump())

    response.raise_for_status()
    print(response.json())
except Exception as e:
    print(e)