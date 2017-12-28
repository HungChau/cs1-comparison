import csv
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import math
from random import randint, seed
import aggregate_data

def recommendation(exampleFileName, problemFileName, alpha, beta, gamma, output = 1):
    if alpha==0:
        alpha=0.000001
    if beta==0:
        beta =0.000001
    if gamma==0:
        gamma=0.000001

    examples = list()
    with open(exampleFileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != "Week":
                examples.append(row)

    # print(examples)
    #remove the last two topics
    # examples = examples[:-1]
    # get
    problemsByTopic = list()
    with open(problemFileName, 'r') as f:
        reader = csv.reader(f)
        topic =1
        problems = dict()
        for row in reader:
            # print(row)
            if row[0] != "Week":
                if int(row[3]) == topic:
                    if int(row[1]) not in problems:
                        conceptSet = set()
                    else:
                        conceptSet = problems[int(row[1])]
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            conceptSet.add(c.split(":")[0])
                    problems[int(row[1])] = conceptSet
                    # print(row[1])
                else:
                    topic +=1
                    problemsByTopic.append(problems)
                    problems = dict()
                    conceptSet = set()
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            conceptSet.add(c.split(":")[0])
                    problems[int(row[1])] = conceptSet
        # if int(row[3]) not in [11,12]:
        #     problemsByTopic.append(problems)
        problemsByTopic.append(problems)


    passConcepts = set()
    currentConcepts = set()
    top = [3,5,10,15]
    precision = [0,0,0,0]
    recall = [0, 0, 0, 0]
    f1 = [0, 0, 0, 0]
    for i in range(0, len(examples)):
        # print(e)
        # e = examples[i]
        # e[1] = e[1].replace("{", "")
        # e[1] = e[1].replace("}", "")
        # e[1] = e[1].replace("'", "")
        # e[1] = e[1].replace(" ", "")
        # for c in e[1].split(","):
        #     if c != '':
        #         currentConcepts.add(c.split(':')[0])

        e = examples[i]
        e[2] = e[2].replace("[","")
        e[2] = e[2].replace("]", "")
        e[2] = e[2].replace("'", "")
        e[2] = e[2].replace(" ", "")
        for c in e[2].split(","):
            if c!= '':
                currentConcepts.add(c)

        # print(len(currentConcepts), len(currentConcepts-passConcepts))
        currentConcepts = currentConcepts - passConcepts
        # print(currentConcepts,"\n")

        rankedList = list()
        for j in range(i,len(problemsByTopic)):
            for key,value in problemsByTopic[j].items():
                concepts_in_problem = value
                currentConcepts_in_problem = concepts_in_problem & currentConcepts
                passConcepts_in_problem = concepts_in_problem & passConcepts
                futureConcepts_in_problem =concepts_in_problem - (currentConcepts_in_problem|passConcepts_in_problem)
                if len(currentConcepts_in_problem) > 0 or len(futureConcepts_in_problem) > 0:
                    score = len(passConcepts_in_problem)*alpha+len(currentConcepts_in_problem)*beta-len(futureConcepts_in_problem)*gamma
                    # score = score/len(concepts_in_problem)
                    rankedList.append((score,key,j+1))

        # print(len(problemsByTopic[i]))
        rankedList = sorted(rankedList, key=itemgetter(0), reverse=True)
        # print(rankedList,"\n")
        concepts_in_current_problems = set()
        for key, value in problemsByTopic[i].items():
            concepts_in_current_problems = concepts_in_current_problems | value

        for t in range(0, len(top)):
            TP = 0
            for idx in range(0, top[t]):
                if idx < len(rankedList):
                    if rankedList[idx][2] == (i + 1):
                        TP += 1
            if top[t] <= len(rankedList):
                precision[t] += TP / top[t]
                # precision[t] = TP / top[t]
            else:
                precision[t] += TP / len(rankedList)
                # precision[t] = TP / len(rankedList)
            recall[t] += TP / len(problemsByTopic[i])
            # recall[t] = TP / len(problemsByTopic[i])
        # print("precision",i,precision)
        # print("recall",i, precision)
        # print(passConcepts)
        passConcepts = passConcepts | concepts_in_current_problems
        # passConcepts = passConcepts | currentConcepts
        currentConcepts = set()

    precision = [x/len(examples) for x in precision]
    recall = [x/len(examples) for x in recall]
    for i in range(0, len(recall)):
        if recall[i] == 0 and precision[i] == 0:
            f1[i] = 0
        else:
            f1[i] = 2 * precision[i] * recall[i] / (recall[i] + precision[i])

    if output == 1:
        for i in range(0, len(recall)):
            print("Precision at top ", top[i], ": ", precision[i])
            print("Recall at top  ", top[i], ": ", recall[i])
            print("F1 at top  ", top[i], ": ", f1[i])

            # return F1 at top 10, since top 10 is best, so choose top 10 at standard
    return f1
    # print(len(problemsByTopic))
    # print(problemsByTopic[2])

# difference with recommendation() is that this function doesn't save the performance metrics of the previous topics, only care about the current topic.
# To compare the performances of wizard with different numbers of examples
def recommendation_error_rate(exampleFileName, problemFileName, alpha, beta, gamma, topic_to_eval, output = 1):
    examples = list()
    with open(exampleFileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != "Week":
                examples.append(row)

    # print(examples)
    #remove the last two topics
    examples = examples[:-2]
    # get
    problemsByTopic = list()
    with open(problemFileName, 'r') as f:
        reader = csv.reader(f)
        topic =1
        problems = dict()
        for row in reader:
            # print(row)
            if row[0] != "Week":
                if int(row[3]) == topic:
                    if int(row[1]) not in problems:
                        conceptSet = set()
                    else:
                        conceptSet = problems[int(row[1])]
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            conceptSet.add(c.split(":")[0])
                    problems[int(row[1])] = conceptSet
                    # print(row[1])
                else:
                    topic +=1
                    problemsByTopic.append(problems)
                    problems = dict()
                    conceptSet = set()
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            conceptSet.add(c.split(":")[0])
                    problems[int(row[1])] = conceptSet
        # if int(row[3]) not in [11,12]:
        #     problemsByTopic.append(problems)
        problemsByTopic.append(problems)


    passConcepts = set()
    currentConcepts = set()
    futureConcepts = set()
    top = [3,5,10,15]
    precision = [0,0,0,0]
    recall = [0, 0, 0, 0]
    f1 = [0, 0, 0, 0]
    for i in range(0, len(examples)):
        # print(e)
        e = examples[i]
        e[2] = e[2].replace("[", "")
        e[2] = e[2].replace("]", "")
        e[2] = e[2].replace("'", "")
        e[2] = e[2].replace(" ", "")
        for c in e[2].split(","):
            if c != '':
                currentConcepts.add(c)

        currentConcepts = currentConcepts - passConcepts
        # print(currentConcepts, "\n")
        # print(currentConcepts)
        rankedList = list()
        for j in range(i,len(problemsByTopic)):
            for key,value in problemsByTopic[j].items():
                concepts_in_problem = value
                currentConcepts_in_problem = concepts_in_problem & currentConcepts
                passConcepts_in_problem = concepts_in_problem & passConcepts
                futureConcepts_in_problem =concepts_in_problem - (currentConcepts_in_problem|passConcepts_in_problem)
                if len(currentConcepts_in_problem) > 0 or len(futureConcepts_in_problem) > 0:
                    score = len(passConcepts_in_problem)*alpha+len(currentConcepts_in_problem)*beta-len(futureConcepts_in_problem)*gamma
                    rankedList.append((score,key,j+1))

        # print(len(problemsByTopic[i]))
        rankedList = sorted(rankedList, key=itemgetter(0), reverse=True)
        # print(rankedList,"\n")
        concepts_in_current_problems = set()
        for key, value in problemsByTopic[i].items():
            concepts_in_current_problems = concepts_in_current_problems | value

        for t in range(0,len(top)):
            TP = 0
            for idx in range(0,top[t]):
                if idx < len(rankedList):
                    if rankedList[idx][2] == (i+1):
                        TP+= 1
            if top[t] <= len(rankedList):
                precision[t] = TP/top[t]
            else:
                precision[t] = TP / len(rankedList)
            recall[t] = TP/len(problemsByTopic[i])

        # for idx in range(0, len(recall)):
        #     if recall[idx] == 0 and precision[idx] == 0:
        #         f1[idx] = 0
        #     else:
        #         f1[idx] = 2 * precision[idx] * recall[idx] / (recall[idx] + precision[idx])

        if (i+1) == topic_to_eval:
            print(currentConcepts, "\n")
            break

        # print(passConcepts)
        passConcepts = passConcepts | concepts_in_current_problems
        # passConcepts = passConcepts | currentConcepts
        currentConcepts = set()

    # precision = [x/len(examples) for x in precision]
    # recall = [x/len(examples) for x in recall]
    for i in range(0, len(recall)):
        if recall[i] == 0 and precision[i] == 0:
            f1[i] = 0
        else:
            f1[i] = 2 * precision[i] * recall[i] / (recall[i] + precision[i])
    print(f1[3])
    if output == 1:
        for i in range(0,len(recall)):
            print("Precision at top ",top[i],": ", precision[i])
            print("Recall at top  ",top[i],": ", recall[i])
            if recall[i]==0 and precision[i]==0:
                f1[i] = 0
            else:
                f1[i] = 2*precision[i]*recall[i]/(recall[i]+precision[i])
            print("F1 at top  ",top[i],": ", f1[i])

    #return F1 at top 10, since top 10 is best, so choose top 10 at standard
    return f1
    # print(len(problemsByTopic))
    # print(problemsByTopic[2])

def recommendation_combined(exampleFileName, problemFileName, alpha, beta, gamma, output = 1):
    examples = list()
    with open(exampleFileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != "Week":
                examples.append(row)

    # print(examples)
    #remove the last two topics
    examples = examples[:-2]
    # get
    number_of_problems = 0
    problemsByTopic = list()
    with open(problemFileName, 'r') as f:
        reader = csv.reader(f)
        topic = 1
        problems = dict()
        idf = dict()
        for row in reader:
            # print(row)
            if row[0] != "Week":
                if int(row[3]) == topic:
                    if int(row[1]) not in problems:
                        conceptSet = dict()
                    else:
                        conceptSet = problems[int(row[1])]
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0],float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet,c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
                    # print(row[1])
                else:
                    topic += 1
                    problemsByTopic.append(problems)
                    number_of_problems+= len((problems))
                    problems = dict()
                    conceptSet = dict()
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0], float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet, c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
        problemsByTopic.append(problems)
        number_of_problems += len((problems))


    passConcepts = set()
    currentConcepts = set()
    futureConcepts = set()
    top = [3,5,10,15]
    precision = [0,0,0,0]
    recall = [0, 0, 0, 0]
    f1 = [0, 0, 0, 0]
    for i in range(0, len(examples)):
        # print(e)
        e = examples[i]
        e[2] = e[2].replace("[","")
        e[2] = e[2].replace("]", "")
        e[2] = e[2].replace("'", "")
        e[2] = e[2].replace(" ", "")
        for c in e[2].split(","):
            if c!= '':
                currentConcepts.add(c)
        # print(currentConcepts)
        rankedList = list()

        for j in range(i,len(problemsByTopic)):
            for key,value in problemsByTopic[j].items():
                number_of_current_concepts = 0
                number_of_past_concepts = 0
                number_of_future_concepts = 0

                concepts_in_problem = value
                for curcon in currentConcepts:
                    if curcon in concepts_in_problem:
                        number_of_current_concepts+= concepts_in_problem[curcon]
                for pastcon in passConcepts:
                    if pastcon in concepts_in_problem:
                        number_of_past_concepts += concepts_in_problem[pastcon]
                for futureconkey, futureconcepvalue in concepts_in_problem.items():
                    if futureconkey not in (currentConcepts|passConcepts):
                        number_of_future_concepts+= futureconcepvalue

                # currentConcepts_in_problem = concepts_in_problem & currentConcepts
                # passConcepts_in_problem = concepts_in_problem & passConcepts
                # futureConcepts_in_problem =concepts_in_problem - (currentConcepts|passConcepts)
                if number_of_current_concepts > 0 or number_of_future_concepts > 0:
                    score = number_of_past_concepts*alpha+number_of_current_concepts*beta-number_of_future_concepts*gamma
                    rankedList.append((score,key,j+1))
                # print(concepts_in_problem)
                # print(passConcepts_in_problem)
                # print(currentConcepts_in_problem)
                # print(futureConcepts_in_problem)
                # print(concepts_in_problem)
                # print(passConcepts_in_problem)
                # print(currentConcepts_in_problem)
                # print(futureConcepts_in_problem)

        # print(len(problemsByTopic[i]))
        rankedList = sorted(rankedList, key=itemgetter(0), reverse=True)
        # print(rankedList,"\n")
        concepts_in_current_problems = set()
        for key, value in problemsByTopic[i].items():
            for c in value.items():
                if c not in concepts_in_current_problems:
                    concepts_in_current_problems.add(c[0])

        for t in range(0,len(top)):
            TP = 0
            for idx in range(0,top[t]):
                if idx < len(rankedList):
                    if rankedList[idx][2] == (i+1):
                        TP+= 1
            if top[t] <= len(rankedList):
                precision[t] += TP/top[t]
            else:
                precision[t] += TP / len(rankedList)
            recall[t] += TP/len(problemsByTopic[i])


        # print(passConcepts)
        passConcepts = passConcepts | concepts_in_current_problems
        # passConcepts = passConcepts | currentConcepts
        currentConcepts = set()

    precision = [x/len(examples) for x in precision]
    recall = [x/len(examples) for x in recall]
    if output ==1:
        for i in range(0,len(recall)):
            print("Precision at top ",top[i],": ", precision[i])
            print("Recall at top  ",top[i],": ", recall[i])
            print("F1 at top  ",top[i],": ", 2*precision[i]*recall[i]/(recall[i]+precision[i]))

    #return F1 at top 10, since top 10 is best, so choose top 10 at standard
    return 2*precision[0]*recall[0]/(recall[0]+precision[0]),2*precision[1]*recall[1]/(recall[1]+precision[1]),2*precision[2]*recall[2]/(recall[2]+precision[2]),2*precision[3]*recall[3]/(recall[3]+precision[3])
    # print(len(problemsByTopic))
    # print(problemsByTopic[2])

def recommendation_tfidf_for_wizard(exampleFileName, problemFileName, alpha, beta, gamma, output = 1):
    examples = list()
    with open(exampleFileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != "Week":
                examples.append(row)

    # print(examples)
    # remove the last two topics
    examples = examples[:-2]
    # read problems from file and organize for computation
    number_of_problems = 0
    problemsByTopic = list()
    with open(problemFileName, 'r') as f:
        reader = csv.reader(f)
        topic = 1
        problems = dict()
        idf = dict()
        for row in reader:
            # print(row)
            if row[0] != "Week":
                if int(row[3]) == topic:
                    if int(row[1]) not in problems:
                        conceptSet = dict()
                    else:
                        conceptSet = problems[int(row[1])]
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0],float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet,c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
                    # print(row[1])
                else:
                    topic += 1
                    problemsByTopic.append(problems)
                    number_of_problems+= len((problems))
                    problems = dict()
                    conceptSet = dict()
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0], float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet, c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
        problemsByTopic.append(problems)
        number_of_problems += len((problems))

    #calculate tf-idf for each problem
    for i in range(0,len(problemsByTopic)):
        for k1,v1 in problemsByTopic[i].items():
            for v2 in v1:
                # print(v2)
                # print(number_of_problems*1.0/idf[v2])
                v1[v2] = (1 + math.log(v1[v2]))*math.log10(number_of_problems*1.0/idf[v2])
            problemsByTopic[i][k1] = v1

    passConcepts = set()
    currentConcepts = set()
    futureConcepts = set()
    top = [3, 5, 10, 15]
    precision = [0, 0, 0, 0]
    recall = [0, 0, 0, 0]
    f1 = [0, 0, 0, 0]
    for i in range(0, len(examples)):
        # print(e)
        e = examples[i]
        e[2] = e[2].replace("[", "")
        e[2] = e[2].replace("]", "")
        e[2] = e[2].replace("'", "")
        e[2] = e[2].replace(" ", "")
        for c in e[2].split(","):
            if c != '':
                currentConcepts.add(c)
        # print(currentConcepts)

        currentConcepts = currentConcepts - passConcepts
        rankedList = list()

        for j in range(i, len(problemsByTopic)):
            for key, value in problemsByTopic[j].items():
                number_of_current_concepts = 0
                number_of_past_concepts = 0
                number_of_future_concepts = 0

                concepts_in_problem = value
                for curcon in currentConcepts:
                    if curcon in concepts_in_problem:
                        number_of_current_concepts += concepts_in_problem[curcon]
                for pastcon in passConcepts:
                    if pastcon in concepts_in_problem:
                        number_of_past_concepts += concepts_in_problem[pastcon]
                for futureconkey, futureconcepvalue in concepts_in_problem.items():
                    if futureconkey not in (currentConcepts | passConcepts):
                        number_of_future_concepts += futureconcepvalue

                # currentConcepts_in_problem = concepts_in_problem & currentConcepts
                # passConcepts_in_problem = concepts_in_problem & passConcepts
                # futureConcepts_in_problem =concepts_in_problem - (currentConcepts|passConcepts)
                if number_of_current_concepts > 0 or number_of_future_concepts > 0:
                    score = number_of_past_concepts * alpha + number_of_current_concepts * beta - number_of_future_concepts * gamma
                    rankedList.append((score, key, j + 1))
                    # print(concepts_in_problem)
                    # print(passConcepts_in_problem)
                    # print(currentConcepts_in_problem)
                    # print(futureConcepts_in_problem)
                    # print(concepts_in_problem)
                    # print(passConcepts_in_problem)
                    # print(currentConcepts_in_problem)
                    # print(futureConcepts_in_problem)

        # print(len(problemsByTopic[i]))
        rankedList = sorted(rankedList, key=itemgetter(0), reverse=True)
        # print(rankedList,"\n")
        concepts_in_current_problems = set()
        for key, value in problemsByTopic[i].items():
            for c in value.items():
                if c not in concepts_in_current_problems:
                    concepts_in_current_problems.add(c[0])

        for t in range(0, len(top)):
            TP = 0
            for idx in range(0, top[t]):
                if idx < len(rankedList):
                    if rankedList[idx][2] == (i + 1):
                        TP += 1
            if top[t] <= len(rankedList):
                precision[t] += TP / top[t]
            else:
                precision[t] += TP / len(rankedList)
            recall[t] += TP / len(problemsByTopic[i])

        # print(passConcepts)
        passConcepts = passConcepts | concepts_in_current_problems
        # passConcepts = passConcepts | currentConcepts
        currentConcepts = set()

    precision = [x / len(examples) for x in precision]
    recall = [x / len(examples) for x in recall]
    if output ==1:
        for i in range(0, len(recall)):
            print("Precision at top ", top[i], ": ", precision[i])
            print("Recall at top  ", top[i], ": ", recall[i])
            print("F1 at top  ", top[i], ": ", 2 * precision[i] * recall[i] / (recall[i] + precision[i]))

    # return F1 at top 10, since top 10 is best, so choose top 10 at standard
    return 2 * precision[0] * recall[0] / (recall[0] + precision[0]), 2 * precision[1] * recall[1] / (
    recall[1] + precision[1]), 2 * precision[2] * recall[2] / (recall[2] + precision[2]), 2 * precision[3] * recall[
               3] / (recall[3] + precision[3])
    # print(len(problemsByTopic))
    # print(problemsByTopic[2])

