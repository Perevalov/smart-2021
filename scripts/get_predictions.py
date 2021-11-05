import requests
import json
import argparse
from tqdm import tqdm

query_dbpedia = "https://webengineering.ins.hs-anhalt.de:41024/predict_dbpedia?question={0}"
query_wikidata = "https://webengineering.ins.hs-anhalt.de:41024/predict_wikidata?question={0}"

headers = {"content-type": "application/json"}

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, # "../data/at/dbpedia/smarttask_dbpedia_test_questions.json"
                        help='questions for prediction')
    parser.add_argument('--output', type=str, # "../data/at/dbpedia/smarttask_dbpedia_test_questions_predictions.json"
                        help='where to save output result')
    args = parser.parse_args()
    return args

def read_json(filename):
    with open(filename) as f:
        return json.load(f)
    
def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    args = arg_parser()
    file = read_json(args.input)

    response = list()
    for q in tqdm(file):
        if 'dbpedia' in args.input:
            query = query_dbpedia
        else:
            query = query_wikidata
            
        result = requests.get(query.format(q['question']) , headers=headers).json()
        q['category'] = result['category']
        q['type'] = result['answer_type']
        response.append(q)
        write_json(response, args.output)