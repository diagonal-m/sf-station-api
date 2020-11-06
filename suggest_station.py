"""
下車飯の路線名および駅名のリアルタイムサジェスト機能のためのクラスを配置するモジュール
"""
import re
import pandas as pd
import MeCab
from pykakasi import kakasi
from Levenshtein import distance as levenshtein

from typing import List


class BaseSuggest:
    """
    ベースサジェストクラス
    """
    def __init__(self):
        """
        初期化メソッド
        """
        k = kakasi()
        k.setMode('K', 'a')
        self.conv = k.getConverter()
        self.tagger = MeCab.Tagger('-d /var/lib/mecab/dic/debian')
        self.df = pd.read_csv('data/station.csv', encoding='cp932')

    def _katakanize(self, text: str) -> str:
        """
        文字列をカタカナにする

        @param text: 入力文字列
        @return: カタカナ文字列
        """
        morphed = [re.split(r"[,\t\s\n]", w) for w in self.tagger.parse(text).split("\n")]
        morphed.remove([""])
        morphed.remove(["EOS"])
        k = [morph[-1] if morph[-1] != "*" else morph[0] for morph in morphed]

        return "".join(k)

    def romanaize(self, text: str) -> list:
        """
        カタカナ文字列をローマ字にして返す

        @param text: カタカナ文字列
        @return: ローマ字に変換済みの文字列
        """
        katakana = self._katakanize(text)

        if type(katakana) == str:
            katakana = [katakana]

        return [self.conv.do(k) for k in katakana]


class LineSuggest(BaseSuggest):
    """
    路線名サジェストクラス
    """
    def __init__(self, line_name: str):
        """
        初期化メソッド
        @param line_name: 入力路線名
        """
        super().__init__()
        self.line = line_name

    def suggest(self) -> list:
        """
        入力された路線名について部分一致路線名かレーベンシュタイン距離が近いものを返す

        @return: 路線名サジェスト e.g.) [{"line_name": line_name1}, {"line_name": line_name2}...]
        """
        roman_lines = list(self.df['line_name_roman'].unique())
        lines = list(self.df['line_name'].unique())
        partial_matches = [line for line in lines if self.line in line]
        if len(partial_matches) > 0:
            return [line for line in partial_matches[:10]]
        inputed_line_roman = self.romanaize(self.line)[0]
        dists = [levenshtein(inputed_line_roman, roman_line) for roman_line in roman_lines]
        idx = sorted(range(len(dists)), key=lambda x: dists[x])[:10]
        return [lines[i] for i in idx]


class StationSuggest(BaseSuggest):
    """
    駅名サジェストクラス
    """
    def __init__(self, line_name: str, station_name: str):
        """
        初期化メソッド
        @param line_name:
        @param station_name:
        """
        super().__init__()
        self.line = line_name
        self.station = station_name

    def suggest(self) -> List[dict]:
        """
        入力された路線名についてレーベンシュタイン距離が近い駅を返す
        @return: 駅名サジェスト e.g.) [{"station_name": station_name1}, {"station_name": station_name2}...]
        """
        roman_stations = self.df[self.df['line_name'] == self.line]['station_name_roman'].to_list()
        stations = self.df[self.df['line_name'] == self.line]['station_name'].to_list()
        inputed_station_roman = self.romanaize(self.station)[0]
        dists = [levenshtein(inputed_station_roman, roman_station) for roman_station in roman_stations]
        idx = sorted(range(len(dists)), key=lambda x: dists[x])[:10]

        return [{"station_name": stations[i]} for i in idx]
