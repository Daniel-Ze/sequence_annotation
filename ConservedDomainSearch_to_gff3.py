#Python script to adjust the Conserved Domain Search output to the standard
#gff3 file format.
#Output needs to be stored as tabstop delimited data.
#How-to use:
#   python /path/to/script/ConservedDomainSearch_to_gff3.py
#   /path/to/FGENESH/output/output.txt name_of_sequence 
#   name_of_gff3_file_to_be_generated
#Tested on python version 2.7.15_1, MacOS High Sierra 10.13.6, Excel 2016 for
#MacOS

from __future__ import print_function
import sys, os, datetime

#Taken from: https://www.agnosticdev.com/content/how-open-file-python
#Matt Eaton on Sun, 12/17/2017 - 10:35 PM
#------------------------------------------------------------------------------
class File():

    def __init__(self):
        #Initializing the variables for the file
        self.file_lines = []
        self.file_input_name = ""
        self.complete_content = ""
        self.file_input_stdin = None
        self.working_path = ""
        self.sequence_name = ""
        self.gff3_name = ""

        #Check if there is filename indicated
        self.parse_stdin()
        if self.file_input_name is not "" or self.file_input_stdin is not None:
            self.read_content_of_file()
        else:
            exit("Somthing went wrong with parsing your input file. Exiting")
        if len(self.file_lines) == 0:
            exit("Nothing to read here. Exiting")


    def parse_stdin(self):
        if len(sys.argv) > 2 and sys.argv[1] is not None:
            self.file_input_name = sys.argv[1]
            self.working_path = os.path.dirname(sys.argv[1])
            self.sequence_name = sys.argv[2]
            self.gff3_name = sys.argv[3]
        elif not sys.stdin.isatty():
            self.file_input_stdin = sys.stdin
        else:
            print("There was an issue locating your input")
            exit("Please provide a valid filename/file as input")

    def read_content_of_file(self):
        try:
            if self.file_input_stdin is None:
                    with open(self.file_input_name, 'r') as file_obj:
                        self.complete_content = file_obj.read()
            else:
                self.complete_content = self.file_input_stdin.read()
            self.file_lines = self.complete_content.split("\n")

        except ValueError:
            error_raised = "Error loading file: " + str(sys.exc_info()[0])
            print("This program needs an input file to continue. Exiting")
#----------------------------------------------------------------------------

def main():
    now = datetime.datetime.now()
    file = File()

    #Generating log and output file
    log = open(file.working_path + '/logfile_log.txt', 'w')
    gff3 = open(file.working_path + '/' + file.gff3_name + '.gff3', 'w')

    #Give the file the GFF3 header
    gff3.write("##gff-version 3")
    gff_format = ''

    log.write("Program started at: " + str(now) + "\n"
              "Logfile and annotation file " + file.gff3_name +
              ".gff3 are generated")


    for lines in file.file_lines:
        if lines != "":                         #check if somethings written
            #Split the tabstop delimited txt file in fields for rearrangement
            lines = lines.rstrip()              #remove linebreaks
            fields = lines.split("\t")          #split at tabstop

            #assign fields to variables
            name = fields[0]
            acession = fields[1]
            description = fields[2]
            interval = fields[3]
            e_value = fields [4]

            #start/stop needs to be split seperatly due to "-"
            start_stop = interval.split("-")
            start = start_stop[0]
            stop = start_stop[1]

            #replace ';' with '' due to confusion of gff3
            description = description.replace(';', '')

            #Write to gff3 output file
            gff_format = gff_format + "\n" + (file.sequence_name+"\t"+name+"\t"+
                                            "Domain"+"\t"+start+"\t"+stop+
                                            "\t.\t"+"?"+"\t.\t"+"ID="+name+
                                            ";e-value="+e_value+";acession="
                                            +acession+";description="+
                                            description)

    print(gff_format)
    gff3.write(gff_format)
    log.write("Success!")

if __name__ == "__main__":
    main()
