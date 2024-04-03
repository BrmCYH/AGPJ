from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional,Union,Literal
@unique
class Role(str, Enum):
    USER :Literal['user','teacher','student'] = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = "system"
    FUNCTION = "function"
    TOOL = "tool"

