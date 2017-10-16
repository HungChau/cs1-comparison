import csv

def ReformatFile(type, file_input_name, file_output_name):
    with open(file_input_name) as f:
        with open(file_output_name, 'w') as w:
            writer = csv.writer(w)
            for line in f:
                start = 0
                row =[]
                idx = line.index(";",start)
                row.append(line[start:idx])
                start = idx+1
                idx = line.index(";", start)
                row.append(line[start:idx])
                start = idx+1
                idx = line.index(";", start)
                row.append(line[start:idx])
                start = idx+1
                idx = line.index(";", start)
                row.append(line[start:idx])
                start = idx + 1
                if type ==1:
                    idx = line.index(";", start)
                    row.append(line[start:idx])
                    start = idx + 1
                idx = line.index(";", start)
                temp = line[start:idx]
                idx = line.index(";", start)
                start = idx + 1
                row.append(line[start:])
                row.append(temp)
                # print(idx)
                # row.append(line)
                writer.writerow(row)
                print(row)
                # print(line)

def ProcessAssignment(fileInputName, fileOutputName, fileExampleName):
    examples = list()
    problems = dict() #get topic number for problems
    with open(fileExampleName,"r") as fread:
        reader = csv.reader(fread)
        for row in reader:
            examples.append(row)
            if "problem_" in row[4]:
                problems[row[4]] = row[3]
                # print(row[3], row[4])
    with open(fileInputName,'r') as fread:
        reader = csv.reader(fread)
        with open(fileOutputName, 'w') as fwrite:
            writer = csv.writer(fwrite)
            for row in reader:
                if row[0] =="Week":
                    writer.writerow([row[0],row[1],row[2],"Topic","Code","Concepts"])
                elif row[3] != "baseline":
                    print("problem_"+str(int(row[1])))
                    if "problem_"+str(int(row[1])) in problems:
                        writer.writerow([row[0],row[1], row[2],problems["problem_"+str(int(row[1]))],row[5], row[6]])

    print(problems)

# ReformatFile(0,"data/arto.examples.csv", "data/arto.examples_with_concepts.csv")
# ReformatFile(1,"assignment-baselines-and-solutions-with-concepts.csv", "assignment-baselines-and-solutions-with-concepts-processed.csv")
ProcessAssignment("data/arto/assignment-baselines-and-solutions-with-concepts-processed.csv", "data/arto.assignment.csv", "data/arto.examples_with_concepts.csv")