import pandas as pd
import math

#A function to calculate pairwise rmse values for each comparison in a comparisons list generate by misc_utils.get_pairwise_comparisons
# input[data]: A pandas dataframe with column names corresponding to the names of comparisons in the comparisons list
# input[comparisons]: A list of lists, where each sublist contains a unique pairwise comparison
# output[rmse_results]: a pandas dataframe in long format containing pairwise RMSE values for each comparison
def pairwise_rmse(data, comparisons):
    
    rmse_results = pd.DataFrame(columns=["comparison1", "comparison2", "rmse"])
    
    #get gene ids
    gene_ids = list(data.columns)
    #iterate through comparisons
    for comparison in comparisons:
        sample1_data = data.loc[comparison[0]]
        sample2_data = data.loc[comparison[1]]
        
        #get data and calculate total error
        total_se = 0
        for gene in gene_ids:
            sample1_value = sample1_data[gene]
            sample2_value = sample2_data[gene]
            
            exp_error = sample1_value - sample2_value
            exp_error = exp_error ** 2
            
            total_se += exp_error
            
        #calculate rsme
        mse = total_se / len(gene_ids)
        rmse = math.sqrt(mse)
        
        #assemble results
        results_df = pd.DataFrame({'comparison1' : [comparison[0]], 'comparison2' : [comparison[1]], 'rmse' : [rmse]})
        
        rmse_results = pd.concat([rmse_results, results_df])
    
    return rmse_results