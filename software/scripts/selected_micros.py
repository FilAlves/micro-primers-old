import sys

readfile = open(sys.argv[1], "r")
outfile1 = open(sys.argv[2], "w")
outfile2 = open(sys.argv[3], "w")

dic_cluster = {}

for line in readfile:
    
    #Split by tab
    selected_line = line.split("\t")

    #Creating dictionary for selection of one sequencing per cluster
    if not selected_line[9] in dic_cluster.keys():
        dic_cluster[selected_line[9]] = selected_line[0]

        #Creating outfile with sequenceID, ssr, start and end positions of the ssr
        selected_micros = list( selected_line[i] for i in [0, 3, 5, 6])
        outfile2.write("\t".join(selected_micros) + "\n")

#creating tab_selected
for keys,values in dic_cluster.items():
    outfile1.write(values + "\n")
