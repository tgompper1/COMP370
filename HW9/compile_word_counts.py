import argparse
import json
import csv
import re

THRESHOLD = 5

STOPWORDS = ["a", "about", "above", "across", "after", "again", "against", "all", "almost", "alone", "along", 
             "already", "also", "although", "always", "among", "an", "and", "another", "any", "anybody", "anyone", 
             "anything", "anywhere", "are", "area", "areas", "around", "as", "ask", "asked", "asking", "asks", "at", 
             "away", "b", "back", "backed", "backing", "backs", "be", "became", "because", "become", "becomes", "been", 
             "before", "began", "behind", "being", "beings", "best", "better", "between", "big", "both", "but", "by", 
             "c", "came", "can", "cannot", "case", "cases", "certain", "certainly", "clear", "clearly", "come", "could", 
             "d", "did", "differ", "different", "differently", "do", "does", "done", "down", "down", "downed", "downing", 
             "downs", "during", "e", "each", "early", "either", "end", "ended", "ending", "ends", "enough", "even", 
             "evenly", "ever", "every", "everybody", "everyone", "everything", "everywhere", "f", "face", "faces", "fact", 
             "facts", "far", "felt", "few", "find", "finds", "first", "for", "four", "from", "full", "fully", "further", 
             "furthered", "furthering", "furthers", "g", "gave", "general", "generally", "get", "gets", "give", "given", 
             "gives", "go", "going", "good", "goods", "got", "great", "greater", "greatest", "group", "grouped", "grouping", 
             "groups", "h", "had", "has", "have", "having", "he", "her", "here", "herself", "high", "high", "high", 
             "higher", "highest", "him", "himself", "his", "how", "however", "i", "if", "important", "in", "interest", 
             "interested", "interesting", "interests", "into", "is", "it", "its", "itself", "j", "just", "k", "keep", 
             "keeps", "kind", "knew", "know", "known", "knows", "l", "large", "largely", "last", "later", "latest", 
             "least", "less", "let", "lets", "like", "likely", "long", "longer", "longest", "m", "made", "make", "making", 
             "man", "many", "may", "me", "member", "members", "men", "might", "more", "most", "mostly", "mr", "mrs", "much",
              "must", "my", "myself", "n", "necessary", "need", "needed", "needing", "needs", "never", "new", "new", "newer",
             "newest", "next", "no", "nobody", "non", "noone", "not", "nothing", "now", "nowhere", "number", "numbers", "o",
             "of", "off", "often", "old", "older", "oldest", "on", "once", "one", "only", "open", "opened", "opening", "opens",
              "or", "order", "ordered", "ordering", "orders", "other", "others", "our", "out", "over", "p", "part", "parted",
              "parting", "parts", "per", "perhaps", "place", "places", "point", "pointed", "pointing", "points", "possible", 
              "present", "presented", "presenting", "presents", "problem", "problems", "put", "puts", "q", "quite", "r",
              "rather", "really", "right", "right", "room", "rooms", "s", "said", "same", "saw", "say", "says", "second", 
              "seconds", "see", "seem", "seemed", "seeming", "seems", "sees", "several", "shall", "she", "should", "show",
              "showed", "showing", "shows", "side", "sides", "since", "small", "smaller", "smallest", "so", "some", "somebody",
              "someone", "something", "somewhere", "state", "states", "still", "still", "such", "sure", "t", "take", "taken", 
              "than", "that", "the", "their", "them", "then", "there", "therefore", "these", "they", "thing", "things", "think", 
              "thinks", "this", "those", "though", "thought", "thoughts", "three", "through", "thus", "to", "today", "together", 
              "too", "took", "toward", "turn", "turned", "turning", "turns", "two", "u", "under", "until", "up", "upon", "us", 
              "use", "used", "uses", "v", "very", "w", "want", "wanted", "wanting", "wants", "was", "way", "ways", "we", "well", 
              "wells", "went", "were", "what", "when", "where", "whether", "which", "while", "who", "whole", "whose", "why", "will", 
              "with", "within", "without", "work", "worked", "working", "works", "would", "x", "y", "year", "years", "yet", "you", 
              "young", "younger", "youngest", "your", "yours", "z"]

PUNCTUATION = ["(", ")", "[", "]", ",", "-", ".", "?", "!", ":", ";", "#", "&"]

def get_word_counts(dialog_file, output_file):

    # prep csv
    file = open(dialog_file)
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    rows = []
    for row in csvreader:
        edited_row = row[2:]
        rows.append(edited_row)

    # prep dictionary 
    ponies = {
        "Twilight Sparkle": {},
        "Applejack" : {},
        "Rarity" : {},
        "Pinkie Pie": {},
        "Rainbow Dash": {},
        "Fluttershy":{}
    }

    # read row by row
    for row in rows:
        pony = row[0]
        dialog = row[1]
        # print(dialog)for 
        for punc in PUNCTUATION:
            if punc in dialog:
                dialog = dialog.replace(punc, " ")
        dialog_list = dialog.split()
        for word in dialog_list:
            word = word.lower()
            # if "[" in word:
            #     word = word.replace("[", "")
            # if "]" in word:
            #     word = word.replace("]", "")
            if word in STOPWORDS:
                continue
            elif pony in ponies:
                if word in ponies[pony]:
                    prev = ponies[pony][word]
                    ponies[pony][word] = prev + 1
                else:
                    ponies[pony][word] = 1
    
   
    for pony, words in ponies.items():
        to_delete = []
        for key in words:
            if words[key] < THRESHOLD:
                to_delete.append(key)
        for word in to_delete:
            words.pop(word)

    # write to json file
    with open(output_file, 'w') as out:
        json.dump(ponies, out)




def main():
    print("running...")
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", dest='word_counts_json', help='output json file', metavar='<word_counts_json>')
    parser.add_argument('-d', dest='clean_dialog', help = 'input csv file', metavar='<clean_dialog.csv file>')
    
    args=parser.parse_args()

    word_counts = args.word_counts_json
    dialog = args.clean_dialog 

    get_word_counts(dialog, word_counts)

if __name__ == "__main__":
    main()

