from flask import Flask, render_template, request
import pickle

movie_list = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Optional: Normalize movie titles to lower case for easier matching
movie_list['title_normalized'] = movie_list['title'].str.strip().str.lower()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    movie_name = request.form['movie_name'].strip().lower()
    filtered_movies = movie_list[movie_list['title_normalized'] == movie_name]

    if filtered_movies.empty:
        error_message = f"Movie '{movie_name}' not found in the dataset."
        return render_template("index.html", error=error_message)

    movie_index = filtered_movies.index[0]
    distances = similarity[movie_index]
    selected_movie = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended = [movie_list.iloc[i[0]].title for i in selected_movie]
    
    return render_template("index.html", movies=recommended)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
