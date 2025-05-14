import requests
import flask

URL_READ_COMMANDS = "https://ntfy.sh/newCommandFromEchoPi/raw"

def listen_to_stream(app: flask.Flask):
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
                        print("[Message] Play")
                        app.post("/api/spotify/control", json={"action": "play"})
                case "pause":
                        print("[Message] Pause")
                        app.post("/api/spotify/control", json={"action": "pause"})
                case "next":
                        print("[Message] Next")
                        app.post("/api/spotify/control", json={"action": "next"})
                case "previous":
                        print("[Message] Previous")
                        app.post("/api/spotify/control", json={"action": "previous"})
                case _:
                    print(f"[Message] Unknown command: {line_decoded}")

if __name__ == "__main__":
    listen_to_stream()