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
from Funcs import Load_Map

# os.chdir('AIAgent')
tool_file = 'tools.json'
def main():
    os.environ['OPENAI_BASE_URL']='base_url'
    os.environ['OPENAI_API_KEY'] = 'apikey'
    api_key = os.environ.get('OPENAI_API_KEY',None)
    base_url = os.environ.get("OPENAI_BASE_URL",None)

    Tool_map , tools = Load_Map(tool_file)
    Model = 'gpt-3.5-turbo'
    agent = AssistantAgent(api_key=api_key,url=base_url,tools=tools,tool_map=Tool_map,model=Model)
    app= run_agent(agent)

    uvicorn.run(app, host='127.0.0.1',port=int(os.environ.get('API_PORT',8000)),workers=1)
    

if __name__=="__main__":
    main()