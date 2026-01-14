from pydantic import BaseModel

class MovieItem(BaseModel):
    movie_name: str
    rating: float | None = None

class GenreItem(BaseModel):
    genre: str
    count: int

class CountItem(BaseModel):
    total: int

class MovieStats(BaseModel):
    movie_name: str
    views: int
    avg_rating: float

