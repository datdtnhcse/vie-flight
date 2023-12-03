import regex
from typing import List, Tuple
from abc import ABC, abstractmethod
from Models.IO import *

PHARSE = (
    ("tàu hỏa", "tàu_hỏa"),
    ("thời gian", "thời_gian"),
    ("thành phố", "thành_phố"),
    ("tp.", "thành_phố "),
    ("đà nẵng", "đà_nẵng"),
    ("nha trang", "nha_trang"),
    ("hồ chí minh", "hồ_chí_minh"),
    ("hà nội", "hà_nội"),
    ("mấy giờ", "mấy_giờ")
)


DICTIONARY = {
    "Root": "Root",
    "tàu_hỏa" : "Noun",
    "thời_gian": "Noun",
    "thành_phố": "Noun",
    "nào": "WH",
    "đến": ("OVerb", "Prep"),
    "mấy_giờ": "WH",
    "chạy": "IVerb",
    "từ": "Prep",
    "là": "Aux",
    "lúc": "Aux",
    "không": "Aux",
    "có": "Aux",
    ",": "Punc",
    "?": "Punc",
    ".": "Punc",
}


PLACE = (
    "hà_nội", "đà_nẵng", "hồ_chí_minh", "nha_trang", "huế",
)


MAPPING = {
    "thời_gian": "TIME",
    "từ": "LEAVE",
    "đến": "ARRIVE",
    "chạy": "RUN",
    "tàu_hỏa": "TRAIN",
    "nào": "WHICH",
    "mấy_giờ": "TIME",
    "là": "WHAT",
    "lúc": "WHEN",
    "có": "YESNO",
    "không": "YESNO",
    "huế": "HUE",
    "nha_trang": "NTRANG",
    "hà_nội": "HN",
    "đà_nẵng": "DANANG",
    "hồ_chí_minh": "HCM",
}

class NLP(ABC):
    def __init__(self) -> None:
        self.variable = []


    def createVariable(self, word: str) -> str:
        i = 0
        while True:
            i += 1
            var = word+str(i)
            if not var in self.variable:
                return var


    @abstractmethod
    def transform(self):
        pass