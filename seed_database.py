"""Script to seed the database."""

import os
import json
from random import choice, randint
from datetime import datetime
from model import Movie, Rating, User

import model

from server import app

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(app)
with app.app_context():
    model.db.create_all()

    # Load movie data from JSON file
    with open('data/movies.json') as f:
        movie_data = json.loads(f.read())

    movies_in_db = []
    for movie in movie_data:
        title, overview, poster_path = (
            movie["title"],
            movie["overview"],
            movie["poster_path"]
        )
        release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
        db_movie = Movie.create(title, overview, release_date, poster_path)
        movies_in_db.append(db_movie)

    model.db.session.add_all(movies_in_db)
    model.db.session.commit()

    for n in range(10):
        email = f'user{n}@test.com'  # Voila! A unique email!
        password = 'test'
        
        user = User.create(email, password)
        model.db.session.add(user)

        for _ in range(10):
            random_movie = choice(movies_in_db)
            score = randint(1, 5)

            rating = Rating.create(user, random_movie, score)
            model.db.session.add(rating)

    model.db.session.commit()
