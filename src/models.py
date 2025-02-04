from dataclasses import dataclass , field
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

@dataclass
class Users(db.Model):
    __tablename__ = 'users'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    name:str = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Users(id={self.id}, name={self.name})>'

class FavouritesType(str, enum.Enum):
    SPECIES = "SPECIES"
    PLANETS = "PLANETS"
    PEOPLE = "PEOPLE"

@dataclass
class Favourites(db.Model):
    __tablename__ = 'favourites'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    user_id:int = db.Column(db.Integer, ForeignKey('users.id'),index=True, nullable=False)
    external_id:int = db.Column(db.Integer, nullable=False)
    type:FavouritesType = db.Column(db.Enum(FavouritesType), nullable=False)
    name:str = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Favorites(id={self.id}, user_id={self.user_id}, name={self.name}, type={self.type})>'

@dataclass
class Species(db.Model):
    __tablename__ = 'species'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    description:str = db.Column(db.String(250), nullable=False)
    name:str = db.Column(db.String(30), nullable=False)
    homeworld:int = db.Column(db.Integer, ForeignKey('planets.id'), nullable=False)

    def __repr__(self):
        return f'<Species(uid={self.id}, name={self.name}, homeworld={self.homeworld})>'

@dataclass
class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    name:str = db.Column(db.String(30), nullable=False)
    gravity:str = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Planets(uid={self.id}, name={self.name}, gravity={self.gravity})>'

@dataclass
class People(db.Model):
    __tablename__ = 'people'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    description:str = db.Column(db.String(50), nullable=False)
    name:str = db.Column(db.String(30), nullable=False)
    homeworld:int = db.Column(db.Integer, ForeignKey('planets.id'), nullable=False)

    def __repr__(self):
        return f'<People(uid={self.id}, name={self.name}, homeworld={self.homeworld})>'