def recommendation_tfidf(exampleFileName, problemFileName):
    examples = list()
    with open(exampleFileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != "Week":
                examples.append(row)

    # print(examples)
    # remove the last two topics
    # examples = examples[:-1]
    # get
    number_of_problems = 0
    problemsByTopic = list()
    with open(problemFileName, 'r') as f:
        reader = csv.reader(f)
        topic = 1
        problems = dict()
        idf = dict()
        for row in reader:
            # print(row)
            if row[0] != "Week":
                if int(row[3]) == topic:
                    if int(row[1]) not in problems:
                        conceptSet = dict()
                    else:
                        conceptSet = problems[int(row[1])]
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0],float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet,c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
                    # print(row[1])
                else:
                    topic += 1
                    problemsByTopic.append(problems)
                    number_of_problems+= len((problems))
                    problems = dict()
                    conceptSet = dict()
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0], float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet, c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
        problemsByTopic.append(problems)
        number_of_problems += len((problems))

    #calculate tf-idf for each problem
    for i in range(0,len(problemsByTopic)):
        for k1,v1 in problemsByTopic[i].items():
            for v2 in v1:
                # print(v2)
                # print(number_of_problems*1.0/idf[v2])
                v1[v2] = (1 + math.log(v1[v2]))*math.log10(number_of_problems*1.0/idf[v2])
            problemsByTopic[i][k1] = v1

    top = [3, 5, 10, 15]
    precision = [0, 0, 0, 0]
    recall = [0, 0, 0, 0]
    f1 = [0, 0, 0, 0]

    for i in range(0, len(examples)):
        currentConcepts = list()
        # print(e)
        e = examples[i]
        e[1] = e[1].replace("{", "")
        e[1] = e[1].replace("}", "")
        e[1] = e[1].replace("'", "")
        e[1] = e[1].replace(" ", "")
        example = 0
        for c in e[1].split(","):
            if c != '':
                currentConcepts.append((c.split(':')[0], int(c.split(':')[1])))

        rankedList = list()
        for j in range(i, len(problemsByTopic)):
            for key, value in problemsByTopic[j].items():
                concepts_in_problem = value
                problem = 0

                for v in concepts_in_problem.values():
                    problem += v * v
                problem = math.sqrt(problem)
                score = 0
                for c in currentConcepts:
                    if c[0] in concepts_in_problem:
                        # print()
                        score += c[1] * concepts_in_problem[c[0]]
                score = score / (problem)
                # score = score/len(concepts_in_problem)
                rankedList.append((score, key, j + 1))

                # currentConcepts_in_problem = concepts_in_problem & currentConcepts
                # passConcepts_in_problem = concepts_in_problem & passConcepts
                # futureConcepts_in_problem = concepts_in_problem - (currentConcepts | passConcepts)
                # if len(currentConcepts_in_problem) > 0:
                #     score = len(passConcepts_in_problem) * alpha + len(currentConcepts_in_problem) * beta - len(
                #         futureConcepts_in_problem) * gamma
                #     rankedList.append((score, key, j + 1))

        rankedList = sorted(rankedList, key=itemgetter(0), reverse=True)

        for t in range(0, len(top)):
            TP = 0
            for idx in range(0, top[t]):
                if idx < len(rankedList):
                    if rankedList[idx][2] == (i + 1):
                        TP += 1
            if top[t] <= len(rankedList):
                precision[t] += TP / top[t]
                # precision[t] = TP / top[t]
            else:
                precision[t] += TP / len(rankedList)
                # precision[t] = TP / len(rankedList)
            recall[t] += TP / len(problemsByTopic[i])
            # recall[t] = TP / len(problemsByTopic[i])
        # print("precision",i,precision)
        # print("recall",i, precision)
        something = 0
        # print(rankedList)

    precision = [x / len(examples) for x in precision]
    recall = [x / len(examples) for x in recall]
    for i in range(0, len(recall)):
        if recall[i] == 0 and precision[i] == 0:
            f1[i] = 0
        else:
            f1[i] = 2 * precision[i] * recall[i] / (recall[i] + precision[i])
    for i in range(0, len(recall)):
        print("Precision at top ", top[i], ": ", precision[i])
        print("Recall at top  ", top[i], ": ", recall[i])
        print("F1 at top  ", top[i], ": ", f1[i])
        # print(examples[9][2])

