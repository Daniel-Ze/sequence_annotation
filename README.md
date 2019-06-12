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
Tool for extraction of fasta sequences via a sequence list file from a multi fasta file. Comes in handy if you're working
with tools like signalP, targetP, EffectorP, AppoplastP.

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


## Extract gene sequences from a fasta file
Script to extract gene sequences (UTR,Exon,Intron) from a multi fasta file using a .gff3 annotation file.

### Working with exGeneGFF.py
Files needed:
- gff3 file with only gene positions (use grep -E "gene" or "Gene" and redirect to new file.gff3)
- fasta.fa file with single or multiple sequences from which the genes will be extracted

Example input .gff3 file:
```
##gff-version 3
##sequence region	1 90
Test	geneFind	CDS	2	25	.	-	.	ID=Gene0001;name=META1_I-int;sw_score=279;perc.div=8.3
Test1	geneFind	CDS	2	4	.	-	.	ID=Gene0002;name=META1_I-int;sw_score=279;perc.div=8.3
```

Example input .fa file:
```
>Test
ACGATAGAAGGGCGACGAGAGCGAGCGAGAGCGAGCAGAGGCGAGCGAGGCGTCGATCG
ATACGTAGCTAGTAGACGAGAAGGGCGACGAGAGCGAGCGAGAGCGAGCAGAGGCGAGC
GAGGCGTCGATCGATACGTAGCTAGTAGACGAGAAGGGCGACGAGAGCGAGCGAGAGCG
AGCAGAGGCGAGCGAGGCGTCGATCGATACGTAGCTAGTAGACGAGAAGGGCGACGAGA
GCGAGCGAGAGCGAGCAGAGGCGAGCGAGGCGTCGATCGATACGTAGCTAGTAGACGAG
AAGGGCGACGAGAGCGAGCGAGAGCG
>Test1
AGAGGCGAGCGAGGCGTCGATCGATACGTAGCTAGTAGACGAGAAGGGCGACGAGAGCG
AGCGAGAGCGAGCAGAGGCGAGCGAGGCGTCGATCGATACGTAGCTAGTAGAGGCGAGC
GAGGCGTCGATCGATACGTAGCTAGTAGACGAGAAGGGCGACGAGAGCGAGCGAGAGCG
AGC
```

The python script can be called as follows:

	> python /path/to/exGeneGFF.py /path/to/CDS.gff3 /path/to/Fasta.fa
	
The script will output a .fa file in the directory of the .gff3 file with with the gene, gc content of gene, length and strand information. The same will be promted to the terminal



## Extract conding sequences from a fasta file
Script to extract coding sequences from a multi fasta file using a .gff3 annotation file.

### Working with exCDSGFF.py
Files needed:
- gff3 file with only the CDS positions (use grep -E "cds" or "CDS" and redirect to new file.gff3)
- fasta.fa file with single or multiple sequences from which the CDSs will be extracted



The python script can be called as follows:

	> python /path/to/transProt.py /path/to/CDS.gff3 /path/to/Fasta.fa

The script will output a .fa file in the directory of the .gff3 file with the CDS, GC content of CDS, length and strand
infromation. The same will be promted to the terminal.

## Translate CDS to protein
This script is translating a multi fasta file with coding sequences to a multi fasta file with protein sequences.

### Working with transProt.py
Files needed:
- single fasta or multi fasta file

Example input:
```
>cds00001 1221 nt  strand: - CS-h1 cds GC 0.43 Exon 4
ATGGGGTTTATTGTAGCATTAGTTCTCATGTCCCTTTTAGCAATGTATCTAGCAGGAGGAGCAGAAGCAGTTTTAAATCTTCAGCCAAACTCTTCAATCTCTATCACGTATCATCCTCATTTTGGTCCTCATGATGATCTGATCCTCCTTGAAATTGATGACAAGCTTCTTCCAGATGTCCTCCACCAGAGGGTAACTTTAAGAGGACAACCCAATGAAGATGCTGTTCTTTGTACTCAATCAAAGACTTATTCTATCAAATTTGTTGGAAACTCCAATTCTGTGTTCCTTATACCCCCAGTAGATCAGTCAGCATTGCATGAACATCCACAATATTCTGATGAGAAAGATGATGACCAGCGGGTTGTTGCATCTGTCATTAAAGTGGCTCCTGGTAACATGGAGCTTGTTGAGGTTGCTCCCAGGCTGGACAAGCTTAAATTGCTTCTCTTGGAGAATCCTTTTACATCTGAGGAGGTCTCAGAGAAAGAGGAATTGGAAGGGATGGAGGAACAGAAAACAAATTTGTTTAAATGGAATGATCTTATAGATAGGGTTCAAGCCAGTGATGATGAATTGAGGTCTGGATTACGGGCTCTTTCAGCAGTAGAGATTGATGGGTATTGGAGAATTGTGGATGAGAAGTACATGGGTACTATTCTGAATATGCTTCTGCACAACTCAGTGTTGAATGATTGGTCATTAGATGCACTTGGTGAAGATGAAGTTGTGGGTGTTCTGGAATCAGATGGTTTTCCTCGCACACTAGGGTTACATTGTTTGCAAGTTTATGGTAGCAAGGTGGATGAGGGTGTTGGCAGTTGTGTATGGAAGTTGGATGAGAGGCGCTTATGCATTCATTTTGCTAGAGAAATCTTGAAGGATGGGAAGAGGAAGATGGAAAGTTTCATGGAGGAGTGGATTCAAAAGATTCCAGATGGGATGCAGGCAAGTTTTGACATGTTGGAAGGTGAAGTTTTGACAGAAAAGTTTGGGGTTGAGACATGGGTTCGTGCCTTTAGTGTTTCTTCCCTGCCCTCTAACCCAGCTGCACGTTTCTCCATGCTTTTTCAAGAGCGGCCAAAATGGGAGTGGAAGGATCTACAGCCCTATATAAGGGATTTGACTGTACCGGGTCTTTCTTCAGAAGGCTTGCTTCTGAAATACACACGAAAAACACAACCAAACTCAGATGCAGAGCCTGTATTTAGTGCCAGATAG
```

The python script can be called as follows:

	>python /path/to/transProt.py /path/to/multi_fasta.fa

The script will output a .fa file in the directory with the CDS.fa file and it will output the sequences in the terminal.
