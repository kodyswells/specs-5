"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db, User, Movie, Rating
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key="dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    return render_template('homepage.html')
    
@app.route('/movies')
def all_movies():
    movies = Movie.all_movies()

    return render_template('all_movies.html', movies = movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = Movie.get_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def all_users():
    users = User.all_users()

    return render_template('all_users.html', users = users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)
    if user:
        flash("User already exists. Please log in.")
    else:
        new_user = User.create(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route('/users/<user_id>')
def show_user(user_id):
    user = User.get_by_id(user_id)

    return render_template('user_details.html', user = user)

@app.route('/login', methods=["POST"])
def login_user():
    """Log in a user."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)

    if user and user.password == password:
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.email}!")
        return redirect("/movies")
    else:
        flash("Invalid email or password.")
        return redirect("/")
    
@app.route('/movies/<movie_id>', methods=["POST"])
def submit_rating(movie_id):
    """Lets a user submit a rating for the movie"""
    
    user_id = session.get("user_id")
    score = request.form.get("score")

    if not user_id:
        flash("You need to log in to rate movies.")
        return redirect("/login")

    user = User.get_by_id(user_id)
    movie = Movie.get_by_id(movie_id)

    if not movie:
        flash("Movie not found.")
        return redirect("/movies")

    try:
        score = int(score)
    except ValueError:
        flash("Invalid score. Please enter an integer between 1 and 5.")
        return redirect(f"/movies/{movie_id}")

    if score < 1 or score > 5:
        flash("Invalid score. Please enter an integer between 1 and 5.")
        return redirect(f"/movies/{movie_id}")

    rating = Rating.create(user, movie, score)

    db.session.add(rating)
    db.session.commit()

    flash("Rating submitted!")
    return redirect(f"/movies/{movie_id}")




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
