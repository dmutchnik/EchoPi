from flask import Flask, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Flask setup
app = Flask(__name__)
CORS(app)

# Spotify setup
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
)

sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route("/api/spotify/current")
def current_track():
    current = sp.current_playback()

    if current and current['is_playing']:
        track = current['item']
        response = {
            "name": track['name'],
            "artists": [artist['name'] for artist in track['artists']],
            "album": track['album']['name'],
            "album_art": track['album']['images'][0]['url'],  # 👈 this line
            "url": track['external_urls']['spotify'],
            "duration": track['duration_ms'] // 1000,
            "volume": current['device']['volume_percent'],
            "progress": current['progress_ms'] // 1000
        }
        return jsonify(response)
    else:
        return jsonify({"message": "Nothing is currently playing."})

from flask import request

@app.route("/api/spotify/control", methods=["POST"])
def control_playback():
    data = request.json
    action = data.get("action")

    try:
        if action == "play":
            sp.start_playback()
        elif action == "pause":
            sp.pause_playback()
        elif action == "next":
            sp.next_track()
        elif action == "previous":
            sp.previous_track()
        else:
            return jsonify({"error": "Invalid action"}), 400

        return jsonify({"status": "success", "action": action})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
