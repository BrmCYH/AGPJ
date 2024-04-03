'''
Tools type define
'''
import json
from typing import Sequence, Callable
from protocol import Tool
import inspect
class Tools:

    @classmethod
    def calculate_gpa(cls, grades: Sequence[str],hours: Sequence[int]) -> float:
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
    Tool_map={}
    def load_Tool(files):
        import json
        try:
            Tool_Definition=json.load(open(files,'r',encoding='utf-8'))
        except FileNotFoundError:
            raise f'Tool json file is not found.Path: {files}'
        return Tool_Definition
    
    def Tool_Compare(Tool_Map):

        functions = dir(Tools)
        print(functions)
        
        pass
    Tool_map = load_Tool(files)
    print(Tool_map)
    tool = Tool_Compare(Tool_map)
    return tool,Tool_map
    


Tool_map = {
    "calculate_gpa": Tools.calculate_gpa,
}

def main():
    tup=Load_Map('tools.json')
if __name__=="__main__":
    main()
    