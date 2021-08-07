import pickle
from auto_complete_data import AutoCompleteData
from config import connection
from initialize_data import Initialize


class AutoComplete:
    def __init__(self):
        """
        initialize the class members
        """
        try:
            with open('trie.pkl', 'rb') as input:
                self.__sentences_trie = pickle.load(input)
        except FileNotFoundError:
            initialize = Initialize('2021-archive')
            initialize.initialize_data()
            with open('trie.pkl', 'rb') as input:
                self.__sentences_trie = pickle.load(input)

    def get_best_k_completions(self, sub_string, k):
        """
        Returns the five highest scored sentences
        :param sub_string: the sub-string to be complete
        :param k: the number of completions to be return
        :return: an array of k AutoCompleteData objects (the k highest scored sentences)
        """
        tuples = self.__sentences_trie.search(sub_string.strip())[:k]
        sentences = []
        for element in tuples:
            sentence = self.get_content(element[0][0], element[0][1])
            sentences.append((sentence, element[0][2], self.get_file_name(element[0][0])))
        for i in range(len(sentences)):
            sentences[i] = AutoCompleteData(sentences[i][0], sentences[i][2], sentences[i][1], tuples[i][1])
        return sentences

    def get_content(self, file_num, line_num):
        """
        get the file name
        :param file_num: the serial number of the file
        :param line_num: the serial number of the line in the file
        :return: the file kine content
        """
        try:
            with connection.cursor() as cursor:
                query = "SELECT content from files_content WHERE file_num = %s and row_num=%s;"
                cursor.execute(query, (file_num, line_num))
                result = cursor.fetchall()
                return result[0]['content']
        except Exception:
            pass

    def get_file_name(self, file_num):
        """
        get the file name
        :param file_num: the serial number of the file
        :return: the file name
        """
        try:
            with connection.cursor() as cursor:
                query = "SELECT file_name from files_names WHERE file_num = %s"
                cursor.execute(query, (file_num))
                result = cursor.fetchall()
                return result[0]['file_name']
        except Exception:
            pass
