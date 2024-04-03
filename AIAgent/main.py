'''
访问接口
'''
import os
import json
from typing import TYPE_CHECKING,Sequence,Dict
import argparse
import uvicorn
from fastapi import FastAPI
from run import run_agent
from Agent import AssistantAgent

from Tools import Tool_map

# os.chdir('AIAgent')
tool_file = 'tools.json'
def main():
    os.environ['OPENAI_BASE_URL']='baseurl'
    os.environ['OPENAI_API_KEY'] = 'key'
    api_key = os.environ.get('OPENAI_API_KEY',None)
    base_url = os.environ.get("OPENAI_BASE_URL",None)
    tools = json.load(open(tool_file,'r',encoding='utf-8'))
    Model = 'gpt-4-0125-preview'
    agent=AssistantAgent(api_key=api_key,url=base_url,tools=tools,tool_map=Tool_map,model=Model)
    app= run_agent(agent)

    uvicorn.run(app, host='127.0.0.1',port=int(os.environ.get('API_PORT',8000)),workers=1)
    

if __name__=="__main__":
    main()