import csv

def assignments(type, file_input_name, file_output_name):
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

assignments(0,"data/arto.examples.csv", "data/arto.examples_with_concepts.csv")
# assignments(1,"assignment-baselines-and-solutions-with-concepts.csv", "assignment-baselines-and-solutions-with-concepts-processed.csv")