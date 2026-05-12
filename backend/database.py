from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "sqlite:///./musicshelf.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Tabella di collegamento molti-a-molti
album_artists = Table(
    "album_artists",
    Base.metadata,
    Column("album_id", Integer, ForeignKey("albums.id"), primary_key=True),
    Column("artist_id", Integer, ForeignKey("artists.id"), primary_key=True),
)

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(String, nullable=True)

    albums = relationship("Album", secondary=album_artists, back_populates="artists")


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)

    artists = relationship("Artist", secondary=album_artists, back_populates="albums")


def init_db():
    Base.metadata.create_all(bind=engine)