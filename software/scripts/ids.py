def change_ids_and_calc_len(rf1, of1, of2):

    #Opening files

    readfile1 = open(rf1, "r")
    outfile1 = open(of1, "w")
    outfile2 = open(of2, "w")

    #ID counter
    counter = 1

    #ID saver
    len_line = ""

    # Cycle trough all lines
    for line in readfile1:

        #Selecting only lines with sequence ID
        if line[0] == ">":

            #Adding ID
            ids_line = line[0] + str(counter) + "_" + line[1:]

            #Saving ID string excluding ">"
            len_line = ids_line[1:]

            counter += 1
            outfile1.write(ids_line)

        #Selecting DNA sequence
        else:
            outfile1.write(line)

            #Calculate sequence size
            size = len(line) - 1

            #Constructing final string
            len_line = len_line.strip("\n")
            len_line = len_line + "\t" + str(size)
            outfile2.write(len_line + "\n")



def len_add(rf1, rf2, of1):
    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

    dic_size = {}

    for line in readfile1:
        selected_line = line.split("\t")
        dic_size[selected_line[0][0:10]] = selected_line[1]

    for line in readfile2:
        selected_line = line.split("\t")
        if selected_line[0][0:10] in dic_size.keys():
            selected_line[6] = selected_line[6].rstrip()
            selected_line.append(dic_size[selected_line[0][0:10]])
            outfile1.write("\t".join(selected_line))


def split(rf1, rf2, of1):
    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

    #Criation Dictionary with ID, start and end of SSR
    dic_micros = {}

    for line in readfile1:
        selected_line = line.split("\t")
        if len(selected_line) > 1:
            dic_micros[selected_line[0][0:10]] = [selected_line[1], selected_line[2]]

    # Search and cut of SSR in selected Sequences
    for line in readfile2:
        selected_line = line.split("\t")

        #Dictionary search
        if selected_line[0][1:11] in dic_micros:
            #Selection of the next line, containing the DNA sequence
            nextline = readfile2.readline()

            #Defining start and end of SSR
            first_cut = int(dic_micros.get(selected_line[0][1:11])[0])
            second_cut = int(dic_micros.get(selected_line[0][1:11])[1]) + 1

            #Slicing away SSR
            nextline = nextline[0 : first_cut] + nextline[second_cut: ]

            #Output writing
            outfile1.write(selected_line[0])
            outfile1.write(nextline)

        #StopIteneration()
    #for keys,values in dic_micros.items():
        #print (values)

#len_add(".temp/length_calc_out.fasta", ".temp/misa_out.misa", ".temp/length_add_out.misa")
split(".temp/good_micros_out.fasta", ".temp/ids_out.fasta", ".temp/split_out.fasta" )




#for keys,values in dic_size.items():
#    print (values)
