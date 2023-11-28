import argparse
import json
import csv
import re

DO_NOT_INCLUDE = ["others", "ponies", "and", "all"]

def build_interaction_network(mlp_script_input, output_file):
    network = {
        # “twilight sparkle”: {
            # “spike”: <# of interactions between twilight sparkle and spike>,
            # “applejack”: <# of interactions between ts and aj>,
            # “pinkie pie”: <# of interactions between ts and pp>,
            # …
        # },
        # “pinkie pie”: {
            # “twilight sparkle”: <# of interactions between ts and pp>
            # ...
        # }
        # ...

    }

    file = open(mlp_script_input)
    csvreader = csv.reader(file)
    header=[]
    header=next(csvreader)
    rows=[]
    for row in csvreader:
        edited_row=[]
        edited_row.append(row[0])
        edited_row.append(row[2])
        rows.append(edited_row)
    mlp_script=rows

    first_row = mlp_script[0]
    prev_episode = first_row[0]
    prev_pony = first_row[1]
    prev_pony = prev_pony.lower()
    for i in range(len(mlp_script)):
        if i == 0:
            continue
        else:
            episode = mlp_script[i][0]
            pony = mlp_script[i][1]
            pony = pony.lower()
            
            if prev_pony == "DEAD":
                prev_pony = pony
                prev_episode=episode
            else:
                dead_word=False
                for word in DO_NOT_INCLUDE:
                    if word in pony:
                        dead_word=True
                if not dead_word:
                    if episode == prev_episode:
                        if pony in network:
                            pony_contacts = network[pony]
                            if prev_pony in pony_contacts:
                                pony_contacts[prev_pony] = pony_contacts[prev_pony]+1
                        elif prev_pony in network:
                            prev_pony_contacts = network[prev_pony]
                            if pony in prev_pony_contacts:
                                prev_pony_contacts[pony] = prev_pony_contacts[pony]+1
                        else:
                            network[pony] = {prev_pony: 1}
                    else:
                        continue
                    
                    prev_pony = pony
                    prev_episode = episode
                else:
                    prev_pony = "DEAD"

    with open(output_file, 'w') as out:
        json.dump(network, out)


        

def main():
    print("running...")
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest='input_script_csv', help='path to input script csv file', metavar='<input_script.csv>')
    parser.add_argument('-o', dest='interaction_network_json', help = 'output path to interaction netork jsonfile ', metavar='<interaction_network.json>')
    
    args=parser.parse_args()

    mlp_script = args.input_script_csv
    interaction_network_path = args.interaction_network_json 

    build_interaction_network(mlp_script, interaction_network_path)

if __name__ == "__main__":
    main()
