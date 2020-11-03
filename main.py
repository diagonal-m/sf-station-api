"""
下車飯の路線名および駅名のリアルタイムサジェスト機能のためのAPI
"""
from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
