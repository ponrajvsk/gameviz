import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

player_name = "Virat Kohli"
search_url = f"https://search.espncricinfo.com/ci/content/site/search.html?search={player_name.replace(' ', '+')}"

response = requests.get(search_url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find player profile links
    player_links = soup.find_all("a", href=True)

    for link in player_links:
        if "/player/" in link["href"]:
            full_profile_url = f"https://www.espncricinfo.com{link['href']}"
            print(f"Profile URL: {full_profile_url}")
            break  # Get the first result
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
