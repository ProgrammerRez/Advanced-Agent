import requests
from schema import APIInput
from dotenv import load_dotenv
import os
load_dotenv()

url = 'https://advanced-agent-production.up.railway.app/research_agent/'
topic = 'String Theory'
mode = 'shallow'

state = APIInput(query=topic,mode=mode)

try:
    response = requests.post(url=url, json=state.model_dump(),params={'api_key':os.getenv('RESEARCH_API_KEY')})

    response.raise_for_status()
    print(response.json())
except Exception as e:
    print(e)