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
        self.file_lines2 = []
        self.file_input_1 = ""
        self.file_input_2 = ""
        self.complete_content1 = ""
        self.complete_content2 = ""
        self.file_input_stdin1 = None
        self.file_input_stdin2 = None
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

        if self.file_input_name2 is not "" or self.file_input_stdin2 is not None:
            self.read_content_of_file()
        else:
            exit("Somthing went wrong with parsing your input file. Exiting. Fasta")
        if len(self.file_lines2) == 0:
            exit("Nothing to read here. Exiting")

    def parse_stdin(self):
        if len(sys.argv) == 3 and sys.argv[1] is not None:
            self.file_input_name1 = sys.argv[1]
            if self.file_input_name1 == "h" or self.file_input_name1 == "-h" or self.file_input_name1 == "-help" or self.file_input_name1 == "help":
                print(" _________________________________________________________________________________________")
                print("|Extract gene sequences from multi fasta file with a .gff3 annotation file.               |\n|")
                print("|Type: python /path/to/transProt.py /path/to/gene.gff3 /path/to/Fasta.fa                  |\n|")
                print("|If still in desperate need for help see: https://github.com/zendl0r/sequence_annotation  |")
                print(" ----------------------------------------------------------------------------------------- ")
                exit()
            self.file_input_name2 = sys.argv[2]
            self.working_path = os.getcwd()
        elif not sys.stdin.isatty():
            self.file_input_stdin1 = sys.stdin
        else:
            print(" _________________________________________________________________________________________")
            print("|Extract gene sequences from multi fasta file with a .gff3 annotation file.               |\n|")
            print("|Type: python /path/to/transProt.py /path/to/gene.gff3/path/to/Fasta.fa                   |\n|")
            print("|If still in desperate need for help see: https://github.com/zendl0r/sequence_annotation  |")
            print(" ----------------------------------------------------------------------------------------- ")
            exit()

    def read_content_of_file(self):
        try:
            if self.file_input_stdin1 is None:
                    with open(self.file_input_name1, 'r') as file_obj:
                        self.complete_content1 = file_obj.read()
            else:
                self.complete_content1 = self.file_input_stdin1.read()
            self.file_lines1 = self.complete_content1.split("\n")

            if self.file_input_stdin2 is None:
                    with open(self.file_input_name2, 'r') as file_obj:
                        self.complete_content2 = file_obj.read()
            else:
                self.complete_content2 = self.file_input_stdin2.read()
            self.file_lines2 = self.complete_content2.split("\n")

        except ValueError:
            error_raised = "Error loading file: " + str(sys.exc_info()[0])
            print("This program needs an input file to continue. Exiting")

#Taken from: https://www.agnosticdev.com/content/how-open-file-python
#Matt Eaton on Sun, 12/17/2017 - 10:35 PM
#------------------------------------------------------------------------------
def convFasta(x):
    new_file = ''
    a = 0
    count_l = len(x)
    for lines in x:
        if lines != "" and lines[:1] == '>':
            new_file = new_file + lines + "\n"
            a = a + 1
            while a < count_l and '>' not in x[a]:
                new_file = new_file + x[a].rstrip()
                a = a + 1
            new_file = new_file + "\n"

    new_file = new_file.split()
    return new_file

def revComp(x):
    nuc = {'A': 'T', 'C' : 'G', 'T' : 'A', 'G' : 'C'}
    seq = ''
    seq_rev = ''
    for _ in x:
        if _ in nuc:
            seq_rev += nuc[_]
        else:
            print("Bis hier hin und nicht weiter: " + seq_rev)
            print("Das wars: " + _)
            print("Achtung achtung!")
            exit("there was an error in the sequence!")
    x = seq_rev[::-1]
    return x

def findGCgene(x,y):
    gc = 0
    totals = 0
    i = 0
    for i in x:
        if i == 'C' or i == 'G':
            gc += 1
        totals += 1
    if gc > 0:
        gc = float(gc)/float(totals)
        gc = round(gc, 2)
    return gc

def extractGene(seqNameFa,lines):
    lines = lines.rstrip()
    fields = lines.split('\t')
    file = File()
    new_file_1 = convFasta(file.file_lines2)

    seqIndex = new_file_1.index(seqNameFa)
    seqIndex = seqIndex + 1
    seq = new_file_1[seqIndex]
    seq = seq[int(fields[3])-1:int(fields[4])]
    if fields[6] == '-':
        seq = revComp(seq)
    return seq

def seqNameOut(new_file_gene, lines, gc, length):
    lines = lines.rstrip()
    fields = lines.split('\t')
    id_1 = fields[8].split(';')
    id_1 = id_1[0].split('=')
    new_file_gene = new_file_gene + "\n" + ">" + id_1[1] + "_" + str(length) + "_nt_" + fields[3] + \
                    "-" + fields[4] + "_strand:_" + str(fields[6]) + "_" + \
                    str(fields[0]) + "_" + str(fields[2]) + "_GC_" + str(gc)

    return new_file_gene

def geneLength(lines):
    lines = lines.rstrip()
    fields = lines.split('\t')
    length = int(fields[3]) - int(fields[4])
    return length

def seqName(lines):
    lines = lines.rstrip()
    fields = lines.split('\t')
    seqNameFa = '>' + str(fields[0])
    return seqNameFa

def main():
    file = File()
    gc = ''
    new_file_gene = ''
    cwd = file.working_path
    out = open(cwd + '/' + file.file_input_name1 + '.fa', 'w')
    for lines in file.file_lines1:
        if lines != '' and lines[:2] != '##':

            length = geneLength(lines)

            sequence_name_fa = seqName(lines)

            seq = extractGene(sequence_name_fa,lines)

            gc = findGCgene(seq, length)

            new_file_gene = seqNameOut(new_file_gene,lines, gc, length)
            new_file_gene = new_file_gene + "\n" + seq
    print(new_file_gene)
    out.write(new_file_gene)
    out.close()
if __name__ == "__main__":
    main()
    #cProfile.run('main()', sort='time')
