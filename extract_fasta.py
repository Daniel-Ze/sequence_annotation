#Python script to extract fasta sequences from multi-fasta files
#How-to use:
#   python /path/to/script/extract_fasta.py /path/to/sequence/list/sequence_list.txt
#   /path/to/fasta/file/fasta_file.fa
#correspondance: d.zendler@gmx.de
#Tested on python version 2.7.15_1, MacOS High Sierra 10.13.6

from __future__ import print_function
import sys, os, datetime
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
            exit("Somthing went wrong with parsing your input file. Exiting. 1")
        if len(self.file_lines1) == 0:
            exit("Nothing to read here. Exiting")

        if self.file_input_name2 is not "" or self.file_input_stdin2 is not None:
            self.read_content_of_file()
        else:
            exit("Somthing went wrong with parsing your input file. Exiting. 2")
        if len(self.file_lines2) == 0:
            exit("Nothing to read here. Exiting")


    def parse_stdin(self):
        if len(sys.argv) == 3 and sys.argv[1] is not None:
            self.file_input_name1 = sys.argv[1]
            self.file_input_name2 = sys.argv[2]
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
def main():
    #Call the current date and time
    now = datetime.datetime.now()
    #------------------------------------------------------------
    #Call the input files
    file = File()
    #------------------------------------------------------------
    seq = ""
    a = 0
    #Generating the outputfile
    out = open(file.working_path + '/out.fa', 'w')
    out.write(";" + str(now) + "\n")
    #------------------------------------------------------------
    #go through the sequencenames to be extracted
    for lines in file.file_lines1:
        #if the line contains something write '>' in front of it
        if lines != "":
            lines = ">" + lines
            #search the index of the matching sequence name in the fasta file
            a = file.file_lines2.index(lines)
            #write the sequence name in seq
            seq = seq + file.file_lines2[a] + "\n"
            #count the index one further to write the Nt or AA sequence in seq
            a = a + 1
            while a < len(file.file_lines2):
                #as long as there is no new '>' the sequence belongs to the
                #sequence name match
                if '>' not in file.file_lines2[a]:
                    seq = seq + file.file_lines2[a] + "\n"
                    a = a + 1
                else:
                    #as soon as a new '>' comes a new sequence starts and the
                    #for loop needs to continue with the next sequence name
                    break
        else:
            break
    #------------------------------------------------------------
    #write the whole sequences in terminal and in file
    print(seq)
    out.write(seq)
    out.close()

    #------------------------------------------------------------
if __name__ == "__main__":
    main()