def recommendation_tfidf_error_rate(exampleFileName, problemFileName,topic_to_eval):
    examples = list()
    with open(exampleFileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != "Week":
                examples.append(row)

    # print(examples)
    # remove the last two topics
    # examples = examples[:-1]
    # get
    number_of_problems = 0
    problemsByTopic = list()
    with open(problemFileName, 'r') as f:
        reader = csv.reader(f)
        topic = 1
        problems = dict()
        idf = dict()
        for row in reader:
            # print(row)
            if row[0] != "Week":
                if int(row[3]) == topic:
                    if int(row[1]) not in problems:
                        conceptSet = dict()
                    else:
                        conceptSet = problems[int(row[1])]
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0],float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet,c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
                    # print(row[1])
                else:
                    topic += 1
                    problemsByTopic.append(problems)
                    number_of_problems+= len((problems))
                    problems = dict()
                    conceptSet = dict()
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0], float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet, c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
        problemsByTopic.append(problems)
        number_of_problems += len((problems))

    #calculate tf-idf for each problem
    for i in range(0,len(problemsByTopic)):
        for k1,v1 in problemsByTopic[i].items():
            for v2 in v1:
                # print(v2)
                # print(number_of_problems*1.0/idf[v2])
                v1[v2] = (1 + math.log(v1[v2]))*math.log10(number_of_problems*1.0/idf[v2])
            problemsByTopic[i][k1] = v1

    top = [3, 5, 10, 15]
    precision = [0, 0, 0, 0]
    recall = [0, 0, 0, 0]
    f1 = [0, 0, 0, 0]

    for i in range(0, len(examples)):
        currentConcepts = list()
        # print(e)
        e = examples[i]
        e[1] = e[1].replace("{", "")
        e[1] = e[1].replace("}", "")
        e[1] = e[1].replace("'", "")
        e[1] = e[1].replace(" ", "")
        example = 0
        for c in e[1].split(","):
            if c != '':
                currentConcepts.append((c.split(':')[0], int(c.split(':')[1])))

        rankedList = list()
        for j in range(i, len(problemsByTopic)):
            for key, value in problemsByTopic[j].items():
                concepts_in_problem = value
                problem = 0

                for v in concepts_in_problem.values():
                    problem += v * v
                problem = math.sqrt(problem)
                score = 0
                for c in currentConcepts:
                    if c[0] in concepts_in_problem:
                        # print()
                        score += c[1] * concepts_in_problem[c[0]]
                score = score / (problem)
                # score = score/len(concepts_in_problem)
                rankedList.append((score, key, j + 1))

                # currentConcepts_in_problem = concepts_in_problem & currentConcepts
                # passConcepts_in_problem = concepts_in_problem & passConcepts
                # futureConcepts_in_problem = concepts_in_problem - (currentConcepts | passConcepts)
                # if len(currentConcepts_in_problem) > 0:
                #     score = len(passConcepts_in_problem) * alpha + len(currentConcepts_in_problem) * beta - len(
                #         futureConcepts_in_problem) * gamma
                #     rankedList.append((score, key, j + 1))

        rankedList = sorted(rankedList, key=itemgetter(0), reverse=True)

        for t in range(0, len(top)):
            TP = 0
            for idx in range(0, top[t]):
                if idx < len(rankedList):
                    if rankedList[idx][2] == (i + 1):
                        TP += 1
            if top[t] <= len(rankedList):
                precision[t] = TP / top[t]
                # precision[t] = TP / top[t]
            else:
                precision[t] = TP / len(rankedList)
                # precision[t] = TP / len(rankedList)
            recall[t] = TP / len(problemsByTopic[i])
            # recall[t] = TP / len(problemsByTopic[i])

        # for t in range(0,len(top)):
        #     TP = 0
        #     for idx in range(0,top[t]):
        #         if idx < len(rankedList):
        #             if rankedList[idx][2] == (i+1):
        #                 TP+= 1
        #     if top[t] <= len(rankedList):
        #         precision[t] = TP/top[t]
        #     else:
        #         precision[t] = TP / len(rankedList)
        #     recall[t] = TP/len(problemsByTopic[i])
        if (i + 1) == topic_to_eval:
            # print(currentConcepts, "\n")
            break

    # precision = [x/len(examples) for x in precision]
    # recall = [x/len(examples) for x in recall]
    for i in range(0, len(recall)):
        if recall[i] == 0 and precision[i] == 0:
            f1[i] = 0
        else:
            f1[i] = 2 * precision[i] * recall[i] / (recall[i] + precision[i])
    return f1

