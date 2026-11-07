from flask import Flask, render_template,request
from model import moviess,recommend
import pandas as pd 




app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home(): 
    name = ""
    movie_name = ""
    searched = False
    if request.method == "POST":
        searched = True
        movie = request.form.get("name")
        if movie in moviess:
            name,movie_name = recommend(movie)
        else:
            name = "movie not found"
        
    return render_template(
    "index.html",
    movies=moviess,
    searched = searched ,
    result = name,
    movie_name = movie_name )

if __name__ == "__main__":
    app.run(debug=True)

