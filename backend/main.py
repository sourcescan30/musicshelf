from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import init_db, SessionLocal
from schemas import ArtistCreate, ArtistOut, AlbumCreate, AlbumOut
from typing import List
import crud
from musicbrainz import search_albums

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "MusicShelf API is alive"}

@app.get("/search")
def search(q: str):
    return search_albums(q)

@app.post("/artists", response_model=ArtistOut)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    return crud.create_artist(db, artist)

@app.get("/artists", response_model=List[ArtistOut])
def get_artists(db: Session = Depends(get_db)):
    return crud.get_artists(db)

@app.post("/albums", response_model=AlbumOut)
def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    return crud.create_album(db, album)

@app.get("/albums", response_model=List[AlbumOut])
def get_albums(db: Session = Depends(get_db)):
    return crud.get_albums(db)
