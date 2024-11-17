from flask import Flask, render_template,request
import pickle

movie_list = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    movie_name = request.form['movie_name']
    movie_index = movie_list[movie_list['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    selected_movie = sorted(list(enumerate(distances)),reverse = True, key = lambda x : x[1])[1:6]
    l = []

    for i in selected_movie:
        l.append(movie_list.iloc[i[0]].title)

    
    return render_template("index.html", movies = l)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
