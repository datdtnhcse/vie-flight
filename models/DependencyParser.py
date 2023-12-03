import regex
from typing import List, Tuple
from abc import ABC, abstractmethod
from Models.IO import *
from Models.Const_flight import *

class DependencyParser(NLP):
    def __init__(self, tokens: List[str], types: List[str]) -> None:
        super().__init__()
        self.SHIFT = 0
        self.RIGHTARC = 1
        self.LEFTARC = 2
        self.REDUCE = 3
        self.operator = {0: "SHIFT", 1: "RIGHTARC", 2: "LEFTARC", 3: "REDUCE"}
        self.step = []
        self.relations = []
        self.stack = [("Root", "Root")]
        self.buffer = list(zip(tokens, types))

    def transform(self) -> List[str]:
        """ MaltParser arc-eager """

        while len(self.buffer) > 0:
            print("buffer",self.buffer)
            print("stack",self.stack)
            token = self.buffer[0]
            word = self.stack[-1]
            op, relation = self.__selectOp(word[1], token[1])

            if op == self.SHIFT:
                relation = ""
                self.stack.append(token)
                del self.buffer[0]
            elif op == self.RIGHTARC:
                relation = "({}, {}, {})".format(relation, word[0], token[0])
                self.relations.append(relation)
                self.stack.append(token)
                del self.buffer[0]
            elif op == self.LEFTARC:
                relation = "({}, {}, {})".format(relation, token[0], word[0])
                self.relations.append(relation)
                del self.stack[-1]
            elif op == self.REDUCE:
                relation = ""
                del self.stack[-1]

            self.step.append("{}\t{}\t{}\t{}".format(self.operator[op], str([ele[0] for ele in self.stack]), str([ele[0] for ele in self.buffer]), relation))

        return self.relations.copy()


    def __selectOp(self, stackType: str, buffType: str) -> Tuple[int, str]:
        if buffType == "Noun":
            if stackType == "Root":
                return self.SHIFT, None
            elif stackType == "Noun" and (len(self.stack) <= 2 or self.stack[-2][1] != "Noun"):
                return self.RIGHTARC, "nmod"
            elif stackType == "WH":
                return self.LEFTARC, "nmod"
            elif stackType == "OVerb":
                return self.RIGHTARC, "dobj"
            elif stackType == "Prep":
                return self.RIGHTARC, "pobj"
            elif stackType == "Aux":
                return self.RIGHTARC, "nmod"
        elif buffType == "WH":
            if stackType == "IVerb" or stackType == "OVerb":
                return self.SHIFT, None
            elif stackType == "Noun" and (len(self.stack) <= 2 or self.stack[-2][1] != "Noun"):
                return self.RIGHTARC, "whmod"
            elif stackType == "Aux" or stackType == "Prep":
                return self.RIGHTARC, "whmod"
        elif buffType == "IVerb":
            if stackType == "Root":
                return self.RIGHTARC, "root"
            elif stackType == "Noun" and (len(self.stack) <= 2 or self.stack[-2][1] != "Noun"):
                return self.LEFTARC, "subj"
            elif stackType == "Aux":
                return self.LEFTARC, "aux"
        elif buffType == "OVerb":
            if stackType == "Root":
                return self.RIGHTARC, "root"
            elif stackType == "Noun" and (len(self.stack) <= 2 or self.stack[-2][1] != "Noun"):
                return self.LEFTARC, "subj"
            elif stackType == "Aux":
                return self.LEFTARC, "aux"
        elif buffType == "Prep":
            if stackType == "IVerb" or stackType == "OVerb":
                return self.RIGHTARC, "pmod"
            elif stackType == "Noun":
                return self.RIGHTARC, "timemod"
        elif buffType == "Aux":
            if stackType == "IVerb" or stackType == "OVerb":
                return self.RIGHTARC, "aux"
            elif not list(filter(lambda x: "root" in x, self.relations)):
                return self.SHIFT, None
        elif buffType == "Time":
            if stackType == "Aux" and (len(self.stack) < 2):
                return self.RIGHTARC, "timemod"
            else:
                return self.RIGHTARC, "rtimemod"
        elif buffType == "ID":
            if stackType == "Noun":
                return self.RIGHTARC, "idmod"
        elif buffType == "Name":
            if stackType == "Noun":
                return self.RIGHTARC, "namemod"
            elif stackType == "Prep":
                return self.RIGHTARC, "pobj"
        elif buffType == "Punc":
            if stackType == "IVerb" or stackType == "OVerb":
                return self.RIGHTARC, "punc"

        return self.REDUCE, None


    def __str__(self) -> str:
        stepStr = "\n".join(step for step in self.step)
        relationStr = " ".join(relation for relation in self.relations)
        return "----- Dependency Parsing -----\n" + stepStr + "\n\n" + relationStr + "\n------------------------------\n\n\n"