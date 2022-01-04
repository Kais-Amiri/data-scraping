import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob



df = pd.read_csv('./glassdoor_reviews.csv')


sentiments_pro =[]
sentiments_con =[]
sentiments_advice =[]

for i in df.index:
    blob_pro = TextBlob(str(df["pro"].iloc[i]))
    sentiment_pro = blob_pro.sentiment.polarity
    sentiments_pro.append(sentiment_pro)

    blob_con = TextBlob(str(df["con"].iloc[i]))
    sentiment_con = blob_con.sentiment.polarity
    sentiments_con.append(sentiment_con)

    blob_advice = TextBlob(str(df["advice"].iloc[i]))
    sentiment_advice = blob_advice.sentiment.polarity
    sentiments_advice.append(sentiment_advice)

sentiments = {
    'sentiments pros': sentiments_pro,
    'sentiments cons': sentiments_con,
    'sentiments advice': sentiments_advice,
}

df = pd.DataFrame(sentiments)
df.to_csv('./sentiments_analys_glassdoor_reviews.csv', index=True, encoding='utf-8')

sbn.displot(data=df, kind="kde")

plt.show()