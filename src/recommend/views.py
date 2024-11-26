import pickle
from django.http import JsonResponse
import pandas as pd
from surprise import Dataset, Reader, SVD

# Load the trained SVD model from the file
with open('recommend/svd_model.pkl', 'rb') as file:
    svd_model = pickle.load(file)

# Load the ratings dataframe (user_id, movie_id, rating) for collaborative filtering
ratings_df = pd.read_csv('recommend/my_dataframe.csv')
movies_df = pd.read_csv('recommend/my_movie.csv')

# Reader object for surprise dataset
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['user_id', 'movie_id', 'rating']], reader)
trainset = data.build_full_trainset()
svd_model.fit(trainset)

#  function to get movie recommendations
def get_top_n_recommendations(user_id, n=5):
    all_movie_ids = ratings_df['movie_id'].unique()
    rated_movies = ratings_df[ratings_df['user_id'] == user_id]['movie_id'].tolist()

    predictions = [
        (movie_id, svd_model.predict(user_id, movie_id).est)
        for movie_id in all_movie_ids if movie_id not in rated_movies
    ]
    predictions.sort(key=lambda x: x[1], reverse=True)


    return predictions[:n]

def recommend(request, id):
    user_id = id

    recommendations = get_top_n_recommendations(user_id)
    
    
    movie_dict = pd.Series(movies_df.movie_title.values, index=movies_df.movie_id).to_dict()

    # Prepare the recommendations with movie titles
    recommendations_with_names = [
        {"movie_id": int(movie_id), "title": movie_dict.get(movie_id, "Unknown Movie"), "predicted_rating": rating}
        for movie_id, rating in recommendations
    ]
    
    # Return the recommendations in JSON format
    return JsonResponse({'user_id': user_id, 'recommendations': recommendations_with_names})
