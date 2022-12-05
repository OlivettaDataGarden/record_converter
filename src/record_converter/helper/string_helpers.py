"""
Module to provide method to process, clean etc strings.

Methods
    - normalize_string 
    - fuzzy_compare_str
    - best_result_from_fuzzy_compare_str
"""
import operator

import unidecode

# from fuzzywuzzy import fuzz, process


def normalize_string(accented_string):
    """
    remove special characters form string and make lower case
    """
    accented_string = accented_string.replace('"', '')
    unaccented_string = unidecode.unidecode(accented_string)
    normalized_string = unaccented_string.lower().strip()
    return normalized_string


# def fuzzy_compare_list(str, choices_list):
#     """
#     Return the best matching entry from choices_list with str
#     based upon token sort algorithm from fuzzywuzzy

#     Args:
#         str (str): string to match
#         choices_list (list of str): choicec from which to match

#     Returns:
#         [dict]: {'fuzzy_sort_ratio': <value of best match>}
#     """
#     result = process.extractOne(
#         str, choices_list, scorer=fuzz.token_sort_ratio)
#     return dict(fuzzy_sort_ratio=result[1])


# def fuzzy_compare_str(str1, str2):
#     fuzzy_ratio = fuzz.ratio(str1, str2)
#     fuzzy_sort_ratio = fuzz.token_sort_ratio(str1, str2)
#     fuzzy_partial_ratio = fuzz.partial_ratio(str1, str2)
#     return {
#         'fuzzy_ratio': fuzzy_ratio,
#         'fuzzy_sort_ratio': fuzzy_sort_ratio,
#         'fuzzy_partial_ratio': fuzzy_partial_ratio}


# def best_result_from_fuzzy_compare_str(str1, str2):
#     all_fuzzy_results = fuzzy_compare_str(str1, str2)
#     key_with_max_fuzzy_value = \
#         max(all_fuzzy_results.items(), key=operator.itemgetter(1))[0]
#     return all_fuzzy_results[key_with_max_fuzzy_value]
