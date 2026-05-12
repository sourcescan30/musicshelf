from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import init_db, SessionLocal, Artist, Album
from schemas import ArtistCreate, ArtistOut, AlbumCreate, AlbumOut
from typing import List
import crud
from musicbrainz import search_albums

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/albums/import")
def import_album(mbid: str, db: Session = Depends(get_db)):
    import musicbrainzngs
    musicbrainzngs.set_useragent("MusicShelf", "0.1", "tuaemail@example.com")

    result = musicbrainzngs.get_release_by_id(mbid, includes=["artists", "release-groups"])
    release = result["release"]

    artists = []
    for credit in release.get("artist-credit", []):
        if isinstance(credit, dict) and "artist" in credit:
            artist_data = credit["artist"]
            existing = db.query(Artist).filter(Artist.name == artist_data["name"]).first()
            if existing:
                artists.append(existing)
            else:
                new_artist = Artist(name=artist_data["name"])
                db.add(new_artist)
                db.commit()
                db.refresh(new_artist)
                artists.append(new_artist)

    genres = release.get("genre-list", [])
    genre_str = None

    db_album = Album(
        title=release["title"],
        year=release.get("date", "")[:4] or None,
        genre=genre_str,
        cover_url=f"https://coverartarchive.org/release/{mbid}/front",
        artists=artists
    )
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

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