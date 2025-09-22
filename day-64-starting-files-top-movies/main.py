import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from wtforms import FloatField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, NumberRange

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

TMDB_API_KEY = os.getenv("DAY_64_STARTING_FILES_TOP_MOVIES_TMDB_API_KEY")

app = Flask(__name__)
Bootstrap5(app)

# CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top-ten-movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialise DB
db = SQLAlchemy(app)


# WTFORM
class EditForm(FlaskForm):
    rating = FloatField("Your Rating out of 10", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = TextAreaField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Update")


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"


# new_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully "
#                 "family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go "
#                 "to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )

with app.app_context():
    db.create_all()
    # existing_movie = db.session.query(Movie).filter_by(title=new_movie.title).first()
    # if not existing_movie:
    #     db.session.add(new_movie)
    #     db.session.commit()


# ROUTES
@app.route("/")
def home():
    result = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc())
    )
    all_movies = result.scalars().all()

    for i, movie in enumerate(all_movies, start=1):
        movie.ranking = i
    db.session.commit()

    return render_template("index.html", all_movies=all_movies)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    movie = db.get_or_404(Movie, id)
    form = EditForm(obj=movie)
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))



@app.route("/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        movie_title = request.form.get("title")
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={
                "api_key": TMDB_API_KEY,
                "query": movie_title,
            }
        )
        data = response.json()["results"]
        return render_template("select.html", movies=data)  # Show choices
    return render_template("add.html")


@app.route("/find/<int:movie_id>")
def find_movie(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}",
        params={"api_key": TMDB_API_KEY, "language": "en-US"}
    )
    movie_data = response.json()
    # At this point, you can create a new Movie object and add to DB
    # Or render another page to confirm details
    return render_template("movie_detail.html", movie=movie_data)


@app.route("/add_to_database/<int:movie_id>", methods=["POST"])
def add_to_database(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}",
        params={"api_key": TMDB_API_KEY, "language": "en-US"}
    )
    movie_data = response.json()

    new_movie = Movie(
        title=movie_data["title"],
        year=int(movie_data.get("release_date", "0000").split("-")[0]) if movie_data.get("release_date") else None,
        description=movie_data.get("overview", "No description available"),
        rating=0.0,  # default placeholder
        ranking=0,  # will be updated later
        review="Not reviewed yet",  # placeholder
        img_url=f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data.get("poster_path") else ""
    )

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
