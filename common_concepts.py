import csv

def python_classes(path1, path2, path3):
    concept_list_1 = []
    with open(path1, 'r') as f1:
        reader = csv.reader(f1)
        for row in reader:
            row[2] = row[2].replace('[','')
            row[2] = row[2].replace(']', '')
            row[2] = row[2].replace("'", "")
            row[2] = row[2].replace(' ', '')
            if row[2] != '':
                concept_list_1 = concept_list_1 + row[2].split(",")
    concept_list_2 = []
    with open(path2, 'r') as f1:
        reader = csv.reader(f1)
        for row in reader:
            row[2] = row[2].replace('[','')
            row[2] = row[2].replace(']', '')
            row[2] = row[2].replace("'", "")
            row[2] = row[2].replace(' ', '')
            if row[2] != '':
                concept_list_2 = concept_list_2 + row[2].split(",")

    with open(path3, "w") as f:
        f.write("The common concepts (")
        f.write(str(len(list(set(concept_list_1).intersection(set(concept_list_2))))))
        f.write("): ")
        f.write(str(list(set(concept_list_1).intersection(set(concept_list_2)))))
        f.write("\nThe concepts taught in C1 but nor C2 (")
        f.write(str(len(list(set(concept_list_1).difference(set(concept_list_2))))))
        f.write("): ")
        f.write(str(list(set(concept_list_1).difference(set(concept_list_2)))))
        f.write("\nThe concepts taught in C2 but nor C1 (")
        f.write(str(len(list(set(concept_list_2).difference(set(concept_list_1))))))
        f.write("): ")
        f.write(str(list(set(concept_list_2).difference(set(concept_list_1)))))
    print(set(concept_list_1).intersection(set(concept_list_2)))
    print(set(concept_list_1).difference(set(concept_list_2)))
    print(set(concept_list_2).difference(set(concept_list_1)))

python_classes("data/peter.examples_with_concepts.aggregated.csv", "data/andrew.examples_with_concepts.aggregated.csv", "data/python_compare_concepts.txt")
python_classes("data/arto.examples_with_concepts.aggregated.csv", "data/arto.examples_with_concepts.aggregated.csv", "data/java_compare_concepts.txt")


