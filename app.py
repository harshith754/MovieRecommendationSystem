from flask import Flask,render_template, redirect, request,jsonify, url_for
import pickle
import pandas as pd
import imdb
import json

app = Flask(__name__)
# Load Files
movies_dict = pickle.load(open("static/movies_dict.pkl", "rb"))

info_dict = pickle.load(open("static/info_dict.pkl", "rb"))
similarity = pickle.load(open("static/similarity.pkl", "rb"))

movies=pd.DataFrame(movies_dict)
info=pd.DataFrame(info_dict)
ia = imdb.IMDb()

def recommendMovies(movie):
    movie_index=movies[movies['movie title']==movie].index[0]

    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]

    for i in movies_list:
      recommended_movies.append(movies['movie title'][i[0]])
    return recommended_movies

movie_name_list = movies['movie title'].values.tolist()

@app.route('/', methods=['GET', 'POST'])
def initial_page():
    print(movie_name_list)
    if request.method == 'POST':
        # Perform some processing when the button is clicked
        # Redirect to the recommended route after processing
        return redirect('/recommend')
    return render_template('homepage.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        # Get the movie name from the form input
        movie_name = request.form['movie_name']
        print("I got",movie_name)

        recommended_movies=  recommendMovies(movie_name)
        # Replace this with your own recommendation logic

        # Render the recommendation result template
        return render_template('recommendations.html', movie_recommendations=recommended_movies)

    movies_df = movies['movie title'].to_frame().reset_index()  # Convert Series to DataFrame
    movies_list = movies_df.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
    movies_json = json.dumps(movies_list)  # Serialize movies list to JSON
    return render_template('recommend.html',movie_name_list=movie_name_list)


@app.route('/recommendations',methods=['POST'])
def fin1():
    return redirect(url_for('initial_page'))
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search_term = request.args.get('term', '')  # Get the search term from request arguments
    movies_list = movie_name_list  # Fetch all movies from the database or data source

    # Filter the movies list based on the search term
    matching_movies = [movie for movie in movies_list if search_term.lower() in movie.lower()]

    return jsonify(matching_movies)


if __name__ == "__main__":
    app.run(debug=True, port=8000)