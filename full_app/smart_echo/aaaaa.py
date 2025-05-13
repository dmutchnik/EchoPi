import requests

URL_READ_COMMANDS = "https://ntfy.sh/newCommandFromEchoPi/raw"

def listen_to_stream():
    """
    Listen to a stream of messages from the ntfy.sh service.
    Manage the calls to the api.
    """
    resp = requests.get(URL_READ_COMMANDS, stream=True)
    latest_message = None
    for line in resp.iter_lines():
        if line:
            # Code that checks the message and calls the api 
            line_decoded = line.decode()
            match line_decoded:
                case "play":
                    if latest_message != "play":
                        print("[Message] Play command received")
                        latest_message = "play"
                case "pause":
                    if latest_message != "pause":
                        print("[Message] Pause command received")
                        latest_message = "pause"
                case "next":
                    if latest_message != "next":
                        print("[Message] Next command received")
                        latest_message = "next"
                case "previous":
                    if latest_message != "previous":
                        print("[Message] Previous command received")
                        latest_message = "previous"
                case _:
                    print(f"[Message] Unknown command: {line_decoded}")

if __name__ == "__main__":
    listen_to_stream()