'''
Tools type define
'''
import json
from typing import Sequence
def calculate_gpa(grades: Sequence[str],hours: Sequence[int]) -> float:
    grade_to_score = {"A": 4, "B": 3, "C": 2}
    total_score, total_hour = 0, 0
    for grade, hour in zip(grades, hours):
        total_score += grade_to_score[grade] * hour
        total_hour += hour
    return total_score / total_hour

Tool_map = {
    "calculate_gpa":calculate_gpa,
}

