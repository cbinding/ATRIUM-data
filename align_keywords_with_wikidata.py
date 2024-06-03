# code suggested by ChatGPT and modified slightly for presentation
# performs call to https://www.wikidata.org/w/api.php?action=wbsearchentities&search=demonstrative%20pronoun&language=en
# then filters to highest scoring results
import requests
from difflib import SequenceMatcher

WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"

def preprocess_keyword(keyword):
    return keyword.strip().lower()

def query_wikidata(keyword):
    params = {
        'action': 'wbsearchentities',
        'search': keyword,
        'language': 'en',
        'format': 'json'
    }
    response = requests.get(WIKIDATA_API_URL, params=params)
    return response.json().get('search', [])

def select_best_match(keyword, results):
    best_match = None
    highest_score = 0
    for result in results:
        score = SequenceMatcher(None, keyword, result['label']).ratio()
        if score > highest_score:
            highest_score = score
            best_match = result
    return best_match

def align_keywords_with_wikidata(keywords):
    aligned_results = []
    for keyword in keywords:
        processed_keyword = preprocess_keyword(keyword)
        results = query_wikidata(processed_keyword)
        best_match = select_best_match(processed_keyword, results)
        if best_match:
            aligned_results.append({
                'keyword': keyword,
                'wikidata_id': best_match['id'],
                'wikidata_url': best_match['concepturi']
            })
        else:
            aligned_results.append({
                'keyword': keyword,
                'wikidata_id': None,
                'wikidata_url': None
            })
    return aligned_results

# Example usage - note "demonstrative pronouns" gives different results to "demonstrative pronoun"
# one quick improvement would be preprocessing to make keywords singular to match Wikidata labels
keywords = [
    "demonstrative pronoun", 
    "definite article", 
    "grammaticalization", 
    "Old Egyptian", 
    "Coptic", 
    "Old Kingdom", 
    "joint attention", 
    "dialect", 
    "ddc:417"
]
aligned_results = align_keywords_with_wikidata(keywords)
for result in aligned_results:
    line = "{url:45}\"{keyword}\"".format(
        url=str(result['wikidata_url']), 
        keyword=str(result['keyword'])
    )
    print(line)

'''
Results:
http://www.wikidata.org/entity/Q34793275     "demonstrative pronoun"
http://www.wikidata.org/entity/Q2865743      "definite article"
http://www.wikidata.org/entity/Q1358208      "grammaticalization"
http://www.wikidata.org/entity/Q447117       "Old Egyptian"
http://www.wikidata.org/entity/Q36155        "Coptic"
http://www.wikidata.org/entity/Q15624191     "Old Kingdom"
http://www.wikidata.org/entity/Q9636076      "joint attention"
http://www.wikidata.org/entity/Q33384        "dialect"
None                                         "ddc:417"
'''
