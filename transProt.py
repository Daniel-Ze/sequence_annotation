#Python script to extract fasta sequences from multi-fasta files
#How-to use:
#   python /path/to/script/extract_fasta.py /path/to/sequence/list/sequence_list.txt
#   /path/to/fasta/file/fasta_file.fa
#correspondance: d.zendler@gmx.de
#Tested on python version 2.7.15_1, MacOS High Sierra 10.13.6

from __future__ import print_function
import sys, os, datetime, time
import cProfile
#------------------------------------------------------------------------------
#Taken from: https://www.agnosticdev.com/content/how-open-file-python
#Matt Eaton on Sun, 12/17/2017 - 10:35 PM
class File():
    def __init__(self):
        #Initializing the variables for the file
        self.file_lines1 = []
        self.file_input_1 = ""
        self.complete_content1 = ""
        self.file_input_stdin1 = None
        self.working_path = ""
        self.sequence_name = ""

        #Check if there is a filename indicated
        self.parse_stdin()
        if self.file_input_name1 is not "" or self.file_input_stdin1 is not None:
            self.read_content_of_file()
        else:
            exit("Somthing went wrong with parsing your input file. Exiting. SeqIDs")
        if len(self.file_lines1) == 0:
            exit("Nothing to read here. Exiting")

    def parse_stdin(self):
        if len(sys.argv) == 2 and sys.argv[1] is not None:
            self.file_input_name1 = sys.argv[1]
            self.working_path = os.getcwd()
        elif not sys.stdin.isatty():
            self.file_input_stdin1 = sys.stdin
        else:
            print("There was an issue locating your input.")
            exit("Please provide a valid filename/file as input")

    def read_content_of_file(self):
        try:
            if self.file_input_stdin1 is None:
                    with open(self.file_input_name1, 'r') as file_obj:
                        self.complete_content1 = file_obj.read()
            else:
                self.complete_content1 = self.file_input_stdin1.read()
            self.file_lines1 = self.complete_content1.split("\n")

        except ValueError:
            error_raised = "Error loading file: " + str(sys.exc_info()[0])
            print("This program needs an input file to continue. Exiting")

#Taken from: https://www.agnosticdev.com/content/how-open-file-python
#Matt Eaton on Sun, 12/17/2017 - 10:35 PM
#------------------------------------------------------------------------------

def convFasta(multiFastaFile):#Write the sequence of a multifasta file in one line per seq

    new_file = ''
    sequence = ''
    a = 0
    count_l = len(multiFastaFile)

    for lines in multiFastaFile:
        if lines != "" and lines[:1] == '>':
            seqName = lines.split('.')
            print(seqName)
            seqName = '.'.join(seqName[0:3]) + '.prot'
            new_file = new_file + seqName
            a = a + 1

            while a < count_l and '>' not in multiFastaFile[a]:
                sequence = sequence + multiFastaFile[a].rstrip()
                a = a + 1

            sequence = transProt(sequence)
            new_file = new_file + ' ' + str(len(sequence)) + ' aa\n' + sequence + "\n"
            sequence = ''

    return new_file

def transProt(CDS):

    lenCDS = len(CDS)
    a = 0
    b = 3
    protein = ''
    lenCDScheck = (float(lenCDS)/3).is_integer()

    if lenCDScheck == False:
        return 'Probelm converting this sequence. Not divisable by 3.'

    prot = {'TTT' : 'F', 'TTC' : 'F', 'TTA' : 'L', 'TTG' : 'L', 'CTT' : 'L', 'CTC' : 'L', 'CTA' : 'L', 'CTG' : 'L', 'ATT' : 'I', 'ATC' : 'I', 'ATA' : 'I', 'ATG' : 'M', 'GTT' : 'V', 'GTC' : 'V', 'GTA' : 'V', 'GTG' : 'V', 'TCT' : 'S', 'TCC' : 'S', 'TCA' : 'S', 'TCG' : 'S', 'CCT' : 'P', 'CCC' : 'P', 'CCA' : 'P', 'CCG' : 'P', 'ACT' : 'T', 'ACC' : 'T', 'ACA' : 'T', 'ACG' : 'T', 'GCT' : 'A', 'GCC' : 'A', 'GCA' : 'A', 'GCG' : 'A', 'TAT' : 'Y', 'TAC' : 'Y', 'CAT' : 'H', 'CAC' : 'H', 'CAA' : 'Q', 'CAG' : 'Q', 'AAT' : 'N', 'AAC' : 'N', 'AAA' : 'K', 'AAG' : 'K', 'GAT' : 'D', 'GAC' : 'D', 'GAA' : 'E', 'GAG' : 'E', 'TGT' : 'C', 'TGC' : 'C', 'CGT' : 'R', 'CGC' : 'R', 'CGA' : 'R', 'CGG' : 'R', 'AGT' : 'S', 'AGC' : 'S', 'AGA' : 'R', 'AGG' : 'R', 'GGT' : 'G', 'GGC' : 'G', 'GGA' : 'G', 'GGG' : 'G', 'TAA' : '*', 'TAG' : '*', 'TGA' : '*', 'TGG' : 'W'}

    while b <= lenCDS:
        protein = protein + prot[CDS[a:b]]
        a = a + 3
        b = b + 3

    return protein

def main():
    file = File()
    cwd = file.working_path
    out = open(cwd + '/' + file.file_input_name1 + '.prot.fa', 'w')
    new_file_1 = convFasta(file.file_lines1)
    print(new_file_1)
    out.write(new_file_1)
    out.close()

#------------------------------------------------------------
if __name__ == "__main__":
    main()
