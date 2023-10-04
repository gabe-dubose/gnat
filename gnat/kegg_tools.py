import json

def parse_brite_json(brite_json):
    #read file
    with open(brite_json, 'r') as infile:
        brite_dict = json.load(infile)
    
    #initialize reformatted dictionary
    brite_reformatted = {}
    
    #get level 1 data
    try:
        for i in range(len(brite_dict['children'])):
            level1_name = " ".join(brite_dict['children'][i]['name'].split(' ')[1:]).strip()
            level1_contents = brite_dict['children'][i]['children']
            #get level2 data
            try:
                for j in range(len(level1_contents)):
                    level2_name = " ".join(level1_contents[j]['name'].split(' ')[1:]).strip()
                    level2_contents = level1_contents[j]['children']
                    #get level 3 data
                    try:
                        for k in range(len(level2_contents)):
                            level3_name = " ".join(level2_contents[k]['name'].split(' ')[1:]).split("[")[0].strip()
                            level3_contents = level2_contents[k]['children']
                            try:
                                #get level 4 data
                                for l in range(len(level3_contents)):
                                    level4_info = level3_contents[l]['name']

                                    #collect information
                                    gene_id = level4_info.split(' ')[0]
                                    try:
                                        name_1 = " ".join(level4_info.split(' ')[1:]).split('\t')[0]
                                    except:
                                        name_1 = 'NA'
                                    try:
                                        ko_number = level4_info.split('\t')[1].split(' ')[0]
                                    except:
                                        ko_number = 'NA'
                                    try:
                                        name_2 = level4_info.split(';')[1].strip()
                                    except:
                                        name_2 = 'NA'

                                    heirarchy = {'functional_group_level1' : level1_name,
                                                'functional_group_level2' : level2_name,
                                                'functional_group_level3' : level3_name}
                                    
                                    #assemble entry for gene_id
                                    entry = {'ko_number' : ko_number,
                                             'description_1' : name_1,
                                             'description_2' : name_2,
                                             'functional_heirarcy' : heirarchy}

                                    #add information to dictionary
                                    if gene_id not in brite_reformatted:
                                        brite_reformatted[gene_id] = []
                                    
                                    brite_reformatted[gene_id].append(entry)
                                    
                            except:
                                pass
                    except:
                        pass
            except:
                pass
    except:
        pass

    return brite_reformatted