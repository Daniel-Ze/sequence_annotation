#Python script to extract fasta sequences from multi-fasta files
#How-to use:
#   python /path/to/script/extract_fasta.py /path/to/sequence/list/sequence_list.txt
#   /path/to/fasta/file/fasta_file.fa
#correspondance: d.zendler@gmx.de
#Tested on python version 2.7.15_1, MacOS High Sierra 10.13.6

from __future__ import print_function
import sys, os, datetime, time
#------------------------------------------------------------------------------
#Taken from: https://www.agnosticdev.com/content/how-open-file-python
#Matt Eaton on Sun, 12/17/2017 - 10:35 PM
class File():
    def __init__(self):
        #Initializing the variables for the file
        self.file_lines_seqIDs = []
        self.file_lines_multiFasta = []
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
        if self.file_input_seqID is not "" or self.file_input_stdin1 is not None:
            self.read_content_of_file()
        else:
            exit("Somthing went wrong with parsing your input file. Exiting. SeqIDs")
        if len(self.file_lines_seqIDs) == 0:
            exit("Nothing to read here. Exiting")

        if self.file_input_multiFasta is not "" or self.file_input_stdin2 is not None:
            self.read_content_of_file()
        else:
            exit("Somthing went wrong with parsing your input file. Exiting. Fasta")
        if len(self.file_lines_multiFasta) == 0:
            exit("Nothing to read here. Exiting")

    def parse_stdin(self):
        if len(sys.argv) == 3 and sys.argv[1] is not None:
            self.file_input_seqID = sys.argv[1]
            self.file_input_multiFasta = sys.argv[2]
            self.working_path = os.getcwd()
        elif not sys.stdin.isatty():
            self.file_input_stdin1 = sys.stdin
        else:
            print("A problem occured.\n")
            print("Calling the script: python seqIDs_file multiFasta.fa\n")
            print("Contact: d.zendler@gmx.de")
            exit("Please provide a valid list of seqIDS and a valid Fasta file")

    def read_content_of_file(self):
        try:
            if self.file_input_stdin1 is None:
                    with open(self.file_input_seqID, 'r') as file_obj:
                        self.complete_content1 = file_obj.read()
            else:
                self.complete_content1 = self.file_input_stdin1.read()
            self.file_lines_seqIDs = self.complete_content1.split("\n")

            if self.file_input_stdin2 is None:
                    with open(self.file_input_multiFasta, 'r') as file_obj:
                        self.complete_content2 = file_obj.read()
            else:
                self.complete_content2 = self.file_input_stdin2.read()
            self.file_lines_multiFasta = self.complete_content2.split()
        except ValueError:
            error_raised = "Error loading file: " + str(sys.exc_info()[0])
            print("This program needs an input file to continue. Exiting")
#function to find the index of the sequences to be extracted--------------------
def findIndexOfSeq(seqID):
    file = File()
    indexList = []
    for line in seqID:
        if line != "":
            line = ">" + line
            indexList.append(file.file_lines_multiFasta.index(line))
    return indexList
#function to extract the sequences----------------------------------------------
def extractSeqs(indexList):
    file = File()
    seq = ''
    for ind in indexList:
        seq = seq + file.file_lines_multiFasta[ind] + "\n"
        ind = ind + 1
        while ind < len(file.file_lines_multiFasta):
            if '>' not in file.file_lines_multiFasta[ind]:
                seq = seq + file.file_lines_multiFasta[ind] + "\n"
                ind = ind + 1
            else:
                break
    return seq
#get the job done---------------------------------------------------------------
def main():
#Call the current date and time-------------------------------------------------
    now = datetime.datetime.now()
#Call the input files-----------------------------------------------------------
    file = File()
#Generating the outputfile------------------------------------------------------
    out = open(file.file_input_seqID + '.fa', 'w')
#go through the sequencenames to be extracted-----------------------------------
    indexList = findIndexOfSeq(file.file_lines_seqIDs)
#get the sequences from the seqID file------------------------------------------
    seq = extractSeqs(indexList)
#write everything to file-------------------------------------------------------
    out.write(seq)
    out.close()

if __name__ == "__main__":
    main()
