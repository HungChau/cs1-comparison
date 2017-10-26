import csv
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt

def recommendation(exampleFileName, problemFileName, alpha, beta, gamma):
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
                concepts_in_problem = value
                currentConcepts_in_problem = concepts_in_problem & currentConcepts
                passConcepts_in_problem = concepts_in_problem & passConcepts
                futureConcepts_in_problem =concepts_in_problem - (currentConcepts|passConcepts)
                if len(currentConcepts_in_problem) > 0:
                    score = len(passConcepts_in_problem)*alpha+len(currentConcepts_in_problem)*beta-len(futureConcepts_in_problem)*gamma
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
            concepts_in_current_problems = concepts_in_current_problems | value

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
    # for i in range(0,len(recall)):
    #     print("Precision at top ",top[i],": ", precision[i])
    #     print("Recall at top  ",top[i],": ", recall[i])
    #     print("F1 at top  ",top[i],": ", 2*precision[i]*recall[i]/(recall[i]+precision[i]))

    #return F1 at top 10, since top 10 is best, so choose top 10 at standard
    return 2*precision[0]*recall[0]/(recall[0]+precision[0]),2*precision[1]*recall[1]/(recall[1]+precision[1]),2*precision[2]*recall[2]/(recall[2]+precision[2]),2*precision[3]*recall[3]/(recall[3]+precision[3])
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
    examples = examples[:-2]
    # get
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
                    if row[1] not in problems:
                        conceptSet = set()
                    else:
                        conceptSet = problems[row[1]]
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            conceptSet.add((c.split(":")[0],float(c.split(":")[1])))
                            if c.split(":")[0] in idf:
                                idf[c.split(":")[0]] += 1
                            else:
                                idf[c.split(":")[0]] = 1

                    problems[int(row[1])] = conceptSet
                    # print(row[1])
                else:
                    topic += 1
                    problemsByTopic.append(problems)
                    problems = dict()
                    conceptSet = set()
                    conceptList = row[5].split(",")
                    for c in conceptList:
                        if c != '':
                            conceptSet.add((c.split(":")[0], float(c.split(":")[1])))
                            if c.split(":")[0] in idf:
                                idf[c.split(":")[0]] += 1
                            else:
                                idf[c.split(":")[0]] = 1

                    problems[int(row[1])] = conceptSet
        problemsByTopic.append(problems)
    print(examples[9][2])


def FindBestParameters():
    best_f1_3 = 0
    best_f1_5 = 0
    best_f1_10 = 0
    best_f1_15 = 0
    for a in range(0, 101):
        print("###########################")
        print(a)
        for b in range(0, 101):
            print(b)
            for c in range(0, 101):
                if a == 0 and b == 0 and c == 0:
                    break
                # print(a,b,c)
                f1_3, f1_5, f1_10, f1_15 = recommendation("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv", a, b, c)
                if f1_3 > best_f1_3:
                    best_f1_3 = f1_3
                    alpha_best_3 = a
                    beta_best_3 = b
                    gamma_best_3 = c
                    print("Current best at top 3:",best_f1_3, alpha_best_3, beta_best_3, gamma_best_3)

                if f1_5 > best_f1_5:
                    best_f1_5 = f1_5
                    alpha_best_5 = a
                    beta_best_5 = b
                    gamma_best_5 = c
                    print("Current best at top 5:",best_f1_5, alpha_best_5, beta_best_5, gamma_best_5)

                if f1_10 > best_f1_10:
                    best_f1_10 = f1_10
                    alpha_best_10 = a
                    beta_best_10 = b
                    gamma_best_10 = c
                    print("Current best at top 10:",best_f1_10, alpha_best_10, beta_best_10, gamma_best_10)

                if f1_15 > best_f1_15:
                    best_f1_15 = f1_15
                    alpha_best_15 = a
                    beta_best_15 = b
                    gamma_best_15 = c
                    print("Current best at top 15:",best_f1_15, alpha_best_15, beta_best_15, gamma_best_15)

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
                                           "data/arto.assignment.csv", b,c, 26))
            if f1_15[-1] > best_f1:
                best_f1 = f1_15[-1]
                alpha_best = b
                beta_best = c
                print(best_f1, alpha_best, beta_best, 26)

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
    plt.title(r'$\gamma$ = -2.6')
    plt.ylabel(r'$\alpha$')
    plt.xlabel(r'$\beta$')
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
    print(best_f1,alpha_best, beta_best, 26)

# DrawContour()
# recommendation("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv", 0.2, 1, 2.6)
# recommendation_tfidf("data/arto.examples_with_concepts.aggregated.csv", "data/arto.assignment.csv")
FindBestParameters()