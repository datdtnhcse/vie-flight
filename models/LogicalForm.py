import regex
from typing import List, Tuple
from abc import ABC, abstractmethod
from Models.IO import *
from Models.Const_flight import *

class LogicalForm(NLP):
    def __init__(self, relations: List[str]) -> None:
        super().__init__()
        self.mode = "WH"
        self.relations = relations
        self.verb = "ATTITUDE"

        for relation in self.relations:
            if "LOBJ" in relation:
                self.verb = "VERB"

        self.logicalForm = ["&"]


    def transform(self) -> Tuple[List[str], str]:
        for i in range(len(self.relations)):
            relation = regex.sub(r'[()]', "", self.relations[i])
            tokens = relation.split()

            if "PRED" in relation:
                self.logicalForm.append("({} {})".format(tokens[2], tokens[0]))
            elif "LSUBJ" in relation:
                if self.verb == "ATTITUDE":
                    self.logicalForm.append("(EXPERIENCER {} {})".format(tokens[0], tokens[2]))
                elif self.verb == "VERB":
                    self.logicalForm.append("(AGENT {} {})".format(tokens[0], tokens[2]))
            elif "LOBJ" in relation:
                self.logicalForm.append("(THEME {} {})".format(tokens[0], tokens[2]))
            elif "PFROM" in relation:
                self.logicalForm.append("(FROM_LOC {} {} {})".format("fl", tokens[0], tokens[2]))
            elif "PTO" in relation:
                self.logicalForm.append("(TO_LOC {} {} {})".format("tl", tokens[0], tokens[2]))
            elif "NMOD" in relation:
                self.logicalForm.append("(NMOD {} {})".format(tokens[0], tokens[2]))
            elif "WHQUERY" in relation:
                self.mode = "WH"
                if "WHICH" in relation:
                    subj = tokens[2][1:-1].split('-')[2]
                    self.relations = [ele.replace(subj, tokens[2]) for ele in self.relations]
                elif "WHEN" in relation and "TIME" in relation:
                    self.logicalForm.append("(AT_TIME {} {})".format(tokens[0], tokens[2]))
                elif "WHAT" in relation and "TIME" in relation:
                    self.logicalForm.append("(RUN_TIME {} {})".format(tokens[0], tokens[2]))
            elif "YNQUERY" in relation:
                self.mode = "YN"
            elif "TIME" in relation:
                self.logicalForm.append("(AT_TIME {} {})".format(tokens[0], tokens[2]))

        return self.logicalForm, self.mode


    def __str__(self) -> str:
        logicalForm = " ".join(ele for ele in self.logicalForm)

        if self.mode == "WH":
            logicalForm = "(WH-QUERY(" + logicalForm + "))"
        elif self.mode == "YN":
            logicalForm = "(YS-QUERY(" + logicalForm + "))"

        logicalForm = logicalForm.replace("-", " ").replace("[", "(").replace("]", ")")
        return "-------- Logical Form --------\n" + logicalForm + "\n------------------------------\n\n\n"