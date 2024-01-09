import pandas as pd
import json
import os

#A function to get all pairwise comparisons from the index column of a pandas dataframe
# input[data]: A pandas dataframe with a defined index column
# output[comparisons]: A list of lists, where each sublist contains a unique pairwise comparison
def get_pairwise_comparisons(data):
    comparisons = []
    for sample1 in list(data.index):
        for sample2 in list(data.index):
            if sample1 != sample2:
                if [sample1, sample2] not in comparisons and [sample2, sample1] not in comparisons:
                    comparison = [sample1, sample2]
                    comparisons.append(comparison)
    return comparisons

#A function to partition gene sequence clusters into individual files
# input[clusters]: A json file where each key is a cluster name and each value is a list of sequence ids in said cluster
# input[sequences]: A fasta file that contains the sequences to be split
#Note: function requires pyfaidx
#Note: function assumes that the header line for each sequence is in NCBI format
def partition_sequence_clusters(clusters, sequences, outdir):
    import pyfaidx

    #load cluster file
    with open(clusters, 'r') as infile:
        cluster_data = json.load(infile)

    #load sequence file
    sequence_data = pyfaidx.Fasta(sequences)
    #store sequence ids
    sequence_ids = list(sequence_data.keys())

    #iterate through each cluster
    for cluster in cluster_data:
        #add file
        os.system(f"touch {outdir}/{cluster}.fasta")
        #open outfile
        with open(f"{outdir}/{cluster}.fasta", 'w') as outfile:
            genes = cluster_data[cluster]
            #iterate through each gene in the cluster
            for gene_id in genes:
                #iterate through the ids in sequence_ids and find the whole id
                for id in sequence_ids:
                    #extract portion that is the protein id
                    protein_id = id.split('_')[2]
                    if gene_id == protein_id:
                        #get sequence
                        gene_sequence = str(sequence_data[id])
                        #write to file
                        outfile.write(f">{gene_id}\n{gene_sequence}\n")

