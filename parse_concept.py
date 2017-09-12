import requests
import csv
import json
import collections

def parse_concepts(source, mode):
    # source = source.replace("\"\"","\"")
    data = {'code': source, 'mode': mode}
    req = requests.post(url='http://acos.cs.hut.fi/python-parser', data=data)
    #parse Json format to string (concept and count)
    #print(req.text)
    jdata = json.loads(req.text)
    dic = jdata['lines']
    list  =[]
    for key in dic:
        for c in dic[key]:
            list.append(c)
    #print(list)
    counter = collections.Counter(list)
    res = ""
    for key, value in counter.items():
        res = res + key+":"+ str(value)+","
    return res[0:len(res)-1]

def add_concept_to_content(input_file, output_file):
    with open(input_file,'r') as f:
        reader = csv.reader(f, delimiter=',')
        problemList = []
        # print(reader)
        with open(output_file, 'w') as w:
            problemWriter = csv.writer(w)
            for row in reader:
                #print(row)
                concepts = parse_concepts(row[1], "simple")
                #problemList = []
                problemList = row
                problemList.append(concepts)
                problemWriter.writerow(problemList)
                print(problemList)

add_concept_to_content('data/peter.examples.csv', 'data/peter.examples_with_concepts.csv')
# add_concept_to_content('data/andrew.examples.csv', 'data/andrew.examples_with_concepts.csv')
# add_concept_to_content('data/peter.problems.csv', 'data/peter.problems_with_concepts.csv')
# add_concept_to_content('data/peter/andrew.problems.csv', 'data/peter/peter.problems_with_concepts.csv')
# your source code here
# source = '''
# print("Hello, world!")
# a = 1
# b = 2
# print(a + b)
# '''
# res = parse_concepts(source,"simple")
# print(res)