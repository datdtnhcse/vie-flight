import os
from typing import List

class IO:
    instance = None

    @staticmethod
    def getInstance():
        if not IO.instance:
            IO.instance = IO()

        return IO.instance

    def writeData(self, file: str, mode: str, data: str) -> None:
        with open(file, mode, encoding='utf8') as f:
            f.write(data)

    def loadData(self, folder: str) -> List[str]:
        data = []
        for file in os.listdir(folder):
            with open(folder+file, "r", encoding='utf8') as f:
                data.append(f.readline())

        return data


    def queryDatabase(self, database: str, *filterData) -> List[str]:
        data = None
        with open('Input/database_flight/{}.txt'.format(database), "r", encoding='utf8') as f:
            data = f.readlines()

        for key in filterData:
            if "?" not in key:
                data = list(filter(lambda x: key in x, data))

        return data