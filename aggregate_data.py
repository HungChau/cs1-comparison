import csv

def aggregate(input_file, output_file):
    with open(input_file,'r') as f:
        reader = csv.reader(f)
        # print(reader)
        current_concept_list =[]
        new_concept_list =[]
        dic_concept = dict()
        with open(output_file, 'w') as w:
            writer = csv.writer(w)
            week = -1
            week_column = 3
            concept_column = 4
            for row in reader:
                if week == -1:
                    week = int(row[week_column])
                if int(row[3]) > week:
                    writer.writerow([week, dic_concept, new_concept_list])
                    dic_concept = dict()
                    new_concept_list = []
                    week += 1
                    content_concepts = row[concept_column].split(",")
                    print(content_concepts)
                    for c in content_concepts:
                        dic_concept[c.split(":")[0]] = int(c.split(":")[1])
                        if c.split(":")[0] not in current_concept_list:
                            new_concept_list.append(c.split(":")[0])
                            current_concept_list.append(c.split(":")[0])
                else:
                    content_concepts = row[concept_column].split(",")
                    print(content_concepts)
                    for c in content_concepts:
                        if c.split(":")[0] in dic_concept:
                            dic_concept[c.split(":")[0]] += int(c.split(":")[1])
                        else:
                            dic_concept[c.split(":")[0]] = int(c.split(":")[1])
                            if c.split(":")[0] not in current_concept_list:
                                new_concept_list.append(c.split(":")[0])
                                current_concept_list.append(c.split(":")[0])
            writer.writerow([week, dic_concept, new_concept_list])

def aggregate_arto(input_file, output_file):
    with open(input_file,'r') as f:
        reader = csv.reader(f)
        # print(reader)
        current_concept_list =[]
        new_concept_list =[]
        dic_concept = dict()
        with open(output_file, 'w') as w:
            writer = csv.writer(w)
            week = -2
            week_column = 3
            concept_column = 6
            for row in reader:
                if week < 0:
                    week += 1
                    if week == 0:
                        week = int(row[week_column])
                else:
                    if row[4] == "code_sample":
                        row[concept_column] = row[concept_column][0:len(row[concept_column]) - 1]
                        if int(row[3]) > week:
                            writer.writerow([week, dic_concept, new_concept_list])
                            dic_concept = dict()
                            new_concept_list = []
                            week += 1
                            content_concepts = row[concept_column].split(",")
                            print(content_concepts)
                            for c in content_concepts:
                                dic_concept[c.split(":")[0]] = int(c.split(":")[1])
                                if c.split(":")[0] not in current_concept_list:
                                    new_concept_list.append(c.split(":")[0])
                                    current_concept_list.append(c.split(":")[0])
                        else:
                            content_concepts = row[concept_column].split(",")
                            print(content_concepts)
                            for c in content_concepts:
                                if c.split(":")[0] in dic_concept:
                                    dic_concept[c.split(":")[0]] += int(c.split(":")[1])
                                else:
                                    dic_concept[c.split(":")[0]] = int(c.split(":")[1])
                                    if c.split(":")[0] not in current_concept_list:
                                        new_concept_list.append(c.split(":")[0])
                                        current_concept_list.append(c.split(":")[0])
            writer.writerow([week, dic_concept, new_concept_list])

# aggregate("data/andrew.examples_with_concepts.csv", "data/andrew.examples_with_concepts.aggregated.csv")
# aggregate("data/andrew.problems_with_concepts.csv", "data/andrew.problems_with_concepts.aggregated.csv")
# aggregate("data/peter.problems_with_concepts.csv", "data/peter.problems_with_concepts.aggregated.csv")
aggregate("data/peter.examples_with_concepts.csv", "data/peter.examples_with_concepts.aggregated.csv")
# aggregate_arto("data/arto.examples_with_concepts.csv", "data/arto.examples_with_concepts.aggregated.csv")

# assignments(1,"assignment-baselines-and-solutions-with-concepts.csv", "assignment-baselines-and-solutions-with-concepts-processed.csv")
# dic = {'Hung':15, "Cuong":14}
# if dic['Hungsad'] != NULL:
#     print(dic['Hungsd'])