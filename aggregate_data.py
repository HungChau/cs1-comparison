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
        count =0
        number_of_examples = 0
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
                if week > -1:
                    if row[4] == "code_sample":
                        count+=1

                        row[concept_column] = row[concept_column][0:len(row[concept_column]) - 1]
                        #replace ';' by ',' if the format uses ';' to separate concepts
                        row[concept_column] = row[concept_column].replace(";",",")
                        if int(row[3]) > week:
                            print(number_of_examples)
                            number_of_examples=1
                            # number_of_examples =0
                            writer.writerow([week, dic_concept, new_concept_list])
                            dic_concept = dict()
                            new_concept_list = []
                            week = int(row[3])
                            content_concepts = row[concept_column].split(",")
                            # print(content_concepts)
                            for c in content_concepts:
                                dic_concept[c.split(":")[0]] = int(c.split(":")[1])
                                if c.split(":")[0] not in current_concept_list:
                                    new_concept_list.append(c.split(":")[0])
                                    current_concept_list.append(c.split(":")[0])
                        else:
                            number_of_examples += 1
                            content_concepts = row[concept_column].split(",")
                            # print(content_concepts)
                            for c in content_concepts:
                                if c.split(":")[0] in dic_concept:
                                    dic_concept[c.split(":")[0]] += int(c.split(":")[1])
                                else:
                                    dic_concept[c.split(":")[0]] = int(c.split(":")[1])
                                    if c.split(":")[0] not in current_concept_list:
                                        new_concept_list.append(c.split(":")[0])
                                        current_concept_list.append(c.split(":")[0])
            writer.writerow([week, dic_concept, new_concept_list])
        print(number_of_examples)
        print("Count: ", count)

#this temporary function is used to create data to test error rates of the wizard with different number of examples
def aggregate_arto_with_random_examples(input_file, output_file, examples, topic):
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        # print(reader)
        current_concept_list = []
        new_concept_list = []
        dic_concept = dict()
        count = 0
        example_index = -1
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
                if week > -1:
                    if row[4] == "code_sample":
                        if example_index==-1 and int(row[3]) == topic: #start index examples of the topic to add to the data
                            example_index = 1

                            #to deal with the case that the previous row is a "problem" row, so the previous topic needs to be written
                            if week < topic:
                                writer.writerow([week, dic_concept, new_concept_list])
                                dic_concept = dict()
                                new_concept_list = []
                                week = topic
                        else:
                            if example_index >=1:
                                example_index +=1

                        if week != topic or (week==topic and example_index in examples):
                            count += 1
                            row[concept_column] = row[concept_column][0:len(row[concept_column]) - 1]
                            if int(row[3]) > week:
                                writer.writerow([week, dic_concept, new_concept_list])
                                dic_concept = dict()
                                new_concept_list = []
                                week = int(row[3])
                                content_concepts = row[concept_column].split(",")
                                # print(content_concepts)
                                for c in content_concepts:
                                    dic_concept[c.split(":")[0]] = int(c.split(":")[1])
                                    if c.split(":")[0] not in current_concept_list:
                                        new_concept_list.append(c.split(":")[0])
                                        current_concept_list.append(c.split(":")[0])
                            else:
                                content_concepts = row[concept_column].split(",")
                                # print(content_concepts)
                                for c in content_concepts:
                                    if c.split(":")[0] in dic_concept:
                                        dic_concept[c.split(":")[0]] += int(c.split(":")[1])
                                    else:
                                        dic_concept[c.split(":")[0]] = int(c.split(":")[1])
                                        if c.split(":")[0] not in current_concept_list:
                                            new_concept_list.append(c.split(":")[0])
                                            current_concept_list.append(c.split(":")[0])
                        elif week==topic:
                            row[concept_column] = row[concept_column][0:len(row[concept_column]) - 1]
                            if int(row[3]) > week:
                                # print(example_index)
                                count += 1
                                # print(new_concept_list)
                                writer.writerow([week, dic_concept, new_concept_list])
                                dic_concept = dict()
                                new_concept_list = []
                                week = int(row[3])
                                content_concepts = row[concept_column].split(",")
                                # print(content_concepts)
                                for c in content_concepts:
                                    dic_concept[c.split(":")[0]] = int(c.split(":")[1])
                                    if c.split(":")[0] not in current_concept_list:
                                        new_concept_list.append(c.split(":")[0])
                                        current_concept_list.append(c.split(":")[0])
            writer.writerow([week, dic_concept, new_concept_list])
        # print("Count: ", count)

# aggregate("data/andrew.examples_with_concepts.csv", "data/andrew.examples_with_concepts.aggregated.csv")
# aggregate("data/andrew.problems_with_concepts.csv", "data/andrew.problems_with_concepts.aggregated.csv")
# aggregate("data/peter.problems_with_concepts.csv", "data/peter.problems_with_concepts.aggregated.csv")
# aggregate("data/peter.examples_with_concepts.csv", "data/peter.examples_with_concepts.aggregated.csv")
# aggregate_arto("data/arto.examples_with_concepts.csv", "data/arto.examples_with_concepts.aggregated.csv")
# aggregate_arto("data/julio.examples_with_concepts.csv", "data/julio.examples_with_concepts.aggregated.csv")
# aggregate_arto_with_random_examples("data/arto.examples_with_concepts.csv", "data/arto.examples_with_concepts.aggregated.csv",[1,2], 2)

# assignments(1,"assignment-baselines-and-solutions-with-concepts.csv", "assignment-baselines-and-solutions-with-concepts-processed.csv")
# dic = {'Hung':15, "Cuong":14}
# if dic['Hungsad'] != NULL:
#     print(dic['Hungsd'])
