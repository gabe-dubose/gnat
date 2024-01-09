import json

def parse_brite_json(brite_json):
    #read file
    with open(brite_json, 'r') as infile:
        brite_dict = json.load(infile)

    #initialize reformatted dictionary
    brite_reformatted = {}

    #begin parsing
    if 'children' in list(brite_dict.keys()):
        parent_group = brite_dict['children']
        #get level1 info
        for level1_group in parent_group:
            if 'name' in level1_group and 'children' in level1_group:
                level1_name = level1_group['name']
                
                #get level2 info
                for level2_group in level1_group['children']:
                    if 'name' in level2_group and 'children' in level2_group:
                        level2_name = level2_group['name']

                        #get level3 info
                        for level3_group in level2_group['children']:
                            if 'name' in level3_group and 'children' in level3_group:
                                level3_name = level3_group['name']
                                
                                #get terminal info
                                for level4_group in level3_group['children']:
                                    if 'name' in level4_group:
                                        gene_information = level4_group['name']
                                        
                                        #clean up info
                                        gene_id = gene_information.split(' ')[0]
                                        level1_name_cleaned = " ".join(level1_name.split(' ')[1:])
                                        level2_name_cleaned = " ".join(level2_name.split(' ')[1:])
                                        level3_name_cleaned = " ".join(level3_name.split(' ')[1:]).split("[")[0].strip()

                                        heirarchy = {'functional_group_level1' : level1_name_cleaned,
                                                    'functional_group_level2' : level2_name_cleaned,
                                                    'functional_group_level3' : level3_name_cleaned}
                                        
                                        name_1 = " ".join(gene_information.split(' ')[1:]).split('\t')[0]
                                        name_2 = gene_information.split(';')[1].strip()
                                        ko_number = gene_information.split('\t')[1].split(' ')[0]

                                        #assemble entry for gene_id
                                        entry = {'ko_number' : ko_number,
                                                    'description_1' : name_1,
                                                    'description_2' : name_2,
                                                    'functional_heirarcy' : heirarchy}
                                        
                                        #add information to dictionary
                                        if gene_id not in brite_reformatted:
                                            brite_reformatted[gene_id] = []
                                        
                                        brite_reformatted[gene_id].append(entry)
    return brite_reformatted