import requests
import threading
from time import sleep

def listen_to_stream():
    resp = requests.get("https://ntfy.sh/avaiableAstrak/raw", stream=True)
    for line in resp.iter_lines():
        if line:
            print("\n[Message]", line.decode())  # Decode bytes to str

# Start the stream listener in a separate thread
thread = threading.Thread(target=listen_to_stream, daemon=True)
thread.start()
counter = 0
# Continue doing other tasks
while True:
    sleep(1)  # Simulate doing other work
    print(f"Number: {counter}")
    counter += 1


