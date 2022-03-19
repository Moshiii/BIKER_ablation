import sys
sys.path.append(".")

import gensim
import algorithm.recommendation as recommendation
import util
import domain
import _pickle as pickle
import pandas as pd
from bs4 import BeautifulSoup





def extract_training_pickle():
    # C:\@code\BIKER_ablation\data\api_questions_pickle_new
    # the pre-trained knowledge base of api-related questions (about 120K questions)
    print("")
    res = []
    for idx, _ in enumerate(answer_list):
        title = title_list[idx]
        answer = answer_list[idx]
        answer = extract_api_from_question_obj(answer)
        if len(answer) != 0:
            res.append([title, list(answer)])
        if idx % 1000 == 0:
            print(idx)
    return res


def preprocess_javadoc(javadoc, javadoc_dict_classes, javadoc_dict_methods):
    javadoc_class=javadoc[javadoc["type"]=="Class"]
    class_name = javadoc_class["API_name"].to_list()
    full_name = javadoc_class["func_name"].to_list()

    for idx, _ in enumerate(full_name):
        javadoc_dict_classes[class_name[idx]] = full_name[idx]

    javadoc_class=javadoc[javadoc["type"]=="function"]
    API_name = javadoc_class["API_name"].to_list()
    full_name = javadoc_class["func_name"].to_list()

    for idx, _ in enumerate(full_name):
        javadoc_dict_methods[API_name[idx]] = full_name[idx]


def extract_api_from_question_obj(answer):

    tmp_set = set()

    soup = BeautifulSoup(answer, 'html.parser', from_encoding='utf-8')

    codes = soup.find_all('code')
    for code in codes:
        code = code.get_text()
        pos = code.find('(')
        if pos != -1:
            code = code[:pos]

        if code in javadoc_dict_methods:
            method_name = javadoc_dict_methods[code]
            if method_name in tmp_set:
                continue
            else:
                tmp_set.add(method_name)

    return tmp_set



df = pd.read_csv("data/raw_python_SO.csv")
print('data loaded')

title_list = df.title.to_list()
answer_list = df.answer.to_list()

javadoc = pd.read_csv("data/python_docstring/python_doc.csv")

javadoc_dict_classes = dict()
javadoc_dict_methods = dict()
preprocess_javadoc(javadoc,javadoc_dict_classes,javadoc_dict_methods) # matrix transformation


print()

table_data_container = extract_training_pickle()

df=pd.DataFrame(table_data_container,columns=['title','answer'])
# print(df)
df.to_csv("data/training/Python_SO_train.csv")
# # parent = pickle.load(open('../data/parent', 'rb')) # parent is a dict(), which stores the ids of each query's duplicate questions
