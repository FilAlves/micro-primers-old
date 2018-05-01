import os
#Creation of hidden temp file
os.system("mkdir .temp")

file = open("input_text.txt", "r")
lines = file.read().splitlines()

#iniciation of trimmomatic
def trimmomatic():
    os.system("echo 'Trimmomatic working...'")
    os.system(
        "java -jar software/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 "
        "%s %s "
        ".temp/trim_out_trimmed_R1.fastq .temp/trim_out_unpaired_R1.fastq "
        ".temp/trim_out_trimmed_R2.fastq .temp/trim_out_unpaired_R2.fastq "
        "ILLUMINACLIP:/home/filalves/projecto/software/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 "
        "LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 2> .temp/trim_log.txt"
        %(lines[0], lines[1])
        )

#Cutadapt
def cutadapt():
    os.system("echo 'Cutadapt working...'")
    os.system("cutadapt -a %s -g %s -o .temp/cut_out_nolink_R1.fastq .temp/trim_out_trimmed_R1.fastq 2> .temp/cut_log_r1.txt" %(lines[2], lines[3]) )
    os.system("cutadapt -a %s -g %s -o .temp/cut_out_nolink_R2.fastq .temp/trim_out_trimmed_R2.fastq 2> .temp/cut_log_r2.txt" %(lines[2], lines[3]) )

#Join sequences
def flash():
    os.system("echo 'Flash working...'")
    os.system("make software/FLASH-1.2.11/flash")
    os.system("software/FLASH-1.2.11/flash .temp/cut_out_nolink_R1.fastq .temp/cut_out_nolink_R2.fastq -M 220 -o .temp/flash_out 2>&1 |"
             " tee .temp/flash.log")

def grep():
    os.system("echo 'Selecting sequences with restriction enzime patterns...'")
    os.system("grep -B1 '^GATC\(\w*\)GATC$' .temp/flash_out.extendedFrags.fastq | sed 's/^@/>/' | perl -pe 's/--\n//g' > .temp/grep_out.fasta")

#Change id's
def ids():
    os.system("echo 'Chaging ids...'")
    os.system("perl software/scripts/changeids.pl .temp/grep_out.fasta")

#Search Microssatelites
def misa():
    os.system("echo 'Misa working...'")
    os.system("perl software/scripts/misa.pl .temp/ids_out.fasta 2> .temp/misa_log.txt")

#Length Calculation
def length_calc():
    os.system("echo 'Calculating sequences lengths...'")
    os.system("perl software/scripts/extraelength.pl .temp/ids_out.fasta")

trimmomatic()
cutadapt()       
flash()
grep()            
ids()             
misa()            
length_calc()

os.system("echo 'Done!'")
