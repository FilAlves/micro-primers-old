import sys

readfile_csv = open(sys.argv[1], "r")
readfile_length = open(sys.argv[2], "r")

outfile = open(sys.argv[3],"w")

#Creating dicitonary with SeqID and ssr length
dic_length = {}

# Dictionary creations
for line in readfile_length:

    #Spliting file by tabs
    selected_line = line.split("\t")

    #Saving only 10 first caracters of ID.
    dic_length[selected_line[0][0:10]] = selected_line[1]

for line in readfile_csv:
    selected_line = line.split("\t")

    #Removing \n from end tab
    selected_line[6] = selected_line[6].rstrip()

    #Creating new tab with ssr length
    if selected_line[0][0:10] in dic_length.keys():
        selected_line.append(dic_length[selected_line[0][0:10]])
        outfile.write("\t".join(selected_line))
