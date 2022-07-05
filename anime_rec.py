import os
import numpy as np
import pandas as pd
import warnings
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity

#code from kaggle 
#https://www.kaggle.com/code/yonatanrabinovich/anime-recommendations-project/notebook

pd.options.display.max_columns

#warning hadle
warnings.filterwarnings("always")
warnings.filterwarnings("ignore")
# rating_path = "/CodeProject/AnimeRecommending/rating.csv"
# anime_path = "/CodeProject/AnimeRecommending/anime.csv"
rating_path = "/CodeProject/Anime/rating.csv"
anime_path = "/CodeProject/Anime/anime.csv"
rating_df = pd.read_csv(rating_path)
# print(rating_df.head())

anime_df=pd.read_csv(anime_path)
# print(anime_df.head())

anime_df=anime_df[~np.isnan(anime_df["rating"])]

# filling mode value for genre and type
anime_df['genre'] = anime_df['genre'].fillna(
anime_df['genre'].dropna().mode().values[0])

anime_df['type'] = anime_df['type'].fillna(
anime_df['type'].dropna().mode().values[0])

#checking if all null values are filled
# print(anime_df.isnull().sum())

rating_df['rating'] = rating_df['rating'].apply(lambda x: np.nan if x==-1 else x)

anime_df = anime_df[anime_df['type']=='TV']

#step 2
rated_anime = rating_df.merge(anime_df, left_on = 'anime_id', right_on = 'anime_id', suffixes= ['_user', ''])

#step 3
rated_anime =rated_anime[['user_id', 'name', 'rating']]

#step 4
rated_anime_7500= rated_anime[rated_anime.user_id <= 7500]

pivot = rated_anime_7500.pivot_table(index=['user_id'], columns=['name'], values='rating')

pivot_n = pivot.apply(lambda x: (x-np.mean(x))/(np.max(x)-np.min(x)), axis=1)

# step 2
pivot_n.fillna(0, inplace=True)

# step 3
pivot_n = pivot_n.T

# step 4
pivot_n = pivot_n.loc[:, (pivot_n != 0).any(axis=0)]

# step 5
piv_sparse = sp.sparse.csr_matrix(pivot_n.values)

anime_similarity = cosine_similarity(piv_sparse)

#Df of anime similarities
ani_sim_df = pd.DataFrame(anime_similarity, index = pivot_n.index, columns = pivot_n.index)

def anime_recommendation(ani_name):
    number = 1
    animeList=[]
    # print('Recommended because you watched {}:\n'.format(ani_name))
    for anime in ani_sim_df.sort_values(by = ani_name, ascending = False).index[1:6]:
        # print(f'#{number}: {anime}, {round(ani_sim_df[anime][ani_name]*100,2)}% match')
        animeList.append(anime)
        number +=1 
    print(animeList)
    return animeList
# anime_recommendation('Overlord') 