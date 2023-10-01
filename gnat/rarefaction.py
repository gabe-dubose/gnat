import pandas as pd
import random

# A function to generate sample pools from pandas dataframe
# input[data]: A pandas dataframe where rows correspond to samples and columns correspond to the unique items within each sample. Sample ids should be the dataframe index
# input[sample_id]: The identifier for the sample to generate the pool for.
# output[total_pool]: A list of components (column headers) within each sample, where the total numebr of each component is equal to the corresponding value in the counts matrix.
def assemble_pool(data, sample_id):
    #get ids
    ids = list(data.columns)
    #get sample_data
    sample_data = data.loc[sample_id]
    #assemble pools
    total_pool = []
    for ind in ids:
        ind_count = int(sample_data[ind])
        for i in range(ind_count):
            total_pool.append(ind)
    return total_pool

#A function to get the rarefaction curve for a given sample pool.
# input[pool]: A pool of components generated by the "assemble_pool" function
# input[minimum_sample]: The subsample size to start rarefaction.
# input[maximum_sample]: The subsample size to stop rarefaction. 
# input[step]: The step size to make between subsample sizes.
# output[curve]: The rarefaction curve for the given pool. 
#   The curve is output as a dictionary formatted as: {'count' : count, 'depth' : subsample_size}
def get_rarefaction_curve(pool, minimum_sample, maximum_sample, step):
    #define maximum sample size
    if maximum_sample == 'total':
        maximum_sample = len(pool)
    elif type(maximum_sample) == int:
        maximum_sample = maximum_sample
    
    #generate rarefaction curves for unique counts
    count = []
    subsample_size = []
    #iteratively sample pool
    for i in range(minimum_sample, maximum_sample, step):
        #select random subsample
        subset = random.sample(pool, i)
        #calculate number of unique entities
        unique_count = len(set(subset))
        count.append(unique_count)
        subsample_size.append(i)
        print(f"Completed subsample size {i}")
    #assemble output
    curve = {'count' : count, 'depth' : subsample_size}
    return curve

#A wrapper function to generate a rarefaction curve for a given sample within a pandas dataframe.
# input[sample_id]: The identifier for the sample to generate the rarefaction curve for.
# input[parameters]: A dictioanry containing the parameters to be passed to the "get_rarefaction_curve" function. Dictionary should be formatted as:
#   parameters = {'minimum_sample' : int, 'maximum_sample' : int, 'step' : int}
# output[rarefaction_curve]: A dictionary containing the sample_id as the key and the rarefaction curve as the the value.
def generate_rarefaction_curve(sample_id, parameters):
    #assemble pool
    sample_pool = assemble_pool(parameters['data'], sample_id)
    #get rarefaction curve
    rarefaction_curve = get_rarefaction_curve(sample_pool, parameters['minimum_sample'], parameters['maximum_sample'], parameters['step'])
    #assemble and return output
    rarefaction_curve = {sample_id : rarefaction_curve}
    return rarefaction_curve

#A wrapper function to iteratively generate rarefaction curves for specified samples.
# input[sample_ids]: A list of sample ids to generate rarefaction curves for.
# output[rarefaction_curves]: A list of rarefaction curves generated from the "generate_rarefaction_curve" function.
def generate_rarefaction_curves(sample_ids, parameters):
    #initialize list to store rarefaction curves
    rarefaction_curves = []
    #get rarefaction curve for each sample in sample_ids
    for sample_id in sample_ids:
        #output progress report
        print(f"Generating rarefaction curve for {sample_id}: ({sample_ids.index(sample_id)+1} of {len(sample_ids)})")
        #get rarefaction curve
        rarefaction_curve = generate_rarefaction_curve(sample_id, parameters)
        rarefaction_curves.append(rarefaction_curve)
    return rarefaction_curves