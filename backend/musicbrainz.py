import musicbrainzngs

musicbrainzngs.set_useragent("MusicShelf", "0.1", "tuaemail@example.com")

def search_albums(query: str):
    result = musicbrainzngs.search_releases(query=query, limit=10)
    albums = []
    for release in result["release-list"]:
        albums.append({
            "mbid": release.get("id"),
            "title": release.get("title"),
            "year": release.get("date", "")[:4] or None,
            "artist": release.get("artist-credit-phrase", "Unknown"),
            "cover_url": f"https://coverartarchive.org/release/{release.get('id')}/front" 
        })
    return albums