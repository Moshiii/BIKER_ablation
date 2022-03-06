import _pickle as pickle
import pandas as pd
from bs4 import BeautifulSoup

import sys
sys.path.append(".")


import util
import read_data



def read_querys_from_file():

    path = 'data/querys_final'
    file = open(path)

    querys = list()

    while True:
        line = file.readline()
        if not line:
            break
        if len(line) <= 2 or '$$$$$' not in line:
            continue

        line = line.replace('\n','')
        line = line.split('$$$$$')

        title = line[0].strip()
        if title[0:2] == '**':
            continue
        if title[-1] == '?':
            title = title[:-1]
        apis = line[1].split(' ')
        apis_set = set()
        for api in apis:
            if len(api.strip())>1:
                apis_set.add(api)
        querys.append([title,list(apis_set)])

    # for item in querys:
    #     print item[0],item[1]



    file.close()

    return querys

test_container = read_querys_from_file()

df=pd.DataFrame(test_container,columns=['title','answer'])

print(df)

df.to_csv("data/testing/BIKER_original_test.csv")
