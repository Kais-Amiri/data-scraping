import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from collections import defaultdict



def cosine_smlrty(df_colum, colum_name):

    parse_review=[]

    for i in range(len(df_colum)):

            parse_review.append(df_colum[i])

    # Create the Document Term Matrix
    count_vectorizer = CountVectorizer(stop_words='english')
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(parse_review)
    # Convert Sparse Matrix to DF
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix,columns=count_vectorizer.get_feature_names()) 

    dj=pd.DataFrame(cosine_similarity(df, dense_output=True))

    #save cosine similarity dataframe
    dj.to_csv('cosine_similarity_'+colum_name+'.csv', index=True, encoding='utf-8')



    # match the similar text
    t=[]

    for j,k in enumerate(dj.values):
        for n in range(len(k)):
            t.append([j,n,k[n]])

    qq=[]
    for i in range(len(t)):
        if t[i][0]==t[i][1]:
            qq.append([t[i][0],t[i][1],0])
        else:
            qq.append(t[i])


    u=defaultdict(list)

    for i in range(len(qq)):
        u[qq[i][0]].append(qq[i][2])
    
    updated_df=pd.DataFrame(u)

    position_maxVal=[]
    for i in range(len(updated_df)):
        position_maxVal.append(np.argmax(updated_df[i]))


    high_sim=[]
    # list of highest similarity index positions
    for j in position_maxVal:
    # this creates in order our highest similiarity by row    
        high_sim.append(parse_review[j])


    # review based on highest similarity value per row as DF
    similar_review_=pd.DataFrame(high_sim,columns=['Similar review'])

    # similiarity values rounded 4 decimal places finding max value per row
    similarity_value_=pd.DataFrame(round(updated_df.max(axis=1),4),columns=['Similarity Value'])

    # review 
    p_review=pd.DataFrame(parse_review,columns=['Parsed review'])

    # put everything together
    cosine_sim_df=pd.concat([p_review,similar_review_,similarity_value_],axis=1)

    cosine_sim_df.to_csv(colum_name+'_similar'+'.csv', index=True, encoding='utf-8')



if __name__ == '__main__':

    df = pd.read_csv('glassdoor_reviews.csv')
    pros = df["pro"]
    cons = df["con"]
    advices = df["advice"]

    cosine_smlrty(pros, "pros")
    cosine_smlrty(cons, "cons")
    cosine_smlrty(advices, "advices")