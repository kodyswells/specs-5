"""CRUD operations"""

from model import db, User, Movie, Rating, connect_to_db

"""Functions Below"""

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def create_movie(title, overview, release_date, poster_path):
    """Create a movie"""

    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    return movie

def get_movie():
    return Movie.query.all()

def get_movie_by_id(movie_id):
    return Movie.query.get(movie_id)

def get_user():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_rating(user, movie, score):
    """Create and return a new rating."""

    rating = Rating(user=user, movie=movie, score=score)

    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)