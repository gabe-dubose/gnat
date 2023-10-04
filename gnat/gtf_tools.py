#A function to extract the gene_id and protein_id from a gtf file
# input[gtf_file]: A gtf file
# output[gene_protein_id_dict]: A dictionary structured as {protein_id : gene_id} such that each gene id can be querried by searching for the corresponding protein id
def get_gene_protein_id_dictionary(gtf_file):
    #initialize dictionary
    gene_protein_id_dict = {}
    #read file
    with open(gtf_file, 'r') as infile:
        lines = infile.readlines()
    
    for line in lines:
        if 'protein_id' in line and 'gene_id' in line and 'orig_protein_id' not in line:
            protein_id = line.split('protein_id')[1].split(';')[0].strip().strip('"')
            gene_id = line.split('gene_id')[1].split(';')[0].strip().strip('"')

            gene_protein_id_dict[protein_id] = gene_id

    return gene_protein_id_dict