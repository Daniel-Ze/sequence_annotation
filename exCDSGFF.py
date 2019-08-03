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
                print("|Translate coding sequences into protein sequences. Only true CDSs are translated!        |\n|")
                print("|To use this script type: python /path/to/transProt.py /path/to/CDS.gff3 /path/to/Fasta.fa|\n|")
                print("|If still in desperate need for help see: https://github.com/zendl0r/sequence_annotation  |")
                print(" ----------------------------------------------------------------------------------------- ")
                exit()
            self.file_input_name2 = sys.argv[2]
            self.working_path = os.path.dirname(os.path.realpath(sys.argv[1]))
        elif not sys.stdin.isatty():
            self.file_input_stdin1 = sys.stdin
        else:
            print(" _________________________________________________________________________________________")
            print("|Translate coding sequences into protein sequences. Only true CDSs are translated!        |\n|")
            print("|To use this script type: python /path/to/transProt.py /path/to/CDS.gff3 /path/to/Fasta.fa|\n|")
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
            self.file_lines2 = self.complete_content2.split()

        except ValueError:
            error_raised = "Error loading file: " + str(sys.exc_info()[0])
            print("This program needs an input file to continue. Exiting")

#Taken from: https://www.agnosticdev.com/content/how-open-file-python
#Matt Eaton on Sun, 12/17/2017 - 10:35 PM
#------------------------------------------------------------------------------

def convFasta(multiFastaFile):
    """Write the sequence of a multifasta file in one line per seq"""
    new_file = ''
    a = 0
    count_l = len(multiFastaFile)
    for lines in multiFastaFile:
        if lines != "" and lines[:1] == '>':
            new_file = new_file + lines + "\n"      #write the sequence name
            a = a + 1
            while a < count_l and '>' not in multiFastaFile[a]:
                new_file = new_file + multiFastaFile[a].rstrip()
                a = a + 1
            new_file = new_file + "\n"
    new_file = new_file.split()
    return new_file

def revComp(x):
    """Reverse complement sequence"""
    nuc = {'A': 'T', 'C' : 'G', 'T' : 'A', 'G' : 'C'}
    seq = ''
    seq_rev = ''
    for _ in x:
        seq_rev += nuc[_]
    x = seq_rev[::-1]
    return x

def findGCgene(x):
    """Calculate the GC content of a sequence"""
    gc = 0
    i = 0
    totals = len(x)
    for i in x:
        if i == 'C' or i == 'G':
            gc += 1
    if gc > 0:
        gc = float(gc)/float(totals)
        gc = round(gc, 2)
    return gc

def main():
    file = File()
    seqIndex = 0
    c = 0
    strand = ''
    seq = ''
    geneID = ''
    gc = ''
    new_file_CDS = ''
    id_1 = ''
    id_2 = ''
    cwd = file.working_path
    file_name = file.file_input_name1.split('/')
    file_name = ''.join(file_name[-1:])
    out = open(cwd + '/' + file_name + '.fa', 'w')

    new_file_1 = convFasta(file.file_lines2)
    for lines in file.file_lines1:
        if lines != "" and lines[:2] != "##":

            lines = lines.rstrip()
            print(lines)
            fields = lines.split("\t")

            sequence_name = ">" + fields[0]
            seqIndex = new_file_1.index(sequence_name) + 1
            feature = fields[2]
            start = fields[3]
            stop = fields[4]
            strand = fields[6]
            id_1 = fields[8].split(";")
            id_1 = id_1[0].split("=")
            id_1 = id_1[1].split(".")
            id_2 = id_1[0]

            if geneID != id_2 and geneID == '':
                seq1 = new_file_1[seqIndex]
                seq1 = seq1[int(start)-1:int(stop)]
                if strand == '-':
                    seq1 = revComp(seq1)
                    seq = seq1 + seq
                    c = c + 1
                else:
                    seq = seq + seq1
                    c = c + 1

            if geneID == id_2:
                seq1 = new_file_1[seqIndex]
                seq1 = seq1[int(start)-1:int(stop)]
                if strand == '-':
                    seq1 = revComp(seq1)
                    seq = seq1 + seq
                    c = c + 1
                else:
                    seq = seq + seq1
                    c = c + 1

            if geneID != id_2 and geneID != '':
                print("Enter if 3")
                length = len(seq)

                gc = findGCgene(seq)
                new_file_CDS = new_file_CDS+"\n" + ">" + geneID + "_" + \
                                str(length) + "_nt_" + "Seq:_" + old_seqName + "_strand:_" + \
                                old_strand + "_" + \
                                feature + "_GC_" + str(gc) + "_Exon_" + \
                                str(c)
                new_file_CDS = new_file_CDS + "\n" + seq
                seq = ''
                seq1 = new_file_1[seqIndex]
                seq1 = seq1[int(start)-1:int(stop)]
                if strand == '-':
                    seq = revComp(seq1)
                else:
                    seq = seq1
                c = 1
            old_seqName = str(fields[0])
            old_strand = strand
            geneID = id_2
#------------------------------------------------------------
    length = len(seq)
    gc = findGCgene(seq)
    new_file_CDS = new_file_CDS+"\n" + ">" + geneID + " " + str(length) + "_nt_" + "Seq:_" + str(fields[0]) + "_strand:_" + strand + "_" + \
                    feature + "_GC_" + str(gc) + "_Exon_" + str(c)
    new_file_CDS = new_file_CDS + "\n" + seq
    print(new_file_CDS)
    out.write(new_file_CDS)
    out.close()
#------------------------------------------------------------
if __name__ == "__main__":
    main()
    #cProfile.run('main()', sort='time')   #uncomment this for infos on the run
