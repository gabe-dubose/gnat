import pandas as pd

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