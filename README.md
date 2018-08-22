# sequence_annotation
Tools for sequence annotation such as fgenesh (softberry), conserved domain search (NCBI), LTR-harvest (genome-tools).

Output of the aformentioned online tools will not allow direct annotation of sequence files. Therefore I'm trying to 
generate a set of python scripts that allow the generation of GFF3 annotation files from the output to facilitate
de novo sequence annotations.

FGENESH:
Find the online tool at:
http://www.softberry.com/berry.phtml?topic=fgenesh&group=programs&subgroup=gfind
Reference: Solovyev V, Kosarev P, Seledsov I, Vorobyev D. Automatic annotation of eukaryotic genes, pseudogenes and promoters. Genome Biol. 2006,7, Suppl 1: P. 10.1-10.12. 

The output gives you start and stop of transcripts (TSS, PolA) plus a possible coding sequence (CDS).
FGENESH_to_gff3.py takes the FGENESH output and transforms it to GFF3.

Working with FGENESH_to_gff3.py:
  So far the FGENESH output needs to be tabstop delimited. I achieved this by using Excel:
    - Copy output and paste in excel
    - Use text to columns
    - Save as tab delimited .txt file
  This needs to be changed in the future.
  
  The python script can be called as follows:
    python /path/of/the/script/FGENESH_to_gff3.py /path/to/the/tab/delimited/FGENESH/output.txt name_of_sequence_to_be_annotated 
    name_of_generated_gff3_file

  The script will output a log_file.txt and a name_of_generated_gff3_file.gff3 file in the working path.
