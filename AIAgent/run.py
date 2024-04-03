from typing import TYPE_CHECKING, List, Iterable
from fastapi import FastAPI, status, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
import os
from Agent import AssistantAgent
from enum import unique, Enum
from protocol import (
    ChatCompletionMessages,
    ChatMessage,
    Role,
    ScoreEvaluationRequest,
    ScoreEvaluationResponse,
)
@unique
class DataRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"
    OBSERVATION = "observation"

def run_agent(agent:AssistantAgent) -> "FastAPI":
    app = FastAPI()
    role_mapping = {
        Role.USER: DataRole.USER.value,
        Role.ASSISTANT: DataRole.ASSISTANT.value,
        Role.SYSTEM: DataRole.SYSTEM.value,
        Role.FUNCTION: DataRole.FUNCTION.value,
        Role.TOOL: DataRole.OBSERVATION.value,
    }
    @app.get('/')
    async def index():
        RedirectResponse('/v1/models')
    @app.get('/v1/models')
    async def list_models():
        
        # if url is None:
        url = os.environ.get("OPENAI_BASE_URL",None)
        if url is None :
            raise ValueError('Redirection url have not given.')
        response = RedirectResponse(url+'/models')
        return response
    @app.post('/v1/chat/completions',status_code=status.HTTP_200_OK,response_model=List[ChatCompletionMessages])
    async def create_chat_completion(request: ChatMessage):
        input_messages=[]
        input_messages.extend(agent.system_prompt)if agent.system_prompt  else[]
        input_messages.append(ChatMessage(role=role_mapping[request.role], content=request.content))
        response = await agent._call(messages=input_messages) # 返回的异步内容 coroutine对象 需要通过await来解析
        return response
    return app