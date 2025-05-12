from flask import Blueprint, jsonify, request
import os, spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
bp = Blueprint("spotify", __name__, url_prefix="/api/spotify")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id     = os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri  = os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"))

@bp.get("/current")
def current_track():
    cur = sp.current_playback()
    if cur and cur["is_playing"]:
        t = cur["item"]
        return jsonify(
            name=t["name"],
            artists=[a["name"] for a in t["artists"]],
            album=t["album"]["name"],
            album_art=t["album"]["images"][0]["url"],
            url=t["external_urls"]["spotify"],
            duration=t["duration_ms"]//1000,
            volume=cur["device"]["volume_percent"],
            progress=cur["progress_ms"]//1000,
        )
    return jsonify(message="Nothing is playing")

@bp.post("/control")
def control():
    action = request.json.get("action")
    match action:
        case "play":     sp.start_playback()
        case "pause":    sp.pause_playback()
        case "next":     sp.next_track()
        case "previous": sp.previous_track()
        case _:          return jsonify(error="invalid action"), 400
    return jsonify(status="ok", action=action)