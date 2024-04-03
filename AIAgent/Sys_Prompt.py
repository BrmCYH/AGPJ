'''
    Define the prompt of AIAgent
'''
from typing import Optional,List,Literal,Dict
from dataclasses import dataclass
@dataclass
class Template:
    role: Literal['system']
    content: str
templates:Dict[str,Template]={}
def _register_sys_template(
    name: str,
    default_system: str
    ) -> None:
    templates[name]=Template(
        role='system',
        content=default_system
    )

_register_sys_template(
    name="Phoenix_assistants",
    default_system=
        "A chat between a curious user and an artificial intelligence assistant. "
)
def get_template(name:str=None,identity:str=None,organization:str=None):
    if not( name or identity or organization):
        
        return [{'role':'system',"content":'A chat between a curious user and an artificial intelligence assistant. '}]
    if name:
        if name in templates.keys():
            return list(templates[name])
        else: 
            raise ValueError('name is not exist!')
    return []