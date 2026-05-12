from sqlalchemy.orm import Session
from database import Artist, Album
from schemas import ArtistCreate, AlbumCreate

def create_artist(db: Session, artist: ArtistCreate):
    db_artist = Artist(name=artist.name, bio=artist.bio)
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def get_artists(db: Session):
    return db.query(Artist).all()

def create_album(db: Session, album: AlbumCreate):
    artists = db.query(Artist).filter(Artist.id.in_(album.artist_ids)).all()
    db_album = Album(
        title=album.title,
        year=album.year,
        genre=album.genre,
        cover_url=album.cover_url,
        artists=artists,
    )
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

def get_albums(db: Session):
    return db.query(Album).all()