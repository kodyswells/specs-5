"""Models for movie ratings app."""
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # ratings = a list of Rating objects

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

    @classmethod
    def create(cls, email, password):
       """Create and return a new user."""

       return cls(email=email, password=password)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()


class Movie(db.Model):
    """A movie."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)

    # ratings = a list of Rating objects

    def __repr__(self):
        return f"<Movie movie_id={self.movie_id} title={self.title}>"

    @classmethod
    def create(cls, title, overview, release_date, poster_path):
        """Create and return a new movie."""

        return cls(
            title=title,
            overview=overview,
            release_date=release_date,
            poster_path=poster_path,
            )
    @classmethod
    def all_movies(cls):
        """Return all movies."""

        return cls.query.all()

    @classmethod
    def get_by_id(cls, movie_id):
        """Return a movie by primary key."""

        return cls.query.get(movie_id)
class Rating(db.Model):
    """A movie rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    movie = db.relationship("Movie", backref="ratings")
    user = db.relationship("User", backref="ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"

    @classmethod
    def create(cls, user, movie, score):
        """Create and return a new movie."""

        return cls(user=user, movie=movie, score=score)

    @classmethod
    def update(cls, rating_id, new_score):
        """ Update a rating given rating_id and the updated score. """
        rating = cls.query.get(rating_id)
        rating.score = new_score


def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
