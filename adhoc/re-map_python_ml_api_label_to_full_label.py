import sys
sys.path.append(".")

import pandas as pd

df = pd.read_csv("data/training/python_ml_total_unique_API_train.csv")

df_python_doc = pd.read_csv("data/python_docstring/python_doc.csv")

df_python_doc= df_python_doc[["func_name","method_or_class_name","package"]]
records = df_python_doc.to_records(index=False)
df_python_doc = list(records)
API_dict={}
# print(list(df_python_doc))
for x in df_python_doc:
    
    full_name=x[0]
    method_class_name=x[1]
    package=x[2]
    API_dict[str(package)+"."+str(method_class_name)]=full_name
# print(API_dict)

def get_full_path(answer):
    answer = eval(answer)
    # print(len(answer))
    API_list=[]
    for a in answer: 
        if a in API_dict:
            # print(API_dict[a])
            API_list.append(API_dict[a])
    return API_list

df['full_answer'] = df.apply(lambda x: get_full_path(x['answer']), axis=1)

df.to_csv("data/training/python_ml_total_unique_API_train_full_name.csv")