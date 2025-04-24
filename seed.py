from datetime import datetime
from models import Genre, Movie
from database import Base, engine, get_db

with get_db().__next__() as session:

  # Создание и удаление таблиц
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)

  # Создание жанров
  genres = [
    Genre(name="Боевик", description="Фильмы с динамичными сценами борьбы и погонями."),
    Genre(name="Комедия", description="Юмористические фильмы, предназначенные для развлечения."),
    Genre(name="Драма", description="Фильмы с глубоким эмоциональным сюжетом."),
    Genre(name="Фантастика", description="Фильмы о будущем, технологиях и космосе."),
    Genre(name="Ужасы", description="Фильмы, предназначенные напугать зрителя."),
    Genre(name="Мелодрама", description="Романтические истории с эмоциональным накалом."),
    Genre(name="Триллер", description="Фильмы с напряженным, захватывающим сюжетом."),
  ]

  session.add_all(genres)
  session.commit()

  # Список фильмов
  movies_data = [
    {
      "title": "Крепкий орешек",
      "year": 1988,
      "duration": 132,
      "rating": 8.2,
      "description": "Полицейский пытается спасти людей, захваченных террористами в небоскребе.",
      "poster_url": "https://example.com/posters/die_hard.jpg",
      "genres": ["Боевик", "Триллер"]
    },
    {
      "title": "Назад в будущее",
      "year": 1985,
      "duration": 116,
      "rating": 8.5,
      "description": "Подросток случайно отправляется в прошлое на машине времени.",
      "poster_url": "https://example.com/posters/back_to_future.jpg",
      "genres": ["Фантастика", "Комедия"]
    },
    {
      "title": "Король Лев",
      "year": 1994,
      "duration": 88,
      "rating": 8.8,
      "description": "Мультфильм о львенке Симбе, который становится королем саванны.",
      "poster_url": "https://example.com/posters/lion_king.jpg",
      "genres": ["Драма", "Мелодрама"]
    },
    {
      "title": "Оно",
      "year": 2017,
      "duration": 135,
      "rating": 7.3,
      "description": "Группа детей сталкивается с древним злом в маленьком городке.",
      "poster_url": "https://example.com/posters/it.jpg",
      "genres": ["Ужасы"]
    },
    {
      "title": "Титаник",
      "year": 1997,
      "duration": 194,
      "rating": 7.8,
      "description": "История любви на фоне гибели легендарного корабля.",
      "poster_url": "https://example.com/posters/titanic.jpg",
      "genres": ["Драма", "Мелодрама"]
    },
    {
      "title": "Матрица",
      "year": 1999,
      "duration": 136,
      "rating": 8.7,
      "description": "Хакер узнает, что реальность — это симуляция.",
      "poster_url": "https://example.com/posters/matrix.jpg",
      "genres": ["Фантастика", "Боевик"]
    },
    {
      "title": "Джокер",
      "year": 2019,
      "duration": 122,
      "rating": 8.4,
      "description": "История становления одного из самых известных злодеев комиксов.",
      "poster_url": "https://example.com/posters/joker.jpg",
      "genres": ["Драма", "Триллер"]
    }
  ]

  # Добавление фильмов
  for movie_data in movies_data:
    movie = Movie(
      title=movie_data["title"],
      year=movie_data["year"],
      duration=movie_data["duration"],
      rating=movie_data["rating"],
      description=movie_data["description"],
      poster_url="/static/posters/29ee4053-355c-4bd7-a04a-1907482ccde0.jpg",
      create_at=datetime.now()
    )

    # Привязка жанров
    for genre_name in movie_data["genres"]:
      genre = session.query(Genre).filter_by(name=genre_name).first()

      if genre:
        movie.genres.append(genre)
    
    session.add(movie)

  session.commit()
  print("Данные успешно добавлены в базу!")

