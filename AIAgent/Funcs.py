'''
Tools type define
'''
import json
from typing import Sequence, Callable, Dict, List
from protocol import Tool
import inspect
class Tools:
    def __init__(self):
        self.functions = {}


    def register_function(self, func):
        self.functions[func.__name__] = func
        
    

def calculate_gpa(grades: Sequence[str],hours: Sequence[int]) -> float:
    grade_to_score = {"A": 4, "B": 3, "C": 2}
    total_score, total_hour = 0, 0
    for grade, hour in zip(grades, hours):
        total_score += grade_to_score[grade] * hour
        total_hour += hour
    return total_score / total_hour



def Load_Map(files:str):
    '''
    返回 Tool 与 Tool_map
    '''
    tools = Tools()
    def load_Tool(files:str=None):
        import json
        try:
            Tool_Definition=json.load(open(files,'r',encoding='utf-8'))
        except FileNotFoundError:
            raise f'Tool json file is not found.Path: {files}'
        return Tool_Definition
    
    Tool_Definition = load_Tool(files)
    
    for itm in Tool_Definition:
        try: 
            tools.register_function(eval(f"{itm['function']['name']}"))
        except:
            continue
     
    return tools.functions , Tool_Definition




def main():
    tup=Load_Map('tools.json')
    
if __name__=="__main__":
    main()
    