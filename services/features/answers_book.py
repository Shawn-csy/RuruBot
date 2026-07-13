"""
解答之書 feature

從 statics/answersbook.json 隨機抽一條答案。
"""
import json
import os
import random
from typing import Optional


def get_answer() -> Optional[str]:
    """隨機抽一條答案，回傳繁體中文文字。"""
    json_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../../statics/answersbook.json'
    )
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    key = random.choice(list(data.keys()))
    return data[key]["answer"]["zh-TW"]
