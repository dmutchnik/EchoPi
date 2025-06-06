from datetime import datetime
from flask import Flask, render_template
from flask_cors import CORS
from echopi.weather import (
    open_meteo_weather, weather_emoji,
    time_of_day, time_string, date_string
)
from echopi.spotify.routes import bp as spotify_bp

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
