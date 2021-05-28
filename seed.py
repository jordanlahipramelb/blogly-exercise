"""Seed file to make sample data for db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Make a bunch of Users
steve = User(first_name="Steve", last_name="Rogers", image_url="https://i.redd.it/fh0y9uxn11t61.jpg")
tony = User(
    first_name="Tony",
    last_name="Stark",
    image_url="https://dailysuperheroes.com/wp-content/uploads/2020/02/tony-stark.jpg",
)
thor = User(
    first_name="Thor",
    last_name="Odinson",
    image_url="https://cdn.vox-cdn.com/thumbor/dvMjjuYxDWDh0E9bZGOrx7ZtJP8=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/9490719/thor_big.jpg",
)
bruce = User(
    first_name="Bruce",
    last_name="Banner",
    image_url="https://www.pinkvilla.com/files/styles/contentpreview/public/avengers-endgame-star-mark-ruffalo-celebrates-bruce-banners-50th-birthday-with-an-endearing-post.jpg?itok=oMFtARBs",
)
natasha = User(
    first_name="Natasha",
    last_name="Romanoff",
    image_url="https://pbs.twimg.com/profile_images/1122956085604827136/xo9p7XOS_400x400.jpg",
)

db.session.add_all([steve, tony, bruce, thor, natasha])

db.session.commit()
