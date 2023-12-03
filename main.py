# from Models.API import *
# from Models.DependencyParser import *
# from Models.GrammarRelation import *
# from Models.LogicalForm import *
# from Models.Procedure import *
from Models.process import *
# from Models.preprocess import *


from Models.IO import *

def main() -> None:
    io = IO.getInstance()
    preprocess = PreProcessing.getInstance()
    process = Process.getInstance()

    sentences = io.loadData("Input/question/")

    for i, text in enumerate(sentences):
        tokens = preprocess.tokenize(text)
        types = preprocess.getWordTypes(tokens)

        output_file = f"Output/output_{i+1}.txt"
        io.writeData(output_file, "w+", f"##### OUTPUT OF QUERY QUESTION {i+1} #####\n\n")

        io.writeData(output_file, "a+", f"----- Tokenize -----\n")
        for token in tokens:
            io.writeData(output_file, "a+", f'{token}\n')
        io.writeData(output_file, "a+", f"------------------------------\n\n\n")

        print(tokens)

        for result in process.pipeline(tokens, types):
            io.writeData(output_file, "a+", str(result))


if __name__ == '__main__':
    main()