Tess Gompper #260947251

### Downloading CSV file 
1. Download to local machine
2. copy to remote machine:
    `scp -P 22 C:\Users\tgomp\Downloads\clean_dialog.csv\clean_dialog.csv tgomp@18.221.182.118:`

### How big is the dataset?
- `wc -l clean_dialog.csv`
- 36860 Lines, 670166 Words

### What's the structure of the data?
- `head -n 1 clean_dialog.csv`
- "title","writer","pony","dialog"
- populated by strings

### How many episodes does it cover?
- `csvsql -I --query "select count(distinct title) from clean_dialog" clean_dialog.csv`
- 197

### Unexpected aspect of the data
- One unexpected aspect of the data for me is that thhe narrator and other characters, like Spike, are considered Ponies. This would present challenges and new questions in analysis because we would have to further consider what lines count when we're looking at the percent of the total a pony had.