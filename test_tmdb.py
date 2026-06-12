import requests

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://api.themoviedb.org/3/movie/550?api_key=8b6e9b0f80c1340d69cab7c761dadf27"

try:
    r = requests.get(url, headers=headers, timeout=30)
    print("Status:", r.status_code)
    print(r.text[:200])
except Exception as e:
    print("Error:", e)