def recommendation_wizard_for_tfidf(exampleFileName, problemFileName, alpha, beta, gamma, output = 1):
    examples = list()
    with open(exampleFileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != "Week":
                examples.append(row)

    # print(examples)
    # remove the last two topics
    examples = examples[:-2]
    # read problems
    number_of_problems = 0
    problemsByTopic = list()
    with open(problemFileName, 'r') as f:
        reader = csv.reader(f)
        topic = 1
        problems = dict()
        idf = dict()
        for row in reader:
            # print(row)
            if row[0] != "Week":
                if int(row[3]) == topic:
                    if int(row[1]) not in problems:
                        conceptSet = dict()
                    else:
                        conceptSet = problems[int(row[1])]
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0],float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet,c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
                    # print(row[1])
                else:
                    topic += 1
                    problemsByTopic.append(problems)
                    number_of_problems+= len((problems))
                    problems = dict()
                    conceptSet = dict()
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            # conceptSet.add((c.split(":")[0], float(c.split(":")[1])))
                            # conceptSet = AddConcept(conceptSet, c)
                            if c.split(':')[0] in conceptSet:
                                conceptSet[c.split(':')[0]] +=  float(c.split(':')[1])
                            else:
                                conceptSet[c.split(':')[0]] = float(c.split(':')[1])
                                if c.split(":")[0] in idf:
                                    idf[c.split(":")[0]] += 1
                                else:
                                    idf[c.split(":")[0]] = 1


                    problems[int(row[1])] = conceptSet
        problemsByTopic.append(problems)
        number_of_problems += len((problems))

    #calculate tf-idf for each problem
    for i in range(0,len(problemsByTopic)):
        for k1,v1 in problemsByTopic[i].items():
            for v2 in v1:
                # print(v2)
                # print(number_of_problems*1.0/idf[v2])
                v1[v2] = (1 + math.log(v1[v2]))*math.log10(number_of_problems*1.0/idf[v2])
            problemsByTopic[i][k1] = v1

    passConcepts = set()
    currentConcepts = list()
    top = [3, 5, 10, 15]
    precision = [0, 0, 0, 0]
    recall = [0, 0, 0, 0]
    f1 = [0, 0, 0, 0]
    for i in range(0, len(examples)):
        # print(e)
        e = examples[i]
        e[1] = e[1].replace("{", "")
        e[1] = e[1].replace("}", "")
        e[1] = e[1].replace("'", "")
        e[1] = e[1].replace(" ", "")
        example = 0
        for c in e[1].split(","):
            if c != '':
                #this includes only new concepts
                if c.split(':')[0] not in passConcepts:
                    currentConcepts.append((c.split(':')[0],int(c.split(':')[1])))
                    example += int(c.split(':')[1])*int(c.split(':')[1])
        example = math.sqrt(example)

        rankedList = list()
        for j in range(i, len(problemsByTopic)):
            currentConcepts_in_problem = set()
            passConcepts_in_problem = set()
            futureConcepts_in_problem = set()
            for key, value in problemsByTopic[j].items():
                concepts_in_problem = value
                # currentConcepts_in_problem = concepts_in_problem & currentConcepts
                for c in currentConcepts:
                    if c[0] in concepts_in_problem:
                        currentConcepts_in_problem.add(c[0])
                for c in passConcepts:
                    if c in concepts_in_problem:
                        passConcepts_in_problem.add(c)

                # passConcepts_in_problem = concepts_in_problem & passConcepts
                # futureConcepts_in_problem = concepts_in_problem - (currentConcepts_in_problem | passConcepts_in_problem)

                problem = 0
                for k,v in concepts_in_problem.items():
                    if k in currentConcepts_in_problem:
                        problem += v*v*beta*beta
                    elif k in passConcepts_in_problem:
                        problem += v*v*alpha*alpha
                    else:
                        problem += v * v * gamma* gamma
                problem = math.sqrt(problem)
                score = 0
                for c in currentConcepts:
                    if c[0] in concepts_in_problem:
                        # print()
                        if c[0] in currentConcepts_in_problem:
                            score += beta*c[1]*concepts_in_problem[c[0]]
                        elif c[0] in passConcepts_in_problem:
                            score += alpha * c[1] * concepts_in_problem[c[0]]
                        else:
                            score -= gamma * c[1] * concepts_in_problem[c[0]]
                score = score/(example*problem)
                rankedList.append((score, key, j + 1))

        rankedList = sorted(rankedList, key=itemgetter(0), reverse=True)

        concepts_in_current_problems = set()
        for key, value in problemsByTopic[i].items():
            for c in value:
                concepts_in_current_problems.add(c)

        for t in range(0, len(top)):
            TP = 0
            for idx in range(0, top[t]):
                if idx < len(rankedList):
                    if rankedList[idx][2] == (i + 1):
                        TP += 1
            if top[t] <= len(rankedList):
                precision[t] += TP / top[t]
            else:
                precision[t] += TP / len(rankedList)
            recall[t] += TP / len(problemsByTopic[i])

        # print(rankedList)
        passConcepts = passConcepts | concepts_in_current_problems
        # add the concepts appear in examples but not in problems chosen by instructor
        for c in currentConcepts:
            if c not in passConcepts:
                passConcepts.add(c)
        currentConcepts = list()

    precision = [x / len(examples) for x in precision]
    recall = [x / len(examples) for x in recall]
    for i in range(0, len(recall)):
        if recall[i] == 0 and precision[i] == 0:
            f1[i] = 0
        else:
            f1[i] = 2 * precision[i] * recall[i] / (recall[i] + precision[i])

    if output == 1:
        for i in range(0, len(recall)):
            print("Precision at top ", top[i], ": ", precision[i])
            print("Recall at top  ", top[i], ": ", recall[i])
            print("F1 at top  ", top[i], ": ", f1[i])

            # return F1 at top 10, since top 10 is best, so choose top 10 at standard
    return f1

