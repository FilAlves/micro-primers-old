import os
#Creation of hidden temp file
#os.system("mkdir .temp"))

file = open("test_text.txt", "r")
lines = file.read().splitlines()

#iniciation of trimmomatic
print(
    "java -jar /Trimmomatic-Src-0.36/trimmomatic-0.33.jar PE -phred33 "
    "%s %s "
    "trim_out_trimmed_R1.fastq trim_out_unpaired_R1.fastq "
    "trim_out_trimmed_R2.fastq trim_out_unpaired_R2.fastq "
    "ILLUMINACLIP:/media/amunoz/bio1/software/Trimmomatic-0.33/adapters/TruSeq2-PE.fa:2:30:10 "
    "LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15"
    %(lines[0], lines[1])
    )

#Cutadapt
os.system("cutadapt -a %s -g %d -o cut_out_nolink_R1.fastq trim_out_trimmed_R1.fastq" %(lines[2], lines[3]) )
os.system("cutadapt -a %s -g %d -o cut_out_nolink_R2.fastq trim_out_trimmed_R2.fastq" %(lines[2], lines[3]) )

#Join sequences
os.sytem("../software/FLASH-1.2.11/flash cut_out_nolink_R1.fastq cut_out_nolink_R2.fastq -M 220 -o flash_out 2>&1 |"
         " tee flash.log"

#hkj
os.system("grep -B1 '^GATC\(\w*\)GATC$' flash_out.extendedFrags.fastq | sed 's/^@/>/' | perl -pe 's/--\n//g' > good_frags.fasta")

#Change id's
os.system("perl changeids.pl good_frags.fasta")

#Search Microssatelites
os.system("../software/misa.pl good_frags_idchanged.fasta")

#Length Calculation
os.system("perl ../micros_joint/extraelength.pl good_frags_idchanged.fasta")
