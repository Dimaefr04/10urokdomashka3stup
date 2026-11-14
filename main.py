from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

movies = [
    {"id": 1, "title": "1+1", "director": "Оливьен Акаш", "year": 2011},
    {"id": 2, "title": "Во все тяжкие", "director": "Мишель Макларен", "year": 2008},
]

class MovieCreate(BaseModel):
    title: str = Field(min_length=2)
    director: str = Field(min_length=2)
    year: int = Field(ge=1900, le=2030)

@app.get("/movies")
def get_movies():
    return movies

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for m in movies:
        if m["id"] == movie_id:
            return m
    raise HTTPException(status_code=404, detail="Фильм не найден")

@app.post("/movies", status_code=201)
def add_movie(movie: MovieCreate):
    for m in movies:
        if m["title"].lower() == movie.title.lower():
            raise HTTPException(status_code=400, detail="Фильм с таким названием уже есть")

    new_id = len(movies) + 1
    new_movie = {"id": new_id, "title": movie.title, "director": movie.director, "year": movie.year}
    movies.append(new_movie)
    return new_movie