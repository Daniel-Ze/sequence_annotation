#Python script to adjust the FGENESH output to the standard gff3 file format
#Output needs to be stored as tabstop delimited data
#How-to use:
#   python /path/to/script/FGENESH_to_gff3.py /path/to/FGENESH/output/output.txt
#   name_of_sequence name_of_gff3_file_to_be_generated
#Tested on python version 2.7.15_1, MacOS High Sierra 10.13.6, Excel 2016 for
#MacOS

from __future__ import print_function
import numpy as np
import sys, os, datetime
#------------------------------------------------------------------------------
#Taken from: https://www.agnosticdev.com/content/how-open-file-python
#Matt Eaton on Sun, 12/17/2017 - 10:35 PM
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

        #Check if there is a filename indicated
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

#Taken from: https://www.agnosticdev.com/content/how-open-file-python
#Matt Eaton on Sun, 12/17/2017 - 10:35 PM
#------------------------------------------------------------------------------
def main():
    #Call the current date and time
    now = datetime.datetime.now()
    #------------------------------------------------------------
    #Call the FGENESH output file
    file = File()
    #------------------------------------------------------------
    #Generating log and output file
    log = open(file.working_path + '/logfile_log.txt', 'w')
    gff3 = open(file.working_path + '/' + file.gff3_name + '.gff3', 'w')
    #------------------------------------------------------------
    #Give the file the GFF3 header
    gff3.write("##gff-version 3")
    #------------------------------------------------------------
    #Log the process
    log.write("Program started at: " + str(now) + "\n"+
              "Annotation file: " + file.working_path +
              "/annotation.gff3 created\n")
    #------------------------------------------------------------
    #generate an empty np.array and other variables used later on
    np_gene_array = np.empty((0,9))
    a='0000'
    gff=''
    gff_cds=''
    gff_gene=''
    #-------------------------------------------------------------------------
    #Going through the FGENESH output file (tabstop delimited) line by line
    #if the lines are not empty adjust the contents of the line to gff3
    for lines in file.file_lines:
        if lines != "":
            print("Line for file: " + lines)

            #Split the tabstop delimited txt file in fields for rearrangement
            lines = lines.rstrip()			#remove the linebreaks at the end
            fields = lines.split("\t")		#split the lines into fields
            fields_ap = fields[0:8]			#only keep the first 8 fields

            #saving the gff3 infos in variables
            num = fields_ap[0]              #gene number
            identi = fields_ap[3]           #gene or cds

            #adjusting the cds numbering to a 5 digit code
            if len(num) == 1:               #checking if the number is below 10
                num = a + num               #creating 5 digit code
            elif len(num) == 2:             #checking if number is below 100
                num = a[0:2] + num          #creating 5 digit code
            elif len(num) == 3:             #checking if number is below 1000
                num = a[0:1] + num          #creating 5 digit code

            strand  = fields_ap[1]          #strand location info
            start   = fields_ap[4]          #start of gene/cds
            stop    = fields_ap[6]          #end of gene/cds
            score   = fields_ap[7]          #probability score

            #write the variables in the gff3 format
            if identi == 'PolA':            #In case of PolA as identifyer
                gff_format = (file.sequence_name+"\t"+"fgenesh"+"\t"+
                            identi+"\t"+start+"\t"+stop+"\t.\t"+strand+
                            "\t.\t"+"ID=gene"+num+";score="+score)

                gff = gff + "\n" + gff_format
                gff_format = gff_format.rstrip()
                gff_format = gff_format.split("\t")
                np_gene_array = np.append(np_gene_array, [gff_format], axis=0)

            elif identi == 'TSS':           #In case of TSS as identifyer
                gff_format = (file.sequence_name+"\t"+"fgenesh"+"\t"+
                            identi+"\t"+start+"\t"+stop+"\t.\t"+strand+
                            "\t.\t"+"ID=gene"+num+";score="+score)

                gff = gff + "\n" + gff_format
                gff_format = gff_format.rstrip()
                gff_format = gff_format.split("\t")
                np_gene_array = np.append(np_gene_array, [gff_format], axis=0)

            else:                           #In case of CDS as identifyer
                gff_format = (file.sequence_name+"\t"+"fgenesh"+"\t"+
                            "cds"+"\t"+start+"\t"+stop+"\t.\t"+strand+
                            "\t.\t"+"ID=cds"+num+";parent=gene"+num+
                            ";score="+score)

                gff_cds = gff_cds + "\n" + gff_format
    #-------------------------------------------------------------------------
    #Getting the length of the array
    x = np_gene_array.shape                 #determining the array length
    y = x[0]
    #-------------------------------------------------------------------------
    #copying the start/end position in one row
    a = 1
    i = 1
    while i <= y/2:
        v = np_gene_array[a,3]
        a = a - 1
        np_gene_array[a,4] = v
        np_gene_array[a,2] = 'gene'
        a = a + 3
        i = i + 1
    #------------------------------------------------------------
    #deleting additional rows from the array
    a = 1
    i = 1
    while i <= y/2:
        np_gene_array = np.delete(np_gene_array, a, 0)
        a = a + 1
        i = i + 1
    #------------------------------------------------------------
    #Adjust the array content to gff3
    i = 1
    a = 0
    while i <= y/2:
        gff_gene = gff_gene + "\n" + (np_gene_array[a,0] + "\t" +
                               np_gene_array[a,1] + "\t" +
                               np_gene_array[a,2] + "\t" +
                               np_gene_array[a,3] + "\t" +
                               np_gene_array[a,4] + "\t" +
                               np_gene_array[a,5] + "\t" +
                               np_gene_array[a,6] + "\t" +
                               np_gene_array[a,7] + "\t" +
                               np_gene_array[a,8])
        a = a + 1
        i = i + 1
    #------------------------------------------------------------
    #Results output to terminal and write to annotation.gff3 file
    print(gff_gene)
    print(gff_cds)
    gff3.write(gff_gene)
    gff3.write(gff_cds)
    log.write("GFF3 annotation was succesfully written to: " +
              file.working_path + "/"+file.gff3_name+".gff3\n")
    log.write("Success!")
    gff3.close()
    log.close()
    #------------------------------------------------------------
if __name__ == "__main__":
    main()
