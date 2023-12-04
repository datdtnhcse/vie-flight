import regex
from typing import List, Tuple
from abc import ABC, abstractmethod
from Models.IO import *
from Models.API import *

class Process:
    instance = None


    @staticmethod
    def getInstance():
        if not Process.instance:
            Process.instance = Process()

        return Process.instance

    def pipeline(self, tokens: List[str], types: List[str]):

        parser = DependencyParser(tokens, types)
        relation = parser.transform()
        yield parser

        grammar = GrammarRelation(relation)
        grammartical = grammar.transform()
        yield grammar

        logical = LogicalForm(grammartical)
        logicalForm, mode = logical.transform()
        yield logical

        procedure = Procedure(logicalForm, mode)
        procedure.transform()
        yield procedure

        result = procedure.execute()
        yield result

