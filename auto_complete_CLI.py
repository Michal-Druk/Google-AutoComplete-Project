from auto_complete import AutoComplete

RESULTS_NUM = 5


class CLI:
    def __init__(self):
        print("Loading the files and preparing the system...")
        self.__data = AutoComplete()

    def run(self):
        """
        get new requests and handles them
        """
        while True:
            print("The system is ready. Enter your text:")
            sentence = " "
            while True:
                sentence += input(sentence)
                if sentence[-1] == "#": break
                completions = self.__data.get_best_k_completions(sentence, RESULTS_NUM)
                if len(completions) == 0:
                    print("No suggestion")
                else:
                    print("Here are {} suggestions:".format(len(completions)))
                    for i in range(len(completions)):
                        print(i + 1, ". ", completions[i].get_completed_sentence(), " (",
                              completions[i].get_source_text(),
                              ":", completions[i].get_offset(), ")")
