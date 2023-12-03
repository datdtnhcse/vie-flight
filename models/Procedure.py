import regex
from typing import List, Tuple
from abc import ABC, abstractmethod
from Models.IO import *
from Models.Const_flight import *

class Procedure(NLP):
    def __init__(self, logicalForm: List[str], mode: str) -> None:
        super().__init__()
        self.logicalForm = logicalForm
        self.mode = mode
        self.subj = []
        self.action = None
        self.varmap = {"TRAIN": "t", "STIME": "st", "DTIME": "dt", "RUN_TIME": "rt"}
        self.variables = ["t", "st", "dt", "rt", "s", "d"]
        self.runtime = [False, ["?t", "?s", "?d", "?rt"]]
        self.atime = [False, ["?t", "?d", "?dt"]]
        self.dtime = [False, ["?t", "?s", "?st"]]


    def transform(self) -> None:
        for relation in self.logicalForm:
            relation = regex.sub(r'[()"]', "", relation)
            tokens = relation.split()

            if "ID" in relation:
                tokens = tokens[2][1:-1].split('-')
                self.atime[1][0] = tokens[1]
                self.dtime[1][0] = tokens[1]
                self.runtime[1][0] = tokens[1]


            if "WH" in relation:
                tokens = tokens[2][1:-1].split('-')
                subj = tokens[2] if tokens[2].lower() not in MAPPING else MAPPING[tokens[2].lower()]
                if subj == "TIME" and "AT_TIME" in relation:
                    self.subj.append("TIME")
                elif subj == "TIME" and "RUN_TIME" in relation:
                    self.subj.append("RUN_TIME")
                    self.runtime[0] = True
                else:
                    self.subj.append(subj)
            elif "FROM_LOC" in relation:
                tokens = tokens[3][1:-1].split('-')
                self.dtime[0] = True
                self.dtime[1][1] = MAPPING[tokens[2].lower()]
                if "TIME" in self.subj:
                    self.subj.append("STIME")
                    self.subj.remove("TIME")
                self.runtime[1][1] = MAPPING[tokens[2].lower()]
            elif "TO_LOC" in relation:
                tokens = tokens[3][1:-1].split('-')
                self.atime[0] = True
                self.atime[1][1] = MAPPING[tokens[2].lower()]
                if "TIME" in self.subj:
                    self.subj.append("DTIME")
                    self.subj.remove("TIME")
                self.runtime[1][2] = MAPPING[tokens[2].lower()]
            elif "AT_TIME" in relation:
                if self.action == "ARRIVE":
                    self.atime[1][2] = tokens[2]
                elif self.action == "LEAVE":
                    self.dtime[1][2] = tokens[2]
            elif len(tokens) == 2:
                self.action = MAPPING[tokens[0].lower()]
                if self.action == "ARRIVE":
                    self.atime[0] = True
            elif "THEME" in relation:
                tokens = tokens[2][1:-1].split('-')
                if self.action == "ARRIVE":
                    self.atime[1][1] = MAPPING[tokens[2].lower()]
                elif self.action == "LEAVE":
                    self.dtime[1][1] = MAPPING[tokens[2].lower()]


    def execute(self) -> str:
        result = ""
        io = IO.getInstance()

        atime = None
        dtime = None
        runtime = None

        ids = set(map(lambda x: x.split()[1], io.queryDatabase("train")))
        if self.atime[0]:
            atime = io.queryDatabase("atime", *self.atime[1])
            ids = ids.intersection(set(map(lambda x: x.split()[1], atime)))
        if self.dtime[0]:
            dtime = io.queryDatabase("dtime", *self.dtime[1])
            ids = ids.intersection(set(map(lambda x: x.split()[1], dtime)))
        if self.runtime[0]:
            runtime = io.queryDatabase("rtime", *self.runtime[1])
            ids = ids.intersection(set(map(lambda x: x.split()[1], runtime)))

        if self.mode == "WH":
            for id in ids:
                for subj in self.subj:
                    if subj == "TRAIN":
                        result += "Tàu hỏa {}. ".format(id)
                    elif subj == "RUN_TIME":
                        time = [ele.split()[4] for ele in runtime if id in ele][0]
                        result += "Thời gian chạy là {}. ".format(time)
                    elif subj == "STIME":
                        time = [ele.split()[3] for ele in dtime if id in ele][0]
                        result += "Chạy lúc {}. ".format(time)
                    elif subj == "DTIME":
                        time = [ele.split()[3] for ele in atime if id in ele][0]
                        result += "Cập bến lúc {}. ".format(time)
                result += "\n"

        elif self.mode == "YN":
            result += "Có. \n" if ids else "Không. \n"

        if result == "":
            result = "Không tồn tại chuyến tàu thỏa yêu cầu. \n"

        return "------ Procedure Execute ------\n" + result + "-------------------------------"


    def __str__(self) -> str:
        procedure = []

        if self.runtime[0]:
            procedure.append("(RUN-TIME {} {} {} {})".format(*self.runtime[1]))
        if self.atime[0]:
            procedure.append("(ATIME {} {} {})".format(*self.atime[1]))
        if self.dtime[0]:
            procedure.append("(DTIME {} {} {})".format(*self.dtime[1]))

        if self.mode == "WH":
            prefix = "PRINT-ALL "

            for subj in self.subj:
                var = self.varmap[subj]
                prefix += "?{} ({} ?{}) ".format(var, subj, var)

            procedure = prefix + " ".join(ele for ele in procedure)
        elif self.mode == "YN":
            procedure = "YES-NO " + " ".join(ele for ele in procedure)

        return "----- Procedure Semantics -----\n(" + procedure + ")\n-------------------------------\n\n\n"