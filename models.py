from sqlalchemy import Column, Integer, String, Float, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from sqlalchemy.sql import func


# Связь многие-ко-многим Genre <-> Movie
movie_genre = Table(
  'movie_genre',
  Base.metadata,
  Column('movie_id', Integer, ForeignKey('movies.id')),
  Column('genre_id', Integer, ForeignKey('genres.id'))
)


class Genre(Base):
  __tablename__ = 'genres'

  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False, unique=True)
  description = Column(String(200))

  movies = relationship("Movie", secondary=movie_genre, back_populates="genres")

  def __repr__(self):
    return f"<Genre(id={self.id}, name='{self.name}')>"


class Movie(Base):
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String(100), nullable=False)
  year = Column(Integer)
  duration = Column(Integer)
  rating = Column(Float)
  description = Column(String(500))
  poster_url = Column(String(200))
  create_at = Column(DateTime, default=datetime.now())

  genres = relationship("Genre", secondary=movie_genre, back_populates="movies")

  def __repr__(self):
    return f"<Movie(id={self.id}, title='{self.title}', year={self.year})>"


class User(Base):
  __tablename__ = "users"

  id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
  username = Column(String(60), nullable=False, unique=True)
  password_hash = Column(String(255), nullable=False)
  email = Column(String(255), nullable=True)
  created_at = Column(DateTime(), server_default=func.now())

  def __repr__(self):
    return f"<User(id={self.id}, title='{self.username}')>"
    
