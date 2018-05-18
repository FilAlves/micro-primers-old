import os

#Creation of hidden temp file
if os.path.isdir(".temp/") == False:
    os.system("mkdir .temp")

if os.path.isdir("logs/") == False:
    os.system("mkdir logs")

#Input file with Sequences to be processed and cutadapt input sequences
file = open("input_text.txt", "r")
lines = file.read().splitlines()

#Sequences Triming of Sequencer adapters
def trimmomatic():
    os.system("echo 'Trimmomatic working...'")
    os.system(
        "java -jar software/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 "
        "%s %s "
        ".temp/trim_out_trimmed_R1.fastq .temp/trim_out_unpaired_R1.fastq "
        ".temp/trim_out_trimmed_R2.fastq .temp/trim_out_unpaired_R2.fastq "
        "ILLUMINACLIP:/home/filalves/projecto/software/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 "
        "LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 2> logs/trim_log.txt"
        %(lines[0], lines[1])
        )

#Adapters removal (specifics from technology)
def cutadapt():
    os.system("echo 'Cutadapt working...'")
    os.system("cutadapt -a %s -g %s -o .temp/cut_out_nolink_R1.fastq .temp/trim_out_trimmed_R1.fastq > logs/cut_log_r1.txt" %(lines[2], lines[3]) )
    os.system("cutadapt -a %s -g %s -o .temp/cut_out_nolink_R2.fastq .temp/trim_out_trimmed_R2.fastq > logs/cut_log_r2.txt" %(lines[2], lines[3]) )

# Fusion of R1 and R2 files
def flash():
    os.system("echo 'Flash working...'")
    os.system("software/FLASH-1.2.11/flash .temp/cut_out_nolink_R1.fastq .temp/cut_out_nolink_R2.fastq -M 220 -o .temp/flash_out 2>&1 |"
             " tee logs/flash.log > logs/flash_log.txt")

# Selecion of fragments that start and ends with the pattern of the restriction enzyme
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
    os.system("perl software/scripts/misa.pl .temp/ids_out.fasta 2> logs/misa_log.txt")

#Length Calculation for later selection of valid microsatellites
def length_calc():
    os.system("echo 'Calculating sequences lengths...'")
    os.system("perl software/scripts/extraelength.pl .temp/ids_out.fasta")

#Extraction of the microsatellite sequence from allignement of fragments with flanking regions
def splitSSR():
    os.system("echo 'splitSSR working...'")
    os.system("perl software/scripts/splitSSR.pl .temp/ids_out.fasta replacement/micros_good.txt")

#Removal of Redundacy
def cdhit():
    os.system("echo 'CD-HIT working...'")
    os.system("software/cdhit/cd-hit-est -o .temp/cdhit_out.txt -i replacement/replacement.txtnoSSR.fasta -c 0.90 -n 10 -T 10 > logs/cdhit_log.txt")

#Cluster assignement
def cluster():
    os.system("echo 'Calculating number of sequences for each cluster...'")
    os.system("perl software/scripts/asign_cluster.pl .temp/cdhit_out.txt.clstr")

#Adding cluster information to Microssatelites table
def cluster_info():
    os.system("echo 'Adding information to the table of microsatellites...'")
    os.system("perl software/scripts/attach_cluster_info.pl .temp/misa_out.misa clusters_out.txt") #.temp/clusters_out.txt")

#Creating input file for Primer3
def create_pseudofasta():
    os.system("echo 'Creating Primer3 input file...'")
    os.system("perl software/scripts/extraeseqs.pl replacement/bugios_good_idchanged.fasta replacement/micros_selected.txt")

#Primer design and creation
def primer3():
    os.system("echo 'Creating Primers...'")
    os.system("software/primer3/src/./primer3_core -default_version=2 -p3_settings_file=software/primer3/CTM_settings_long.txt "
              ".temp/pseudo_out.fasta -output=.temp/micros_selected_long.primers")

#Selection of primers following laboratory criteria
def select():
    os.system("echo 'Selecting best primers...'")
    os.system("perl software/scripts/select_oligos.pl .temp/micros_selected_long.primers replacement/tab_selected.txt > logs/select_log.txt")

#Removal of .temp directory
def junk():
    os.system("rm -r .temp/")

#Pipeline
trimmomatic()
cutadapt()
flash()
grep()
ids()
misa()
length_calc()
splitSSR()
cdhit()
cluster()
cluster_info()
create_pseudofasta()
primer3()
select()
junk()

os.system("echo 'Done!'")


#É preciso fazer make do CD-HIT, Primer3 e flash

#Replacement Files:
#bugios_good_idchanged.fasta
#micros_good.txt
#micros_selected.txt
#replacement.txtnoSSR.fasta
#tab_selected.txt
