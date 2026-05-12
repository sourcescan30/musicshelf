from pydantic import BaseModel
from typing import Optional, List

class ArtistBase(BaseModel):
    name: str
    bio: Optional[str] = None

class ArtistCreate(ArtistBase):
    pass

class ArtistOut(ArtistBase):
    id: int

    class Config:
        from_attributes = True

class AlbumBase(BaseModel):
    title: str
    year: Optional[int] = None
    genre: Optional[str] = None
    cover_url: Optional[str] = None

class AlbumCreate(AlbumBase):
    artist_ids: List[int] = []

class AlbumOut(AlbumBase):
    id: int
    artists: List[ArtistOut] = []

    class Config:
        from_attributes = True