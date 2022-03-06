import _pickle as pickle
import pandas as pd
from bs4 import BeautifulSoup
import sys
sys.path.append(".")
import util
import  algorithm.recommendation as recommendation
import gensim


def extract_training_pickle():
    # C:\@code\BIKER_ablation\data\api_questions_pickle_new
    questions = pickle.load(open('data/api_questions_pickle_new', 'rb')) # the pre-trained knowledge base of api-related questions (about 120K questions)
    print("")
    res=[]
    for idx, question in enumerate(questions): 
        title = question.title
        answer = extract_api_from_question_obj(question)
        if len(answer)!=0:
            res.append([title,list(answer)])
        if idx%1000==0: print(idx)
    return res

def preprocess_javadoc(javadoc,javadoc_dict_classes,javadoc_dict_methods):

    for api in javadoc:
        
        api_full = api.package_name+'.'+api.class_name
        javadoc_dict_classes[api.class_name] = api_full

        for api_method in api.methods:
            api_full = api.package_name+'.'+api.class_name+'.'+api_method
            javadoc_dict_methods[api.class_name+'.'+api_method] = api_full


def extract_api_from_question_obj(question):

    tmp_set = set()

    for answer in question.answers:

        if int(answer.score)<0:
            continue

        soup = BeautifulSoup(answer.body, 'html.parser', from_encoding='utf-8')
        links = soup.find_all('a')
        for link in links:
            link = link['href']
            if 'docs.oracle.com/javase/' in link and '/api/' in link and 'html' in link:
                pair = util.parse_api_link(link)  # pair[0] is class name, pair[1] is method name

                if pair[1] != '':
                    method_name = pair[0] + '.' + pair[1]
                    if method_name in tmp_set:
                        continue
                    else:
                        tmp_set.add(method_name)


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

    real_set=set()
    for t in tmp_set:

        if not t.startswith("java"):continue
        real_set.add(t)

    return real_set


w2v = gensim.models.Word2Vec.load('data/w2v_model_stemmed') # pre-trained word embedding
idf = pickle.load(open('data/idf','rb')) # pre-trained idf value of all words in the w2v dictionary
questions = pickle.load(open('data/api_questions_pickle_new', 'rb')) # the pre-trained knowledge base of api-related questions (about 120K questions)
# questions = recommendation.preprocess_all_questions(questions, idf, w2v) # matrix transformation
javadoc = pickle.load(open('data/javadoc_pickle_wordsegmented','rb')) # the pre-trained knowledge base of javadoc
javadoc_dict_classes = dict()
javadoc_dict_methods = dict()
preprocess_javadoc(javadoc,javadoc_dict_classes,javadoc_dict_methods) # matrix transformation

table_data_container = extract_training_pickle()

df=pd.DataFrame(table_data_container,columns=['title','answer'])
print(df)
df.to_csv("data/training/BIKER_original_train.csv")
# parent = pickle.load(open('../data/parent', 'rb')) # parent is a dict(), which stores the ids of each query's duplicate questions
