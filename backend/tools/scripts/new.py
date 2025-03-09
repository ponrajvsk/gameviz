import requests

player_id = 253802  # Replace with player ID from Cricsheet
url = f"https://hsapi.espncricinfo.com/v1/pages/player/stats?playerId={player_id}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Failed to fetch data. HTTP {response.status_code}")
