import sys

readfile = open(sys.argv[1], "r")
outfile = open(sys.argv[2], "w")
outfile2 = open(sys.argv[3], "w")
#outfile3 = open(sys.argv[4], "w")

#Minimal number of bases after and before SSR
min_ext_dist = 50

#Mnimal repetitions of SSR
min_rep = 5

#Types of ssr to exclude from further search
exclude_ssr = ["p1","c","c*"]


for line in readfile:
    #Split by tab
    selected_line = line.split("\t")

    #Select line which do not contain c, c* and p1 type SSR
    if not selected_line[2] in exclude_ssr:

        #Remove second "_" from ID. It messes with splitSSR script.
        remove_under = list(selected_line[0])
        for i in range (10, (len(remove_under))-1):
            if remove_under[i] == "_":
                remove_under[i] = " "
        selected_line[0] = "".join(remove_under)

        # Selecting only sequences that have at least 50 bases before and after the SSR
        if int(selected_line[7]) - int(selected_line[6]) >= min_ext_dist and int(selected_line[5]) >= min_ext_dist:
            good_micros = list( selected_line[i] for i in [0, 5, 6, 7])
            outfile.write("\t".join(good_micros))
            outfile2.write("\t".join(selected_line))


#Adding "\n" to the end of the file. It alsos messes with splitSSR script
outfile.write("\n")
