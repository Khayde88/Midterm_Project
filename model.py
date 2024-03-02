from pydantic import BaseModel


class Track(BaseModel):
    id: int = None
    title: str
    artist: str
    duration: float
    genre: str
