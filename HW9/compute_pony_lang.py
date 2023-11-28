import argparse
import math
import json
 
def compute_ponies(n, counts):
    f = open(counts)
    counts_open = json.load(f)
    to_return={}
    for pony, words in counts_open.items():
        word_tfidfs = {}
        for key in words:
            c = get_tf_idf(key, pony, counts)
            word_tfidfs[key] = c
        top_n = []
        temp_words = words
        for i in range(0, int(n)):
            cur_max = 0
            cur_max_key = ""
            for key in temp_words:
                if temp_words[key] > cur_max:
                    cur_max = temp_words[key]
                    cur_max_key = key
            temp_words.pop(cur_max_key)
            top_n.append(cur_max_key)
            # print(pony + ": " + cur_max_key)
        to_return[pony] = top_n

    with open("distinctive_pony_words.json", 'w') as out:
        json.dump(to_return, out)
        
            
            



def get_tf_idf(w, pony, counts):
    tf = get_tf(w, pony, counts)
    idf = get_idf(w, counts)
    tf_idf = tf * idf
    return tf_idf

def get_tf(w, pony, counts):
    f = open(counts)
    counts_open = json.load(f)
    tf = counts_open[pony][w]
    return tf

def get_idf(w, counts):
    f = open(counts)
    counts_open = json.load(f)
    num_ponies_used_w = 0
    num_ponies = 0
    for pony, words in counts_open.items():
        num_ponies +=1
        if w in words:
            num_ponies_used_w += 1
    idf = math.log(num_ponies/num_ponies_used_w)
    return idf
    
        

def main():
    print("running...")
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest='pony_counts_json', help='pony word counts json file', metavar='<pony_counts.json>')
    parser.add_argument('-n', dest='num_words', help = 'input csv file', metavar='<num_words>')
    
    args=parser.parse_args()

    pony_counts = args.pony_counts_json
    num_words = args.num_words

    compute_ponies(num_words, pony_counts)



if __name__ == "__main__":
    main()