def FindBestParameters():
    best_f1_3 = 0
    best_f1_5 = 0
    best_f1_10 = 0
    best_f1_15 = 0
    for a in range(1, 101):
        print("###########################")
        print(a)
        for b in range(1, 101):
            print(b)
            for c in range(1, 101):
                if a != 0 or b != 0 or c != 0:
                    f1_3, f1_5, f1_10, f1_15 = recommendation("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv", a, b, c,0)
                    if f1_3 > best_f1_3:
                        best_f1_3 = f1_3
                        alpha_best_3 = a
                        beta_best_3 = b
                        gamma_best_3 = c
                        print("Current best at top 3:",best_f1_3,"\t", alpha_best_3, beta_best_3, gamma_best_3)

                    if f1_5 > best_f1_5:
                        best_f1_5 = f1_5
                        alpha_best_5 = a
                        beta_best_5 = b
                        gamma_best_5 = c
                        print("Current best at top 5:",best_f1_5,"\t", alpha_best_5, beta_best_5, gamma_best_5)

                    if f1_10 > best_f1_10:
                        best_f1_10 = f1_10
                        alpha_best_10 = a
                        beta_best_10 = b
                        gamma_best_10 = c
                        print("Current best at top 10:",best_f1_10,"\t", alpha_best_10, beta_best_10, gamma_best_10)

                    if f1_15 > best_f1_15:
                        best_f1_15 = f1_15
                        alpha_best_15 = a
                        beta_best_15 = b
                        gamma_best_15 = c
                        print("Current best at top 15:",best_f1_15,"\t", alpha_best_15, beta_best_15, gamma_best_15)

    print("RESULT")
    print("Top 3: ",best_f1_3, alpha_best_3, beta_best_3, gamma_best_3)
    print("Top 5: ", best_f1_5, alpha_best_5, beta_best_5, gamma_best_5)
    print("Top 10: ", best_f1_10, alpha_best_10, beta_best_10, gamma_best_10)
    print("Top 15: ", best_f1_15, alpha_best_15, beta_best_15, gamma_best_15)

