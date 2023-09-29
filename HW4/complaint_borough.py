# Tess Gompper #260947251
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="Outputs the number of each complaint type per borough for a given (creation) date range")
# borough_complaints.py -i <the input csv file> -s <start date> -e <end date> [-o <output file>]
parser.add_argument("-i", help="Input File", metavar="<the input csv file>", required=True)
parser.add_argument("-s", help="start date", metavar="<start date>", required=True)
parser.add_argument("-e", help="end date", metavar="<end date>", required=True)
parser.add_argument("-o", help="optional output file", metavar="<output file>", required=False)

args = parser.parse_args()

df = pd.read_csv(args.i)
start_date = pd.to_datetime(args.s)
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(args.e)

# reformat dates to compare with pandas
df['createdDate'] = df['createdDate'].str.split().str[0]
df['createdDate'] = pd.to_datetime(df['createdDate'], format="%m/%d/%Y")

filtered_df = df[(df['createdDate'] >= start_date) & (df['createdDate'] <= end_date)]

projected = filtered_df[['complaintType', 'borough']]

result =  projected.groupby(['complaintType', 'borough']).size().reset_index(name='count')


# output file provided
if args.o:
    result.to_csv(args.o)
# no output file provided
else:
     print(result)