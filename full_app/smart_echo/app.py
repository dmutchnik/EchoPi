from datetime import datetime
from flask import Flask, render_template
from flask_cors import CORS
from echopi.weather import (
    open_meteo_weather, weather_emoji,
    time_of_day, time_string, date_string
)
from echopi.spotify.routes import bp as spotify_bp
import requests
import threading
from time import sleep

URL_READ_COMMANDS = "https://ntfy.sh/newCommandFromEchoPi/raw"

app = Flask(__name__, template_folder="templates")
app.register_blueprint(spotify_bp)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def index():
    now     = datetime.now()
    weather = open_meteo_weather(40.1163, -88.2435)
    wemoji  = weather_emoji(weather)
    return render_template("index.html",
                           time=time_string(now),
                           date_string=date_string(now),
                           time_of_day=time_of_day(now),
                           temperature_f=weather["temp_F"],
                           weather_emoji=wemoji[0],
                           weather_type=wemoji[1])



def listen_to_stream():
    """
    Listen to a stream of messages from the ntfy.sh service.
    Manage the calls to the api.
    """
    resp = requests.get(URL_READ_COMMANDS, stream=True)
    for line in resp.iter_lines():
        if line:
            # Code that checks the message and calls the api 
            line_decoded = line.decode()
            match line_decoded:
                case "play":
                    print("[Message] Play command received")
                case "pause":
                    print("[Message] Pause command received")
                case "next":
                    print("[Message] Next command received")
                case "previous":
                    print("[Message] Previous command received")
                case _:
                    print(f"[Message] Unknown command: {line_decoded}")

def send_current_song():
    """
    Send the current title of the song to the ntfy.sh service.
    """
    pass


if __name__ == "__main__":

    thread = threading.Thread(target=listen_to_stream, daemon=True)
    thread.start()
    counter = 0

    app.run(host="0.0.0.0", port=5000, debug=True)
