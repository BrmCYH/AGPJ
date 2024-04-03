import time
from enum import Enum, unique
from typing import List, Optional, Dict, Union, Callable, Literal

from pydantic import BaseModel, Field


@unique
class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"
    TOOL = "tool"


@unique
class Finish(str, Enum):
    STOP = "stop"
    LENGTH = "length"
    TOOL = "tool_calls"

class ChatMessage(BaseModel):
    role: Optional[Role]
    content: str

class ToolMessage(BaseModel):
    role: Optional[Role]
    content: str
    name: str
    
ChatCompletionMessages = Union[
    ChatMessage,
    ToolMessage,
]


class Function(BaseModel):
    name: str
    arguments: str


class FunctionCall(BaseModel):
    id: Literal["call_default"] = "call_default"
    type: Literal["function"] = "function"
    function: Function



class ChatCompletionMessage(BaseModel):
    role: Optional[Role] = None
    content: Optional[str] = None
    tool_calls: Optional[List[FunctionCall]] = None



class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    tools: list = []
    do_sample: bool = True
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: int = 1
    max_tokens: Optional[int] = None
    stream: bool = False


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: Finish


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: ChatCompletionMessage
    finish_reason: Optional[Finish] = None


class ChatCompletionResponseUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: Literal["chatcmpl-default"] = "chatcmpl-default"
    object: Literal["chat.completion"] = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: ChatCompletionResponseUsage


class ChatCompletionStreamResponse(BaseModel):
    id: Literal["chatcmpl-default"] = "chatcmpl-default"
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionResponseStreamChoice]


class ScoreEvaluationRequest(BaseModel):
    model: str
    messages: List[str]
    max_length: Optional[int] = None


class ScoreEvaluationResponse(BaseModel):
    id: Literal["scoreeval-default"] = "scoreeval-default"
    object: Literal["score.evaluation"] = "score.evaluation"
    model: str
    scores: List[float]

# Model List
class ModelCard(BaseModel):
    id: str
    object: Literal["model"] = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: Literal["owner"] = "owner"


class ModelList(BaseModel):
    object: Literal["list"] = "list"
    data: List[ModelCard] = []

class Tool(BaseModel):
    name: str
    function: Callable

