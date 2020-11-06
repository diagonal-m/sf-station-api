"""
下車飯の路線名および駅名のリアルタイムサジェスト機能のためのAPI
"""
from fastapi import FastAPI, Query
import uvicorn
from suggest_station import LineSuggest, StationSuggest

from typing import List

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/line")
def suggest_line(line_name: str = Query(None)) -> List[dict]:
    """
    入力された路線名に対してサジェストを返す
    "/line?line_name=路線名"

    @param line_name: 入力路線名
    @return: 路線名サジェスト e.g.) [{"line_name": line_name1}, {"line_name": line_name2}...]
    """
    ls = LineSuggest(line_name)
    print(ls.suggest())
    return ls.suggest()


@app.get("/station")
def suggest_line(line_name: str = Query(None), station_name: str = Query(None)) -> List[dict]:
    """
    入力された路線名に対してサジェストを返す
    "/line?line_name=路線名&station_name=駅名"

    @param line_name: 入力路線名(正しい路線名)
    @param station_name: 入力駅名
    @return: 駅名サジェスト e.g.) [{"station_name": station_name1}, {"station_name": station_name2}...]
    """
    ss = StationSuggest(line_name, station_name)
    return ss.suggest()


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
