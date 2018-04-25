import os
#Creation of hidden temp file
os.system("mkdir .temp")

file = open("test_text.txt", "r")
lines = file.read().splitlines()

#iniciation of trimmomatic
def trimmomatic():
    os.system(
        "java -jar software/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 "
        "%s %s "
        ".temp/trim_out_trimmed_R1.fastq .temp/trim_out_unpaired_R1.fastq "
        ".temp/trim_out_trimmed_R2.fastq .temp/trim_out_unpaired_R2.fastq "
        "ILLUMINACLIP:/home/filalves/projecto/software/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 "
        "LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15"
        %(lines[0], lines[1])
        )

#Cutadapt
def cutadapt():
    os.system("cutadapt -a %s -g %s -o .temp/cut_out_nolink_R1.fastq .temp/trim_out_trimmed_R1.fastq" %(lines[2], lines[3]) )
    os.system("cutadapt -a %s -g %s -o .temp/cut_out_nolink_R2.fastq .temp/trim_out_trimmed_R2.fastq" %(lines[2], lines[3]) )

#Join sequences
def flash():
    os.system("make software/FLASH-1.2.11/flash")
    os.system("software/FLASH-1.2.11/flash .temp/cut_out_nolink_R1.fastq .temp/cut_out_nolink_R2.fastq -M 220 -o .temp/flash_out 2>&1 |"
             " tee flash.log")

def grep():
    os.system("grep -B1 '^GATC\(\w*\)GATC$' .temp/flash_out.extendedFrags.fastq | sed 's/^@/>/' | perl -pe 's/--\n//g' > grep_out.fasta")

#Change id's
def ids():
    os.system("perl software/scripts/changeids.pl grep_out.fasta")

#Search Microssatelites
def misa():
    os.system("perl misa.pl ids_out.fasta")


#Length Calculation
def length_calc():
    os.system("perl ../micros_joint/extraelength.pl good_frags_idchanged.fasta")


trimmomatic()
cutadapt()
flash()
ids()


#cutadapt()       A FUNCIONAR
#flash()          A FUNCIONAR
#ids()            Script não aceita o path na pasta .temp/
#misa()            Mensagem de erro