def DrawContour():
    best_f1 = 0
    f1_15 = list()
    x = np.arange(101)/10
    y = np.arange(101)/10
    for b in range(0, 101):
        # print("###########################")
        for c in range(0, 101):
            # z[4] = recommendation("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv", 2,
            #                        b, c)
            f1_15.append(recommendation("data/arto.examples_with_concepts.aggregated.csv",
                                           "data/arto.assignment.csv",1.25, b,c,0)[3])
            if f1_15[-1] >= best_f1:
                best_f1 = f1_15[-1]
                para1_best = b
                para2_best = c
                print(best_f1,1.25, para1_best,para2_best)

    # print(z)
    z = np.copy(f1_15)
    x1, y1 = np.meshgrid(x, y)
    z = z.reshape(len(x1), len(y1))
    xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate
    # rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    # zi = rbf(xi, yi)

    plt.imshow(z, vmin=z.min(), vmax=z.max(), origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()])
    # plt.scatter(x, y, c=z)
    plt.title(r'$\alpha$ = 0.125')
    plt.ylabel(r'$\beta$')
    plt.xlabel(r'$\gamma$')
    plt.colorbar()
    plt.show()
    # # print(z)
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # x1, y1 = np.meshgrid(x, y)
    # z = z.reshape(len(x1), len(y1))
    # plt.contour(x1, y1, z)
    # ax.contourf(x, y, z)
    # # plt.scatter(x, y, c=z1)
    # plt.colorbar()
    # plt.show()
    print("RESULT")
    print(best_f1,1.25,para1_best, para2_best)

