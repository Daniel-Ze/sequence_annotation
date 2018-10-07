# Sequence annotation
Tools for sequence annotation such as fgenesh (softberry), conserved domain search (NCBI)

Output of the aformentioned online tools will not allow direct annotation of sequence files. Therefore I'm trying to 
generate a set of python scripts that allow the generation of GFF3 annotation files from the output to facilitate
de novo sequence annotations.

## FGENESH:
Find the online tool at:

http://www.softberry.com/berry.phtml?topic=fgenesh&group=programs&subgroup=gfind

Reference: Solovyev V, Kosarev P, Seledsov I, Vorobyev D. Automatic annotation of eukaryotic genes, pseudogenes and promoters. Genome Biol. 2006,7, Suppl 1: P. 10.1-10.12. 

The output gives you start and stop of transcripts (TSS, PolA) plus a possible coding sequence (CDS).
FGENESH_to_gff3.py takes the FGENESH output and transforms it to GFF3.

### Working with FGENESH_to_gff3.py:
So far the FGENESH output needs to be tabstop delimited. I achieved this by using Excel:

- Copy output and paste in excel
- Use text to columns
- Save as tab delimited .txt file

Example input:
```
1	-		PolA	5175			1.66				
1	-	1	CDSl	5343	-	5714	20.13	5343	-	5714	372
1	-	2	CDSi	6033	-	6902	63.41	6033	-	6902	870
1	-	3	CDSi	7077	-	7496	32.54	7077	-	7496	420
1	-	4	CDSi	7545	-	7985	7.65	7545	-	7985	441
1	-	5	CDSi	8025	-	8137	4.58	8025	-	8135	111
1	-	6	CDSi	8342	-	8518	4.47	8343	-	8516	174
1	-	7	CDSi	8672	-	8910	4.59	8673	-	8909	237
1	-	8	CDSi	9193	-	9332	3.68	9195	-	9332	138
1	-	9	CDSi	9372	-	9794	23.35	9372	-	9794	423
1	-	10	CDSi	9894	-	9958	2.42	9894	-	9956	63
1	-	11	CDSf	10254	-	10383	5.93	10255	-	10383	129
1	-		TSS	10807			-9.04				
```

This needs to be changed in the future.
  
  The python script can be called as follows:
	
    >python /path/of/the/script/FGENESH_to_gff3.py /path/to/the/tab/delimited/FGENESH/output.txt name_of_sequence_to_be_annotated name_of_generated_gff3_file

  The script will output a log_file.txt and a name_of_generated_gff3_file.gff3 file in the working path.

## Conserved Domain Search:
Find the online tool at:

https://www.ncbi.nlm.nih.gov/Structure/cdd/wrpsb.cgi

References:
Marchler-Bauer A et al. (2017), "CDD/SPARCLE: functional classification of proteins via subfamily domain architectures.", Nucleic Acids Res.45(D)200-3.
Marchler-Bauer A et al. (2015), "CDD: NCBI's conserved domain database.", Nucleic Acids Res.43(D)222-6.
Marchler-Bauer A et al. (2011), "CDD: a Conserved Domain Database for the functional annotation of proteins.", Nucleic Acids Res.39(D)225-9.
Marchler-Bauer A, Bryant SH (2004), "CD-Search: protein domain annotations on the fly.", Nucleic Acids Res.32(W)327-331.

The output gives you start and stop position of conserved and well known domain structures.
ConservedDomainSearch_to_gff3.py takes the output and transforms it to a gff3 file.
Optional ConservedDomainSearch_to_gff3.py can offset the annotation position as the input for the Conserved Domain Search is limited to 200000 bases.

### Working with ConservedDomainSearch_to_gff3.py
So far the ConservedDomainSearch output needs to be tabstop delimited. I achieved this by using Excel:

- Copy output and paste in excel
- Save as tab delimited .txt file

Example input:
```
NB-ARC	pfam00931	NB-ARC domain;	1063-1902	5.72E-66
RX-CC_like	cd14798	Coiled-coil domain of the potato virux X resistance protein and similar proteins; The potato ...	550-936	1.28E-29
PLN03210	PLN03210	Resistant to P. syringae 6; Provisional	997-1692	8.82E-08
PLN00113	PLN00113	leucine-rich repeat receptor-like protein kinase; Provisional	2116-2991	1.61E-03
```
This needs to be changed in the future.

The python script can be called as follows:

	>python /path/of/the/script/ConservedDomainSearch_to_gff3.py /path/to/the/tab/delimited/FGENESH/output.txt name_of_sequence_to_be_annotated name_of_generated_gff3_file 0

The '0' can be changed to any wanted offset value for easy merging of multiple outputs.

The script will output a log_file.txt and a name_of_generated_gff3_file.gff3 file in the working path.

# Sequence manipulation
## Extract fasta sequences from multi fasta file
Tool for extraction of fasta sequences via a sequence list file from a multi fasta file.

### Working with extract_fasta.py
Files needed:
- File with sequence names with one name per line
- Fasta file with multiple sequences

Example input sequence names as .txt file:
```
Test1
Test
```
Example input fasta file as .fa:
```
>Test
AGACGAGAAGGGCGACGAGAGCGAGCGAGAGCGAGC
>Test1
AGAGGCGAGCGAGGCGTCGATCGATACGTAGCTAGT
```

The python script can be called as follows:
	>python /path/to/the/script/extract_fasta.py /path/to/the/sequence/neme/file/SeqIDs.txt /path/to/the/multi/fasta/file/Sequences.fa

The script will output a .fa file in the working directory with the fasta file and it will output the sequences in the terminal.


