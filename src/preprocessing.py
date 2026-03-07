import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

movies = pd.read_csv("/Users/sushank/Documents/Data_analysis/movie-prediction/data/preprocessed/tmdb_5000_movies.csv")
cast = pd.read_csv("/Users/sushank/Documents/Data_analysis/movie-prediction/data/preprocessed/tmdb_5000_credits.csv")
movies.shape
print(movies.columns)
movies.head(1)
print(cast.columns)
cast.head(1)
cast = cast.rename(columns={"movie_id":"id"})
print(movies.merge(cast, on="title").columns)
merged_movies = movies.merge(cast, on="title")
movies.merge(cast, on="title").head(1)

merged_movies[merged_movies['id_x'] == merged_movies['id_y']].count()
counts = merged_movies.groupby(['id_x', 'id_y']).size().reset_index(name='count')

print(counts)
#ok that means 3 movies got combined it doesnt matter now 
print(merged_movies.columns)
merged_movies.head(1)
#we will keep Genres, id, keywords, (drop all movies other than en), overview, tagline, title_x, cast, crew(directer)
# merged_movies = merged_movies.rename(columns={"title_x": "title"})


merged_movies = merged_movies.drop("homepage", axis=1)
merged_movies.isnull().sum()

merged_movies.dropna(inplace=True)
merged_movies.shape
merged_movies.duplicated().sum()
merged_movies.columns
merged_movies = merged_movies.rename(columns={"id_x": 'id'})
movies_df = merged_movies[["genres", "id", "keywords", "overview", "tagline", "title", "cast", "crew"]]
movies_df.info()
#this is not a list this is a string of a list we need to convert this string into the list somehow
movies_df.iloc[0].genres
import ast
# this will convert string into list properly
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L
movies_df["genres"] = movies_df["genres"].apply(convert)
movies_df.iloc[0].genres
movies_df.head(1)
movies_df.iloc[0].keywords
movies_df["keywords"] = movies_df["keywords"].apply(convert)
movies_df.iloc[0].cast
def convert_cast(obj):
    L = []
    count = 0
    for i in ast.literal_eval(obj):
        if count != 3:
            L.append(i["name"])
        else:
            break
        count += 1
    return L
movies_df["cast"] = movies_df["cast"].apply(convert_cast)
movies_df.head(1)
movies_df.iloc[0].crew
def convert_crew(obj):
    L = []
    for i in ast.literal_eval(obj):
        if(i["department"] == "Directing"):
            L.append(i["name"])
            break
    return L
movies_df["crew"] = movies_df["crew"].apply(convert_crew)
movies_df.head(1)
movies_df['overview'] = movies_df['overview'].apply(lambda x: x.split())
movies_df['tagline'] = movies_df['tagline'].apply(lambda x: x.split())

movies_df.head(1)
movies_df.to_csv("Listed_features.csv",index=False)
movies_df["genres"] = movies_df["genres"].apply(lambda x: [i.replace(" ", "") for i in x])
movies_df["keywords"] = movies_df["keywords"].apply(lambda x: [i.replace(" ", "") for i in x])
movies_df["overview"] = movies_df["overview"].apply(lambda x: [i.replace(" ", "") for i in x])
movies_df["tagline"] = movies_df["tagline"].apply(lambda x: [i.replace(" ", "") for i in x])
movies_df["cast"] = movies_df["cast"].apply(lambda x: [i.replace(" ", "") for i in x])
movies_df["crew"] = movies_df["crew"].apply(lambda x: [i.replace(" ", "") for i in x])
movies_df.head()
movies_df["tags"] = movies_df["genres"]+ movies_df["keywords"]+ movies_df["tagline"] + movies_df["overview"]+ movies_df["cast"]+ movies_df["crew"]
movies_df.head(1)
new_df = movies_df[["id", "title", "tags"]]
new_df.head(1)
new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))
new_df.head(1)
new_df["tags"][0]
new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())
new_df.to_csv("final_features_with_tags.csv", index=False)
