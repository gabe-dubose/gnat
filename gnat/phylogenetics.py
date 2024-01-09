from distutils import extension
import os

#A function to iterate through a directory of fasta files, perform multiple sequence alignments
# input[direcotry]: The path to the directory containing fasta files
# input[extension]: The file extension for fasta files
#Note: This function assumes that muscle is installed and callable from the command line
def batch_alignments(directory, extension, alignment_outdir):
    #get files
    files = os.listdir(directory)
    #iterate through file
    for file in files:
        #get complete files
        completed = os.listdir(alignment_outdir)
        #keep only ones with correct suffix
        if file.split('.')[1] == extension:
            #check if file has been completed
            alignment_file = f"{file.split('.')[0]}_alignment.fasta"
            if alignment_file not in completed:
                #check if alignment is running
                working_alignment = f"{file.split('.')[0]}.working"
                if working_alignment not in completed:
                    #add working indicator
                    os.system(f"touch {alignment_outdir}/{working_alignment}")
                    #run alignment
                    alignment_command = f"muscle -align {directory}/{file} -output {alignment_outdir}/{file.split('.')[0]}_alignment.fasta"
                    os.system(alignment_command)
                    #Once completed, remove working indicator
                    os.system(f"rm {alignment_outdir}/{working_alignment}")
            else:
                print(f"Skipping: {alignment_file} [Working or Completed]")

#A function to iterate through a directory of alignments in fasta format and make a phylogenetic tree
#Note: This function assumes that iqtree is installed and callable from the command line
def batch_phylogenies(alignment_dir, extension, phylogeny_outdir):
    #get files
    files = os.listdir(alignment_dir)
    #iterate through file
    for file in files:
        completed = os.listdir(phylogeny_outdir)
        #keep only ones with correct suffix
        if file.split('.')[1] == extension:
            #check if phylogeny has been completed
            phylogeny_file = f"{file}.treefile"
            if phylogeny_file not in completed:
                #check if phylogeny is working
                working_phylogeny = f"{file.split('.')[0]}.workingphylo"
                if working_phylogeny not in completed:
                    #add working indicator
                    os.system(f"touch {phylogeny_outdir}/{working_phylogeny}")
                    #make phylogeny
                    phylogeny_command = f"iqtree -s {alignment_dir}/{file} -B 1000 -redo"
                    os.system(phylogeny_command)
                    #remove working indicator
                    os.system(f"rm {phylogeny_outdir}/{working_phylogeny}")
            else:
                print(f"Skipping: {phylogeny_file} [Working or Completed]")
    #clean up
    #move tree file to outdir
    os.system(f"mv {alignment_dir}/*.treefile {phylogeny_outdir}")

#A function to calcualte the Faith index (sum branch lengths) for a given tree.
# input[newick_file]: A file containing a phylogenetic tree in newick format
# output[faith_index]: A numeric values representing Faith's Phylogenetic Diversity index (sum of branch lengths)
#Note: function requires the Bio python module
def faith_index(newick_file):
    from Bio import Phylo

    tree = Phylo.read(newick_file, "newick")