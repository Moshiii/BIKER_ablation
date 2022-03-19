import os
import ast
import pandas as pd

import sys
# print(sys.path)


root_path = 'c:\\users\\wmswm\\appdata\\local\\programs\\python\\python310\\lib\\site-packages\\'

name_docstring_pair = []

for x in ["keras", "matplotlib", "nltk", "numpy", "pandas", "pyspark", "scipy", "sklearn", "tensorflow", "torch"]:
    # print(os.listdir(root_path))
    my_list = []
    for root, subdirs, files in os.walk(root_path+x):
        for f in files:
            if f.endswith('.py'):
                my_list.append(os.path.join(root, f))

    # print(my_list)

    
    for name in my_list:
        with open(name, 'rb') as fd:
            file_contents = fd.read()
        package_path = x+name.split(x)[1].replace(".py", "").replace("\\", ".")
        if "._" in package_path:
            continue
        if ".test" in package_path:
            continue
        print(package_path)
        module = ast.parse(file_contents)
        for node in module.body:
            if not isinstance(node, ast.FunctionDef) and not isinstance(node, ast.ClassDef):
                continue
            if node.name.startswith("_"):
                continue
            if ast.get_docstring(node) == None:
                continue
            docstring = ast.get_docstring(node).split("\n")[0]
            if isinstance(node, ast.FunctionDef):
                name_docstring_pair.append(["function",x, package_path+"."+node.name, package_path.split(".")[-1]+"."+node.name,node.name, docstring])

            if isinstance(node, ast.ClassDef):
                name_docstring_pair.append(["Class",x, package_path+"."+node.name, node.name,node.name, docstring])

                for sub_node in node.body:
                    if not isinstance(sub_node, ast.FunctionDef) and not isinstance(sub_node, ast.ClassDef):
                        continue
                    if sub_node.name.startswith("_"):
                        continue
                    if ast.get_docstring(sub_node) == None:
                        continue
                    docstring = ast.get_docstring(sub_node).split("\n")[0]
                    if isinstance(sub_node, ast.FunctionDef):
                        name_docstring_pair.append(
                            ["function",x, package_path+"."+node.name+"."+sub_node.name, node.name+"."+sub_node.name,sub_node.name, docstring])

df = pd.DataFrame(name_docstring_pair, columns=["type","package", "func_name","API_name","method_or_class_name", "docstring"])

df = df.drop_duplicates()
df.to_csv("data\\python_docstring\\python_doc.csv")
