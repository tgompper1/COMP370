import pandas as pd

df = pd.read_csv("IRAhandle_tweets_1.csv")

df = df.head(10000).loc[(df['language']=='English') & (df['content'].str.contains("?", regex=False)==False)]

df = df[["tweet_id", "publish_date", "content"]]
df["trump_mention"] = df['content'].str.contains(r"\bTrump\b", case=True)
df.to_csv('dataset.tsv', sep="\t")

percent_true=df["trump_mention"].value_counts(normalize=True)[True]*100
percent_true = percent_true.round(3)

results = pd.DataFrame([['frac-trump-mentions', percent_true]], columns=['result', 'value'])
results.to_csv('results.tsv', sep="\t")