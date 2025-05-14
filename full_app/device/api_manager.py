import requests

TOPIC = "newCommandFromEchoPi"

def send_message(msg = ""):
    url = f"https://ntfy.sh/{TOPIC}"
    resp = requests.post(url, data=msg)
    if not(200 > resp.status_code >= 300): 
        print(f"Failed to send message: {resp.status_code} - {resp.text}")


