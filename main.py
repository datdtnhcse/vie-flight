from Models.API import *
from Models.IO import *

def main() -> None:
    io = IO.getInstance()
    preprocess = PreProcessing.getInstance()
    process = Process.getInstance()

    sentences = io.loadData("Input/question_flight/")
    for i, text in enumerate(sentences):
        try:
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
        except:
            continue


if __name__ == '__main__':
    main()