from openai import OpenAI
from typing import Literal, List, Optional, Union, Sequence, Dict, Callable, Iterable
import os,json
from dataclasses import dataclass
from Sys_Prompt import get_template

from litellm import acompletion
from tenacity import retry, wait_random_exponential, stop_after_attempt
from protocol import ChatCompletionMessages, ChatCompletionResponse, FunctionCall, ToolMessage, Function, Tool, AssistantMessage, ChatMessage

@dataclass
class Response:
    response_text: str
    response_length: int
    prompt_length: int
    finish_reason: Literal["stop", "length"]
@dataclass
class Teacher:
    id : str
    department : str
    location : str
    identity : str = 'teacher'
@dataclass
class Student:
    id :str
    dormitory : str
    identity : str = 'student'
@dataclass
class User:
    info : str
    name : str
    # history : Sequence[Dict[str:Response]]=None
    Identity : Optional[Union[Teacher,Student]]=None
    

class AssistantAgent(object):
    '''
    个人Agent实例 
        1. 个人信息加载--存储信息
        2. 前后端消息传输
        3. 个人信息保存
        4. 建立连接接口 OpenAI
    '''
    def __init__(self,
                model : str,
                api_key : Optional[Union[str,None]] = None,
                url : Union[str,None]= None,
                tools : List[Dict]=None,
                tool_map: Optional[Dict[str,Callable]]=None,
                organization : Union[str,None]=None,
                name : Union[str,None]=None,
                identity : Union[str,None]=None,
                ):
        if not url:
            try:
                url = os.environ.get('OPENAI_BASE_URL') 
            except ValueError:
                raise ValueError('Need server url!')
        if api_key is None:
            try:
                api_key = os.environ.get("OPENAI_API_KEY")
            except ValueError:
                raise (
                    "The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable"
                )
        self.client = OpenAI(base_url=url,api_key=api_key)
        self.system_prompt = get_template(name,identity,organization)
        self.tools = tools
        self.tool_map = tool_map
        self.model = model


    async def execute_func_call(self,tool_call: FunctionCall) -> List[ChatCompletionMessages]:
        func_call=[]
        try:
            function_to_call = self.tool_map.get(tool_call.function.name)
        except ValueError:
            raise f'Error: function {tool_call.function.name} is not exists in tool_map!'
        try:
            function_args = json.loads(tool_call.function.arguments)
        except ValueError:
            raise f'Error: func Arguments aren\'t to uses!'
        
        try:
            function_response = function_to_call(
                    **function_args
                )
        except:
            func_call.append(AssistantMessage(role = 'assistant', content = None, function_call = Function(name=f"{tool_call.function.name}",arguments=f"{tool_call.function.arguments}")))
            func_call.append(ToolMessage(role ='function', name = f'{tool_call.function.name}', content = f"{function_response}"))
            raise f'Error: function {function_to_call} run error,detail{tool_call}'
        func_call.append(AssistantMessage(role = 'assistant', content = None, function_call = Function(name=f"{tool_call.function.name}",arguments=f"{tool_call.function.arguments}")))
        func_call.append(ToolMessage(role ='function', name = f'{tool_call.function.name}', content = f"{function_response}"))
        return func_call
            
    
    @retry(wait= wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(self,messages:List[ChatCompletionMessages], tool_choice=None) -> ChatCompletionResponse:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools
            )
            return response
        except Exception as e:
            raise  ("Unable to generate ChatCompletion response"
                    f'Exception: {e}')

    async def _call(self,
            messages:List[ChatCompletionMessages],
            ) ->List[ChatCompletionMessages]:
        response = self.chat_completion_request(messages=messages)

        if response.choices[0].finish_reason == 'tool_calls':
            try: 
                tool_calls = response.choices[0].message.tool_calls
            except:
                raise 'Tool call error!\nmessage:{response.choices[0].message}!'
            for tool_call in tool_calls:
                messages.extend(
                    await self.execute_func_call(
                                tool_call
                            )
                )
            print(messages)
            response = self.chat_completion_request(messages=messages)
            print(response)
        messages.append(AssistantMessage(role = response.choices[0].message.role,content = f'{response.choices[0].message.content}', function_call=response.choices[0].message.function_call))
        return messages
    
