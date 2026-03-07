from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
cv =CountVectorizer(max_features=5000, stop_words="english")
df = pd.read_csv("/Users/sushank/Documents/Data_analysis/movie-prediction/data/processed/final_features_with_tags.csv")
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
def stem(obj):
    y = [] 
    for i in obj.split():
        y.append(ps.stem(i))
    return " ".join(y)
df['tags'] = df['tags'].apply(stem)
vectors = cv.fit_transform(df["tags"]).toarray()
cv.get_feature_names_out()
from sklearn.metrics.pairwise import cosine_similarity
cosine_similarity(vectors)[0] #har movie ka har movie k sath cosine dist( angle )
df[df["title"] == "Avatar"].index[0]
similarity_mat = cosine_similarity(vectors)
list(enumerate(similarity_mat[0]))
#index with similarty usefull for sorting

sorted(list(enumerate(similarity_mat[0])), reverse=True, key = lambda x : x[1])[1:6] #excluding the first(itself)
def recommend(movie):
    movie_index = df[df["title"] == movie].index[0]
    movie_list_title = []
    distances = similarity_mat[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x : x[1])[1:6] #excluding the first(itself)
    for i in movie_list:
        print(df.iloc[i[0]].title)

recommend("Iron Man")
import pickle

pickle.dump(df, open("movies.pkl","wb"))
pickle.dump(similarity_mat, open("similarity.pkl","wb"))
pickle.dump(cv, open("vectorizer.pkl","wb"))
