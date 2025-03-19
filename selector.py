import requests
import random
import re

def get_steamid_from_url(url):
    if url.endswith('/'):
        url = url[:-1]
    
    match = re.search(r'steamcommunity\.com/(id|profiles)/([^/]+)', url)
    if match:
        return match.group(2)
    
    match = re.search(r'store\.steampowered\.com/wishlist/id/([^/]+)', url)
    if match:
        return match.group(1)
    
    return None

def resolve_vanity_url(username):
    # ⚠️ Set your Steam API key here! Get it from: https://steamcommunity.com/dev/apikey
    api_key = "" 

    if not api_key:
        print("❌ Error: Steam API key is missing! Please set it in the code.")
        return None

    url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={api_key}&vanityurl={username}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('response', {}).get('success') == 1:
            return data['response']['steamid']
    
    return None

def fetch_wishlist(steamid):
    url = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?steamid={steamid}"
    response = requests.get(url)

    if response.status_code == 200:
        wishlist_data = response.json()
        return wishlist_data.get("response", {}).get("items", [])

    return []

def get_game_info(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get(str(appid), {}).get("success"):
            return data[str(appid)]["data"]["name"]

    return "Unknown Game"

def choose_random_game(games):
    return random.choice(games) if games else None

def main():
    profile_url = input("Enter your Steam Profile URL or Wishlist URL: ").strip()
    steamid = get_steamid_from_url(profile_url)

    if not steamid:
        print("❌ Invalid Steam Profile or Wishlist URL.")
        return

    if not steamid.isdigit():
        print("🔄 Resolving SteamID64...")
        steamid = resolve_vanity_url(steamid)
        if not steamid:
            print("❌ Failed to resolve SteamID64.")
            return

    print(f"📡 Fetching wishlist for SteamID: {steamid}...")
    games = fetch_wishlist(steamid)

    if games:
        random_game = choose_random_game(games)
        appid = random_game["appid"]
        game_name = get_game_info(appid)
        game_url = f"https://store.steampowered.com/app/{appid}/"

        print(f"🎮 Random game from your wishlist: {game_name} (AppID: {appid})")
        print(f"🔗 Steam Store URL: {game_url}")
    else:
        print("❌ No games found in your wishlist. Is your wishlist public?")

if __name__ == "__main__":
    main()