#This function perform error rates of different number of examples
def CheckErrorRate():
    # topic = [(2,32),(3,13),(4,18),(5,22),(6,12),(7,30),(8,35),(9,37)]
    # topic = [(1,6),(2, 32), (3, 13), (4, 15), (5, 22), (6, 12), (7, 30), (8, 72), (9, 17)]
    topic = [(2, 32), (3, 13), (4, 3),(5,12), (6, 22), (7, 12), (8, 30), (9, 72)]
    # topic = [(2, 32), (3, 13), (5, 12), (6, 22), (8, 30)]
    # topic = [(8, 30)]
    label = list() #save the scatters to add legend
    name_of_topic = list()  #names of the scatters by topic
    for t in topic:
        name_of_topic.append("Topic "+str(t[0]))
        max = 10
        number_of_examples = np.arange(1,max+1)
        f1 = [0]*(max)
        for time in range(0, 10):
            for i in range(1,max+1):
                seed(time+2)
                examples = list()
                for j in range(0,i):
                    ranNum = randint(1,t[1])
                    while ranNum in examples:
                        ranNum = randint(1, topic[0][1])
                    examples.append((ranNum))
                # print(examples)
                if i ==max:
                    hkc =0
                print(i)
                print(examples)
                aggregate_data.aggregate_arto_with_random_examples("data/arto.examples_with_concepts.csv", "data/arto.examples_with_concepts.aggregated.csv",examples,t[0])
                f1[i-1] += recommendation_error_rate("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv", 0.2, 1, 1.5, t[0],0)[3]
                # f1[i - 1] += recommendation_tfidf_error_rate("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv",t[0])[3]
        f1 = [x / 10 for x in f1]
        label.append(plt.scatter(number_of_examples,f1, s =5, alpha=0.8))
        plt.plot(number_of_examples, f1)
    # print(f1)
    plt.xlabel("Number of examples")
    plt.ylabel("F1 score at top 15")
    # plt.title("tf-idf")
    plt.title("wizard")
    plt.legend(label,
               name_of_topic,
               scatterpoints=1,
               loc='upper left',
               bbox_to_anchor=(0.8,0.3),
               ncol=1,
               fontsize=8)
    plt.show()
        # print(examples

# DrawContour()
# aggregate_data.aggregate_arto("data/arto.examples_with_concepts.csv", "data/arto.examples_with_concepts.aggregated.csv")
# recommendation("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv", 0.2, 1, 1.5)
# print("\n\n")
# recommendation_tfidf("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv")
# print("\n\n")
# recommendation_wizard_for_tfidf("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv", 0.2, 1, 1.5)
CheckErrorRate()
# print("\n\n")
# recommendation_tfidf_for_wizard("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv",0.2, 1, 1.5)
# recommendation_combined("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv", 0.2, 1, 1.5)

# FindBestParameters()

# a ="dsadafgert"
# a = a.replace("\[asf]","")
# print(a