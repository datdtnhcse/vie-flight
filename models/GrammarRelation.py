import regex
from typing import List, Tuple
from abc import ABC, abstractmethod
from Models.IO import *
from Models.Const_flight import *

class GrammarRelation(NLP):
    def __init__(self, relations: List[str]) -> None:
        super().__init__()
        self.variable = ["s1"]
        for i in range(len(relations)):
            relations[i] = regex.sub(r'[,()]', "", relations[i])

            if "namemod" in relations[i]:
                tokens = relations[i].split()
                name = ("[NAME-{}-\"{}\"]".format(super().createVariable(tokens[2][0]), tokens[2].upper()))
                tokens = relations[i-1].split()
                tokens[2] = name
                relations[i-1] = " ".join(token for token in tokens)
            elif "pobj" in relations[i]:
                tokens = relations[i].split()
                if tokens[2] in PLACE:
                    name = ("[NAME-{}-\"{}\"]".format(super().createVariable(tokens[2][0]), tokens[2].upper()))
                    tokens[2] = name
                    relations[i] = " ".join(token for token in tokens)
            elif "whmod" in relations[i] and "aux" in relations[i-1]:
                tokens = relations[i-1].split()
                pred = tokens[1]
                aux = tokens[2]
                tokens = relations[i].split()
                tokens[1] = pred
                tokens.append(aux)
                relations[i] = " ".join(token for token in tokens)
            elif "idmod" in relations[i]:
                tokens = relations[i].split()
                relations = [relation.replace(tokens[1], "[ID-{}-{}]".format(tokens[2], tokens[1])) for relation in relations]

        self.dep_relation = relations
        self.gram_relation = set()


    def transform(self) -> List[str]:
        for relation in self.dep_relation:
            transformRelation = self.__relationTransform(relation)

            if transformRelation:
                self.gram_relation.add(transformRelation)

        self.gram_relation = list(self.gram_relation)
        query = list(filter(lambda x: "QUERY" in x, self.gram_relation))
        pred = list(filter(lambda x: "PRED" in x, self.gram_relation))
        subj = list(filter(lambda x: "LSUBJ" in x, self.gram_relation))
        lobj = list(filter(lambda x: "LOBJ" in x, self.gram_relation))
        other = list(filter(lambda x: "QUERY" not in x and "PRED" not in x and "LSUBJ" not in x and "LOBJ" not in x, self.gram_relation))
        self.gram_relation = query+pred+subj+lobj+other
        return self.gram_relation


    def __relationTransform(self, relation: str) -> str:
        result = ""
        relation = relation.split()

        if "root" in relation:
            result = "({} PRED {})".format("s1", relation[2].upper())
        elif "subj" in relation:
            result = "({} LSUBJ {})".format("s1", relation[2].upper())
        elif "dobj" in relation:
            result = "({} LOBJ {})".format("s1", relation[2])
        elif "timemod" in relation:
            result = "({} TIME {})".format("s1", relation[2].upper())
        elif "whmod" in relation:
            if MAPPING[relation[2]] == "WHICH":
                result = "({} WHQUERY [WHICH-{}-{}])".format("s1", self.createVariable(relation[1][0]), relation[1].upper())
            elif MAPPING[relation[2]] == "TIME":
                result = "({} WHQUERY [{}-{}-TIME])".format("s1", MAPPING[relation[3]], "s1")
        elif "pobj" in relation:
            if "từ" in relation:
                result = "({} PFROM {})".format("s1", relation[2])
            elif "đến" in relation:
                result = "({} PTO {})".format("s1", relation[2])
        elif "aux" in relation and relation[2] in MAPPING and MAPPING[relation[2]] == "YESNO":
            result = "({} YNQUERY {})".format("s1", relation[1].upper())
        elif "nmod" in relation:
            result = "({} NMOD {})".format(relation[1].upper(), relation[2].upper())

        return result


    def __str__(self) -> str:
        relations = "\n".join(relation for relation in self.gram_relation)
        relations = relations.replace("-", " ").replace("[", "(").replace("]", ")")

        return "---- Grammartical Relation ----\n" + relations + "\n-------------------------------\n\n\n"
