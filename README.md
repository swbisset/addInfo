# addInfo.py
Adds information from different csv and fasta files. The most common use for this has been adding extra information (*i.e.* Genus/ species level information) to a csv file generated from an NCBI BLAST+ alignment. 

**Warning:** addInfo.py is written in *Python version 2.7*, not *Python 3.0*. Maybe one day that will be fixed. 

## Usage 
Essentially, addInfo.py takes in two inputs: **File1** is a csv or tsv file (such as a BLAST+ multi-query output file) which needs some additional information added. **File2** is a file, which can be in csv, tsv, or another (*e.g.* fasta) input, and contains the additional information to be added as a new column to **File1**. Importantly, both **File1** and **File2** need to have at least one column each which contains the same information, such as gene or protein IDs, or whatever it is you are wanting to compare. 

### Optional flags

1. *-1/ -2 --column1/ --column2* 

   These flags take in an integer, pointing to which columns in **File1** and **File2** to compare to, respectively. Note that these flags expect the columns to start at 1, not 0. Defaults for *-1* and *-2* are 1 for both. 

2. *-1 --integer*

   This flag takes an integer of which column to take from **File2** to add to **File1**. Like the above flags, a minimum value of 1 is expected. The default value for this flag is 2. 
   
3. *-H --header* 

   This flag denotes whether or not **File1** contains a header. If it is selected, the first line of **File1** will be written to the output prior to comparison. 
   
4. *-f --fasta* 

   Use this flag if **File2** is in fasta format. The incoming fasta file will then be read in as a two-column list, comprising IDs in one column and sequences in the other, 
   
5. *-o --output* 

   Name the output file. The file format will be as a csv, so should include that as a suffix. Default output format if this flag is not selected is `[File1]_info.csv`. 
