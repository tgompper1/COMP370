import argparse
import json
import random
import csv

PYTHONENCODING = "utf-8"

def get_posts(file, num_posts):
    """
        return a list of num_posts posts from file
    """
    with open(file) as f:
        page_json = json.load(f)
    # page_json = file.json()
    page = page_json.get("data")
    new_posts = page.get("children")
    total_num_posts = 0
    i =0
    for child in new_posts:
        child_post = new_posts[i].get("data")
        total_num_posts+=1
        i+=1
        print(total_num_posts)

    if total_num_posts <= int(num_posts):
        posts_to_return = [0]*total_num_posts
        p=0
        for i in range(total_num_posts):
            posts_to_return[i] = new_posts[i].get("data")
    else:
        posts_to_return = [0]*num_posts
        for i in range(num_posts):
            p = random.randrange(total_num_posts)
            posts_to_return[i] = new_posts[p].get("data")

    return posts_to_return

def get_author_title(post):
    #data = post['data']
    author = post['author_fullname']
    title = post['title']

    return [author, title, ""]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", dest='out_file', help='output tsv file', metavar='<out_file>')
    parser.add_argument('json_file', help = 'input json file', metavar='<json_file>')
    parser.add_argument('num_posts_to_output', help = 'number of posts to output', metavar='<num_posts_to_output>')
    
    args=parser.parse_args()

    out_file = args.out_file
    json_file = args.json_file
    num_posts = args.num_posts_to_output

    posts = get_posts(json_file, num_posts)
    #print(posts)
    information = []
    headers=["name", "title", "coding"]
    information.append(headers) # headers
    #print(information)

    for post in posts:
        author_title = get_author_title(post)
        #print(author_title)
        information.append(author_title)

    with open(out_file,"w+", encoding=PYTHONENCODING) as tsv:
        csvWriter = csv.writer(tsv,delimiter='\t')
        csvWriter.writerows(information)

if __name__ == "__main__":
    main()