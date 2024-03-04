# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from model import Track

app = FastAPI()

# Enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the "frontend" folder to serve styles.css and index.html
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Define a route for the root URL to serve the index.html file
@app.get("/", response_class=HTMLResponse, name="Get Index")
async def read_root():
    return FileResponse("frontend/index.html")


# Mock database
music_tracks = [
    Track(
        id=1,
        title="Sample Track 1",
        artist="Sample Artist 1",
        duration=3,
        genre="Pop",
    ),
    Track(
        id=2,
        title="Sample Track 2",
        artist="Sample Artist 2",
        duration=4.3,
        genre="Rock",
    ),
    Track(
        id=3,
        title="Sample Track 3",
        artist="Sample Artist 3",
        duration=3.2,
        genre="Hip-Hop",
    ),
    Track(
        id=4,
        title="Sample Track 4",
        artist="Sample Artist 4",
        duration=3.5,
        genre="Country",
    ),
    # Can add more tracks
]


@app.post("/tracks/", response_model=Track)
def create_track(track: Track):
    # Generate a unique ID for the new track
    track.id = len(music_tracks) + 1
    music_tracks.append(track)
    return track


@app.get("/tracks/", response_model=List[Track])
def read_tracks():
    return music_tracks


@app.get("/tracks/{track_id}", response_model=Track)
def read_track(track_id: int):
    track = next((t for t in music_tracks if t.id == track_id), None)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@app.put("/tracks/{track_id}", response_model=Track)
def update_track(track_id: int, updated_track: Track):
    track_index = next(
        (i for i, t in enumerate(music_tracks) if t.id == track_id), None
    )
    if track_index is None:
        raise HTTPException(status_code=404, detail="Track not found")

    # Update the track with the new information
    music_tracks[track_index] = updated_track
    return updated_track


@app.delete("/tracks/{track_id}", response_model=Track)
def delete_track(track_id: int):
    track_index = next(
        (i for i, t in enumerate(music_tracks) if t.id == track_id), None
    )
    if track_index is None:
        raise HTTPException(status_code=404, detail="Track not found")

    deleted_track = music_tracks.pop(track_index)
    return deleted_track
