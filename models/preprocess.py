from unicodedata import normalize
from underthesea import word_tokenize
import re

import regex
from typing import List, Tuple
from abc import ABC, abstractmethod
from Models.IO import *
from Models.Const_flight import *

class PreProcessing:
    instance = None

    @staticmethod
    def getInstance():
        if not PreProcessing.instance:
            PreProcessing.instance = PreProcessing()

        return PreProcessing.instance


    def tokenize(self, text: str) -> List[str]:
        """
        Remove unknown words and add time expressions to POS dictionary.
        Return a list of preprocessed tokens from the given text.
        """

        text = normalize("NFC", text)

        # Remove redundant whitespaces
        text = re.sub(r"\s{2,}", " ", text)

        # Add space before question mark
        text = re.sub(r"(.)\?", r"\1 ?", text)

        text = text.replace(" HR","HR").replace("Tp.","Tp. ").replace("TP.","TP. ")

        text = text.strip().replace("  "," ")
        if text[-1] == ".":
            text = text[:-1]

        text =word_tokenize(text, format="text")

        text = text.lower()

        for phrase, word in PHARSE:
            text = text.replace(phrase, word)

        text = re.sub(r'\b(\d+)\s*:\s*(\d+hr)\b', r'\1:\2', text)
        text = re.sub(r'\b(\d+) giờ',r'\1:00hr',text)
        return text.split()

    def getWordTypes(self, tokens: List[str]) -> List[str]:
        types = []

        for i, token in enumerate(tokens):
            if token in DICTIONARY:
                if isinstance(DICTIONARY[token], str):
                    types.append(DICTIONARY[token])
                else:
                    index = i
                    while index > 0:
                        index -= 1
                        if types[index] == "Prep":
                            types.append(DICTIONARY[token][1])
                            break
                    else:
                        types.append(DICTIONARY[token][0])
            elif token in PLACE:
                types.append("Name")
            else:
                types.append("ID" if regex.search("b\d", token) else "Time")


        return types