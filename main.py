"""
下車飯の路線名および駅名のリアルタイムサジェスト機能のためのAPI
"""
from fastapi import FastAPI, Query
import uvicorn

from typing import List

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/line")
def prac(line_name: str = Query(None)) -> list:
    """
    実験用関数
    e.g.) "東急"
    """
    prac_list = ['東急東横線', '東急大井町線', 'JR山手線', '東急田園都市線']
    partial_matches = [line for line in prac_list if line_name in line]
    return [line_name, partial_matches]


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
