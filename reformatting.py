import csv

#Sort the nodes in the embedding file to be ascending and format to csv.
def sort_format_data(embedding_file):
    with open('embeddingfiles/' + embedding_file, 'r') as in_file:
        stripped = list((line.strip() for line in in_file))
        lines = []
        for line in stripped[1:]:
            split = line.split(" ")
            lines.append(split)
        
        lines.sort(key=lambda x: int(x[0]))
        size_dimensions = stripped[0].split(" ")
        for dimension in range(int(size_dimensions[1])-3):
            size_dimensions.append('')
        
        lines.insert(0, size_dimensions)

    with open('embeddingfiles/formattedfiles/formatted_' + embedding_file + ".csv", 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)

sort_format_data('APP-BlogCatalog-edgelist.txt.embeddings-64.src')

#Sort the labels to be ascending and add a top row to work with pandas dataframe
def sort_format_labels(label_file):
    with open('labelfiles/' +label_file, 'r') as f:
        r = csv.reader(f)
        data = [line for line in r]
        data.sort(key=lambda x: int(x[0]))
        
    with open('labelfiles/formattedfiles/formatted_'+label_file,'w',newline='') as f:
        w = csv.writer(f)
        w.writerow([0,0])
        w.writerows(data)


#Finds which labels are missing in the embedding file and number of rows
def find_labels(datafile, labelfile): 
    with open(datafile, 'r') as in_file:
        data=list(csv.reader(in_file))
        number_rows = data[0][0]
        data.pop(0)


    with open(labelfile, 'r') as label_file:
        labels=list(csv.reader(label_file))

        missing_nodes = []
        for i in range(len(data) -1):
            try:
                if int(data[i][0])+1 != int(data[i+1][0]):
                    difference = int(data[i+1][0]) - int(data[i][0])
                    for j in range(1, difference):
                        missing_nodes.append(int(data[i][0])+j)
            except:
                pass

    length = int(number_rows) + len(missing_nodes)
    return missing_nodes, length


#Delete duplicated in the list of labels
def delete_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


#For each node that has multiple labels, add the label to a list and return the list
def multi_label_nodes(labelfile):
    with open('labelfiles/formattedfiles/formatted_' + labelfile, 'r') as in_file:
        r = csv.reader(in_file)
        data = [line for line in r]

    duplicates = []
    for i in range(len(data) -1):
        try: 
            if int(data[i][0]) == int(data[i+1][0]):
                duplicates.append(data[i][0])
        except:
            pass

    return duplicates

#Add nodes to the embedding to match the labels. Edit the first cell to the new number of rows
def add_nodes_embedding(datafile, labelfile):
    total_rows = []
    counter = 0
    duplicates = multi_label_nodes(labelfile)
    with open('embeddingfiles/formattedfiles/formatted_'+ datafile + '.csv', 'r') as f:
        mycsv = csv.reader(f)
        total_rows.append(next(mycsv))
        for row in mycsv:
            total_rows.append(row)
            for dublicate in duplicates:
                if row[0] == dublicate:
                    total_rows.append(row)
                    counter += 1

        old_total = int(total_rows[0][0])
        total_rows[0][0] = int(old_total) + counter
    with open('embeddingfiles/formattedfiles/formatted_'+ datafile + '.csv', 'w', newline='') as g:
        writer = csv.writer(g)
        for row in total_rows:
            writer.writerow(row)